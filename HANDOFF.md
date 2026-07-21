# RyderShare Intelligence — handoff brief

Written 2026-07-21 for whoever continues this work. The README covers the build; this file
covers the state, the conventions, and the traps.

## What this is

An offline, single-file HTML vision prototype of RyderShare Intelligence — an AI-native layer
on RyderShare for a Dedicated customer (Summit Beverage Group; persona: Dana, transportation
manager). It exists for exec demos. Isaac (Head of Product & Design, Baton) owns it and
directs every change; he reviews locally and says "push" when a change should ship.

## Where things live

- **This folder** holds everything the latest build needs (cleaned 2026-07-21).
- **Repo**: `github.com/isaac-baton/mission-control`, branch `main`. Vercel auto-deploys;
  `index.html` at the repo root is the site. Live at **prototype.staging.baton.io**. Last
  deployed commit: `53abe09`.
- **Local preview on Isaac's machine**: an always-on system service serves the build on
  **localhost:8791**, and the build script mirrors `index.html` into its serve directory
  (best-effort — the mirror step skips silently elsewhere). Never start a dev server for
  this project on his machine; the port is taken by design. The old **localhost:8765**
  belongs to another AI's copy of this project ("Kimi") — its build script mirrors into
  the old directory, so never serve from or trust the content on 8765.
- **Push flow**: clone the repo into scratch space (session scratch gets wiped, so re-clone
  each time), `rsync -a --delete src/ <clone>/src/ && cp index.html <clone>/`, commit, push,
  then poll the GitHub deployments API for the commit's deployment to reach `success` (Vercel
  missed a webhook once — always verify), and finally confirm the live file's byte size
  matches the local build.
- **Unpushed right now**: the real-geometry Network map (new `assets/*.json` +
  `src/v2/gen_map_layers.py` + the T12 block in the build), the folder cleanup, and the
  rewritten `README.md`/this file. The repo still carries stale root files from the original
  import (`support.js`, `index-v2.html`, `uploads/`) — drop them on the next push.

## Architecture

- The **design source** (`RyderShare Intelligence.dc.html`) is verbatim and never hand-edited.
- **`src/build_v2.py`** assembles `index.html`: it inlines the source, applies anchored,
  count-asserted string transforms (a failed assert aborts the build — that is the safety
  net), layers the `src/v2/` patch files, inlines the hand-written **dc-lite runtime**
  (`src/runtime.js`: `sc-if`, index-keyed `sc-for`, `{{ }}` bindings, `on*` events,
  `style-hover` compiled to `!important` classes, synchronous setState), embeds fonts/logo,
  tightens every em dash (` — ` → `—`, Isaac's non-negotiable), and mirrors the output to
  the local preview's serve directory when it exists.
- **`src/v2/logic.js`** defines `ComponentV2` over the design's V1 logic: routes and gating,
  all V2 state, the per-agent audit-log data (`AGLOG` + `entriesFor` with live "Just now"
  entries), the decision handlers, and the ask bar's dynamic intent engine.
- **Generators** (run only when editing them): `src/v2/gen_workforce.py` builds the dark
  Agents page; `src/v2/gen_map_layers.py` builds the map's interstate/city layer using the
  projection fit `x = 43.53·lon + 4439.6`, `y = −47.45·lat + 1778.3` (reproduces the design's
  own city anchors to ~1px).
- `window.__app` exposes the component instance for debugging.

## Product state (all deployed)

- **Splash** (`#/insights`, pre-enable): "Put your supply chain on autopilot." with the 24/7
  agents subtitle; Enable runs a ~5s staged activation. A reload resets the whole demo;
  `?intel=1` is the only boot override.
- **Autopilot** (`#/agents`): the Agent Feed — live-count header ("Your agents worked
  overnight—5 things need you." → all-clear at 0), four state-bound analytics cards, one
  timeline with the five decisions embedded (storm plan → a 560px decision panel with the
  dossier and working Adjust cost math; two adaptive-capacity moves → rate-chart panels;
  tender + trailer as chips), green receipts in place, and month-grouped history behind
  "See all history" (collapsed by default — a stated requirement).
- **Agents** (`#/workforce`): the dark showroom — eight agent cards with hue auras, ghost
  icons, enable-flash rings, and audit side panels; the whole page and its panels theme dark
  (panels self-bind `data-ptheme` because they mount outside the themed root).
- **Network**: the real-geometry map (LOCAL, not yet pushed) — dissolved Census state
  silhouette with each internal border drawn once, cased roads (one geometry, casing under
  a white core; US interstates + Canada Federal/State tiers + Mexico Interstate/Federal,
  classified per country by point-in-polygon), Canada/Mexico province fills via a
  TopoJSON-style shared-arc pipeline (Natural Earth topology is NOT Census-clean — a full
  dissolve mis-chains and flips provinces into water), province labels, anchor cities,
  small heading-arrow pin markers, storm track + forecast cone. The design source's own
  hand-drawn states AND its cased road network are excised at build time — never let both
  road systems render.
- **Reviews**: the document-style review with Jun/May/Apr tabs. **Shipments**: the board.
- **Ask bar**: scripted answers (q1–q6) take priority, then ~10 on-domain dynamic intents
  composed from live state (including load-ref lookup and the approval queue), then an
  in-character conversational tier with rotating variants ("do I matter" gets a grounded
  deflection, never a confession). Unscripted asks log to the console to grow the bank.
- **Adaptive Capacity** is the 8th agent, grounded in the internal PRFAQ: lane-level flexing
  both directions (lock brokerage lanes into dedicated when spot rises; flex a soft dedicated
  lane out), dual sign-off everywhere.

## Isaac's standing rules (violating these gets work rejected)

1. **Tone**: his voice everywhere (see the `isaacs-tone-of-voice` skill). Complete sentences
   with a subject and verb; no "X, not Y" antithesis; no "[noun], [participle]" tagline
   cadence; no stacked short fragments; no performed candor; em dashes always tight (the
   build enforces this one).
2. **Process**: change locally, tell him it's ready at localhost:8765, and push only when he
   says "push". Verify what you claim — he catches unverified assertions.
3. **Design taste**: no sub-tabs on Autopilot (rejected twice with rationale); calm but never
   bare or flat; he likes the dark cinematic Agents aesthetic; timeline dots must center on
   the line; verbatim demo numbers are locked; the approve→settle drain is the demo's money
   moment and must stay legible.

## Traps that cost real time

- Screenshots of background browser tabs freeze CSS animations — panels look transparent when
  they are not. Trust computed styles and `elementFromPoint`, and use zoom for fine detail.
- The runtime writes bound `style` attributes via `cssText`, which normalizes hex colors to
  `rgb()` — attribute-substring CSS selectors need both forms.
- On macOS, launchd agents cannot read privacy-protected folders (TCC) — that is why the
  preview service serves a mirror directory instead of this folder directly.
- Patch-file source keeps spaced em dashes (tightening happens at build) — string replacements
  against source files must use the spaced form, against `index.html` the tight form.
- The one prior layout regression came from a dropped `</div>` in `agents2.html` — it pushed
  later screens out of the scroll container. Check open/close counts after structural edits.
