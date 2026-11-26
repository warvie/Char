# Benchmark: lighting computed in the fragment shader on the texture pixel (current) vs baked into a light texture on the CPU
import asyncio,json
from playwright.async_api import async_playwright
JS=r"""
async()=>{
const W=1024,H=768,cv=document.createElement('canvas');cv.width=W;cv.height=H;document.body.appendChild(cv);
const gl=cv.getContext('webgl2');const out={};
function prog(vs,fs){const mk=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};const p=gl.createProgram();gl.attachShader(p,mk(gl.VERTEX_SHADER,vs));gl.attachShader(p,mk(gl.FRAGMENT_SHADER,fs));gl.linkProgram(p);return p}
// scene: a wall of 64x48 block faces (16x16 texels each) filling the screen, world position = face grid in metres
const VS=`#version 300 es
in vec2 p;out vec2 uv;out vec3 wp;void main(){uv=p*.5+.5;wp=vec3(uv.x*32.,uv.y*24.,0.);gl_Position=vec4(p,0,1);}`;
const buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);
// albedo texture 1024x768 (16 texels per 0.5 m face)
const alb=new Uint8Array(W*H*4);for(let i=0;i<alb.length;i++)alb[i]=(i*2654435761>>>24)&255;
const tex=(d,w,h)=>{const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,w,h,0,gl.RGBA,gl.UNSIGNED_BYTE,d);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);return t};
const tA=tex(alb,W,H),occ=new Uint8Array(384*288*4).fill(255),tO=tex(occ,384,288);
const L=[];for(let i=0;i<12;i++)L.push([Math.random()*32,Math.random()*24,1+Math.random()*3,8+Math.random()*20]);
const LG=`uniform vec4 dlP[12];uniform sampler2D occ;
float band(float d,float r){float t=floor(sqrt(d/r)*8.)*.125;return t>=1.?0.:1.-t*t*(.4+.6*t);}
vec2 oct(vec3 d){d/=abs(d.x)+abs(d.y)+abs(d.z);vec2 q=d.xz;if(d.y<0.)q=(1.-abs(q.yx))*vec2(q.x>=0.?1.:-1.,q.y>=0.?1.:-1.);return q*.5+.5;}`;
const FA=`#version 300 es
precision highp float;in vec2 uv;in vec3 wp;out vec4 o;uniform sampler2D alb;${LG}
void main(){vec3 Pq=(floor(wp*16.)+.5)/16.;vec3 c=texture(alb,uv).rgb,a=vec3(.05);
 for(int i=0;i<12;i++){vec3 v=Pq-dlP[i].xyz;float d=length(v);if(d>dlP[i].w)continue;vec2 t=clamp(floor(oct(v/d)*96.),0.,95.);float hd=texture(occ,(vec2(mod(float(i),4.),floor(float(i)/4.))*96.+t+.5)/vec2(384.,288.)).r*dlP[i].w;
  if(d>hd+.3)continue;a+=vec3(.42)*band(d,dlP[i].w);}o=vec4(c*a,1);}`;
const FB=`#version 300 es
precision highp float;in vec2 uv;in vec3 wp;out vec4 o;uniform sampler2D alb,lmap;void main(){o=vec4(texture(alb,uv).rgb*(vec3(.05)+texture(lmap,uv).rgb*4.),1);}`;
const pA=prog(VS,FA),pB=prog(VS,FB);
const draw=(p,setup)=>{gl.useProgram(p);const l=gl.getAttribLocation(p,'p');gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.enableVertexAttribArray(l);gl.vertexAttribPointer(l,2,gl.FLOAT,false,0,0);setup();gl.drawArrays(gl.TRIANGLE_STRIP,0,4)};
const frames=(n,f)=>{f();gl.finish();const t0=performance.now();for(let i=0;i<n;i++)f();const px=new Uint8Array(4);gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);return(performance.now()-t0)/n};
const setA=()=>{gl.uniform4fv(gl.getUniformLocation(pA,'dlP'),L.flat());gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tA);gl.uniform1i(gl.getUniformLocation(pA,'alb'),0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,tO);gl.uniform1i(gl.getUniformLocation(pA,'occ'),1)};
out.shader_ms_per_frame=frames(60,()=>draw(pA,setA));
const FO=FA.replace('a+=vec3(.42)*band(d,dlP[i].w);','float x=d/dlP[i].w,win=clamp(1.-x*x*x*x,0.,1.);a+=vec3(1.)*win*win/(1.+d*d*.35);');const pO=prog(VS,FO);
const setO=()=>{gl.uniform4fv(gl.getUniformLocation(pO,'dlP'),L.flat());gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tA);gl.uniform1i(gl.getUniformLocation(pO,'alb'),0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,tO);gl.uniform1i(gl.getUniformLocation(pO,'occ'),1)};
out.shader_old_smooth_falloff_ms=frames(60,()=>draw(pO,setO));
const F6=FA.replace('for(int i=0;i<12;i++){','for(int i=0;i<12;i++){if(i>=6)break;');const p6=prog(VS,F6);
const set6=()=>{gl.uniform4fv(gl.getUniformLocation(p6,'dlP'),L.flat());gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tA);gl.uniform1i(gl.getUniformLocation(p6,'alb'),0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,tO);gl.uniform1i(gl.getUniformLocation(p6,'occ'),1)};
out.shader_6_lights_after_culling_ms=frames(60,()=>draw(p6,set6));
// baked: CPU computes the light of every texel (same banding and occlusion lookup), uploads it, shader just samples it
const lm=new Uint8Array(W*H*4),tL=tex(lm,W,H);
const band=(d,r)=>{const x=Math.min(1,d/r),k=Math.floor(Math.sqrt(x)*8);return k>=8?0:1-Math.pow(k/8,2.6)};
const bake=()=>{for(let y=0;y<H;y++)for(let x=0;x<W;x++){const px=(x+.5)/32,py=(y+.5)/32;let a=0;for(const l of L){const dx=px-l[0],dy=py-l[1],dz=-l[2],d=Math.hypot(dx,dy,dz);if(d>l[3])continue;const s=Math.abs(dx)+Math.abs(dy)+Math.abs(dz),u=dx/s,v=dz/s;const hd=occ[((Math.min(95,(v*.5+.5)*96|0))*384+Math.min(95,(u*.5+.5)*96|0))*4]/255*l[3];if(d>hd+.3)continue;a+=.42*band(d,l[3])}
  const o=(y*W+x)*4,q=Math.min(255,a*64);lm[o]=lm[o+1]=lm[o+2]=q;lm[o+3]=255}
 gl.bindTexture(gl.TEXTURE_2D,tL);gl.texSubImage2D(gl.TEXTURE_2D,0,0,0,W,H,gl.RGBA,gl.UNSIGNED_BYTE,lm)};
let t0=performance.now();for(let i=0;i<1;i++)bake();gl.finish();out.bake_ms_per_light_change=(performance.now()-t0)/1;
const setB=()=>{gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,tA);gl.uniform1i(gl.getUniformLocation(pB,'alb'),0);gl.activeTexture(gl.TEXTURE1);gl.bindTexture(gl.TEXTURE_2D,tL);gl.uniform1i(gl.getUniformLocation(pB,'lmap'),1)};
out.baked_render_ms_per_frame=frames(60,()=>draw(pB,setB));
// a light moving every frame (flashlight, headlights): baked must re-bake each frame
out.baked_with_moving_light_ms_per_frame=out.baked_render_ms_per_frame+out.bake_ms_per_light_change;
return out}
"""
async def main():
  async with async_playwright() as pw:
    b=await pw.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);pg=await b.new_page()
    r=await pg.evaluate(JS);print(json.dumps(r,indent=1));await b.close()
asyncio.run(main())
