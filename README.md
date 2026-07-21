# RyderShare Intelligence — vision prototype

This is the RyderShare Intelligence demo: an AI-native layer on RyderShare for a Dedicated
customer (Summit Beverage Group), built for exec demos. PRD of record: `docs/PRD.md`.

## The deliverable

**`index.html`** — one self-contained file (~830 KB). Open it in any browser, including from
`file://` with the network disabled — no server, no build step, no CDN. Vercel serves this
file at the site root (repo: `isaac-baton/mission-control`, live at prototype.staging.baton.io).

Useful addresses:

- `index.html` — the full journey from the pre-enable splash ("Put your supply chain on
  autopilot.") through activation
- `index.html?intel=1#/agents` — boots enabled, straight onto the Autopilot feed
- A reload resets the demo state; `?intel=1` is the only boot override

## What's in the product

- **Autopilot** — the agent feed: analytics cards, a chronological timeline with five
  decisions embedded (storm plan, two adaptive-capacity flex moves, backhaul tender,
  trailer service), receipts as you approve, and month-grouped history behind
  "See all history"
- **Agents** — the dark showroom for the eight agents, each with an audit-log side panel
- **Network** — live map with real state geometry, an interstate-corridor layer, and the
  storm overlay
- **Insights / Reviews / Shipments** — digest, document-style business reviews with month
  tabs, and the load board
- **Ask bar** — scripted answers for the core questions plus a dynamic intent engine that
  answers unscripted questions in character

## Build

```
python3 src/build_v2.py
```

The build inlines the design source (`RyderShare Intelligence.dc.html`) verbatim, applies
anchored count-asserted transforms, layers the `src/v2/` patch files, swaps the preview
stack for the hand-written dc-lite runtime (`src/runtime.js`), embeds fonts and the logo
from `assets/`, and writes `index.html` (plus a best-effort mirror for the always-on local
preview server on Isaac's machine).

Two generators produce patch files and only need re-running when you change them:

```
python3 src/v2/gen_workforce.py    # the dark Agents page (cards, hues, ghost icons)
python3 src/v2/gen_map_layers.py   # all map geometry: states/provinces, roads, cities, labels
```

## Layout

- `RyderShare Intelligence.dc.html` — design source of record (never edited by hand)
- `src/build_v2.py` — the canonical build
- `src/runtime.js` — dc-lite runtime (sc-if / sc-for / bindings / events)
- `src/v2/` — patch layer: screens, panels, logic, styles, generators
- `assets/` — Inter variable font + logo, embedded at build time
- `docs/PRD.md` — the PRD
