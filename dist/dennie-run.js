/*!
 * <dennie-run> — a tiny endless runner for imdennie.com
 * Drop-in Web Component. No dependencies. ~15 KB (~5 KB gzipped).
 *
 * Usage:
 *   <script src="/dennie-run.js" defer></script>
 *   <dennie-run></dennie-run>
 *
 * Optional attributes:
 *   contact-href="#contact"   link shown after a great run (score ≥ 1000)
 *   height="120"              canvas height in px
 *
 * Inherits color + font from its parent, so it matches light and dark themes.
 * Accent can be set with CSS:  dennie-run { --dennie-run-accent: #3b5bdb; }
 */
(function () {
  if (customElements.get('dennie-run')) return;

  var LABELS = ['Bug', 'Scope creep', 'Meeting', 'Edge case', 'Feedback', 'Jira',
    'v2', 'Pixel push', 'Deadline', 'Legacy code', 'Quick sync', 'One more tweak'];
  var MILESTONES = [
    [100, 'Tysha shipped ✓'],
    [300, 'Numi shipped ✓'],
    [600, 'Karta shipped ✓'],
    [1000, 'Unstoppable. Let’s talk.']
  ];
  var STORE_KEY = 'dennie-run-best';
  var G = 0.56, JUMP_V = 9.6, CUT_V = 3.4, R = 7;

  function readBest() { try { return +localStorage.getItem(STORE_KEY) || 0; } catch (e) { return 0; } }
  function saveBest(v) { try { localStorage.setItem(STORE_KEY, String(v)); } catch (e) {} }
  function rand(a, b) { return a + Math.random() * (b - a); }
  function pad(n) { return String(Math.floor(n)).padStart(5, '0'); }

  class DennieRun extends HTMLElement {
    connectedCallback() {
      if (this._root) return;
      var root = this._root = this.attachShadow({ mode: 'open' });
      var h = parseInt(this.getAttribute('height'), 10) || 120;
      root.innerHTML =
        '<style>' +
        ':host{display:block;color:inherit;font:inherit;-webkit-tap-highlight-color:transparent;-webkit-user-select:none;user-select:none}' +
        '.wrap{position:relative;cursor:pointer;outline:none;border-radius:10px;touch-action:manipulation}' +
        '.wrap:focus-visible{box-shadow:0 0 0 2px currentColor}.wrap.ptr:focus-visible{box-shadow:none}' +
        'canvas{display:block;width:100%;height:' + h + 'px}' +
        '.status{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:6px;font-size:12px;line-height:1.4;min-height:1.4em;font-variant-numeric:tabular-nums}' +
        '.l{opacity:.6}.r{opacity:.45;white-space:nowrap}' +
        'a{color:inherit;opacity:1;text-underline-offset:3px}' +
        '</style>' +
        '<div class="wrap" tabindex="0" role="application" aria-label="Mini game. Press Space or tap to jump over obstacles.">' +
        '<canvas></canvas></div>' +
        '<div class="status"><span class="l" aria-live="polite"></span><span class="r"></span></div>';

      this.$wrap = root.querySelector('.wrap');
      this.$cv = root.querySelector('canvas');
      this.$l = root.querySelector('.l');
      this.$r = root.querySelector('.r');
      this.ctx = this.$cv.getContext('2d');
      this.best = readBest();
      this.reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
      this.fine = matchMedia('(pointer: fine)').matches;
      this.visible = true;
      this.state = 'idle';
      this.t = 0;
      this._loop = this._loop.bind(this);

      this._bind();
      this._resize();
      this._reset();
      this._status();
      this._kick();
    }

    disconnectedCallback() {
      cancelAnimationFrame(this._raf); this._raf = 0;
      this._ro && this._ro.disconnect();
      this._io && this._io.disconnect();
      document.removeEventListener('visibilitychange', this._onVis);
    }

    /* ---------- setup ---------- */
    _bind() {
      var self = this, w = this.$wrap, down = null;
      w.addEventListener('pointerdown', function (e) {
        if (e.button > 0) return;
        down = { x: e.clientX, y: e.clientY, touch: e.pointerType !== 'mouse' };
        w.classList.add('ptr');
        if (!down.touch) { e.preventDefault(); w.focus({ preventScroll: true }); }
        // During a run, jump immediately. When idle on touch, wait for a real tap (not a scroll).
        if (self.state === 'run' || !down.touch) self._press();
      });
      w.addEventListener('pointerup', function (e) {
        if (down && down.touch && self.state !== 'run' &&
            Math.hypot(e.clientX - down.x, e.clientY - down.y) < 10) self._press();
        down = null; self._release();
      });
      w.addEventListener('pointercancel', function () { down = null; self._release(); });
      w.addEventListener('keydown', function (e) {
        w.classList.remove('ptr');
        if (e.code === 'Space' || e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Enter') {
          e.preventDefault(); if (!e.repeat) self._press();
        }
      });
      w.addEventListener('keyup', function (e) {
        if (e.code === 'Space' || e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Enter') self._release();
      });
      w.addEventListener('blur', function () { if (self.state === 'run') self._pause(); });

      this._ro = new ResizeObserver(function () { self._resize(); self._draw(); });
      this._ro.observe(w);
      this._io = new IntersectionObserver(function (en) {
        self.visible = en[0].isIntersecting;
        if (!self.visible && self.state === 'run') self._pause();
        self._kick();
      });
      this._io.observe(w);
      this._onVis = function () { if (document.hidden && self.state === 'run') self._pause(); };
      document.addEventListener('visibilitychange', this._onVis);
    }

    _resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.W = this.$cv.clientWidth || 300;
      this.H = this.$cv.clientHeight || 120;
      this.$cv.width = Math.round(this.W * dpr);
      this.$cv.height = Math.round(this.H * dpr);
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      this.groundY = this.H - 24;
      this.px = Math.min(56, this.W * 0.14);
      this.maxSpeed = Math.min(11.5, 6.5 + this.W / 140);
    }

    _reset() {
      this.dist = 0; this.score = 0; this.speed = 5;
      this.h = 0; this.vh = 0; this.held = false; this.buffer = 0; this.land = 0;
      this.obs = []; this.msgs = []; this.mi = 0; this.hitBy = null;
      this.nextGap = this.W * 0.6;
    }

    /* ---------- input ---------- */
    _press() {
      var now = performance.now();
      if (this.state === 'over' && now - this.overAt < 450) return;
      if (this.state === 'idle' || this.state === 'over') { this._reset(); this.state = 'run'; this._status(); this._kick(); this._jump(); return; }
      if (this.state === 'paused') { this.state = 'run'; this._status(); this._kick(); return; }
      this.held = true;
      if (this.h <= 0.01) this._jump(); else this.buffer = 8; // jump buffer
    }
    _release() {
      this.held = false;
      if (this.state === 'run' && this.vh > CUT_V) this.vh = CUT_V; // short hop
    }
    _jump() { this.held = true; this.vh = JUMP_V; this.h = 0.01; }

    _pause() { this.state = 'paused'; this._status(); this._draw(); }

    /* ---------- loop ---------- */
    _kick() {
      var animIdle = this.state === 'idle' && !this.reduced;
      var need = this.visible && !document.hidden && (this.state === 'run' || animIdle);
      if (need && !this._raf) { this._last = performance.now(); this._raf = requestAnimationFrame(this._loop); }
      if (!need) this._draw();
    }

    _loop(now) {
      this._raf = 0;
      var dt = Math.min(2, (now - this._last) / 16.667); this._last = now;
      this.t += dt;
      if (this.state === 'run') this._step(dt);
      this._draw();
      this._kick();
    }

    _step(dt) {
      // speed ramps with score
      this.speed = Math.min(this.maxSpeed, 5 + this.score * 0.0065);
      var dx = this.speed * dt;
      this.dist += dx;
      this.score = this.dist / 25;

      // player physics
      if (this.h > 0) {
        this.vh -= G * dt;
        this.h += this.vh * dt;
        if (this.h <= 0) {
          this.h = 0; this.vh = 0; this.land = 1;
          if (this.buffer > 0) { this._jump(); this.held = false; }
        }
      }
      if (this.buffer > 0) this.buffer -= dt;
      if (this.land > 0) this.land = Math.max(0, this.land - 0.12 * dt);

      // obstacles
      var ctx = this.ctx; ctx.font = this._font(11, 500);
      for (var i = 0; i < this.obs.length; i++) this.obs[i].x -= dx;
      while (this.obs.length && this.obs[0].x + this.obs[0].w < -10) this.obs.shift();
      var lastX = this.obs.length ? this.obs[this.obs.length - 1].x + this.obs[this.obs.length - 1].w : -Infinity;
      if (this.W - lastX > this.nextGap) {
        var label = LABELS[(Math.random() * LABELS.length) | 0];
        var w = Math.min(96, Math.ceil(ctx.measureText(label).width) + 16);
        this.obs.push({ x: this.W + 4, w: w, h: Math.round(rand(17, 23)), label: label });
        var minGap = 170 + this.speed * 17;
        this.nextGap = rand(minGap, minGap + 230);
      }

      // collision (forgiving circle vs rounded rect)
      var cx = this.px, cy = this.groundY - R - this.h, rr = R * 0.82;
      for (var j = 0; j < this.obs.length; j++) {
        var o = this.obs[j], top = this.groundY - o.h;
        var nx = Math.max(o.x + 2, Math.min(cx, o.x + o.w - 2));
        var ny = Math.max(top + 2, Math.min(cy, this.groundY));
        if ((cx - nx) * (cx - nx) + (cy - ny) * (cy - ny) < rr * rr) { this._over(o.label); return; }
      }

      // milestones
      if (this.mi < MILESTONES.length && this.score >= MILESTONES[this.mi][0]) {
        this.msgs.push({ text: MILESTONES[this.mi][1], t: 0 });
        this.mi++;
      }
      for (var k = this.msgs.length - 1; k >= 0; k--) { this.msgs[k].t += dt; if (this.msgs[k].t > 120) this.msgs.splice(k, 1); }
    }

    _over(label) {
      this.state = 'over'; this.hitBy = label; this.overAt = performance.now();
      var s = Math.floor(this.score);
      if (s > this.best) { this.best = s; saveBest(s); this.newBest = true; } else this.newBest = false;
      this._status();
    }

    /* ---------- render ---------- */
    _font(size, weight) {
      var fam = getComputedStyle(this).fontFamily || 'system-ui, sans-serif';
      return (weight || 400) + ' ' + size + 'px ' + fam;
    }

    _draw() {
      var ctx = this.ctx, W = this.W, H = this.H, gy = this.groundY;
      var cs = getComputedStyle(this);
      var fg = cs.color || '#111';
      var accent = cs.getPropertyValue('--dennie-run-accent').trim() || fg;
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = fg; ctx.strokeStyle = fg;

      // ground: a designer's ruler
      ctx.globalAlpha = 0.28; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(0, gy + 0.5); ctx.lineTo(W, gy + 0.5); ctx.stroke();
      ctx.globalAlpha = 0.22;
      var off = this.dist % 10;
      for (var x = -off, n = Math.floor(this.dist / 10); x < W; x += 10, n++) {
        var len = n % 10 === 0 ? 7 : n % 5 === 0 ? 4.5 : 2.5;
        ctx.fillRect(Math.round(x), gy + 1, 1, len);
      }

      // obstacles: pill-shaped "blockers"
      ctx.font = this._font(11, 500); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      for (var i = 0; i < this.obs.length; i++) {
        var o = this.obs[i], top = gy - o.h, r = Math.min(o.h / 2, 9);
        var hit = this.state === 'over' && o.label === this.hitBy && o.x < this.px + 20 && o.x + o.w > this.px - 20;
        ctx.beginPath(); this._rr(o.x, top, o.w, o.h, r);
        ctx.globalAlpha = hit ? 0.9 : 0.07; ctx.fillStyle = hit ? accent : fg; ctx.fill();
        ctx.globalAlpha = 0.75; ctx.strokeStyle = hit ? accent : fg; ctx.lineWidth = 1; ctx.stroke();
        ctx.globalAlpha = hit ? 1 : 0.85; ctx.fillStyle = fg;
        if (hit) { ctx.save(); ctx.globalCompositeOperation = 'destination-out'; }
        ctx.fillText(o.label, o.x + o.w / 2, top + o.h / 2 + 0.5);
        if (hit) ctx.restore();
      }
      ctx.fillStyle = fg; ctx.strokeStyle = fg;

      // player: the dot from "dennie."
      var h = this.h;
      if (this.state === 'idle' && !this.reduced) h = Math.max(0, Math.sin(this.t / 11)) * 6;
      var stretch = Math.min(Math.abs(this.vh) / 40, 0.18);
      var sy = 1 + stretch - this.land * 0.22, sx = 1 / sy;
      var cx = this.px, cy = gy - R * sy - h;
      ctx.globalAlpha = 0.12 * Math.max(0, 1 - h / 70);
      ctx.beginPath(); ctx.ellipse(cx, gy + 2, R * (1 - h / 140), 1.6, 0, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.ellipse(cx, cy, R * sx, R * sy, 0, 0, Math.PI * 2);
      if (this.state === 'over') { ctx.lineWidth = 2; ctx.strokeStyle = accent; ctx.stroke(); }
      else { ctx.fillStyle = this.state === 'run' ? accent : fg; ctx.fill(); }
      ctx.fillStyle = fg; ctx.strokeStyle = fg;

      // score
      ctx.textAlign = 'right'; ctx.textBaseline = 'top';
      ctx.font = this._font(11, 500);
      if (this.state !== 'idle') {
        ctx.globalAlpha = 0.85; ctx.fillText(pad(this.score), W - 2, 6);
        if (this.best) { ctx.globalAlpha = 0.4; ctx.fillText('HI ' + pad(this.best) + '   ', W - 2 - ctx.measureText(pad(this.score)).width, 6); }
      }

      // milestone toasts
      ctx.textAlign = 'left'; ctx.font = this._font(12, 600);
      for (var k = 0; k < this.msgs.length; k++) {
        var m = this.msgs[k], a = m.t < 12 ? m.t / 12 : m.t > 90 ? Math.max(0, (120 - m.t) / 30) : 1;
        ctx.globalAlpha = a; ctx.fillStyle = accent;
        ctx.fillText(m.text, 2, 6 + (this.reduced ? 0 : (1 - Math.min(1, m.t / 12)) * 6));
      }
      ctx.globalAlpha = 1; ctx.fillStyle = fg;

      // center hint in idle / paused
      if (this.state === 'idle' || this.state === 'paused') {
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.font = this._font(12, 500);
        ctx.globalAlpha = 0.5;
        ctx.fillText(this.state === 'paused' ? 'Paused' : 'Ship it. Dodge the blockers.', W / 2, gy / 2 + 4);
        ctx.globalAlpha = 1;
      }
    }

    _rr(x, y, w, h, r) {
      var c = this.ctx;
      c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r);
      c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath();
    }

    _status() {
      var act = this.fine ? 'Press Space or click' : 'Tap';
      var best = this.best ? 'Best ' + this.best : '';
      var l = '', r = best;
      if (this.state === 'idle') l = act + ' to play';
      else if (this.state === 'run') { l = ''; r = ''; }
      else if (this.state === 'paused') l = 'Paused. ' + act + ' to resume';
      else if (this.state === 'over') {
        var s = Math.floor(this.score);
        l = 'Blocked by ' + this.hitBy.toLowerCase() + ' at ' + s + (this.newBest ? '. New best!' : '.') + ' ' + act + ' to retry';
      }
      this.$l.textContent = l;
      this.$r.textContent = r;
      if (this.state === 'over' && this.score >= 1000) {
        var a = document.createElement('a');
        a.href = this.getAttribute('contact-href') || '#contact';
        a.textContent = 'You clearly ship. Let’s work together →';
        this.$r.textContent = ''; this.$r.appendChild(a);
      }
    }
  }

  customElements.define('dennie-run', DennieRun);
})();
