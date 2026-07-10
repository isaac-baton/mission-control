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

# T11b — agent tiles get a "See all actions" affordance opening the audit-log
# side panel (one per agent; the meta line becomes a meta + action row).
SEE_ALL = (
    '<button data-log="{key}" onClick="{{{{ openAgLog }}}}" '
    'style="background:none;border:0;padding:0;font-family:inherit;font-size:11.5px;'
    'font-weight:500;color:#307CA7;cursor:pointer;white-space:nowrap">See all actions →</button>'
)
for key, meta in (
    ("agEta", "Last action · Today 6:04 AM"),
    ("agDock", "Last action · Today 5:58 AM"),
    ("agAudit", "Last run · Jul 1 · 214 lines"),
    ("agBh", "Draft waiting · MEM → DAL"),
):
    sub(f"see-all-actions {key}",
        f'<div style="font-size:11.5px;color:#A9AAAC;margin-top:6px">{meta}</div>',
        f'<div style="font-size:11.5px;color:#A9AAAC;margin-top:6px">{meta} · '
        + SEE_ALL.format(key=key) + '</div>')

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

# T11a4 — backhaul tile footer follows the in-log tender approval; paused
# semantics get a one-line definition (paused = analysis only).
sub("backhaul tile footer states",
    'Draft waiting · MEM → DAL · <button data-log="agBh"',
    '<sc-if value="{{ bhDraftWaiting }}">Draft waiting · MEM → DAL</sc-if>'
    '<sc-if value="{{ bhTenderSent }}"><span style="color:#1F7A61">Tender sent today · awaiting carrier response</span></sc-if>'
    ' · <button data-log="agBh"')
sub("paused semantics",
    'Drafts tenders for approved empty lanes. Never sends without your approval.</div>',
    'Drafts tenders for approved empty lanes. Paused = analysis only; nothing sends without your approval.</div>')

# T11a5 — value ledger on the agents screen: what Intelligence returned.
LEDGER = (
    '<div data-intel-only="" style="display:flex;align-items:center;gap:22px;flex-wrap:wrap;background:#fff;border:1px solid #E3E4E5;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.15);padding:12px 18px;margin:14px 0 4px">'
    '<span style="font-size:11px;font-weight:500;letter-spacing:0.04em;text-transform:uppercase;color:#696B6F">Intelligence this month</span>'
    '<span style="font-size:13px;color:#1D1D20;font-weight:600">{{ ledgerDisputed }}</span>'
    '<span style="width:3px;height:3px;border-radius:50%;background:#C5C6C7"></span>'
    '<span style="font-size:13px;color:#1D1D20;font-weight:600">{{ ledgerStorm }}</span>'
    '<span style="width:3px;height:3px;border-radius:50%;background:#C5C6C7"></span>'
    '<span style="font-size:13px;color:#1D1D20;font-weight:600">≈ $458K/yr identified in backhaul</span>'
    '</div>')
sub("agents value ledger",
    'nothing ships without your decision on cost-bearing changes</div>',
    'nothing ships without your decision on cost-bearing changes</div>' + LEDGER)

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

# T11b2 — the audit-log side panel itself, mounted inside the agents route
agent_log = (V2 / "agent-log.html").read_text(encoding="utf-8")
sub("agent log panel insert",
    '<div data-screen-label="AI agents" style="padding:24px 24px 140px">',
    '<div data-screen-label="AI agents" style="padding:24px 24px 140px">\n' + agent_log)

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
window.__dcBoot(ComponentV2, {json.dumps(props)});
</script>
</body>
</html>
"""

OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.name}: {OUT.stat().st_size:,} bytes")
for a in applied:
    print("  ✓", a)
