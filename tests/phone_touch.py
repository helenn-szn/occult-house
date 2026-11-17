import asyncio, time, math
from playwright.async_api import async_playwright
import os
URL = os.environ.get('GAME_URL', 'http://127.0.0.1:8000/index.html')
LOG = open('phone.log', 'w')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': 844, 'height': 390}, is_mobile=True, has_touch=True, device_scale_factor=1,
                                  user_agent='Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36')
        pg = await ctx.new_page(); pg.set_default_timeout(300000); E = pg.evaluate; errs = []
        pg.on('pageerror', lambda e: errs.append(str(e) + ' ' + str(e.stack)[:300]))
        cdp = await ctx.new_cdp_session(pg)
        async def wait(js, secs=180):
            t = time.time()
            while time.time() - t < secs:
                if await E(js): return True
                await asyncio.sleep(.6)
            return False
        async def touch(kind, pts):
            await cdp.send('Input.dispatchTouchEvent', {'type': kind, 'touchPoints': [{'x': x, 'y': y, 'id': i} for i, (x, y) in pts]})
        await pg.goto(URL); await wait('window.__t&&__t.ready()', 300)
        log('touch mode:', await E("document.body.classList.contains('touch')"))
        await pg.screenshot(path='p0_title.png')
        await E("__t.go()"); await asyncio.sleep(2); await pg.screenshot(path='p1_help.png')
        await E("__t.closeHelp()"); await wait("__t.INTRO.on", 30); await E("__t.skip()"); await wait("__t.INTRO.done", 90); await asyncio.sleep(3)
        await pg.screenshot(path='p2_hall.png')
        # joystick: drag up on the left
        p0 = await E("__t.pos()")
        await touch('touchStart', [(0, (110, 300))]); await asyncio.sleep(.3)
        for k in range(1, 6):
            await touch('touchMove', [(0, (110, 300 - k * 12))]); await asyncio.sleep(.2)
        await asyncio.sleep(6); await pg.screenshot(path='p3_stick.png')
        await touch('touchEnd', [])
        p1 = await E("__t.pos()")
        log('joystick moved', round(math.hypot(p1[0] - p0[0], p1[1] - p0[1]), 2), 'm')
        # tap the floor ahead to walk
        await E(f"__t.set(-1.2,0.1,{-math.pi/2},-0.25)"); await asyncio.sleep(2)
        await touch('touchStart', [(1, (560, 330))]); await asyncio.sleep(.08); await touch('touchEnd', [])
        await asyncio.sleep(1)
        log('tap-to-walk path:', await E("JSON.stringify(__t.WALK.path.map(p=>p.map(v=>+v.toFixed(2))))"))
        await wait("!__t.WALK.path.length", 60); log('after tap walk pos', await E("__t.pos().map(v=>+v.toFixed(2))"))
        # the Doll Room countdown at phone size
        await E("__t.KEY.have.clock=true;__t.travel('doll')"); await wait("__t.room()==='doll'&&!__t.sw()", 90)
        await E("__t.INTRO_SEEN.doll=true;__t.SEEK.t=99"); await wait("__t.SEEK.state==='hunt'", 120)
        await E("__t.SEEK.t=52"); await asyncio.sleep(3); await pg.screenshot(path='p4_timer.png')
        # Chinese at phone size
        await E("__t.setLang(true)"); await asyncio.sleep(3); await pg.screenshot(path='p5_zh.png')
        await E("__t.setLang(false)")
        # death screen
        await E("__t.gameOver('doll','Button found you first. The dolls have a new friend to play with, for ever.')")
        await wait("document.getElementById('gameover').style.display==='flex'", 120); await asyncio.sleep(1); await pg.screenshot(path='p6_dead.png')
        await E("document.getElementById('goRetry').click()"); log('retry ok', await wait("!__t.QS.go&&!__t.sw()", 90))
        # ending + Marigold keepsake
        await E("for(const k of ['doll','cards','study','gallery','knock'])__t.KEY.have[k]=true;__t.travel('hall')"); await wait("__t.room()==='hall'&&!__t.sw()", 90)
        await E("__t.startEnding()"); await wait("document.getElementById('ending').style.display==='flex'", 240)
        await E("localStorage.setItem('occultHouseKept',JSON.stringify(__t.KS().filter(k=>k.id!=='marigold').map(k=>k.id)))")
        await E("document.getElementById('keepOpen').click()")
        ok = await wait("document.getElementById('keepOut').style.display==='block'", 400, )
        log('marigold keepsake', ok, await E("document.getElementById('keepName').textContent"), await E("document.getElementById('keepCount').textContent"))
        await E("document.getElementById('keepImg').scrollIntoView()"); await asyncio.sleep(1); await pg.screenshot(path='p7_end.png')
        log('errors:', errs)
        await b.close()
asyncio.run(main())
