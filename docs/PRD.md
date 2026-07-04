# PRD — RyderShare Intelligence: a vision prototype for the next chapter of RyderShare for DTS

**Author:** Isaac (Head of Product & Design, Baton)
**Date:** July 2, 2026
**Status:** v3.1 — FINAL for Claude Design execution. Verified: Builder dry-run 8.5/10 with zero blockers; Devil's Advocate must/should-fixes applied; independent Verifier gate passed (all critique items resolved, arithmetic recomputed clean, N1–N6 defects fixed).
**Deliverable:** A clickable, interactive prototype presented to Tom Regan (EVP, DTS) and the DTS VPs the week of July 6, 2026

---

## 0. To Claude Design — how to execute this PRD

You are building a **vision prototype**, not a production app. Read this entire document before writing code. Everything you need is here: screens, exact copy, exact data, design tokens, and interaction behaviors. Where this PRD is silent, default to the plainest possible treatment — this product's design language is calm, dense, and utilitarian.

**Build requirements (each is binding):**
1. **One self-contained HTML file, zero external network requests, verified working from `file://` with the network disabled.** This will be demoed in a boardroom on unknown wifi. Embed Inter 400/500/600/700 as base64 WOFF2 subsets if feasible; regardless, declare a metric-compatible system fallback stack (`Inter, -apple-system, 'Segoe UI', sans-serif`) so the page degrades cleanly. No CDN scripts, no map tiles, no Google Fonts runtime dependency.
2. **Map is a static inline SVG** (spec in 10.5) — no Leaflet, no tiles. **Charts are hand-rolled inline SVG** (line, bars, waterfall, KPI strip) — no chart library; it's the only way to hit the exact tokens.
3. Icons: inline SVG, Lucide-style line icons, 18px in rail, 16px inline. Zero emojis anywhere in the UI.
4. Every element on the demo path (Section 3) must be functional. Off-path elements may be inert but must look real: no lorem ipsum, no dead `#` jumps, no empty states. Clicking an inert element does nothing, silently.
5. **Chips and opportunity cards are hard-bound actions** (each submits a specific canonical question or navigates to a specific route). **The keyword router (8.2) applies to typed input only.** Never pass a chip label through the router.
6. State is in-memory only; a reload is a clean demo reset (that's a rehearsal feature). The S4 approved state persists for the session. Unknown/invalid hash → redirect `#/shipments`. Scroll-to-top on every route change; no scroll restoration.
7. Respect `prefers-reduced-motion` (all reveals become instant). Motion budget is 10.4.
8. Persistent footer badge on every screen: `Vision prototype · Synthetic data · Baton Product & Design` — 11px grey-400, bottom-right, on a `rgba(255,255,255,0.85)` pill so it stays legible over the map.
9. Accessibility floor: all small green text uses `#1F7A61` (never `#34A081` below 18px); DISPATCHED chip text `#276A92`; keyboard focus-visible = 2px `#307CA7` outline, 2px offset.
10. Acceptance checklist is Section 12. Self-verify every line before calling the build done.

---

## 1. Why this prototype exists

Back in 2020–21, RyderShare was a genuine competitive advantage: launched May 2020, it made Ryder the first mover on collaborative visibility while most DTS competitors had nothing. That advantage has eroded. J.B. Hunt DCS customers get 1,500+ KPIs through 360, Werner EDGE runs on 100% of Werner's dedicated trips, NFI markets a control tower with digital-twin modeling. Our own VOC tells the same story: 95% of decision-makers say RyderShare delivers value, but only 82% say it delivers actionable insight and 78% say it beats competitors. Visibility is table stakes now.

Tom Regan sees the next frontier clearly, and he's asked us to sketch it: AI features inside RyderShare that let a DTS customer access key insights about their own business — operational metrics, cost insights (billing, fuel, backhaul), and an LLM concept where they prompt for information and get an answer.

We have been building toward this since the Vision 2025 doc: CommAgent answers customer questions, InsightAgent turns operational data into business intelligence, RiskAgent gets ahead of disruptions. The foundations we sequenced there are now behind us — the Turvo migration is complete (120 customers, 21,000 loads a week on RyderShare 2.0), Mission Control shipped in May as our first research-driven workspace, and the 2026 roadmap lands data-trust signals in Q2 and exception clarity plus proactive alerts in H2. The arc Jerry framed for the strategy narrative holds here: RyderShare showed you your freight → RyderShare highlights what's important → **RyderShare explains your business and recommends actions.** This prototype is step three, made clickable.

Two more reasons this matters right now. First, DTS analytics today is embedded Power BI — and the ask coming out of the June roadmapping session with Tom's team was a RyderShare-native reporting experience, baked into our product. Second, customers are openly demanding it: a marquee DTS account is building its own AI agents and challenging us to show what "Ryder 2.0" looks like.

The competitive claim we will make in the room is scoped, and every qualifier is load-bearing: **no dedicated transportation provider today offers customers a conversational AI over their fleet's operational and cost data.** The pattern is already shipped and proven in adjacent logistics software — project44, FourKites, Uber Freight, Flexport — and Penske is one release away from adding a prompt on top of Catalyst AI. The white space is real; the window is likely 12–18 months. (Never say a flat "no one has this" — see Appendix B for the Penske rebuttal.)

**The purpose of the prototype is to make the room believe the next chapter is real and near.** Not a mockup on a slide — a product Tom's VPs can click, type into, and imagine selling against Penske next quarter.

## 2. What we are building (and not building)

**One line:** RyderShare Intelligence — the customer's fleet, explained: every DTS customer opens RyderShare and can see, ask, and act on the business behind their freight.

| Tom's ask | Capability in prototype | Vision 2025 lineage |
|---|---|---|
| "Key operational metrics… key insights about their business" | **Insights home** — AI weekly digest, KPI cards, trends, opportunities | InsightAgent |
| "Cost insights (billing, fuel, backhaul)" | **Ask RyderShare** answers on invoice variance, backhaul value, backhaul enrollment + **auto-generated Business Review** | InsightAgent |
| "LLM concept where they can prompt the info and get the answer" | **Ask RyderShare** — natural-language prompt bar with cited, chart-backed answers | CommAgent |
| (Where Mission Control points) | **Risk radar** — proactive at-risk loads with a recommended, human-approved plan | RiskAgent |

**Not building:** production AI, real data connections, mobile, login/permissions, internal ops views, admin, settings. All data is synthetic (Section 9). The prototype never claims a feature is shipped — it shows where RyderShare goes next.

## 3. The room and the demo script

**Audience:** Tom Regan + DTS VPs, in-person; Isaac drives on a large screen, then VPs may click around themselves. Both modes must work: a tight scripted path and safe free exploration. One audience fact shapes the script: **most of Tom's VPs have not seen RyderShare 2.0 up close** — beat 1 is product grounding, not filler.

**Six beats, under five minutes.** Everything on this path must be flawless.

| Beat | Action | Line that lands it | Time |
|---|---|---|---|
| 1. Today | Land on **Shipments** (S0a) — the board customers live in | "This is RyderShare today. Every load, live. Every competitor now has a version of this screen." | 0:20 |
| 2. Mission Control | Click **Network** in the rail → S0b map view | "This is Mission Control — shipped in May. The whole network at a glance. This is where the last chapter ends." | 0:25 |
| 3. Insights | Click **Insights** (red-dot badge) → S1. Let the digest sit on screen a beat | "And this is the next chapter. The moment Dana logs in, RyderShare has already read her business for her." | 0:50 |
| 4. Ask | Click the prompt bar, type **"Why was my June invoice 8% higher than May?"** → answer streams with waterfall + sources. Then tap follow-up chip **"How much is my empty backhaul worth?"** | "This is the LLM concept — grounded in her loads and invoices, with sources she can audit. And the backhaul answer is the one that pays for the program." | 1:50 |
| 5. Review | Rail → **Reviews** (S3). One slow scroll | "The monthly review our teams build by hand — generated in 42 seconds, for every account, every month." | 0:45 |
| 6. Proactive | S1 risk card → **Risk radar** (S4). Click **Approve plan** → confirmation | "And it doesn't wait to be asked. Thursday's storm, handled Tuesday — with a human approving the plan." | 0:45 |

**Close (spoken, back on S1):** "Everything you just saw runs on data RyderShare collects today, with the trust-hardening already on our 2026 roadmap underneath it. The AI layer is the investment conversation — and the window to own this in DTS is open now. Next step, exactly as Tom framed it: structured feedback sessions with two or three current RyderShare customers this quarter, and a sized proposal behind them. One more thing this buys us: insight that saves a customer money is renewal defense — accounts where RyderShare is absent are the ones we've been losing."

**Interruption protocol (this will not run linearly — EVPs interrupt at the first wow):**
- Reset move: clicking **Insights** in the rail always re-anchors the spine; every beat is reachable from S1 in one action.
- If the room is hot, drive with suggestion chips instead of typing — same answers, zero typo risk.
- Pre-agreed drop order if time collapses: beat 6, then beat 5. Beats 1–4 are the non-negotiable core.
- Budget note: the six beats sum to 4:55 with Q3 ending beat 4. If Tom's enrollment follow-up (Q5) plays live, compress the close to its first sentence — the spine has no other slack.
- If a VP grabs the mouse: everything clickable either works or fails silently; unscripted questions get the honest fallback (8.5). Let them type — the fallback is part of the pitch.

**Wow moments, in priority order:** (1) the invoice answer streaming in with a waterfall and clickable sources; (2) the backhaul pair — value, then enrollment — aimed at Tom's favorite economics topic; (3) the 42-second business review; (4) approve-a-plan.

## 4. The customer lens

The room watches through a customer's eyes. The prototype is logged in as:

**Dana Whitfield — VP Supply Chain, Summit Beverage Group (SBG).** Fictional, deliberately archetypal: a beverage distributor running a Ryder dedicated fleet from four DCs (Dallas DC-01, Memphis DC-02, Atlanta DC-03, Orlando DC-04), 46 tractors, 71 drivers, ~275 loads/week, multi-stop retail delivery **with driver + helper crews and driver unload standard** — which is why per-stop economics run rich and unload time is a live cost lever. Dana's world: service to retail accounts, cost per stop, fuel exposure, and an invoice she defends internally every month.

Her Ryder account team (contact cards): **Marcus Reed, DTS Account Manager**.

⚠️ All names, customers, and numbers are synthetic. Do not use any real Ryder customer name anywhere in the prototype.

## 5. Information architecture

The prototype lives inside the real RyderShare 2.0 shell. Get the shell right and the whole demo reads as the actual product growing — get it wrong and it reads as a concept car.

```
Left rail (~64px, charcoal grey-700, icon + 10px label stacked per item, top → bottom):
  [RyderShare emblem — solid #CE1126 square, white mark, per reference PNGs]
  Shipments   — list icon        → S0a  (landing)
  Network     — globe/map icon   → S0b  (Mission Control)
  Insights    — sparkle icon     → S1   (NEW — 8px #CE1126 dot badge, Insights ONLY,
                                          persists all session; it marks NEW, not unread)
  Reviews     — file-chart icon  → S3
  Risk        — shield icon      → S4
  [spacer]
  Settings, Log out — pinned bottom, inert
Active item: darker tile (grey-900) + 2px #CE1126 left-edge accent (existing product pattern).
No rail item is active while on #/ask.

Top bar (white, 48px, 1px grey-75 bottom border):
  RyderShare logo lockup: red emblem + "RYDER" in #CE1126 + "SHARE" in grey-500 #44464B + ™.
  SHARE is ALWAYS grey — trademark rule; never recolor it.
  Right: "Report an issue" text link (inert) · 28px avatar circle "DW".
```

Ask RyderShare (S2) is not a rail item — it opens from any prompt bar and shows a back arrow returning to the originating screen.

Routing: hash-based (`#/shipments`, `#/network`, `#/insights`, `#/ask`, `#/reviews`, `#/risk`). Land on `#/shipments`. Unknown hash → `#/shipments`.

## 6. Screen specs

### S0a — Shipments (the load board, "RyderShare today")

Purpose: instant recognition of the shipped product. Familiar, dense, competent. Mirrors the real board (see `reference-screens/load-board-list.png`).

- **Search input** top-left (rectangular, 1px grey-100 border, placeholder "Search Ryder # or reference", inert).
- **Filter chip row:** pill chips with icon + label + caret — `Cost Center (2)` (active: light-blue tint #ECF4F9), `Next stop ETA is`, `Select date`, `Route`, `Location`, `Trailer` + `Reset` text link. All inert.
- **Status overview band** (collapsible card, expanded by default): header row `⌄ Status overview · This week`; five count tiles: `PLANNED 18` · `DISPATCHED 26` · `STARTED 34` · `COMPLETED 189` · `RUNNING LATE 3` (count on yellow-50 chip). Labels 11px uppercase; numbers 20px/600. Collapse toggle works (nice free-exploration touch, trivial to build).
- **Table** — real product columns: `REFERENCE #` · `RYDER #` · `STATUS` · `ORIGIN` · `DESTINATION` · `STOPS` · `NEXT STOP ETA` · `UPDATED`. Two-line origin/destination cells (site name over city/state), ~84px rows (per reference PNG), headers 11px/500 uppercase grey-400, horizontal dividers only. 12 rows — exact data in 9.6. STOPS cells show `n/m` + slim progress bar (blue; yellow if running late, with amber warning triangle + "Running late" text under). UPDATED shows freshness text ("12m ago") — the data-trust signal the product ships this quarter.
- **Prompt bar (the one new element):** fixed at the bottom of the content area (page scrolls beneath it), 720px centered — sparkle icon + placeholder `Ask anything about your fleet — try "Why was my June invoice higher?"` + `NEW` chip inside the bar, right-aligned (the chip swaps for the submit button when input is non-empty). Click focuses; typing + Enter routes to S2 with the input submitted; **Enter on empty input opens S2 in its empty state** (that's the only path to S2's suggestion-chip state, and it's the safest way to hand the mouse to a VP).

### S0b — Network (Mission Control, simplified)

Purpose: "the last chapter" — the shipped May 2026 map workspace. Mirrors `reference-screens/mission-control-core-desktop.png`.

- **Left card list (360px):** header "Active loads" (20px/600) + "Updated 15 mins ago" meta right; search box ("Search by Ryder # or reference", inert); tabs `Location (8)` / `No location (1)` — red underline on active; tab switching may be inert.
- **8 load cards** (matching the 8 map markers, data 9.6b): each card — truck icon + reference title (14px/600), city/state + freshness line (12px grey-400), `NEXT` label + stop name, **ETA bold** (`ETA 2:40 PM ET · Jul 7`; late variant: `Running late: ETA 4:15 PM ET` in yellow-900; match each card's zone to its 9.6 row), slim progress bar (blue; yellow if late) + `n/n stops` right label. List scrolls silently to its end.
- **Map (remaining width, full-bleed, static SVG per 10.5):** US Southeast; 8 circular directional-arrow markers — 6 blue, 2 yellow; white pill overlays top-left `White glove (2)` · `Running late (2)`; map control pills bottom-right `Center map` `Traffic` (inert).
- **Marker click:** small white info card anchored to the marker — load reference (14px/600), status chip, ETA line, `View load` inert link. One shared implementation across markers, content per 9.6b. Click elsewhere dismisses.
- **No prompt bar here** — this screen is deliberately "before."

### S1 — Insights home (the InsightAgent surface)

Purpose: "the exec dashboard the VP of Transportation sees each morning." Dense but calm.

Layout (24px page padding, 16px section gaps):

1. **Greeting row:** "Good morning, Dana" (24px/600 — the one sanctioned heading-scale bump) + "Tuesday, July 7, 2026 · Summit Beverage Group" (13px grey-400). Right: **prompt bar** (480px, same behavior as S0a's, including empty-Enter → S2 empty state).
2. **AI digest card** (full width; white; 1px grey-75; 8px radius; whisper shadow; 3px #CE1126 left accent — the one sanctioned brand-red structural use; header: sparkle icon + `YOUR FLEET THIS WEEK` label + `GENERATED 6:02 AM` meta):
   > A strong week. On-time delivery held at **96.2%**, comfortably above your 95% target, and cost per stop held near plan at **$248** — up $6 on peak-season volume. Two things worth your attention: driver unload time at **Orlando DC-04** is running nearly 3× a typical month, and **Thursday's Gulf storm** puts 6 loads at risk — a mitigation plan is ready in [Risk radar](#/risk). Your **June business review** is [ready to read](#/reviews).
   Both inline links are live (blue-600). Footer: `Sources (3)` expander (8.3) listing: Load records · Invoice SBG-2026-06 · Site telemetry.
3. **KPI row — 5 cards** (26px/600 tabular numbers, 11px uppercase labels, 12px trend line):
   - `ON-TIME DELIVERY` **96.2%** · `▲ 2.1 pts vs May` (green #1F7A61)
   - `COST PER STOP` **$248** · `▲ $6 vs May` (yellow-900)
   - `LOADS DELIVERED` **1,187** · `June total` (neutral)
   - `FUEL` **$3.68/gal** · `DOE ▲ $0.19 · $180K June` (yellow-900)
   - `EMPTY MILES` **18.4%** · `▼ 0.6 pt vs May` (green #1F7A61)
4. **Two chart cards side by side (58/42, equal heights, ~260px plot area, 16px padding):**
   - "On-time delivery, last 8 weeks" — line chart, weekly `93.8, 94.4, 94.1, 95.0, 95.6, 96.0, 96.3, 96.2`, dashed 95% target line. 1.5px blue-600 line; hover dots show value in a charcoal tooltip.
   - "Cost per stop, last 6 months" — bars `Jan 251 · Feb 246 · Mar 244 · Apr 240 · May 242 · Jun 248`, grey-100 bars, June in blue-600, value labels on top (12px grey-700).
5. **Opportunities — row of 3 cards.** Each: line icon · title (14px/600) · one-line body (13px grey-400) · dollar chip (green tint #E8F5F0, text #1F7A61) · `Ask about this →` link. **Each card is hard-bound: it opens S2 and submits its canonical question** (bubble shows the canonical string, not the card title):
   - **Backhaul capacity** — "Three return lanes run empty on a regular schedule." · `≈ $458K/yr gross` → submits Q3's question
   - **Orlando unload windows** — "Shifting DC-04 windows to 6–10 AM cuts unload-surge accessorials." · `≈ $132K/yr` → submits Q2's question
   - **Saturday consolidation** — "Atlanta Saturday routes ran at 61% trailer utilization in June." · `≈ $96K/yr` → submits Q6's question
6. **Risk card (full-width, compact):** shield icon · `THIS WEEK` label · "Tropical system, Gulf Coast — Thursday, July 9. **6 loads at risk.** Mitigation plan ready." · `Review plan` button (secondary variant) → S4.

### S2 — Ask RyderShare (conversation view)

Purpose: the LLM concept, made concrete and trustworthy.

- **Header row:** back arrow (returns to the screen that opened S2) · sparkle icon + "Ask RyderShare" (16px/600 — sanctioned one-off size) · `CONCEPT` chip (uppercase 11px, yellow-50 bg, yellow-900 text).
- **Thread column, 760px centered.** User message right-aligned in a grey-25 bubble (13px). Answer = full-width bordered card (white, 1px grey-75, 8px radius, whisper shadow, 20px padding). Thread persists for the session; reopening S2 with an existing thread scrolls to the latest message and shows no suggestion chips (chips appear only when the thread is empty).
- **Answer anatomy (all scripted answers):**
  1. Headline answer, one sentence (15px/600 — sanctioned one-off).
  2. Chart or table (per-answer spec, 8.4).
  3. Narrative, 2–4 sentences (13.5px grey-700, numbers bolded).
  4. `Sources (n)` expander (8.3) — n varies per answer.
  5. Follow-up chips (2–3 bordered pill buttons; **hard-bound**: submit a canonical question or navigate).
  6. Footer (11px grey-400): `Generated from your RyderShare data · Jul 7, 2026 · Verify before financial decisions`.
- **Streaming behavior:** on submit — user bubble appears instantly; typing indicator (three pulsing dots) ~600ms; answer card reveals in *sections* (headline → chart → narrative → sources/chips) at ~250ms stagger, each 200ms fade + 8px rise. No character streaming. Total under 1.5s. Input stays enabled during the reveal; Enter is ignored until it completes.
- **First open (empty thread):** 4 suggestion chips above the docked prompt bar — the canonical questions for Q1, Q2, Q3, Q4.
- **Prompt bar:** docked bottom, 720px centered, identical to S0a's.

### S3 — Reviews (auto-generated monthly business review)

Purpose: the artifact every VP in the room pays a team to assemble by hand — and the renewal-defense weapon for accounts where RyderShare's value is invisible today.

Document column, ~920px centered (it's a review with a Download button; beat 5 is one slow scroll).

- **Title block:** eyebrow `BUSINESS REVIEW · GENERATED JUL 1, 2026 · 42 SECONDS` (11px uppercase grey-400) · "Summit Beverage Group — June 2026" (20px/600) · right: `Share` + `Download PDF` buttons (both secondary, inert).
- **Executive summary card (~90 words):**
  > June was Summit Beverage Group's strongest service month of 2026: **96.2% on-time delivery** against a 95% target, on record peak volume of **1,187 loads**, with **no preventable safety incidents**. Total invoice rose **8.0% to $1.84M** — planned seasonal volume and the flex routes approved in April explain 79% of the increase, and nothing ran off-contract. Fuel exposure stayed moderate as the DOE index rose $0.19/gal. The largest open opportunities: backhaul monetization (**≈ $458K/yr gross**) and Orlando unload windows (**≈ $132K/yr**).
- **KPI grid (8 tiles, 4×2):** `ON-TIME 96.2% ▲2.1` · `COST/STOP $248 ▲$6` · `LOADS 1,187` · `SAFETY 0 preventable · 0.4/100K mi TTM ▼` · `FUEL $180K · $3.68/gal` · `EMPTY MILES 18.4% ▼0.6` · `BILLING ACCURACY 99.2%` · `DISPUTES 9 · 4.2-day avg`.
- **Invoice bridge (centerpiece):** horizontal waterfall "May $1.706M → June $1.842M": `Volume +$69.8K` · `Seasonal flex routes +$38.6K` · `Accessorials +$18.8K` · `Fuel surcharge +$9.3K`. Increase bars blue-600, endpoint bars grey-700, value labels always visible (12px), dashed grey-100 connectors.
- **Recommendations (3 numbered rows, descending dollar order):** reuse the S1 opportunity titles + bodies **verbatim** (reconciliation is part of the trust story) · green dollar chip · `Discuss with Marcus Reed →` (inert). 1. Backhaul capacity ≈$458K/yr gross · 2. Orlando unload windows ≈$132K/yr · 3. Saturday consolidation ≈$96K/yr.
- **Footer strip:** "Prepared by RyderShare Intelligence for Dana Whitfield · Data through Jun 30, 2026."

### S4 — Risk radar (the RiskAgent teaser)

Purpose: proactive, with a human hand on the wheel.

- **Title row:** "Risk radar" (20px/600) · chip `6 LOADS AT RISK · THU JUL 9` (yellow-50/yellow-900).
- **Cause banner (yellow-50 card, 3px yellow-500 left rule):** weather icon · "Tropical system expected across the Gulf Coast Thursday. Orlando and Atlanta corridors affected. Confidence: high — NWS advisory 041."
- **At-risk loads table (6 rows, data 9.7):** `LOAD` · `ROUTE` · `STOPS` · `SCHEDULED` · `RISK` (chips: `WEATHER` yellow; rows 4 and 6 add `DOCK` grey) · `RECOMMENDED ACTION`.
- **Plan card:** `RECOMMENDED PLAN` label · "Pre-load and dispatch 4 Orlando loads Wednesday evening; reroute 2 Atlanta loads via I-75 (+40 min transit). Customer deliveries unaffected. Estimated cost impact **+$1,840**; estimated avoided service failures: **6**." · Buttons: **`Approve plan`** (primary charcoal) · `Adjust` (secondary, inert).
- **Approve behavior:** button disables and swaps to `Plan approved` + inline check icon; toast slides in top-right, auto-dismisses after 5s: "Plan approved — 6 loads updated. Marcus Reed and your Orlando and Atlanta DCs have been notified."; the table's RECOMMENDED ACTION cells flip to `Scheduled` — plain 13px grey-700 text + 14px green check icon (#1F7A61). Approved state persists for the session (re-entry shows the flipped table; the S1 risk card and Q4's answer stay as static snapshots — if asked, "the answer reflects when it was generated").

## 7. Voice of the AI (copy rules for generated content)

1. Plain business English. No logistics jargon without context, no exclamation marks, no first person ("I").
2. Numbers are **bolded** in narrative text; **every displayed figure traces to Section 9** — no orphan numbers.
3. Always attribute causes ("planned seasonal volume and the flex routes approved in April") — the AI explains; it never just reports.
4. Never overclaim: "≈" on projections, "estimated" on modeled numbers, "gross" vs. "to you" stated explicitly on shared-revenue figures, the verify footer on every answer.
5. Zero emojis. Sentence case everywhere except the product's existing uppercase micro-labels.

## 8. Ask RyderShare — conversation spec

### 8.1 Prompt bar
Rounded-full (24px radius), 1px grey-100 border, white bg; sparkle icon left (16px, blue-600); placeholder 13px grey-200. Focus: border grey-400 + shadow `0 2px 8px rgba(0,0,0,0.08)`. Enter submits (ignored while an answer is revealing); a circular charcoal submit button (arrow-up icon) appears at right when input is non-empty (replacing the `NEW` chip on S0a's bar). Empty-input Enter opens S2's empty state.

### 8.2 Keyword routing — typed input only
Lowercase the input; **replace punctuation with spaces** (never delete — "on-time" must become "on time", not "ontime"); collapse whitespace; first match wins. Match whole words for `late` (word-boundary — "calculate"/"later" must not match).

| Priority | Input contains any of | Answer |
|---|---|---|
| 1 | `invoice` · `bill` · `higher` · `charge` | Q2 |
| 2 | `enroll` · `enrollment` · `involve` | Q5 |
| 3 | `backhaul` · `empty` · `return` | Q3 |
| 4 | `saturday` · `consolidate` · `consolidation` · `utilization` | Q6 |
| 5 | `risk` · `storm` · `weather` · `late` (whole word) | Q4 |
| 6 | `perform` · `otd` · `on time` · `ontime` · `month` · `kpi` · `metric` · `fleet` | Q1 |
| — | anything else | Fallback (8.5) |

Canonical questions (used by chips/cards — hard-bound, never routed): Q1 `How did my fleet perform last month?` · Q2 `Why was my June invoice 8% higher than May?` · Q3 `How much is my empty backhaul worth?` · Q4 `Which loads are at risk this week?` · Q5 `What would backhaul enrollment involve?` · Q6 `Could we consolidate my Saturday routes?`

### 8.3 Sources expander (the trust pattern — non-negotiable)
Collapsed: `Sources (n) ⌄` 12px blue-600 link — n is per answer. Expanded: bordered sub-card, one row per source — document/database line icon + label (13px) + meta (12px grey-400). Rows hover to grey-25 but are inert. **Source registry (every citation anywhere in the prototype uses exactly these rows):**
- `Invoice SBG-2026-06 · 214 line items · issued Jul 1, 2026`
- `Load records · 1,187 loads · Jun 1–30, 2026`
- `DOE/EIA national diesel index · June 2026`
- `Contract SBG-DTS-2024 · rate schedule C`
- `Site telemetry · 4 DC feeds · Jun–Jul 2026`
- `NWS advisory 041 · issued Jul 6, 2026`
- `Load schedule · week of Jul 6, 2026`
- `Ryder network freight availability · June 2026`
- `Market rate index · dry van blend · June 2026`

This is the "show your work" principle from the MCP thesis — every answer cites the governed records behind it, so the room sees auditable data access rather than an oracle.

### 8.4 The six scripted answers

**Q1 — "How did my fleet perform last month?"**
- Headline: "June was your strongest service month of 2026 — 96.2% on-time on record volume."
- Visual: compact KPI strip (OTD 96.2% ▲2.1 · Cost/stop $248 ▲$6 · Loads 1,187 · Empty miles 18.4% ▼0.6) above the 8-week OTD line chart (reuse S1's).
- Narrative: "On-time delivery met or beat your **95%** target for the fifth straight week, helped by better dwell-time estimates at Memphis and April's dispatch change. Of **12** missed stops, **9** have documented causes — dock congestion at two Tampa retailers accounts for most. **No preventable safety incidents** in June; the trailing rate is **0.4 per 100K miles**, ahead of plan. Cost per stop rose **$6** on peak volume, in line with your seasonal plan."
- Sources (3): Load records · Site telemetry · Invoice SBG-2026-06.
- Chips: `Why was my June invoice 8% higher than May?` → Q2 · `Which loads are at risk this week?` → Q4.

**Q2 — "Why was my June invoice 8% higher than May?" (the money moment)**
- Headline: "Your June invoice rose $136.5K (8.0%) — 79% of it is the planned seasonal volume and flex capacity approved in April."
- Visual: waterfall — May $1.706M → `Volume +$69.8K` → `Seasonal flex routes +$38.6K` → `Accessorials +$18.8K` → `Fuel surcharge +$9.3K` → June $1.842M. (Headline and chart must visibly agree: volume + flex = $108.4K = 79%.)
- Narrative: "Volume added **45 loads** over May at summer peak, and the **two flex routes** added June 1 carried their planned fixed cost. Accessorials ran **$18.8K** — half of it driver unload surge at **Orlando DC-04** (11 events vs. a typical 4). The fuel surcharge added **$9.3K** as the DOE index rose **$0.19/gal**. Nothing ran off-contract; the one avoidable item is Orlando unload windows — worth **≈ $132K/yr**."
- Sources (4): Invoice SBG-2026-06 · Contract SBG-DTS-2024 · DOE/EIA index · Load records.
- Chips: `How much is my empty backhaul worth?` → Q3 (⚠ demo-critical) · `How did my fleet perform last month?` → Q1.

**Q3 — "How much is my empty backhaul worth?" (aimed at Tom)**
- Headline: "About $8.8K a week — ≈ $458K a year gross — on three return lanes that run empty today."
- Visual: lane table — `MEM → DAL · 1,860 empty mi/wk · ≈ $3.9K/wk` · `ATL → MEM · 1,410 · ≈ $2.9K/wk` · `ORL → ATL · 1,030 · ≈ $2.0K/wk` (registry 9.8; no schematic — the table carries it).
- Narrative: "**18.4%** of your fleet miles ran empty in June, mostly on your inter-DC transfer and inbound legs. Three return lanes are consistent enough to match against Ryder-managed network freight — an estimated **$458K/yr gross** at current market rates (≈ **$2.05/mi** blended), roughly **$320K/yr to SBG** under a typical revenue share. Lanes enroll individually; **MEM → DAL alone is 44%** of the opportunity."
- Sources (3): Load records · Ryder network freight availability · Market rate index.
- Chips: `What would backhaul enrollment involve?` → Q5 · `Show my June business review` → navigates to S3.

**Q4 — "Which loads are at risk this week?"**
- Headline: "6 loads are at risk Thursday from the Gulf storm — a mitigation plan is ready."
- Visual: compact 6-row at-risk table (same data as S4, 9.7).
- Narrative: "A tropical system is expected across the Gulf Coast **Thursday, July 9**. Four Orlando loads can pre-load Wednesday evening; two Atlanta loads reroute via I-75 with **+40 minutes** transit. Estimated cost impact **+$1,840** against **6** avoided service failures."
- Sources (3): NWS advisory 041 · Load schedule · Site telemetry.
- Chips: `Open Risk radar` → navigates to S4 · `Why was my June invoice 8% higher than May?` → Q2.

**Q5 — "What would backhaul enrollment involve?" (Tom's follow-up, scripted so it never dead-ends)**
- Headline: "Lane by lane, starting where the money is — no contract restructuring to begin."
- Visual: three numbered rows (table-style): `1 · Opt in per lane — MEM → DAL first (44% of the opportunity)` · `2 · Ryder's network desk matches your empty legs against Ryder-managed freight; you approve standing schedules` · `3 · Credits net against your monthly invoice under a per-lane revenue-share rider`.
- Narrative: "Enrollment is per lane, so SBG can start with **MEM → DAL** and expand as the credits prove out. At the estimated **$458K/yr gross**, a typical share returns **≈ $320K/yr to SBG**. Your Ryder team models the exact split and standing schedule before anything is committed."
- Sources (2): Contract SBG-DTS-2024 · Ryder network freight availability.
- Chips: `How much is my empty backhaul worth?` → Q3 · `Show my June business review` → navigates to S3.

**Q6 — "Could we consolidate my Saturday routes?" (kills the last dead-end)**
- Headline: "Yes — three Saturday Atlanta routes ran at 61% average trailer utilization in June; two could carry the volume."
- Visual: route table — `ATL-SAT-A · 68% util` · `ATL-SAT-B · 59%` · `ATL-SAT-C · 56%` · `Consolidated (2 routes) · ≈ 87% est.` (9.8).
- Narrative: "All Saturday stops fit a two-route plan within existing **6 AM–2 PM** delivery windows, releasing one tractor and crew per Saturday — **≈ $8K/mo, ≈ $96K/yr**. Service risk is low: the modeled plan keeps every stop inside its current window."
- Sources (2): Load records · Load schedule.
- Chips: `Why was my June invoice 8% higher than May?` → Q2 · `How much is my empty backhaul worth?` → Q3.

### 8.5 Fallback (any unscripted typed input)
Answer card, no chart, **no sources expander** (it claims no data): "In the live product this would be answered from your RyderShare data. This prototype scripts a handful of questions — try one of these." + the four primary suggestion chips (Q1–Q4). Same honesty footer. Never fake an answer — the honest fallback is part of the pitch.

## 9. Data pack (single source of truth — every displayed figure reconciles to this)

### 9.1 Account
Summit Beverage Group (SBG) · Ryder DTS since 2021 · DCs: Dallas DC-01, Memphis DC-02, Atlanta DC-03, Orlando DC-04 · 46 tractors · 71 drivers (driver + helper crews; driver unload standard) · ~275 loads/wk · multi-stop retail delivery.

### 9.2 June 2026 headline metrics
| Metric | June | May | Delta |
|---|---|---|---|
| Loads delivered | 1,187 | 1,142 | +45 |
| Stops | 7,441 | 7,046 | +395 |
| On-time delivery | 96.2% | 94.1% | ▲ 2.1 pts |
| Total invoice | $1,842,300 | $1,705,800 | +$136.5K (+8.0%) |
| Cost per stop | $248 | $242 | ▲ $6 |
| Fuel | $179,600 · 48.8K gal · DOE $3.68/gal | $170,100 · DOE $3.49 | DOE ▲ $0.19 |
| Empty miles | 18.4% | 19.0% | ▼ 0.6 pt |
| Billing accuracy | 99.2% · 9 disputes · 4.2-day avg resolution | — | — |
| Missed stops | 12 (9 with documented cause) | — | — |
| Safety | 0 preventable incidents · 0.4/100K mi TTM (ahead of plan) | — | — |

### 9.3 Invoice bridge (sums exactly to +$136,500)
Volume +$69,800 · Seasonal flex routes +$38,600 · Accessorials +$18,800 · Fuel surcharge +$9,300. Accessorial split: driver unload surge $9,400 · layover $4,200 · redeliveries $3,600 · detention $1,600 — 11 unload-surge events at Orlando DC-04 vs. a typical 4/month (the digest's "nearly 3×"). Volume + flex = $108,400 = 79% of the increase.

### 9.4 Opportunities (annualized; "≈" always; identical wherever shown)
Backhaul ≈$458K/yr **gross** (≈$320K/yr to SBG at a typical revenue share) · Orlando unload windows ≈$132K/yr · Saturday consolidation ≈$96K/yr.

### 9.5 Series
OTD 8 weeks: 93.8 · 94.4 · 94.1 · 95.0 · 95.6 · 96.0 · 96.3 · 96.2 (target 95 — week 4 ties it; copy says "met or beat"). Cost/stop 6 months: 251 · 246 · 244 · 240 · 242 · 248.

### 9.6 Shipments board — the exact 12 rows
Status-overview band (This week): PLANNED 18 · DISPATCHED 26 · STARTED 34 · COMPLETED 189 · RUNNING LATE 3 (sum 270 ≈ weekly volume; the board below is page 1 — no caption needed). **No board row reuses a 9.7 at-risk ID.**

| REFERENCE # | RYDER # | STATUS | ORIGIN | DESTINATION | STOPS | NEXT STOP ETA | UPDATED |
|---|---|---|---|---|---|---|---|
| SBG-31240 | 884210331 | STARTED | Orlando DC-04 · Orlando, FL | Tampa retail loop · Tampa, FL | 3/8 | 2:40 PM ET · Jul 7 | 8m ago |
| SBG-31241 | 884210332 | STARTED · RUNNING LATE | Atlanta DC-03 · Atlanta, GA | Savannah corridor · Savannah, GA | 2/5 | Running late: 4:15 PM ET | 3m ago |
| SBG-31242 | 884210333 | STARTED | Dallas DC-01 · Dallas, TX | Fort Worth metro · Fort Worth, TX | 5/7 | 1:55 PM CT · Jul 7 | 12m ago |
| SBG-31243 | 884210334 | STARTED · RUNNING LATE | Memphis DC-02 · Memphis, TN | Nashville retail · Nashville, TN | 1/6 | Running late: 3:05 PM CT | 6m ago |
| SBG-31244 | 884210335 | DISPATCHED | Orlando DC-04 · Orlando, FL | Jacksonville run · Jacksonville, FL | 0/6 | 3:30 PM ET · Jul 7 | 15m ago |
| SBG-31245 | 884210336 | DISPATCHED | Atlanta DC-03 · Atlanta, GA | Macon/Columbus · Macon, GA | 0/6 | 4:10 PM ET · Jul 7 | 21m ago |
| SBG-31246 | 884210337 | PLANNED | Dallas DC-01 · Dallas, TX | Austin corridor · Austin, TX | 0/9 | Appointment 6:00 AM CT · Jul 8 | 34m ago |
| SBG-31247 | 884210338 | STARTED | Memphis DC-02 · Memphis, TN | Little Rock loop · Little Rock, AR | 4/6 | 2:20 PM CT · Jul 7 | 9m ago |
| SBG-31248 | 884210339 | STARTED | Orlando DC-04 · Orlando, FL | Miami corridor · Miami, FL | 6/9 | 5:45 PM ET · Jul 7 | 5m ago |
| SBG-31249 | 884210340 | COMPLETED | Atlanta DC-03 · Atlanta, GA | Athens retail · Athens, GA | 5/5 | Delivered 11:32 AM ET | 1h ago |
| SBG-31250 | 884210341 | COMPLETED | Dallas DC-01 · Dallas, TX | Waco run · Waco, TX | 7/7 | Delivered 10:58 AM CT | 1h ago |
| SBG-31251 | 884210342 | COMPLETED | Memphis DC-02 · Memphis, TN | Jackson loop · Jackson, TN | 6/6 | Delivered 12:04 PM CT | 46m ago |

Drivers are not a board column (matches the real product). 

### 9.6b Network view (8 cards = 8 markers)
The 8 in-motion rows above (SBG-31240–31248, excluding PLANNED 31246): 6 blue (on-time), 2 yellow (31241, 31243 — the running-late pair). Tabs: `Location (8)` / `No location (1)`. Map pills: `White glove (2)` (31242, 31248) · `Running late (2)`. Marker positions: FL ×3 (Tampa, Jacksonville, Miami corridors), GA ×2 (Savannah, Macon), TX ×1 (Fort Worth), TN ×1 (Nashville), AR ×1 (Little Rock) — matching the 8 in-motion rows exactly. The band's third late load is a non-GPS unit — if anyone asks, that's the data-trust story, and it's why `No location (1)` exists.

### 9.7 At-risk loads (6 — Thursday, distinct ID range)
`SBG-31307 · ORL → Tampa retail loop · 8 · Thu 6:00 AM · WEATHER` · `SBG-31309 · ORL → Jacksonville run · 6 · Thu 7:30 AM · WEATHER` · `SBG-31315 · ORL → Miami corridor · 9 · Thu 5:15 AM · WEATHER` · `SBG-31321 · ORL → Orlando metro · 7 · Thu 8:00 AM · WEATHER + DOCK` · `SBG-31288 · ATL → Savannah corridor · 5 · Thu 9:45 AM · WEATHER` · `SBG-31294 · ATL → Macon/Columbus · 6 · Thu 10:30 AM · WEATHER + DOCK`. Actions: rows 1–4 `Pre-load Wed 6:00 PM` · rows 5–6 `Reroute via I-75 (+40 min)`.

### 9.8 Modeled-figure registry (everything else displayed anywhere)
- Backhaul lanes: MEM→DAL 1,860 empty mi/wk ≈ $3.9K/wk · ATL→MEM 1,410 ≈ $2.9K/wk · ORL→ATL 1,030 ≈ $2.0K/wk → $8.8K/wk → ≈$458K/yr gross → ≈$320K/yr to SBG (typical share) · blended rate ≈$2.05/mi · MEM→DAL = 44% of total.
- Saturday routes: ATL-SAT-A 68% · ATL-SAT-B 59% · ATL-SAT-C 56% (avg 61%) → consolidated 2-route plan ≈87% est. · windows 6 AM–2 PM hold · ≈$8K/mo → ≈$96K/yr.
- Storm plan: +$1,840 est. cost (pre-load overtime ≈$1,040 + reroute fuel/time ≈$800) · +40 min transit on reroutes · 6 avoided service failures.
- Unload surge norm: 4 events/typical month vs 11 in June ("nearly 3×").
- Review generation time: **42 seconds** (S3 eyebrow + beat 5 line).
- Missed-stop concentration: dock congestion at **two Tampa retailers** (Q1 narrative).
- Source-row metas (e.g., "214 line items") are registered in the 8.3 source registry, which serves as §9's extension for citation chrome.

## 10. Design system (ground truth: RyderShare 2.0 Figma, June 2026)

### 10.1 Principles
Color carries status semantics only — everything else is near-black on white. Red is brand, never data. Density is high, decoration is zero, motion is minimal. The AI layer answers in the same chip/card/table vocabulary as the rest of the product so it reads as RyderShare growing up, not a bolt-on. **Where these tokens conflict with the reference PNGs or any older artifact, this section wins.**

### 10.2 Tokens
```
Brand:    Ryder red #CE1126 (emblem, rail active edge, tab underline, Insights NEW dot,
          digest left-accent). NEVER buttons, charts, or status.
Greys:    900 #1D1D20 (primary text) · 700 #303235 (rail bg, charcoal buttons)
          500 #44464B (logo "SHARE", strong secondary) · 400 #696B6F (secondary text)
          200 #A9AAAC (placeholder) · 100 #C5C6C7 (input borders) · 75 #E3E4E5 (card/table
          borders) · 50 #ECEDED · 25 #F5F6F6 (recessed bg, hover) · white #FFFFFF
Blue:     600 #307CA7 (links, charts, progress, on-time markers) · tint #ECF4F9
Yellow:   500 #F0C005 (late markers/bars) · 50 #FEF9E6 (chip bg) · 900 #655102 (chip text)
Green:    #1F7A61 for ALL green text at UI sizes · tint bg #E8F5F0 · #34A081 only for
          large/graphic uses (≥18px or shapes)
Type:     Inter (embedded) + system fallback. Page titles 20/600 · S1 greeting 24/600 ·
          answer headlines 15/600 · S2 header 16/600 · section labels 11/500 UPPERCASE
          +0.04em grey-400 · body 13–14/400 · emphasized 14/600 · KPI numbers 26/600
          tabular-nums · meta 12/400 · chips 11/500 UPPERCASE. No monospace anywhere.
Cards:    white · 1px #E3E4E5 · 8px radius · shadow 0 1px 3px rgba(0,0,0,0.15) (whisper).
Chips:    UPPERCASE tinted — PLANNED #FEF9E6/#655102 (cream, per product) ·
          DISPATCHED #ECF4F9/#276A92 · STARTED #E8F5F0/#1F7A61 · COMPLETED #E8F5F0/#1F7A61 ·
          RUNNING LATE #FEF9E6/#655102 · WEATHER #FEF9E6/#655102 · DOCK #F5F6F6/#44464B ·
          NEW + CONCEPT #FEF9E6/#655102.
Tables:   horizontal 1px #E3E4E5 dividers only · headers 11px/500 UPPERCASE grey-400 ·
          S0a rows ~84px (two-line cells, per product) · other tables 44px · hover #F5F6F6.
Buttons:  primary = charcoal #303235 bg, white text, 6px radius, 13px/500;
          secondary = white, 1px #C5C6C7, grey-700 text.
Filter chips: bordered pill, icon + label + caret, 13px; active = #ECF4F9 tint.
Charts:   single-hue #307CA7 on white · horizontal gridlines #ECEDED only · axis 11px
          grey-400 · value labels 12px grey-700 · 300ms fade-in max · no gradients/3D.
Tooltips: charcoal #303235 bg · white 11px text · 4px radius · 6px/8px padding
          (chart hovers + freshness tooltips).
Progress: 4px bars — blue-600 on grey-50 track; yellow-500 when running late.
Focus:    2px #307CA7 outline, 2px offset, :focus-visible only.
AI accent: sparkle icon (blue-600) + NEW/CONCEPT chips + the digest's red left rule.
          Nothing glows, nothing is purple, no gradient "AI shimmer". Calm capability.
```

### 10.3 Component reuse map
Status overview band, board table, status chips, filter chips, freshness text/tooltips, card-list + map (Network), progress bars → reuse exactly as shipped (match `reference-screens/`). New (sanctioned) components: KPI cards, line/bar/waterfall charts, AI digest card, prompt bar, answer cards, sources expander, opportunity cards, plan card, toast. Each new component uses existing borders, radii, type ramp, and chip vocabulary.

### 10.4 Motion budget
Hover 150ms; answer-section reveal 200ms fade + 8px rise, 250ms stagger; typing dots pulse; toast slide 200ms, auto-dismiss 5s; chart fade-in 300ms once; approve state swap instant; band collapse 200ms. Nothing else moves. `prefers-reduced-motion`: all reveals instant.

### 10.5 Static SVG map spec (S0b + marker click cards)
Landmass fill #F5F6F6 on white; state borders 1px #E3E4E5; no labels except four city dots (3px grey-400) labeled DAL · MEM · ATL · ORL (11px grey-400). Simplified Southeast outline (TX→FL, up through TN and AR — all five marker states visibly inside the frame) — geographic *impression*, not cartographic accuracy. Markers: 22px circles (blue-600 / yellow-500) with a white directional-arrow glyph, whisper shadow; positions per 9.6b. White pill overlays per S0b. The map never pans or zooms.

## 11. What the prototype must make the room feel

1. **Recognition → evolution.** Beats 1–2 must look like the RyderShare Tom's team has seen so beats 3–6 read as the same product growing. The shell, chips, and table patterns do this work — treat them as load-bearing.
2. **Trust.** Sources on every answer, verify footers, freshness timestamps, a human approving every action, and an honest fallback that never fakes an answer. The AI shows its work — that grammar comes straight from the data-trust roadmap and the MCP thesis, and it is what separates this from a chatbot demo.
3. **Money.** Every insight carries a dollar figure; the backhaul pair (value → enrollment) carries the biggest and is aimed at Tom — with gross vs. share stated plainly, because a hedged number he can trust beats a big one he has to correct.
4. **Scoped differentiation.** On-screen, the prototype never name-drops competitors. The spoken claim uses Section 1's hedged formulation verbatim; the Penske rebuttal is Appendix B.

## 12. Acceptance checklist (Claude Design self-verifies)

- [ ] Opens from `file://` with network disabled — fonts degrade cleanly, map renders (it's inline SVG), zero external requests in DevTools
- [ ] Lands on `#/shipments`; all 5 rail destinations render; unknown hash → `#/shipments`; S2 back arrow returns to the screen that opened it; no rail item active on `#/ask`
- [ ] Demo path in order with zero dead ends: S0a → Network → Insights → type "Why was my June invoice 8% higher than May?" → Q2 → chip → Q3 → chip → Q5 renders (Tom's follow-up) → rail Reviews → S1 risk card → S4 → Approve → toast + table flip + button disables
- [ ] All six questions answer correctly when typed (8.2 rules: punctuation→spaces, `late` word-boundary) and via hard-bound chips/cards; unscripted input hits the fallback (no sources expander on fallback)
- [ ] Digest links navigate (#/risk, #/reviews); `Sources (n)` expanders open/close on digest + all six answers, using only 8.3 registry rows
- [ ] Every displayed figure appears in Section 9 (spot-checks: bridge sums +$136.5K and headline "79%" = volume+flex; $458K gross / $320K share consistent across Q3, Q5, S1, S3; 96.2% everywhere; no date shows the review generated before Jul 1)
- [ ] Tokens match 10.2 — "SHARE" grey-500; red only in the 5 sanctioned spots; charts single-hue blue; PLANNED chip cream; small green text #1F7A61; no emojis; no monospace; no gradients or glows
- [ ] Free exploration is safe: every visible control works or fails silently; S4 approve is idempotent; reload resets cleanly; footer badge on every screen; `prefers-reduced-motion` honored; clean at 1440×900 and 1280×800

## 13. Open decisions (Isaac)

1. **Naming:** "RyderShare Intelligence" + "Ask RyderShare" are placeholders (alternatives: RyderShare IQ, RS Copilot). The `CONCEPT` chip keeps naming low-stakes for the room.
2. **Customer identity:** synthetic SBG vs. an anonymized profile shaped like a marquee DTS account. Synthetic is the safe default in a leadership room; the multi-DC beverage archetype keeps it relatable.
3. **Power BI framing — recommended resolution:** say "this is the RyderShare-native reporting experience your team asked for in June" (their words; no Power BI mention, no chatbot mention). If pressed on other AI efforts: "ours is grounded in the records that run the product — one system of record, one answer." The prototype supports either posture.
4. **Beat 6 (Risk radar)** drops first if time collapses, then beat 5 (already encoded in the interruption protocol).
5. Post-demo, per Tom's note: the close now commits to structured feedback with 2–3 current RS customers this quarter + a sized proposal to follow. Discovery mechanics stay out of prototype scope.

## Appendix A — reference screenshots (attach alongside this PRD)

In `reference-screens/`: `mission-control-core-desktop.png` (Network layout ground truth) · `load-board-list.png` (board + status band ground truth) · `status-overview-cards.png` (band styling) · `details-page-redesign.png` (current detail patterns) · `search-filters-list.png` (filter chips) · `mission-control-details.png` (chips/cards in context). Match these for pattern, then apply 10.2 tokens as law.

## Appendix B — presenter's Q&A (talk track only; not part of the build)

1. **"That $458K — whose money is it, and who finds the freight?"** Gross at market rates (≈$2.05/mi blended). Under a typical revenue share, roughly $320K lands with the customer — and that's the point: it's their money we're finding. Ryder's network desk sources and matches the freight; lanes enroll one at a time, MEM→DAL first at 44% of the opportunity. (The prototype answers this — Q3 and Q5.)
2. **"What would it take to build — cost and when?"** Phased: the digest and generated reviews ride on data RyderShare already collects — nearer-term; the conversational layer is gated on the LLM platform path maturing. Commit to a sized proposal in two weeks. **Do not improvise a dollar figure in the room.**
3. **"Can I put this in front of [marquee account] next week?"** Yes, as a concept — the CONCEPT chip and the honest fallback protect it. And that is exactly the customer-feedback step Tom asked for: propose them as the first structured session.
4. **"How is this different from the chatbot TM is bringing in, or Power BI Copilot?"** Never name-check. Answer on grounding: every answer cites the governed records that run the product — one system of record, one answer. A BI copilot reports on an extract; this explains the operation and acts on it, with a human approving.
5. **"Who else has this — what about Penske?"** Use Section 1's hedged claim verbatim. Catalyst AI is benchmarking analytics for fleet management — no conversational interface, no dedicated cost/billing intelligence. The adjacent proof (project44, FourKites, Uber Freight) is exactly why the window is 12–18 months, not forever.
6. **If the board counts get questioned** ("275 a week — why do the tiles say 270, and why only 12 rows?"): the status band covers this week (270 loads and counting); the table is page 1 of that window; the Network map shows located actives only, so its Running-late pill reads 2 while the band reads 3 — the third late load is a non-GPS unit, which is exactly the data-trust roadmap's point, not a bug.
