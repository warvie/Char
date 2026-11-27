import asyncio,subprocess
from playwright.async_api import async_playwright
STUB=open('/tmp/t/three_stub.js').read()+";THREE.Sprite=THREE.Mesh;THREE.SpriteMaterial=function(){return{}};"
async def main():
    srv=subprocess.Popen(['python3','-m','http.server','8768','-d','/tmp/t/srv'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);await asyncio.sleep(1)
    try:
      async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        ctx=await b.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True);pg=await ctx.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.route('**/three.min.js',lambda r:r.fulfill(body=STUB,content_type='application/javascript'))
        await pg.route('https://fonts.googleapis.com/**',lambda r:r.fulfill(body='',content_type='text/css'))
        await pg.goto('http://localhost:8768/index.html');await asyncio.sleep(2);await pg.tap('#bSolo');await asyncio.sleep(3)
        await pg.evaluate("(()=>{const s=document.querySelector('#devSel');s.value='1';s.dispatchEvent(new Event('change'))})()");await asyncio.sleep(1)
        st=lambda: pg.evaluate("(()=>{const h=document.querySelector('#devHud'),r=h.getBoundingClientRect(),t=document.querySelector('#devTxt');return [h.className,Math.round(r.width),Math.round(r.height),t.textContent.length,getComputedStyle(t).display]})()")
        print('open',await st());print(await pg.evaluate("""(()=>{const b=document.querySelector('#devMin').getBoundingClientRect();const e=document.elementFromPoint(b.x+b.width/2,b.y+b.height/2);let p=document.querySelector('#devHud'),ch=[];while(p){ch.push(p.tagName+'#'+p.id+' z'+getComputedStyle(p).zIndex+' pe'+getComputedStyle(p).pointerEvents);p=p.parentElement}return [b.x,b.y,e&&(e.tagName+'#'+e.id),ch]})()"""))
        bb0=await pg.evaluate("(()=>{const b=document.querySelector('#devMin').getBoundingClientRect();return[b.x+b.width/2,b.y+b.height/2]})()");print('btn at',bb0);await pg.touchscreen.tap(bb0[0],bb0[1]);await asyncio.sleep(.6);print('after tap',await st())
        bb=await pg.evaluate("(()=>{const b=document.querySelector('#devMin').getBoundingClientRect();return[b.x+b.width/2,b.y+b.height/2]})()");print('btn now at',bb);await pg.touchscreen.tap(bb[0],bb[1]);await asyncio.sleep(.6);print('after 2nd tap',await st())
        print(errs[:3]);await b.close()
    finally: srv.terminate()
asyncio.run(main())
