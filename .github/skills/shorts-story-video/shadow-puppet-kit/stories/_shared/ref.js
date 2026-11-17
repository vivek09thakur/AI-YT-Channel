  
  const FF = '"IM Fell English"';
  const TAU = Math.PI * 2;
  const NZ = H.makeNoise(108);
  const sm = H.smooth, cl = H.clamp, lerp = H.lerp, EO = H.ease.out, EIO = H.ease.inOut;
  const LAY = {};
  function lay(name, w, h) {
    let c = LAY[name];
    if (!c || c.width !== w || c.height !== h) c = LAY[name] = H.layer(w, h);
    const x = c.getContext('2d');
    x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over'; x.globalAlpha = 1; x.filter = 'none';
    x.clearRect(0, 0, c.width, c.height);
    return c;
  }
  
  const PAL = {
    saffron: '#f08a24', kesari: '#ff7f11', turmeric: '#f6c445', marigold: '#ffa726', amber: '#f7a234',
    kumkum: '#c8102e', vermilion: '#e03e1e', maroon: '#6a1020', burnt: '#b4471a',
    rama: '#2e8fa3', krishna: '#1f6a8c', peacock: '#17857a', indigo: '#1d1b4b', night: '#120c2e',
    gold: '#e9b949', brass: '#c9942b', sandal: '#f5e0b8', cream: '#fff3d6', lotus: '#e87c93', tulsi: '#3f7a3a',
    brown: '#5e2a10', deep: '#2f1207', ink: '#241006', ash: '#efe7da', smoke: '#4a3a3a',
  };
  const mixc = (a, b, u) => H.rgba(H.mix(a, b, cl(u)));

  function sky(c, W, Hh, stops) {
    const g = c.createLinearGradient(0, 0, 0, Hh);
    stops.forEach(([o, col]) => g.addColorStop(o, col));
    c.fillStyle = g; c.fillRect(0, 0, W, Hh);
  }
  
  function streaks(c, W, Hh, t, o) {
    o = o || {};
    const r = H.rng(o.seed || 5), n = o.n || 90, col = o.color || PAL.cream, ymax = o.ymax == null ? Hh : o.ymax;
    c.save(); c.strokeStyle = col; c.lineCap = 'butt';
    for (let i = 0; i < n; i++) {
      const y = r() * ymax, len = 60 + r() * 420, sp = 4 + r() * 10, x0 = ((r() * (W + len) + t * sp) % (W + len)) - len;
      c.globalAlpha = (o.alpha || 0.22) * (0.5 + r() * 0.5); c.lineWidth = 1 + r() * 1.6;
      c.beginPath(); c.moveTo(x0, y); c.lineTo(x0 + len, y); c.stroke();
    }
    c.restore();
  }
  
  function sun(c, x, y, r, col, halo) {
    c.save();
    const g = c.createRadialGradient(x, y, r * 0.8, x, y, r * (halo || 3));
    g.addColorStop(0, H.rgba(col, 0.55)); g.addColorStop(1, H.rgba(col, 0));
    c.fillStyle = g; c.fillRect(x - r * 4, y - r * 4, r * 8, r * 8);
    c.fillStyle = col; c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    c.restore();
  }
  
  function cloud(c, x, y, w, h, fill, line, seed) {
    const r = H.rng(seed || 1), n = Math.max(3, Math.round(w / (h * 0.9))), bw = w / n;
    c.save(); c.beginPath(); c.moveTo(x, y);
    for (let i = 0; i < n; i++) {
      const edge = i === 0 || i === n - 1;
      const bx = x + bw * (i + 0.5), br = bw * 0.6 * (edge ? 0.8 : 0.9 + r() * 0.5), by = y - h * (edge ? 0.3 : 0.4 + r() * 0.45);
      c.arc(bx, by, br, Math.PI, 0, false);
    }
    c.lineTo(x + w, y); c.closePath();
    c.fillStyle = fill; c.fill();
    if (line) {
      c.clip(); c.strokeStyle = line; c.lineWidth = 2.2;
      for (let yy = y - h * 1.6; yy < y; yy += 6 + r() * 6) {
        const x0 = x - 20 + r() * w * 0.55, x1 = x0 + w * (0.25 + r() * 0.7);
        c.beginPath(); c.moveTo(x0, yy); c.lineTo(x1, yy); c.stroke();
      }
    }
    c.restore();
  }
  
  function cloudBank(c, W, y, t, o) {
    const r = H.rng(o.seed || 9), n = o.n || 5, span = W + 700;
    for (let i = 0; i < n; i++) {
      const w = 180 + r() * 320, h = 40 + r() * 50, base = r() * span, yy = y + (r() - 0.5) * (o.spread || 80);
      const x = ((base + t * (o.speed || 6) * (0.6 + r() * 0.8)) % span) - 350;
      cloud(c, x, yy, w, h, o.fill, o.line, 100 + i + (o.seed || 0));
    }
  }
  
  function hills(c, W, Hh, y, amp, col, seed, drift) {
    c.save(); c.fillStyle = col; c.beginPath(); c.moveTo(-10, Hh + 10); c.lineTo(-10, y);
    for (let x = -10; x <= W + 10; x += 12) c.lineTo(x, y - amp * (0.5 + 0.5 * NZ.fbm2((x + (drift || 0)) * 0.0022 + seed * 7, seed, 3)) - amp * 0.3 * Math.sin((x + (drift || 0)) * 0.004 + seed));
    c.lineTo(W + 10, Hh + 10); c.closePath(); c.fill(); c.restore();
  }
  
  function ocean(c, W, Hh, y, t, cols) {
    c.save();
    for (let k = 0; k < cols.length; k++) {
      const yy = y + k * ((Hh - y) / cols.length);
      c.fillStyle = cols[k]; c.beginPath(); c.moveTo(-10, Hh + 10); c.lineTo(-10, yy);
      for (let x = -10; x <= W + 10; x += 10) c.lineTo(x, yy + Math.sin(x * 0.03 + t * (1.2 + k * 0.3) + k) * (4 + k * 2) + Math.sin(x * 0.011 - t * 0.7) * 3);
      c.lineTo(W + 10, Hh + 10); c.closePath(); c.fill();
    }
    c.restore();
  }
  
  function tree(c, x, y, s, col, o) {
    o = o || {};
    c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col; c.strokeStyle = col;
    if (o.palm) {
      c.lineWidth = 7; c.lineCap = 'round'; c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(10, -90, 4, -170); c.stroke();
      for (let k = 0; k < 7; k++) { const a = -Math.PI * 0.95 + k * (Math.PI * 0.9 / 6); c.beginPath(); c.moveTo(4, -170); c.quadraticCurveTo(4 + Math.cos(a) * 60, -170 + Math.sin(a) * 60 - 20, 4 + Math.cos(a) * 95, -170 + Math.sin(a) * 95 + 30); c.quadraticCurveTo(4 + Math.cos(a) * 55, -170 + Math.sin(a) * 50 + 8, 4, -164); c.fill(); }
    } else {
      c.fillRect(-7, -70, 14, 72);
      [[0, -120, 46], [-34, -92, 34], [34, -94, 36], [0, -78, 30]].forEach(([dx, dy, r]) => { c.beginPath(); c.arc(dx, dy, r, 0, TAU); c.fill(); });
    }
    c.restore();
  }
  
  function flag(c, x, y, h, col, t, dir) {
    c.save(); c.strokeStyle = PAL.deep; c.lineWidth = 3; c.beginPath(); c.moveTo(x, y); c.lineTo(x, y - h); c.stroke();
    c.fillStyle = PAL.deep; c.beginPath(); c.arc(x, y - h, 4, 0, TAU); c.fill();
    const d = dir || 1, w = h * 0.55, fh = h * 0.22, wv = Math.sin(t * 5 + x) * 5;
    c.fillStyle = col; c.beginPath(); c.moveTo(x, y - h + 4); c.quadraticCurveTo(x + d * w * 0.5, y - h + 4 + wv, x + d * w, y - h + fh * 0.5 + wv * 1.4); c.lineTo(x, y - h + fh + 4); c.closePath(); c.fill();
    c.restore();
  }
  
  function finial(c, x, y, s, col, t) {
    c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col; c.strokeStyle = col;
    c.beginPath(); c.arc(0, -18, 14, 0, TAU); c.fill();
    c.lineWidth = 4; c.beginPath(); c.moveTo(0, -32); c.lineTo(0, -120); c.stroke();
    c.beginPath(); c.arc(0, -58, 9, 0, TAU); c.fill();
    const wv = Math.sin(t * 4) * 4;
    c.beginPath(); c.moveTo(0, -120); c.quadraticCurveTo(30, -126 + wv, 62, -108 + wv); c.quadraticCurveTo(34, -104 + wv * 0.6, 0, -84); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(0, -130); c.lineTo(0, -144); c.stroke();
    c.restore();
  }
  
  function temple(c, o, t) {
    const x = o.x, y = o.y, s = o.s || 1, col = o.col || PAL.brown, lite = o.lite || mixc(col, PAL.cream, 0.18);
    c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col;
    c.fillRect(-330, 0, 660, 26); c.fillRect(-300, 26, 600, 22); c.fillRect(-260, 48, 520, 18);
    [-250, -95, 95, 250].forEach((px) => {
      c.fillRect(px - 12, -210, 24, 212);
      c.beginPath(); c.moveTo(px - 26, -210); c.lineTo(px + 26, -210); c.lineTo(px + 16, -236); c.lineTo(px - 16, -236); c.closePath(); c.fill();
      c.fillRect(px - 20, -16, 40, 16);
    });
    c.beginPath(); c.moveTo(-430, -236); c.lineTo(430, -236); c.lineTo(400, -262); c.lineTo(-400, -262); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-400, -262); c.lineTo(400, -262); c.lineTo(250, -330); c.lineTo(-250, -330); c.closePath(); c.fill();
    c.fillRect(-440, -250, 880, 10);
    c.fillRect(-190, -352, 380, 24); c.fillRect(-150, -374, 300, 24);
    c.fillRect(-120, -416, 240, 44);
    c.fillStyle = lite; for (let k = -100; k <= 100; k += 25) { c.beginPath(); c.arc(k, -384, 9, Math.PI, 0); c.fill(); }
    c.fillStyle = col;
    c.beginPath(); c.moveTo(-118, -416); c.bezierCurveTo(-140, -470, -110, -530, -40, -560); c.quadraticCurveTo(-8, -576, 0, -600); c.quadraticCurveTo(8, -576, 40, -560); c.bezierCurveTo(110, -530, 140, -470, 118, -416); c.closePath(); c.fill();
    c.fillStyle = lite; c.fillRect(-118, -424, 236, 5); c.fillStyle = col;
    finial(c, 0, -596, 1, col, t || 0);
    c.restore();
  }
  
  function skyline(c, x, y, s, col, t) {
    c.save(); c.translate(x, y); c.scale(s, s); c.fillStyle = col;
    const dome = (dx, w, h) => { c.beginPath(); c.moveTo(dx - w / 2, 0); c.lineTo(dx - w / 2, -h * 0.4); c.bezierCurveTo(dx - w / 2 - w * 0.1, -h * 0.75, dx - w * 0.25, -h * 0.95, dx, -h); c.bezierCurveTo(dx + w * 0.25, -h * 0.95, dx + w / 2 + w * 0.1, -h * 0.75, dx + w / 2, -h * 0.4); c.lineTo(dx + w / 2, 0); c.closePath(); c.fill(); c.fillRect(dx - 2, -h - 22, 4, 22); };
    const spire = (dx, w, h) => { c.beginPath(); c.moveTo(dx - w / 2, 0); c.lineTo(dx - w * 0.25, -h * 0.7); c.lineTo(dx, -h); c.lineTo(dx + w * 0.25, -h * 0.7); c.lineTo(dx + w / 2, 0); c.closePath(); c.fill(); };
    c.fillRect(-520, -30, 1040, 40);
    for (let k = -480; k <= 480; k += 60) c.fillRect(k - 6, -46, 12, 18);
    [[-420, 90, 140], [-200, 150, 220], [0, 220, 320], [210, 140, 200], [430, 100, 150]].forEach(([dx, w, h]) => dome(dx, w, h));
    [[-320, 50, 170], [-100, 40, 200], [110, 44, 210], [330, 50, 160]].forEach(([dx, w, h]) => spire(dx, w, h));
    [-470, -300, 320, 470].forEach((fx, i) => flag(c, fx, -30, 60 + (i % 2) * 20, PAL.saffron, t || 0, i < 2 ? 1 : -1));
    c.restore();
  }
  
  function lotus(c, x, y, s, col, col2) {
    c.save(); c.translate(x, y); c.scale(s, s);
    for (const [n, r, cc] of [[9, 1, col], [7, 0.72, col2 || col]]) {
      c.fillStyle = cc;
      for (let k = 0; k < n; k++) { const a = (k - (n - 1) / 2) * (Math.PI * 0.95 / (n - 1)); c.save(); c.rotate(a); c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(12 * r, -26 * r, 0, -56 * r); c.quadraticCurveTo(-12 * r, -26 * r, 0, 0); c.fill(); c.restore(); }
    }
    c.restore();
  }
  
  function rays(c, x, y, r0, r1, n, col, t, alpha) {
    c.save(); c.translate(x, y); c.rotate((t || 0) * 0.05); c.globalAlpha = alpha == null ? 0.35 : alpha; c.fillStyle = col;
    for (let k = 0; k < n; k++) { const a = k * TAU / n, w = TAU / n * 0.42; c.beginPath(); c.moveTo(Math.cos(a - w) * r0, Math.sin(a - w) * r0); c.lineTo(Math.cos(a - w * 0.7) * r1, Math.sin(a - w * 0.7) * r1); c.lineTo(Math.cos(a + w * 0.7) * r1, Math.sin(a + w * 0.7) * r1); c.lineTo(Math.cos(a + w) * r0, Math.sin(a + w) * r0); c.closePath(); c.fill(); }
    c.restore();
  }
  
  function flames(c, x, y, s, t, seed, n) {
    const r = H.rng(seed || 3); n = n || 7;
    c.save(); c.translate(x, y); c.scale(s, s);
    for (let k = 0; k < n; k++) {
      const bx = (r() - 0.5) * 120, h = 60 + r() * 90, w = 22 + r() * 22, ph = r() * TAU, sp = 3 + r() * 3;
      const hh = h * (0.8 + 0.2 * Math.sin(t * sp + ph)), lean = Math.sin(t * sp * 0.6 + ph) * 12;
      for (const [f, col] of [[1, PAL.vermilion], [0.68, PAL.marigold], [0.36, PAL.turmeric]]) {
        c.fillStyle = col; c.beginPath(); c.moveTo(bx - w * f, 0); c.quadraticCurveTo(bx - w * f * 0.4 + lean * f, -hh * f * 0.5, bx + lean * f * 1.6, -hh * f); c.quadraticCurveTo(bx + w * f * 0.4 + lean * f, -hh * f * 0.5, bx + w * f, 0); c.closePath(); c.fill();
      }
    }
    c.restore();
  }
  
  function bolt(c, x, y, len, seed, col) {
    const r = H.rng(seed); c.save(); c.strokeStyle = col || PAL.cream; c.lineWidth = 4; c.lineJoin = 'miter'; c.beginPath(); c.moveTo(x, y);
    let yy = y, xx = x; while (yy < y + len) { yy += 30 + r() * 40; xx += (r() - 0.5) * 70; c.lineTo(xx, yy); }
    c.stroke(); c.lineWidth = 12; c.globalAlpha = 0.25; c.stroke(); c.restore();
  }

  const FK = 0.66;
  function figure(c, o) {
    const d = o.dir == null ? 1 : o.dir, skin = o.skin || PAL.rama, cloth = o.cloth || PAL.turmeric, sash = o.sash || PAL.kumkum;
    const gold = o.gold || PAL.gold, hair = o.hair || PAL.ink, pose = o.pose || 'stand', ph = o.ph || 0, s = o.s || 1;
    const sw = pose === 'walk' ? Math.sin(ph * TAU) : 0, lift = pose === 'walk' ? Math.abs(Math.cos(ph * TAU)) * 5 : 0;
    const skinS = mixc(skin, PAL.ink, 0.28), clothS = mixc(cloth, PAL.ink, 0.25), lite = mixc(skin, PAL.cream, 0.3);
    const poly = (pts, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); c.fill(); };
    const tri = (x, y, w, h, col) => poly([[x - w / 2, y], [x + w / 2, y], [x, y - h]], col);
    const limb = (x0, y0, x1, y1, w0, w1, col) => { const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L; poly([[x0 + nx * w0, y0 + ny * w0], [x1 + nx * w1, y1 + ny * w1], [x1 - nx * w1, y1 - ny * w1], [x0 - nx * w0, y0 - ny * w0]], col); };
    c.save(); c.translate(o.x, o.y - lift); c.scale(s * d * FK, s * FK);
    const kneel = pose === 'kneel', dy = kneel ? 76 : 0;
    const hipY = -168 + dy, waistY = -190 + dy, shY = -290 + dy, neckY = -312 + dy, hy = -352 + dy;
    if (o.glow) { const g = c.createRadialGradient(0, hy + 140, 20, 0, hy + 140, 300); g.addColorStop(0, H.rgba(o.glow, 0.5)); g.addColorStop(1, H.rgba(o.glow, 0)); c.fillStyle = g; c.fillRect(-330, hy - 200, 660, 560); }
    const monkey = o.face === 'monkey', woman = o.face === 'woman';

    if (o.tail) { c.strokeStyle = skin; c.lineWidth = 16; c.lineCap = 'round'; c.beginPath(); c.moveTo(-26, hipY + 10); c.bezierCurveTo(-110, hipY + 16, -130, hipY - 110, -70, hipY - 140); c.quadraticCurveTo(-36, hipY - 152, -46, hipY - 118); c.stroke(); }
    if (o.bow) { c.save(); c.translate(-50, shY + 10); c.rotate(-0.22); poly([[-9, -24], [9, -24], [12, 96], [-12, 96]], PAL.burnt); c.fillStyle = gold; c.fillRect(-10, -24, 20, 7); c.fillRect(-11, 60, 22, 6); for (const k of [-7, 0, 7]) { c.strokeStyle = PAL.deep; c.lineWidth = 2; c.beginPath(); c.moveTo(k, -24); c.lineTo(k * 1.5, -70); c.stroke(); tri(k * 1.5, -66, 10, 16, PAL.cream); } c.restore(); }

    const foot = (fx, fy, col) => { poly([[fx - 8, fy], [fx + 36, fy], [fx + 40, fy - 4], [fx + 10, fy - 12], [fx - 8, fy - 10]], col); c.fillStyle = gold; c.fillRect(fx - 7, fy - 20, 15, 5); };
    if (kneel) {
      limb(6, hipY + 16, -34, -10, 16, 10, skinS); limb(-34, -10, 40, -4, 10, 8, skinS); foot(40, 0, skinS);
      limb(-6, hipY + 16, 44, hipY + 60, 16, 11, skin); limb(44, hipY + 60, 46, -2, 11, 8, skin); foot(46, 0, skin);
    } else {
      for (const [a, back] of [[-sw * 0.55, 1], [sw * 0.55, 0]]) {
        const col = back ? skinS : skin, kx = Math.sin(a) * 70, ky = hipY + 20 + Math.cos(a) * 70, bend = pose === 'walk' ? Math.max(0, -Math.sin(a)) * 0.7 : 0.03;
        const fx = kx + Math.sin(a + bend) * 76, fy = ky + Math.cos(a + bend) * 76;
        limb(back ? 8 : -8, hipY + 20, kx, ky, 16, 9, col); limb(kx, ky, fx, fy, 9, 6, col); foot(fx, fy, col);
      }
    }
    const hem = kneel ? hipY + 40 : -52;
    poly([[-32, waistY], [32, waistY], [58 + sw * 14, hem], [-62 - sw * 14, hem]], cloth);
    poly([[-10, waistY], [12, waistY], [26 + sw * 8, hem], [-14 + sw * 8, hem]], clothS);
    poly([[-32, waistY], [-20, waistY], [-42 - sw * 14, hem], [-62 - sw * 14, hem]], clothS);
    if (!monkey) poly([[-30, waistY + 4], [-16, waistY + 4], [-70 - sw * 20, hem + 12], [-96 - sw * 26, hem + 22], [-60 - sw * 16, hem - 18]], sash);
    poly([[-36, waistY - 10], [36, waistY - 10], [34, waistY + 4], [-34, waistY + 4]], gold);
    poly([[-10, waistY - 16], [10, waistY - 16], [6, waistY + 10], [-6, waistY + 10]], PAL.kumkum);
    poly([[-64, shY], [64, shY], [34, waistY], [-34, waistY]], skin);
    poly([[-64, shY], [-34, shY], [-26, waistY], [-34, waistY]], skinS);
    if (woman) poly([[-64, shY], [64, shY], [40, waistY - 36], [-40, waistY - 36]], sash);
    else if (!monkey) { poly([[-28, shY + 10], [28, shY + 10], [22, shY + 52], [-22, shY + 52]], gold); poly([[-20, shY + 18], [20, shY + 18], [15, shY + 44], [-15, shY + 44]], PAL.kumkum); poly([[-8, shY + 24], [8, shY + 24], [6, shY + 38], [-6, shY + 38]], gold); }
    if (!monkey) poly([[-58, shY + 4], [-40, shY + 4], [20, waistY - 10], [8, waistY - 10]], sash);
    c.fillStyle = PAL.ink; for (let i = 0; i <= 12; i++) { const a = 0.2 + (Math.PI - 0.4) * i / 12; c.beginPath(); c.arc(Math.cos(a) * 36, shY - 6 + Math.sin(a) * 30, 2.6, 0, TAU); c.fill(); }

    let back = [0.3 - sw * 0.6, 0.7], front = [-0.3 + sw * 0.6, 0.7], target = null;
    if (pose === 'aim') { back = [1.2, -2.8]; front = [1.55, -0.05]; }
    if (pose === 'raise') { front = [-2.6, -0.4]; back = [0.2, 0.9]; }
    if (pose === 'namaste') target = [40, shY + 60];
    if (pose === 'kneel') target = [60, shY + 90];
    if (o.arms) { front = o.arms[0]; back = o.arms[1]; target = null; }
    const L1 = 70, L2 = 64;
    const handAt = (A, sx) => { const ex = sx + Math.sin(A[0]) * L1, ey = shY + 10 + Math.cos(A[0]) * L1; return [ex, ey, ex + Math.sin(A[0] + A[1]) * L2, ey + Math.cos(A[0] + A[1]) * L2]; };
    const ik = (sx, tx, ty) => { const sy = shY + 10, dx = tx - sx, dyy = ty - sy, D = Math.min(Math.hypot(dx, dyy), L1 + L2 - 1), a = Math.acos(cl((L1 * L1 + D * D - L2 * L2) / (2 * L1 * D), -1, 1)), b = Math.atan2(dyy, dx) + a; return [sx + Math.cos(b) * L1, sy + Math.sin(b) * L1, tx, ty]; };
    const arm = (A, col, isFront) => {
      const sx = isFront ? 46 : -46, [ex, ey, hx, hy2] = target ? ik(sx, target[0], target[1]) : handAt(A, sx);
      limb(sx, shY + 10, ex, ey, 15, 10, col); limb(ex, ey, hx, hy2, 10, 6, col);
      const dl = Math.hypot(hx - ex, hy2 - ey) || 1, ux = (hx - ex) / dl, uy = (hy2 - ey) / dl;
      poly([[hx - uy * 7, hy2 + ux * 7], [hx + uy * 7, hy2 - ux * 7], [hx + ux * 26 + uy * 2, hy2 + uy * 26 - ux * 2], [hx + ux * 18 - uy * 9, hy2 + uy * 18 + ux * 9]], col);
      c.fillStyle = gold; c.save(); c.translate(lerp(sx, ex, 0.5), lerp(shY + 10, ey, 0.5)); c.rotate(Math.atan2(ey - shY - 10, ex - sx)); c.fillRect(-5, -14, 10, 28); c.restore();
      c.fillStyle = PAL.ink; c.save(); c.translate(lerp(ex, hx, 0.85), lerp(ey, hy2, 0.85)); c.rotate(Math.atan2(hy2 - ey, hx - ex)); c.fillRect(-3, -9, 6, 18); c.restore();
      return [hx, hy2];
    };
    const bh = arm(back, skinS, false);
    if (o.bow) {
      const fh = handAt(front, 46).slice(2), R = 118, dr = o.draw || 0;
      c.save(); c.translate(fh[0], fh[1]);
      c.strokeStyle = PAL.brass; c.lineWidth = 9; c.beginPath(); c.arc(-R * 0.5, 0, R, -1.2, 1.2); c.stroke();
      c.strokeStyle = PAL.kumkum; c.beginPath(); c.arc(-R * 0.5, 0, R, -0.22, 0.22); c.stroke();
      const tx = -R * 0.5 + Math.cos(1.2) * R, ty = Math.sin(1.2) * R;
      tri(tx, -ty - 6, 10, 16, PAL.brass); c.save(); c.translate(tx, ty + 6); c.scale(1, -1); tri(0, 0, 10, 16, PAL.brass); c.restore();
      const nock = [lerp(tx, bh[0] - fh[0], dr), lerp(0, bh[1] - fh[1], dr)];
      c.strokeStyle = PAL.cream; c.lineWidth = 2; c.beginPath(); c.moveTo(tx, -ty); c.lineTo(nock[0], nock[1]); c.lineTo(tx, ty); c.stroke();
      if (dr > 0.05) { const ax = nock[0] + 230 - nock[0] * 0.4, ay = nock[1] * 0.3; c.strokeStyle = PAL.deep; c.lineWidth = 3; c.beginPath(); c.moveTo(nock[0], nock[1]); c.lineTo(ax, ay); c.stroke(); c.save(); c.translate(ax, ay); c.rotate(Math.PI / 2); tri(0, 0, 12, 22, PAL.cream); c.restore(); poly([[nock[0], nock[1] - 7], [nock[0] + 22, nock[1]], [nock[0], nock[1] + 7]], PAL.kumkum); }
      c.restore();
    }
    const fh = arm(front, skin, true);
    if (o.mace) { c.save(); c.translate(fh[0], fh[1]); c.rotate(o.maceA == null ? -0.5 : o.maceA); poly([[-6, 20], [6, 20], [4, -86], [-4, -86]], PAL.brass); c.fillStyle = gold; c.beginPath(); c.arc(0, -118, 34, 0, TAU); c.fill(); c.fillStyle = PAL.brass; c.beginPath(); c.arc(0, -118, 21, 0, TAU); c.fill(); c.fillStyle = PAL.kumkum; c.beginPath(); c.arc(0, -118, 7, 0, TAU); c.fill(); c.restore(); }

    poly([[-13, neckY], [13, neckY], [17, shY + 2], [-17, shY + 2]], skin);
    poly([[-13, neckY + 1], [13, neckY + 1], [0, neckY + 10]], skinS);
    if (monkey) {
      poly([[-28, hy - 30], [16, hy - 34], [30, hy - 14], [46, hy + 2], [44, hy + 16], [26, hy + 26], [4, hy + 38], [-18, hy + 32], [-30, hy + 8]], skin);
      poly([[-28, hy - 30], [-16, hy - 30], [-18, hy + 32], [-30, hy + 8]], skinS);
      poly([[18, hy - 6], [46, hy + 2], [44, hy + 16], [26, hy + 26], [12, hy + 20]], mixc(skin, PAL.cream, 0.55));
      c.fillStyle = skin; c.beginPath(); c.arc(-22, hy - 18, 11, 0, TAU); c.fill(); c.fillStyle = mixc(skin, PAL.cream, 0.4); c.beginPath(); c.arc(-22, hy - 18, 5, 0, TAU); c.fill();
      poly([[2, hy - 14], [26, hy - 16], [26, hy - 11], [2, hy - 9]], PAL.ink);
      poly([[4, hy - 6], [24, hy - 8], [16, hy + 2]], PAL.cream); c.fillStyle = PAL.ink; c.beginPath(); c.arc(16, hy - 5, 3.4, 0, TAU); c.fill();
      c.fillStyle = PAL.ink; c.beginPath(); c.arc(44, hy + 6, 3, 0, TAU); c.fill();
      poly([[26, hy + 18], [40, hy + 16], [30, hy + 22]], PAL.kumkum);
    } else {
      poly([[-26, hy - 34], [14, hy - 36], [24, hy - 22], [27, hy - 12], [42, hy + 2], [27, hy + 8], [31, hy + 17], [23, hy + 30], [2, hy + 40], [-18, hy + 32], [-28, hy + 6]], skin);
      poly([[-26, hy - 34], [-14, hy - 34], [-16, hy + 30], [-18, hy + 32], [-28, hy + 6]], skinS);
      poly([[-28, hy - 36], [16, hy - 38], [24, hy - 22], [-4, hy - 24], [-27, hy - 18]], hair);
      poly([[-27, hy - 6], [-19, hy - 2], [-20, hy + 14], [-30, hy + 10]], skinS);
      c.fillStyle = gold; c.beginPath(); c.arc(-24, hy + 18, 5, 0, TAU); c.fill(); tri(-24, hy + 32, 8, -10, gold);
      poly([[4, hy - 16], [27, hy - 18], [27, hy - 13], [4, hy - 11]], PAL.ink);
      poly([[5, hy - 7], [26, hy - 9], [17, hy + 2]], PAL.cream);
      c.fillStyle = o.eyeCol || PAL.ink; c.beginPath(); c.arc(17, hy - 6, 3.6, 0, TAU); c.fill();
      c.fillStyle = lite; c.beginPath(); c.arc(14, hy + 14, 4, 0, TAU); c.fill();
      poly([[22, hy + 15], [31, hy + 17], [23, hy + 22]], PAL.kumkum);
    }
    if (o.tilak) poly([[-2, hy - 32], [4, hy - 32], [2, hy - 18], [0, hy - 18]], PAL.kumkum);
    const crown = o.crown || 'bun';
    if (crown === 'bun' && !monkey) { poly([[-30, hy - 30], [-6, hy - 30], [-10, hy - 60], [-26, hy - 60]], hair); c.fillStyle = gold; c.fillRect(-28, hy - 46, 20, 5); }
    if (crown === 'long') { poly([[-26, hy - 32], [-8, hy - 32], [-14, hy + 20], [-10, hy + 110], [-34, hy + 130], [-44, hy + 60], [-36, hy]], hair); c.fillStyle = gold; c.beginPath(); c.arc(-14, hy - 30, 5, 0, TAU); c.fill(); }
    if (crown === 'tall' || crown === 'king') {
      const tiers = crown === 'king' ? 5 : 4;
      poly([[-32, hy - 28], [32, hy - 28], [28, hy - 42], [-28, hy - 42]], gold);
      poly([[-32, hy - 28], [32, hy - 28], [30, hy - 34], [-30, hy - 34]], PAL.kumkum);
      for (let i = 0; i < tiers; i++) { const w = 48 - i * 10, y0 = hy - 42 - i * 22; poly([[-w / 2, y0], [w / 2, y0], [w / 2 - 6, y0 - 22], [-w / 2 + 6, y0 - 22]], i % 2 ? PAL.brass : gold); c.fillStyle = PAL.kumkum; c.beginPath(); c.arc(0, y0 - 11, 3.5, 0, TAU); c.fill(); }
      tri(0, hy - 42 - tiers * 22, 14, 26, gold); c.fillStyle = PAL.cream; c.beginPath(); c.arc(0, hy - 42 - tiers * 22 - 30, 4, 0, TAU); c.fill();
      poly([[-34, hy - 44], [-26, hy - 44], [-44, hy - 72], [-52, hy - 66]], gold); poly([[34, hy - 44], [26, hy - 44], [44, hy - 72], [52, hy - 66]], gold);
      if (crown === 'king') { poly([[-40, hy - 50], [-30, hy - 50], [-56, hy - 100], [-66, hy - 90]], PAL.brass); poly([[40, hy - 50], [30, hy - 50], [56, hy - 100], [66, hy - 90]], PAL.brass); }
    }
    if (crown === 'cap') { c.fillStyle = gold; c.beginPath(); c.arc(-2, hy - 20, 32, Math.PI, 0); c.fill(); poly([[-34, hy - 20], [30, hy - 20], [30, hy - 12], [-34, hy - 12]], PAL.brass); c.fillStyle = PAL.kumkum; c.beginPath(); c.arc(-2, hy - 40, 5, 0, TAU); c.fill(); }
    c.restore();
  }

  function ravana(c, o) {
    const d = o.dir == null ? -1 : o.dir, skin = o.skin || PAL.maroon, s = o.s || 1, K = 1.15 * FK;
    const poly = (pts, col) => { c.fillStyle = col; c.beginPath(); c.moveTo(pts[0][0], pts[0][1]); for (let i = 1; i < pts.length; i++) c.lineTo(pts[i][0], pts[i][1]); c.closePath(); c.fill(); };
    const head = (col, dd) => {
      c.save(); c.scale(dd, 1);
      poly([[-26, -34], [14, -36], [24, -22], [27, -12], [42, 2], [27, 8], [31, 17], [23, 30], [2, 40], [-18, 32], [-28, 6]], col);
      poly([[-28, -36], [16, -38], [24, -22], [-4, -24], [-27, -18]], PAL.ink);
      poly([[4, -16], [27, -18], [27, -13], [4, -11]], PAL.ink);
      poly([[5, -7], [26, -9], [17, 2]], PAL.kumkum); c.fillStyle = PAL.ink; c.beginPath(); c.arc(17, -6, 3.4, 0, TAU); c.fill();
      poly([[10, 18], [34, 14], [36, 22], [12, 26]], PAL.ink);
      poly([[-32, -28], [32, -28], [26, -46], [14, -60], [0, -84], [-14, -60], [-26, -46]], PAL.gold); c.fillStyle = PAL.kumkum; c.beginPath(); c.arc(0, -48, 5, 0, TAU); c.fill();
      c.restore();
    };
    c.save(); c.translate(o.x, o.y); c.scale(s * d, s);
    for (let k = 4; k >= 1; k--) for (const sd of [-1, 1]) {
      c.save(); c.translate(sd * k * 24 * K, -352 * K + k * 5); c.scale(K * (0.86 - k * 0.08), K * (0.86 - k * 0.08));
      head(mixc(skin, PAL.ink, 0.1 + k * 0.08), sd);
      c.restore();
    }
    figure(c, { x: 0, y: 0, s: 1.15, dir: 1, skin, cloth: PAL.ink, sash: PAL.gold, crown: 'king', pose: o.pose || 'stand', arms: o.arms || [[-0.9, -0.9], [0.9, -1.4]], eyeCol: PAL.kumkum, mace: o.mace });
    c.strokeStyle = mixc(skin, PAL.ink, 0.2); c.lineWidth = 14 * K; c.lineCap = 'butt';
    for (const [a1, a2, sd] of [[-2.3, -0.6, 1], [2.3, 0.6, -1], [-1.9, -1.4, 1], [1.9, 1.4, -1]]) {
      const x0 = sd * 40 * K, y0 = -280 * K, L1 = 70 * K, L2 = 64 * K;
      c.beginPath(); c.moveTo(x0, y0); c.lineTo(x0 + Math.sin(a1) * L1, y0 + Math.cos(a1) * L1); c.lineTo(x0 + Math.sin(a1) * L1 + Math.sin(a2) * L2, y0 + Math.cos(a1) * L1 + Math.cos(a2) * L2); c.stroke();
    }
    c.restore();
  }

  function vanara(c, x, y, s, dir, ph, col) {
    figure(c, { x, y, s, dir, skin: col || PAL.burnt, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'none', face: 'monkey', pose: 'walk', ph, tail: true, mace: true, maceA: -0.9 });
  }
  
  function elephant(c, x, y, s, dir, col, t) {
    c.save(); c.translate(x, y); c.scale(s * (dir || 1), s); c.fillStyle = col || PAL.brown;
    c.beginPath(); c.ellipse(-40, -150, 130, 95, 0, 0, TAU); c.fill();
    for (const lx of [-120, -70, 10, 60]) c.fillRect(lx - 20, -120, 40, 120);
    c.beginPath(); c.arc(110, -190, 62, 0, TAU); c.fill();
    c.beginPath(); c.ellipse(60, -190, 50, 70, 0.2, 0, TAU); c.fill();
    const sw = Math.sin((t || 0) * 1.5) * 10;
    c.lineWidth = 34; c.strokeStyle = col || PAL.brown; c.lineCap = 'round'; c.beginPath(); c.moveTo(150, -170); c.quadraticCurveTo(190 + sw, -90, 160 + sw, -10); c.stroke();
    c.strokeStyle = PAL.sandal; c.lineWidth = 8; c.beginPath(); c.moveTo(140, -160); c.quadraticCurveTo(200, -150, 220, -110); c.stroke();
    c.fillStyle = PAL.kumkum; c.beginPath(); c.moveTo(-130, -200); c.lineTo(40, -200); c.lineTo(50, -120); c.lineTo(-140, -120); c.closePath(); c.fill();
    c.fillStyle = PAL.gold; c.fillRect(-140, -128, 190, 8); for (let k = -120; k < 40; k += 24) { c.beginPath(); c.arc(k, -112, 5, 0, TAU); c.fill(); }
    c.beginPath(); c.moveTo(118, -250); c.lineTo(100, -176); c.lineTo(140, -176); c.closePath(); c.fill();
    c.fillStyle = PAL.cream; c.beginPath(); c.ellipse(124, -184, 8, 4, -0.2, 0, TAU); c.fill(); c.fillStyle = PAL.ink; c.beginPath(); c.arc(126, -184, 3, 0, TAU); c.fill();
    c.restore();
  }
  
  function crownOnly(c, x, y, s, a) {
    c.save(); c.translate(x, y); c.rotate(a || 0); c.scale(s, s); c.fillStyle = PAL.gold;
    c.beginPath(); c.moveTo(-24, 0); c.lineTo(24, 0); c.lineTo(18, -26); c.lineTo(8, -36); c.lineTo(0, -80); c.lineTo(-8, -36); c.lineTo(-18, -26); c.closePath(); c.fill();
    c.fillStyle = PAL.kumkum; c.beginPath(); c.arc(0, -20, 5, 0, TAU); c.fill(); c.fillStyle = PAL.brass; c.fillRect(-24, -4, 48, 4);
    c.restore();
  }
  
  function bridge(c, x0, x1, y, prog, col) {
    const r = H.rng(44), n = 40, far = x0 + (x1 - x0) * prog;
    c.save(); c.fillStyle = col;
    for (let k = 0; k < n; k++) { const x = x0 + (x1 - x0) * (k / n); if (x > far) break; const w = (x1 - x0) / n * 0.9, h = 14 + r() * 10; c.beginPath(); c.roundRect(x, y - h / 2 + (r() - 0.5) * 6, w, h, 5); c.fill(); }
    c.restore();
  }

  function title(c, text, x, y, size, col, o) {
    o = o || {}; c.save(); c.font = `${o.italic ? 'italic ' : ''}400 ${size}px ${FF}`; c.textAlign = o.align || 'center'; c.textBaseline = 'alphabetic';
    if (o.glow) { c.shadowColor = o.glow; c.shadowBlur = o.blur || 30; }
    if (o.letter) c.letterSpacing = o.letter;
    if (o.stroke) { c.lineWidth = o.strokeW || 6; c.strokeStyle = o.stroke; c.lineJoin = 'round'; c.strokeText(text, x, y); }
    c.fillStyle = col; c.fillText(text, x, y); c.restore();
  }
  
  function wrapText(c, text, x, y, maxW, lh, font, col, o) {
    o = o || {}; c.save(); c.font = font; c.textAlign = 'center'; c.textBaseline = 'middle';
    const words = text.split(' '), lines = [[]]; let w = 0;
    for (const wd of words) { const ww = c.measureText(wd + ' ').width; if (w + ww > maxW && lines[lines.length - 1].length) { lines.push([]); w = 0; } lines[lines.length - 1].push(wd); w += ww; }
    lines.forEach((L, i) => { const yy = y + (i - (lines.length - 1) / 2) * lh, s = L.join(' '); if (o.stroke) { c.lineWidth = o.strokeW || 8; c.strokeStyle = o.stroke; c.lineJoin = 'round'; c.strokeText(s, x, yy); } c.fillStyle = col; c.fillText(s, x, yy); });
    c.restore(); return lines.length;
  }
