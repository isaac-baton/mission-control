# RyderShare Intelligence — vision prototype

Implementation of the Claude Design project **RyderShare Intelligence** (`.dc.html`), built for
the Tom Regan / DTS VPs demo (week of Jul 6, 2026). PRD of record: `docs/PRD.md` (v3.1 FINAL).

## The deliverable

**`index.html`** — the **Version 2** onboarding journey (see the V2 section below). This is the
deployed site: Vercel serves `index.html` at the root. Built by `python3 src/build_v2.py`.

One self-contained file (~698 KB). Open it in any browser, including from `file://` with the
network disabled — no server, no build step, no CDN.

- Zero external requests (verified via the Performance API: 0 resource fetches). Inter is embedded
  as a base64 WOFF2 (variable, latin subset) with the PRD's metric-compatible fallback stack;
  the RyderShare wordmark is an inline data URI; the US map and all charts are inline SVG.
- Reload = clean demo reset (per PRD §0.6). Unknown/invalid hash redirects to `#/shipments`.
- `prefers-reduced-motion` honored (CSS media query + the logic's fast reveal path, 30 ms vs 550 ms).

Routes: `#/shipments` `#/network` `#/insights` `#/reviews` `#/risk` (+ `#/agents`, and `#/ask`
which opens the Ask RyderShare slide-over on top of the current screen).

**Version 1** (the "product as if Intelligence is already on" — no onboarding) is superseded on the
live site but stays reproducible: `python3 src/build.py` → `v1.html` (gitignored, not deployed).

## How it was built

The Claude Design preview runs the design file on React + Babel + `support.js` pulled from unpkg —
fine in the tool, but not demoable offline. This implementation keeps the design's markup and
logic **verbatim** (zero transcription drift from what was signed off in Claude Design) and swaps
the preview stack for `src/runtime.js`, a ~350-line dependency-free runtime that implements the
same template semantics: `sc-if` / `sc-for`, `{{ path }}` text/attribute bindings, React-style
event attributes (`onChange` ⇒ `input`), callback refs, `style-hover` pseudo-classes, and
synchronous `setState` commits against `renderVals()`.

```
RyderShare Intelligence.dc.html   design source of record (exported from Claude Design)
support.js                        the preview runtime it replaces (reference only)
src/runtime.js                    dc-lite standalone runtime (shared by both builds)
src/build_v2.py                   canonical build → index.html (V2, deployed)
src/v2/                           V2 patch layer: landing.html, logic.js, v2.css
src/build.py                      legacy V1 build → v1.html (gitignored)
assets/                           Inter woff2 + logo png (embedded at build time)
docs/PRD.md                       the PRD (from the design project's uploads/)
uploads/                          logo at its original path, so the .dc.html preview also works locally
```

**Rebuild after a design change:** replace `RyderShare Intelligence.dc.html` with the new export
from claude.ai/design, then run `python3 src/build_v2.py` (rebuilds `index.html`). The V2 build
applies count-asserted transforms over the verbatim source, so a design re-export that moves an
anchor fails the build loudly instead of drifting silently. If the design adds template features
the runtime doesn't know (new `on*` events are handled generically; `sc-for` nesting, `$index`,
mixed-string attributes are supported), `src/runtime.js` is the place to extend.

## Verification (2026-07-03)

Compared side-by-side against the live design preview (original `.dc.html` + CDN runtime) — all
six screens pixel-equivalent, and the PRD §12 acceptance checklist passed line by line:

- Demo path S0a → Network → Insights → typed Q2 (waterfall + Sources 4) → Q3 chip → Q5 chip →
  Reviews → risk card → S4 Approve (toast, table flips to Scheduled, button disables, storm zone
  dims to 0.35, approved state cascades to Shipments band / Insights / Agents to-dos).
- Keyword router per §8.2: punctuation stripped, `late` word-boundary (`lately` ⇒ fallback),
  chips hard-bound (never routed). Fallback answer has no sources expander.
- Filters (status tiles, 4 multi-select menus with count labels, search, reset), sort with CSS
  order + arrows, map zoom/pan/markers/layers/tabs, load panels from board rows and map popups,
  agent toggles with AI-flash, tender dismiss / trailer scheduling, decisions counter 3 → 0.
- Reduced-motion delays measured: [30, 60] reduced vs [550, 1470] normal. Binding commit ≈0.9 ms.
- Menus close on outside click via the fixed backdrop. Reload resets. 1280×800 and 1440×900 clean.
- `file://` load verified in Chrome (screenshot), zero network.

Prop defaults baked at build time: `motion: true`, `startRoute: "shipments"` (same as the design's
Tweaks panel).

## Version 2 — the onboarding journey (`index.html`, deployed)

V2 tells the adoption story: RyderShare **without** Intelligence, then the switch flips.
Built by `python3 src/build_v2.py` from the same verbatim design source plus a patch layer in
`src/v2/` (landing markup, `ComponentV2` logic, gating CSS).

- **Pre-enable** — the rail holds only Shipments / Network / Insights (pulsing cue); no prompt
  bar, no storm plan, no Why? links, no network brief, no at-risk tile, no Backhaul $ layer.
  A one-line teaser sits in the storm band's slot. `#/insights` is a landing page: hero, four
  benefit cards, the four agents, a trust card, Enable CTA. Deep links to gated routes
  (`#/risk`, `#/agents`, `#/reviews`, `#/ask`) land on the landing.
- **Enable** — a ~5s staged activation ("Connecting… · Reading June — 1,187 loads · 214
  invoice lines · Generating your first digest") inside a corner-matched fast rainbow ring, then
  the same page becomes the intelligence hub (its persistent glows only — no extra flash) and the
  rail grows to six destinations. AI surfaces discovered on *other* pages (shipments storm band,
  network brief) carry a one-time ~3s rainbow flash (`[data-intel-flash]`) while the enable moment
  is fresh. Reduced motion ⇒ instant enable.
  Pre-enable there is no storm overlay anywhere (map zone, label, layer pill, board band) —
  weather response arrives with Intelligence. No "Concept" chips: it presents as real product.
- **Map tiles** — the Network stat strip renders as cards (taller, larger icons); the two
  actionable tiles (Running late → filters the load list, At-risk → Risk radar) carry a chevron.
- **State** — in-memory; reload returns to the un-enabled state (demo reset).
  `?intel=1` boots straight to enabled for rehearsal.
