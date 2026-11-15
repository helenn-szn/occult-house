# Occult House

A first-person haunted museum that runs in the browser. You walk through the rooms of an old investigator's house at night, study the cursed objects in their collection, and break the curator's rules at your own risk.

Built for the Manycore Aholo Global 3D AI Hackathon (#Manycorehackathon).

## Built with Manycore Aholo

| Part | Tool |
|---|---|
| The Front Hall | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| The Doll Room | Aholo World API, generated from a text prompt and an edited 360° panorama |
| The Passage | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| The Portrait Gallery | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| The gallery's twelve portraits (each painting and its changed version) | Lux3D multimodal to image, then cropped, darkened and aged into oil paintings |
| The Antiquities Study | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| The study's relics: the Brine Mirror, the Bell of St. Orrin, the Hollow Idol, Old Tom and the Ledger of Names | Lux3D text to 3D (G1) |
| The Card Parlour | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| Panorama edits (lights off, midnight) | Lux3D multimodal to image |
| Marigold, the rag doll | Lux3D text to 3D (G1) |
| The player's hand | Lux3D text to 3D (G1) |
| The Vesper Deck, the spirit board and its pointer | Lux3D text to 3D (G1) |
| Mr. Ambrose Vane, the curator | Lux3D text to 3D (G1), humanoid auto-rig, and animation retarget (idle, talking, walk) |

Rendering uses [three.js](https://threejs.org) and [Spark](https://sparkjs.dev) for the Gaussian-splat rooms.

## What is playable now

- **The welcome**: ring the bell, sign the visitor agreement, and meet the curator, Mr. Ambrose Vane, in the Front Hall. He gives you three rules and a map.
- **The Front Hall**, **the Doll Room**, **the Card Parlour** and **the Passage**: walkable splat rooms, darkened in code so only red light and your own light show the way.
- **Marigold**: she sits in a locked cabinet and turns to face you when you look away.
- **The first rule**: touch her cabinet and the house answers. Knocks, a blackout, an empty cabinet, and something behind you.
- **The Card Parlour**: draw a card from the Vesper Deck and it becomes an omen that comes true later in your visit. The Tower puts every light out at the next doorway, The Moon sets the figure on your trail, The Lovers brings Marigold to sit across the table from you, and the blank card waits. Put your hand on the spirit board's pointer and it spells a message about your visit. Both count as touching the exhibits.
- **Ghosts and investigations**: a ghost appears, waits to be seen, and leaves the room. Follow it, and the Listener (a needle meter in the corner) leads you to what it wants you to find. Each clue moves the trail to another room; the last one closes the case. Two cases so far: The Tall Guest, about the curator, and The Light in the Doll Room, about Marigold's owner. Press J for the case files.
- **The Antiquities Study**: examine the five relics in their red cases and read each provenance card, then answer the curator's ledger. Its three questions can only be answered with what you found elsewhere in the house. Wrong answers have consequences; right ones open a drawer and close the case.
- **The Portrait Gallery**: six portraits. Look away and one of them changes; find which and examine it before it changes back. Catch three changes to close the case. Pick wrong and the gallery notices you.
- **A challenge in every room, and a key in four pieces**: wind the stopped clock in the Front Hall (hold E while the hall goes dark), find Button the doll by her giggling before time runs out, knock back door II's pattern in the Passage, and beat Edgar at higher or lower in the Card Parlour. Each gives a piece of a brass key.
- **The restricted lift**: the door marked STAFF ONLY in the Passage takes the whole key. It opens onto the Lift Landing, a real Aholo room, and locks behind you. At the far end a brass cage lift is waiting. Step in, the gate runs shut, and the lift falls past every floor on the dial. No one is allowed in, and there is no way back.
- **The map** shows every room with a picture of it, the doors between them, and where you are. You travel by opening doors. Each room on the map shows how far a walk it is from where you stand.
- **The radar** in the top corner shows the room you're in, turned so you always face up, with a diamond for every door. Under it, each door is listed nearest first, with its distance in metres and an arrow pointing the way.
- **The endings**: leave by the front door at any time, or the house calls you back once every rule is broken or every case is closed. The curator is waiting. Five endings: The Lift (you took the restricted lift), The Guest (no rules broken), The Visitor (one or two), The Exhibit (all three: you wake inside Marigold's cabinet) and The Curator (all four cases closed: he hands you his keys). An end card sums up your visit.
- **The second rule**: down in the Passage, three doors at the end say DO NOT OPEN. Two will not open, and something answers from the other side. The third lets you into Room Nine: the front hall again, the wrong way round, and the only way out is to find what does not belong.
- **The third rule**: the curator says no cameras, but there is one in your pocket. Through its lens you see what the eye cannot: figures in the rooms and writing on the walls. Every photo cracks the lens and brings them closer. On the eighth photo the figure comes through the lens. You wake in the Front Hall with the curator standing over you, and from then on the figure follows you through the house, waiting behind you until you turn around.

## Controls

- W A S D to walk, mouse to look (click to capture the mouse, Esc to release)
- E to interact, J for the case files, C to raise the camera (click or Space takes a photo), M for the map, Space or click to move the curator's welcome along, L to switch your light, N to switch night mode
- With a game controller: left stick to walk, right stick to look, A to use things (hold A for the clock), B to close, X to raise the camera, RT or RB to take a photo, Y or View for the map, LB for the case files, D-pad up and down for Edgar's game
- On a phone or tablet (best held sideways): a joystick appears under your left thumb to walk, drag on the right to look, tap to continue or take a photo, and on-screen buttons for using things, the camera and the map

Headphones recommended. All sound is synthesised in the page.

## Run locally

It is a static site with no build step. Serve the folder with any web server, for example:

```
npx serve .
```

Then open the address it prints. Opening `index.html` directly from disk will not work, because the browser blocks loading the room and model files that way.

## Files

```
index.html            the game
assets/front_hall.spz the Front Hall (compressed Gaussian splats)
assets/doll_room.spz  the Doll Room (compressed Gaussian splats)
assets/passage.spz    the Passage (compressed Gaussian splats)
assets/parlour.spz    the Card Parlour (compressed Gaussian splats)
assets/study.spz      the Antiquities Study (compressed Gaussian splats)
assets/gallery.spz    the Portrait Gallery (compressed Gaussian splats)
assets/lift.spz       the Lift Landing, behind the STAFF ONLY door (compressed Gaussian splats)
assets/portrait_*.jpg the gallery's paintings, two versions of each
assets/map_*.jpg      the map's pictures of each room, cropped from the room panoramas
assets/marigold.glb   Marigold
assets/hand_right.glb the player's right hand
assets/curator.glb    the curator, rigged, with idle, talk and walk animations
assets/deck.glb       the Vesper Deck
assets/board.glb      the spirit board
assets/planchette.glb the board's pointer
assets/relic_*.glb    the study's relics, shown up close when examined
```

All characters, objects and names are invented.
