# RyderShare Intelligence — vision prototype

Implementation of the Claude Design project **RyderShare Intelligence** (`.dc.html`), built for
the Tom Regan / DTS VPs demo (week of Jul 6, 2026). PRD of record: `docs/PRD.md` (v3.1 FINAL).

## The deliverable

**`rydershare-intelligence.html`** — one self-contained file (~675 KB). Open it in any browser,
including from `file://` with the network disabled. No server, no build step, no CDN.

- Zero external requests (verified via the Performance API: 0 resource fetches). Inter is embedded
  as a base64 WOFF2 (variable, latin subset) with the PRD's metric-compatible fallback stack;
  the RyderShare wordmark is an inline data URI; the US map and all charts are inline SVG.
- Reload = clean demo reset (per PRD §0.6). Unknown/invalid hash redirects to `#/shipments`.
- `prefers-reduced-motion` honored (CSS media query + the logic's fast reveal path, 30 ms vs 550 ms).

Routes: `#/shipments` `#/network` `#/insights` `#/reviews` `#/risk` (+ `#/agents`, and `#/ask`
which opens the Ask RyderShare slide-over on top of the current screen).

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
src/runtime.js                    dc-lite standalone runtime
src/build.py                      assembles the single-file deliverable
assets/                           Inter woff2 + logo png (embedded at build time)
docs/PRD.md                       the PRD (from the design project's uploads/)
uploads/                          logo at its original path, so the .dc.html preview also works locally
```

**Rebuild after a design change:** replace `RyderShare Intelligence.dc.html` with the new export
from claude.ai/design, then run `python3 src/build.py`. If the design ever adds template features
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
