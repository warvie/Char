import asyncio,json
from playwright.async_api import async_playwright
JS=r"""
async()=>{const W=800,H=500,cv=document.createElement('canvas');cv.width=W;cv.height=H;const gl=cv.getContext('webgl2',{antialias:false});
const mk=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(x);return x};
const prog=fs=>{const p=gl.createProgram();gl.attachShader(p,mk(gl.VERTEX_SHADER,'#version 300 es\nin vec2 p;uniform float z;out vec2 uv;void main(){uv=p;gl_Position=vec4(p,z,1);}'));gl.attachShader(p,mk(gl.FRAGMENT_SHADER,fs));gl.linkProgram(p);return p};
const heavy=prog(`#version 300 es
precision highp float;in vec2 uv;out vec4 o;uniform vec4 L[12];void main(){vec3 P=vec3(uv*20.,0.),a=vec3(0.);for(int k=0;k<4;k++)for(int i=0;i<12;i++){vec3 v=P-L[i].xyz;float d=length(v)+float(k);float t=floor(sqrt(d/L[i].w)*8.)*.125;a+=vec3(1.-t*t)*.01*sin(d);}o=vec4(a,1);}`);
const cheap=prog('#version 300 es\nprecision lowp float;out vec4 o;void main(){o=vec4(0);}');
const b=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,b);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
const Ls=[];for(let i=0;i<12;i++)Ls.push(Math.random()*20-10,Math.random()*20-10,0,20);
const layers=[.8,.6,.4,.2,0,-.2];// drawn back to front: worst case, every layer shaded
const draw=(p,z)=>{gl.useProgram(p);gl.uniform1f(gl.getUniformLocation(p,'z'),z);if(p===heavy)gl.uniform4fv(gl.getUniformLocation(p,'L'),Ls);gl.drawArrays(gl.TRIANGLE_STRIP,0,4)};
gl.enable(gl.DEPTH_TEST);const px=new Uint8Array(4);
const run=(pre)=>{const t0=performance.now();for(let f=0;f<10;f++){gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  if(pre){gl.colorMask(false,false,false,false);gl.depthFunc(gl.LESS);for(const z of layers)draw(cheap,z);gl.colorMask(true,true,true,true);gl.depthFunc(gl.LEQUAL);}else gl.depthFunc(gl.LESS);
  for(const z of layers)draw(heavy,z)}gl.readPixels(0,0,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px);return(performance.now()-t0)/10};
run(false);return{no_prepass_ms:run(false),with_prepass_ms:run(true),no_prepass_ms_again:run(false),with_prepass_ms_again:run(true)}}
"""
async def main():
  async with async_playwright() as pw:
    b=await pw.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);pg=await b.new_page()
    print(json.dumps(await pg.evaluate(JS),indent=1));await b.close()
asyncio.run(main())
