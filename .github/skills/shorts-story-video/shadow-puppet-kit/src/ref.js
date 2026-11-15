  // ---------- Shadow Puppet Theatre (reference helpers, unchanged) ----------
  // Black cut-out puppets with punched cut-work, pinned joints and rods, pressed against a backlit cloth screen.
  // Pipeline per frame: lamp light on the cloth -> coloured gels (multiply) -> silhouettes (each puppet is drawn on
  // its own scratch layer, holes punched with destination-out, then laid on the shadow layer, blurred if it is held
  // away from the screen) -> cloth weave, light diffusion, grain.
  const INK = 'rgb(20,8,4)';
  const FF = '"IM Fell English"';
  const NF = '"Libre Baskerville"'; // lining figures for the counters
  const TAU = Math.PI * 2;
  const NZ = H.makeNoise(4242);
  const sm = H.smooth, cl = H.clamp, lerp = H.lerp, EO = H.ease.out, EIO = H.ease.inOut;
  const LAY = {};
  function lay(name, w, h) {
    let c = LAY[name];
    if (!c) c = LAY[name] = H.layer(w, h);
    const x = c.getContext('2d');
    x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1; x.filter = 'none';
    x.clearRect(0, 0, c.width, c.height);
    return c;
  }

  // ---------- small drawing helpers ----------
  function cut(p, fn) { p.save(); p.globalCompositeOperation = 'destination-out'; p.fillStyle = '#000'; p.strokeStyle = '#000'; fn(); p.restore(); }
  function dot(c, x, y, r) { c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); }
  // teardrop: round end at (x,y), point at distance len along angle a
  function tear(c, x, y, len, w, a) {
    c.save(); c.translate(x, y); c.rotate(a);
    c.beginPath(); c.moveTo(0, -w / 2); c.quadraticCurveTo(len * 0.55, -w * 0.45, len, 0); c.quadraticCurveTo(len * 0.55, w * 0.45, 0, w / 2);
    c.arc(0, 0, w / 2, Math.PI / 2, Math.PI * 1.5); c.fill(); c.restore();
  }
  // a pivot pin: a punched ring around a rivet head
  function pin(p, x, y, r) { r = r || 8; cut(p, () => dot(p, x, y, r)); p.fillStyle = INK; dot(p, x, y, r * 0.55); }
  const both = (cs, fn) => cs.forEach(fn);
  const wpt = (p, x, y) => { const q = p.getTransform().transformPoint(new DOMPoint(x, y)); return [q.x, q.y]; };
  // a cubic bezier point / tangent
  const bz = (P, u) => { const v = 1 - u; return [v * v * v * P[0][0] + 3 * v * v * u * P[1][0] + 3 * v * u * u * P[2][0] + u * u * u * P[3][0], v * v * v * P[0][1] + 3 * v * v * u * P[1][1] + 3 * v * u * u * P[2][1] + u * u * u * P[3][1]]; };
  const bzA = (P, u) => { const a = bz(P, Math.max(0, u - 0.01)), b = bz(P, Math.min(1, u + 0.01)); return Math.atan2(b[1] - a[1], b[0] - a[0]); };
  const swing = (t, t0, amp, k, w) => (t > t0 ? amp * Math.exp(-(t - t0) * k) * Math.sin((t - t0) * w) : 0);
  const blinkAt = (t, list) => list.reduce((m, b) => Math.max(m, 1 - Math.abs((t - b) / 0.08)), 0);

  // ---------- frame lifecycle ----------
  function begin(W, Hh) { return { W, Hh, S: lay('S', W, Hh), G: lay('G', W, Hh), rods: [] }; }
  // draw one puppet: fn(p, g, rods) on a fresh scratch layer, then lay it on the shadow layer
  function pup(st, o, fn) {
    const P = lay('P', st.W, st.Hh), p = P.getContext('2d'), g = st.G.getContext('2d');
    p.fillStyle = INK; p.strokeStyle = INK;
    g.save(); fn(p, g, st.rods); g.restore();
    const s = st.S.getContext('2d');
    s.save(); s.globalAlpha = o.alpha == null ? 1 : o.alpha; if (o.blur) s.filter = `blur(${o.blur}px)`; s.drawImage(P, 0, 0); s.restore();
  }
  const STOPS = [[0, [255, 232, 168]], [0.16, [255, 200, 104]], [0.42, [238, 132, 46]], [0.68, [168, 60, 20]], [0.88, [84, 24, 9]], [1, [38, 10, 4]]];
  function lamp(ctx, W, Hh, t, b, flare) {
    const f = 1 + 0.045 * NZ.n2(t * 6.1, 0.3) + 0.025 * NZ.n2(t * 17.3, 2.2);
    const B = Math.max(0, b * f);
    const cx = 640 + NZ.n2(t * 0.9, 5) * 12, cy = 320 + NZ.n2(7, t * 0.8) * 9;
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, W, Hh);
    const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, 860 + (flare || 0) * 200);
    STOPS.forEach(([o, c]) => g.addColorStop(o, H.rgba(c.map((v) => Math.min(255, v * B + (255 - v) * (flare || 0) * 0.7)), 1)));
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, Hh);
  }
  function weave(W, Hh) {
    if (LAY._weave) return LAY._weave;
    const c = H.layer(W, Hh), x = c.getContext('2d'), img = x.createImageData(W, Hh), d = img.data, r = H.rng(77);
    const row = Float32Array.from({ length: Hh }, () => 0.6 + r() * 0.8), col = Float32Array.from({ length: W }, () => 0.6 + r() * 0.8);
    for (let y = 0; y < Hh; y++) for (let X = 0; X < W; X++) {
      const i = (y * W + X) * 4;
      const th = (y % 3 === 0 ? 1 : y % 3 === 1 ? 0.35 : 0) * row[y] * (0.7 + 0.3 * Math.sin(X * 0.05 + row[y] * 9));
      const tv = (X % 3 === 0 ? 1 : X % 3 === 1 ? 0.3 : 0) * col[X] * (0.7 + 0.3 * Math.sin(y * 0.043 + col[X] * 7));
      const v = 255 * (1 - 0.075 * th - 0.06 * tv);
      d[i] = v; d[i + 1] = v * 0.985; d[i + 2] = v * 0.97; d[i + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    // soft folds and slubs of the cloth (low-res, scaled up)
    const f = H.layer(160, 90), fx = f.getContext('2d'), fi = fx.createImageData(160, 90);
    for (let y = 0; y < 90; y++) for (let X = 0; X < 160; X++) {
      const v = 255 * (1 - 0.07 * (0.5 + 0.5 * NZ.fbm2(X * 0.05, y * 0.012, 3)) - 0.03 * (0.5 + 0.5 * NZ.n2(X * 0.4, y * 0.2)));
      const i = (y * 160 + X) * 4; fi.data[i] = fi.data[i + 1] = fi.data[i + 2] = v; fi.data[i + 3] = 255;
    }
    fx.putImageData(fi, 0, 0);
    x.globalCompositeOperation = 'multiply'; x.imageSmoothingEnabled = true; x.drawImage(f, 0, 0, W, Hh);
    // a vertical seam in the cloth
    x.globalCompositeOperation = 'multiply'; x.fillStyle = 'rgba(200,190,180,1)'; x.fillRect(214, 0, 2, Hh); x.fillStyle = 'rgba(232,226,220,1)'; x.fillRect(211, 0, 7, Hh);
    LAY._weave = c; return c;
  }
  function grainTile(k) {
    const key = '_grain' + k;
    if (LAY[key]) return LAY[key];
    const c = H.layer(256, 256), x = c.getContext('2d'), img = x.createImageData(256, 256), r = H.rng(900 + k);
    for (let i = 0; i < img.data.length; i += 4) { const w = r() < 0.5 ? 0 : 255; img.data[i] = img.data[i + 1] = img.data[i + 2] = w; img.data[i + 3] = r() * 26; }
    x.putImageData(img, 0, 0); LAY[key] = c; return c;
  }
  function end(ctx, st, t) {
    const { W, Hh } = st;
    // rods: thin sticks running down out of frame to the puppeteers, a little off the screen so a little soft
    if (st.rods.length) {
      const R = lay('R', W, Hh), r = R.getContext('2d');
      r.strokeStyle = INK; r.lineCap = 'round';
      st.rods.forEach(([x, y, w, a]) => { r.globalAlpha = a == null ? 1 : a; r.lineWidth = w || 3.2; r.beginPath(); r.moveTo(x, y); r.lineTo(x + (x - 640) * 0.14 + 18, Hh + 40); r.stroke(); dot(r, x, y, (w || 3.2) * 1.2); });
      r.globalAlpha = 1;
      const s = st.S.getContext('2d'); s.save(); s.filter = 'blur(1.3px)'; s.globalAlpha = 0.9; s.drawImage(R, 0, 0); s.restore();
    }
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(st.G, 0, 0); ctx.restore();
    ctx.save(); ctx.filter = 'blur(0.7px)'; ctx.globalAlpha = 0.97; ctx.drawImage(st.S, 0, 0); ctx.restore();
    // the cloth
    ctx.save(); ctx.globalCompositeOperation = 'multiply'; ctx.drawImage(weave(W, Hh), 0, 0); ctx.restore();
    // light diffusing through the cloth: glow bleeding into the shadows and around the punched holes
    const hl = lay('half', W / 4, Hh / 4), hx = hl.getContext('2d');
    hx.filter = 'blur(5px)'; hx.drawImage(ctx.canvas, 0, 0, W / 4, Hh / 4);
    ctx.save(); ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = 0.13; ctx.drawImage(hl, 0, 0, W, Hh); ctx.restore();
    // grain, shifted at 12 fps
    const fr = Math.floor(t * 12), gt = grainTile(fr % 3), gr = H.rng(fr + 5);
    ctx.save(); ctx.fillStyle = ctx.createPattern(gt, 'repeat'); ctx.translate(-gr() * 256, -gr() * 256); ctx.fillRect(0, 0, W + 256, Hh + 256); ctx.restore();
    H.vignette(ctx, W, Hh, 0.38, '20,5,2');
  }

  // ---------- stage furniture (cached) ----------
  function valance(W) {
    if (LAY._val) return LAY._val;
    const c = H.layer(W, 80), p = c.getContext('2d');
    p.fillStyle = INK; p.fillRect(0, 0, W, 14);
    for (let x = -16; x < W + 32; x += 32) { p.beginPath(); p.arc(x + 16, 13, 16, 0, Math.PI); p.fill(); }
    for (let x = 32; x < W; x += 64) { p.fillRect(x - 1, 20, 2, 22); tear(p, x, 40, 18, 9, Math.PI / 2); dot(p, x, 40, 5); }
    cut(p, () => { for (let x = 8; x < W; x += 12) dot(p, x, 6, 1.8); for (let x = -16; x < W + 32; x += 32) { dot(p, x + 16, 20, 3.2); tear(p, x + 10, 17, 7, 3.4, 2.4); tear(p, x + 22, 17, 7, 3.4, 0.74); } });
    LAY._val = c; return c;
  }
  function ground(W) {
    if (LAY._gnd) return LAY._gnd;
    const c = H.layer(W, 110), p = c.getContext('2d'), r = H.rng(31);
    p.fillStyle = INK; p.strokeStyle = INK; p.fillRect(0, 96, W, 14);
    // filigree grass: thin curved blades
    for (let x = -10; x < W + 10; x += 5 + r() * 6) {
      const h = 14 + r() * 34 * (0.6 + 0.4 * Math.sin(x * 0.013) ** 2), lean = (r() - 0.5) * 22, w = 2 + r() * 2.5;
      p.beginPath(); p.moveTo(x - w, 100); p.quadraticCurveTo(x + lean * 0.3, 100 - h * 0.6, x + lean, 100 - h); p.quadraticCurveTo(x + lean * 0.3 + w * 0.6, 100 - h * 0.55, x + w, 100); p.fill();
    }
    // curls, ferns, little flowers
    p.lineCap = 'round';
    for (let x = 60; x < W; x += 150 + r() * 90) {
      const dir = r() < 0.5 ? -1 : 1, h = 40 + r() * 26;
      p.lineWidth = 3; p.beginPath(); p.moveTo(x, 100); p.quadraticCurveTo(x + dir * 6, 100 - h * 0.6, x + dir * 2, 100 - h);
      for (let a = 0; a < 5.5; a += 0.3) { const rr = 10 * (1 - a / 6.2); p.lineTo(x + dir * (2 + 10 - Math.cos(a) * rr), 100 - h - Math.sin(a) * rr * dir * dir); }
      p.stroke();
      for (let k = 1; k < 4; k++) tear(p, x + dir * 3, 100 - h * k / 4.2, 14, 6, dir > 0 ? -0.5 : Math.PI + 0.5);
    }
    for (let x = 140; x < W; x += 260 + r() * 120) {
      const h = 50 + r() * 20; p.lineWidth = 2; p.beginPath(); p.moveTo(x, 100); p.quadraticCurveTo(x + 8, 100 - h / 2, x + 3, 100 - h); p.stroke();
      for (let k = 0; k < 6; k++) tear(p, x + 3, 100 - h, 11, 6, k * TAU / 6);
      cut(p, () => dot(p, x + 3, 100 - h, 2.4));
    }
    LAY._gnd = c; return c;
  }
  // a fern frond cut from hide (local coords: base at 0,0, growing up)
  function fernShape(p) {
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 10; p.lineCap = 'round';
    p.beginPath(); p.moveTo(0, 0); p.quadraticCurveTo(40, -200, 10, -360); p.stroke();
    for (let k = 1; k < 13; k++) { const q = k / 13, y = -q * 340, x = 40 * Math.sin(q * 2.4) - 4; tear(p, x, y, 110 * (1 - q * 0.6), 34 * (1 - q * 0.5), 0.2 - q * 0.3); tear(p, x, y, 90 * (1 - q * 0.6), 30 * (1 - q * 0.5), Math.PI - 0.4 + q * 0.2); }
  }
  // explainer depth cue: the same fern held right up by the lamp, so its shadow is huge and very soft.
  // The blurred sprite is cached once; per frame it is only rotated (sway) and laid on the shadow layer.
  const FERN_OX = 170, FERN_OY = 440;
  function nearFern(st, t, side, a) {
    if (!LAY._fern) {
      const c = H.layer(380, 520), x = c.getContext('2d');
      const raw = H.layer(380, 520), rx = raw.getContext('2d'); rx.translate(FERN_OX, FERN_OY); fernShape(rx);
      x.filter = 'blur(7px)'; x.drawImage(raw, 0, 0); LAY._fern = c;
    }
    const s = st.S.getContext('2d');
    s.save(); s.globalAlpha = a;
    if (side > 0) { s.translate(st.W, 0); s.scale(-1, 1); }
    s.translate(-30, 770); s.rotate(0.5 + Math.sin(t * 0.8) * 0.03); s.scale(1.08, 1.08);
    s.drawImage(LAY._fern, -FERN_OX, -FERN_OY);
    s.restore();
  }
  function stage(st, t) {
    const s = st.S.getContext('2d');
    s.drawImage(valance(st.W), 0, 0);
    s.drawImage(ground(st.W), 0, st.Hh - 110);
  }

  // a hanging tag with cut-out letters. o: x,y (hang pin) rot flip w h text size badge('x'|'v') badgeS
  function tag(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); });
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 2;
    p.beginPath(); p.moveTo(0, 0); p.lineTo(0, 30); p.stroke(); dot(p, 0, 0, 4);
    both([p, g], (c) => { c.translate(0, 30 + o.h / 2); c.scale(o.flip == null ? 1 : o.flip, 1); });
    const w = o.w, h = o.h;
    p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, 12); p.fill();
    for (let x = -w / 2 + 10; x <= w / 2 - 10; x += 14) { dot(p, x, -h / 2, 4.5); dot(p, x, h / 2, 4.5); }
    cut(p, () => {
      p.lineWidth = 2.4; p.beginPath(); p.roundRect(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 7); p.stroke();
      p.font = `italic 400 ${o.size}px ${FF}`; p.textAlign = 'center'; p.textBaseline = 'middle'; p.fillText(o.text, o.tx || 0, 3);
    });
    if (o.badge && o.badgeS > 0.01) badge(p, g, { x: w / 2 - 38, y: 0, s: o.badgeS, ok: o.badge === 'v' });
    both([p, g], (c) => c.restore());
  }
  function badge(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.scale(o.s, o.s); });
    p.fillStyle = INK; dot(p, 0, 0, 40);
    for (let k = 0; k < 12; k++) dot(p, Math.cos(k * TAU / 12) * 40, Math.sin(k * TAU / 12) * 40, 7);
    cut(p, () => dot(p, 0, 0, 31));
    g.fillStyle = o.ok ? 'rgb(110,220,120)' : 'rgb(240,60,46)'; dot(g, 0, 0, 33);
    p.strokeStyle = INK; p.lineCap = 'round'; p.lineWidth = 11; p.beginPath();
    if (o.ok) { p.moveTo(-16, 1); p.lineTo(-4, 14); p.lineTo(18, -14); } else { p.moveTo(-14, -14); p.lineTo(14, 14); p.moveTo(14, -14); p.lineTo(-14, 14); }
    p.stroke();
    both([p, g], (c) => c.restore());
  }
  // small label plaque with cut letters, hung on a string of length `hang` (0 = sits)
  function plaque(p, o) {
    p.save(); p.translate(o.x, o.y); p.rotate(o.rot || 0);
    p.font = `italic 400 ${o.size}px ${FF}`;
    const tw = p.measureText(o.text).width, w = tw + o.size * 1.1, h = o.size * 1.5;
    p.fillStyle = INK; p.strokeStyle = INK;
    if (o.hang) { p.lineWidth = 2; p.beginPath(); p.moveTo(0, -h / 2); p.lineTo(0, -h / 2 - o.hang); p.stroke(); }
    p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, h * 0.28); p.fill();
    dot(p, -w / 2 - 4, 0, h * 0.24); dot(p, w / 2 + 4, 0, h * 0.24);
    cut(p, () => {
      p.lineWidth = 2; p.beginPath(); p.roundRect(-w / 2 + 6, -h / 2 + 6, w - 12, h - 12, h * 0.2); p.stroke();
      dot(p, -w / 2 - 4, 0, h * 0.09); dot(p, w / 2 + 4, 0, h * 0.09);
      p.textAlign = 'center'; p.textBaseline = 'middle'; p.fillText(o.text, 0, 2);
    });
    p.restore();
  }
  // a growing vine-arrow (cut from one strip of hide): P = cubic bezier, prog 0..1
  function vine(p, P, prog, w) {
    if (prog <= 0.001) return;
    w = w || 7; p.fillStyle = INK; p.strokeStyle = INK; p.lineCap = 'round'; p.lineJoin = 'round';
    const N = 60, n = Math.max(2, Math.ceil(N * prog));
    p.lineWidth = w; p.beginPath();
    for (let i = 0; i <= n; i++) { const q = bz(P, Math.min(prog, i / N)); if (i === 0) p.moveTo(q[0], q[1]); else p.lineTo(q[0], q[1]); }
    p.stroke();
    // start curl
    const s0 = bz(P, 0), a0 = bzA(P, 0);
    p.lineWidth = 3.5; p.beginPath();
    for (let a = 0; a < 5.2; a += 0.25) { const r = 16 * (1 - a / 6), aa = a0 + Math.PI + a; p.lineTo(s0[0] + Math.cos(a0 + Math.PI) * 4 + Math.cos(aa) * r - Math.cos(a0 + Math.PI) * 16, s0[1] + Math.sin(a0 + Math.PI) * 4 + Math.sin(aa) * r - Math.sin(a0 + Math.PI) * 16); }
    p.stroke();
    // leaves
    [0.18, 0.34, 0.5, 0.66, 0.8].forEach((u, i) => {
      if (u > prog - 0.06) return;
      const q = bz(P, u), a = bzA(P, u) + (i % 2 ? 1 : -1) * 0.9, gr = Math.min(1, (prog - u) / 0.12);
      tear(p, q[0], q[1], 26 * gr, 11 * gr, a);
      cut(p, () => { p.lineWidth = 1.4; p.beginPath(); p.moveTo(q[0] + Math.cos(a) * 5, q[1] + Math.sin(a) * 5); p.lineTo(q[0] + Math.cos(a) * 20 * gr, q[1] + Math.sin(a) * 20 * gr); p.stroke(); });
    });
    // spade arrowhead
    const e = bz(P, prog), ea = bzA(P, prog);
    p.save(); p.translate(e[0], e[1]); p.rotate(ea);
    p.beginPath(); p.moveTo(30, 0); p.quadraticCurveTo(8, -6, -4, -19); p.quadraticCurveTo(2, -6, -6, 0); p.quadraticCurveTo(2, 6, -4, 19); p.quadraticCurveTo(8, 6, 30, 0); p.fill();
    cut(p, () => dot(p, 6, 0, 3.2));
    p.restore();
  }
  // hanging intertitle card with cut-out lettering. o: x,y centre, w,h, s, rot (about the top), lines [{text,size,y,italic,arrow}]
  function titleCard(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y - o.h / 2 * o.s); c.rotate(o.rot || 0); c.scale(o.s, o.s); c.translate(0, o.h / 2); });
    const w = o.w, h = o.h;
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 2.4;
    p.beginPath(); p.moveTo(-w * 0.32, -h / 2); p.lineTo(-w * 0.32, -h / 2 - 900); p.moveTo(w * 0.32, -h / 2); p.lineTo(w * 0.32, -h / 2 - 900); p.stroke();
    p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, 14); p.fill();
    for (let x = -w / 2 + 12; x <= w / 2 - 12; x += 16) { dot(p, x, -h / 2, 6); dot(p, x, h / 2, 6); }
    for (const sx of [-1, 1]) { p.beginPath(); p.arc(sx * w / 2, 0, h * 0.22, -Math.PI / 2, Math.PI / 2, sx < 0); p.fill(); }
    cut(p, () => {
      p.lineWidth = 3; p.beginPath(); p.roundRect(-w / 2 + 14, -h / 2 + 14, w - 28, h - 28, 8); p.stroke();
      for (let x = -w / 2 + 34; x <= w / 2 - 34; x += 11) { dot(p, x, -h / 2 + 24, 1.8); dot(p, x, h / 2 - 24, 1.8); }
      for (const sx of [-1, 1]) for (const sy of [-1, 1]) {
        const cx = sx * (w / 2 - 34), cy = sy * (h / 2 - 34);
        dot(p, cx, cy, 4);
        [0, 1, 2].forEach((k) => tear(p, cx, cy, 14, 6, Math.atan2(-sy, -sx) + (k - 1) * 0.7 + Math.PI));
      }
      for (const sx of [-1, 1]) { dot(p, sx * (w / 2 + h * 0.1), 0, h * 0.07); }
      o.lines.forEach((L) => {
        p.font = `${L.italic ? 'italic ' : ''}400 ${L.size}px ${FF}`; p.textAlign = 'center'; p.textBaseline = 'alphabetic';
        if (L.arrow) {
          const tw = p.measureText(L.text).width, aw = L.size * 1.2, gap = L.size * 0.3, x0 = -(tw + aw + gap) / 2, ay = L.y - L.size * 0.3;
          p.fillText(L.text, x0 + aw + gap + tw / 2, L.y);
          p.fillRect(x0, ay - 3.5, aw - 16, 7);
          p.beginPath(); p.moveTo(x0 + aw, ay); p.lineTo(x0 + aw - 24, ay - 15); p.lineTo(x0 + aw - 24, ay + 15); p.closePath(); p.fill();
          dot(p, x0, ay, 7);
        } else p.fillText(L.text, 0, L.y);
      });
    });
    both([p, g], (c) => c.restore());
  }
  function star(p, x, y, r) { p.beginPath(); for (let i = 0; i < 10; i++) { const rr = i % 2 ? r * 0.42 : r, a = i * TAU / 10 - Math.PI / 2; p.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr); } p.fill(); }
  function curtains(p, W, Hh, cover, t) {
    const e = cover * (W / 2 + 40);
    for (const sd of [-1, 1]) {
      const wave = (y) => Math.sin(y * 0.018 + t * 2 + sd) * 10 + Math.sin(y * 0.05) * 4;
      const inner = (y) => (sd < 0 ? e - 40 + wave(y) : W - e + 40 + wave(y));
      const outer = sd < 0 ? -60 : W + 60;
      p.fillStyle = INK; p.beginPath(); p.moveTo(outer, -10);
      for (let y = -10; y <= Hh + 10; y += 20) p.lineTo(inner(y), y);
      p.lineTo(outer, Hh + 10); p.closePath(); p.fill();
      for (let y = 30; y < Hh; y += 24) { tear(p, inner(y), y, 18, 9, sd < 0 ? 0 : Math.PI); }
      cut(p, () => {
        for (let k = 1; k < 9; k++) {
          const x = sd < 0 ? inner(0) - k * 70 : inner(0) + k * 70;
          for (let y = 50; y < Hh - 20; y += 22) { const xx = x + wave(y) * 0.6 + Math.sin(y * 0.03 + k) * 6; p.save(); p.translate(xx, y); p.rotate(Math.PI / 4); p.fillRect(-3.4, -3.4, 6.8, 6.8); p.restore(); }
        }
        for (let y = 40; y < Hh - 20; y += 18) dot(p, inner(y) - sd * 18, y, 3);
      });
    }
  }
