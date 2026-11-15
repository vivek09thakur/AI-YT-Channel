  // ---------- Kauwa kabhi nahi bhoolta: timing from the voiceover ----------
  // Word times (s) from whisper on 05_Audio/lekha_base.wav (Seed-VC keeps the timing). A new take = edit WT only.
  const WT = {
    pareshan: 0.97, saalon: 2.85, aur1: 4.20, doston: 4.69, bhi: 5.25,
    kahani: 6.20, uw: 7.72, sach: 10.40,
    y2006: 11.66, scientist: 12.53, mask: 14.17, kuch: 15.12, pakde: 15.43, chot: 16.99, tag: 18.90, chhod: 19.56,
    uske: 20.42, mask2: 21.68, cheekh: 24.33, jhund: 25.11,
    dusra: 26.89, dmask: 27.43, dhyan: 29.30,
    twist: 30.32, kabhi: 33.64, sikha: 36.59, dushman: 37.65,
    aur2: 38.47, nafrat: 38.91, fifteen: 39.64, zyada: 40.29,
    research2: 41.14, mar: 43.63, jama: 46.04, khatra: 49.70, kaun: 50.52,
    agli: 51.28, izzat: 52.91, wo: 54.39, shehar: 56.00, last: 59.29,
  };
  const DURATION = 60.3; // last word ends 59.29 + ~1 s hold on the takeaway
  const LEAD = 0.1;      // visuals lead their word by 0.1 s (never lag)
  const at = (k) => WT[k] - LEAD;
  // scene changes, each placed in a breath of the voice
  const SC = { research: 6.2, twist: 30.25, dead: 41.17, end: 51.2 };
  const BEATS = [
    { n: 1, name: 'Hook', t0: 0, t1: 6.1, vo: 'Aapne kabhi kauwe ko pareshan kiya hai? Woh aapka chehra saalon yaad rakhega… aur apne doston ko bhi bata dega.', screen: 'SAALON' },
    { n: 2, name: 'The research', t0: 6.1, t1: 11.5, vo: 'Ye kahani nahi hai. America ki University of Washington mein scientists ne ise sach mein test kiya.', screen: 'University of Washington, USA · REAL RESEARCH' },
    { n: 3, name: 'The mask experiment', t0: 11.5, t1: 20.4, vo: '2006 mein ek scientist ne ek ajeeb sa mask pehna, aur campus ke kuch kauwe pakde. Unhe chot nahi pahunchayi. Bas pakda, tag kiya aur chhod diya.', screen: '2006' },
    { n: 4, name: 'The crows attack', t0: 20.4, t1: 26.8, vo: 'Uske baad jo bhi wo mask pehen kar campus mein chalta, kauwe uske upar cheekhne lagte. Jhund bana kar peeche padte.', screen: 'KAA! ×4' },
    { n: 5, name: 'Dangerous vs neutral mask', t0: 26.8, t1: 30.2, vo: 'Ek dusra mask bhi pehna gaya, aur us par kisi ne dhyan nahi diya.', screen: '❌ · ✅ badges' },
    { n: 6, name: 'The twist', t0: 30.2, t1: 38.4, vo: 'Ab twist suniye. Kuch saal baad wo kauwe bhi cheekh rahe the jo kabhi pakde hi nahi gaye the. Matlab kauwon ne ek dusre ko sikha diya ki dushman kaun hai.', screen: 'TWIST · SIKHA DIYA' },
    { n: 7, name: '15+ years', t0: 38.4, t1: 41.1, vo: 'Aur ye nafrat 15 saal se zyada chali.', screen: '2006 → 2021+ · 15+ · SAAL' },
    { n: 8, name: 'The dead-crow gathering', t0: 41.1, t1: 51.2, vo: 'Ek aur research mein dekha gaya ki jab koi kauwa mar jaata hai, to baaki kauwe uske aas-paas jama ho jaate hain. Scientists ka maanna hai ki aise wo seekhte hain ki khatra kahan hai, aur kaun hai.', screen: '2015 · map pin · ?' },
    { n: 9, name: 'Ending + CTA', t0: 51.2, t1: DURATION, vo: 'To agli baar kauwa dikhe, to izzat se pesh aaiye, kyunki wo aapko dekh raha hai. Aur aapke shehar ka kauwa kitna smart hai? Comment mein bataiye.', screen: 'WOH DEKH RAHA HAI · Aapke shehar ka kauwa kitna smart hai?' },
  ];

  const RED = 'rgb(240,60,46)', GOLD = 'rgb(255,214,96)', SKY = 'rgb(140,200,230)';
  const EYE_DIM = [150, 84, 40], EYE_HOT = [255, 70, 44];
  const pop = (t, t0, d) => H.ease.back(cl((t - t0) / (d || 0.22)));   // 0 -> overshoot -> 1
  const dip = (t, c) => Math.sin(Math.PI * cl((t - (c - 0.25)) / 0.5)); // lamp turned down and up around c
  const flapW = (t, k) => 0.15 + 0.85 * (0.5 + 0.5 * Math.sin(t * 17 + k * 1.7));

  // ---------- puppets ----------
  // crow, side view facing left (dir -1 faces right). Feet at (x,y); ~230 units tall at s=1.
  // o: s dir tilt head face(0 profile .. 1 frontal) glare wing legs blink eye([r,g,b]) band(0..1) noRods
  function crow(p, g, o, rods) {
    const d = o.dir == null ? 1 : o.dir;
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.tilt || 0); c.scale(o.s * d, o.s); });
    p.fillStyle = INK; p.strokeStyle = INK;
    // legs, toes and the optional leg band
    if (o.legs !== false) {
      p.lineCap = 'round'; p.lineWidth = 7;
      for (const lx of [-8, 14]) {
        p.beginPath(); p.moveTo(lx + 5, -70); p.lineTo(lx, -4); p.stroke();
        [Math.PI - 0.05, Math.PI - 0.5, 0.15].forEach((a) => tear(p, lx, -4, 22, 6, a));
      }
      if (o.band > 0.01) {
        both([p, g], (c) => { c.save(); c.translate(-6, -30); c.scale(o.band, o.band); });
        p.fillStyle = INK; p.beginPath(); p.roundRect(-11, -10, 22, 20, 5); p.fill();
        cut(p, () => { p.fillRect(-7, -4, 14, 8); });
        g.fillStyle = GOLD; g.fillRect(-8, -5, 16, 10);
        both([p, g], (c) => c.restore());
      }
    }
    // tail fan
    p.beginPath(); p.moveTo(46, -116); p.lineTo(168, -84); p.quadraticCurveTo(182, -60, 166, -36); p.lineTo(44, -78); p.closePath(); p.fill();
    cut(p, () => { p.lineWidth = 2; for (let k = 0; k < 3; k++) { p.beginPath(); p.moveTo(80, -98 + k * 9); p.lineTo(160, -76 + k * 14); p.stroke(); } });
    // body and breast
    p.beginPath(); p.ellipse(8, -108, 76, 46, -0.32, 0, TAU); p.fill();
    p.beginPath(); p.ellipse(-38, -138, 36, 31, -0.6, 0, TAU); p.fill();
    cut(p, () => {
      for (let i = 0; i < 26; i++) { const a = i / 26 * TAU; dot(p, 8 + Math.cos(a) * 60 * Math.cos(-0.32) - Math.sin(a) * 34 * Math.sin(-0.32), -108 + Math.cos(a) * 60 * Math.sin(-0.32) + Math.sin(a) * 34 * Math.cos(-0.32), 2.4); }
      for (let row = 0; row < 3; row++) for (let k = 0; k < 4 - row; k++) tear(p, -50 + k * 15 + row * 7, -118 + row * 13, 11, 6, Math.PI / 2 + 0.3);
    });
    // wing, pinned at the shoulder; lifts for flight
    both([p, g], (c) => { c.save(); c.translate(-4, -128); c.rotate(-(o.wing || 0)); });
    p.fillStyle = INK;
    p.beginPath(); p.moveTo(-16, -6); p.bezierCurveTo(40, -28, 112, -14, 150, 24); p.bezierCurveTo(110, 32, 46, 34, -8, 18); p.closePath(); p.fill();
    for (let k = 0; k < 5; k++) tear(p, 82 + k * 13, 20 - k * 2, 40 - k * 3, 10, 0.32 - k * 0.04);
    cut(p, () => {
      for (let k = 0; k < 6; k++) tear(p, 6 + k * 19, 3 + k * 1.6, 15, 5, 0.1);
      p.lineWidth = 1.8; p.beginPath(); p.moveTo(0, 10); p.quadraticCurveTo(60, 14, 128, 24); p.stroke();
    });
    pin(p, 0, 0, 7);
    if (rods && !o.noRods) rods.push([...wpt(p, 118, 20), 2.4]);
    both([p, g], (c) => c.restore());
    // head, pinned at the neck; flips between profile and frontal (a second head card swung round on its pin)
    both([p, g], (c) => { c.save(); c.translate(-48, -140); c.rotate(o.head || 0); c.translate(48, 140); });
    const face = o.face || 0, eye = H.rgba(o.eye || [255, 196, 90]), bl = o.blink || 0;
    if (face < 0.5) {
      const sx = Math.max(0.04, 1 - face * 2);
      both([p, g], (c) => { c.save(); c.translate(-62, -160); c.scale(sx, 1); c.translate(62, 160); });
      p.fillStyle = INK; dot(p, -62, -160, 33);
      p.beginPath(); p.moveTo(-80, -180); p.quadraticCurveTo(-118, -182, -158, -160); p.quadraticCurveTo(-120, -150, -84, -144); p.closePath(); p.fill();
      cut(p, () => {
        dot(p, -68, -168, 9);
        p.lineWidth = 1.8; p.beginPath(); p.moveTo(-92, -162); p.lineTo(-146, -159); p.stroke();
        for (let k = 0; k < 7; k++) { const a = -2.6 + k * 0.3; dot(p, -60 + Math.cos(a) * 24, -160 + Math.sin(a) * 24, 1.8); }
      });
      g.fillStyle = eye; dot(g, -68, -168, 10);
      p.fillStyle = INK; dot(p, -70, -168, 3.6);
      if (bl > 0) { p.fillRect(-79, -179, 22, 22 * bl); }
      both([p, g], (c) => c.restore());
    } else {
      const sx = Math.max(0.04, (face - 0.5) * 2);
      both([p, g], (c) => { c.save(); c.translate(-58, -160); c.scale(sx, 1); c.translate(58, 160); });
      p.fillStyle = INK; p.beginPath(); p.ellipse(-58, -160, 36, 38, 0, 0, TAU); p.fill();
      // the heavy crow beak, seen head-on: a long wedge from between the eyes
      p.beginPath(); p.moveTo(-76, -164); p.quadraticCurveTo(-58, -170, -40, -164); p.lineTo(-52, -112); p.lineTo(-58, -92); p.lineTo(-64, -112); p.closePath(); p.fill();
      cut(p, () => {
        dot(p, -78, -170, 9); dot(p, -38, -170, 9);
        p.lineWidth = 1.6; p.beginPath(); p.moveTo(-58, -150); p.lineTo(-58, -104); p.stroke();
        dot(p, -64, -148, 2); dot(p, -52, -148, 2);
      });
      g.fillStyle = eye; dot(g, -78, -170, 10); dot(g, -38, -170, 10);
      p.fillStyle = INK; dot(p, -78, -169, 3.8); dot(p, -38, -169, 3.8);
      if (o.glare) { // brows pulled down toward the beak
        p.beginPath(); p.moveTo(-91, -184); p.lineTo(-65, -184); p.lineTo(-65, -167); p.closePath(); p.fill();
        p.beginPath(); p.moveTo(-25, -184); p.lineTo(-51, -184); p.lineTo(-51, -167); p.closePath(); p.fill();
      }
      if (bl > 0) { p.fillRect(-89, -181, 62, 22 * bl); }
      both([p, g], (c) => c.restore());
    }
    pin(p, -48, -140, 6);
    both([p, g], (c) => c.restore());
    if (rods && !o.noRods) rods.push([...wpt(p, 10, -70), 3.2]);
    both([p, g], (c) => c.restore());
  }
  // where a crow's chest is on screen (for vines)
  const chest = (x, y, s, dir) => [x - 20 * s * (dir || 1), y - 112 * s];

  // a face mask, front on, centred at (x,y), ~120 wide at s=1. kind 'cave' (the dangerous one) or 'plain' (the control)
  function mask(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); c.scale(o.s, o.s); });
    p.fillStyle = INK; p.strokeStyle = INK;
    if (o.stick) { p.fillRect(-5, 50, 10, o.stick); }
    if (o.kind === 'cave') {
      for (let k = 0; k <= 12; k++) { const a = Math.PI + 0.1 + k / 12 * (Math.PI - 0.2); tear(p, Math.cos(a) * 34, Math.sin(a) * 40 - 10, 44 + (k % 2) * 18, 17, a); }
      p.beginPath(); p.ellipse(0, 4, 52, 62, 0, 0, TAU); p.fill();
      for (let k = -3; k <= 3; k++) tear(p, k * 13, 44, 34 + (3 - Math.abs(k)) * 7, 15, Math.PI / 2 + k * 0.14);
      cut(p, () => {
        p.beginPath(); p.ellipse(-21, -6, 12, 8, 0.1, 0, TAU); p.fill(); p.beginPath(); p.ellipse(21, -6, 12, 8, -0.1, 0, TAU); p.fill();
        p.lineWidth = 3; p.beginPath(); p.moveTo(-40, -24); p.quadraticCurveTo(0, -14, 40, -24); p.stroke();
        dot(p, -7, 17, 3.4); dot(p, 7, 17, 3.4);
        p.fillRect(-26, 30, 52, 11);
        p.lineWidth = 1.6; p.beginPath(); p.moveTo(-44, 6); p.lineTo(-34, 14); p.moveTo(44, 6); p.lineTo(34, 14); p.stroke();
      });
      p.fillStyle = INK; for (let k = -2; k <= 2; k++) p.fillRect(k * 10 - 1.5, 30, 3, 11);
      g.fillStyle = RED; g.beginPath(); g.ellipse(-21, -6, 13, 9, 0, 0, TAU); g.fill(); g.beginPath(); g.ellipse(21, -6, 13, 9, 0, 0, TAU); g.fill();
      g.fillStyle = 'rgb(255,190,120)'; g.fillRect(-27, 29, 54, 13);
    } else {
      for (const sx of [-1, 1]) { p.beginPath(); p.ellipse(sx * 48, 0, 9, 16, 0, 0, TAU); p.fill(); }
      p.beginPath(); p.ellipse(0, 0, 48, 60, 0, 0, TAU); p.fill();
      cut(p, () => {
        p.beginPath(); p.ellipse(-17, -10, 10, 5, 0, 0, TAU); p.fill(); p.beginPath(); p.ellipse(17, -10, 10, 5, 0, 0, TAU); p.fill();
        p.lineWidth = 2; p.beginPath(); p.moveTo(0, -2); p.lineTo(-4, 14); p.lineTo(3, 14); p.stroke();
        p.fillRect(-14, 28, 28, 3);
        for (let k = 0; k < 28; k++) { const a = k / 28 * TAU; dot(p, Math.cos(a) * 41, Math.sin(a) * 53, 1.6); }
      });
      g.fillStyle = 'rgb(200,236,220)'; g.beginPath(); g.ellipse(-17, -10, 11, 6, 0, 0, TAU); g.fill(); g.beginPath(); g.ellipse(17, -10, 11, 6, 0, 0, TAU); g.fill();
    }
    both([p, g], (c) => c.restore());
  }

  // a person in a lab coat, side view facing left, feet at (x,y), ~430 tall at s=1. o: step arm mask('cave'|'plain'|null)
  function person(p, g, o, rods) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.scale(o.s * (o.dir || 1), o.s); });
    p.fillStyle = INK; p.strokeStyle = INK;
    const st = o.step || 0;
    for (const [hx, ph] of [[-8, 0], [12, Math.PI]]) {
      both([p, g], (c) => { c.save(); c.translate(hx, -196); c.rotate(Math.sin(st + ph) * 0.32); });
      p.beginPath(); p.moveTo(-15, 0); p.lineTo(15, 0); p.lineTo(10, 186); p.lineTo(-10, 186); p.closePath(); p.fill();
      p.beginPath(); p.ellipse(-14, 190, 26, 10, 0, 0, TAU); p.fill();
      pin(p, 0, 0, 6);
      both([p, g], (c) => c.restore());
    }
    p.beginPath(); p.moveTo(-46, -340); p.quadraticCurveTo(-62, -260, -64, -146); p.lineTo(68, -146); p.quadraticCurveTo(58, -260, 46, -340); p.closePath(); p.fill();
    cut(p, () => {
      p.lineWidth = 2.4; p.beginPath(); p.moveTo(-30, -338); p.lineTo(-4, -290); p.lineTo(-18, -150); p.stroke();
      for (let y = -280; y < -160; y += 26) dot(p, -10, y, 3.4);
      p.beginPath(); p.roundRect(14, -244, 30, 26, 4); p.stroke();
      for (let x = -56; x < 62; x += 10) dot(p, x, -158, 1.8);
    });
    both([p, g], (c) => { c.save(); c.translate(6, -326); c.rotate(o.arm == null ? 0.12 : o.arm); });
    p.beginPath(); p.roundRect(-12, -6, 24, 150, 12); p.fill();
    p.beginPath(); p.ellipse(-2, 152, 14, 19, 0, 0, TAU); p.fill();
    cut(p, () => { p.lineWidth = 2; p.beginPath(); p.moveTo(-11, 124); p.lineTo(11, 124); p.stroke(); });
    if (rods && !o.noRods) rods.push([...wpt(p, 0, 156), 2.6]);
    pin(p, 0, 0, 7);
    both([p, g], (c) => c.restore());
    p.fillStyle = INK; p.fillRect(-14, -366, 26, 34);
    if (o.mask) mask(p, g, { x: -8, y: -396, s: 0.95, kind: o.mask });
    else {
      p.beginPath(); p.ellipse(-4, -394, 36, 42, 0, 0, TAU); p.fill();
      p.beginPath(); p.moveTo(-36, -404); p.lineTo(-52, -384); p.lineTo(-36, -378); p.closePath(); p.fill();
      cut(p, () => dot(p, -20, -400, 4));
    }
    if (rods && !o.noRods) rods.push([...wpt(p, 4, -220), 3.4]);
    both([p, g], (c) => c.restore());
  }

  // a cord net, top at (x,y), bell shaped; holes punched as diamonds
  function net(p, o) {
    const w = o.w, h = o.h, hw = (y) => w / 2 * Math.sqrt(cl(y / h, 0.02, 1));
    p.save(); p.translate(o.x, o.y); p.rotate(o.rot || 0);
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 2.2;
    p.beginPath(); p.moveTo(0, 0); p.lineTo(0, -900); p.stroke();
    // open cord lattice inside the bell, so whatever is caught still reads through it
    const bell = new Path2D(); bell.moveTo(0, 0); for (let y = 0; y <= h; y += 6) bell.lineTo(hw(y), y); for (let y = h; y >= 0; y -= 6) bell.lineTo(-hw(y), y); bell.closePath();
    p.save(); p.clip(bell); p.lineWidth = 2.6;
    for (let k = -w; k <= w; k += 34) { p.beginPath(); p.moveTo(k, 0); p.lineTo(k + h, h); p.moveTo(k, 0); p.lineTo(k - h, h); p.stroke(); }
    p.restore();
    p.lineWidth = 5; p.stroke(bell);
    p.fillRect(-w / 2 - 4, h - 8, w + 8, 12);
    for (let x = -w / 2; x <= w / 2; x += 38) dot(p, x, h + 4, 8);
    for (let y = 30; y < h; y += 40) { dot(p, hw(y), y, 4); dot(p, -hw(y), y, 4); }
    p.restore();
  }

  // pointed (gothic) arch outline
  function arch(c, x, y, w, h) { c.moveTo(x - w / 2, y); c.lineTo(x - w / 2, y - h + w * 0.7); c.quadraticCurveTo(x - w / 2, y - h + w * 0.1, x, y - h); c.quadraticCurveTo(x + w / 2, y - h + w * 0.1, x + w / 2, y - h + w * 0.7); c.lineTo(x + w / 2, y); c.closePath(); }
  function tree(p, x, y, h) {
    p.fillStyle = INK; p.fillRect(x - 5, y - h * 0.45, 10, h * 0.45);
    for (let k = 0; k < 14; k++) { const a = -Math.PI / 2 + (k / 13 - 0.5) * 2.6, r = h * (0.18 + 0.12 * ((k * 7) % 3)); tear(p, x + Math.cos(a) * r * 0.5, y - h * 0.62 + Math.sin(a) * r * 0.5, h * 0.28, h * 0.14, a); }
    p.beginPath(); p.ellipse(x, y - h * 0.62, h * 0.2, h * 0.26, 0, 0, TAU); p.fill();
  }
  // the campus "photo": a pinned picture frame, a gothic library facade cut against a sky gel
  function campusCard(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); c.scale(o.s, o.s); });
    const w = 700, h = 420;
    p.fillStyle = INK; p.strokeStyle = INK;
    p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, 10); p.fill();
    for (let x = -w / 2 + 8; x <= w / 2 - 8; x += 14) { dot(p, x, -h / 2, 5); dot(p, x, h / 2, 5); }
    for (let y = -h / 2 + 14; y <= h / 2 - 14; y += 14) { dot(p, -w / 2, y, 5); dot(p, w / 2, y, 5); }
    cut(p, () => { p.beginPath(); p.roundRect(-w / 2 + 24, -h / 2 + 24, w - 48, h - 48, 6); p.fill(); });
    g.fillStyle = SKY; g.fillRect(-w / 2 + 22, -h / 2 + 22, w - 44, h - 44);
    const gy = h / 2 - 40;
    p.fillStyle = INK; p.fillRect(-w / 2 + 24, gy, w - 48, 20);
    // library: central hall with a steep gable, two spired towers, low side wings
    p.beginPath(); p.moveTo(-120, gy); p.lineTo(-120, -40); p.lineTo(0, -128); p.lineTo(120, -40); p.lineTo(120, gy); p.closePath(); p.fill();
    for (const sx of [-1, 1]) {
      p.fillRect(sx * 150 - 26, -96, 52, gy + 96);
      p.beginPath(); p.moveTo(sx * 150 - 26, -96); p.lineTo(sx * 150, -170); p.lineTo(sx * 150 + 26, -96); p.closePath(); p.fill();
      p.fillRect(sx > 0 ? 176 : -270, 0, 94, gy);
      for (let k = 0; k < 3; k++) { p.beginPath(); p.moveTo(sx * (190 + k * 30) - 6, 0); p.lineTo(sx * (190 + k * 30), -22); p.lineTo(sx * (190 + k * 30) + 6, 0); p.fill(); }
    }
    for (let k = -2; k <= 2; k++) { p.beginPath(); p.moveTo(k * 48 - 5, -40 - (2 - Math.abs(k)) * 30); p.lineTo(k * 48, -66 - (2 - Math.abs(k)) * 30); p.lineTo(k * 48 + 5, -40 - (2 - Math.abs(k)) * 30); p.fill(); }
    cut(p, () => {
      p.beginPath(); for (let k = -2; k <= 2; k++) arch(p, k * 44, gy - 16, 26, 118); p.fill();
      dot(p, 0, -66, 20);
      p.beginPath(); for (const sx of [-1, 1]) arch(p, sx * 150, -20, 16, 50); for (const sx of [-1, 1]) for (let k = 0; k < 2; k++) arch(p, sx * (204 + k * 34), gy - 20, 14, 60); p.fill();
    });
    p.fillStyle = INK; dot(p, 0, -66, 8); for (let k = 0; k < 8; k++) { p.save(); p.translate(0, -66); p.rotate(k * TAU / 8); p.fillRect(-1.5, 0, 3, 20); p.restore(); }
    tree(p, -300, gy, 150); tree(p, 300, gy, 130);
    // a crow sits on the gable
    crow(p, g, { x: 26, y: -118, s: 0.16, noRods: true, eye: [255, 196, 90] });
    for (const sx of [-1, 1]) for (const sy of [-1, 1]) pin(p, sx * (w / 2 - 12), sy * (h / 2 - 12), 9);
    both([p, g], (c) => c.restore());
  }

  // a rubber-stamp style plaque with cut letters over a gel. o: x y rot s text size gel
  function stamp(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); c.scale(o.s, o.s); });
    p.font = `400 ${o.size}px ${FF}`;
    const tw = p.measureText(o.text).width, w = tw + o.size * 1.2, h = o.size * 1.6;
    p.fillStyle = INK; p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, 10); p.fill();
    for (let x = -w / 2 + 6; x <= w / 2 - 6; x += 15) { dot(p, x, -h / 2, 5.5); dot(p, x, h / 2, 5.5); }
    for (let y = -h / 2 + 15; y <= h / 2 - 15; y += 15) { dot(p, -w / 2, y, 5.5); dot(p, w / 2, y, 5.5); }
    cut(p, () => {
      p.lineWidth = 3; p.beginPath(); p.roundRect(-w / 2 + 9, -h / 2 + 9, w - 18, h - 18, 6); p.stroke();
      p.lineWidth = 1.5; p.beginPath(); p.roundRect(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32, 4); p.stroke();
      p.textAlign = 'center'; p.textBaseline = 'middle'; p.fillText(o.text, 0, o.size * 0.06);
    });
    g.fillStyle = o.gel || RED; g.fillRect(-w / 2 + 6, -h / 2 + 6, w - 12, h - 12);
    both([p, g], (c) => c.restore());
  }
  // little cut hide crumbs thrown out when a stamp lands (the "dust puff" of this medium)
  function crumbs(p, x, y, u, seed, spread) {
    if (u <= 0 || u >= 1) return;
    const r = H.rng(seed);
    p.fillStyle = INK;
    for (let k = 0; k < 16; k++) {
      const a = r() * TAU, d = (spread || 260) * (0.4 + r() * 0.6) * EO(u), s = (3 + r() * 6) * (1 - u);
      p.save(); p.translate(x + Math.cos(a) * d, y + Math.sin(a) * d * 0.55 + 60 * u * u); p.rotate(r() * 6 + u * 4);
      p.fillRect(-s, -s * 0.6, s * 2, s * 1.2); p.restore();
    }
  }
  // a hanging tag with a gel behind its letters (same frame as tag())
  function gelTag(p, g, o, color) {
    tag(p, g, o);
    g.save(); g.translate(o.x, o.y); g.rotate(o.rot || 0); g.translate(0, 30 + o.h / 2); g.scale(o.flip == null ? 1 : o.flip, 1);
    g.fillStyle = color; g.fillRect(-o.w / 2 + 6, -o.h / 2 + 6, o.w - 12, o.h - 12); g.restore();
  }
  // a jagged "KAA!" shout burst
  function kaa(p, g, o) {
    if (o.s < 0.02) return;
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); c.scale(o.s, o.s); });
    const r = H.rng(o.seed || 3);
    p.fillStyle = INK; p.beginPath();
    for (let i = 0; i < 28; i++) { const a = i / 28 * TAU, rr = (i % 2 ? 58 : 84 + r() * 16); p.lineTo(Math.cos(a) * rr * 1.25, Math.sin(a) * rr * 0.85); }
    p.closePath(); p.fill();
    cut(p, () => { p.font = `400 42px ${FF}`; p.textAlign = 'center'; p.textBaseline = 'middle'; p.fillText('KAA!', 0, 3); });
    g.fillStyle = RED; g.beginPath(); g.ellipse(0, 0, 62, 40, 0, 0, TAU); g.fill();
    both([p, g], (c) => c.restore());
  }
  // a ring cut from hide with a red gel slot, drawn on round its centre. prog 0..1
  function ring(p, g, x, y, r, prog) {
    if (prog <= 0.001) return;
    const a0 = -Math.PI * 0.6, a1 = a0 + TAU * prog;
    p.save(); p.strokeStyle = INK; p.lineCap = 'round'; p.lineWidth = 16; p.beginPath(); p.arc(x, y, r, a0, a1); p.stroke(); p.restore();
    cut(p, () => { p.lineWidth = 5; p.lineCap = 'round'; p.beginPath(); p.arc(x, y, r, a0 + 0.05, a1 - 0.05); p.stroke(); });
    g.save(); g.strokeStyle = RED; g.lineWidth = 7; g.beginPath(); g.arc(x, y, r, a0, a1); g.stroke(); g.restore();
  }
  // a torn hide strip hung down the middle of the screen to split it
  function divider(p, x, yb) {
    if (yb <= 0) return;
    const j = (y, k) => Math.sin(y * 1.7 + k) * 4 + Math.sin(y * 0.53 + k * 2) * 3;
    p.fillStyle = INK; p.beginPath(); p.moveTo(x - 14, -10);
    for (let y = -10; y <= yb; y += 14) p.lineTo(x - 15 + j(y, 1), y);
    for (let y = yb; y >= -10; y -= 14) p.lineTo(x + 15 + j(y, 4), y);
    p.closePath(); p.fill();
    cut(p, () => { for (let y = 70; y < yb - 10; y += 30) { p.save(); p.translate(x, y); p.rotate(Math.PI / 4); p.fillRect(-4, -4, 8, 8); p.restore(); } });
  }
  function mapPin(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.scale(o.s, o.s); });
    p.fillStyle = INK; p.beginPath(); p.moveTo(0, 0); p.bezierCurveTo(-16, -30, -46, -54, -46, -88); p.arc(0, -88, 46, Math.PI, 0); p.bezierCurveTo(46, -54, 16, -30, 0, 0); p.fill();
    cut(p, () => { dot(p, 0, -88, 22); for (let k = 0; k < 14; k++) { const a = k / 14 * TAU; dot(p, Math.cos(a) * 36, -88 + Math.sin(a) * 36, 2); } });
    g.fillStyle = RED; dot(g, 0, -88, 23);
    both([p, g], (c) => c.restore());
  }
  // folded hands in a lace medallion
  function namaste(p, g, o) {
    if (o.s < 0.02) return;
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); c.scale(o.s, o.s); });
    p.fillStyle = INK; dot(p, 0, 0, 74);
    for (let k = 0; k < 18; k++) dot(p, Math.cos(k * TAU / 18) * 74, Math.sin(k * TAU / 18) * 74, 9);
    cut(p, () => dot(p, 0, 0, 60));
    g.fillStyle = GOLD; dot(g, 0, 0, 61);
    p.fillStyle = INK;
    for (const sd of [-1, 1]) {
      p.save(); p.scale(sd, 1);
      p.beginPath(); p.moveTo(1, -44); p.bezierCurveTo(4, -52, 15, -50, 17, -38); p.lineTo(24, 18); p.quadraticCurveTo(24, 34, 10, 40); p.lineTo(1, 40); p.closePath(); p.fill();
      p.beginPath(); p.ellipse(20, 2, 7, 15, -0.35, 0, TAU); p.fill();
      p.fillRect(0, 40, 24, 14);
      p.restore();
    }
    cut(p, () => { p.lineWidth = 1.6; for (const sd of [-1, 1]) { p.beginPath(); p.moveTo(sd * 9, -36); p.lineTo(sd * 11, -4); p.stroke(); } p.beginPath(); p.moveTo(-24, 47); p.lineTo(24, 47); p.stroke(); });
    both([p, g], (c) => c.restore());
  }
  // an eye charm hung on a string (stands in for the 👁 in the line)
  function eyeCharm(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); });
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 2;
    p.beginPath(); p.moveTo(0, -46); p.lineTo(0, -46 - (o.hang || 60)); p.stroke();
    p.beginPath(); p.moveTo(-74, 0); p.quadraticCurveTo(0, -78, 74, 0); p.quadraticCurveTo(0, 78, -74, 0); p.fill();
    cut(p, () => { p.beginPath(); p.moveTo(-58, 0); p.quadraticCurveTo(0, -56, 58, 0); p.quadraticCurveTo(0, 56, -58, 0); p.fill(); });
    g.fillStyle = 'rgb(255,200,110)'; g.beginPath(); g.moveTo(-60, 0); g.quadraticCurveTo(0, -58, 60, 0); g.quadraticCurveTo(0, 58, -60, 0); g.fill();
    p.fillStyle = INK; dot(p, 0, 0, 22); cut(p, () => dot(p, 7, -7, 6));
    both([p, g], (c) => c.restore());
  }
  // a speech bubble card for the closing question
  function bubble(p, g, o) {
    both([p, g], (c) => { c.save(); c.translate(o.x, o.y); c.rotate(o.rot || 0); });
    const w = 620, h = 176;
    p.fillStyle = INK; p.strokeStyle = INK;
    p.beginPath(); p.roundRect(-w / 2, -h / 2, w, h, 44); p.fill();
    p.beginPath(); p.moveTo(-w / 2 + 70, h / 2 - 6); p.lineTo(-w / 2 + 30, h / 2 + 64); p.lineTo(-w / 2 + 150, h / 2 - 6); p.closePath(); p.fill();
    for (let x = -w / 2 + 44; x <= w / 2 - 44; x += 16) { dot(p, x, -h / 2, 5.5); dot(p, x, h / 2, 5.5); }
    cut(p, () => {
      p.lineWidth = 2.6; p.beginPath(); p.roundRect(-w / 2 + 12, -h / 2 + 12, w - 24, h - 24, 34); p.stroke();
      p.font = `italic 400 44px ${FF}`; p.textAlign = 'center'; p.textBaseline = 'alphabetic';
      p.fillText('Aapke shehar ka kauwa', 0, -12);
      p.fillText('kitna smart hai?', -28, 50);
      const ax = 170, ay = 22; p.fillRect(ax - 4, ay - 10, 8, 26); p.beginPath(); p.moveTo(ax - 15, ay + 12); p.lineTo(ax + 15, ay + 12); p.lineTo(ax, ay + 32); p.closePath(); p.fill();
    });
    g.fillStyle = 'rgb(255,226,170)'; g.beginPath(); g.roundRect(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16, 38); g.fill();
    both([p, g], (c) => c.restore());
  }
  // counter board on strings (as in the reference), digits in lining figures
  function board(p, x, y, rot, text, size, popK) {
    p.save(); p.translate(x, y); p.rotate(rot);
    p.fillStyle = INK; p.strokeStyle = INK; p.lineWidth = 2;
    p.beginPath(); p.moveTo(-270, 40); p.lineTo(-270, -420); p.moveTo(270, 40); p.lineTo(270, -420); p.stroke();
    p.fillRect(-276, 28, 552, 8); dot(p, -276, 32, 8); dot(p, 276, 32, 8);
    p.save(); p.font = `400 ${size}px ${NF}`; const cw = p.measureText(text).width, fit = Math.min(1, 500 / cw); p.translate(0, -8); p.scale(popK * fit, popK * fit); p.textAlign = 'center'; p.textBaseline = 'alphabetic'; p.fillText(text, 0, 0); p.restore();
    p.restore();
  }

  // ---------- scenes ----------
  // the hook and the ending share the same big crow
  const BIG = { x: 520, y: 905, s: 2.8 };
  function sceneHook(st, t) {
    const face = sm(at('pareshan'), at('pareshan') + 0.12, t);
    // three more crows: slide in from the edges, then all turn to the viewer at once
    const sIn = EO(sm(at('aur1'), at('aur1') + 0.7, t)), turn = sm(at('bhi'), at('bhi') + 0.16, t);
    if (t > at('aur1')) pup(st, { blur: 1.4 }, (p, g, rods) => {
      crow(p, g, { x: lerp(1460, 1130, sIn), y: 708 - Math.abs(Math.sin(sIn * Math.PI * 2)) * 18 * (1 - sIn), s: 0.9, face: turn, glare: true, eye: EYE_DIM.map((v, i) => lerp(v, EYE_HOT[i], turn)), wing: 0.05, blink: blinkAt(t, [5.9]) }, rods);
      crow(p, g, { x: lerp(-260, 170, sIn), y: 712 - Math.abs(Math.sin(sIn * Math.PI * 2)) * 18 * (1 - sIn), s: 0.85, dir: -1, face: turn, glare: true, eye: EYE_DIM.map((v, i) => lerp(v, EYE_HOT[i], turn)), wing: 0.05 }, rods);
      const fy = lerp(-120, 470, sIn), fl = sIn < 0.98 ? flapW(t, 2) : 0.25 + 0.06 * Math.sin(t * 3);
      crow(p, g, { x: lerp(1420, 1010, sIn), y: fy, s: 0.8, wing: fl, legs: false, face: turn, glare: true, eye: EYE_DIM.map((v, i) => lerp(v, EYE_HOT[i], turn)) }, rods);
    });
    // the big crow: stares, then jerks round to face us on "pareshan"
    pup(st, {}, (p, g, rods) => crow(p, g, {
      ...BIG, y: BIG.y + Math.sin(t * 1.3) * 4, face, head: 0.04 * Math.sin(t * 0.9) - 0.12 * Math.sin(Math.PI * face) , glare: t > at('saalon'),
      eye: [255, 196, 90], wing: 0.03 + 0.02 * Math.sin(t * 2), blink: blinkAt(t, [2.2, 3.85]), noRods: false,
    }, rods));
    // SAALON slams down like a stamp
    if (t > at('saalon')) {
      const u = cl((t - at('saalon')) / 0.12), s = lerp(1.55, 1, EO(u)) + swing(t, at('saalon') + 0.12, 0.05, 6, 30);
      pup(st, {}, (p, g) => { stamp(p, g, { x: 930, y: 175, rot: -0.07, s, text: 'SAALON', size: 104 }); crumbs(p, 930, 190, (t - at('saalon') - 0.1) / 0.6, 11, 330); });
    }
  }

  // research -> mask experiment -> attack -> split: one continuous stage
  const SCI0 = 900, SCI_Y = 692, SCI_S = 0.95;
  const maskPt = (x) => [x - 8 * SCI_S, SCI_Y - 396 * SCI_S];
  function sciX(t) {
    const inU = EO(sm(at('scientist'), at('scientist') + 1.0, t));
    const walk = EIO(sm(WT.uske, 23.4, t));
    const left = EIO(sm(at('dusra'), at('dusra') + 0.5, t));
    return lerp(lerp(lerp(1500, SCI0, inU), 620, walk), 330, left);
  }
  function sceneStage(st, t) {
    // the campus picture: hangs on the screen, then is hoisted away
    const hoist = EIO(sm(11.25, 11.85, t));
    if (hoist < 1) pup(st, {}, (p, g) => {
      const cy = lerp(330, -420, hoist), rot = swing(t, SC.research, 0.03, 1.5, 5) + 0.01 * Math.sin(t * 1.2);
      campusCard(p, g, { x: 600, y: cy, s: 1, rot });
      p.save(); p.strokeStyle = INK; p.lineWidth = 2; p.beginPath(); p.moveTo(600, cy - 210); p.lineTo(600, -10); p.stroke(); p.restore();
      if (t > at('sach')) {
        const u = cl((t - at('sach')) / 0.12);
        stamp(p, g, { x: 850, y: cy - 150, rot: -0.24, s: lerp(1.5, 1, EO(u)) + swing(t, at('sach') + 0.12, 0.05, 6, 30), text: 'REAL RESEARCH', size: 46 });
        crumbs(p, 850, cy - 140, (t - at('sach') - 0.1) / 0.55, 21, 220);
      }
    });
    // University of Washington, USA: a typed strip rising on its rod
    if (t > at('uw') && t < 11.9) pup(st, {}, (p, g, rods) => {
      const rise = EO(sm(at('uw'), at('uw') + 0.35, t)) - EIO(sm(11.3, 11.8, t));
      const full = 'University of Washington, USA', n = Math.round(full.length * cl((t - at('uw')) / 0.75));
      const y = lerp(820, 642, rise);
      p.save(); p.font = `italic 400 36px ${FF}`; const w = p.measureText(full).width + 46; p.restore();
      p.fillStyle = INK; p.beginPath(); p.roundRect(600 - w / 2, y - 30, w, 60, 14); p.fill();
      cut(p, () => { p.lineWidth = 2; p.beginPath(); p.roundRect(600 - w / 2 + 6, y - 24, w - 12, 48, 10); p.stroke(); p.font = `italic 400 36px ${FF}`; p.textAlign = 'left'; p.textBaseline = 'middle'; p.fillText(full.slice(0, n), 600 - w / 2 + 23, y + 2); });
      rods.push([600, y + 30, 3]);
    });
    // 2006 tag flips in at top left
    if (t > at('y2006')) pup(st, {}, (p, g) => {
      const fu = sm(at('y2006'), at('y2006') + 0.3, t), flip = Math.max(0.04, Math.abs(Math.cos((1 - fu) * Math.PI / 2)));
      tag(p, g, { x: 170, y: 52, rot: swing(t, at('y2006') + 0.3, 0.1, 2.5, 8), flip, w: 220, h: 100, text: '2006', size: 70 });
    });
    // the scientist in the caveman mask
    const sx = sciX(t), stepping = t < at('scientist') + 1.0 || (t > WT.uske && t < 23.4) || (t > at('dusra') && t < at('dusra') + 0.5);
    const hop = stepping ? Math.abs(Math.sin(t * 7)) * 10 : 0;
    if (t > at('scientist')) pup(st, {}, (p, g, rods) => person(p, g, { x: sx, y: SCI_Y - hop, s: SCI_S, step: stepping ? t * 7 : 0, arm: 0.12 + (stepping ? Math.sin(t * 7) * 0.2 : 0), mask: 'cave' }, rods));
    // red ring drawn round the mask on "mask"
    if (t > at('mask') && t < WT.uske + 0.3) pup(st, { alpha: 1 - sm(WT.uske, WT.uske + 0.3, t) }, (p, g) => { const [mx, my] = maskPt(sx); ring(p, g, mx, my, 104, EIO(sm(at('mask'), at('mask') + 0.38, t))); });
    // two crows hop in; the net drops over them; leg bands; the net lifts and they fly off
    const crowsIn = EO(sm(at('kuch') - 0.5, at('kuch'), t)), flyU = sm(WT.chhod, WT.chhod + 0.9, t);
    if (t > at('kuch') - 0.5 && flyU < 1) pup(st, {}, (p, g, rods) => {
      [[230, 0], [380, 1]].forEach(([x0, i]) => {
        const band = EO(cl((t - at('tag') - i * 0.12) / 0.16)) * (t > at('tag') + i * 0.12 ? 1 : 0);
        const fy = lerp(692, -260, EIO(flyU)), fx = x0 + 120 * flyU * (i ? 1 : -0.4);
        crow(p, g, { x: lerp(-200 - i * 120, x0, crowsIn) + (fx - x0), y: flyU > 0 ? fy : 692 - Math.abs(Math.sin(crowsIn * Math.PI * 2)) * 14 * (1 - crowsIn), s: 0.72, dir: -1, wing: flyU > 0 ? flapW(t, i) : 0.04, legs: true, band, blink: blinkAt(t, [WT.chot + 0.1 + i * 0.15]), head: t > WT.chot && t < WT.chot + 0.8 ? 0.12 * Math.sin((t - WT.chot) * 8) * (1 - (t - WT.chot) / 0.8) : 0, noRods: flyU > 0.05 }, rods);
      });
    });
    const drop = EO(sm(at('pakde'), at('pakde') + 0.25, t)), lift = EIO(sm(at('chhod'), at('chhod') + 0.45, t));
    if (t > at('pakde') && lift < 1) pup(st, {}, (p) => net(p, { x: 305, y: lerp(-420, 432, drop) - lift * 760 + swing(t, at('pakde') + 0.25, 16, 5, 18) * (1 - lift), w: 360, h: 262, rot: swing(t, at('pakde') + 0.25, 0.03, 3, 9) }));
    // the attack: crows circle the masked head, KAA! bursts
    const nC = t < at('jhund') ? 6 : 9;
    if (t > at('cheekh') && t < SC.twist) {
      const [mx, my] = maskPt(sx), R = lerp(lerp(250, 185, EO(sm(at('jhund'), at('jhund') + 0.6, t))), 150, sm(at('dusra'), at('dusra') + 0.5, t));
      pup(st, {}, (p, g) => {
        for (let k = 0; k < 9; k++) {
          const t0 = (k < 6 ? at('cheekh') + k * 0.1 : at('jhund') + (k - 6) * 0.12), u = EO(sm(t0, t0 + 0.55, t));
          if (u <= 0) continue;
          const gone = k >= 6 ? sm(at('dusra'), at('dusra') + 0.4, t) : 0;
          const a = k / nC * TAU + t * 1.7, ox = mx + Math.cos(a) * R * 1.25, oy = my + Math.sin(a) * R * 0.75;
          const sxk = [-300, 1580, 640, -300, 1580, 640, -300, 1580, 640][k], syk = [80, 120, -200, 520, 480, -200, 300, 300, -200][k];
          const x = lerp(sxk, ox, u), y = lerp(syk, oy, u) - gone * 700;
          crow(p, g, { x, y: y + 60, s: 0.5, dir: Math.cos(a + Math.PI / 2) < 0 ? 1 : -1, wing: flapW(t, k), legs: false, face: 0, eye: EYE_HOT, noRods: true });
        }
      });
      // shout bursts pop one after another
      const KA = [[-1, -0.9], [1.1, -0.7], [-1.25, 0.35], [1.2, 0.5]];
      pup(st, {}, (p, g) => KA.forEach(([kx, ky], i) => {
        const t0 = at('cheekh') + i * 0.34, out = sm(at('dusra') - 0.2, at('dusra') + 0.05, t);
        kaa(p, g, { x: mx + kx * 260, y: my + ky * 200 + 40, s: (t > t0 ? pop(t, t0) : 0) * 0.82 * (1 - out), rot: (i % 2 ? 0.12 : -0.1) + Math.sin(t * 9 + i) * 0.03, seed: 40 + i });
      }));
    }
    // the split: a torn strip drops down the middle; the control mask on the right
    if (t > at('dusra')) {
      pup(st, {}, (p) => divider(p, 640, lerp(0, 740, EO(sm(at('dusra'), at('dusra') + 0.28, t)))));
      const inR = EO(sm(at('dmask') - 0.25, at('dmask') + 0.35, t));
      pup(st, {}, (p, g, rods) => {
        person(p, g, { x: lerp(1500, 960, inR), y: SCI_Y - (inR < 1 ? Math.abs(Math.sin(t * 7)) * 10 : 0), s: SCI_S, step: inR < 1 ? t * 7 : 0, mask: 'plain' }, rods);
        // two calm crows; the near one pecks at the ground
        const peck = Math.max(Math.sin(Math.PI * sm(28.3, 28.6, t)), Math.sin(Math.PI * sm(at('dhyan'), at('dhyan') + 0.3, t)));
        crow(p, g, { x: lerp(1400, 790, EO(sm(27.6, 28.1, t))), y: 692, s: 0.62, dir: 1, head: -0.95 * peck, tilt: -0.15 * peck, blink: blinkAt(t, [29.0]) }, rods);
        crow(p, g, { x: lerp(1500, 1180, EO(sm(27.7, 28.2, t))), y: 692, s: 0.58, dir: 1, head: 0.05 * Math.sin(t * 2), blink: blinkAt(t, [28.7]) }, rods);
      });
      pup(st, {}, (p, g) => {
        const sx1 = pop(t, 27.5, 0.25), sx2 = pop(t, 28.0, 0.25);
        for (const [x, s, ok, t0] of [[480, sx1, false, 27.5], [1150, sx2, true, 28.0]]) {
          if (s <= 0.01) continue;
          const yy = 150 + swing(t, t0 + 0.25, 8, 3, 9);
          p.save(); p.strokeStyle = INK; p.lineWidth = 2; p.beginPath(); p.moveTo(x, yy - 50 * s); p.lineTo(x, -10); p.stroke(); p.restore();
          badge(p, g, { x, y: yy, s: s * 1.25, ok });
        }
      });
    }
  }

  // the twist: one tagged crow teaches the others
  const RING = [[150, 690, -1, 0], [345, 640, -1, 0], [935, 640, 1, 0], [1130, 690, 1, 0], [170, 500, -1, 1], [1110, 500, 1, 1]];
  const C0 = { x: 640, y: 690, s: 0.62 };
  const vineT = (i) => at('kabhi') + i * 0.22;
  function sceneTwist(st, t) {
    // TWIST card drops in, then is hoisted to the corner
    const hp = EIO(sm(31.0, 31.5, t)), out = EIO(sm(WT.aur2 - 0.1, WT.aur2 + 0.3, t));
    pup(st, {}, (p, g) => titleCard(p, g, {
      x: lerp(640, 190, hp), y: lerp(lerp(-240, 260, EO(sm(at('twist'), at('twist') + 0.35, t))), 92, hp) - out * 300, w: 520, h: 170, s: lerp(1, 0.55, hp),
      rot: swing(t, at('twist') + 0.35, 0.08, 2.2, 7) + swing(t, 31.5, 0.05, 2.5, 8),
      lines: [{ text: 'TWIST', size: 92, y: 32 }],
    }));
    const fly = EIO(sm(WT.aur2, WT.aur2 + 0.6, t));
    const glare = sm(at('dushman') + 0.05, at('dushman') + 0.22, t);
    // vines grow out from the tagged crow to the others
    pup(st, { alpha: 1 - sm(WT.aur2 - 0.1, WT.aur2 + 0.25, t) }, (p) => {
      const [x0, y0] = chest(C0.x, C0.y, C0.s, 1);
      RING.forEach(([x, y, d, f], i) => {
        const [x1, y1] = chest(x, y, f ? 0.5 : 0.55, d);
        const P = [[x0, y0 - 20], [lerp(x0, x1, 0.3), y0 - 150 - (f ? 40 : 0)], [lerp(x0, x1, 0.75), y1 - (f ? 40 : 120)], [x1 + (x1 < x0 ? 40 : -40), y1 - 30]];
        vine(p, P, EIO(sm(vineT(i), vineT(i) + 0.4, t)), 6);
      });
    });
    pup(st, {}, (p, g, rods) => {
      RING.forEach(([x, y, d, f], i) => {
        const lit = sm(vineT(i) + 0.38, vineT(i) + 0.48, t), yy = y - fly * (760 + i * 40), xx = x + fly * d * -80;
        const eye = EYE_DIM.map((v, k) => lerp(v, EYE_HOT[k], lit));
        crow(p, g, { x: xx, y: f ? yy + Math.sin(t * 2 + i) * 6 : yy, s: f ? 0.5 : 0.55, dir: d, wing: f || fly > 0 ? flapW(t, i) * (f ? 0.6 : 1) : 0.04, legs: !f && fly === 0, eye, face: glare, glare: glare > 0.5, head: glare < 0.5 ? 0.05 * Math.sin(t * 1.5 + i) : 0, noRods: f || fly > 0, blink: blinkAt(t, [31.2 + i * 0.3]) }, rods);
        // sparks as each crow lights up
        const sp = sm(vineT(i) + 0.4, vineT(i) + 0.9, t);
        if (sp > 0 && sp < 1) { p.fillStyle = INK; const [hx, hy] = chest(x, y, 0.55, d); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + i, dd = 50 + sp * 50; p.save(); p.translate(hx + Math.cos(a) * dd, hy - 40 + Math.sin(a) * dd); p.rotate(sp * 3); star(p, 0, 0, 11 * Math.sin(Math.PI * sp)); p.restore(); } }
      });
      crow(p, g, { ...C0, y: C0.y - fly * 760, band: 1, eye: EYE_HOT, face: glare, glare: glare > 0.5, wing: fly > 0 ? flapW(t, 9) : 0.04 + 0.03 * Math.sin(t * 2), legs: fly === 0, noRods: fly > 0, head: glare < 0.5 ? -0.05 + 0.04 * Math.sin(t * 1.3) : 0 }, rods);
    });
    // SIKHA DIYA
    if (t > at('sikha')) {
      const u = cl((t - at('sikha')) / 0.12), lift = EIO(sm(WT.aur2 - 0.1, WT.aur2 + 0.3, t));
      pup(st, {}, (p, g) => { stamp(p, g, { x: 640, y: 372 - lift * 600, rot: 0.04, s: lerp(1.5, 1, EO(u)) + swing(t, at('sikha') + 0.12, 0.05, 6, 30), text: 'SIKHA DIYA', size: 90 }); crumbs(p, 640, 380, (t - at('sikha') - 0.1) / 0.6, 31, 360); });
    }
    // the enemy: the caveman mask drops in on its string; later it drifts back behind the counter and fades
    if (t > at('dushman')) {
      const dropY = lerp(-140, 170, EO(sm(at('dushman'), at('dushman') + 0.3, t))), back = EIO(sm(WT.aur2, 41.0, t));
      pup(st, { blur: 0.5 + 9 * back, alpha: 1 - 0.72 * back }, (p, g) => {
        g.globalAlpha = 1 - 0.85 * back; g.filter = `blur(${0.5 + 9 * back}px)`;   // the gels go soft and faint with it
        const y = lerp(dropY, 330, back), s = lerp(0.82, 2.3, back), rot = swing(t, at('dushman') + 0.3, 0.12, 2.5, 7);
        p.save(); p.strokeStyle = INK; p.lineWidth = 2; p.beginPath(); p.moveTo(640, y - 110 * s); p.lineTo(640, -10); p.stroke(); p.restore();
        mask(p, g, { x: 640, y, s, rot, kind: 'cave' });
      });
    }
    // 15+ years: the counter board drops and rolls the years
    if (t > WT.aur2) {
      const dy = lerp(-360, 0, EO(sm(WT.aur2, WT.aur2 + 0.35, t))) - 900 * sm(40.85, 41.2, t);
      const yr = Math.round(2006 + 15 * EO(sm(at('nafrat'), at('fifteen') - 0.05, t)));
      const landed = t >= at('fifteen'), hit = landed ? Math.exp(-(t - at('fifteen')) * 7) : 0;
      pup(st, {}, (p) => {
        board(p, 640, 470 + dy, swing(t, WT.aur2 + 0.35, 0.03, 2.5, 7) + swing(t, at('fifteen'), 0.03, 3, 10), landed ? '15+' : String(yr), landed ? 190 : 150, 1 + 0.16 * hit);
        if (landed) {
          vine(p, [[470, 520 + dy], [560, 560 + dy], [720, 500 + dy], [820, 528 + dy]], EIO(sm(at('zyada'), at('zyada') + 0.35, t)), 7);
          plaque(p, { x: 1000, y: lerp(-80, 420, EO(sm(at('fifteen'), at('fifteen') + 0.25, t))) + dy, text: 'SAAL', size: 60, rot: swing(t, at('fifteen') + 0.25, 0.07, 3, 9), hang: 420 });
          plaque(p, { x: 640, y: lerp(-80, 150, EO(sm(at('fifteen') + 0.1, at('fifteen') + 0.35, t))) + dy * 0.3, text: '2006 → 2021+', size: 36, rot: swing(t, at('fifteen') + 0.35, 0.05, 3, 9), hang: 120 });
        }
      });
    }
  }
  // transition: a crow flies at the lamp until its shadow covers the screen (after the reference's owl)
  function flyOver(st, t) {
    const q = sm(40.85, 41.55, t);
    const s = lerp(0.7, 9, Math.pow(q, 1.2));
    const cx = lerp(980, 700, EIO(sm(0, 0.5, q))) + 500 * sm(0.5, 1, q) * sm(0.5, 1, q), cy = lerp(640, 420, EIO(sm(0, 0.5, q))) + 400 * s * 0.25;
    pup(st, { blur: 1 + 26 * q, alpha: 1 - 0.1 * q }, (p, g) => {
      g.filter = `blur(${1 + 26 * q}px)`; g.globalAlpha = 1 - q;
      crow(p, g, { x: cx, y: cy, s, wing: 0.4 + 0.9 * flapW(t, 3), legs: false, noRods: true, eye: EYE_HOT });
    });
    const cover = sm(0.25, 0.42, q) * (1 - sm(0.5, 0.72, q));
    if (cover > 0) { const s2 = st.S.getContext('2d'); s2.save(); s2.globalAlpha = cover * 0.93; s2.fillStyle = INK; s2.fillRect(0, 0, st.W, st.Hh); s2.restore(); }
  }

  // the dead-crow gathering
  const GATHER = [[300, 692, -1, 0.58], [445, 662, -1, 0.5], [980, 662, 1, 0.5], [1125, 692, 1, 0.58], [175, 648, -1, 0.4]];
  function sceneDead(st, t) {
    pup(st, {}, (p, g) => tag(p, g, { x: 170, y: 52, rot: swing(t, SC.dead + 0.2, 0.1, 2.5, 8), flip: Math.max(0.04, sm(SC.dead, SC.dead + 0.3, t)), w: 220, h: 100, text: '2015', size: 70 }));
    // the still crow is brought to the screen from far back (soft -> sharp)
    const near = sm(at('mar'), at('mar') + 0.6, t);
    // lying on its back, feet curled up, eyes closed
    if (near > 0) pup(st, { blur: 0.6 + 16 * (1 - near), alpha: near }, (p, g) => {
      g.globalAlpha = near;
      crow(p, g, { x: 610, y: 692 - 104, s: 0.7, tilt: 2.55, head: 0.35, wing: -0.05, blink: 1, eye: [90, 50, 30], noRods: true });
    });
    // crows come down one by one and stand round it, heads low
    pup(st, {}, (p, g, rods) => GATHER.forEach(([x, y, d, s], i) => {
      const t0 = at('jama') + i * 0.38, u = EO(sm(t0, t0 + 0.45, t));
      if (u <= 0) return;
      crow(p, g, { x, y: lerp(-200, y, u), s, dir: d, wing: u < 1 ? flapW(t, i) : 0.03, legs: u > 0.7, head: -0.28 * sm(t0 + 0.5, t0 + 1.2, t), blink: blinkAt(t, [48.5 + i * 0.4]), eye: [200, 120, 60], noRods: i === 4 }, rods);
    }));
    // khatra kahan hai: a map pin drops on the spot
    if (t > at('khatra')) pup(st, {}, (p, g) => mapPin(p, g, { x: 640, y: lerp(-100, 560, EO(sm(at('khatra'), at('khatra') + 0.22, t))) - Math.abs(swing(t, at('khatra') + 0.22, 18, 6, 16)), s: 1.15 }));
    // aur kaun hai: a faint person at the edge, tagged with a red question mark
    if (t > at('kaun')) {
      const u = sm(at('kaun'), at('kaun') + 0.35, t);
      pup(st, { blur: 3.5, alpha: 0.72 * u }, (p, g) => person(p, g, { x: 1240, y: 692, s: 0.95, noRods: true }));
      pup(st, {}, (p, g) => gelTag(p, g, { x: 1105, y: lerp(-160, 120, EO(sm(at('kaun') + 0.05, at('kaun') + 0.3, t))), rot: swing(t, at('kaun') + 0.3, 0.12, 2.5, 8), w: 100, h: 110, text: '?', size: 84 }, RED));
    }
  }

  // the ending: back to the big crow, it tilts its head; push in on its eye; the closing question
  function sceneEnd(st, t) {
    const zoom = 1 + 0.8 * EIO(sm(at('wo'), 56.6, t));
    const back = sm(at('shehar'), at('shehar') + 0.5, t);
    const E = [BIG.x - 68 * BIG.s, BIG.y - 168 * BIG.s];
    pup(st, { blur: 0.4 + 5 * back, alpha: 1 - 0.55 * back }, (p, g, rods) => {
      g.globalAlpha = 1 - 0.75 * back; g.filter = `blur(${0.4 + 5 * back}px)`;
      both([p, g], (c) => { c.save(); c.translate(E[0], E[1]); c.scale(zoom, zoom); c.translate(-E[0], -E[1]); });
      crow(p, g, { ...BIG, y: BIG.y + Math.sin(t * 1.3) * 4, head: 0.24 * EIO(sm(51.5, 52.4, t)) + 0.03 * Math.sin(t), eye: [255, 196, 90], blink: blinkAt(t, [53.6, 58.4]), wing: 0.03, noRods: zoom > 1.01 }, zoom > 1.01 ? null : rods);
      both([p, g], (c) => c.restore());
    });
    // folded hands pop in beside it, then lift away for the line
    const nm = t > at('izzat') ? pop(t, at('izzat'), 0.26) : 0, nmOut = EIO(sm(at('wo') - 0.2, at('wo') + 0.15, t));
    if (nm > 0 && nmOut < 1) pup(st, {}, (p, g) => {
      const y = 400 - nmOut * 600;
      p.save(); p.strokeStyle = INK; p.lineWidth = 2; p.beginPath(); p.moveTo(960, y - 80 * nm); p.lineTo(960, -10); p.stroke(); p.restore();
      namaste(p, g, { x: 960, y, s: nm * 1.15, rot: swing(t, at('izzat') + 0.26, 0.1, 2.5, 8) });
    });
    // WOH DEKH RAHA HAI types onto a hanging card; an eye charm swings below it
    if (t > at('wo')) {
      const full = 'WOH DEKH RAHA HAI', n = Math.round(full.length * cl((t - WT.wo) / 0.95));
      pup(st, {}, (p, g) => {
        titleCard(p, g, { x: 800, y: lerp(-200, 170, EO(sm(at('wo'), at('wo') + 0.3, t))), w: 840, h: 150, s: 1, rot: swing(t, at('wo') + 0.3, 0.04, 2.2, 6), lines: [{ text: full.slice(0, n) + ' '.repeat(full.length - n), size: 66, y: 24 }] });
        if (t > WT.wo + 1.0) eyeCharm(p, g, { x: 1120, y: lerp(-80, 330, EO(sm(WT.wo + 1.0, WT.wo + 1.3, t))), rot: swing(t, WT.wo + 1.3, 0.12, 2.2, 7), hang: 120 });
      });
    }
    // the closing question rises from below and keeps bobbing
    if (t > at('shehar')) pup(st, {}, (p, g, rods) => {
      const u = H.ease.back(cl((t - at('shehar')) / 0.45)), y = lerp(900, 560, u) + (t > WT.shehar + 0.4 ? Math.sin((t - WT.shehar - 0.4) * 4) * 6 : 0);
      bubble(p, g, { x: 820, y, rot: swing(t, at('shehar') + 0.45, 0.04, 1.2, 6) });
      rods.push([700, y + 88, 3.4]);
    });
  }

  function explainerFrame(ctx, W, Hh, t) {
    const st = begin(W, Hh);
    let b = sm(0, 0.55, t) * (1 - 0.35 * Math.max(0, NZ.n2(t * 23, 3.3)) * (1 - sm(0.35, 0.7, t)));
    b *= t < SC.twist ? 1 : t < SC.dead ? 0.74 : t < SC.end ? 0.6 : 1.04;     // darker for the twist, muted for the dead crow
    b *= 1 - 0.93 * Math.max(dip(t, SC.research), dip(t, SC.end));          // the lamp is turned down and up again
    const flare = t > at('fifteen') ? Math.exp(-(t - at('fifteen')) * 3) * 0.32 : 0;  // 15+: the flame flares
    // the screen shakes once on "pareshan"
    const sh = t > at('pareshan') ? Math.exp(-(t - at('pareshan')) * 14) * Math.sin((t - at('pareshan')) * 70) * 9 : 0;
    ctx.save();
    if (Math.abs(sh) > 0.05) { ctx.translate(W / 2 + sh, Hh / 2 + sh * 0.4); ctx.scale(1.02, 1.02); ctx.translate(-W / 2, -Hh / 2); }
    lamp(ctx, W, Hh, t, b + flare * 0.3, flare);
    if (t < SC.research) sceneHook(st, t);
    else if (t < SC.twist) sceneStage(st, t);
    else if (t < SC.dead) sceneTwist(st, t);
    else if (t < SC.end) sceneDead(st, t);
    else sceneEnd(st, t);
    if (t > 40.8 && t < 41.6) flyOver(st, t);
    stage(st, t);
    // soft near-lamp fern for depth on the open stages
    if (t > SC.research && t < SC.twist) nearFern(st, t, -1, 0.7);
    else if (t > SC.dead && t < SC.end) nearFern(st, t, 1, 0.6);
    // lace curtains close and part for the twist
    const cover = EIO(sm(29.9, 30.2, t)) * (1 - EIO(sm(30.35, 30.7, t)));
    if (cover > 0.001) pup(st, {}, (p) => curtains(p, W, Hh, cover, t));
    end(ctx, st, t);
    // the gathering: the vignette slowly closes in
    if (t > SC.dead && t < SC.end) H.vignette(ctx, W, Hh, 0.55 * sm(at('jama'), 49.0, t), '10,3,1');
    ctx.restore();
  }
