#!/usr/bin/env python3
"""Build the LEGACY V1 prototype (always-enabled, no onboarding journey).

Superseded on the live site by V2 (src/build_v2.py → index.html). Kept so the
V1 "product as if already enabled" variant stays reproducible; its output
(v1.html) is gitignored and NOT deployed.

Assembles one self-contained HTML file from:
  - RyderShare Intelligence.dc.html  (design source of record — markup + logic, kept verbatim)
  - src/runtime.js                   (dc-lite runtime replacing support.js/React/Babel/CDN)
  - assets/inter-400.woff2           (Inter variable font, latin subset — embedded base64)
  - assets/rydershare-logo.png       (embedded as data URI)

PRD build requirement #1: one file, zero external network requests, works from file://.
"""
import base64
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "RyderShare Intelligence.dc.html"
OUT = ROOT / "v1.html"  # legacy V1 output — gitignored, not deployed (V2 owns index.html)

src = SRC.read_text(encoding="utf-8")

# ---- extract the three sections of the design file ----
helmet = re.search(r"<helmet>(.*?)</helmet>", src, re.S).group(1)
helmet_css = re.search(r"<style>(.*?)</style>", helmet, re.S).group(1).strip()

markup = re.search(r"</helmet>(.*?)</x-dc>", src, re.S).group(1)

script_m = re.search(
    r'<script type="text/x-dc" data-dc-script data-props="([^"]*)">(.*?)</script>',
    src, re.S)
props_defaults_json = html.unescape(script_m.group(1))
logic_src = script_m.group(2)

# default props from the design file's own prop schema (motion=true, startRoute=shipments)
props_schema = json.loads(props_defaults_json)
props = {k: v.get("default") for k, v in props_schema.items()}

# ---- markup transforms (minimal, mechanical) ----
# 1. embed the RyderShare wordmark as a data URI
logo_b64 = base64.b64encode((ROOT / "assets" / "rydershare-logo.png").read_bytes()).decode()
markup, n_logo = re.subn(
    r'src="uploads/pasted-1783059767944-0\.png"',
    f'src="data:image/png;base64,{logo_b64}"',
    markup)
assert n_logo == 1, f"expected 1 logo reference, replaced {n_logo}"

# 2. strip editor-only attributes (runtime would also ignore them; smaller file)
markup = re.sub(r'\s+hint-placeholder-val="\{\{ (?:true|false) \}\}"', "", markup)
markup = re.sub(r'\s+hint-placeholder-count="\d+"', "", markup)
markup = re.sub(r'\s+data-comment-anchor="[^"]*"', "", markup)

leftover = re.findall(r"uploads/[^\"')\s]*", markup)
assert not leftover, f"unembedded upload references remain: {leftover}"

# ---- font: Inter variable (latin subset) as a single embedded face ----
font_b64 = base64.b64encode((ROOT / "assets" / "inter-400.woff2").read_bytes()).decode()
inter_css = (ROOT / "assets" / "inter.css").read_text()
latin_range = None
for subset, body in re.findall(r"/\*\s*([a-z0-9-]+)\s*\*/\s*@font-face\s*\{([^}]+)\}", inter_css):
    if subset == "latin":
        latin_range = re.search(r"unicode-range:\s*([^;]+);", body).group(1).strip()
        break
assert latin_range, "latin unicode-range not found"

font_css = (
    "@font-face{font-family:'Inter';font-style:normal;font-weight:100 900;"
    "font-display:swap;"
    f"src:url(data:font/woff2;base64,{font_b64}) format('woff2');"
    f"unicode-range:{latin_range}}}"
)

runtime_js = (ROOT / "src" / "runtime.js").read_text(encoding="utf-8")

boot_css = (
    # hide the raw template until the first commit resolves bindings
    "body:not(.dc-ready){visibility:hidden}"
    "x-dc{display:contents}"
)

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
<style>{boot_css}</style>
</head>
<body>
<x-dc>{markup}</x-dc>
<script>
{runtime_js}
</script>
<script>
{logic_src}
window.__dcBoot(Component, {json.dumps(props)});
</script>
</body>
</html>
"""

OUT.write_text(out, encoding="utf-8")
print(f"wrote {OUT.name}: {OUT.stat().st_size:,} bytes")
print(f"props: {props}")
