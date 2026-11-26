# Shading LOD benchmark: a ground plane seen from head height out to the horizon (most pixels are far away, as in the game),
# old shading (full quality everywhere) vs distance-adaptive shading. Same work items as the game's block shader: ray-traced sun
# (3D texture walk), ray-traced AO (4 short walks), shadow-map taps, 12 dynamic lights with a visibility-map read each
import asyncio,json
from playwright.async_api import async_playwright
JS=r"""
async()=>{
const W=1024,H=640,cv=document.createElement('canvas');cv.width=W;cv.height=H;const gl=cv.getContext('webgl2');const out={};
const mk=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};
const prog=fs=>{const p=gl.createProgram();gl.attachShader(p,mk(gl.VERTEX_SHADER,`#version 300 es
in vec2 p;out vec2 uv;void main(){uv=p*.5+.5;gl_Position=vec4(p,0,1);}`));gl.attachShader(p,mk(gl.FRAGMENT_SHADER,fs));gl.linkProgram(p);return p};
const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
const t3=gl.createTexture();gl.bindTexture(gl.TEXTURE_3D,t3);const N=64,v=new Uint8Array(N*N*N);for(let i=0;i<v.length;i++)v[i]=(i*2654435761>>>28)===0?255:0;
gl.texImage3D(gl.TEXTURE_3D,0,gl.R8,N,N,N,0,gl.RED,gl.UNSIGNED_BYTE,v);gl.texParameteri(gl.TEXTURE_3D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_3D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
const t2=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t2);const m=new Uint8Array(512*512*4);for(let i=0;i<m.length;i++)m[i]=(i*40503)&255;gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,512,512,0,gl.RGBA,gl.UNSIGNED_BYTE,m);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);
const COMMON=`#version 300 es
precision highp float;in vec2 uv;out vec4 o;uniform highp sampler3D vox;uniform sampler2D sm;uniform vec4 L[12];
float walk(vec3 p,vec3 d,int n){vec3 c=floor(p);for(int i=0;i<64;i++){if(i>=n)break;c+=sign(d)*step(abs(d.yzx),abs(d))*step(abs(d.zxy),abs(d));if(texelFetch(vox,ivec3(mod(c,64.)),0).r>.5)return 0.;}return 1.;}
float tap(vec3 q){return step(.3,texture(sm,fract(q.xz*.05)).r);}
vec3 world(){float y=uv.y*.6-.45;if(y>=-.002)y=-.002;float t=1.6/-y;return vec3((uv.x-.5)*t*1.4,0.,t);} // ground under a camera at 1.6 m
float lights(vec3 P){float a=0.;for(int i=0;i<12;i++){vec3 v=P-L[i].xyz;float d=length(v);if(d>L[i].w)continue;float hd=texture(sm,fract(v.xz/d*.5+.5)).g*L[i].w;if(d>hd+.3)continue;float t=floor(sqrt(d/L[i].w)*8.)*.125;a+=1.-t*t*(.4+.6*t);}return a;}`;
const OLD=COMMON+`
void main(){vec3 P=world(),q=(floor(P*16.)+.5)/16.;float s=tap(q)*tap(q+.01)*tap(q-.01)*tap(q+vec3(.01,0,-.01))*tap(q+vec3(-.01,0,.01));
 s*=walk(q*2.,normalize(vec3(.4,.8,.3)),56);float ao=0.;for(int k=0;k<4;k++)ao+=walk(q*2.,normalize(vec3(k<2?1.:-1.,1.,k%2==0?1.:-1.)),3);
 o=vec4(vec3(s*.6+ao*.05+lights(q)*.1),1.);}`;
const NEW=COMMON+`
float shL(vec3 P){float d=max(length(P)-6.,0.)/22.;return min(d*sqrt(d),6.95);}
vec3 shQ(vec3 P,float lv){float g=16./exp2(lv);return(floor(P*g)+.5)/g;}
float lev(vec3 P,float lv){vec3 q=shQ(P,lv);if(lv>2.5){if(lv>4.5)return tap(q);float h=exp2(lv)/64.;return(tap(q+vec3(h,0,h))+tap(q-vec3(h,0,h))+tap(q+vec3(h,0,-h))+tap(q-vec3(h,0,-h)))*.25;}
 float s=tap(q);if(lv<.5)s*=tap(q+.01)*tap(q-.01)*tap(q+vec3(.01,0,-.01))*tap(q+vec3(-.01,0,.01));return s*walk(q*2.,normalize(vec3(.4,.8,.3)),int(56.*max(.35,1.-lv*.25)));}
void main(){vec3 P=world();float Lv=shL(P),lf=floor(Lv),b=lf<6.?smoothstep(.7,1.,Lv-lf):0.;float s=lev(P,lf);if(b>0.)s=mix(s,lev(P,lf+1.),b);
 float ao=0.,k=1.-smoothstep(1.,2.,Lv);if(k>0.)for(int j=0;j<4;j++)ao+=walk(P*2.,normalize(vec3(j<2?1.:-1.,1.,j%2==0?1.:-1.)),3)*k;
 vec3 P0=lf<.5?(floor(P*16.)+.5)/16.:shQ(P,lf);float li=lights(P0);if(b>0.)li=mix(li,lights(shQ(P,lf+1.)),b);
 o=vec4(vec3(s*.6+ao*.05+li*.1),1.);}`;
const Ls=[];for(let i=0;i<12;i++)Ls.push(Math.random()*40-20,0,Math.random()*120,8+Math.random()*20);
const run=(fs)=>{const p=prog(fs);gl.useProgram(p);const l=gl.getAttribLocation(p,'p');gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0);
  gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_3D,t3);gl.uniform1i(gl.getUniformLocation(p,'vox'),0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,t2);gl.uniform1i(gl.getUniformLocation(p,'sm'),1);gl.uniform4fv(gl.getUniformLocation(p,'L'),Ls);
  const px=new Uint8Array(4);gl.drawArrays(gl.TRIANGLE_STRIP,0,4);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);const t0=performance.now();for(let i=0;i<20;i++)gl.drawArrays(gl.TRIANGLE_STRIP,0,4);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);return(performance.now()-t0)/20};
out.full_quality_ms=run(OLD);out.adaptive_ms=run(NEW);
const nol=s=>s.replace('lights(q)*.1','0.').replace('float li=lights(P0);if(b>0.)li=mix(li,lights(shQ(P,lf+1.)),b);','float li=0.;');
out.no_lights_full=run(nol(OLD));out.no_lights_adaptive=run(nol(NEW));
const empty=COMMON+'void main(){o=vec4(world(),1.);}';out.empty_shader=run(empty);
const onlyL=COMMON+'void main(){vec3 P=world();o=vec4(lights((floor(P*16.)+.5)/16.));}';out.lights_only=run(onlyL);return out}
"""
async def main():
  async with async_playwright() as pw:
    b=await pw.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);pg=await b.new_page()
    print(json.dumps(await pg.evaluate(JS),indent=1));await b.close()
asyncio.run(main())
