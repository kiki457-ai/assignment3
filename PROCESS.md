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

- **Detection.** On load the page probes the course AI service with a cheap
  authenticated request (`probeAiService()`), and again whenever the keys change. That
  single boolean decides whether the AI path is available at all.
- **Fallback.** If the service is not reachable — or if the AI call throws for any
  reason —
  `buildOfflineStory()` answers instead. It is a real generator: the problem comes from
  `zoneProblems[zone]`, the method from `heroBeats[hero]`, and any other heroes on the
  board are woven in at the climax. Four places × five heroes, with the extra-hero line on
  top.

The part I care about most is the labelling. Every story says where it came from — a badge
at the top of the screen for the current mode, and a line under the story heading for that
particular story. If the service was down, it says the service was down. If the key was
rejected, it says the key was rejected and then still tells you a story. Nobody has to
guess whether what they are reading is the AI or the fallback.

This is also why `🎨 Draw illustration` behaves differently from `⚡ Accept the mission`.
There is no offline picture generator, so I did not fake one: the button explains what is
missing instead. A fallback that produces something worse and pretends it is the real
thing is worse than an honest "not available here".

## User trial

**Three classmates, tried on 25 October, on the live page.** I sat each of them in front
of it and said only *"Have a go at this. Tell me what you're thinking as you go."* I did
not explain the board, did not point at anything, and did not step in while they were
working. When they stopped, I asked *"What did you think would happen when you pressed
that?"*

### What they attempted

All three found **🚀 Start the mission** immediately — it is the only pressable-looking
thing on the home screen, and the camera dropping onto the island reads clearly as the
page responding. What came next was much less certain. One of them **clicked the hero
portraits instead of dragging them**: a round portrait with a name under it looks like a
button, and nothing on the dock said it wanted to be dragged. Another got a hero onto the
island and then stopped — they had placed it, the camera had flown in close, and they had
no idea the next move was to press **⚡ Accept the mission**. The hint line along the top
did say so, but it named both steps at once and was read as decoration. Nobody got stuck
on removing a hero; two of them found **↺ Clear all** on a second run without being told.

### Where they hesitated

The longest pause came right after the first successful drop. The camera pushes in close
on the hero you just placed, which reads as the *end* of something rather than the middle
of it — one of them said "is that it?" and started rotating the island to see whether
there was anything else to find. That is the moment the loop was least legible: the board
had changed, the story had not, and nothing on screen said the story was one press away.

### What I changed because of it

- **The hint now names only the next step, and it moves to where the eyes are.** With
  nothing placed it reads *"⬆ Drag a hero from the dock onto a place — press and hold,
  then let go"*, and a small bobbing **⬆ Drag me onto a place** tag sits on the dock
  itself — the person who clicked was looking at the dock, not at the top of the screen.
  Once a hero is down the tag disappears, the line becomes *"Good — now press ⚡ Accept
  the mission"*, and that button glows until it is pressed. After the story appears the
  line points at **🎵 Listen** and **🎨 Draw illustration**.
- **I did not add a tutorial or an overlay.** The loop is three steps long; explaining it
  in prose would be longer than the loop itself, and an overlay would cover the thing
  they are meant to be looking at. Naming the one live step costs one line and leaves the
  board visible.
- **The voice.** One of them said the narration sounded unpleasant, and they are right —
  it is the browser reading, not a recorded or AI-generated voice, because the course
  audio models cannot be called from a static page (documented above). What I could
  change is *which* voice it uses and how fast: the page now picks the best voice the
  device has instead of leaving the browser default, the default speed is slower (0.85×),
  and **⚙️ Settings** lets you choose any installed voice. I kept the feature rather than
  dropping it: for a five-year-old, the difference between a story you can hear and one
  you cannot is bigger than the difference between a smooth voice and a stiff one — and
  the README says plainly where the voice comes from and that Edge exposes the smoother
  ones.

### A change already made from my own testing

Before handing it to anyone else, I ran the board myself and hit things worth fixing:

- Clearing the board meant hunting for and tapping each placed figure individually on a
  slowly spinning island — easy to miss a small target. That is why **↺ Clear all** exists
  next to the mission button. Individual recall by tapping a figure is still there for
  removing one hero; the reset is for starting over.
- The first wiring of the illustration button called the course media endpoint directly
  and died with a bare "Failed to fetch". The cause was not the code but the endpoint:
  the media API sends no CORS headers, so a static page is not allowed to read its
  responses. Rather than routing traffic through a third-party proxy, the fix was to use
  the story gateway's own proxy of the same image model, which is CORS-enabled — the
  illustration now works from the page with no extra service, and the limitation is
  documented instead of hidden.

## AI tools

I used AI tools, so here is the honest account.

**CodeBuddy, an AI coding agent (used for this assignment).** Used for the code changes
described above — the offline story engine structure, the service detection and mode
badge, the fallback wiring in `generateStory` / `generateImage` / `readStory`, the
`↺ Clear all` reset, and the first drafts of this README and PROCESS file.

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

**The course AI service (used at runtime, by the page).** The course provides an
OpenAI-compatible gateway plus an Easel media API. In AI mode the story is written by
`gpt-6-luna` through the gateway, and illustrations by `qwen-image-2.1` (via the
gateway's proxy of the Easel image model, because the media API itself is not callable
from a browser). Narration uses the browser's built-in `speechSynthesis`; the media API
also offers a Suno voice, but it is not callable from a static page (no CORS headers,
and the shared key is not opened for the audio models), so that path is implemented and
documented as a silent fallback. This is described in the README and degrades to the
offline engine whenever the service is unreachable.

**An AI music tool (used for `bgm.mp3`).** The background track is AI-generated, not taken
from a music library or a recording. I generated it rather than downloading a track for two
reasons: there is no third-party rights question over a file I generated, and the piece was
made for this interface — a calm loop that sits under a children's story instead of an
arbitrary licensed track. The page still treats it as optional, so removing it never breaks
anything.

**Vidu Q3 (used in the graduation project, not in this repository).** Used to make the
concept video for the wider project. No output from it ships here.

## Repository hygiene

Checked before committing: no personal information, no recordings of other people. The
one deliberate exception worth stating plainly: the **shared course API keys are included
in the source**, because the assignment's AI features are meant to run out of the box for
whoever opens the page and the keys are class-issued, not personal. They can be
overridden in the in-page Settings, and values typed there stay in `localStorage` and are
never written to a file. The background music (`bgm.mp3`, 1.8 MB) is committed with the
page because the assignment is graded from the live GitHub Pages URL and a silent board
would read as a bug. The page still treats it as optional: if the file is missing, 🔊
says so instead of failing, and the Web Audio sound effects keep working.
