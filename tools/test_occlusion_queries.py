import asyncio,json
from playwright.async_api import async_playwright
JS=r"""
async()=>{const cv=document.createElement('canvas');cv.width=320;cv.height=240;const gl=cv.getContext('webgl2');
const sh=(t,src)=>{const o=gl.createShader(t);gl.shaderSource(o,src);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(o);return o};
const prog=(v,f)=>{const p=gl.createProgram();gl.attachShader(p,sh(gl.VERTEX_SHADER,v));gl.attachShader(p,sh(gl.FRAGMENT_SHADER,f));gl.bindAttribLocation(p,0,'c');gl.linkProgram(p);return p};
// the game's query program, verbatim
const P=prog('#version 300 es\nin vec3 c;uniform mat4 vp;uniform vec3 lo,hi;void main(){gl_Position=vp*vec4(mix(lo,hi,c),1.);}','#version 300 es\nprecision lowp float;out vec4 o;void main(){o=vec4(0.);}');
const vao=gl.createVertexArray();gl.bindVertexArray(vao);const vb=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,vb);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([0,0,0,1,0,0,1,1,0,0,1,0,0,0,1,1,0,1,1,1,1,0,1,1]),gl.STATIC_DRAW);
gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,3,gl.FLOAT,false,0,0);const ib=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib);
gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint8Array([0,1,2,0,2,3,4,6,5,4,7,6,0,4,5,0,5,1,1,5,6,1,6,2,2,6,7,2,7,3,3,7,4,3,4,0]),gl.STATIC_DRAW);
// perspective camera at origin looking down -z
const f=1/Math.tan(.6),n=.05,F=300,a=320/240;const vp=new Float32Array([f/a,0,0,0, 0,f,0,0, 0,0,(F+n)/(n-F),-1, 0,0,2*F*n/(n-F),0]);
const uVP=gl.getUniformLocation(P,'vp'),uLo=gl.getUniformLocation(P,'lo'),uHi=gl.getUniformLocation(P,'hi');gl.useProgram(P);gl.uniformMatrix4fv(uVP,false,vp);
gl.viewport(0,0,320,240);gl.clearDepth(1);gl.clear(gl.DEPTH_BUFFER_BIT|gl.COLOR_BUFFER_BIT);gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.disable(gl.CULL_FACE);
// scene: a solid wall 2 m wide 2 m tall at 5 m (writes depth); a "glass" pane at 3 m to the right that doesn't write depth
const box=(lo,hi)=>{gl.uniform3f(uLo,...lo);gl.uniform3f(uHi,...hi);gl.drawElements(gl.TRIANGLES,36,gl.UNSIGNED_BYTE,0)};
gl.depthMask(true);box([-1,-1,-5.1],[1,1,-5]);gl.depthMask(false);box([1.5,-1,-3.1],[3.5,1,-3]);
// the game's test pass: no colour, no depth writes, LEQUAL, inflated by .35
gl.colorMask(false,false,false,false);const Pd=.35,cases={behind_wall:[[-.4,-.4,-12],[.4,.4,-11]],partly_behind_wall:[[.5,-.4,-12],[2,.4,-11]],behind_glass:[[2,-.4,-12],[3,.4,-11]],in_front_of_wall:[[-.3,-.3,-4],[.3,.3,-3.5]],behind_camera:[[-1,-1,2],[1,1,3]]};
const qs={};for(const[k,[lo,hi]]of Object.entries(cases)){const q=gl.createQuery();gl.beginQuery(gl.ANY_SAMPLES_PASSED_CONSERVATIVE,q);box(lo.map(v=>v-Pd),hi.map(v=>v+Pd));gl.endQuery(gl.ANY_SAMPLES_PASSED_CONSERVATIVE);qs[k]=q}
gl.finish();await new Promise(r=>setTimeout(r,200));const out={};for(const[k,q]of Object.entries(qs))out[k]={available:gl.getQueryParameter(q,gl.QUERY_RESULT_AVAILABLE),visible:!!gl.getQueryParameter(q,gl.QUERY_RESULT)};return out}
"""
async def main():
  async with async_playwright() as pw:
    b=await pw.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);pg=await b.new_page()
    print(json.dumps(await pg.evaluate(JS),indent=1));await b.close()
asyncio.run(main())
