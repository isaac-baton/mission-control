/* V2 — RyderShare Intelligence onboarding layer.
 *
 * Extends the verbatim V1 Component. Pre-enable, the product is "RyderShare
 * today": no AI surfaces (CSS-gated via [data-intel]), the AI rail routes are
 * hidden, and #/insights is a landing page that sells the capability. Enabling
 * runs a short staged activation, then the same route becomes the intelligence
 * hub and every AI surface unlocks with a few seconds of rainbow flash
 * ([data-intel-flash]). In-memory only: reload returns to the un-enabled state
 * (demo reset). `?intel=1` or the startEnabled prop boots straight to enabled.
 */
var __initialHash = (typeof location !== 'undefined' ? location.hash : '');

class ComponentV2 extends Component {
  constructor(props) {
    super(props);
    var self = this;
    this.INTEL_GATED = ['insights', 'agents', 'reviews', 'risk', 'ask', 'workforce'];
    this.VALID = this.VALID.concat(['workforce']);

    // The document-style review shipped as THE reviews screen; the old
    // #/reviews2 preview address stays as an alias.
    if (__initialHash === '#/reviews2') {
      this.state.route = 'reviews';
      try { history.replaceState(null, '', '#/reviews'); } catch (e) {}
    }
    if (__initialHash === '#/workforce') {
      this.state.route = 'workforce';
      try { history.replaceState(null, '', '#/workforce'); } catch (e) {}
    }
    // Risk radar merged into Autopilot (the agents route): every old entry
    // point — cold loads, hash changes, in-app nav — lands on the merged tab.
    if (this.state.route === 'risk') {
      this.state.route = 'agents';
      try { history.replaceState(null, '', '#/agents'); } catch (e) {}
    }
    this.state.revMonth = 'jun'; // reviews month tabs: 'jun' | 'may' | 'apr'

    // A reload is a clean rehearsal reset — nothing persists across refreshes.
    // ?intel=1 is the one deep-link override for booting straight into enabled.
    var startOn = props.startEnabled === true;
    try {
      var qs = new URLSearchParams(location.search);
      if (qs.get('intel') === '1') startOn = true;
      sessionStorage.removeItem('rsIntelState'); // clear any pre-reset-era blob
    } catch (e) {}

    this.state.intel = startOn;
    this.state.intelFlash = '';
    this.state.activating = false;
    this.state.actStep = 0;
    this.state.agLog = null; // which agent's actions log is open ('agEta'|'agDock'|'agAudit'|'agBh')
    this.state.disputeFiled = false; // in-log approval: duplicate-fee dispute
    this.state.tenderSent = false;   // in-log approval: MEM → DAL tender
    this.state.everAsked = false;    // retires the ask bar's New badge
    this.state.noticeOpen = false;   // receiver-notice artifact expander
    this.state.agDwell = true;       // Detention & dwell agent
    this.state.agDocs = true;        // Documents & POD agent
    this.state.agSafety = true;      // Safety coach agent
    this.state.riskExpanded = false; // approved incident details re-expand
    this.state.wfOpen = null;        // workforce showroom: which agent's history is open
    this.state.detClaimFiled = false; // in-log approval: Macon detention claim
    this.state.osdFiled = false;      // in-log approval: OS&D short-shipment claim
    // SBG-31252 — the board's third late load (GPS-offline unit, driver-reported
    // ETA). The Network "No location" tab reconciles the map's 2 late pins with
    // the board's 3; this row is the one an exec would ask to see.
    this.R18 = { ref: 'SBG-31252', ry: '884210395', st: 'STARTED', late: true, dc: 'DC-02', ds: 'AR', cc: 'CC-110', eta: 'today' };
    this.ROWS.push(this.R18);
    this.DET['SBG-31252'] = { o: 'Memphis DC-02', oc: 'Memphis, TN', d: 'Jonesboro loop', c2: 'Jonesboro, AR', m: 5, n: 2, eta: 'Driver-reported 3:40 PM CT', up: '48m ago', dep: 'Departed 6:40 AM CT', tr: 'TR-4451' };

    // Per-agent audit log. The entry mix deliberately encodes the Vision 2025
    // agentic patterns: auto-within-guardrails, confidence-threshold escalation
    // ("routed to you"), agent-to-agent handoffs, self-healing, and the
    // human-feedback loop ("learned from your edit").
    var GREEN = 'background:#E8F5F0;color:#1F7A61', AMBER = 'background:#FEF9E6;color:#655102',
        BLUE = 'background:#ECF4F9;color:#276A92', GREY = 'background:#F5F6F6;color:#44464B';
    this.AGLOG = {
      agEta: {
        title: 'ETA & notifications',
        summary: 'Last 7 days · 23 actions · 19 auto · 3 approved by you · 1 routed to you',
        guard: 'Auto: receiver notices for ETA shifts up to 60 minutes. Needs you: bigger shifts and anything cost-bearing.',
        entries: [
          { t: 'Today · 6:04 AM', title: 'Pushed updated ETA to 2 receivers', d: 'SBG-31241 Savannah corridor — ETA 4:15 PM ET (was 3:05). First-stop dock delay; downstream stops hold.', chip: 'Sent', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Today · 5:52 AM', title: 'Nudged a silent telematics feed', d: 'SBG-31253 went 45 minutes without a ping near Tyler, TX. Re-polled the unit; updates resumed.', chip: 'Resolved', cs: GREEN, who: 'Auto · self-healing' },
          { t: 'Mon Jul 6 · 4:41 PM', title: 'Answered a receiver ETA query', d: 'Savannah receiving asked for tomorrow\u2019s window; replied from the live plan in 40 seconds.', chip: 'Sent', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Mon Jul 6 · 9:15 AM', title: 'Held a notification for review', d: 'SBG-31248 Miami corridor ETA moved 2h 10m — beyond the 60-minute guardrail, so nothing went out without you.', chip: 'Escalated', cs: AMBER, who: 'Routed to you — over guardrail' },
          { t: 'Sun Jul 5 · 6:00 PM', title: 'Sent the weekly receiver digest', d: 'On-time summary and this week’s appointment windows to 14 receiving locations.', chip: 'Sent', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Fri Jul 3 · 3:22 PM', title: 'Updated the delay-notice template', d: 'You shortened the delay-reason wording on Thursday; the edit now applies to every notice.', chip: 'Learned', cs: BLUE, who: 'From your edit · feedback loop' }
        ]
      },
      agDock: {
        title: 'Dock scheduling',
        summary: 'Last 7 days · 17 actions · 14 auto · 2 approved by you · 1 declined by receiver',
        guard: 'Auto: slot requests and swaps at your DCs. Needs you: receiver-side changes it cannot confirm.',
        entries: [
          { t: 'Today · 5:58 AM', title: 'Confirmed storm pre-load dock slots', d: 'Orlando DC-04, Wednesday 6:00–7:00 PM for the 4 pre-load candidates in the storm plan.', chip: 'Confirmed', cs: GREEN, who: 'Handed off from Risk radar' },
          { t: 'Today · 5:30 AM', title: 'Moved a congested receiver window', d: 'Tampa retail #2 backs up Friday afternoons; shifted Friday 1:40 PM to 3:10 PM before it bit.', chip: 'Confirmed', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Mon Jul 6 · 2:05 PM', title: 'Requested an earlier unload window', d: 'SBG-31248 Miami corridor — asked the receiver for 5:00 PM, cutting an estimated 35-minute wait.', chip: 'Pending', cs: AMBER, who: 'Auto · awaiting receiver' },
          { t: 'Mon Jul 6 · 8:12 AM', title: 'Flagged recurring Friday congestion', d: '9 of 12 June missed stops trace to two Tampa docks. Pattern sent to your weekly digest.', chip: 'Flagged', cs: BLUE, who: 'Sent to Insights' },
          { t: 'Thu Jul 2 · 4:44 PM', title: 'Receiver declined a proposed swap', d: 'Macon receiver kept its 9:00 AM window over the proposed 7:00 AM. Your Ryder team follows up.', chip: 'Escalated', cs: AMBER, who: 'Routed to your Ryder team' },
          { t: 'Wed Jul 1 · 7:30 AM', title: 'Booked the week’s dock slots', d: '11 slots across 4 DCs for the week of Jul 6, matched to planned load-out times.', chip: 'Confirmed', cs: GREEN, who: 'Auto · within guardrails' }
        ]
      },
      agAudit: {
        title: 'Invoice audit',
        summary: 'June cycle · 214 lines audited · 1 dispute drafted · $1,120 recovered',
        guard: 'Auto: line-by-line checks against contract rates. Needs you: filing disputes — anything cost-bearing.',
        entries: [
          { t: 'Wed Jul 1 · 6:14 AM', title: 'Verified fuel surcharge against DOE', d: 'June surcharge +$9.3K tracks the index at $3.68/gal — within the contract formula.', chip: 'Clean', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Wed Jul 1 · 6:12 AM', title: 'Explained the accessorial variance', d: '$18.8K — half is the driver-unload surge at Orlando DC-04 (11 events vs. a typical 4).', chip: 'Flagged', cs: AMBER, who: 'Sent to Insights' },
          { t: 'Wed Jul 1 · 6:12 AM', title: 'Audited the June invoice', d: '214 line items against rate schedule C. Nothing ran off-contract.', chip: 'Clean', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Tue Jun 30 · 5:02 PM', title: 'Drafted a duplicate-fee dispute', d: 'Lumper fee billed twice on SBG-31228 ($214). The dispute files when you approve it.', chip: 'Draft', cs: AMBER, who: 'Awaiting your approval', act: 'fileDispute', actLabel: 'Approve & file dispute' },
          { t: 'Fri Jun 26 · 9:40 AM', title: 'Closed two detention disputes', d: 'Carrier credits applied; $1,120 recovered on the June invoice.', chip: 'Recovered', cs: GREEN, who: 'Approved by you' },
          { t: 'Wed Jun 24 · 8:00 AM', title: 'Caught rate-schedule drift', d: '3 lanes were billing at 2025 rates; corrected with billing before the June invoice issued.', chip: 'Fixed', cs: GREEN, who: 'Auto · within guardrails' }
        ]
      },
      agBh: {
        title: 'Backhaul tender',
        summary: 'Draft queue · 1 tender awaiting you · 3 lanes scoped · nothing sends itself',
        guard: 'Auto: matching, pricing, and lane analysis. Needs you: every tender — nothing sends without your approval.',
        entries: [
          { t: 'Today · 5:45 AM', title: 'Refreshed the MEM → DAL tender draft', d: '3 loads/wk of Ryder-managed freight ≈ $3.9K/wk gross; credits net against your invoice. Expires Friday.', chip: 'Draft', cs: AMBER, who: 'Awaiting your approval', act: 'sendTender', actLabel: 'Approve & send tender' },
          { t: 'Mon Jul 6 · 11:20 AM', title: 'Matched network freight to your lane', d: 'MEM → DAL runs 1,860 empty mi/wk; matched against 3 candidate shippers on Ryder’s network desk.', chip: 'Matched', cs: BLUE, who: 'Auto · analysis only' },
          { t: 'Sun Jul 5 · 6:30 PM', title: 'Re-priced the lane at market', d: 'Blended rate held at ≈ $2.05/mi; weekly value unchanged.', chip: 'Updated', cs: GREY, who: 'Auto · analysis only' },
          { t: 'Thu Jul 2 · 3:15 PM', title: 'Scoped the ATL → MEM return lane', d: '1,410 empty mi/wk ≈ $2.9K/wk gross; queued behind MEM → DAL in the opportunity list.', chip: 'Scoped', cs: BLUE, who: 'Auto · analysis only' },
          { t: 'Wed Jul 1 · 10:00 AM', title: 'Sized the full backhaul opportunity', d: 'Three lanes ≈ $458K/yr gross at market; a typical revenue share returns ≈ $320K/yr to SBG.', chip: 'Sized', cs: BLUE, who: 'Sent to Insights' },
          { t: 'Tue Jun 30 · 2:20 PM', title: 'Prepared the enrollment brief', d: 'Per-lane steps and the revenue-share model, ready for your review — lanes enroll one at a time.', chip: 'Ready', cs: GREY, who: 'Awaiting your approval' }
        ]
      },
      agDwell: {
        title: 'Detention & dwell',
        summary: 'June · 41 dock stops timed · $1,120 in evidence handed to Invoice audit · 1 claim ready',
        guard: 'Auto: dwell timing and evidence assembly. Needs you: filing any claim — cost-bearing.',
        entries: [
          { t: 'Today · 7:15 AM', title: 'Timed a 96-minute dock hold', d: 'SBG-31248 Miami receiver held the trailer 36 minutes past free time; evidence pack assembled — geofence stamps + BOL times.', chip: 'Assembled', cs: BLUE, who: 'Auto · within guardrails' },
          { t: 'Mon Jul 6 · 6:10 PM', title: 'Draft detention claim ready — Macon', d: '$186 for 47 minutes over free time on Jul 2; receiver signature and telematics attached. Files when you approve.', chip: 'Draft', cs: AMBER, who: 'Awaiting your approval', act: 'fileDetention', actLabel: 'Approve & file claim' },
          { t: 'Fri Jul 3 · 4:30 PM', title: 'Flagged Tampa retail #2 as chronic', d: 'Fourth consecutive Friday over free time; pattern sent to your weekly digest and Dock scheduling.', chip: 'Flagged', cs: BLUE, who: 'Sent to Insights' },
          { t: 'Wed Jul 1 · 6:12 AM', title: 'Handed detention evidence to Invoice audit', d: 'Two May holds documented; $1,120 in carrier credits filed with the June invoice.', chip: 'Recovered', cs: GREEN, who: 'Handed off to Invoice audit' },
          { t: 'Tue Jun 30 · 3:05 PM', title: 'Learned your free-time terms', d: 'You corrected the Macon contract to 60 minutes; all future timing uses it.', chip: 'Learned', cs: BLUE, who: 'From your edit · feedback loop' }
        ]
      },
      agDocs: {
        title: 'Documents & POD',
        summary: 'June cycle · 214 PODs matched · 2 chased & recovered · 1 OS&D draft',
        guard: 'Auto: chasing, matching, and sharing paperwork. Needs you: anything that changes an invoice or files a claim.',
        entries: [
          { t: 'Today · 6:20 AM', title: 'Matched yesterday\u2019s PODs to loads', d: '14 of 14 in by 6 AM; all signatures clean.', chip: 'Clean', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Mon Jul 6 · 4:41 PM', title: 'Shared the POD pack with Athens retail', d: 'Consignee requested proof of delivery for SBG-31249; sent from the repository with the BOL attached.', chip: 'Sent', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Fri Jul 3 · 11:40 AM', title: 'Chased two missing PODs', d: 'TR-4440 and TR-4442 drivers nudged; both documents in by 5 PM, billing unblocked.', chip: 'Resolved', cs: GREEN, who: 'Auto · self-healing' },
          { t: 'Thu Jul 2 · 9:05 AM', title: 'Drafted an OS&D claim from a POD notation', d: 'Two cases short noted on SBG-31249; $312 claim drafted with photos and BOL line refs.', chip: 'Draft', cs: AMBER, who: 'Awaiting your approval', act: 'fileOsd', actLabel: 'Approve & file OS&D claim' },
          { t: 'Wed Jul 1 · 6:12 AM', title: '3-way matched the June invoice', d: '214 lines against BOLs and PODs for Invoice audit — zero unmatched.', chip: 'Clean', cs: GREEN, who: 'Handed off to Invoice audit' }
        ]
      },
      agSafety: {
        title: 'Safety coach',
        summary: 'TTM 0.4/100K mi · 12 events coached in June · 61-day clean streak',
        guard: 'Auto: micro-coaching for minor events. Escalates: repeated patterns go to the Ryder safety lead — drivers are Ryder\u2019s, reviews stay human.',
        entries: [
          { t: 'Today · 5:40 AM', title: 'Briefed Thursday drivers on the storm corridor', d: 'Start-of-day risk briefing for the 6 storm-plan routes: crosswinds, staging changes, revised windows.', chip: 'Sent', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Mon Jul 6 · 2:50 PM', title: 'Assigned self-coaching for hard braking', d: 'TR-4438 on I-4 near Orlando; the driver completed the module the same day.', chip: 'Coached', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'Thu Jul 2 · 10:15 AM', title: 'Routed a repeat pattern to the Ryder safety lead', d: 'Following-distance alerts on two runs in one week — human review, not automation.', chip: 'Escalated', cs: AMBER, who: 'Routed to your Ryder team' },
          { t: 'Wed Jul 1 · 6:00 AM', title: 'June closed with zero preventable incidents', d: 'Clean streak at 61 days; TTM rate 0.4/100K mi, trending down.', chip: 'Clean', cs: GREEN, who: 'Auto · within guardrails' },
          { t: 'May 2 · 3:00 PM', title: 'Closed the April incident review', d: 'Coaching plan completed; the April business review carries the record.', chip: 'Closed', cs: GREY, who: 'Approved by your Ryder team' }
        ]
      }
    };

    // A cold load on a gated route lands on the landing page instead
    // (#/insights is the landing pre-enable, so it stays reachable).
    if (!startOn) {
      if (['agents', 'reviews', 'reviews2', 'risk'].indexOf(this.state.route) >= 0) {
        this.state.route = 'insights';
        try { history.replaceState(null, '', '#/insights'); } catch (e) {}
      }
      if (this.state.askOpen) { this.state.askOpen = false; this.state.route = 'insights'; try { history.replaceState(null, '', '#/insights'); } catch (e) {} }
    }

    // Ask is part of Intelligence: pre-enable, any entry point routes to the pitch.
    var baseOpenAsk = this.openAsk;
    this.openAsk = function (text, qid) {
      if (!self.state.intel) { self.nav('insights'); return; }
      baseOpenAsk(text, qid);
    };

    // Gate hash navigation to AI routes pre-enable.
    var baseCDM = this.componentDidMount;
    this.componentDidMount = function () {
      baseCDM();
      var origOnHash = self._onHash;
      window.removeEventListener('hashchange', origOnHash);
      self._onHash = function () {
        var h = location.hash.replace(/^#\//, '');
        if (h === 'reviews2') { // legacy preview address
          try { history.replaceState(null, '', '#/reviews'); } catch (e) {}
          h = 'reviews';
        }
        if (h === 'risk') { // merged into Autopilot
          try { history.replaceState(null, '', '#/agents'); } catch (e) {}
          h = 'agents';
        }
        if (!self.state.intel && self.INTEL_GATED.indexOf(h) >= 0 && h !== 'insights') {
          try { history.replaceState(null, '', '#/insights'); } catch (e) {}
          if (self.state.route !== 'insights') self.setRoute('insights');
          return;
        }
        origOnHash();
      };
      window.addEventListener('hashchange', self._onHash);
    };

    var baseRV = this.renderVals;
    this.renderVals = function () {
      var v = baseRV();
      var s = self.state;
      v.dataIntel = s.intel ? 'on' : 'off';
      v.pageTheme = s.route === 'workforce' ? 'dark' : 'light';
      v.intelOn = s.intel;
      v.intelFlash = s.intelFlash;

      // ----- Reviews: month tabs (document review, generated monthly) -----
      var M = s.revMonth;
      v.revJun = M === 'jun'; v.revMay = M === 'may'; v.revApr = M === 'apr';
      var tabOn = 'font-weight:600;color:#1D1D20;box-shadow:inset 0 -2px 0 #1D1D20';
      var tabOff = 'color:#696B6F';
      v.revTabJunSt = v.revJun ? tabOn : tabOff;
      v.revTabMaySt = v.revMay ? tabOn : tabOff;
      v.revTabAprSt = v.revApr ? tabOn : tabOff;
      v.pickMonth = function (e) { self.setState({ revMonth: e.currentTarget.dataset.m }); };
      var REV = {
        jun: { gen: 'Generated Jul 1, 2026 · 42 seconds', meta: 'June 2026 · Prepared for Dana Whitfield · Data through Jun 30, 2026',
               bt: 'Invoice bridge — May to June', bc: 'May $1.706M → June $1.842M · +$136.5K (+8.0%)', st: 'June scorecard',
               src: 'Prepared by RyderShare Intelligence · Sources: Invoice SBG-2026-06 · Load records Jun 1–30 · Contract SBG-DTS-2024',
               sc: ['96.2%', '▲ 2.1 pts', '$248', '▲ $6', '1,187', 'June total', '0', 'preventable', '$180K', '$3.68/gal', '18.4%', '▼ 0.6 pt', '99.2%', '9', '4.2-day avg'] },
        may: { gen: 'Generated Jun 1, 2026 · 38 seconds', meta: 'May 2026 · Prepared for Dana Whitfield · Data through May 31, 2026',
               bt: 'Invoice bridge — April to May', bc: 'April $1.689M → May $1.706M · +$17.0K (+1.0%)', st: 'May scorecard',
               src: 'Prepared by RyderShare Intelligence · Sources: Invoice SBG-2026-05 · Load records May 1–31 · Contract SBG-DTS-2024',
               sc: ['94.1%', '▲ 0.3 pts', '$242', '▲ $2', '1,142', 'May total', '0', 'preventable', '$168K', '$3.49/gal', '19.0%', '▼ 0.2 pt', '99.1%', '11', '4.8-day avg'] },
        apr: { gen: 'Generated May 1, 2026 · 41 seconds', meta: 'April 2026 · Prepared for Dana Whitfield · Data through Apr 30, 2026',
               bt: 'Invoice bridge — March to April', bc: 'March $1.702M → April $1.689M · −$13.0K (−0.8%)', st: 'April scorecard',
               src: 'Prepared by RyderShare Intelligence · Sources: Invoice SBG-2026-04 · Load records Apr 1–30 · Contract SBG-DTS-2024',
               sc: ['93.8%', '▼ 0.4 pts', '$240', '▲ $1', '1,098', 'April total', '1', '0.5/100K TTM', '$161K', '$3.42/gal', '19.2%', '▲ 0.1 pt', '98.9%', '8', '5.1-day avg'] }
      };
      var RM = REV[M] || REV.jun;
      v.revGenerated = RM.gen; v.revMeta = RM.meta;
      v.revBridgeTitle = RM.bt; v.revBridgeCaption = RM.bc;
      v.revScoreTitle = RM.st; v.revSources = RM.src;
      v.scOtd = RM.sc[0]; v.scOtdD = RM.sc[1]; v.scCost = RM.sc[2]; v.scCostD = RM.sc[3];
      v.scLoads = RM.sc[4]; v.scLoadsD = RM.sc[5]; v.scSafety = RM.sc[6]; v.scSafetyD = RM.sc[7];
      v.scFuel = RM.sc[8]; v.scFuelD = RM.sc[9]; v.scEmpty = RM.sc[10]; v.scEmptyD = RM.sc[11];
      v.scBilling = RM.sc[12]; v.scDisputes = RM.sc[13]; v.scDisputesD = RM.sc[14];

      // ----- Board row 19 (SBG-31252): filters, count label, and full re-sort -----
      var R = self.R18;
      var r18vis = true;
      if (s.fStatus === 'LATE') { if (!R.late) r18vis = false; }
      else if (s.fStatus && R.st !== s.fStatus) r18vis = false;
      if (s.fOrigin.length && s.fOrigin.indexOf(R.dc) < 0) r18vis = false;
      if (s.fDest.length && s.fDest.indexOf(R.ds) < 0) r18vis = false;
      if (s.fCc.length && s.fCc.indexOf(R.cc) < 0) r18vis = false;
      if (s.fEta.length && s.fEta.indexOf(R.eta) < 0) r18vis = false;
      var q18 = s.q.trim().toLowerCase();
      if (q18 && R.ref.toLowerCase().indexOf(q18) < 0 && R.ry.indexOf(q18) < 0) r18vis = false;
      v.r18St = r18vis ? '' : 'display:none';
      var nVis = r18vis ? 1 : 0;
      for (var ri = 0; ri < 18; ri++) { if (v['r' + ri + 'St'] === '') nVis++; }
      v.rowsNone = nVis === 0;
      v.showingLabel = nVis === 19 ? 'Showing 19 of 267 · this week · page 1' : 'Showing ' + nVis + ' of 19 on this page';
      var ETAK2 = [14.67, 16.25, 14.92, 16.08, 15.5, 16.17, 999, 15.33, 17.75, 11.53, 11.97, 13.07, 16.33, 15.58, 17.08, 16.42, 17.75, 16.83, 15.67];
      var UPDK2 = [8, 3, 12, 6, 15, 21, 34, 9, 5, 60, 60, 46, 11, 7, 18, 4, 13, 9, 48];
      var STPK2 = [37.5, 40, 71.4, 16.7, 0, 0, 0, 66.7, 66.7, 100, 100, 100, 33.3, 60, 0, 57.1, 20, 33.3, 40];
      var STOK2 = { PLANNED: 0, DISPATCHED: 1, STARTED: 2, COMPLETED: 4 };
      if (s.sortK) {
        var rowAt = function (ii) { return ii === 18 ? R : self.ROWS[ii]; };
        var keyf2 = function (ii) {
          var rr = rowAt(ii);
          if (s.sortK === 'ref') return rr.ref;
          if (s.sortK === 'ry') return rr.ry;
          if (s.sortK === 'st') return (rr.late ? 3 : STOK2[rr.st]);
          if (s.sortK === 'origin') return rr.dc;
          if (s.sortK === 'dest') return self.DET[rr.ref].d;
          if (s.sortK === 'stops') return STPK2[ii];
          if (s.sortK === 'eta') return ETAK2[ii];
          return UPDK2[ii];
        };
        var idxs2 = [];
        for (var qa = 0; qa < 19; qa++) idxs2.push(qa);
        idxs2.sort(function (a2, b2) { var ka = keyf2(a2), kb = keyf2(b2); return (ka < kb ? -1 : ka > kb ? 1 : 0) * s.sortD; });
        for (var qb = 0; qb < 19; qb++) { v['r' + idxs2[qb] + 'Ord'] = 'order:' + qb; }
      } else {
        v.r18Ord = '';
      }

      // ----- Backhaul tile footer reflects the in-log tender approval -----
      v.bhDraftWaiting = !s.tenderSent;
      v.bhTenderSent = s.tenderSent;

      // ----- Value ledger: what Intelligence returned this month -----
      // Stat tiles: number-first, labels flip live on approvals. Plan cost
      // uses the same formula as the risk page so adjustments carry through.
      var pc2 = 1840 + (s.adjWin === '8' ? 310 : 0) + (s.adjRoute === '16' ? 450 : 0);
      var lv = 1120 + (s.disputeFiled ? 214 : 0) + (s.detClaimFiled ? 186 : 0) + (s.osdFiled ? 312 : 0);
      v.ledgerV1 = '$' + lv.toLocaleString('en-US');
      v.ledgerL1 = lv > 1120 ? 'Recovered or in dispute' : 'Recovered in June';
      v.ledgerL2 = s.approved ? 'Failures avoided · +$' + pc2.toLocaleString('en-US') : 'At-risk loads · plan ready';
      // Merged incident module (ex Risk radar): full detail until approved,
      // then a one-line active bar with re-expand.
      v.riskOpen = !s.approved || s.riskExpanded;
      v.riskCollapsed = s.approved && !s.riskExpanded;
      v.riskToggle = function () { self.setState({ riskExpanded: !self.state.riskExpanded }); };
      v.decQueueEmpty = s.tenderGone && s.wSched;

      // Workforce showroom
      v.isWorkforce = s.route === 'workforce';
      v.wfEtaHist = s.wfOpen === 'agEta'; v.wfDockHist = s.wfOpen === 'agDock';
      v.wfAuditHist = s.wfOpen === 'agAudit'; v.wfBhHist = s.wfOpen === 'agBh';
      v.wfDwellHist = s.wfOpen === 'agDwell'; v.wfDocsHist = s.wfOpen === 'agDocs';
      v.wfSafetyHist = s.wfOpen === 'agSafety';
      v.agEtaHistClosed = s.wfOpen !== 'agEta'; v.agDockHistClosed = s.wfOpen !== 'agDock';
      v.agAuditHistClosed = s.wfOpen !== 'agAudit'; v.agBhHistClosed = s.wfOpen !== 'agBh';
      v.agDwellHistClosed = s.wfOpen !== 'agDwell'; v.agDocsHistClosed = s.wfOpen !== 'agDocs';
      v.agSafetyHistClosed = s.wfOpen !== 'agSafety';
      v.wfEntries = s.wfOpen ? self.entriesFor(s.wfOpen).entries : [];
      v.wfHist = function (e) {
        if (e.stopPropagation) e.stopPropagation();
        var k = e.currentTarget.dataset.w;
        self.setState({ wfOpen: self.state.wfOpen === k ? null : k });
      };
      v.wfEtaSum = self.entriesFor('agEta').summary;
      v.wfDockSum = self.entriesFor('agDock').summary;
      v.wfAuditSum = self.entriesFor('agAudit').summary;
      v.wfBhSum = self.entriesFor('agBh').summary;
      v.wfDwellSum = self.entriesFor('agDwell').summary;
      v.wfDocsSum = self.entriesFor('agDocs').summary;
      v.wfSafetySum = self.entriesFor('agSafety').summary;

      // Right-side meta per agent row: when it last acted — live, so a
      // session approval reads "Just now".
      v.agEtaMeta = s.approved ? 'Last action · Just now' : 'Last action · Today 6:04 AM';
      v.agDockMeta = s.approved ? 'Last action · Just now' : 'Last action · Today 5:58 AM';
      v.agAuditMeta = s.disputeFiled ? 'Last action · Just now' : 'Last run · Jul 1';
      v.agBhMeta = s.tenderSent ? 'Tender sent · Just now' : 'Draft waiting · MEM \u2192 DAL';
      v.agDwellMeta = s.detClaimFiled ? 'Last action · Just now' : 'Last action · Today 7:15 AM';
      v.agDocsMeta = s.osdFiled ? 'Last action · Just now' : 'Last action · Today 6:20 AM';
      v.agSafetyMeta = 'Last action · Today 5:40 AM';
      // Toggles sit inside clickable agent rows — don't let the tap bubble
      // into the row's open-log handler.
      var baseTog = v.agToggle;
      v.agToggle = function (e) { if (e.stopPropagation) e.stopPropagation(); baseTog(e); };
      // Weather response is Intelligence: pre-enable the map carries no storm overlay.
      if (!s.intel) v.stormOp = '0';
      v.showLanding = s.route === 'insights' && !s.intel;
      v.showIntelHub = s.route === 'insights' && s.intel;
      v.showGlobalBar = v.showGlobalBar && s.intel;
      // The "New" badge on the ask bars retires after the first question.
      v.p0Emp = v.p0Emp && !s.everAsked;
      v.p1Emp = v.p1Emp && !s.everAsked;
      v.p2Emp = v.p2Emp && !s.everAsked;
      v.actIdle = !s.activating;
      v.activating = s.activating;
      v.act1 = s.actStep >= 1; v.act1Done = s.actStep > 1; v.act1Now = s.actStep === 1;
      v.act2 = s.actStep >= 2; v.act2Done = s.actStep > 2; v.act2Now = s.actStep === 2;
      v.act3 = s.actStep >= 3; v.act3Done = false;         v.act3Now = s.actStep === 3;
      v.enableIntel = function () { self.enableIntel(); };
      // Agent actions log (audit trail side panel on the AI agents screen).
      // The log is live: approvals taken this session — the storm plan, the
      // trailer service, in-log approvals — appear as "Just now" entries, so
      // the audit trail visibly reacts to what the user just did.
      var L = s.agLog ? self.AGLOG[s.agLog] : null;
      v.agLogOpen = !!L && (s.route === 'agents' || s.route === 'workforce');
      v.agLogIsEta = s.agLog === 'agEta';
      v.agLogIsDock = s.agLog === 'agDock';
      v.agLogIsAudit = s.agLog === 'agAudit';
      v.agLogIsBh = s.agLog === 'agBh';
      v.agLogIsDwell = s.agLog === 'agDwell';
      v.agLogIsDocs = s.agLog === 'agDocs';
      v.agLogIsSafety = s.agLog === 'agSafety';
      var swOn2 = 'background:#34A081', swOff2 = 'background:#C5C6C7';
      var knOn2 = 'transform:translateX(14px)', knOff2 = 'transform:translateX(0)';
      ['agDwell', 'agDocs', 'agSafety'].forEach(function (k2) {
        var on = !!s[k2];
        v[k2 + 'On'] = on; v[k2 + 'Off'] = !on;
        v[k2 + 'Track'] = on ? swOn2 : swOff2;
        v[k2 + 'Knob'] = on ? knOn2 : knOff2;
        v[k2 + 'Flash'] = s.agFlash === k2 ? 'on' : '';
      });
      v.agLogTitle = L ? L.title : '';
      v.agLogSummary = L ? L.summary : '';
      v.agLogGuard = L ? L.guard : '';
      var LF = s.agLog ? self.entriesFor(s.agLog) : null;
      if (LF) { v.agLogSummary = LF.summary; }
      v.agLogEntries = LF ? LF.entries : [];
      v.agLogAction = function (e) {
        if (e.stopPropagation) e.stopPropagation();
        var k = e.currentTarget.dataset.k;
        if (k === 'fileDispute') self.setState({ disputeFiled: true });
        else if (k === 'sendTender') self.setState({ tenderSent: true, tenderGone: true });
        else if (k === 'fileDetention') self.setState({ detClaimFiled: true });
        else if (k === 'fileOsd') self.setState({ osdFiled: true });
      };
      // Evidence, not claims: the storm-notice entry expands to the artifact sent.
      v.stormNoticeOpen = !!s.noticeOpen;
      v.noticeToggleLabel = s.noticeOpen ? 'Hide the notice' : 'View the notice it sent →';
      v.toggleNotice = function () { self.setState({ noticeOpen: !self.state.noticeOpen }); };
      v.agLogStatusOn = !!(s.agLog && s[s.agLog]);
      v.agLogStatusOff = !!(s.agLog && !s[s.agLog]);
      v.openAgLog = function (e) {
        if (e.stopPropagation) e.stopPropagation();
        self.setState({ agLog: e.currentTarget.dataset.log });
      };
      v.closeAgLog = function () { self.setState({ agLog: null }); };
      return v;
    };
  }

  // One source of truth for an agent's audit entries + summary, including the
  // live session variants — used by the side panel and the workforce showroom.
  entriesFor(key) {
    var s = this.state;
    var L = this.AGLOG[key];
    var GREEN2 = 'background:#E8F5F0;color:#1F7A61';
    var entries = L.entries, summary = L.summary;
    if (key === 'agEta' && s.approved) {
      entries = [{ t: 'Just now', title: 'Sent storm-plan notices to 6 receivers', d: 'Thursday pre-loads and reroutes confirmed to every affected receiving location, per the plan you approved.', chip: 'Sent', cs: GREEN2, who: 'Handed off from Risk radar — approved by you', exp: 1 }].concat(entries);
    }
    if (key === 'agDock') {
      var pre = [];
      if (s.wSched) pre.push({ t: 'Just now', title: 'Scheduled trailer 4482 service', d: 'Preventive service booked for the open Saturday window at Orlando DC-04 — no route impact.', chip: 'Confirmed', cs: GREEN2, who: 'Approved by you' });
      if (s.approved) pre.push({ t: 'Just now', title: 'Locked Wednesday pre-load slots', d: '4 storm-plan loads staged at Orlando DC-04, 6:00–7:00 PM, per the plan you approved.', chip: 'Confirmed', cs: GREEN2, who: 'Approved by you' });
      entries = pre.concat(entries);
    }
    if (key === 'agAudit' && s.disputeFiled) {
      entries = entries.map(function (en) {
        if (en.act !== 'fileDispute') return en;
        return { t: 'Just now', title: 'Filed the duplicate-fee dispute', d: 'Lumper fee billed twice on SBG-31228 ($214) — dispute submitted to carrier billing.', chip: 'Filed', cs: GREEN2, who: 'Approved by you' };
      });
      summary = 'June cycle · 214 lines audited · 1 dispute filed today · $1,120 recovered';
    }
    if (key === 'agBh' && s.tenderSent) {
      entries = entries.map(function (en) {
        if (en.act !== 'sendTender') return en;
        return { t: 'Just now', title: 'Sent the MEM \u2192 DAL tender', d: '3 loads/wk \u2248 $3.9K/wk gross — tender sent to the Ryder network desk; credits net against your invoice.', chip: 'Sent', cs: GREEN2, who: 'Approved by you' };
      });
      summary = 'Tender sent today · 2 lanes scoped next · nothing sends itself';
    }
    if (key === 'agDwell' && s.detClaimFiled) {
      entries = entries.map(function (en) {
        if (en.act !== 'fileDetention') return en;
        return { t: 'Just now', title: 'Filed the Macon detention claim', d: '$186 claim submitted with telematics evidence; receiver acknowledged receipt.', chip: 'Filed', cs: GREEN2, who: 'Approved by you' };
      });
      summary = 'June · 41 dock stops timed · 1 claim filed today · $1,120 recovered via Invoice audit';
    }
    if (key === 'agDocs' && s.osdFiled) {
      entries = entries.map(function (en) {
        if (en.act !== 'fileOsd') return en;
        return { t: 'Just now', title: 'Filed the OS&D claim', d: '$312 short-shipment claim submitted; the carrier has 30 days to respond.', chip: 'Filed', cs: GREEN2, who: 'Approved by you' };
      });
      summary = 'June cycle · 214 PODs matched · 1 OS&D claim filed today';
    }
    return { entries: entries, summary: summary };
  }

  nav(r) {
    if (r === 'risk') r = 'agents';
    super.nav(r);
  }

  setRoute(r) {
    // Route changes collapse open overlays (detail panel, ask slide-over, map
    // popup, actions log) so the next screen arrives clean; the ask thread
    // itself is preserved — only the panel closes.
    if (r !== this.state.route) {
      var patch = {};
      if (this.state.agLog) patch.agLog = null;
      if (this.state.loadRef) patch.loadRef = null;
      if (this.state.askOpen) patch.askOpen = false;
      if (this.state.marker >= 0) { patch.marker = -1; patch.popPx = null; }
      if (this.state.menu) patch.menu = null;
      for (var k in patch) { this.setState(patch); break; }
    }
    super.setRoute(r);
  }

  submit(text, qid) {
    // First successful ask retires the prompt bar's "New" badge for the session.
    if (!this.state.everAsked) this.setState({ everAsked: true });
    super.submit(text, qid);
  }

  enableIntel() {
    if (this.state.intel || this.state.activating) return;
    var self = this;
    var finish = function () {
      self.setState({ activating: false, actStep: 0, intel: true, intelFlash: 'on' }, function () {
        requestAnimationFrame(function () { if (self._main) self._main.scrollTop = 0; });
      });
      self.t(function () { self.setState({ intelFlash: '' }); }, 5200);
    };
    if (this.rm()) { finish(); return; }
    this.setState({ activating: true, actStep: 1 });
    requestAnimationFrame(function () { if (self._main) self._main.scrollTop = 0; });
    this.t(function () { self.setState({ actStep: 2 }); }, 1700);
    this.t(function () { self.setState({ actStep: 3 }); }, 3400);
    this.t(finish, 5200);
  }
}
