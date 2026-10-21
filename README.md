# Storypad — Whimsy Island

An interactive story board. You drop a hero onto a place, ask for the mission, and the
island tells you a story about what happened there.

![Storypad: the mission story open in demo mode, with the offline engine's note under the heading](assets/screenshot.png)

---

## The idea

Storypad started as part of my graduation project on **NFC interactive storytelling for
children**. The physical version is a printed board with five NFC tokens and an Arduino
reader; you tap a token onto a spot on the board and the story responds.

For this assignment I took that same interaction and rebuilt the part that matters — the
loop between *placing a character*, *the programme responding*, and *the feedback you get
back* — as a single web page that anyone can open. The board is now a 3D island with four
places on it. Everything driven by hardware in the original (placing, recalling, moving
between places) is done with the mouse or a finger here, so the interaction can be tested
without any equipment.

## Who it is for

Children around 5–8, reading together with an adult. The story is short, spoken aloud if
you want it, and there is no text to type and no way to fail. A second audience is anyone
marking or reading this repository — see *Two ways it answers* below.

## The main interaction

The loop is one cycle, and every cycle is the same shape:

| You do | The programme does | You see / hear |
|---|---|---|
| Press **Start the mission** | The camera drops from the home view onto the board | The island stops spinning, the five heroes appear in a dock |
| **Drag a hero** onto one of the four places | Raycasts the drop point, plants a voxel figure there, plays a drop sound | The figure pops in, the camera flies to an overview of that place and then pushes in close on the hero |
| Drop a **second hero** somewhere else | Same again | Each hero keeps its own label over its head |
| Press **⚡ Accept the mission** | Reads which heroes are placed and where, then builds a story from exactly that cast | A story appears, with a line saying where it came from |
| Press **🎵 Listen** | Reads the story aloud | Audio plays from the speakers |
| Press **🎨 Draw illustration** | *(AI mode only)* Sends the cast to an image model | A picture appears under the story |
| Tap a placed hero, or press **↺ Clear all** | Removes the figure, frees the dock slot | The hero returns to the dock, ready to be placed again |

Placing a *different* hero in a *different* place genuinely changes the story — the
problem comes from the place, the method comes from the hero, and any extra heroes join in
at the climax. Gardener at Oasis Park and Explorer at Quiet Street are different stories,
not the same story with the names swapped.

## Two ways it answers

The board always completes the loop. What changes is *which engine writes the story*:

- **AI mode** — with a Gemini API key and the local NFC bridge running, the story is
  written on the spot by `gemini-2.5-flash`, customised to the exact cast you placed.
- **Demo mode** — without either of those, the built-in offline story engine answers. It
  is a real generator, not a canned paragraph: it pulls the problem from the zone you
  dropped on and the method from the hero you dropped, then assembles a five-beat story
  with any other heroes joining in at the climax.

The badge at the top of the screen tells you which one you are in, and the line under the
story heading says where that particular story came from. **You do not need an API key, a
server, or an internet connection to try the interaction** — press Start, drag a hero,
press Accept the mission, and a story comes back.

## How to run it

The page loads Three.js from a CDN, so it needs a one-time internet connection. Serve it
over HTTP rather than opening the file directly — browsers block some local file access,
and it keeps the asset paths working.

```bash
# from the project folder
python -m http.server 8000
```

Then open <http://localhost:8000>. Any static server works:

```bash
npx serve .
# or
php -S localhost:8000
```

**Dependencies.** There is no build step and no `package.json`. The only external
dependency is Three.js r128, loaded from `cdnjs.cloudflare.com` in the `<head>`. If that
CDN is blocked, the 3D board will not appear and the page shows a plain error message
instead of a blank screen.

**Optional: AI mode.** Two extra steps, both skippable:

1. Paste a Gemini API key into **⚙️ Settings**. It is kept in `localStorage` in your own
   browser and is never sent anywhere except to the Google endpoint.
2. Run the NFC bridge on `localhost:8765`. It is the small Python service from the
   graduation project; it also proxies the Gemini calls, which is why AI mode needs it.
   Without it the page falls back to demo mode after about a second.

**Optional: background music.** The original track is not mine to publish, so no audio
file is included. Name any mp3 `bgm.mp3` and put it next to `index.html` and it will play,
or leave it out — pressing 🔊 then tells you plainly that the file is missing, and the
sound effects still work.

## What I added for this assignment

The board and the 3D island existed before this assignment. What I added here:

- **The offline story engine**, so the interaction completes with no server and no key.
- **Bridge detection and the mode badge**, so the player always knows which engine is
  answering instead of staring at a failed request.
- **Graceful failure**: every AI failure falls back to a story rather than an error, and
  shows a 🔄 Try again button.
- **↺ Clear all**, a single reset after watching someone hunt for the individual recall
  targets during a trial.
- **Missing-file handling** for the optional `bgm.mp3`.
- **Demo-mode narration** through the browser's own speech synthesis, so 🎵 Listen works
  with no API key.
- The whole interface translated into English.

See [PROCESS.md](PROCESS.md) for the design decisions and the user trial behind these.

## Known limitations

- **The illustration button needs AI mode.** There is no offline picture generator, so
  🎨 Draw illustration explains what is missing rather than drawing something. The story
  itself is unaffected.
- **Demo mode has a fixed vocabulary.** It draws on 4 places × 5 heroes plus the
  combinations between them, so it will repeat if you try the same pair twice. AI mode
  does not have this limit.
- **Browser speech voices vary.** Demo-mode narration uses whatever voices the operating
  system provides, so it can sound flat on some machines.
- **No persistence.** Reloading the page clears the board. The API key is remembered; the
  story is not.
- **Touch is supported but tuned for desktop.** Dragging works on a touchscreen, and the
  dock is sized for a mouse.
- **The NFC hardware path is not testable from the repository.** The bridge expects an
  Arduino on a serial port; without it, the mouse does the same job.

## Files

```
index.html            the whole experience (markup, styles, Three.js scene, story engine)
assets/               the five hero portraits
_tools/               one-off scripts used during development, kept for the record
README.md             this file
PROCESS.md            starting idea, design changes, user trial, AI use
CREDITS.md            borrowed code, data and media
```

## Credits

See [CREDITS.md](CREDITS.md). Summary: Three.js (MIT) for the 3D board; the hero
portraits and the mission illustrations are AI-generated; the story text is generated by
Gemini in AI mode and by the built-in engine in demo mode.
