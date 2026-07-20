# Generates src/v2/workforce.html — the dark Agents showroom page.
# Run from the project root: python3 src/v2/gen_workforce.py
from pathlib import Path

# Hues scatter warm/cool across the 2-col grid so no column or diagonal
# reads as a same-color group: blue|orange / green|purple / yellow|red / cyan|teal.
HUES = {
 'agEta':   ('#5AC8FA', 'Eta'), 'agDock':  ('#FFB86B', 'Dock'), 'agAudit': ('#4CD9A8', 'Audit'),
 'agBh':    ('#A78BFA', 'Bh'), 'agDwell': ('#FFD84D', 'Dwell'), 'agDocs':  ('#FF5C5C', 'Docs'),
 'agSafety':('#9BE8FF', 'Safety'), 'agFlex': ('#2DD4BF', 'Flex'),
}
ICONS = {
 'agEta':   '<path d="m22 2-7 20-4-9-9-4z"></path><path d="M22 2 11 13"></path>',
 'agDock':  '<rect x="3" y="4" width="18" height="18" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line>',
 'agAudit': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"></path><path d="M14 2v4a2 2 0 0 0 2 2h4"></path><line x1="8" y1="13" x2="16" y2="13"></line><line x1="8" y1="17" x2="14" y2="17"></line>',
 'agBh':    '<path d="m17 2 4 4-4 4"></path><path d="M3 11v-1a4 4 0 0 1 4-4h14"></path><path d="m7 22-4-4 4-4"></path><path d="M21 13v1a4 4 0 0 1-4 4H3"></path>',
 'agDwell': '<line x1="10" x2="14" y1="2" y2="2"></line><line x1="12" x2="15" y1="14" y2="11"></line><circle cx="12" cy="14" r="8"></circle>',
 'agDocs':  '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z"></path><path d="M14 2v4a2 2 0 0 0 2 2h4"></path><path d="m9 15 2 2 4-4"></path>',
 'agSafety':'<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1 1 0 0 1 1.52 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"></path><path d="m9 12 2 2 4-4"></path>',
 'agFlex':  '<path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.8-1.1 2-1.7 3.3-1.7H22"></path><path d="m18 2 4 4-4 4"></path><path d="M2 6h1.9c1.5 0 2.9.9 3.6 2.2"></path><path d="M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8"></path><path d="m18 22 4-4-4-4"></path>',
}
META = {
 'agEta':   ('ETA &amp; notifications', 'Sends updated delivery ETAs to receivers automatically; delays over 60 minutes are held for you.', 'Auto: receiver notices for ETA shifts up to 60 minutes. Needs you: bigger shifts and anything cost-bearing.'),
 'agDock':  ('Dock scheduling', 'Books and reshuffles dock slots at your DCs autonomously; receiver-side changes need a yes.', 'Auto: slot requests and swaps at your DCs. Needs you: receiver-side changes it cannot confirm.'),
 'agAudit': ('Invoice audit', 'Audits every invoice line against contract rates; drafts disputes that file on your approval.', 'Auto: line-by-line checks against contract rates. Needs you: filing disputes — anything cost-bearing.'),
 'agBh':    ('Backhaul tender', 'Scouts empty lanes and drafts tenders; the analysis runs automatically and every tender waits for your approval.', 'Auto: matching, pricing, and lane analysis. Needs you: every tender — nothing sends without your approval.'),
 'agDwell': ('Detention &amp; dwell', 'Times every dock hold and assembles claim evidence; filing always waits for your approval.', 'Auto: dwell timing and evidence assembly. Needs you: filing any claim — cost-bearing.'),
 'agDocs':  ('Documents &amp; POD', 'Chases, matches, and shares paperwork on its own; anything touching an invoice needs you.', 'Auto: chasing, matching, and sharing paperwork. Needs you: anything that changes an invoice or files a claim.'),
 'agSafety':('Safety coach', 'Turns telematics events into driver coaching; repeat patterns escalate to your Ryder safety lead.', 'Auto: micro-coaching for minor events. Escalates: repeated patterns go to your Ryder safety lead, and a person reviews every case.'),
 'agFlex':  ('Adaptive capacity', 'Re-prices every lane against the spot market weekly and drafts flex moves in both directions — locking loads into dedicated rates or releasing them to brokerage.', 'Auto: lane-level rate watch and eligibility checks. Needs you: every flex move — dual sign-off with your Ryder account team before any load changes mode.'),
}
SUMS = {'agEta':'wfEtaSum','agDock':'wfDockSum','agAudit':'wfAuditSum','agBh':'wfBhSum','agDwell':'wfDwellSum','agDocs':'wfDocsSum','agSafety':'wfSafetySum','agFlex':'wfFlexSum'}


def backdrop(key):
    """Aura wash + particle dots + a large faint outline of the agent's icon,
    clipped inside the card so the enable-flash ring can live on the card edge."""
    hue, suf = HUES[key]
    return (f'<div style="position:absolute;inset:0;border-radius:13px;overflow:hidden;pointer-events:none" aria-hidden="true">'
            f'<svg style="position:absolute;inset:0;width:100%;height:100%" viewBox="0 0 520 260" preserveAspectRatio="xMidYMid slice">'
            f'<defs>'
            f'<radialGradient id="wfa{suf}" cx="82%" cy="10%" r="75%"><stop offset="0%" stop-color="{hue}" stop-opacity="0.34"/><stop offset="55%" stop-color="{hue}" stop-opacity="0.10"/><stop offset="100%" stop-color="{hue}" stop-opacity="0"/></radialGradient>'
            f'<radialGradient id="wfb{suf}" cx="8%" cy="100%" r="60%"><stop offset="0%" stop-color="{hue}" stop-opacity="0.14"/><stop offset="100%" stop-color="{hue}" stop-opacity="0"/></radialGradient>'
            f'</defs>'
            f'<rect width="520" height="260" fill="url(#wfa{suf})"/>'
            f'<rect width="520" height="260" fill="url(#wfb{suf})"/>'
            f'</svg>'
            f'<svg width="150" height="150" viewBox="0 0 24 24" fill="none" stroke="{hue}" stroke-opacity="0.11" stroke-width="0.45" stroke-linecap="round" stroke-linejoin="round" style="position:absolute;right:-20px;bottom:-34px;transform:rotate(-9deg)">{ICONS[key]}</svg>'
            f'</div>')


def card(key):
    hue, _ = HUES[key]
    name, desc, guard = META[key]
    return f'''            <div data-aiflash="{{{{ {key}Flash }}}}" style="position:relative;background:#17181C;border:1px solid #26272C;border-radius:14px;padding:24px 26px;display:flex;flex-direction:column;gap:12px">
              {backdrop(key)}
              <div style="position:relative;display:flex;align-items:center;gap:12px">
                <span style="width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);display:flex;align-items:center;justify-content:center;flex:none"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{hue}" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</svg></span>
                <span style="font-size:19px;font-weight:600;color:#F4F5F7;letter-spacing:-0.01em">{name}</span>
                <sc-if value="{{{{ {key}On }}}}"><span style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:10.5px;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;background:rgba(52,160,129,0.16);color:#5BDCAF;border:1px solid rgba(91,220,175,0.25)">Active</span></sc-if>
                <sc-if value="{{{{ {key}Off }}}}"><span style="display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:10.5px;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;background:rgba(255,255,255,0.07);color:#9BA0A8;border:1px solid rgba(255,255,255,0.12)">Paused</span></sc-if>
                <span style="flex:1"></span>
                <button data-a="{key}" onClick="{{{{ agToggle }}}}" aria-label="Toggle {name}" style="width:34px;height:20px;border-radius:999px;border:0;cursor:pointer;position:relative;transition:background .15s ease;flex:none;{{{{ {key}Track }}}}"><span style="position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,0.4);transition:transform .15s ease;{{{{ {key}Knob }}}}"></span></button>
              </div>
              <div style="position:relative;font-size:13.5px;color:#C4C8CF;line-height:1.6">{desc}</div>
              <div style="position:relative;font-size:12px;color:#82868E;line-height:1.55">{guard}</div>
              <div style="position:relative;display:flex;align-items:center;gap:10px;margin-top:2px;flex-wrap:wrap">
                <span style="font-size:12px;color:{hue};font-variant-numeric:tabular-nums">{{{{ {SUMS[key]} }}}}</span>
                <span style="flex:1"></span>
                <button data-log="{key}" onClick="{{{{ openAgLog }}}}" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);color:#E8EAED;border-radius:7px;padding:6px 13px;font-size:12px;font-weight:500;cursor:pointer;font-family:inherit;white-space:nowrap" style-hover="background:rgba(255,255,255,0.12)">View history</button>
              </div>
            </div>
'''


cards = ''.join(card(k) for k in HUES)
page = f'''<sc-if value="{{{{ isWorkforce }}}}">
        <div data-screen-label="Workforce" style="min-height:100%;padding:26px 24px 160px">
          <div style="max-width:1100px;margin:0 auto;animation:rev .45s ease both">
            <div style="display:flex;align-items:center;gap:8px">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#5AC8FA" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M9.94 15.5a2 2 0 0 0-1.44-1.44l-6.13-1.58a.5.5 0 0 1 0-.96L8.5 9.94a2 2 0 0 0 1.44-1.44l1.58-6.13a.5.5 0 0 1 .96 0l1.58 6.13a2 2 0 0 0 1.44 1.44l6.13 1.58a.5.5 0 0 1 0 .96l-6.13 1.58a2 2 0 0 0-1.44 1.44l-1.58 6.13a.5.5 0 0 1-.96 0z"></path></svg>
              <span style="font-size:11px;font-weight:500;letter-spacing:0.04em;text-transform:uppercase;color:#8A8F98">Your workforce</span>
            </div>
            <div style="font-size:30px;font-weight:600;color:#F4F5F7;letter-spacing:-0.01em;margin-top:12px;line-height:1.2">8 AI agents at your disposal</div>
            <div style="font-size:13.5px;color:#8A8F98;margin-top:8px">Every action is logged and reversible · anything cost-bearing waits for you · repeat patterns go to your Ryder team</div>
            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin-top:28px">
{cards}            </div>
            <div style="font-size:11.5px;color:#5C6066;margin-top:26px">Agents run on the records that already run your freight — loads, invoices, telematics, contracts. Tune any guardrail with your Ryder team.</div>
          </div>
        </div>
        </sc-if>
'''
out = Path(__file__).parent / 'workforce.html'
out.write_text(page)
print(f'wrote {out.name}: {len(page)} chars')
