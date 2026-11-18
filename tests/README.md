# Tests

Automated runs of the real game in a headless browser, using [Playwright](https://playwright.dev/python/). Each script loads the page, plays through part of the game, and checks what the player would see: the trial panel, prompts, the radar, the map, the death screen, the endings and the keepsake.

| Script | What it plays | Latest result |
|---|---|---|
| [`playthrough.py`](playthrough.py) | The whole game from the title screen: how to play, the curator's welcome, all six trials in order (including failing and dying), retrying a room, the STAFF ONLY lift trap, the front door, the ending and the keepsake. It also checks that all 24 recorded sounds load and that the page logs no errors. | [48 of 48 checks passed](results/playthrough.log) (18 Nov 2026) |
| [`phone_touch.py`](phone_touch.py) | A phone (844 × 390, touch): the joystick, tap-to-walk, swipe to look (swipe right turns right), the GUIDE ME button walking you to the clock, dying and retrying, and the keepsake. | [log](results/phone_touch.log) |
| [`phone_ledger.py`](phone_ledger.py) | A phone again, plus three openings of the Study's ledger, to check it draws different random questions and shuffles the answers. | [log](results/phone_ledger.log) |

## Running them

```
pip install playwright
playwright install chromium
python3 -m http.server 8000        # in the repo folder, in another terminal
python3 tests/playthrough.py
```

Set `GAME_URL` to test another address, for example the live site:

```
GAME_URL=https://occult-house-nine.vercel.app python3 tests/playthrough.py
```

The scripts drive the game through a small test hook (`window.__t`) so they can skip long waits, such as the curator's speech. Everything they check is what appears on screen. A headless browser renders the splat rooms in software, so a full playthrough takes about 25 minutes.
