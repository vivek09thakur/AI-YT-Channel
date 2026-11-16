  
  const TITLE = 'RAMAYAN';
  const HOOK = ['The greatest story', 'ever told.'];
  const REEL_SUBTITLE = 'A 2 minute trailer';

  const SC = { dawn: 8.2, ayodhya: 18.0, rama: 24.2, exile: 36.4, walk: 48.2, ravana: 58.0, dharma: 76.4, forest: 85.0, shore: 87.4, leap: 90.0, lanka: 92.6, army: 95.4, battle: 103.5, title: 113.6 };
  const FADE = 0.9;
  const REEL_FOCUS = {
    open: [640, 400],
    dawn: (t) => [lerp(360 + (t - SC.dawn) * 14, 1000, EIO(sm(13.4, 14.8, t))), 420],
    ayodhya: [640, 420],
    rama: [640, 440],
    exile: (t) => [560 + EIO(sm(44.7, 48.2, t)) * 240, 430],
    walk: [620, 430],
    ravana: [640, 420],
    dharma: (t) => [lerp(500, 760, EIO(sm(80.6, 82.0, t))), 400],
    forest: [540, 430],
    shore: [340, 430],
    leap: (t) => [cl(lerp(-150, 1250, cl((t - SC.leap) / (SC.lanka - SC.leap + 0.6))), 200, 1080), 360],
    lanka: [640, 380],
    army: (t) => [lerp(300, 640, EIO(sm(97.4, 99.4, t))), 450],
    battle: (t) => [lerp(420, 880, EIO(sm(111.5, 111.95, t))), 430],
    title: [640, 470],
  };
  const BEATS = [
    { n: 1, name: 'Before time', t0: 0, t1: SC.dawn, vo: 'Before the beginning of time as we know it... Before the greatest war ever witnessed...', screen: 'Night sky, a sun under the hills, spears rising' },
    { n: 2, name: 'A world of gods and mortals', t0: SC.dawn, t1: SC.ayodhya, vo: 'There existed a world where gods walked among mortals, where destiny shaped kingdoms, and where the eternal battle between Dharma and Adharma was about to begin.', screen: 'Sunrise, a god and a mortal walk, a shadow waits' },
    { n: 3, name: 'Ayodhya', t0: SC.ayodhya, t1: SC.rama, vo: 'In the magnificent kingdom of Ayodhya... A prince was born.', screen: 'The pavilion temple, elephants, a lotus of light' },
    { n: 4, name: 'Rama', t0: SC.rama, t1: SC.exile, vo: 'A prince whose name would echo through eternity. Rama. The son of Dasharatha. The protector of the innocent. The embodiment of righteousness.', screen: 'RAMA · hero with bow before the sun' },
    { n: 5, name: 'Exile', t0: SC.exile, t1: SC.walk, vo: 'But destiny does not always follow the path of happiness. A crown was taken away. A kingdom was left behind. And a prince willingly embraced fourteen years of exile.', screen: 'The crown lifts away, the palace recedes, the forest arrives' },
    { n: 6, name: 'Sita and Lakshmana', t0: SC.walk, t1: SC.ravana, vo: 'Alongside him walked Sita... The embodiment of strength and devotion. And Lakshmana... Whose loyalty knew no boundaries.', screen: 'Three walk through the forest' },
    { n: 7, name: 'Ravana', t0: SC.ravana, t1: SC.dharma, vo: 'Deep within the forests... A darkness was awakening. The mighty Ravana. King of Lanka. A conqueror feared by gods and mortals alike. His pride would challenge the heavens. His actions would ignite a war that would shake the foundations of the universe.', screen: 'RAVANA · ten heads rise, golden Lanka, lightning' },
    { n: 8, name: 'Dharma', t0: SC.dharma, t1: SC.forest, vo: 'But he had underestimated one thing. The power of Dharma. The power of devotion. And the strength of a promise.', screen: 'Rama draws the bow, Hanuman kneels, Sita in a ring of gold' },
    { n: 9, name: 'The journey', t0: SC.forest, t1: SC.army, vo: "From the forests of Panchavati... To the shores of the mighty ocean... From Hanuman's legendary leap... To the burning skies of Lanka...", screen: 'Forest · shore · the leap · Lanka burns' },
    { n: 10, name: 'The army and the bridge', t0: SC.army, t1: SC.battle, vo: 'An army would rise. A bridge would be built across the impossible. And the greatest battle of all time would begin.', screen: 'Vanaras march, the bridge grows, arrows fill the sky' },
    { n: 11, name: 'One arrow', t0: SC.battle, t1: SC.title, vo: 'When darkness threatens the world... When evil believes itself invincible... When Dharma stands against Adharma... One warrior will rise. One arrow will change everything.', screen: 'Rama vs Ravana, split sky, the arrow' },
    { n: 12, name: 'Title', t0: SC.title, t1: DURATION, vo: 'And one name... Will become eternal. RAMAYAN. The story of a prince. The journey of a god. And the eternal victory of Dharma.', screen: 'RAMAYAN over the temple at sunrise' },
  ];

  function sceneCosmos(c, W, Hh, t) {
    const u = sm(0, SC.dawn, t);
    c.save(); cam(c, W, Hh, 0.06 * u);
    sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.8 * (1 - u * 0.5));
    streaks(c, W, Hh, t, { color: PAL.lotus, alpha: 0.12, seed: 2, n: 60 });
    sun(c, 640, 600 - u * 30, 110, PAL.kesari, 4);
    cloudBank(c, W, 300, t, { seed: 3, n: 4, fill: H.rgba(PAL.maroon, 0.9), line: H.rgba(PAL.night, 0.6), speed: 4 });
    hills(c, W, Hh, 540, 90, PAL.maroon, 1); hills(c, W, Hh, 600, 70, PAL.deep, 2);
    
    const r = H.rng(8), w = fade(t, 4.4, 2.2);
    c.strokeStyle = PAL.ink; c.fillStyle = PAL.ink; c.lineWidth = 3;
    for (let i = 0; i < 46; i++) { const x = 20 + r() * (W - 40), h = (70 + r() * 120) * EO(cl(w * 1.4 - r() * 0.4)), y0 = 650 - 40 * Math.sin(x * 0.004 + 2); if (h < 2) continue; c.beginPath(); c.moveTo(x, y0); c.lineTo(x, y0 - h); c.stroke(); c.beginPath(); c.moveTo(x - 6, y0 - h); c.lineTo(x, y0 - h - 22); c.lineTo(x + 6, y0 - h); c.closePath(); c.fill(); if (i % 5 === 0) { c.fillStyle = PAL.kumkum; c.beginPath(); c.moveTo(x, y0 - h + 2); c.lineTo(x + 26, y0 - h + 10); c.lineTo(x, y0 - h + 20); c.closePath(); c.fill(); c.fillStyle = PAL.ink; } }
    hills(c, W, Hh, 680, 40, PAL.ink, 3);
    c.restore();
  }
  
  function sceneDawn(c, W, Hh, t) {
    const u = sm(SC.dawn, SC.dawn + 7, t), tt = t - SC.dawn;
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.dawn, SC.ayodhya, t));
    sky(c, W, Hh, mixStops(NIGHT, WARM, u)); stars(c, W, Hh, t, 0.6 * (1 - u));
    streaks(c, W, Hh, t, { alpha: 0.2 * u + 0.06, seed: 5 });
    sun(c, 640, lerp(600, 330, EO(u)), 120, PAL.turmeric, 3.2);
    rays(c, 640, lerp(600, 330, EO(u)), 130, 700, 24, PAL.cream, t, 0.12 * u);
    cloudBank(c, W, 250, t, { seed: 4, n: 5, fill: mixc(PAL.maroon, PAL.sandal, u * 0.85), line: mixc(PAL.night, PAL.saffron, u), speed: 5, spread: 120 });
    skyline(c, 640, 560, 0.55, mixc(PAL.indigo, PAL.burnt, u * 0.8), t);
    hills(c, W, Hh, 560, 60, mixc(PAL.maroon, PAL.burnt, u), 4); hills(c, W, Hh, 620, 70, mixc(PAL.deep, PAL.brown, u), 5);
    
    const a = fade(t, 8.4, 1.0), gx = 300 + tt * 14;
    if (a > 0) {
      c.save(); c.globalAlpha = a;
      figure(c, { x: gx, y: 650, s: 0.62, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', pose: 'walk', ph: tt * 1.3, glow: PAL.turmeric, tilak: true });
      figure(c, { x: gx - 95, y: 652, s: 0.58, dir: 1, skin: PAL.sandal, cloth: PAL.cream, sash: PAL.burnt, crown: 'bun', pose: 'walk', ph: tt * 1.3 + 0.5 });
      c.restore();
    }
    
    const dk = EO(fade(t, 13.8, 1.4));
    if (dk > 0) {
      const g = c.createLinearGradient(W * 0.5, 0, W, 0); g.addColorStop(0, H.rgba(PAL.night, 0)); g.addColorStop(1, H.rgba(PAL.night, 0.55 * dk)); c.fillStyle = g; c.fillRect(0, 0, W, Hh);
      figure(c, { x: 1040, y: 652 + (1 - dk) * 160, s: 0.75, dir: -1, skin: PAL.ink, cloth: PAL.maroon, sash: PAL.kumkum, crown: 'king', hair: PAL.ink, eyeCol: PAL.kumkum, arms: [[-1.2, -1.2], [0.4, 0.6]] });
    }
    hills(c, W, Hh, 690, 30, PAL.deep, 6);
    c.restore();
  }
  
  function sceneAyodhya(c, W, Hh, t) {
    const tt = t - SC.ayodhya;
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.ayodhya, SC.rama, t), 0, 20);
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 7 });
    sun(c, 640, 250, 100, PAL.turmeric, 3);
    cloudBank(c, W, 190, t, { seed: 11, n: 6, fill: PAL.sandal, line: PAL.saffron, speed: 6, spread: 140 });
    skyline(c, 200, 520, 0.45, mixc(PAL.brown, PAL.saffron, 0.45), t); skyline(c, 1080, 520, 0.45, mixc(PAL.brown, PAL.saffron, 0.45), t);
    hills(c, W, Hh, 540, 50, mixc(PAL.brown, PAL.saffron, 0.3), 7);
    
    const b = pop(t, 21.5, 0.9);
    if (b > 0) { rays(c, 640, 430, 40, 420 * b, 20, PAL.cream, t, 0.4 * b); sun(c, 640, 440, 22 * b, PAL.cream, 5); lotus(c, 640, 470, 1.3 * b, PAL.lotus, PAL.cream); }
    temple(c, { x: 640, y: 560, s: 0.78, col: PAL.brown }, t);
    
    figure(c, { x: 500, y: 560, s: 0.62, dir: 1, skin: PAL.sandal, cloth: PAL.kumkum, sash: PAL.gold, crown: 'king', pose: 'namaste' });
    figure(c, { x: 790, y: 560, s: 0.58, dir: -1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'namaste' });
    elephant(c, 150 + tt * 4, 630, 0.5, 1, PAL.deep, t); elephant(c, 1130 - tt * 4, 630, 0.5, -1, PAL.deep, t);
    [-410, 410].forEach((dx, i) => flag(c, 640 + dx, 560, 150, i ? PAL.saffron : PAL.kumkum, t, i ? -1 : 1));
    hills(c, W, Hh, 660, 30, PAL.deep, 8);
    c.restore();
  }
  
  function sceneRama(c, W, Hh, t) {
    const tt = t - SC.rama;
    c.save(); cam(c, W, Hh, 0.08 * sm(SC.rama, SC.exile, t), 0, 40);
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 13 });
    rays(c, 640, 330, 150, 760, 28, PAL.turmeric, t, 0.3);
    sun(c, 640, 330, 160, PAL.turmeric, 2.6);
    cloudBank(c, W, 520, t, { seed: 14, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5, spread: 60 });
    hills(c, W, Hh, 600, 60, mixc(PAL.brown, PAL.saffron, 0.35), 9); hills(c, W, Hh, 660, 40, PAL.brown, 10);
    const kn = EO(fade(t, 32.3, 0.8));
    if (kn > 0) { figure(c, { x: 330, y: 700, s: 0.7 * kn, dir: 1, skin: PAL.sandal, cloth: PAL.cream, sash: PAL.burnt, crown: 'bun', pose: 'kneel' }); figure(c, { x: 950, y: 700, s: 0.7 * kn, dir: -1, skin: PAL.sandal, cloth: PAL.cream, sash: PAL.tulsi, crown: 'long', face: 'woman', pose: 'kneel' }); }
    const lo = pop(t, 34.3, 0.7);
    if (lo > 0) [220, 420, 860, 1060].forEach((x, i) => lotus(c, x, 712, 0.9 * lo, PAL.lotus, PAL.cream));
    figure(c, { x: 640, y: 700, s: 1.45, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', bow: true, tilak: true, pose: 'stand', arms: [[-0.55, 0.3], [0.35, 0.8]] });
    hills(c, W, Hh, 712, 16, PAL.deep, 11);
    c.restore();
  }
  
  function sceneExile(c, W, Hh, t) {
    const u = sm(SC.exile, SC.walk, t), tt = t - SC.exile;
    c.save(); cam(c, W, Hh, 0.04 * u);
    sky(c, W, Hh, mixStops(WARM, DUSK, u)); streaks(c, W, Hh, t, { seed: 17, alpha: 0.18 });
    sun(c, 980, lerp(260, 420, u), 90, PAL.marigold, 3);
    cloudBank(c, W, 230, t, { seed: 18, n: 5, fill: mixc(PAL.sandal, PAL.burnt, u * 0.5), line: PAL.saffron, speed: 6, spread: 120 });
    hills(c, W, Hh, 560, 50, mixc(PAL.brown, PAL.saffron, 0.35 - u * 0.2), 12);
    const slide = EIO(sm(42.4, 45.5, t)) * 760;
    temple(c, { x: 300 - slide, y: 600, s: 0.5, col: PAL.brown }, t);
    flag(c, 300 - slide - 165, 600, 90, PAL.saffron, t, 1); flag(c, 300 - slide + 165, 600, 90, PAL.kumkum, t, -1);
    
    const fin = EIO(sm(44.6, 47.6, t)) * 620, r = H.rng(20);
    for (let i = 0; i < 7; i++) tree(c, 1400 - fin + i * 110 + r() * 40, 650 + r() * 20, 1.0 + r() * 0.4, i % 2 ? PAL.tulsi : mixc(PAL.tulsi, PAL.deep, 0.45), { palm: i % 3 === 0 });
    hills(c, W, Hh, 660, 30, PAL.brown, 13);
    
    const crownOff = t >= 40.1, walk = sm(44.7, 45.3, t), x = 560 + EIO(sm(44.7, 48.2, t)) * 240;
    figure(c, { x, y: 690, s: 1.05, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: crownOff ? 'bun' : 'tall', bow: true, tilak: true, pose: walk > 0 ? 'walk' : 'stand', ph: (t - 44.7) * 1.3, arms: walk > 0 ? null : [[-0.45, 0.3], [0.3, 0.8]] });
    if (crownOff && t < 44) { const k = EO(fade(t, 40.1, 2.2)); c.save(); c.globalAlpha = 1 - sm(42.2, 44, t); crownOnly(c, x, 690 - 1.05 * 236 - k * 260, 1.05, k * 0.6); c.restore(); }
    hills(c, W, Hh, 700, 14, PAL.deep, 14);
    c.restore();
  }
  
  function sceneWalk(c, W, Hh, t) {
    const tt = t - SC.walk;
    c.save(); cam(c, W, Hh, 0.03 * sm(SC.walk, SC.ravana, t));
    sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 21, alpha: 0.16 });
    sun(c, 640, 300, 110, PAL.marigold, 3);
    cloudBank(c, W, 260, t, { seed: 22, n: 5, fill: mixc(PAL.sandal, PAL.burnt, 0.35), line: PAL.burnt, speed: 7, spread: 100 });
    hills(c, W, Hh, 480, 80, mixc(PAL.tulsi, PAL.saffron, 0.4), 15, tt * 10);
    const r = H.rng(23), layer = (sp, y, s, col, n, palm) => { const span = W + 400; for (let i = 0; i < n; i++) { const bx = r() * span, x = ((bx - tt * sp) % span + span) % span - 200; tree(c, x, y + r() * 16, s * (0.9 + r() * 0.3), col, { palm: palm && i % 3 === 0 }); } };
    layer(18, 560, 0.7, mixc(PAL.tulsi, PAL.saffron, 0.2), 9, false);
    hills(c, W, Hh, 590, 30, PAL.tulsi, 16, tt * 25);
    layer(36, 640, 1.0, mixc(PAL.tulsi, PAL.deep, 0.35), 8, true);
    c.fillStyle = PAL.brown; c.fillRect(0, 660, W, 60);
    const ph = tt * 1.35, sita = 0.5 + 0.5 * Math.sin(Math.PI * sm(48.4, 49.2, t)) * (t < 53.6 ? 1 : 0), lak = t > 53.6 ? 1 : 0;
    figure(c, { x: 440, y: 668, s: 0.95, dir: 1, skin: PAL.burnt, cloth: PAL.kumkum, sash: PAL.gold, crown: 'bun', bow: true, pose: 'walk', ph: ph + 0.3, glow: lak ? PAL.vermilion : null, tilak: true });
    figure(c, { x: 610, y: 668, s: 0.9, dir: 1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'walk', ph: ph + 0.6, glow: t > 48.4 && t < 53.6 ? PAL.turmeric : null });
    figure(c, { x: 790, y: 668, s: 0.98, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', bow: true, pose: 'walk', ph, tilak: true });
    void sita;
    layer(80, 735, 1.25, PAL.deep, 5, false);
    ocean(c, W, Hh, 690, t, [PAL.peacock, mixc(PAL.peacock, PAL.cream, 0.2), mixc(PAL.peacock, PAL.cream, 0.38)]);
    c.restore();
  }
  
  function sceneRavana(c, W, Hh, t) {
    const tt = t - SC.ravana;
    const fl = Math.max(Math.exp(-Math.max(0, t - 69.9) * 5) * (t > 69.9 ? 1 : 0), Math.exp(-Math.max(0, t - 72.4) * 5) * (t > 72.4 ? 1 : 0));
    const shake = t > 72.4 ? Math.exp(-(t - 72.4) * 1.6) * Math.sin((t - 72.4) * 40) * 10 : 0;
    c.save(); cam(c, W, Hh, 0.06 * sm(SC.ravana, SC.dharma, t), shake, shake * 0.5);
    sky(c, W, Hh, [[0, PAL.night], [0.5, PAL.maroon], [0.85, PAL.vermilion], [1, PAL.burnt]]);
    streaks(c, W, Hh, t, { color: PAL.lotus, alpha: 0.14, seed: 24, n: 70 });
    sun(c, 640, 400, 90, PAL.vermilion, 3);
    cloudBank(c, W, 200, t, { seed: 25, n: 6, fill: PAL.maroon, line: PAL.night, speed: 9, spread: 140 });
    
    const lk = EO(fade(t, 65.2, 1.4));
    if (lk > 0) { c.save(); c.globalAlpha = lk; sun(c, 1000, 520, 20, PAL.gold, 12); skyline(c, 1000, 520, 0.42, PAL.gold, t); c.restore(); }
    ocean(c, W, Hh, 520, t, [PAL.indigo, mixc(PAL.indigo, PAL.maroon, 0.4), mixc(PAL.indigo, PAL.maroon, 0.7)]);
    hills(c, W, Hh, 600, 50, PAL.deep, 17);
    
    const rise = EO(fade(t, 62.9, 2.0)), ry = 700 + (1 - rise) * 520 + Math.sin(t * 1.2) * 3;
    if (rise > 0) ravana(c, { x: 640, y: ry, s: 1.3, dir: -1, mace: t > 66 });
    
    const r = H.rng(26);
    for (let i = 0; i < 10; i++) tree(c, 40 + i * 135 + r() * 50, 720 + r() * 10, 1.3 + r() * 0.5, PAL.ink, { palm: i % 4 === 1 });
    const ey = fade(t, 60.6, 1.0);
    if (ey > 0 && t < 64) { c.save(); c.globalAlpha = ey * (1 - sm(62.9, 64, t)); c.fillStyle = PAL.kumkum; c.shadowColor = PAL.vermilion; c.shadowBlur = 14; for (let i = 0; i < 7; i++) { const x = 100 + r() * 1080, y = 560 + r() * 110, bl = Math.sin(t * 3 + i) > 0.9 ? 0.2 : 1; c.beginPath(); c.ellipse(x, y, 7, 3.2 * bl, 0, 0, TAU); c.fill(); c.beginPath(); c.ellipse(x + 20, y, 7, 3.2 * bl, 0, 0, TAU); c.fill(); } c.restore(); }
    const fire = fade(t, 72.4, 2.0);
    if (fire > 0) { flames(c, 160, 730, 1.4 * fire, t, 1, 7); flames(c, 1120, 730, 1.4 * fire, t, 2, 7); }
    if (fl > 0.02) { bolt(c, t > 72.4 ? 900 : 360, 0, 420, t > 72.4 ? 31 : 30); c.fillStyle = H.rgba(PAL.cream, fl * 0.55); c.fillRect(0, 0, W, Hh); }
    c.restore();
  }
  
  function sceneDharma(c, W, Hh, t) {
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.dharma, SC.forest, t));
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 27 });
    rays(c, 420, 300, 100, 900, 32, PAL.turmeric, t, 0.25 * fade(t, 79.1, 0.8) + 0.1);
    sun(c, 420, 300, 140, PAL.turmeric, 2.6);
    cloudBank(c, W, 560, t, { seed: 28, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5, spread: 60 });
    hills(c, W, Hh, 640, 50, mixc(PAL.brown, PAL.saffron, 0.35), 18);
    const pr = pop(t, 82.7, 0.8);
    if (pr > 0) { c.save(); c.translate(1040, 230); c.scale(pr, pr); c.strokeStyle = PAL.gold; c.lineWidth = 10; c.beginPath(); c.arc(0, 0, 120, 0, TAU); c.stroke(); c.fillStyle = H.rgba(PAL.cream, 0.5); c.beginPath(); c.arc(0, 0, 115, 0, TAU); c.fill(); lotus(c, 0, 96, 0.9, PAL.lotus, PAL.cream); figure(c, { x: 0, y: 96, s: 0.6, dir: -1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'namaste' }); c.restore(); }
    const dr = EO(fade(t, 76.8, 2.4));
    figure(c, { x: 480, y: 960, s: 2.3, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', bow: true, draw: dr, pose: 'aim', tilak: true });
    const hk = EO(fade(t, 80.9, 1.0));
    if (hk > 0) figure(c, { x: 1010, y: 700, s: 1.05 * hk, dir: -1, skin: PAL.kesari, cloth: PAL.kumkum, sash: PAL.gold, crown: 'cap', face: 'monkey', pose: 'kneel', tail: true, glow: PAL.turmeric });
    hills(c, W, Hh, 706, 16, PAL.deep, 19);
    c.restore();
  }
  
  function sceneForest(c, W, Hh, t) {
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.forest, SC.shore, t));
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 29 });
    sun(c, 900, 220, 90, PAL.turmeric, 3);
    hills(c, W, Hh, 480, 90, mixc(PAL.tulsi, PAL.saffron, 0.45), 20);
    const r = H.rng(30);
    for (let i = 0; i < 9; i++) tree(c, 30 + i * 150 + r() * 60, 600 + r() * 20, 0.9 + r() * 0.4, mixc(PAL.tulsi, PAL.saffron, 0.15), { palm: i % 3 === 1 });
    hills(c, W, Hh, 620, 30, PAL.tulsi, 21);
    
    c.fillStyle = PAL.brown; c.fillRect(540, 560, 14, 110); c.fillRect(720, 560, 14, 110); c.fillStyle = PAL.sandal; c.beginPath(); c.moveTo(500, 580); c.lineTo(640, 470); c.lineTo(780, 580); c.closePath(); c.fill(); c.fillStyle = PAL.burnt; c.fillRect(500, 578, 280, 10);
    figure(c, { x: 660, y: 670, s: 0.75, dir: -1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'stand' });
    figure(c, { x: 420, y: 680, s: 0.8, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', bow: true, tilak: true });
    for (let i = 0; i < 4; i++) tree(c, 60 + i * 400 + r() * 80, 740, 1.4, PAL.deep, { palm: i % 2 === 0 });
    c.fillStyle = PAL.deep; c.fillRect(0, 690, W, 40);
    c.restore();
  }
  
  function sceneShore(c, W, Hh, t) {
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.shore, SC.leap, t));
    sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 31, alpha: 0.16 });
    sun(c, 900, 330, 110, PAL.marigold, 3);
    cloudBank(c, W, 250, t, { seed: 32, n: 5, fill: mixc(PAL.sandal, PAL.burnt, 0.3), line: PAL.burnt, speed: 7, spread: 100 });
    ocean(c, W, Hh, 440, t, [PAL.krishna, PAL.peacock, mixc(PAL.peacock, PAL.cream, 0.25), mixc(PAL.peacock, PAL.cream, 0.45)]);
    c.fillStyle = PAL.sandal; c.beginPath(); c.moveTo(0, 720); c.lineTo(0, 600); c.quadraticCurveTo(300, 560, 520, 640); c.quadraticCurveTo(700, 700, 900, 720); c.closePath(); c.fill();
    tree(c, 90, 610, 1.2, PAL.deep, { palm: true }); tree(c, 180, 630, 0.9, PAL.deep, { palm: true });
    figure(c, { x: 330, y: 640, s: 0.9, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', bow: true, tilak: true, arms: [[-1.1, 0.4], [0.2, 0.6]] });
    figure(c, { x: 250, y: 650, s: 0.85, dir: 1, skin: PAL.burnt, cloth: PAL.kumkum, sash: PAL.gold, crown: 'bun', bow: true });
    figure(c, { x: 440, y: 655, s: 0.85, dir: 1, skin: PAL.kesari, cloth: PAL.kumkum, sash: PAL.gold, crown: 'cap', face: 'monkey', tail: true, mace: true });
    c.restore();
  }
  
  function sceneLeap(c, W, Hh, t) {
    const u = cl((t - SC.leap) / (SC.lanka - SC.leap + 0.6));
    c.save(); cam(c, W, Hh, 0.04 * u);
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 33, alpha: 0.28, n: 120 });
    sun(c, 640, 300, 170, PAL.turmeric, 2.4); rays(c, 640, 300, 170, 800, 30, PAL.cream, t, 0.15);
    cloudBank(c, W, 420, t, { seed: 34, n: 6, fill: PAL.sandal, line: PAL.saffron, speed: 40, spread: 120 });
    ocean(c, W, Hh, 560, t, [PAL.krishna, PAL.peacock, mixc(PAL.peacock, PAL.cream, 0.25), mixc(PAL.peacock, PAL.cream, 0.45)]);
    skyline(c, 1250, 560, 0.4, PAL.gold, t);
    const x = lerp(-150, 1250, u), y = 560 - Math.sin(u * Math.PI) * 420;
    c.save(); c.translate(x, y); c.rotate(-0.35 + u * 0.5);
    figure(c, { x: 0, y: 0, s: 1.5, dir: 1, skin: PAL.kesari, cloth: PAL.kumkum, sash: PAL.gold, crown: 'cap', face: 'monkey', tail: true, mace: true, maceA: -2.2, pose: 'raise', glow: PAL.turmeric });
    c.restore();
    c.restore();
  }
  
  function sceneLanka(c, W, Hh, t) {
    const tt = t - SC.lanka;
    c.save(); cam(c, W, Hh, 0.06 * sm(SC.lanka, SC.army, t));
    sky(c, W, Hh, [[0, PAL.night], [0.45, PAL.maroon], [0.8, PAL.vermilion], [1, PAL.kesari]]);
    streaks(c, W, Hh, t, { color: PAL.marigold, alpha: 0.25, seed: 35 });
    cloudBank(c, W, 220, t, { seed: 36, n: 6, fill: PAL.smoke, line: PAL.night, speed: 14, spread: 160 });
    skyline(c, 640, 600, 0.9, PAL.gold, t);
    for (let i = 0; i < 6; i++) flames(c, 120 + i * 210, 610, 1.3 + (i % 2) * 0.4, t, 40 + i, 6);
    const r = H.rng(37); c.fillStyle = PAL.smoke;
    for (let i = 0; i < 8; i++) { const x = 100 + r() * 1080, s = 20 + r() * 30, y = 520 - ((tt * (20 + r() * 30) + r() * 300) % 400); c.globalAlpha = 0.5 * (1 - (520 - y) / 400); c.beginPath(); c.arc(x, y, s, 0, TAU); c.fill(); }
    c.globalAlpha = 1;
    figure(c, { x: 640, y: 280, s: 0.8, dir: -1, skin: PAL.kesari, cloth: PAL.kumkum, sash: PAL.gold, crown: 'cap', face: 'monkey', tail: true, mace: true, maceA: -1.4, pose: 'raise' });
    flames(c, 585, 170, 0.55, t, 50, 4);
    c.fillStyle = PAL.deep; c.fillRect(0, 640, W, 80); hills(c, W, Hh, 660, 30, PAL.ink, 22);
    c.restore();
  }
  
  function sceneArmy(c, W, Hh, t) {
    const tt = t - SC.army;
    c.save(); cam(c, W, Hh, 0.05 * sm(SC.army, SC.battle, t));
    sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 38, alpha: 0.18 });
    sun(c, 1000, 300, 110, PAL.marigold, 3);
    cloudBank(c, W, 220, t, { seed: 39, n: 5, fill: mixc(PAL.sandal, PAL.burnt, 0.3), line: PAL.burnt, speed: 7, spread: 100 });
    skyline(c, 1180, 520, 0.4, PAL.gold, t);
    ocean(c, W, Hh, 480, t, [PAL.krishna, PAL.peacock, mixc(PAL.peacock, PAL.cream, 0.25), mixc(PAL.peacock, PAL.cream, 0.45)]);
    
    const ar = fade(t, 100.7, 2.5), r = H.rng(41);
    if (ar > 0) { c.strokeStyle = PAL.deep; c.lineWidth = 3; for (let i = 0; i < 30; i++) { const u = cl(ar * 1.6 - r() * 0.6), x0 = 100 + r() * 400, x1 = x0 + 500 + r() * 400, h = 150 + r() * 200; if (u <= 0) continue; const x = lerp(x0, x1, u), y = 520 - Math.sin(u * Math.PI) * h, dxu = (x1 - x0) / 60, dyu = -Math.cos(u * Math.PI) * Math.PI * h / 60; c.beginPath(); c.moveTo(x, y); c.lineTo(x - dxu * 2.2, y - dyu * 2.2); c.stroke(); } }
    const br = EO(sm(97.7, 100.6, t));
    bridge(c, -20, 1080, 560, br, PAL.sandal);
    
    const rise = EO(fade(t, 95.6, 1.6)), march = Math.max(0, t - 97.4) * 70;
    for (let k = 0; k < 16; k++) { const x = 60 + k * 72 - 500 + march - (k % 2) * 20; if (x < -40 || x > -20 + 1100 * br + 30) continue; const yy = x < 180 ? 600 + (1 - rise) * 160 : 556; vanara(c, x, yy + (k % 3) * 3, 0.42 + (k % 3) * 0.04, 1, tt * 1.6 + k * 0.37, k % 4 === 0 ? PAL.kesari : PAL.burnt); }
    hills(c, W, Hh, 600, 50, PAL.brown, 23); hills(c, W, Hh, 660, 30, PAL.deep, 24);
    figure(c, { x: 250, y: 700, s: 1.0, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', bow: true, tilak: true, arms: [[-1.4, 0.2], [0.3, 0.8]] });
    figure(c, { x: 140, y: 705, s: 0.95, dir: 1, skin: PAL.burnt, cloth: PAL.kumkum, sash: PAL.gold, crown: 'bun', bow: true });
    c.restore();
  }
  
  function sceneBattle(c, W, Hh, t) {
    const tt = t - SC.battle, rise = EO(fade(t, 109.7, 1.2)), draw = EO(fade(t, 109.7, 1.6));
    const shot = t > 111.6 ? cl((t - 111.6) / 0.45) : 0, hit = t > 112.05, win = EO(fade(t, 112.05, 1.4));
    const flash = hit ? Math.exp(-(t - 112.05) * 4) : 0;
    c.save(); cam(c, W, Hh, 0.08 * sm(SC.battle, SC.title, t), 0, 30);
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 42, alpha: 0.2 });
    const g = c.createLinearGradient(W * 0.35, 0, W * 0.75, 0); g.addColorStop(0, H.rgba(PAL.night, 0)); g.addColorStop(1, H.rgba(PAL.night, 0.82 * (1 - win)));
    c.fillStyle = g; c.fillRect(0, 0, W, Hh);
    sun(c, 300, 280, 130, PAL.turmeric, 2.8); rays(c, 300, 280, 130, 800, 28, PAL.cream, t, 0.12 + 0.25 * rise);
    cloudBank(c, W, 250, t, { seed: 43, n: 6, fill: mixc(PAL.sandal, PAL.maroon, 0.3 * (1 - win)), line: PAL.burnt, speed: 8, spread: 120 });
    hills(c, W, Hh, 600, 50, mixc(PAL.brown, PAL.saffron, 0.3), 25); hills(c, W, Hh, 660, 30, PAL.brown, 26);
    c.save(); c.globalAlpha = 1 - win; ravana(c, { x: 960, y: 700, s: 1.35, dir: -1, mace: true, arms: [[-1.4, -1.0], [1.2, -1.6]] }); flames(c, 1150, 715, 1.2, t, 60, 6); c.restore();
    [120, 260].forEach((x) => lotus(c, x, 712, 0.9, PAL.lotus, PAL.cream));
    figure(c, { x: 360 + rise * 30, y: 700, s: 1.35 + rise * 0.1, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', bow: true, draw: shot > 0 ? 0 : draw, pose: 'aim', tilak: true, glow: rise > 0 ? PAL.turmeric : null });
    if (shot > 0 && shot < 1) { const x0 = 520, y0 = 455, x1 = 930, y1 = 420, x = lerp(x0, x1, shot), y = lerp(y0, y1, shot); const tg = c.createLinearGradient(x - 220, y, x, y); tg.addColorStop(0, H.rgba(PAL.cream, 0)); tg.addColorStop(1, PAL.cream); c.strokeStyle = tg; c.lineWidth = 8; c.beginPath(); c.moveTo(x - 220, y + 18); c.lineTo(x, y); c.stroke(); c.strokeStyle = PAL.deep; c.lineWidth = 4; c.beginPath(); c.moveTo(x - 120, y + 10); c.lineTo(x, y); c.stroke(); c.fillStyle = PAL.ash; c.beginPath(); c.moveTo(x + 26, y - 2); c.lineTo(x, y - 10); c.lineTo(x, y + 8); c.closePath(); c.fill(); }
    if (flash > 0.02) { rays(c, 930, 420, 10, 900, 36, PAL.cream, t * 3, flash * 0.8); c.fillStyle = H.rgba(PAL.cream, flash * 0.7); c.fillRect(0, 0, W, Hh); }
    hills(c, W, Hh, 712, 16, PAL.deep, 27);
    void tt;
    c.restore();
  }
  
  function sceneTitle(c, W, Hh, t) {
    const u = sm(SC.title, DURATION, t);
    c.save(); cam(c, W, Hh, 0.05 * u, 0, 10);
    sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 44, n: 110, alpha: 0.26 });
    rays(c, 640, 440, 120, 900, 30, PAL.cream, t, 0.14);
    sun(c, 640, 440, 125, PAL.turmeric, 3);
    cloudBank(c, W, 300, t, { seed: 45, n: 7, fill: PAL.sandal, line: PAL.saffron, speed: 5, spread: 200 });
    hills(c, W, Hh, 560, 60, mixc(PAL.brown, PAL.saffron, 0.4), 28); hills(c, W, Hh, 620, 40, mixc(PAL.brown, PAL.saffron, 0.2), 29);
    temple(c, { x: 640, y: 630, s: 0.6, col: PAL.brown }, t);
    figure(c, { x: 470, y: 630, s: 0.56, dir: 1, skin: PAL.kesari, cloth: PAL.kumkum, sash: PAL.gold, crown: 'cap', face: 'monkey', pose: 'kneel', tail: true });
    figure(c, { x: 590, y: 630, s: 0.6, dir: 1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', bow: true, tilak: true, arms: [[-0.5, 0.3], [0.3, 0.8]] });
    figure(c, { x: 690, y: 630, s: 0.57, dir: 1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'stand' });
    figure(c, { x: 790, y: 630, s: 0.59, dir: 1, skin: PAL.burnt, cloth: PAL.kumkum, sash: PAL.gold, crown: 'bun', bow: true });
    [-300, 300].forEach((dx, i) => flag(c, 640 + dx, 630, 120, i ? PAL.saffron : PAL.kumkum, t, i ? -1 : 1));
    hills(c, W, Hh, 700, 20, PAL.deep, 30);
    c.restore();
  }

  const SCENES = [[0, sceneCosmos], [SC.dawn, sceneDawn], [SC.ayodhya, sceneAyodhya], [SC.rama, sceneRama], [SC.exile, sceneExile], [SC.walk, sceneWalk], [SC.ravana, sceneRavana], [SC.dharma, sceneDharma], [SC.forest, sceneForest], [SC.shore, sceneShore], [SC.leap, sceneLeap], [SC.lanka, sceneLanka], [SC.army, sceneArmy], [SC.battle, sceneBattle], [SC.title, sceneTitle]];
