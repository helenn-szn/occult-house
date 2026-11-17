import asyncio, math, sys, time, json
from playwright.async_api import async_playwright
import os
URL = os.environ.get('GAME_URL', 'http://127.0.0.1:8000/index.html')

LOG = open('e2e5.log', 'w')
RESULTS = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail)); log(('PASS ' if ok else 'FAIL ') + name + (' :: ' + str(detail) if detail else ''))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'])
        pg = await b.new_page(viewport={'width': 420, 'height': 260})
        errs = []
        pg.on('pageerror', lambda e: errs.append('PAGEERROR ' + str(e)))
        pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
        pg.on('requestfailed', lambda r: errs.append('REQFAIL ' + r.url) if 'fonts.g' not in r.url else None)
        pg.set_default_timeout(240000)
        E = pg.evaluate
        async def wait(js, secs=120, step=0.7):
            t = time.time()
            while time.time() - t < secs:
                try:
                    if await E(js): return True
                except Exception as ex:
                    log('  wait err', ex)
                await asyncio.sleep(step)
            return False
        async def stand(x, z, tx=None, tz=None, yaw=None):
            if yaw is None: yaw = math.atan2(-(tx - x), -(tz - z))
            await E(f"__t.set({x},{z},{yaw},-0.05)")
            await asyncio.sleep(0.8)
        async def label():
            return await E("(()=>{const c=__t.find();return c?c.label:null})()")
        async def press(code='KeyE'):
            await E(f"dispatchEvent(new KeyboardEvent('keydown',{{code:'{code}'}}));dispatchEvent(new KeyboardEvent('keyup',{{code:'{code}'}}))")
        async def ready_idle(secs=90):
            return await wait("!__t.sw()&&__t.E.phase==='idle'&&!__t.CAM.seq", secs)
        async def go_door(to):
            room = await E("__t.room()")
            d = await E(f"__t.ROOMS['{room}'].doors.find(d=>d.to==='{to}')")
            if not d:
                check(f'door {room}->{to} exists', False); return False
            px, pz = d['p']
            rects = await E(f"__t.ROOMS['{room}'].rects")
            # nearest standable point to the door, inside the room
            best = None
            for r in rects:
                cx = min(max(px, r['x0']), r['x1']); cz = min(max(pz, r['z0']), r['z1'])
                dd = math.hypot(cx - px, cz - pz)
                if best is None or dd < best[0]: best = (dd, cx, cz)
            _, sx, sz = best
            await stand(sx, sz, px + 0.001, pz + 0.3) if (sx, sz) == (px, pz) else await stand(sx, sz, px, pz)
            await ready_idle()
            lb = await label()
            await press()
            ok = await wait(f"__t.room()==='{to}'&&!__t.sw()", 120)
            check(f'walk through door {room} -> {to}', ok, f'prompt was "{lb}"')
            await asyncio.sleep(1.5)
            return ok
        async def use_spot(label_part, x, z, tx, tz):
            await stand(x, z, tx, tz)
            lb = await label()
            ok = lb is not None and label_part.lower() in lb.lower()
            check(f'prompt "{label_part}"', ok, f'got "{lb}"')
            if ok: await press()
            return ok
        async def solve_case_step(cid):
            st = await E(f"(()=>{{const c=__t.CASES.find(c=>c.id==='{cid}'),st=__t.INV.cases['{cid}'];return {{step:st.step,phase:st.phase,s:c.steps[st.step]}}}})()")
            s = st['s']; room = await E("__t.room()")
            if s['room'] != room:
                check(f'case {cid} step {st["step"]} in {room}', False, f'expected room {s["room"]}'); return False
            okg = await wait(f"__t.INV.cases['{cid}'].phase==='ghost'||__t.INV.cases['{cid}'].phase==='leave'||__t.INV.cases['{cid}'].phase==='clue'", 120)
            gx, gz = s['ghost']
            # stand a little way from the ghost, inside the room, and look at it
            rects = await E(f"__t.ROOMS['{room}'].rects")
            cands = []
            for r in rects:
                for fx in [0.25, 0.5, 0.75]:
                    for fz in [0.25, 0.5, 0.75]:
                        x = r['x0'] + (r['x1'] - r['x0']) * fx; z = r['z0'] + (r['z1'] - r['z0']) * fz
                        d = math.hypot(x - gx, z - gz)
                        if 1.0 < d < 5: cands.append((abs(d - 1.8), x, z))
            cands.sort(); _, x, z = cands[0]
            await stand(x, z, gx, gz)
            okc = await wait(f"__t.INV.cases['{cid}'].phase==='clue'", 150)
            check(f'case {cid} step {st["step"]}: ghost seen and led off', okg and okc, await E(f"__t.INV.cases['{cid}'].phase"))
            if not okc: return False
            cx, cz = s['clue']['p']
            best = None
            for r in rects:
                sx = min(max(cx, r['x0']), r['x1']); sz = min(max(cz, r['z0']), r['z1'])
                dd = math.hypot(sx - cx, sz - cz)
                if best is None or dd < best[0]: best = (dd, sx, sz)
            _, sx, sz = best
            await stand(sx, sz, yaw=0)
            lb = await label()
            await press()
            ok = await wait(f"__t.INV.cases['{cid}'].step>{st['step']}", 20)
            check(f'case {cid} step {st["step"]}: clue examined', ok, f'prompt "{lb}", clue distance {best[0]:.2f}')
            await asyncio.sleep(1)
            return ok

        t0 = time.time()
        await pg.goto(URL)
        ok = await wait("window.__t&&__t.ready()", 300, 1.5)
        check('house loads', ok, f'{time.time()-t0:.0f}s')
        await E("__t.go()"); await asyncio.sleep(2); await E("window.__DT=0.6")
        hp = await E("({open:__t.help(),rows:document.querySelectorAll('#help .hcard').length+1,txt:document.getElementById('help').textContent})")
        check('how to play opens before the welcome, as 6 cards', hp['open'] and hp['rows'] == 7, hp['rows'])
        check('how to play explains three chances and death', 'Three chances' in hp['txt'] and 'die' in hp['txt'])
        check('welcome waits while the page is open', not await E("__t.INTRO.on"))
        await E("__t.closeHelp()")
        ok = await wait("__t.INTRO.on", 30); check('closing it starts the curator welcome', ok)
        await E("__t.skip()"); ok = await wait("__t.INTRO.done", 60); check('welcome finishes', ok)
        await asyncio.sleep(2)
        q = await E("document.getElementById('quest').innerText")
        check('trial panel shows trial 1: the clock, with 3 chances', 'TRIAL 1 OF 6' in q and 'Wind the clock' in q and '●●●' in q, q.replace('\n', ' | '))
        await E("__t.openMap()"); await asyncio.sleep(1.5)
        locks = await E("[...document.querySelectorAll('#mapSvg text')].filter(t=>t.textContent==='🔒').length")
        check('map shows the 5 later rooms locked', locks == 5, locks)
        await E("__t.closeMap()"); await asyncio.sleep(1.5)
        rd = await E("document.getElementById('radarT').innerText")
        check('radar marks locked doors', rd.count('(locked)') >= 4, rd.replace('\n', ' | '))
        # a locked door
        await stand(0.3, -0.78, 0.62, -0.78)
        lb = await label(); await press(); await asyncio.sleep(2)
        check('Doll Room door is locked before the clock', lb and lb.startswith('Locked') and await E("__t.room()") == 'hall', lb)
        await stand(-2.95, 0, -3.4, 0)
        lb = await label(); check('front door shows 0 of 6 keys', lb and '0 of 6' in lb, lb)
        # the clock: let go too soon once (a strike), then wind it
        await stand(-1.25, 0.5, -1.25, 1.2)
        await E("dispatchEvent(new KeyboardEvent('keydown',{code:'KeyE'}))")
        await wait("__t.CLOCK.hold>1.3", 120, 0.3)
        await E("dispatchEvent(new KeyboardEvent('keyup',{code:'KeyE'}))")
        ok = await wait("__t.QS.strikes.hall===1", 40)
        check('letting go of the clock too soon costs a chance', ok, await E("document.getElementById('qC').innerText"))
        await asyncio.sleep(2)
        await E("dispatchEvent(new KeyboardEvent('keydown',{code:'KeyE'}))")
        ok = await wait("__t.CLOCK.done", 240)
        await E("dispatchEvent(new KeyboardEvent('keyup',{code:'KeyE'}))")
        check('wind the clock -> key 1', ok and await E("__t.stage()===1"))
        await asyncio.sleep(2)
        check('Doll Room unlocked, Parlour still locked', await E("__t.roomOpen('doll')&&!__t.roomOpen('parlour')"))
        q = await E("document.getElementById('quest').innerText"); check('panel points to the Doll Room', 'Doll Room' in q, q.replace('\n', ' | '))
        # camera: raise and lower (the one rule)
        await wait("__t.CAM.has", 60); await E("__t.raiseCam()"); await asyncio.sleep(1); await E("__t.raiseCam()")
        check('camera use is noticed', await E("__t.CAM.used"))
        # doll room
        await go_door('doll')
        ok = await wait("__t.SEEK.state==='hunt'", 150); check("Button hides", ok)
        sp = await E("__t.SEEK.spot"); await stand(sp[0] + 0.3, sp[1], sp[0], sp[1]); lb = await label(); await press()
        check('find Button -> key 2', await wait("__t.stage()===2", 15), lb)
        await go_door('hall')
        # parlour: die on purpose, retry, then win
        await go_door('parlour')
        await stand(-1.25, -1.35, -1.25, -1.1); lb = await label(); check("Edgar's chair prompt", lb and 'edgar' in lb.lower(), lb)
        await press()
        check("sitting in Edgar's chair opens his game", await wait("__t.HL.open", 60))
        for i in range(3):
            await E("__t.HL.card=13;__t.hlGuess(true)"); await asyncio.sleep(0.6)
        ok = await wait("document.getElementById('gameover').style.display==='flex'", 60)
        go = await E("({t:document.getElementById('goTitle').textContent,w:document.getElementById('goWhy').textContent,where:document.getElementById('goWhere').textContent})")
        check('three lost hands -> you die (game over)', ok and go['t'] == 'YOU DIED', go)
        await E("document.getElementById('goRetry').click()")
        ok = await wait("!__t.QS.go&&__t.room()==='parlour'&&!__t.sw()", 60)
        check('Try again -> back in the parlour, chances reset, keys kept', ok and await E("(__t.QS.strikes.parlour||0)===0&&__t.HL.losses===0&&__t.stage()===2"))
        await stand(-1.25, -1.35, -1.25, -1.1); await press(); await wait("__t.HL.open", 60)
        for i in range(30):
            if await E("__t.stage()>=3"): break
            if not await E("__t.HL.open"): await E("__t.openHL()")
            r = await E("(()=>{__t.HL.card=1;__t.hlGuess(true);return JSON.stringify({streak:__t.HL.streak,losses:__t.HL.losses,open:__t.HL.open,go:__t.QS.go,sw:__t.sw(),cam:__t.CAM.up,stage:__t.stage()})})()"); log('   guess', r); await asyncio.sleep(0.4)
        check('beat Edgar -> key 3', await E("__t.stage()===3"))
        await go_door('hall')
        # study: one wrong appraisal, then right
        await go_door('study')
        for r in ['mirror', 'bell', 'idol', 'skull', 'ledger']:
            await E(f"__t.examineRelic('{r}')"); await asyncio.sleep(1)
        await E("__t.openLedger()"); await asyncio.sleep(1)
        await E("__t.QUIZ.forEach(Q=>__t.answer(__t.RELICS.find(r=>r.id!==Q.a).id))"); await asyncio.sleep(1)
        check('wrong appraisal costs a chance', await E("__t.QS.strikes.study===1"))
        await E("__t.openLedger()"); await asyncio.sleep(1)
        await E("__t.QUIZ.forEach(Q=>__t.answer(Q.a))")
        check('Appraisal -> key 4', await wait("__t.stage()===4", 60))
        await go_door('hall')
        # gallery
        lb = None
        await stand(-2.35, -0.95, -2.35, -1.15); lb = await label(); await press()
        check('stairs open now -> Portrait Gallery', await wait("__t.room()==='gallery'&&!__t.sw()", 90), lb)
        for i in range(3):
            await stand(2.0, 0, yaw=-math.pi / 2)
            ok = await wait("!!__t.SIT.pending", 150); pend = await E("__t.SIT.pending")
            if ok: await E(f"__t.examinePortrait('{pend}')"); await asyncio.sleep(1.5)
        check('The Sitting -> key 5', await wait("__t.stage()===5", 60))
        await go_door('hall')
        # passage: knock, then the lift trap
        await go_door('passage')
        await stand(-3.4, 0.0, -4.2, 0.0); lb = await label(); await press()
        check('knock prompt straight away', lb == 'Knock on door II', lb)
        ok = await wait("__t.KNOCK.state==='answer'", 40); pat = await E("__t.KNOCK.pat")
        for n in pat:
            await E(f"for(let i=0;i<{n};i++)__t.knockTap()"); await asyncio.sleep(1.4)
        check(f'knock back {pat} -> key 6', await wait("__t.stage()===6", 30))
        q = await E("document.getElementById('quest').innerText"); check('panel: every trial passed, leave the house', 'Leave the house' in q, q.replace('\n', ' | '))
        await stand(-0.25, -1.1, -0.25, -1.45); lb = await label(); await press(); await asyncio.sleep(1)
        check('STAFF ONLY warns first', await E("__t.room()") == 'passage' and await E("__t.QS.staffWarn>0"), lb)
        await press()
        check('second press -> Lift Landing', await wait("__t.room()==='lift'&&!__t.sw()", 90))
        await stand(0.2, 0, -0.3, 0); await press()
        ok = await wait("document.getElementById('gameover').style.display==='flex'", 240, 1.5)
        check('stepping into the lift -> TRAPPED game over', ok and await E("document.getElementById('goTitle').textContent") == 'TRAPPED')
        await E("document.getElementById('goRetry').click()")
        ok = await wait("!__t.QS.go&&__t.room()==='passage'&&!__t.sw()&&!__t.END.on&&!__t.LIFT.in", 60)
        check('Try again -> back in the Passage, keys kept', ok and await E("__t.stage()===6"))
        await go_door('hall')
        await stand(-2.95, 0, -3.4, 0); lb = await label(); await press()
        check('front door opens with 6 keys', lb and 'leave' in lb.lower(), lb)
        ok = await wait("document.getElementById('ending').style.display==='flex'", 240, 1.5)
        title = await E("document.getElementById('endTitle').textContent"); stats = await E("document.getElementById('endStats').innerText")
        check('ending: The Visitor (camera used)', ok and 'VISITOR' in title, title + ' | ' + stats.replace('\n', ' | '))
        n_snd = await E("Object.keys(__t.SFX.buf).length"); check('all 24 recorded sounds loaded', n_snd == 24, n_snd)
        await E("document.getElementById('keepOpen').click()"); ok = await wait("document.getElementById('keepOut').style.display==='block'", 240, 1.5)
        check('keepsake parcel opens with a picture', ok and await E("document.getElementById('keepImg').src.length>10000"), await E("document.getElementById('keepName').textContent"))
        await pg.screenshot(path='e2e5_end.png')
        log('--- errors ---')
        for e in errs: log(e)
        check('no page errors / failed requests', not [e for e in errs if e.startswith('PAGEERROR') or e.startswith('REQFAIL')], len(errs))
        n = sum(1 for r in RESULTS if r[1]); log(f'=== {n}/{len(RESULTS)} passed in {time.time()-t0:.0f}s')
        await b.close()
asyncio.run(main())
