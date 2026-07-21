# Generates the Network map's geometry layers from real data, in the design's
# own coordinate space, so every existing interaction (markers, popups, zoom
# clamp, storm click-through) keeps working untouched.
#
#   src/v2/map-base.html   — Canada/Mexico admin1 + all CONUS states (gap-free,
#                            Census 20m) + major highways (TIGER-derived), which
#                            REPLACES the design's two hand-drawn state groups
#   src/v2/map-roads.html  — anchor cities + the storm track/cone, injected
#                            before the state-labels group (as before)
#
# The design projects equirectangularly; this affine reproduces its own city
# anchors (DAL/MEM/ATL/ORL, Houston, New Orleans) to ~1px:
#   x = 43.53·lon + 4439.6      y = −47.45·lat + 1778.3
#
# Coverage is sized to the map's zoom clamp (mv.w ≤ 2600, x ∈ [−1150, 3550],
# y ∈ [−560, 2284]) so a full zoom-out never runs off the geometry.
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
V2 = Path(__file__).parent

AX, BX = 43.53, 4439.6
AY, BY = -47.45, 1778.3


def P(lon, lat):
    return (AX * lon + BX, AY * lat + BY)


# lon/lat window that covers the zoom clamp with margin
LON_LO, LON_HI = -130.0, -52.0
LAT_LO, LAT_HI = 5.0, 52.5

FOCUS_FIPS = {'48', '40', '29', '05', '22', '28', '01', '47', '13', '12', '45', '37', '21'}
SKIP_FIPS = {'02', '15', '72'}  # Alaska, Hawaii, Puerto Rico


def dp(pts, tol):
    """Douglas-Peucker on an open polyline of map-space points."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        if b - a < 2:
            continue
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        ln = math.hypot(dx, dy) or 1e-9
        dmax, imax = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / ln
            if d > dmax:
                dmax, imax = d, i
        if dmax > tol:
            keep[imax] = True
            stack.append((a, imax))
            stack.append((imax, b))
    return [p for p, k in zip(pts, keep) if k]


def dp_ring(pts, tol):
    """DP for a CLOSED ring: a ring's first==last point makes the plain DP
    baseline zero-length (every distance computes to 0 and the ring collapses),
    so split the ring into two arcs at the point farthest from pts[0]."""
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    if len(pts) < 6:
        return pts
    x0, y0 = pts[0]
    m = max(range(1, len(pts)), key=lambda i: (pts[i][0] - x0) ** 2 + (pts[i][1] - y0) ** 2)
    a = dp(pts[: m + 1], tol)
    b = dp(pts[m:] + [pts[0]], tol)
    return a[:-1] + b[:-1]


def ring_area(pts):
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def in_window(lon, lat):
    return LON_LO <= lon <= LON_HI and LAT_LO <= lat <= LAT_HI


def rings_of(geom):
    if geom['type'] == 'Polygon':
        return geom['coordinates']
    if geom['type'] == 'MultiPolygon':
        return [r for poly in geom['coordinates'] for r in poly]
    return []


def lines_of(geom):
    if geom['type'] == 'LineString':
        return [geom['coordinates']]
    if geom['type'] == 'MultiLineString':
        return geom['coordinates']
    return []


def fmt(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def topo_layers(features, tol, min_area, min_border_len=6):
    """Dissolve features into ONE filled silhouette plus each internal border
    drawn exactly once. Stroking every polygon draws shared borders twice, and
    independent DP simplification makes the two copies diverge — at deep zoom
    that renders as twin grey strokes with a white sliver between them (reads
    as a cased white 'road'). Returns (d_fill, d_borders)."""
    Q = 100000.0

    def q(pt):
        return (round(pt[0] * Q), round(pt[1] * Q))

    rings = []
    for feat in features:
        for ring in rings_of(feat['geometry']):
            pts = [q(p) for p in ring]
            dd = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
            if len(dd) > 1 and dd[0] == dd[-1]:
                dd = dd[:-1]
            if len(dd) >= 3:
                rings.append(dd)

    def skey(a, b):
        return (a, b) if a <= b else (b, a)

    count = {}
    for ring in rings:
        for i in range(len(ring)):
            k = skey(ring[i], ring[(i + 1) % len(ring)])
            count[k] = count.get(k, 0) + 1

    outline = [k for k, c in count.items() if c == 1]
    borders = [k for k, c in count.items() if c > 1]

    def chains(segs):
        """Join segments into polylines, breaking at junction nodes."""
        adj = {}
        for a, b in segs:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
        used = set()
        out = []

        def walk(a, b):
            path = [a, b]
            used.add(skey(a, b))
            while True:
                cur, prev = path[-1], path[-2]
                if len(adj[cur]) != 2:
                    break
                nxt = [n for n in adj[cur] if skey(cur, n) not in used]
                if not nxt:
                    break
                used.add(skey(cur, nxt[0]))
                path.append(nxt[0])
            return path

        for node in adj:
            if len(adj[node]) != 2:
                for n in adj[node]:
                    if skey(node, n) not in used:
                        out.append(walk(node, n))
        for a, b in segs:  # leftover pure cycles (islands, lake shorelines)
            if skey(a, b) not in used:
                out.append(walk(a, b))
        return out

    def windowed(path):
        return any(in_window(x / Q, y / Q) for x, y in path[:: max(1, len(path) // 24)])

    fill_parts, border_parts = [], []
    for ring in chains(outline):
        if not windowed(ring):
            continue
        closed = len(ring) > 1 and ring[0] == ring[-1]
        pts = dp_ring([P(x / Q, y / Q) for x, y in (ring[:-1] if closed else ring)], tol)
        if len(pts) < 4 or ring_area(pts) < min_area:
            continue
        fill_parts.append('M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in pts) + 'Z')
    for path in chains(borders):
        if not windowed(path):
            continue
        for run in clip_path_north([P(x / Q, y / Q) for x, y in path]):
            pts = dp(run, tol)
            if len(pts) < 2:
                continue
            length = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
            if length < min_border_len:
                continue
            border_parts.append('M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in pts))
    print(f'  topo_layers: {len(fill_parts)} fill rings, {len(border_parts)} border lines')
    return ''.join(fill_parts), ''.join(border_parts)


CLIP_Y = -760.0  # north clip in map space — beyond the zoom clamp's reach
# (mv.y ≥ −560), so the straight clip edge can never scroll into view. The
# far-north halves of the provinces are half a megabyte of invisible points.


def clip_ring_north(pts):
    """Sutherland-Hodgman against y >= CLIP_Y (map y grows southward)."""
    out = []
    for i in range(len(pts)):
        cx, cy = pts[i]
        px, py = pts[i - 1]
        cin, pin = cy >= CLIP_Y, py >= CLIP_Y
        if cin != pin:
            t = (CLIP_Y - py) / (cy - py)
            out.append((px + (cx - px) * t, CLIP_Y))
        if cin:
            out.append((cx, cy))
    return out


def clip_path_north(pts):
    """Split an open polyline into the runs south of CLIP_Y."""
    runs, cur = [], []
    for i, (x, y) in enumerate(pts):
        if y >= CLIP_Y:
            if not cur and i > 0 and pts[i - 1][1] < CLIP_Y:
                px, py = pts[i - 1]
                t = (CLIP_Y - py) / (y - py)
                cur.append((px + (x - px) * t, CLIP_Y))
            cur.append((x, y))
        elif cur:
            px, py = pts[i - 1]
            t = (CLIP_Y - py) / (y - py)
            cur.append((px + (x - px) * t, CLIP_Y))
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def arc_layers(features, tol, min_area, min_border_len=6):
    """TopoJSON-style arcs for data whose topology mostly-but-not-exactly
    matches (Natural Earth admin1): split every ring into arcs at junction
    vertices, simplify each arc ONCE in a cache, and reassemble the rings
    from the cached arcs. Neighboring provinces reuse byte-identical
    geometry, so no tolerance can open cracks between fills, and each
    shared border is emitted exactly once. The full dissolve (topo_layers)
    is NOT safe here — one mismatched edge breaks ring chaining, and under
    evenodd a bogus ring flips whole provinces into water (Toronto sat on
    water). Returns (d_fill, d_borders)."""
    Q = 100000.0

    def q(pt):
        return (round(pt[0] * Q), round(pt[1] * Q))

    def skey(a, b):
        return (a, b) if a <= b else (b, a)

    rings = []
    for feat in features:
        for ring in rings_of(feat['geometry']):
            if not any(in_window(lon, lat) for lon, lat in ring[:: max(1, len(ring) // 24)]):
                continue
            pts = [q(p) for p in ring]
            dd = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
            if len(dd) > 1 and dd[0] == dd[-1]:
                dd = dd[:-1]
            if len(dd) >= 3:
                rings.append(dd)

    count, adj = {}, {}
    for ring in rings:
        for i in range(len(ring)):
            a, b = ring[i], ring[(i + 1) % len(ring)]
            count[skey(a, b)] = count.get(skey(a, b), 0) + 1
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)

    arc_cache = {}

    def arc_pts(vseq):
        t = tuple(vseq)
        ck = min(t, t[::-1])
        if ck not in arc_cache:
            mpts = [P(x / Q, y / Q) for x, y in ck]
            if ck[0] == ck[-1]:
                mm = dp_ring(mpts[:-1], tol)
                arc_cache[ck] = mm + [mm[0]]
            else:
                arc_cache[ck] = dp(mpts, tol)
        pts = arc_cache[ck]
        return pts if t == ck else pts[::-1]

    fill_parts, border_parts, border_done = [], [], set()
    for ring in rings:
        n = len(ring)
        node_idx = [i for i in range(n) if len(adj[ring[i]]) != 2]
        if not node_idx:
            arcs = [ring + [ring[0]]]
        else:
            s = node_idx[0]
            rot = ring[s:] + ring[:s]
            rn = [i for i in range(n) if len(adj[rot[i]]) != 2]
            arcs = [rot[i:j + 1] for i, j in zip(rn, rn[1:])] + [rot[rn[-1]:] + [rot[0]]]
        ring_pts = []
        for a in arcs:
            seg = arc_pts(a)
            ring_pts += seg if not ring_pts else seg[1:]
            if count[skey(a[0], a[1])] >= 2:
                ck = min(tuple(a), tuple(a)[::-1])
                if ck not in border_done:
                    border_done.add(ck)
                    for run in clip_path_north(arc_pts(list(ck))):
                        length = sum(math.hypot(run[i + 1][0] - run[i][0], run[i + 1][1] - run[i][1]) for i in range(len(run) - 1))
                        if len(run) >= 2 and length >= min_border_len:
                            border_parts.append('M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in run))
        pts = clip_ring_north(ring_pts[:-1])
        if len(pts) < 4 or ring_area(pts) < min_area:
            continue
        fill_parts.append('M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in pts) + 'Z')
    print(f'  arc_layers: {len(fill_parts)} fill rings, {len(border_parts)} border lines, {len(arc_cache)} arcs')
    return ''.join(fill_parts), ''.join(border_parts)


def line_paths(features, tol, min_len, dedupe_px=2.8):
    """Lines → path 'd', dropping near-duplicate parallels (TIGER carries the
    two carriageways of an interstate as separate geometries ~1px apart, which
    renders as twin grey strokes with a white sliver between them)."""
    parts = []
    grid = {}  # 6px cells of accepted sample points
    CELL = 6.0

    def near_accepted(x, y):
        cx, cy = int(x // CELL), int(y // CELL)
        for gx in (cx - 1, cx, cx + 1):
            for gy in (cy - 1, cy, cy + 1):
                for ax, ay in grid.get((gx, gy), ()):
                    if (ax - x) ** 2 + (ay - y) ** 2 <= dedupe_px ** 2:
                        return True
        return False

    def register(pts):
        # register densified samples so gaps between vertices still match
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            seg = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(seg // 3))
            for t in range(n + 1):
                x, y = x1 + (x2 - x1) * t / n, y1 + (y2 - y1) * t / n
                grid.setdefault((int(x // CELL), int(y // CELL)), []).append((x, y))

    kept = skipped = 0
    for feat in features:
        for line in lines_of(feat['geometry']):
            if not any(in_window(lon, lat) for lon, lat in line[:: max(1, len(line) // 12)]):
                continue
            raw = [P(lon, lat) for lon, lat in line]
            pts = dp(raw, tol)
            if len(pts) < 2:
                continue
            length = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
            if length < min_len:
                continue
            samples = raw[:: max(1, len(raw) // 10)]
            hits = sum(1 for x, y in samples if near_accepted(x, y))
            if samples and hits / len(samples) >= 0.6:
                skipped += 1
                continue
            kept += 1
            register(raw)
            parts.append('M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in pts))
    print(f'  line_paths: kept {kept}, deduped {skipped}')
    return ''.join(parts)


# ------------------------------------------------------------------- load
states = json.load(open(ROOT / 'assets' / 'us-states-20m.json'))['features']
na = json.load(open(ROOT / 'assets' / 'na-admin1-ca-mx.json'))['features']
roads = json.load(open(ROOT / 'assets' / 'na-roads-major.json'))['features']

focus = [f for f in states if f['properties']['STATE'] in FOCUS_FIPS]
rest = [f for f in states if f['properties']['STATE'] not in FOCUS_FIPS | SKIP_FIPS]

# ---- roads, selected per country: the file tags Canada's majors (Trans-
# Canada, the 400-series) as Federal/State — an Interstate-only filter
# erases every Canadian road. Classify each feature by point-in-polygon
# against the admin1 shapes, then take each country's real top tiers.
_admin_polys = []
for _f in na:
    _g = _f['geometry']
    for _poly in ([_g['coordinates']] if _g['type'] == 'Polygon' else _g['coordinates']):
        _ext = _poly[0]
        _xs = [p[0] for p in _ext]
        _ys = [p[1] for p in _ext]
        _admin_polys.append((_f['properties']['admin'], (min(_xs), min(_ys), max(_xs), max(_ys)), _ext))


def _pip(x, y, ring):
    inside = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def road_country(feat):
    lines = lines_of(feat['geometry'])
    if not lines:
        return 'US'
    line = lines[0]
    for lon, lat in line[:: max(1, len(line) // 3)][:4]:
        for admin, (x0, y0, x1, y1), ext in _admin_polys:
            if x0 <= lon <= x1 and y0 <= lat <= y1 and _pip(lon, lat, ext):
                return 'CA' if admin == 'Canada' else 'MX'
    return 'US'


WANT = {'US': {'Interstate'}, 'CA': {'Federal', 'State'}, 'MX': {'Interstate', 'Federal'}}
_by_country = {'US': [], 'CA': [], 'MX': []}
for _f in roads:
    _c = road_country(_f)
    if _f['properties'].get('level') in WANT[_c]:
        _by_country[_c].append(_f)
# US first so the dedupe favors interstates where networks meet at the border
picked = _by_country['US'] + _by_country['CA'] + _by_country['MX']
print(f"  roads picked: US {len(_by_country['US'])} · CA {len(_by_country['CA'])} · MX {len(_by_country['MX'])}")

# One uniform near-white fill for the whole US (no regional tinting) and a
# slightly muted tone for Canada/Mexico context. The US uses the exact
# topological dissolve (Census shares vertices perfectly; evenodd turns lake
# shorelines into real water holes); Canada/Mexico use the crack-free union
# fill plus whatever borders DO match, drawn once.
na_fill, na_bord = arc_layers(na, 1.4, 60)
us_fill, us_bord = topo_layers(rest + focus, 1.1, 30)
d_int = line_paths(picked, 1.5, 18)

base = (
    '<path d="' + na_fill + '" fill="#EFF0F2" fill-rule="nonzero" stroke="none"></path>'
    '<path d="' + na_bord + '" fill="none" stroke="#DDE0E3" stroke-width="1" vector-effect="non-scaling-stroke"></path>'
    '<path d="' + us_fill + '" fill="#FAFAF9" fill-rule="evenodd" stroke="#D8DCDF" stroke-width="1" vector-effect="non-scaling-stroke"></path>'
    '<path d="' + us_bord + '" fill="none" stroke="#D8DCDF" stroke-width="1" vector-effect="non-scaling-stroke"></path>'
    # Cased roads (the standard map idiom): the SAME geometry drawn twice,
    # casing under a white core, so the two strokes can never drift apart.
    '<path d="' + d_int + '" fill="none" stroke="#D5DADE" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>'
    '<path d="' + d_int + '" fill="none" stroke="#FFFFFF" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></path>'
)
(V2 / 'map-base.html').write_text(base)

# ------------------------------------------------------- cities + storm cone
SE_CITIES = [
    ('Tampa', -82.46, 27.95), ('Miami', -80.19, 25.76), ('Jacksonville', -81.66, 30.33),
    ('Savannah', -81.10, 32.08), ('Nashville', -86.78, 36.16),
]
FAR_CITIES = [
    ('Chicago', -87.63, 41.88), ('St. Louis', -90.20, 38.63), ('Kansas City', -94.58, 39.10),
    ('Denver', -104.99, 39.74), ('Phoenix', -112.07, 33.45), ('Los Angeles', -118.24, 34.05),
    ('Seattle', -122.33, 47.61), ('Minneapolis', -93.27, 44.98), ('Detroit', -83.05, 42.33),
    ('New York', -74.01, 40.71), ('Washington', -77.04, 38.91), ('Toronto', -79.38, 43.65),
    ('Montreal', -73.57, 45.50), ('Monterrey', -100.32, 25.67), ('Mexico City', -99.13, 19.43),
    ('Vancouver', -123.12, 49.28), ('Calgary', -114.07, 51.05), ('Winnipeg', -97.14, 49.90),
    ('Ottawa', -75.70, 45.42), ('El Paso', -106.49, 31.76), ('Guadalajara', -103.35, 20.67),
]

# Province/state labels for Canada and Mexico, in the design's own label
# idiom (same group styling as its US state labels, a shade quieter).
PROVINCES = [
    ('BRITISH COLUMBIA', -122.6, 51.0), ('ALBERTA', -114.8, 51.8), ('SASKATCHEWAN', -106.2, 51.8),
    ('MANITOBA', -98.6, 51.8), ('ONTARIO', -82.5, 47.9), ('QUÉBEC', -73.9, 48.7),
    ('BAJA CALIFORNIA', -115.3, 30.6), ('SONORA', -110.6, 29.6), ('CHIHUAHUA', -106.3, 28.8),
    ('COAHUILA', -102.2, 27.4), ('DURANGO', -104.8, 24.8), ('NUEVO LEÓN', -99.9, 24.9),
    ('TAMAULIPAS', -98.4, 23.7),
]

cities = ''
for name, lon, lat in SE_CITIES + FAR_CITIES:
    x, y = P(lon, lat)
    cities += (f'<g transform="translate({fmt(x)} {fmt(y)}) scale({{{{ mGl }}}})" style="pointer-events:none;paint-order:stroke;stroke:#FFFFFF;stroke-width:2.4px">'
               f'<circle r="2.5" fill="#A9AAAC"></circle>'
               f'<text y="14" text-anchor="middle" font-size="9.5" font-family="Inter, sans-serif" fill="#A9AAAC">{name}</text></g>')

# Storm track with growing forecast radii, ending at the design's affected-area
# boundary (its dashed region centers near lon −84.2, lat 28.8). Bound to the
# same {{ stormOp }} opacity as the existing overlay, so it hides pre-enable.
TRACK = [(-90.6, 23.6), (-88.6, 25.3), (-86.6, 27.0), (-84.9, 28.2)]
RADII = [22, 34, 48, 64]
tx = [P(lon, lat) for lon, lat in TRACK]
storm = '<g opacity="{{ stormOp }}" style="pointer-events:none">'
storm += '<path d="M' + 'L'.join(f'{fmt(x)},{fmt(y)}' for x, y in tx) + '" fill="none" stroke="#E2907F" stroke-width="1.4" stroke-dasharray="7 5" stroke-linecap="round" vector-effect="non-scaling-stroke"></path>'
for (x, y), r in zip(tx, RADII):
    storm += f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" fill="rgba(214,90,60,0.05)" stroke="#E8AC9E" stroke-width="1" stroke-dasharray="3 4" vector-effect="non-scaling-stroke"></circle>'
storm += f'<circle cx="{fmt(tx[0][0])}" cy="{fmt(tx[0][1])}" r="3.4" fill="#DC6B60"></circle>'
storm += '</g>'

labels = ('<g fill="#C6C9CC" font-family="Inter, sans-serif" font-size="15" font-weight="500"'
          ' letter-spacing="0.08em" text-anchor="middle"'
          ' style="pointer-events:none;paint-order:stroke;stroke:#F1F2F3;stroke-width:3px">')
for name, lon, lat in PROVINCES:
    x, y = P(lon, lat)
    labels += f'<text x="{fmt(x)}" y="{fmt(y)}">{name}</text>'
labels += '</g>'

out = labels + '\n              ' + storm + '\n              ' + cities + '\n              '
(V2 / 'map-roads.html').write_text(out)

print(f'map-base.html: {len(base):,} chars (na {len(na_fill) + len(na_bord):,} · us {len(us_fill) + len(us_bord):,} · int {len(d_int):,})')
print(f'map-roads.html: {len(out):,} chars · {len(SE_CITIES) + len(FAR_CITIES)} cities · {len(PROVINCES)} province labels · storm cone {len(TRACK)} waypoints')
