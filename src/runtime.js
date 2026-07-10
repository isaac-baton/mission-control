/* dc-lite — a dependency-free standalone runtime for Claude Design dc templates.
 *
 * Replaces the design-preview stack (support.js + React + ReactDOM + Babel from
 * unpkg) so the prototype runs from file:// with zero network requests, per the
 * PRD build requirements. Implements exactly the template features this design
 * uses, with the same semantics as the preview runtime:
 *
 *   <sc-if value="{{ cond }}">…</sc-if>        conditional mount/unmount
 *   <sc-for list="{{ arr }}" as="x">…</sc-for> keyed-by-index list render, {{ $index }}
 *   {{ path.to.value }}                        text + attribute bindings (dot paths only)
 *   attr="static {{ path }} static"            string-interpolated attributes
 *   onClick="{{ handler }}" etc.               event listeners (onChange ⇒ 'input', like React)
 *   ref="{{ fn }}"                             callback refs; called with null on unmount
 *   style-hover="css"                          generated .cls:hover rule (same as preview)
 *   style="…{{ x }}…"                          full cssText replacement per commit
 *
 * The logic class contract matches the preview's StreamableLogic (aliased DCLogic):
 * this.state, setState(objOrFn, cb) with synchronous commit, renderVals() re-run
 * per commit, componentDidMount after first commit, props merged under renderVals.
 */
(function () {
  'use strict';

  /* ---------- style-hover pseudo-class sheet (mirrors createPseudoSheet) ----------
   * Declarations are stamped !important so authored hover/focus states beat the
   * element's inline style attribute — without it, any property also present
   * inline (nearly all of them here) silently never changes on hover. */
  var pseudoEl = null, pseudoCache = Object.create(null), pseudoN = 0;
  function pseudoClass(pseudo, css) {
    var k = pseudo + '|' + css;
    var hit = pseudoCache[k];
    if (hit) return hit;
    if (!pseudoEl) { pseudoEl = document.createElement('style'); document.head.appendChild(pseudoEl); }
    var cls = 'scp' + (pseudoN++).toString(36);
    var sel = (pseudo === 'before' || pseudo === 'after') ? '.' + cls + '::' + pseudo : '.' + cls + ':' + pseudo;
    var boosted = css.split(';').map(function (d) {
      d = d.trim();
      if (!d || d.indexOf('!important') >= 0) return d;
      return d + ' !important';
    }).filter(Boolean).join(';');
    pseudoEl.sheet.insertRule(sel + '{' + boosted + '}', pseudoEl.sheet.cssRules.length);
    pseudoCache[k] = cls;
    return cls;
  }

  /* ---------- {{ expr }} resolution — identifier dot-paths, $index, true/false ---------- */
  function resolve(scope, expr) {
    expr = expr.trim();
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    var parts = expr.split('.');
    var cur = scope ? scope[parts[0].trim()] : undefined;
    for (var i = 1; i < parts.length; i++) {
      if (cur == null) return undefined;
      cur = cur[parts[i].trim()];
    }
    return cur;
  }

  var BIND_SPLIT = /\{\{([\s\S]+?)\}\}/g;
  var WHOLE = /^\s*\{\{([\s\S]+?)\}\}\s*$/;

  /* attr/text value → getter(scope), or null when static */
  function compileValue(raw) {
    var m = raw.match(WHOLE);
    if (m) {
      var p = m[1];
      return function (scope) { return resolve(scope, p); };
    }
    if (raw.indexOf('{{') < 0) return null;
    var parts = raw.split(BIND_SPLIT);
    return function (scope) {
      var out = '';
      for (var i = 0; i < parts.length; i++) {
        if (i & 1) { var v = resolve(scope, parts[i]); out += (v == null ? '' : v); }
        else out += parts[i];
      }
      return out;
    };
  }

  /* React-equivalent event mapping: onChange on inputs fires per keystroke = 'input' */
  var EVENT_MAP = {
    onclick: 'click', ondblclick: 'dblclick', onchange: 'input', oninput: 'input',
    onsubmit: 'submit', onkeydown: 'keydown', onkeyup: 'keyup', onkeypress: 'keypress',
    onmousedown: 'mousedown', onmousemove: 'mousemove', onmouseup: 'mouseup',
    onmouseenter: 'mouseenter', onmouseleave: 'mouseleave', onwheel: 'wheel',
    onfocus: 'focus', onblur: 'blur', onscroll: 'scroll'
  };

  /* ---------- template compilation ----------
   * Bindings form a tree: if/for own their children so unmounted regions are
   * neither evaluated nor touched. update(scope) applies current values.
   */

  function compileChildren(el, scopeGet) {
    var binds = [];
    var child = el.firstChild;
    while (child) {
      var next = child.nextSibling; // compile may replace nodes
      compileNode(child, binds, scopeGet);
      child = next;
    }
    return binds;
  }

  function compileNode(node, binds, scopeGet) {
    if (node.nodeType === 3) { // text
      if (node.nodeValue.indexOf('{{') >= 0) compileText(node, binds, scopeGet);
      return;
    }
    if (node.nodeType !== 1) return; // comments etc.
    var tag = node.tagName.toLowerCase();
    if (tag === 'sc-if') { compileIf(node, binds, scopeGet); return; }
    if (tag === 'sc-for') { compileFor(node, binds, scopeGet); return; }
    compileAttrs(node, binds, scopeGet);
    var kids = compileChildren(node, scopeGet);
    for (var i = 0; i < kids.length; i++) binds.push(kids[i]);
  }

  function compileText(node, binds, scopeGet) {
    var parts = node.nodeValue.split(BIND_SPLIT);
    var frag = document.createDocumentFragment();
    for (var i = 0; i < parts.length; i++) {
      var t = document.createTextNode(i & 1 ? '' : parts[i]);
      if (i & 1) {
        binds.push({
          t: 'text', node: t, expr: parts[i], last: undefined,
          update: textUpdate, scopeGet: scopeGet
        });
      }
      frag.appendChild(t);
    }
    node.parentNode.replaceChild(frag, node);
  }
  function textUpdate() {
    var v = resolve(this.scopeGet(), this.expr);
    var s = v == null ? '' : String(v);
    if (s !== this.last) { this.last = s; this.node.nodeValue = s; }
  }

  function compileAttrs(el, binds, scopeGet) {
    var attrs = [];
    for (var i = 0; i < el.attributes.length; i++) attrs.push(el.attributes[i]);
    for (var a = 0; a < attrs.length; a++) {
      var name = attrs[a].name, value = attrs[a].value;
      if (name.indexOf('hint-') === 0 || name === 'data-comment-anchor') { el.removeAttribute(name); continue; }
      if (name.indexOf('style-') === 0 && name !== 'style') {
        el.classList.add(pseudoClass(name.slice(6), value));
        el.removeAttribute(name);
        continue;
      }
      var isEvent = name.slice(0, 2) === 'on' && (EVENT_MAP[name] || value.indexOf('{{') >= 0);
      if (isEvent) {
        var evName = EVENT_MAP[name] || name.slice(2).toLowerCase();
        var m = value.match(WHOLE);
        if (m) attachEvent(el, evName, m[1], scopeGet);
        el.removeAttribute(name);
        continue;
      }
      if (name === 'ref') {
        var mr = value.match(WHOLE);
        if (mr) binds.push({ t: 'ref', el: el, expr: mr[1], lastFn: null, update: refUpdate, scopeGet: scopeGet });
        el.removeAttribute(name);
        continue;
      }
      var get = compileValue(value);
      if (!get) continue;
      // property-backed attributes behave like React controlled props
      if (name === 'value' || name === 'checked' || name === 'disabled') el.removeAttribute(name);
      binds.push({ t: 'attr', el: el, name: name, get: get, last: undefined, update: attrUpdate, scopeGet: scopeGet });
    }
  }

  function attachEvent(el, evName, expr, scopeGet) {
    el.addEventListener(evName, function (e) {
      var fn = resolve(scopeGet(), expr);
      if (typeof fn === 'function') fn(e);
    }, evName === 'wheel' ? { passive: true } : false);
  }

  function refUpdate() {
    var fn = resolve(this.scopeGet(), this.expr);
    if (typeof fn === 'function') { this.lastFn = fn; fn(this.el); }
  }

  function attrUpdate() {
    var v = this.get(this.scopeGet());
    if (v === this.last) return;
    this.last = v;
    var el = this.el, name = this.name;
    if (name === 'value') { var s = v == null ? '' : String(v); if (el.value !== s) el.value = s; return; }
    if (name === 'checked') { el.checked = !!v; return; }
    if (name === 'disabled') { el.disabled = !!v; return; }
    if (name === 'style') { el.style.cssText = v == null ? '' : String(v); return; }
    if (v == null || v === false) { el.removeAttribute(name); return; }
    el.setAttribute(name, v === true ? '' : String(v));
  }

  /* ----- sc-if: single compiled instance, mounted/unmounted before an anchor ----- */
  function compileIf(el, binds, scopeGet) {
    var anchor = document.createComment('sc-if');
    el.parentNode.insertBefore(anchor, el);
    var expr = (el.getAttribute('value') || '').match(WHOLE);
    var nodes = [];
    while (el.firstChild) nodes.push(el.removeChild(el.firstChild));
    el.parentNode.removeChild(el);
    // compile children inside a detached holder so structure is walkable
    var holder = document.createDocumentFragment();
    for (var i = 0; i < nodes.length; i++) holder.appendChild(nodes[i]);
    var kidBinds = [];
    var child = holder.firstChild;
    while (child) { var next = child.nextSibling; compileNode(child, kidBinds, scopeGet); child = next; }
    nodes = []; // re-snapshot: compileText may have replaced nodes
    for (var j = 0; j < holder.childNodes.length; j++) nodes.push(holder.childNodes[j]);
    binds.push({
      t: 'if', anchor: anchor, nodes: nodes, kids: kidBinds, holder: holder,
      expr: expr ? expr[1] : 'false', on: false, update: ifUpdate, scopeGet: scopeGet
    });
  }
  function ifUpdate() {
    var want = !!resolve(this.scopeGet(), this.expr);
    if (want && !this.on) {
      var parent = this.anchor.parentNode;
      for (var i = 0; i < this.nodes.length; i++) parent.insertBefore(this.nodes[i], this.anchor);
      this.on = true;
    } else if (!want && this.on) {
      for (var j = 0; j < this.nodes.length; j++) this.holder.appendChild(this.nodes[j]);
      this.on = false;
      detachRefs(this.kids);
      return;
    }
    if (this.on) evalBinds(this.kids);
  }
  function detachRefs(binds) {
    for (var i = 0; i < binds.length; i++) {
      var b = binds[i];
      if (b.t === 'ref' && b.lastFn) { b.lastFn(null); b.lastFn = null; }
      else if (b.t === 'if' && b.on) detachRefs(b.kids);
      else if (b.t === 'for') for (var k = 0; k < b.items.length; k++) detachRefs(b.items[k].kids);
    }
  }

  /* ----- sc-for: template cloned per item; rebuilt when list JSON changes ----- */
  function compileFor(el, binds, scopeGet) {
    var anchor = document.createComment('sc-for');
    el.parentNode.insertBefore(anchor, el);
    var expr = (el.getAttribute('list') || '').match(WHOLE);
    var asName = el.getAttribute('as') || 'item';
    var tpl = document.createDocumentFragment();
    while (el.firstChild) tpl.appendChild(el.removeChild(el.firstChild));
    el.parentNode.removeChild(el);
    binds.push({
      t: 'for', anchor: anchor, tpl: tpl, asName: asName,
      expr: expr ? expr[1] : '', items: [], list: [],
      update: forUpdate, scopeGet: scopeGet
    });
  }
  // Index-keyed reconciliation, matching React's behavior for unkeyed lists:
  // existing instances keep their DOM (their bindings re-evaluate against the
  // item now at that index — nested sc-ifs mount/unmount as needed), new
  // indexes append fresh instances, extras are removed from the end. This is
  // what keeps the chat thread stable when a message is added: old bubbles
  // are untouched and only the new ones run their entrance animations.
  function forUpdate() {
    var self = this;
    var list = resolve(this.scopeGet(), this.expr);
    if (!Array.isArray(list)) list = [];
    this.list = list;
    while (this.items.length > list.length) {
      var it = this.items.pop();
      detachRefs(it.kids);
      for (var n = 0; n < it.nodes.length; n++) {
        var nd = it.nodes[n];
        if (nd.parentNode) nd.parentNode.removeChild(nd);
      }
    }
    var parent = this.anchor.parentNode;
    for (var x = this.items.length; x < list.length; x++) {
      (function (ix) {
        var itemScopeGet = function () {
          var base = self.scopeGet();
          var s = Object.assign({}, base);
          s[self.asName] = self.list[ix];
          s.$index = ix;
          return s;
        };
        var frag = self.tpl.cloneNode(true);
        var kidBinds = [];
        var child = frag.firstChild;
        while (child) { var next = child.nextSibling; compileNode(child, kidBinds, itemScopeGet); child = next; }
        var nodes = [];
        for (var j = 0; j < frag.childNodes.length; j++) nodes.push(frag.childNodes[j]);
        parent.insertBefore(frag, self.anchor);
        self.items.push({ nodes: nodes, kids: kidBinds });
      })(x);
    }
    for (var k = 0; k < this.items.length; k++) evalBinds(this.items[k].kids);
  }

  function evalBinds(binds) {
    for (var i = 0; i < binds.length; i++) binds[i].update();
  }

  /* ---------- logic base class (mirrors StreamableLogic) ---------- */
  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
    this.__host = null;
  }
  DCLogic.prototype.setState = function (update, cb) {
    if (this.__host) this.__host.setLogicState(update, cb);
  };
  DCLogic.prototype.forceUpdate = function () {
    if (this.__host) this.__host.commit();
  };
  DCLogic.prototype.componentDidMount = function () {};
  DCLogic.prototype.componentWillUnmount = function () {};
  DCLogic.prototype.renderVals = function () { return {}; };

  /* ---------- host: compile once, commit synchronously on setState ---------- */
  function boot(Component, props) {
    var rootEl = document.querySelector('x-dc');
    var vals = {};
    var scopeGet = function () { return vals; };
    var rootBinds = compileChildren(rootEl, scopeGet);

    var logic = new Component(props || {});
    var committing = false;
    var host = {
      setLogicState: function (update, cb) {
        var patch = typeof update === 'function' ? update(logic.state) : update;
        if (patch) logic.state = Object.assign({}, logic.state, patch);
        host.commit();
        if (cb) cb();
      },
      commit: function () {
        if (committing) return; // renderVals must not re-enter
        committing = true;
        try {
          vals = Object.assign({}, logic.props, logic.renderVals());
          evalBinds(rootBinds);
        } finally {
          committing = false;
        }
      }
    };
    logic.__host = host;
    host.commit();
    document.body.classList.add('dc-ready');
    if (typeof logic.componentDidMount === 'function') logic.componentDidMount();
    return logic;
  }

  window.DCLogic = DCLogic;
  window.__dcBoot = boot;
})();
