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
class ComponentV2 extends Component {
  constructor(props) {
    super(props);
    var self = this;
    this.INTEL_GATED = ['insights', 'agents', 'reviews', 'risk', 'ask'];

    var startOn = props.startEnabled === true;
    try {
      if (new URLSearchParams(location.search).get('intel') === '1') startOn = true;
    } catch (e) {}

    this.state.intel = startOn;
    this.state.intelFlash = '';
    this.state.activating = false;
    this.state.actStep = 0;

    // A cold load on a gated route lands on the landing page instead
    // (#/insights is the landing pre-enable, so it stays reachable).
    if (!startOn) {
      if (['agents', 'reviews', 'risk'].indexOf(this.state.route) >= 0) {
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
      v.intelOn = s.intel;
      v.intelFlash = s.intelFlash;
      // Weather response is Intelligence: pre-enable the map carries no storm overlay.
      if (!s.intel) v.stormOp = '0';
      v.showLanding = s.route === 'insights' && !s.intel;
      v.showIntelHub = s.route === 'insights' && s.intel;
      v.showGlobalBar = v.showGlobalBar && s.intel;
      v.actIdle = !s.activating;
      v.activating = s.activating;
      v.act1 = s.actStep >= 1; v.act1Done = s.actStep > 1; v.act1Now = s.actStep === 1;
      v.act2 = s.actStep >= 2; v.act2Done = s.actStep > 2; v.act2Now = s.actStep === 2;
      v.act3 = s.actStep >= 3; v.act3Done = false;         v.act3Now = s.actStep === 3;
      v.enableIntel = function () { self.enableIntel(); };
      return v;
    };
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
