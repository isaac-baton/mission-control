# Mission Control Dashboard — Design Spec v2
### Rydershare Product-Aligned Design | Light Theme
**Designer:** Senior Product Designer
**Date:** 2026-03-18
**Status:** Replaces v1 (dark theme "Radius" spec). Aligned to actual Rydershare product visual language from Figma source files.

---

## 0. Design Philosophy

This spec treats Mission Control as a **new page within the existing Rydershare application**, not a standalone product. It must feel like a natural extension of the tool Ryder operators already use daily. Every component should pass the test: "Could this exist on the same screen as the existing shipment detail view?"

**Guiding principles:**
- Match the product, not a mood board. White backgrounds, clean borders, no visual drama.
- Functional density over visual spectacle. Ops users need information, not atmosphere.
- New capabilities (KPI cards, fleet map, severity hierarchy) are introduced as tasteful extensions of existing patterns, not as foreign elements.
- Zero gratuitous animation. Motion only where it communicates state change.

---

## 1. Layout Architecture

### The Rydershare Shell (Existing — Do Not Modify)

The application shell is fixed. Mission Control lives inside it.

```
┌──────┬──────────────────────────────────────────────────────┐
│      │  RYDERSHARE          Report an issue    (avatar)     │
│ ICON │  ─────────────────────────────────────────────────── │
│ NAV  │                                                      │
│      │                 MAIN CONTENT AREA                    │
│ ~44px│                                                      │
│      │           (this is what we design)                   │
│      │                                                      │
│      │                                                      │
│      │                                                      │
└──────┴──────────────────────────────────────────────────────┘
```

**Sidebar (~44px):** Dark/near-black, icon-only navigation. Mission Control gets a new icon here — a radar/dashboard icon. Active state: white icon, possibly with a left accent bar matching the product's existing active indicator pattern.

**Header bar:** White background, RYDERSHARE logo left, "Report an issue" + user avatar right. Unchanged.

### Main Content Area Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Mission Control                              [Filter bar]  │
│  ─────────────────────────────────────────────────────────  │
├────────────┬────────────┬────────────┬──────────────────────┤
│  KPI Card  │  KPI Card  │  KPI Card  │     KPI Card        │
│  In Transit│  Exceptions│  On-Time % │     Avg Resolution   │
├────────────┴────────────┴────────────┴──────────┬───────────┤
│                                                  │           │
│               FLEET MAP                          │ PRIORITY  │
│          (Google Maps style)                     │  QUEUE    │
│                                                  │           │
│                                                  │  (card    │
│                                                  │   list)   │
│                                                  │           │
├──────────────────────────────────────────────────┴───────────┤
│  SHIPMENT TABLE                                              │
│  (full width, existing table pattern)                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Spacing & Grid

| Property | Value | Rationale |
|----------|-------|-----------|
| Content max-width | Fluid (no max-width) | Matches existing product — content stretches to fill |
| Content padding | 24px horizontal, 20px top | Matches existing page padding from Figma |
| Section gaps | 16px vertical | Consistent with product's vertical rhythm |
| Card internal padding | 16px–20px | Matches existing summary card padding |
| Table row height | ~44px | Matches existing shipment table |
| Page title margin-bottom | 20px | Matches existing pages |

---

## 2. Color System — Product-Aligned

### Surface Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-page` | `#FFFFFF` | Main content background |
| `--bg-subtle` | `#F9FAFB` | Alternating table rows, recessed areas |
| `--bg-card` | `#FFFFFF` | Card backgrounds |
| `--border-default` | `#E5E7EB` | Card borders, table row dividers, section dividers |
| `--border-strong` | `#D1D5DB` | Input borders, active card borders |

### Text Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--text-primary` | `#1A1A1A` | Page titles, primary values, shipment IDs |
| `--text-secondary` | `#6B7280` | Descriptions, secondary info, carrier names |
| `--text-label` | `#9CA3AF` | UPPERCASE column headers, field labels |

### Status Colors (Matched to Existing Product)

These are pulled directly from the Rydershare Figma files. Each status uses colored text on a tinted background pill.

| Status | Text Color | Background | Border | Product Match |
|--------|-----------|------------|--------|---------------|
| STARTED | `#16A34A` | `#F0FDF4` | `#BBF7D0` | Green on light green |
| PLANNED | `#6B7280` | `#F3F4F6` | `#E5E7EB` | Grey on light grey |
| DISPATCHED | `#2563EB` | `#EFF6FF` | `#BFDBFE` | Blue on light blue |
| IN TRANSIT | `#2563EB` | `#EFF6FF` | `#BFDBFE` | Blue on light blue (same as dispatched) |
| COMPLETED | `#16A34A` | `#F0FDF4` | `#BBF7D0` | Green on green |
| CANCELLED | `#DC2626` | `#FEF2F2` | `#FECACA` | Red on light red |

### Exception/Severity Colors (New for Mission Control)

These extend the product palette for severity hierarchy — a concept the product needs but doesn't yet have explicit tokens for. The exception patterns already exist (amber triangle, red circle) in the data tables.

| Severity | Text Color | Background | Icon | Existing Product Precedent |
|----------|-----------|------------|------|---------------------------|
| Critical | `#DC2626` | `#FEF2F2` | Red circle (existing) | Red exception count in tables |
| Warning | `#D97706` | `#FFFBEB` | Amber triangle (existing) | Amber warning icon in tables |
| Info | `#2563EB` | `#EFF6FF` | Blue info circle | Blue text pattern |
| Normal | `#6B7280` | `#F3F4F6` | None | Grey/neutral pattern |

### Accent Color

The product uses teal/blue-green as its subtle accent (links, "View all" actions). NOT purple or magenta.

| Token | Value | Usage |
|-------|-------|-------|
| `--accent` | `#0D9488` (teal-600) | "View all" links, interactive highlights |
| `--accent-hover` | `#0F766E` (teal-700) | Link hover states |

---

## 3. Typography

**Font family:** Inter (or the system sans-serif stack the product uses — visually Inter-like)

**Critical rule:** NO monospace font (JetBrains Mono) anywhere. The product does not use monospace for numbers, IDs, timestamps, or anything else. All text is the same sans-serif.

| Element | Size | Weight | Case | Spacing | Product Reference |
|---------|------|--------|------|---------|------------------|
| Page title ("Mission Control") | 24px | 700 (Bold) | Sentence | Normal | Matches "Shipment Details" title |
| KPI number | 28px | 600 (Semi-bold) | Normal | -0.01em | New — larger than anything in product, but proportional |
| KPI label | 11px | 500 | UPPERCASE | 0.05em | Matches column header pattern |
| Section heading | 16px | 600 | Sentence | Normal | Matches sub-headings |
| Table column header | 10–11px | 500 | UPPERCASE | 0.05em | Exact match to existing table headers |
| Table body text | 13–14px | 400 | Normal | Normal | Exact match to existing table rows |
| Filter pill text | 13px | 400 | Normal | Normal | Matches existing filter dropdowns |
| Badge/status text | 11px | 500 | UPPERCASE | 0.03em | Matches existing status pills |
| Timestamp / meta | 12px | 400 | Normal | Normal | Matches existing secondary text |
| "View all" links | 13px | 500 | Normal | Normal | Matches existing teal links |

### Font Variant

```css
font-variant-numeric: tabular-nums;
```

Apply to KPI numbers and table columns with numeric data. This ensures columns align without needing a monospace font.

---

## 4. Component Mapping

### 4a. Page Header & Filter Bar

**What exists in the product:** A horizontal row of pill-shaped dropdown filters with rounded borders. Some pills have leading icons (search magnifier, calendar, location pin, tractor icon, trailer icon). Active filters have a green fill. A "Reset" text link and "Copy search link" action sit at the right.

**For Mission Control:**

```
Mission Control                    [🔍 Search] [📅 Date range ▾] [📍 Region ▾] [🚛 Carrier ▾] [⚠ Severity ▾]  Reset
```

- Page title: "Mission Control" in 24px bold, left-aligned
- Filter pills: Identical to existing product filters — rounded border (`border-radius: 20px`), `1px solid #E5E7EB`, padding `8px 16px`, 13px text
- Filter icons: Same icon style as existing (search magnifier, calendar, location pin)
- Active filter: Light green fill (`#F0FDF4`) with green border (`#BBF7D0`) — exactly matching existing active filter styling
- "Reset" link: Teal color, right side
- **New filter: "Severity"** — dropdown with Critical / Warning / All options. Uses the exception amber/red colors inside the dropdown.

**What NOT to do:** No "global status pulse dot" next to the title. No UTC clock display. No notification bell. These are not patterns the product uses.

### 4b. KPI Strip (4 Summary Cards)

**What exists in the product:** Rows of bordered summary cards at top of pages (visible in shipment detail view). Bordered, not shadowed. Key-value pair layout.

**For Mission Control — extending the pattern:**

Four cards in a horizontal row. Each card:
- White background (`#FFFFFF`)
- `1px solid #E5E7EB` border
- `border-radius: 8px`
- Internal padding: `16px 20px`
- NO shadow (product cards don't use shadow)
- NO gradient backgrounds
- NO sparkline charts
- NO glow effects

**Card content structure:**

```
┌─────────────────────┐
│  LABEL              │  ← 11px, uppercase, grey (#9CA3AF), letter-spaced
│  247                │  ← 28px, semi-bold, dark (#1A1A1A)
│  ▲ 3 from 1hr ago  │  ← 12px, colored by direction (red up = bad, green down = good)
└─────────────────────┘
```

**The four cards:**

1. **IN TRANSIT** — count of active shipments. Neutral (dark text, no severity color).
2. **EXCEPTIONS** — active exception count. If > 0, the number uses `#DC2626` (red) to match the existing red exception count pattern in tables.
3. **ON-TIME RATE** — percentage. Green text if >= 95%, amber if 90-95%, red if < 90%.
4. **AVG RESOLUTION** — hours. Neutral unless above threshold.

**Trend indicator:** Small up/down arrow + context text. Uses semantic colors (red = worsening, green = improving). Arrow is a simple 10px SVG chevron, not an elaborate icon.

**Why no sparklines:** The product has zero chart/sparkline patterns. Introducing them in a KPI card would be visually foreign. The trend arrow + text gives the same directional information without introducing a new visual pattern.

### 4c. Fleet Map

**What exists in the product:** Standard Google Maps integration. Route shown as blue dashed line. Numbered circular stop markers. Clean, minimal styling — the map is just a map, not a dark artistic rendering.

**For Mission Control:**

- **Map provider:** Google Maps, standard light style (NOT dark tiles, NOT stylized)
- **Container:** White card with `1px solid #E5E7EB` border, `border-radius: 8px`, no shadow
- **Map header inside card:** "FLEET OVERVIEW" label in 11px uppercase grey, matching section title pattern
- **Shipment markers:** Colored circles matching the status system:
  - Critical exception: Red circle (`#DC2626`), matching existing red exception indicator
  - Warning exception: Amber circle (`#D97706`), matching existing amber triangle pattern
  - Normal/on-track: Teal/blue circle (`#2563EB`), matching existing in-transit blue
  - Distribution centers: Small grey diamond markers with subtle outline
- **Cluster behavior:** At zoom levels where markers overlap, show a numbered cluster circle (grey background, dark text, count number) — standard Google Maps marker clustering
- **Route lines:** Blue dashed lines for active routes, matching existing detail view route rendering
- **Click interaction:** Clicking a marker opens a small info card (not a dark tooltip — a white card) with shipment ID, status badge, carrier, ETA. Styled identically to existing product tooltips/popovers.

**What is new here:**
The product currently shows single-shipment maps in the detail view. The fleet overview map showing all shipments simultaneously is new. But the visual language (marker style, route rendering, card-based info display) all map to existing patterns.

**What NOT to do:**
- No dark map tiles
- No glow effects on markers
- No "threat pulse" animation (see Section 6 for how to handle critical items)
- No radial gradient overlays
- No background grid lines
- No animated dots traveling along routes
- No glassmorphism / backdrop-filter overlays on map

### 4d. Priority Queue (Right Rail)

**What exists in the product:** The event timeline in the detail view uses card-based list items with circular icons, timestamps, event names, and expandable details with chevron arrows.

**For Mission Control — extending the event card pattern:**

The priority queue is a vertical scrollable list of exception cards, sorted by severity then by age (oldest unresolved first).

**Card structure:**

```
┌──────────────────────────────────────┐
│ ⚠ SHP-40921           2h 14m ago    │  ← Exception icon + Shipment ID (14px semi-bold) + timestamp (12px grey)
│ Carrier departure delay — Memphis    │  ← Description (13px, secondary text)
│ [CRITICAL]  DAL → MEM  Werner       │  ← Status badge + route + carrier (12px)
└──────────────────────────────────────┘
```

**Styling:**
- White background, `1px solid #E5E7EB` border-bottom (matching existing list divider pattern)
- Left accent border: 3px solid, colored by severity (red for critical, amber for warning) — this is new but follows a common enterprise pattern and is visually lightweight
- Padding: `14px 16px`
- Hover: `background: #F9FAFB` (matching existing hover patterns)
- Click: navigates to shipment detail view (existing page)

**Section header:**
```
PRIORITY QUEUE                    12 active    View all →
```
- "PRIORITY QUEUE": 11px uppercase grey label
- "12 active": badge using existing count-in-rounded-pill pattern (`background: #F3F4F6`, 10px text)
- "View all": teal link, matches existing "View all" pattern

**Severity tabs (within queue section):**
```
[All]  [Critical]  [Warning]
```
- These use the existing tab navigation pattern from the product (text tabs with colored underline on active). NOT the segmented-control/pill-toggle pattern from the current build.
- Active tab: dark text with orange/amber underline (matching existing tab indicator)

**Max visible items:** 6-8 depending on viewport. Scrollable within the rail. The queue has a fixed height that matches the map height.

### 4e. Shipment Table

**What exists in the product:** Data tables with minimal borders (thin grey horizontal lines between rows, no vertical cell borders). UPPERCASE grey column headers. Status shown as small colored text pills. Exception counts with warning/error icons.

**For Mission Control — direct reuse of existing pattern:**

This is the most straightforward section. Use the exact existing table styling.

**Columns:**

| Column | Width | Styling |
|--------|-------|---------|
| SHIPMENT ID | 120px | Semi-bold, dark text, left-aligned |
| CUSTOMER | 140px | Regular, secondary text |
| ROUTE | 160px | "DAL → MEM" format with arrow, regular text |
| CARRIER | 120px | Regular, secondary text |
| STATUS | 100px | Colored status pill (existing pattern) |
| EXCEPTIONS | 80px | Exception count with icon — amber triangle + number, red circle + number (existing pattern) |
| ETA | 100px | Date/time, regular text |
| VARIANCE | 80px | "+2.4 hrs" in red if late, "-0.5 hrs" in green if early |
| ACTIONS | 80px | "View" link in teal |

**Table features:**
- Sticky header row (UPPERCASE grey labels)
- Row dividers: `1px solid #E5E7EB` horizontal lines only
- Row hover: `background: #F9FAFB`
- Critical rows: NO tinted background. Instead, the exception column shows the red circle with count — this is how the existing product indicates severity. Adding a full row background tint would be a departure.
- Sortable columns: clicking header adds a small sort arrow (existing table pattern)
- Pagination: standard pagination at bottom ("Showing 1-25 of 247") — not virtual scroll. The product uses pagination, not infinite scroll.

**Section header:**
```
SHIPMENTS                    247 total    [🔍 Search within table]
```

**Filter row (below header, above table):**
Uses the same pill-shaped filter pattern as the page-level filter bar, but scoped to the table. "Status", "Exception type", "Carrier" dropdowns.

### 4f. Timeline / Activity Feed (REMOVED)

The v1 spec included a horizontal timeline / activity feed section at the bottom. **This is removed.** The existing product has an event timeline in the shipment detail view (card-based, expandable). Duplicating it at the dashboard level adds clutter without clear value. The priority queue already surfaces the most urgent recent events.

If real-time event awareness is needed at the dashboard level, it should be handled through the priority queue (new items appear at top) and toast notifications (see Section 5e), not through a dedicated timeline section.

---

## 5. Interaction Patterns

### 5a. Filtering

**Global filter bar** (below page title): Applies to all sections. Uses existing pill dropdown pattern.
- Active filters: green-filled pills (matching product)
- Clearing: "Reset" teal link removes all filters
- URL persistence: filter state in URL params for shareability (new, but invisible to user)

**Table-level filters**: Additional filter pills scoped to the shipment table only. Product already has this pattern.

### 5b. Drill-Down

**One-click path:** Click any shipment ID (in table, priority queue, or map info card) to navigate to the existing shipment detail page. This is NOT a slide-over panel — it's standard page navigation, matching how the product already works.

**Why not a slide-over:** The product doesn't use slide-over/drawer panels. Its detail views are full pages with left info panel + right map. Introducing a slide-over pattern would be inconsistent. If there's demand for "quick peek" behavior later, that's a product-wide pattern decision, not something Mission Control should pioneer alone.

### 5c. Map Interactions

- **Hover on marker:** Small white tooltip card appears near marker. Shows: Shipment ID, status badge, carrier name, ETA. Styled as a small white card with border and subtle shadow (`0 2px 8px rgba(0,0,0,0.1)`) — matching standard Google Maps info window styling, not a dark glassmorphic tooltip.
- **Click on marker:** Same info card, but persists (doesn't dismiss on mouseout). Click "View details" link in card to navigate to shipment detail.
- **Zoom/pan:** Standard Google Maps controls. No custom overlay controls.

### 5d. Priority Queue Interactions

- **Click card:** Navigate to shipment detail page
- **Severity tab toggle:** Filter queue list (no page reload, just client-side filter)
- **New exception appears:** Card inserts at appropriate position in sorted list. Subtle border flash (the left accent border briefly thickens from 3px to 4px and back over 300ms) to draw attention without being dramatic.

### 5e. Real-Time Updates

- **KPI values:** Update in place. Number changes with a quick CSS transition (`color` briefly shifts to the semantic color for 1s then returns to default). No count-up animation.
- **New priority items:** Insert into queue at sorted position
- **Toast notifications for critical events:** Small white card that slides in from top-right corner. White background, red left border (matching critical severity). Auto-dismiss after 10 seconds. Shows: "Critical: [shipment ID] — [exception type]" with "View" link. This extends the product's existing notification pattern.

### 5f. Keyboard Navigation

Standard browser behavior. Tab through interactive elements. No custom keyboard shortcuts. The product doesn't have custom keyboard shortcuts, so Mission Control shouldn't either.

---

## 6. What's New vs. Existing — And How New Elements Fit

### Existing Patterns (Direct Reuse)

| Component | Product Source | Notes |
|-----------|--------------|-------|
| Sidebar icon nav | All pages | Add one new icon for Mission Control |
| Header bar | All pages | Unchanged |
| Filter bar (pill dropdowns) | Shipment list view | Same component, different filter options |
| Data table | Shipment list view | Same columns/styling, mission control adds "Variance" column |
| Status badges | Shipment list/detail | Exact same colored pills |
| Exception indicators | Shipment table | Amber triangle + red circle with counts |
| "View all" links | Multiple pages | Teal text link pattern |
| Tab navigation | Detail view | Text tabs with underline indicator |

### New Components (Tasteful Extensions)

| Component | What's New | How It Fits |
|-----------|-----------|-------------|
| **KPI cards** | The product doesn't have summary metric cards. These are new. | Styled as a row of bordered cards matching the existing summary card pattern (seen in detail view info panels). Same border, padding, and background. The larger 28px number is the one new typographic scale addition — justified because KPIs need to be glanceable from further away than detail view fields. |
| **Fleet overview map** | Product has single-shipment maps. Fleet-wide map is new. | Uses the same Google Maps integration and marker style. The multi-marker view is a zoom-out of the existing single-shipment pattern. Marker colors follow the existing status color system exactly. |
| **Priority queue** | Product has event timelines per shipment. A cross-shipment priority list is new. | Built using the same card-list pattern as the event timeline. Left accent border is the only new visual element — it's restrained (3px, only on the left edge) and follows a widely understood severity-banding pattern. |
| **Trend indicators** | Small up/down arrows with context text on KPI cards. Product doesn't show trends. | Minimal footprint — a 10px arrow SVG and 12px text. Uses existing semantic colors. Doesn't introduce charts, sparklines, or any new visual vocabulary. |
| **Severity hierarchy** | Product has exception icons but no explicit severity tiers. Mission Control adds Critical vs. Warning as distinct tiers. | Maps directly to existing visual patterns: red circle = critical, amber triangle = warning. The hierarchy is implicit in the current product; Mission Control just makes it explicit and sortable. |
| **Toast notifications** | Product doesn't have toast notifications. | Standard enterprise pattern. White card, colored left border, top-right position. If the broader product later adopts toasts, this establishes the pattern. |

### What Is Explicitly NOT Included (Removed from v1)

| v1 Element | Why Removed |
|------------|-------------|
| Dark theme | Product is white/light. Period. |
| Noise texture overlay | Product has no decorative textures. |
| JetBrains Mono | Product doesn't use monospace. |
| Sparkline charts | Product has zero chart patterns. |
| "Threat Pulse" animation | No animation patterns exist in the product. A pulsing marker would look alien. Critical items are indicated by color (red) and icon (red circle), not motion. |
| Glow effects on cards/badges | Product uses flat colored backgrounds, not glows. |
| Glassmorphism / backdrop-filter | Product doesn't use translucent surfaces. |
| Slide-over detail panel | Product uses full-page navigation for details. |
| Custom keyboard shortcuts | Product doesn't have them. |
| Timeline / activity feed section | Redundant with priority queue. Over-designed for a v1. |
| Horizontal collapsed timeline bar | No product precedent. Adds complexity. |
| "Radius" branding | The product is RYDERSHARE, not Radius. |
| Purple/magenta accent colors | Product accent is teal/blue-green, not purple. |
| Animated dots on map routes | Product shows static route lines. |
| Virtual scroll on table | Product uses standard pagination. |
| Side nav expanding to 240px with labels | Product sidebar is narrow icon-only (~44px). It doesn't expand. |

---

## 7. Responsive Behavior

| Breakpoint | Behavior |
|------------|----------|
| 1440px+ | Full layout: 4 KPI cards in row, map + priority queue side by side, full table |
| 1280px | KPI cards compress slightly. Map and queue maintain side-by-side. Table hides low-priority columns (Variance, Actions). |
| 1024px | Map goes full width. Priority queue moves below map. KPI cards: 2x2 grid. |
| < 1024px | Not a target. Show message directing users to desktop. |

---

## 8. Accessibility

- All status colors paired with text labels AND icons (never color alone)
- Status badges always include text: "CRITICAL", "STARTED", etc.
- Exception icons (triangle, circle) provide shape differentiation beyond color
- Focus indicators: `2px solid #0D9488` (teal) outline with `2px` offset — visible on white backgrounds
- Minimum click/touch target: 32px
- `aria-live="polite"` on KPI card values for screen reader updates
- `aria-live="assertive"` on toast notifications for critical alerts
- No animation that can't be disabled via `prefers-reduced-motion`

---

## 9. Token Summary (Quick Reference for Builder)

```
SHELL:
  Sidebar:        ~44px, dark, icon-only (existing, unchanged)
  Header:         White bar, RYDERSHARE logo (existing, unchanged)
  Content area:   White background, 24px horizontal padding

LAYOUT:
  KPI cards:      4 across, horizontal row, 16px gap
  Map:            ~65% width
  Priority queue: ~35% width, matches map height
  Table:          Full width below map/queue
  Section gaps:   16px vertical

COLORS:
  Background:     #FFFFFF
  Subtle bg:      #F9FAFB
  Border:         #E5E7EB (default), #D1D5DB (strong)
  Text primary:   #1A1A1A
  Text secondary: #6B7280
  Text label:     #9CA3AF
  Accent:         #0D9488 (teal)

  Status green:   text #16A34A, bg #F0FDF4
  Status blue:    text #2563EB, bg #EFF6FF
  Status grey:    text #6B7280, bg #F3F4F6
  Status red:     text #DC2626, bg #FEF2F2
  Warning amber:  text #D97706, bg #FFFBEB

TYPOGRAPHY:
  Font:           Inter (system sans-serif fallback)
  Page title:     24px / 700
  KPI number:     28px / 600 (tabular-nums)
  KPI label:      11px / 500 / UPPERCASE
  Section head:   16px / 600
  Table header:   10-11px / 500 / UPPERCASE / letter-spaced
  Table body:     13-14px / 400
  Badge:          11px / 500 / UPPERCASE
  Meta/timestamp: 12px / 400
  NO MONOSPACE ANYWHERE

COMPONENTS:
  Cards:          White bg, 1px #E5E7EB border, 8px radius, no shadow
  Filters:        Pill shape, 20px radius, 1px border, icons optional
  Status pills:   Colored text on tinted bg, 4px radius
  Table:          Horizontal dividers only, sticky header, pagination
  Queue cards:    List with border-bottom dividers, 3px left severity accent
  Map:            Google Maps light style, colored circle markers
  Toast:          White card, top-right, colored left border, auto-dismiss

INTERACTIONS:
  Hover:          Background shifts to #F9FAFB
  Click:          Navigate to detail page (full page nav, no slide-over)
  Real-time:      Quiet updates — number transitions, queue inserts
  Animation:      Near zero. Only: subtle border flash on new queue items,
                  color transition on KPI number changes (1s).
                  prefers-reduced-motion disables all.
```

---

*Spec ready for Builder implementation and Devil's Advocate review.*
