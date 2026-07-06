#!/usr/bin/env python3
"""Build Version 2 — RyderShare Intelligence with an onboarding/enable journey.

V1 (index.html) stays untouched. This script applies a set of anchored,
count-asserted transforms to the verbatim V1 design source and splices in the
V2 layer (landing page markup, ComponentV2 logic, gating CSS), producing
index-v2.html. Every transform asserts its expected hit count so a future
design re-export fails loudly here instead of silently drifting.
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "RyderShare Intelligence.dc.html"
OUT = ROOT / "index.html"  # canonical deployed build (Vercel serves index.html at the site root)
V2 = ROOT / "src" / "v2"

src = SRC.read_text(encoding="utf-8")

helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
helmet_css = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1).strip()
markup = re.search(r"</helmet>(.*?)</x-dc>", src, re.S).group(1)
script_m = re.search(
    r'<script type="text/x-dc" data-dc-script data-props="([^"]*)">(.*?)</script>',
    src, re.S)
logic_src = script_m.group(2)

props = {"motion": True, "startRoute": "shipments", "startEnabled": False}

# ---------------------------------------------------------------- transforms
applied = []

def sub(label, find, replace, count=1):
    global markup
    n = markup.count(find)
    assert n == count, f"{label}: expected {count} anchor hit(s), found {n}"
    markup = markup.replace(find, replace)
    applied.append(f"{label} ({count})")

# T1 — app root carries the intel state for CSS gating
sub("root data-intel",
    '<div style="display:flex;height:100vh;overflow:hidden;background:#F5F6F6">',
    '<div data-intel="{{ dataIntel }}" style="display:flex;height:100vh;overflow:hidden;background:#F5F6F6">')

# T2 — AI rail destinations exist only once Intelligence is on
RAIL_STYLE = 'style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;height:56px;text-decoration:none;color:rgba(255,255,255,0.78)"'
for r in ("agents", "reviews", "risk"):
    sub(f"rail gate #{r}",
        f'<a href="#/{r}" {RAIL_STYLE}',
        f'<a href="#/{r}" data-intel-only="" {RAIL_STYLE}')

# T3 — red activity dots (Insights + AI agents) are post-enable signals
sub("rail activity dots",
    '<span style="position:absolute;top:7px;right:15px;width:8px;height:8px;border-radius:50%;background:#CE1126;z-index:2"></span>',
    '<span data-intel-only="" style="position:absolute;top:7px;right:15px;width:8px;height:8px;border-radius:50%;background:#CE1126;z-index:2"></span>',
    count=2)

# T4 — pre-enable, Insights gets a soft pulsing cue instead of the red dot
sub("rail insights pulse cue",
    '<sc-if value="{{ isInsights }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;inset:0;background:#1D1D20;box-shadow:inset 2px 0 0 #CE1126"></span></sc-if>\n      <span data-intel-only=""',
    '<sc-if value="{{ isInsights }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;inset:0;background:#1D1D20;box-shadow:inset 2px 0 0 #CE1126"></span></sc-if>\n      <span data-intel-off-only="" style="position:absolute;top:7px;right:15px;width:8px;height:8px;border-radius:50%;background:#5AC8FA;z-index:2;animation:dotPulse 2.4s ease infinite"></span>\n      <span data-intel-only=""')

# T5 — shipments teaser banner (pre-enable) in the storm band's slot
TEASER = (
    '<div data-intel-off-only="" style="margin-bottom:14px">\n'
    '          <button data-nav="insights" onClick="{{ navTo }}" data-aiedge="" style="position:relative;overflow:hidden;display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:#fff;border:1px solid #E3E4E5;border-radius:8px;padding:11px 16px;cursor:pointer;font-family:inherit;box-shadow:0 1px 3px rgba(0,0,0,0.15)" style-hover="background:#F5F6F6">\n'
    '            <svg style="flex:none" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#276A92" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M9.94 15.5a2 2 0 0 0-1.44-1.44l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94a2 2 0 0 0 1.44-1.44l1.58-6.13a.5.5 0 0 1 .96 0l1.58 6.13a2 2 0 0 0 1.44 1.44l6.13 1.58a.5.5 0 0 1 0 .96l-6.13 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z"></path></svg>\n'
    '            <span style="font-size:13px;color:#303235;flex:1"><b style="font-weight:600">New — RyderShare Intelligence.</b> Digests, cited answers, and a storm plan before you ask.</span>\n'
    '            <span style="font-size:12.5px;font-weight:500;color:#307CA7;white-space:nowrap">See what it finds →</span>\n'
    '          </button>\n'
    '          </div>\n'
    '          ')
sub("shipments teaser insert",
    '<sc-if value="{{ notApproved }}" hint-placeholder-val="{{ false }}">\n          <button data-nav="risk"',
    TEASER + '<sc-if value="{{ notApproved }}" hint-placeholder-val="{{ false }}">\n          <button data-nav="risk"')

# T6 — storm band (proactive AI) gates + flashes on enable
sub("storm band notApproved",
    '<button data-nav="risk" onClick="{{ navTo }}" style="display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:#FEF9E6;',
    '<button data-nav="risk" onClick="{{ navTo }}" data-intel-only="" data-intel-flash="{{ intelFlash }}" style="display:flex;align-items:center;gap:10px;width:100%;text-align:left;background:#FEF9E6;')
sub("storm band approved",
    '<div style="display:flex;align-items:center;gap:10px;background:#E8F5F0;border-left:3px solid #34A081;border-radius:8px;padding:11px 16px;margin-bottom:14px">',
    '<div data-intel-only="" style="display:flex;align-items:center;gap:10px;background:#E8F5F0;border-left:3px solid #34A081;border-radius:8px;padding:11px 16px;margin-bottom:14px">')

# T7 — network brief card (the 2nd data-aiglow="card", after the Late(2) pill)
sub("network brief gate",
    'Late (2)</button>\n              </div>\n              <div data-aiglow="card" ',
    'Late (2)</button>\n              </div>\n              <div data-aiglow="card" data-intel-only="" data-intel-flash="{{ intelFlash }}" ')

# T8 — every "Why late?" entry point is Intelligence
sub("askLate gates", ' onClick="{{ askLate }}"', ' data-intel-only="" onClick="{{ askLate }}"', count=6)

# T9 — load-panel ask-chip cards (both panel variants)
sub("panel ask-chip cards",
    'Driver + helper crew</div></div>\n            </div>\n            <div data-aiglow="card" ',
    'Driver + helper crew</div></div>\n            </div>\n            <div data-aiglow="card" data-intel-only="" ',
    count=2)

# T10 — backhaul $ map layer is Intelligence economics
sub("backhaul layer pill", '<button data-y="lyBh" ', '<button data-y="lyBh" data-intel-only="" ')

# T10b — storm overlay controls are part of the Intelligence response
# (the storm zone/label itself is zeroed via stormOp in ComponentV2)
sub("storm layer pill", '<button data-y="lyStorm" ', '<button data-y="lyStorm" data-intel-only="" ')

# T10c — this is the product, not a concept: drop the Ask-panel chip
sub("concept chip",
    '<span style="display:inline-flex;align-items:center;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:500;letter-spacing:0.04em;text-transform:uppercase;line-height:16px;background:#FEF9E6;color:#655102">Concept</span>',
    '')

# T11 — the at-risk KPI tile on Network is an Intelligence prediction
i = markup.find('At-risk · Thu')
assert i > 0, "at-risk tile label not found"
j = markup.rfind('<button ', max(0, i - 1200), i)
assert j > 0, "at-risk tile container not resolved"
markup = markup[:j] + '<button data-intel-only="" ' + markup[j + len('<button '):]
applied.append("at-risk KPI tile (1)")

# T11b — Network stat strip: card-like tiles, larger icons, chevrons on the
# two actionable tiles (Running late → list filter, At-risk → risk radar).
s0 = markup.find('<!-- Mission-control stat strip -->')
s1 = markup.find('<div style="display:flex;flex:1;min-height:0">', s0)
assert 0 < s0 < s1, "stat strip bounds not found"
strip = markup[s0:s1]

CHEVRON = ('<svg style="flex:none;position:absolute;right:12px;top:50%;transform:translateY(-50%)" '
           'width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#A9AAAC" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"></path></svg>')

def strip_sub(label, find, replace, count):
    global strip
    n = strip.count(find)
    assert n == count, f"{label}: expected {count} in strip, found {n}"
    strip = strip.replace(find, replace)
    applied.append(f"{label} ({count})")

strip_sub("strip auto-fit columns",
    "grid-template-columns:repeat(8,minmax(0,1fr))",
    "grid-template-columns:repeat(auto-fit,minmax(120px,1fr))", 1)
strip_sub("tile card padding",
    "padding:9px 12px;min-width:0;display:flex;flex-direction:column;gap:3px",
    "padding:16px 14px;min-width:0;display:flex;flex-direction:column;gap:7px;justify-content:center", 8)
strip_sub("tile icon size", 'width="13" height="13"', 'width="18" height="18"', 8)
strip_sub("tile value size", "font-size:16px;font-weight:600;color:", "font-size:18px;font-weight:600;color:", 8)
# actionable tiles: room for the chevron + the chevron itself
strip_sub("late tile affordance",
    '<button data-f="late" onClick="{{ nfClick }}" style="background:#fff;',
    '<button data-f="late" onClick="{{ nfClick }}" style="position:relative;padding-right:32px;background:#fff;', 1)
# (the at-risk tile got data-intel-only in T11; anchor on its label context instead)
k = strip.find('At-risk · Thu')
b = strip.rfind('<button ', 0, k)
assert b > 0, "at-risk strip button not found"
tag_end = strip.find('style="background:#fff;', b)
assert 0 < tag_end < k, "at-risk style attr not found"
strip = strip[:tag_end] + 'style="position:relative;padding-right:32px;background:#fff;' + strip[tag_end + len('style="background:#fff;'):]
applied.append("risk tile affordance (1)")
n_close = strip.count('</button>')
assert n_close == 2, f"expected 2 buttons in strip, found {n_close}"
strip = strip.replace('</button>', CHEVRON + '</button>')
applied.append("tile chevrons (2)")

markup = markup[:s0] + strip + markup[s1:]

# T12 — #/insights: landing pre-enable, intelligence hub post-enable
HUB_ANCHOR = '<sc-if value="{{ isInsights }}" hint-placeholder-val="{{ false }}"><div data-screen-label="Insights"'
landing = (V2 / "landing.html").read_text(encoding="utf-8")
sub("insights hub rebind + landing insert",
    HUB_ANCHOR,
    landing + '\n        <sc-if value="{{ showIntelHub }}"><div data-screen-label="Insights"')

# T13 — enable-moment flash stays only on surfaces discovered on OTHER pages
# (shipments storm band, network brief — set in T6/T7). The hub itself keeps
# just its persistent glows: a triple rainbow on one page read as noise.

leftover = re.findall(r"uploads/[^\"')\s]*", markup)

# ------------------------------------------------------------------ assemble
logo_b64 = base64.b64encode((ROOT / "assets" / "rydershare-logo.png").read_bytes()).decode()
markup, n_logo = re.subn(
    r'src="uploads/pasted-1783059767944-0\.png"',
    f'src="data:image/png;base64,{logo_b64}"',
    markup)
assert n_logo == 1

markup = re.sub(r'\s+hint-placeholder-val="\{\{ (?:true|false) \}\}"', "", markup)
markup = re.sub(r'\s+hint-placeholder-count="\d+"', "", markup)
markup = re.sub(r'\s+data-comment-anchor="[^"]*"', "", markup)
leftover = re.findall(r"uploads/[^\"')\s]*", markup)
assert not leftover, f"unembedded upload references remain: {leftover}"

font_b64 = base64.b64encode((ROOT / "assets" / "inter-400.woff2").read_bytes()).decode()
inter_css = (ROOT / "assets" / "inter.css").read_text()
latin_range = None
for subset, body in re.findall(r"/\*\s*([a-z0-9-]+)\s*\*/\s*@font-face\s*\{([^}]+)\}", inter_css):
    if subset == "latin":
        latin_range = re.search(r"unicode-range:\s*([^;]+);", body).group(1).strip()
        break
assert latin_range

font_css = (
    "@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;"
    "font-display:swap;"
    f"src:url(data:font/woff2;base64,{font_b64}) format('woff2');"
    f"unicode-range:{latin_range}}}"
)

runtime_js = (ROOT / "src" / "runtime.js").read_text(encoding="utf-8")
v2_logic = (V2 / "logic.js").read_text(encoding="utf-8")
v2_css = (V2 / "v2.css").read_text(encoding="utf-8").strip()

boot_css = "body:not(.dc-ready){visibility:hidden}x-dc{display:contents}"

out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RyderShare Intelligence</title>
<style>{font_css}</style>
<style>
{helmet_css}
</style>
<style>
{v2_css}
</style>
<style>{boot_css}</style>
</head>
<body>
<x-dc>{markup}</x-dc>
<script>
{runtime_js}
</script>
<script>
{logic_src}
{v2_logic}
window.__dcBoot(ComponentV2, {json.dumps(props)});
</script>
</body>
</html>
"""

OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.name}: {OUT.stat().st_size:,} bytes")
for a in applied:
    print("  ✓", a)
