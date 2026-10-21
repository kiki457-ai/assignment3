# Credits

## Code

**Three.js r128** — <https://threejs.org> — MIT License. Loaded from
`cdnjs.cloudflare.com`. Used for the 3D island, the voxel characters, the raycasting that
figures out where a hero was dropped, and the camera moves.

**Storypad.** Written by me. The board, the four places, the voxel character builder, the
particle effects, the drag-and-drop handling and the offline story engine are my own work
for this assignment, developed from the 3D board of my graduation project (NFC interactive
storytelling for children). Where it is not mine, it is listed below.

**Sound effects.** Generated in the page with the Web Audio API — the pickup and drop
sounds are oscillators and noise bursts written in `index.html`, not audio files. No
external samples.

**`_tools/localize.py`, `_tools/localize2.py`.** One-off development scripts written with
an AI coding agent to translate the interface strings in bulk. Kept in the repository so
the change is visible in the history.

**Course AI service.** The story gateway (`api.ait4x.org`) and Easel media API
(`easel.ait4x.org`) are provided by the course. The shared course keys ship with the page
so the AI features work on first open.

## Media

**Hero portraits** (`assets/gardener.png`, `explorer.png`, `chef.png`, `party.jpg`,
`storyteller.jpg`). Generated with an AI image model for my graduation project, based on
my own art direction. They are my own generated assets.

**Mission illustrations.** Generated at runtime by `qwen-image-2.1` (the course gateway's
proxy of the Easel image model), from a prompt the page builds out of the heroes you
placed. Not stored in the repository.

**Background music.** Not included. The track used during development is not mine to
publish, so no audio file ships here. `index.html` looks for an optional `bgm.mp3` next to
it; if you want music, supply your own file with that name.

## Text and data

**Story text.** In AI mode, written at runtime by `gpt-6-luna` (course gateway) from a
prompt the page builds from your placement, with a system instruction I wrote. In demo
mode, written by the offline story engine in `index.html`, which assembles a story from
the zone problems and hero beats I wrote for it.

**Place and character designs.** Mine. The four places — Oasis Park, Knowledge Academy,
Quiet Street, Sunny Community — and the five heroes — Gardener, Explorer, Little Chef,
Party Host, Storyteller — come from the graduation project.

## Not used

No course example code is included in this repository. No datasets. No stock media. No
other person's writing.
