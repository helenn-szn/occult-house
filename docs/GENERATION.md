# How the assets were made

Every room, model and portrait in Occult House came from Manycore Aholo. This is the working log, run by run: the tool, the exact prompt and what came back. Download links and task outputs are left out.

**Workflow.** Rooms: write a prompt (or make a 360° panorama with Lux3D multimodal to image, then darken it with an edit instruction) → Aholo World generate → SPZ splat → loaded in three.js with Spark, then darkened and lit in code. Objects and characters: Lux3D text to 3D (G1) → GLB, reduced in size → loaded with GLTFLoader. The curator then went through humanoid auto-rig and animation retarget. Portraits: Lux3D multimodal to image (version A from text, version B from A plus a change) → cropped, darkened and aged into oil paintings.

### Run 1: first test (brief, page 7)

#### Doll Room, v1 (first attempt)

- Tool: World generate (text prompt only, no reference image)
- Prompt: A small dark room in an old house at night, floral wallpaper, shelves and chairs crowded with antique dolls, a wooden display cabinet glowing red from inside, worn carpet, photorealistic
- Time taken: about 10 minutes (started ~17:00, finished ~17:10)
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z

#### Marigold, v1 (first attempt)

- Tool: Lux3D Text to 3D, model G1, output GLB, default face count (200,000)
- Prompt: A worn hand-sewn rag doll with orange wool hair, button eyes and a faded floral dress, sitting upright, photorealistic
- Time taken: about 6 minutes (started ~17:00, finished ~17:06)
- Credits used: 20

### Run 2: darker Doll Room

#### Doll Room panorama, dark edit v1

- Tool: Lux3D multimodal to image
- Instruction: Same room, same layout. Switch off both ceiling lamps. Make it midnight outside the window with the curtains drawn. Keep only the red glow from the doll alcove and cabinet. Everything else in near darkness.
- Credits used: 12

#### Doll Room, v2

- Tool: World generate (text prompt + one reference image)
- Prompt: A small dark room in an old house at midnight, ceiling lamps off, curtains drawn, floral wallpaper, shelves and chairs crowded with antique dolls, lit only by the red glow from a doll alcove and a wooden display cabinet, everything else in near darkness, worn carpet, photorealistic
- Credits used: not reported by the World tools

### Run 3: dark edit at panorama size (attempt)

#### Doll Room panorama, dark edit v2

- Tool: Lux3D multimodal to image
- Instruction: same as dark edit v1, plus: Output must be a 360-degree equirectangular panorama with a 2:1 aspect ratio, 4096 x 2048 pixels, matching the input image's framing exactly; do not crop to a square.
- Result size: 1024 x 1024 (square). The size request in the instruction was ignored; the tool has no size setting.
- Credits used: 12

#### Doll Room panorama, local dark grades (no Aholo job)

### Run 4: hand and forearm

- Tool: Lux3D Text to 3D, model G1, face count 30,000, output GLB
- Prompt: A realistic adult right hand and forearm in a dark wool coat sleeve, palm open and fingers slightly spread, photorealistic
- Credits used: 20 (charged at submission)

### Run 5: Front hall panorama (attempt)

- Tool: Lux3D multimodal to image, text only
- Prompt: 360-degree equirectangular panorama, 2:1 aspect ratio, 4096 x 2048 pixels. Front hall of an old two-storey house at midnight. A grandfather clock beside a coat stand, a small table of framed family photographs, a guest book open on a lectern, wood panelling below faded floral wallpaper, a staircase going up into darkness, the heavy front door closed behind. Lit only by one dim red-shaded table lamp and faint moonlight through a stained-glass window above the door. Deep shadows, photorealistic.
- Credits used: 12
- Result size: 1024 x 1024 (square). Third multimodal-to-image result in a row at 1024 x 1024; the tool appears to output square images only.

### Run 6: Front hall room

#### Front hall, v1

- Tool: World generate (text prompt only)
- Prompt: Front hall of an old two-storey house at midnight, almost completely dark. A grandfather clock beside a coat stand, a small table of framed family photographs, a guest book open on a lectern, wood panelling below faded floral wallpaper, a staircase going up into darkness, the heavy front door closed behind. No ceiling lights on. Lit only by one dim red-shaded table lamp and faint cold moonlight through a stained-glass window above the door. Everything else in near darkness, deep black shadows, photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look: not midnight-dark. A ceiling chandelier is lit despite "no ceiling lights on", and the hall is evenly warm-lit; the red table lamp is a small accent. Same pattern as Doll Room v1.

### Run 7: The Curator (Mr. Ambrose Vane), model, rig and animations

#### Curator model, v1

- Tool: Lux3D Text to 3D, model G1, face count 50,000, output GLB
- Prompt: A tall thin elderly man in an old-fashioned dark three-piece suit and long black coat, pale gaunt face, slicked grey hair, white gloves, standing in a T-pose with arms straight out to the sides, full body, photorealistic
- Credits used: 20

#### Curator rig, v1

- Tool: Lux3D humanoid auto-rig, on the textured GLB above
- Credits used: 15

#### Curator animations, v1

- Tool: Lux3D humanoid animation retarget, on the rigged GLB above; separate files, GLB, not in place
- Presets chosen: `Idle_Loop` (idle), `Idle_Talking_Loop` (talking/gesturing), `Walk_Formal_Loop` (slow walk)
- Credits used: 6 (for all three)

### Run 8: The Passage

#### The Passage, v1

- Tool: World generate (text prompt only)
- Prompt: A narrow low basement corridor in an old house at midnight. Bare brick and peeling plaster walls, three closed old wooden doors along it, each with a hand-painted sign reading DO NOT OPEN. Lit only by two bare bulbs giving a dim red light, deep shadows at both ends. Photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look (from a small preview): brick corridor with red bulbs, but evenly lit in warm orange rather than deep shadow; more than three doors, several with small sign plates (wording not readable at preview size); both ends open into side rooms lit by warm table lamps instead of fading into darkness.

### Run 9: Card Parlour (15 November)

#### Card Parlour, v1

- Tool: World generate (text prompt only)
- Prompt: A dim Victorian card parlour in an old house at midnight. A round table with a dark green baize top in the middle, a green glass-shaded lamp hanging low over it giving the only light, four empty chairs pulled up to the table, heavy red velvet curtains drawn, dark wood panelling, glass cabinets of old playing cards and fortune-telling objects along the walls. Deep shadows. Photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look (from a small preview): content matches the prompt well (green baize round table, low green lamp, four chairs, red curtains, dark panelling, glass-fronted cabinets). Lighting does not: the room is evenly lit rather than lit only by the lamp, and an open doorway shows a brightly lit neighbouring room with a chandelier.

### Run 10: Card Parlour objects (15 November)

#### The Vesper Deck (tarot cards), v1

- Prompt: A stack of antique tarot cards with black and gold backs tied with a red ribbon, photorealistic
- Credits used: 20

#### The Parlour Board (spirit board), v1

- Prompt: An antique wooden spirit board with a painted alphabet, numbers, and YES / NO / GOODBYE, flat on a table, photorealistic
- Credits used: 20

#### Planchette (spirit board pointer), v1

- Prompt: A heart-shaped wooden planchette with a round glass viewing window, photorealistic
- Credits used: 20

### Run 11: Antiquities Study (15 November)

#### Antiquities Study, v1

- Tool: World generate (text prompt only)
- Prompt: A cluttered antiquities study in an old house at midnight. A heavy desk with a green-shaded banker's lamp and an open leather ledger, tall bookcases, five glass display cases holding strange relics, each lit faintly red from inside, a wall of framed old maps, crosses and charms hung on the walls. Deep shadows. Photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look (from a preview): content matches the prompt closely: desk with green banker's lamp and an open book, a row of five red-lit display cases behind it, a wall of framed maps, crosses on the walls, tall bookcases. Lighting does not: the room is evenly warm-lit rather than in deep shadow, with an extra lit table lamp and a lit doorway on the left.

### Run 12: Antiquities Study objects (15 November)

#### The Brine Mirror, v1

- Prompt: A black scrying mirror in a corroded silver frame crusted with white salt

#### The Bell of St. Orrin, v1

- Prompt: A small tarnished bronze hand bell with a carved wooden handle

#### The Hollow Idol, v1

- Prompt: A crude faceless carved wooden idol bound with frayed red cord

#### Old Tom (skull), v1

- Prompt: An old skull on a brass stand with a melted candle on top

#### The Ledger of Names, v1

- Prompt: A thick leather-bound ledger with a brass lock and a red ribbon marker

### Run 13: Portrait Gallery (15 November)

#### Portrait Gallery, v1

- Tool: World generate (text prompt only)
- Prompt: A long narrow wood-panelled portrait gallery in an old house at midnight. Six large empty gilded picture frames hung in a row along both walls, a dark runner carpet down the middle, a single bench, a tall window at the far end with curtains drawn. Lit only by dim red picture lights above each frame. Deep shadows. Photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look (from a small preview): the darkest room so far. Dark wood panelling, dark runner carpet, a bench, red picture lights above pale empty frames along both walls. Still not fully midnight-dark: the ceiling is lit a soft pink, the frames glow cream, and the far window looks bright rather than curtained.

### Run 14: Portrait Gallery paintings, Version A and Version B (15 November)

- Tool: Lux3D multimodal to image. 12 credits each, 144 in total. Each job took about 35 to 45 seconds.
- Method: the six Version A images were generated from text. Each Version B was generated with its Version A as the reference image, plus an instruction to keep the same painting and make the change.
- Prompt pattern (A): "A dark Victorian oil painting with cracked varnish, dim lighting, no frame, portrait orientation 3:4, of [subject]."
- Prompt pattern (B): "Same painting, same [subject], same style, colours and composition. Change: [change]. Dark Victorian oil painting with cracked varnish, dim lighting, no frame, portrait orientation 3:4."
- Result, all twelve: 1024 x 1024 (square, not 3:4). None look like dark oil paintings: every one is a photo-style image of the subject alone on a plain grey or white studio background, like a reference image for 3D generation.
| Painting | A task | B task | Did the change come through? |
|---|---|---|---|
| The Widow of Ashby Lane | `8008141` | `8008277` | No: B is almost identical to A; no stare or reaching hand visible |
| The Empty Chair | `8008145` | `8008281` | Partly: a yellow shape on the seat, but no clear girl; no window in either |
| Family of Five | `8008150` | `8008285` | Unclear: background changed; sixth figure not visible at preview size |
| The Lamplighter | `8008155` | `8008290` | Yes: B has him facing away on a foggy street with an unlit street lamp (A has no street) |
| Portrait of a Young Man, 1931 | `8008162` | `8008335` | Yes: B is the same man in the same suit, aged and grey |
| The Next Guest | `8008252` | `8008339` | Partly: A is a closed ornate doorway; B opens it onto darkness, but no silhouette visible |

### Run 15: Cage elevator (15 November)

#### Cage Elevator, v1

- Tool: World generate (text prompt only)
- Prompt: The inside of a tiny old 1920s cage elevator at midnight, brass lattice gates closed, dark wood panelled walls with deep scratches, a semicircular brass floor indicator dial above the gates, one bare flickering bulb, no buttons anywhere. Claustrophobic, deep shadows, photorealistic.
- Credits used: not reported by the World tools
- Scene type detected: indoor; up axis: Z
- Look (from a small preview): the viewpoint is outside the elevator, not inside it. The panorama shows a wood-panelled lobby with a marble floor, with a brass lattice cage elevator standing in the middle, lit by one bulb inside. Fairly dark overall. Not tiny or claustrophobic; the floor indicator dial and the scratches could not be confirmed at preview size.

## Mr. Vane's voice

- Script: the 24 English lines he speaks, in play order ([vane_script.txt](vane_script.txt)), each with its file name ([vane_lines.csv](vane_lines.csv)).
- Method: the whole script was voiced as one recording, then cut at the pauses between lines into 24 clips. Each cut was checked against the line's expected length and its sentence breaks, then the clips were faded at the edges and levelled to the same loudness (`assets/vo/`, 1.9 MB).
