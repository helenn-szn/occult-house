# Occult House

A first-person haunted museum that runs in the browser. You walk through the rooms of an old investigator's house at night, study the cursed objects in their collection, and break the curator's rules at your own risk.

Built for the Manycore Aholo Global 3D AI Hackathon (#Manycorehackathon).

## Built with Manycore Aholo

| Part | Tool |
|---|---|
| The Front Hall | Aholo World API, generated from a 360° panorama made with Lux3D multimodal to image |
| The Doll Room | Aholo World API, generated from a text prompt and an edited 360° panorama |
| Panorama edits (lights off, midnight) | Lux3D multimodal to image |
| Marigold, the rag doll | Lux3D text to 3D (G1) |
| The player's hand | Lux3D text to 3D (G1) |

Rendering uses [three.js](https://threejs.org) and [Spark](https://sparkjs.dev) for the Gaussian-splat rooms.

## What is playable now

- **The welcome**: ring the bell, sign the visitor agreement, and meet the curator, Mr. Ambrose Vane, in the Front Hall. He gives you three rules and a map.
- **The map**: press M to see the house and travel to any room you have unlocked.
- **The Front Hall** and **the Doll Room**: walkable splat rooms, darkened in code so only red light and your own light show the way.
- **Marigold**: she sits in a locked cabinet and turns to face you when you look away.
- **The first rule**: touch her cabinet and the house answers. Knocks, a blackout, an empty cabinet, and something behind you.

The curator is a placeholder figure until his Lux3D model is generated.

## Controls

- W A S D to walk, mouse to look (click to capture the mouse, Esc to release)
- E to interact, M for the map, L to switch your light, N to switch night mode
- On a phone: drag the left side to walk, the right side to look

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
assets/marigold.glb   Marigold
assets/hand_right.glb the player's right hand
```

All characters, objects and names are invented.
