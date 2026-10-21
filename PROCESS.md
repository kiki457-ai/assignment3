# Process notes

## Starting idea

The starting point was not "make a website". It was a question left over from my
graduation project: **when a child puts a physical token on a physical board, what should
the software do that feels like a response rather than a reaction?**

The graduation project answers that with hardware — an Arduino Uno R3 with a PN532 NFC
reader, five tokens, and a printed board with four places on it. That is good research and
terrible to hand to someone to try: it needs a serial port, a Python bridge service and a
pile of kit.

So for this assignment I took the same interaction and asked what the smallest version of
it would be. I kept the shape — a board with places on it, characters you put on those
places, a story that comes out of the combination — and dropped the hardware. Placing a
token became dragging a portrait. Everything else is the same loop.

Two decisions came out of that:

1. **The placement has to matter.** If dropping the Gardener in the park and dropping the
   Explorer in the street produce the same story with names swapped, the interaction is
   decoration. So the place supplies the problem and the hero supplies the method.
2. **It has to run for someone with nothing installed.** The original needed a bridge
   service and an API key before a single thing happened on screen. That is fine for a
   studio demo and useless for a marker opening a repository.

## A change I made: the story always gets told

The most important change was to the failure path, and it started as a fix to something I
got wrong.

My first version called Gemini directly and showed a red error message when the request
failed. That is honest, and it is also a dead end: the person has done everything right,
pressed the button, and now has to debug a network service to see the payoff. The
interaction just stopped.

So I split the response into two layers:

- **Detection.** On entering the board, `detectBridge()` tries the local bridge with a
  1.2 second timeout. That single boolean, plus whether a key is saved, decides whether
  the AI path is available at all.
- **Fallback.** If it is not — or if the AI call throws for any reason —
  `buildOfflineStory()` answers instead. It is a real generator: the problem comes from
  `zoneProblems[zone]`, the method from `heroBeats[hero]`, and any other heroes on the
  board are woven in at the climax. Four places × five heroes, with the extra-hero line on
  top.

The part I care about most is the labelling. Every story says where it came from — a badge
at the top of the screen for the current mode, and a line under the story heading for that
particular story. If the bridge was down, it says the bridge was down. If the key was
rejected, it says the key was rejected and then still tells you a story. Nobody has to
guess whether what they are reading is the AI or the fallback.

This is also why `🎨 Draw illustration` behaves differently from `⚡ Accept the mission`.
There is no offline picture generator, so I did not fake one: the button explains what is
missing instead. A fallback that produces something worse and pretends it is the real
thing is worse than an honest "not available here".

## User trial

> **Status: not yet done — this section must be filled in before submission.**
> The assignment asks for a trial with someone else, observed *before* explaining how it
> works. I cannot do that part for you. Below is what I ran, what I noticed, and the exact
> prompts to use.

### What to do

1. Sit someone down in front of the page. Do **not** explain it.
2. Say only: *"Have a go at this. Tell me what you're thinking as you go."*
3. Stay quiet. Do not point at anything. Do not rescue them.
4. After they stop, ask: *"What did you think would happen when you pressed that?"*

### What to watch for

- Do they find the **Start the mission** button, or look for a way in?
- Do they understand the portraits can be **dragged**? Or do they click them first?
- Where does the **first hesitation** happen — that is the thing to fix.
- After the story appears, do they connect it to what they placed? Ask them.
- Do they work out how to **remove** a hero, or do they get stuck with the board full?
- What do they try **second**? That tells you what the loop invited.

### What to write up afterwards

Three short paragraphs, no names needed:

- **What they attempted** — the actual sequence, including the wrong turns.
- **Where they hesitated** — one moment, described specifically.
- **One change you made because of it**, or why you decided to keep the design.

### A change already made from my own testing

Before handing it to anyone else, I ran the board myself and hit two things worth fixing:

- Clearing the board meant hunting for and tapping each placed figure individually on a
  slowly spinning island — easy to miss a small target. That is why **↺ Clear all** exists
  next to the mission button. Individual recall by tapping a figure is still there for
  removing one hero; the reset is for starting over.
- With no bridge running, the page probed it every 600 ms and filled the browser console
  with failed requests. Invisible to a player, but noisy and unfair on the machine. The
  polling now backs off after five consecutive failures and the status pill says plainly
  that the reader is not connected, so the page settles down in demo mode instead of
  quietly hammering a service that is not there.

## AI tools

I used AI tools, so here is the honest account.

**Claude Code (used for this assignment).** Used for the code changes described above —
the offline story engine structure, the bridge detection and mode badge, the fallback
wiring in `generateStory` / `generateImage` / `readStory`, the `↺ Clear all` reset, and the
first drafts of this README and PROCESS file.

- **A suggestion I kept.** When the AI call fails, fall back to the offline engine and
  label the story's origin, rather than showing an error and stopping. My instinct was to
  make the error message friendlier; the better answer was to make the loop complete and
  be transparent about which engine answered. The labelling is what makes that honest
  rather than deceptive.
- **A suggestion I changed.** The first plan was to rewrite `index.html` wholesale as an
  English version. Looking at it, that meant hand-rewriting about 1,500 lines of Three.js
  scene code — the buildings, the voxel character builder, the particle system — with a
  real chance of breaking the board for the sake of translating comments. I changed the
  approach: two one-off scripts (`_tools/localize.py`, `_tools/localize2.py`) do exact
  string replacement for the copy and comments, and the behavioural changes were made by
  hand in the specific functions that needed them. The scripts are kept in the repository
  so the history shows what was done.

**Gemini (used at runtime, by the page).** In AI mode the story is written by
`gemini-2.5-flash`, illustrations by `imagen-4.0`, and narration by
`gemini-2.5-flash-preview-tts`. This is described in the README and is entirely optional.

**Vidu Q3 (used in the graduation project, not in this repository).** Used to make the
concept video for the wider project. No output from it ships here.

## Repository hygiene

Checked before committing: no API keys in the source (the key is entered by the user and
kept in `localStorage`, never written to a file), no personal information, no recordings
of other people. The original background music track is deliberately excluded because I do
not have the right to publish it — the page handles the missing file instead.
