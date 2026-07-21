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
    '<div data-intel="{{ dataIntel }}" data-theme="{{ pageTheme }}" style="display:flex;height:100vh;overflow:hidden;background:#F5F6F6">')

# T12 — Network map, brought up to visibility-platform standard (project44
# Movement / FourKites conventions): quieter water, land with more contrast,
# an interstate-corridor layer under the labels, five missing anchor cities,
# smaller pin-style load markers, and a softer storm overlay.
sub("map water softened",
    'background:#D9E7F0;overflow:hidden;min-width:0;cursor:grab',
    'background:linear-gradient(180deg,#E0E7EE,#D6E0E9);overflow:hidden;min-width:0;cursor:grab')
# The design's two hand-drawn state groups (gappy borders, SE-only coverage)
# are excised wholesale and replaced with the generated basemap: Canada/Mexico
# admin1 + gap-free Census states + TIGER-derived highways, sized to the zoom
# clamp so a full zoom-out stays on real geometry.
_g1 = markup.find('<g fill="#F1F2F0" stroke="#D5D8DA" stroke-width="1">')
assert _g1 > 0, "map state group 1 not found"
_g2 = markup.find('<g fill="#F7F8F6" stroke="#DEE0E2" stroke-width="1">', _g1)
assert _g2 > 0, "map state group 2 not found"
_g2e = markup.find('</g>', _g2) + len('</g>')
assert markup.find('</g>', _g1) < _g2, "state groups not adjacent as expected"
map_base = (V2 / "map-base.html").read_text(encoding="utf-8")
markup = markup[:_g1] + map_base + markup[_g2e:]
applied.append("map basemap replaced with real geometry (1)")
# The design source ALSO carries its own cased road network (a grey-casing
# group under a white-core group over identical geometry). With the real
# TIGER interstates in the basemap, that layer renders as a second road
# system a few px off the real one — excise both groups wholesale.
for _sig in ('<g fill="none" stroke="#DDDFE1" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">',
             '<g fill="none" stroke="#FFFFFF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'):
    _r = markup.find(_sig)
    assert _r > 0, "design road group not found: " + _sig[:44]
    assert markup.find(_sig, _r + 1) < 0, "design road group signature not unique: " + _sig[:44]
    _re = markup.find('</g>', _r) + len('</g>')
    markup = markup[:_r] + markup[_re:]
applied.append("design's own cased road layer excised (2)")
map_roads = (V2 / "map-roads.html").read_text(encoding="utf-8")
_lbl = markup.find('style="pointer-events:none;paint-order:stroke;stroke:#F7F8F6;stroke-width:3px">')
assert _lbl > 0, "state labels group not found"
_lbl = markup.rfind('<g ', 0, _lbl)
markup = markup[:_lbl] + map_roads + markup[_lbl:]
applied.append("interstate corridors + anchor cities injected (1)")
sub("marker halos resized (blue)",
    'r="15" fill="rgba(48,124,167,0.14)"', 'r="10.5" fill="rgba(48,124,167,0.16)"', 55)
sub("marker halos resized (amber)",
    'r="15" fill="rgba(240,192,5,0.18)"', 'r="10.5" fill="rgba(240,192,5,0.20)"', 5)
sub("marker cores resized (blue)",
    'r="11" fill="#307CA7" stroke="#fff" stroke-width="2"', 'r="7" fill="#307CA7" stroke="#fff" stroke-width="1.6"', 55)
sub("marker cores resized (amber)",
    'r="11" fill="#F0C005" stroke="#fff" stroke-width="2"', 'r="7" fill="#F0C005" stroke="#fff" stroke-width="1.6"', 5)
sub("marker heading arrows resized",
    '"M0,-6.5 L4.5,5.5 L0,3 L-4.5,5.5 Z"', '"M0,-4.2 L2.9,3.6 L0,1.9 L-2.9,3.6 Z"', 60)
sub("storm overlay softened",
    'fill="rgba(206,17,38,0.07)" stroke="#DC6B60" stroke-width="1"',
    'fill="rgba(214,90,60,0.06)" stroke="#E2907F" stroke-width="1.2"')

# footer badge hook so the dark theme can restyle it
sub("footer badge hook",
    '<div style="position:absolute;left:12px;bottom:10px;z-index:9;pointer-events:none;background:rgba(255,255,255,0.85);',
    '<div data-badge="" style="position:absolute;left:12px;bottom:10px;z-index:9;pointer-events:none;background:rgba(255,255,255,0.85);')

# T2 — AI rail destinations exist only once Intelligence is on
RAIL_STYLE = 'style="position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;height:56px;text-decoration:none;color:rgba(255,255,255,0.78)"'
for r in ("agents", "reviews", "risk"):
    sub(f"rail gate #{r}",
        f'<a href="#/{r}" {RAIL_STYLE}',
        f'<a href="#/{r}" data-intel-only="" {RAIL_STYLE}')

# T3 — the red activity dots (Insights + Autopilot) are removed entirely
sub("rail activity dots removed",
    '<span style="position:absolute;top:7px;right:15px;width:8px;height:8px;border-radius:50%;background:#CE1126;z-index:2"></span>',
    '',
    count=2)

# T4 — pre-enable, Insights keeps its soft pulsing discovery cue
sub("rail insights pulse cue",
    '<sc-if value="{{ isInsights }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;inset:0;background:#1D1D20;box-shadow:inset 2px 0 0 #CE1126"></span></sc-if>',
    '<sc-if value="{{ isInsights }}" hint-placeholder-val="{{ false }}"><span style="position:absolute;inset:0;background:#1D1D20;box-shadow:inset 2px 0 0 #CE1126"></span></sc-if>\n      <span data-intel-off-only="" style="position:absolute;top:7px;right:15px;width:8px;height:8px;border-radius:50%;background:#5AC8FA;z-index:2;animation:dotPulse 2.4s ease infinite"></span>')

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

# T11a2 — the document-style review ships as THE reviews screen (judge verdict:
# a review is an artifact customers forward, not a second dashboard). The old
# tile-grid reviews section is removed wholesale; the replacement binds to the
# same isReviews route, so the rail is unchanged.
_rs = markup.find('<div data-screen-label="Reviews"')
assert _rs > 0, "old reviews screen not found"
_rs = markup.rfind('<sc-if', 0, _rs)
_re = markup.find('<div data-screen-label="Risk radar"', _rs)
_re = markup.rfind('<sc-if', 0, _re)
assert 10000 < (_re - _rs) < 16000, f"old reviews slice looks wrong ({_re - _rs} chars)"
markup = markup[:_rs] + markup[_re:]
applied.append("old reviews screen removed (1)")

reviews2 = (V2 / "reviews2.html").read_text(encoding="utf-8")
RISK_SCREEN_ANCHOR = '<sc-if value="{{ isRisk }}" hint-placeholder-val="{{ false }}"><div data-screen-label="Risk radar"'
sub("document review screen insert",
    RISK_SCREEN_ANCHOR,
    reviews2 + '\n        ' + RISK_SCREEN_ANCHOR)

# T11a3 — board gains its third late load, SBG-31252 (GPS-offline unit): the
# Network "No location" copy references it, and an exec will ask to see it.
# Clone the SBG-31241 late row and adapt fields; bindings r18St/r18Ord are
# computed in ComponentV2.
_r41 = markup.find('<div data-ref="SBG-31241" onClick="{{ openLoad }}"')
_r42 = markup.find('<div data-ref="SBG-31242" onClick="{{ openLoad }}"', _r41)
assert 0 < _r41 < _r42, "31241 row not found"
row = markup[_r41:_r42]
_wb = row.find('data-l="SBG-31241"')
if _wb >= 0:
    _wb0 = row.rfind('<button', 0, _wb)
    _wb1 = row.find('</button>', _wb) + len('</button>')
    row = row[:_wb0] + row[_wb1:]
for old, new in (
    ('SBG-31241', 'SBG-31252'), ('884210332', '884210395'),
    ('Atlanta DC-03', 'Memphis DC-02'), ('Savannah corridor', 'Jonesboro loop'),
    ('Savannah, GA', 'Jonesboro, AR'),
    ('4:15 PM ET · Jul 7', 'Driver-reported 3:40 PM CT'), ('3m ago', '48m ago'),
    ('{{ r1St }}', '{{ r18St }}'), ('{{ r1Ord }}', '{{ r18Ord }}'),
):
    assert old in row, f"row field {old!r} not found"
    row = row.replace(old, new)
_r53 = markup.find('<div data-ref="SBG-31253" onClick="{{ openLoad }}"')
assert _r53 > 0, "31253 row not found"
markup = markup[:_r53] + row + markup[_r53:]
applied.append("board row SBG-31252 (1)")

# T11a6 — Risk radar: the "if you do nothing" counterfactual under the plan
# card. Reframes Approve as economics (judge frontier idea #3) and fills the
# page's empty lower half. The plan-cost figure is the live {{ planCostLabel }}
# binding, so Adjust updates the comparison too.
COUNTERFACTUAL = (
    '\n            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px">'
    '<div style="background:#fff;border:1px solid #E3E4E5;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.15);padding:18px 22px">'
    '<div style="display:flex;align-items:center;gap:9px"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#655102" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M6 16.33A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 .5 8.97"></path><path d="m13 12-3 5h4l-3 5"></path></svg>'
    '<span style="font-size:13px;font-weight:600;color:#44464B">If you do nothing</span></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:14px;font-size:13px;color:#303235"><span>Service failures Thursday</span><b style="font-weight:600;color:#655102">6</b></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:9px;font-size:13px;color:#303235"><span>Est. exposure — redelivery + detention</span><b style="font-weight:600;color:#655102">≈ $9.8K</b></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:9px;font-size:13px;color:#303235"><span>On-time next week</span><b style="font-weight:600;color:#655102">▼ ≈ 2.2 pts</b></div>'
    '</div>'
    '<div style="background:#fff;border:1px solid #E3E4E5;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.15);padding:18px 22px">'
    '<div style="display:flex;align-items:center;gap:9px"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#1F7A61" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="m9 12 2 2 4-4"></path></svg>'
    '<span style="font-size:13px;font-weight:600;color:#1D1D20">With the plan</span>'
    '<sc-if value="{{ approved }}"><span style="display:inline-flex;align-items:center;padding:2px 8px;border-radius:4px;font-size:11px;font-weight:500;letter-spacing:0.04em;text-transform:uppercase;background:#E8F5F0;color:#1F7A61">Active</span></sc-if></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:14px;font-size:13px;color:#303235"><span>Service failures Thursday</span><b style="font-weight:600;color:#1F7A61">0 — deliveries unaffected</b></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:9px;font-size:13px;color:#303235"><span>Cost to run the plan</span><b style="font-weight:600;color:#1D1D20">{{ planCostLabel }}</b></div>'
    '<div style="display:flex;justify-content:space-between;gap:12px;margin-top:9px;font-size:13px;color:#303235"><span>On-time next week</span><b style="font-weight:600;color:#1F7A61">holds at 96.2%</b></div>'
    '</div></div>'
    '<div style="font-size:11.5px;color:#A9AAAC;margin-top:10px">Estimates from June service-failure costs and this week\'s load values · Sources · Load records · Invoice SBG-2026-06</div>')
sub("risk counterfactual",
    'nothing is committed until you approve.</div>\n              </div>\n              </sc-if>\n            </div>',
    'nothing is committed until you approve.</div>\n              </div>\n              </sc-if>\n            </div>'
    + COUNTERFACTUAL)

# T11a7 — once the plan is approved it is locked (adjOpen is forced closed),
# so the Adjust button would be a dead click; render it only pre-approval.
ADJUST_BTN = '<button style="background:#fff;border:1px solid #C5C6C7;color:#303235;border-radius:6px;padding:9px 16px;font-size:13px;font-weight:500;cursor:pointer;font-family:inherit" onClick="{{ adjToggle }}" style-hover="background:#F5F6F6">Adjust</button>'
sub("adjust hidden when locked",
    ADJUST_BTN,
    '<sc-if value="{{ notApproved }}">' + ADJUST_BTN + '</sc-if>')

# T11b0 — Risk radar merges into Autopilot: slice the risk screen's working
# content (advisory, load table, plan card, counterfactual — all bindings are
# route-agnostic), delete the screen, drop its rail item, and rename the
# agents rail item. The slice becomes the incident module on the merged tab.
_rk = markup.find('<div data-screen-label="Risk radar"')
assert _rk > 0, "risk screen not found"
_rs2 = markup.rfind('<sc-if', 0, _rk)
# no labeled screen follows Risk — terminate at the screen's compact close
_re2 = markup.find('</div></sc-if>', _rk)
assert _re2 > 0, "risk screen close not found"
_re2 += len('</div></sc-if>')
risk_section = markup[_rs2:_re2]
assert 15000 < len(risk_section) < 32000, f"risk slice looks wrong ({len(risk_section)} chars)"

_adv = risk_section.find('Tropical system expected across the Gulf Coast')
assert _adv > 0, "risk advisory not found"
_adv = risk_section.rfind('<div', 0, _adv)
_cfe = risk_section.find("Estimates from June service-failure costs")
assert _cfe > 0, "counterfactual footer not found"
_cfe = risk_section.find('</div>', _cfe) + len('</div>')
INCIDENT_BODY = risk_section[_adv:_cfe]
markup = markup[:_rs2] + markup[_re2:]
applied.append("risk screen merged out (1)")

# The storm renders as a compact queue row + receipt authored in agents2.html;
# its full dossier lives in the storm decision panel (flex-panel.html). The
# inline INCIDENT module is retired — INCIDENT_BODY is no longer injected.

sub("risk rail item removed",
    f'<a href="#/risk" data-intel-only="" {RAIL_STYLE}', '<a data-removed-risk ')
_ri = markup.find('<a data-removed-risk ')
_rj = markup.find('</a>', _ri) + len('</a>')
markup = markup[:_ri] + markup[_rj:]

# T11b1 — AI agents screen, redesigned (principal-designer spec: decisions
# promoted to hero, agents as one-line rows, ledger as stat tiles, topics as
# fact fragments). The old section is sliced out; the authored replacement's
# opening div is byte-identical so the panel insert below keeps anchoring.
_ad = markup.find('<div data-screen-label="AI agents"')
assert _ad > 0, "agents screen not found"
_as = markup.rfind('<sc-if', 0, _ad)
_ae = markup.find('data-screen-label', _ad + 40)
_ae = markup.rfind('<sc-if', 0, _ae)
assert 20000 < (_ae - _as) < 30000, f"agents slice looks wrong ({_ae - _as} chars)"
agents2 = (V2 / "agents2.html").read_text(encoding="utf-8")
assert agents2.count('<!--INCIDENT-->') == 0, "inline incident placeholder is retired"
workforce = (V2 / "workforce.html").read_text(encoding="utf-8")
markup = markup[:_as] + agents2 + '\n        ' + workforce + '\n        ' + markup[_ae:]
applied.append("agents screen redesign + incident + workforce (1)")

# Rail + copy renames for the merged tab
sub("rail label Autopilot",
    '<span style="position:relative;font-size:10px;font-weight:500">AI agents</span>',
    '<span style="position:relative;font-size:10px;font-weight:500">Autopilot</span>')
sub("digest link renamed", '>Risk radar</', '>Autopilot</')
sub("digest opener de-fragmented",
    '>A strong week. On-time delivery held at',
    '>It was a strong week: on-time delivery held at')

# The Workforce showroom is a first-class rail tab ("Agents", bot icon);
# Autopilot swaps to a gauge — the control-room instrument, not the robot.
BOT_ICON = '<svg style="position:relative" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="9" width="14" height="11" rx="2"></rect><path d="M12 9V5"></path><circle cx="12" cy="4" r="1"></circle><path d="M9.5 13.5v2"></path><path d="M14.5 13.5v2"></path><path d="M2 14h3"></path><path d="M19 14h3"></path></svg>'
GAUGE_ICON = '<svg style="position:relative" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="m12 14 4-4"></path><path d="M3.34 19a10 10 0 1 1 17.32 0"></path></svg>'
sub("autopilot gauge icon", BOT_ICON, GAUGE_ICON)

AGENTS_TAB = (
    f'<a href="#/workforce" data-intel-only="" {RAIL_STYLE} style-hover="background:rgba(255,255,255,0.06)">\n'
    '      <sc-if value="{{ isWorkforce }}"><span style="position:absolute;inset:0;background:#1D1D20;box-shadow:inset 2px 0 0 #CE1126"></span></sc-if>\n'
    '      ' + BOT_ICON + '\n'
    '      <span style="position:relative;font-size:10px;font-weight:500">Agents</span>\n'
    '    </a>\n    '
)
_ap = markup.find('<a href="#/agents" data-intel-only="" ')
assert _ap > 0, "autopilot rail item not found"
_ap_end = markup.find('</a>', _ap) + len('</a>')
markup = markup[:_ap_end] + '\n    ' + AGENTS_TAB + markup[_ap_end:]
applied.append("agents rail tab (1)")

# Rail order: Insights · Shipments · Network · Autopilot · Reviews · Agents
# (Isaac, 2026-07-20). Extract the six rail anchors (identified by their
# 56px rail style, so in-page links to the same routes are not touched)
# and re-emit them in order at the first one's position.
RAIL_ORDER = ['#/insights', '#/shipments', '#/network', '#/agents', '#/reviews', '#/workforce']
_items = []
for _href in RAIL_ORDER:
    _j = 0
    while True:
        _j = markup.find(f'<a href="{_href}" ', _j)
        assert _j > 0, f"rail item not found: {_href}"
        if 'height:56px' in markup[_j:_j + 420]:
            break
        _j += 1
    _e = markup.find('</a>', _j) + len('</a>')
    _items.append((_j, _e, markup[_j:_e]))
_first = min(_j for _j, _e, _h in _items)
for _j, _e, _h in sorted(_items, reverse=True):
    markup = markup[:_j] + markup[_e:]
markup = markup[:_first] + '\n    '.join(_h for _j, _e, _h in _items) + markup[_first:]
applied.append("rail reordered: Insights first, agentic tabs at the bottom (1)")

# T11b2 — the audit-log side panel itself, mounted inside the agents route
agent_log = (V2 / "agent-log.html").read_text(encoding="utf-8")
sub("agent log panel insert",
    '<!-- S0a docked prompt bar -->',
    agent_log + '\n      <!-- S0a docked prompt bar -->')

# T11b2b — the adaptive-capacity decision panel (rate charts + approve)
flex_panel = (V2 / "flex-panel.html").read_text(encoding="utf-8")
sub("flex decision panel insert",
    '<!-- S0a docked prompt bar -->',
    flex_panel + '\n      <!-- S0a docked prompt bar -->')

# T11b3 — dynamic ask answers: one generic bubble template renders any
# intent-engine answer (logic.js dynSubmit); styling mirrors the fb bubble.
_pill = ('padding:7px 13px;border:1px solid #C5C6C7;border-radius:999px;background:#fff;'
         'font-size:12.5px;color:#303235;cursor:pointer;font-family:inherit')
DYN_BUBBLE = (
    '<sc-if value="{{ msg.isDyn }}">\n'
    '                <div style="background:#fff;border:1px solid #E3E4E5;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.15);padding:20px;margin:16px 0">\n'
    '                  <div style="animation:rev .2s ease both;font-size:13.5px;color:#303235;line-height:1.6">{{ msg.dynText }}</div>\n'
    '                  <sc-if value="{{ msg.hasDyn2 }}"><div style="animation:rev .2s ease both;animation-delay:.18s;font-size:13.5px;color:#303235;line-height:1.6;margin-top:10px">{{ msg.dynText2 }}</div></sc-if>\n'
    '                  <sc-if value="{{ msg.hasPills }}">\n'
    '                  <div style="animation:rev .2s ease both;animation-delay:.26s;display:flex;flex-wrap:wrap;gap:8px;margin-top:14px">\n'
    f'                    <sc-if value="{{{{ msg.hasP1 }}}}"><button data-q="{{{{ msg.p1Q }}}}" onClick="{{{{ askQ }}}}" style="{_pill}" style-hover="background:#F5F6F6">{{{{ msg.p1Label }}}}</button></sc-if>\n'
    f'                    <sc-if value="{{{{ msg.hasP2 }}}}"><button data-q="{{{{ msg.p2Q }}}}" onClick="{{{{ askQ }}}}" style="{_pill}" style-hover="background:#F5F6F6">{{{{ msg.p2Label }}}}</button></sc-if>\n'
    '                  </div>\n'
    '                  </sc-if>\n'
    '                  <div style="animation:rev .2s ease both;animation-delay:.4s;font-size:11px;color:#696B6F;margin-top:14px;padding-top:12px;border-top:1px solid #ECEDED">{{ msg.dynFoot }}</div>\n'
    '                </div>\n'
    '                </sc-if>\n'
    '                ')
sub("dynamic answer bubble insert",
    '<sc-if value="{{ msg.isFB }}">',
    DYN_BUBBLE + '<sc-if value="{{ msg.isFB }}">')

# T11b4 — the Ask panel and its docked pills/input follow the dark theme on
# the Agents tab. Both mounts are fixed furniture outside the themed root, so
# they self-bind the theme the same way the audit panel does.
sub("ask panel theme binding",
    '<div data-screen-label="Ask RyderShare" style="',
    '<div data-screen-label="Ask RyderShare" data-aask="" data-ptheme="{{ pageTheme }}" style="')
sub("ask dock theme binding",
    '<div style="position:fixed;right:12px;bottom:12px;width:596px;max-width:calc(92vw - 24px);z-index:26">',
    '<div data-aask="" data-ptheme="{{ pageTheme }}" style="position:fixed;right:12px;bottom:12px;width:596px;max-width:calc(92vw - 24px);z-index:26">')

# T11c — Ask panel: the suggestion pills float in a fixed block over the
# thread; with three long pills wrapping to two rows that block is ~150px
# tall, so the thread needs more bottom clearance than the design's 130px or
# the pills sit on the last chat bubble. Opaque pills keep the layers legible
# while content scrolls beneath.
sub("ask thread bottom clearance",
    '<div style="max-width:760px;margin:0 auto;padding:20px 20px 130px">',
    '<div style="max-width:760px;margin:0 auto;padding:20px 20px 180px">')
sub("opaque suggestion pills",
    "background:rgba(255,255,255,0.96)",
    "background:#fff")

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
window.__app = window.__dcBoot(ComponentV2, {json.dumps(props)});
</script>
</body>
</html>
"""


# T-final — Isaac's voice: em dashes are always tight (word—word, never
# word — word), across every string in the file. Runs last so it covers the
# verbatim design copy, the patch layers, and the inlined logic alike.
_dash_n = out.count(' — ')
out = out.replace(' — ', '—')
applied.append(f"em dashes tightened ({_dash_n})")

OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.name}: {OUT.stat().st_size:,} bytes")

# Mirror to the always-on local preview (a LaunchAgent serves this dir on
# :8791 — it lives outside ~/Desktop because macOS TCC blocks launchd agents
# from privacy-protected folders). NOTE: the old :8765/.rydershare-preview
# pair is abandoned to Kimi's copy of this script, which mirrors there too
# and was silently overwriting our builds.
_preview = Path.home() / ".rydershare-preview-claude" / "index.html"
try:
    _preview.parent.mkdir(exist_ok=True)
    _preview.write_text(out, encoding="utf-8")
    print(f"mirrored to {_preview}")
except OSError as e:
    print(f"preview mirror skipped: {e}")
for a in applied:
    print("  ✓", a)
