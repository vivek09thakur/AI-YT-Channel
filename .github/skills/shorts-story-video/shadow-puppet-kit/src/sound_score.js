  function scoreSound(k0) {
    const D = DURATION;

    const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
    const k = { ...k0, tone: (t, p) => live(t) && k0.tone(t, p), noise: (t, p) => live(t) && k0.noise(t, p) };
    const gam = (t, n, g = 1, pan = 0, minor = false) => {
      const f = k.hz(n);
      k.tone(t, { f, dur: 1.9, gain: 0.13 * g, a: 0.002, pan, verb: 0.3, minor });
      k.tone(t, { f: f * 1.007, dur: 1.6, gain: 0.07 * g, a: 0.002, pan, verb: 0.3, minor });
      k.tone(t, { f: f * 2.01, dur: 0.55, gain: 0.04 * g, a: 0.002, pan, minor });
      if (f * 2.95 < 2500) k.tone(t, { f: f * 2.95, dur: 0.22, gain: 0.018 * g, a: 0.002, pan, minor });
      k.noise(t, { dur: 0.02, filter: 'bandpass', f: Math.min(2200, f * 1.6), q: 2, gain: 0.08 * g, pan, minor });
    };
    const gong = (t, g = 1) => {
      k.play('thud', t, { f: 90, gain: 0.7 * g });
      k.tone(t, { f: [[0, 98], [3.6, 95]], dur: 3.6, gain: 0.36 * g, a: 0.012, verb: 0.45 });
      k.tone(t, { f: [[0, 99.2], [3.2, 96]], dur: 3.2, gain: 0.16 * g, a: 0.02 });
      k.tone(t, { f: 202, dur: 2.2, gain: 0.1 * g, a: 0.01, verb: 0.4 });
      k.tone(t, { f: 277, dur: 1.4, gain: 0.05 * g, a: 0.01 });
      k.noise(t, { dur: 0.3, color: 'brown', filter: 'lowpass', f: 450, gain: 0.3 * g });
    };
    const tap = (t, f = 640, g = 0.55, pan = 0, minor = true) => { k.play('tock', t, { f, gain: g, pan, minor }); k.noise(t, { dur: 0.014, filter: 'bandpass', f: 1700, q: 2.5, gain: 0.32 * g, a: 0.001, pan, minor }); };
    const hide = (t, dur, g = 0.5, pan = 0, minor = true) => k.play('paper', t, { dur, gain: g, pan, minor });
    const slide = (t, dur, g = 0.12, minor = true) => k.noise(t, { dur, color: 'brown', filter: 'lowpass', f: [[0, 260], [dur * 0.5, 520], [dur, 240]], gain: g, a: dur * 0.4, minor });
    const flap = (t, g = 0.25, pan = 0, minor = true) => k.noise(t, { dur: 0.11, color: 'pink', filter: 'lowpass', f: [[0, 900], [0.11, 300]], gain: g, a: 0.03, pan, minor });
    const flaps = (t0, t1, step, g, pan) => { for (let t = t0; t < t1; t += step) flap(t, g, pan); };

    const caw = (t, g = 1, pan = 0, minor = true, p = 1) => [0, 0.17].forEach((dt, i) => {
      k.tone(t + dt, { f: [[0, 760 * p], [0.15, 520 * p]], type: 'sawtooth', dur: 0.16, gain: 0.07 * g * (i ? 0.8 : 1), a: 0.01, hold: 0.06, filter: 'bandpass', f2: 1300, q: 2.5, pan, minor });
      k.noise(t + dt, { dur: 0.14, filter: 'bandpass', f: 1600 * p, q: 3, gain: 0.08 * g, a: 0.01, pan, minor });
    });
    const swell = (t, g = 0.35) => k.noise(t, { dur: 0.5, color: 'brown', filter: 'lowpass', f: [[0, 600], [0.25, 140], [0.5, 600]], gain: g, a: 0.05, hold: 0.3 });

    k.noise(0.04, { dur: 0.45, color: 'brown', filter: 'lowpass', f: [[0, 200], [0.12, 700], [0.45, 180]], gain: 0.4, a: 0.05 });
    [0.18, 0.31, 0.47].forEach((t, i) => k.noise(t, { dur: 0.012, filter: 'bandpass', f: 1300 + i * 300, q: 1.5, gain: 0.12, minor: true }));
    [3.6, 9.2, 13.4, 22.0, 32.1, 45.0, 53.9].forEach((t, i) => k.noise(t, { dur: 0.01, filter: 'bandpass', f: 1500 + i * 120, q: 1.4, gain: 0.07, minor: true }));

    tap(at('pareshan'), 300, 0.9, -0.3, false); k.play('thud', at('pareshan'), { f: 120, gain: 0.45 });
    k.play('stamp', at('saalon'), { gain: 1.0, pan: 0.4 }); hide(at('saalon') + 0.05, 0.3, 0.4, 0.4);
    hide(at('aur1'), 0.6, 0.55, 0.6); hide(at('aur1') + 0.05, 0.6, 0.5, -0.7); flaps(at('aur1'), at('aur1') + 0.7, 0.13, 0.2, 0.5);
    tap(at('aur1') + 0.66, 420, 0.5, 0.7); tap(at('aur1') + 0.7, 380, 0.5, -0.8);
    gam(at('bhi'), 'A4', 0.7, 0); caw(at('bhi') + 0.12, 0.8, 0.6); caw(at('bhi') + 0.2, 0.7, -0.6, true, 0.9);

    swell(SC.research - 0.25);
    tap(at('uw') + 0.33, 700, 0.5, 0); k.play('typing', at('uw') + 0.05, { n: 12, rate: 0.06, gain: 0.6, minor: true });
    k.play('stamp', at('sach'), { gain: 1.0, pan: 0.4 }); hide(at('sach') + 0.05, 0.3, 0.35, 0.4);

    slide(11.25, 0.6, 0.14);
    flap(at('y2006'), 0.3, -0.7); tap(at('y2006') + 0.28, 760, 0.6, -0.7);
    for (let t = at('scientist'); t < at('scientist') + 1.0; t += Math.PI / 7) tap(t, 360, 0.45, 0.6);
    k.play('stroke', at('mask'), { material: 'brush', dur: 0.38, gain: 0.9, minor: true }); gam(at('mask') + 0.38, 'D4', 0.6, 0.4);
    for (let t = at('kuch') - 0.5; t < at('kuch'); t += 0.17) tap(t, 520, 0.35, -0.6);
    hide(at('pakde'), 0.25, 0.7, -0.5, false); k.play('thud', at('pakde') + 0.25, { f: 140, gain: 0.5, pan: -0.5 }); tap(at('pakde') + 0.42, 300, 0.4, -0.5);
    caw(at('pakde') + 0.35, 0.6, -0.5, true, 1.1);
    gam(at('chot') + 0.1, 'G4', 0.4, -0.4, true);
    k.play('tick', at('tag'), { gain: 0.9, pan: -0.6 }); k.play('tick', at('tag') + 0.12, { gain: 0.9, pan: -0.4 });
    gam(at('tag') + 0.02, 'A5', 0.35, -0.5, true);
    slide(at('chhod'), 0.45, 0.13); flaps(WT.chhod, WT.chhod + 0.9, 0.12, 0.3, -0.5);

    for (let t = WT.uske; t < 23.4; t += Math.PI / 7) tap(t, 360, 0.4, 0.2);
    flaps(at('cheekh'), at('dusra'), 0.15, 0.16, 0);
    [0, 1, 2, 3].forEach((i) => { const t = at('cheekh') + i * 0.34; k.play('pop', t, { f: 380, gain: 0.5, pan: i % 2 ? 0.5 : -0.5, minor: true }); caw(t + 0.02, 1.0, i % 2 ? 0.5 : -0.5, false, 1 - i * 0.04); });
    k.play('whoosh', at('jhund'), { dur: 0.6, top: 1400, gain: 0.5 }); caw(at('jhund') + 0.3, 0.8, -0.3, true, 0.92); caw(at('jhund') + 0.45, 0.7, 0.4, true, 1.06);

    hide(at('dusra'), 0.28, 0.5); k.play('thud', at('dusra') + 0.28, { f: 110, gain: 0.45 });
    for (let t = at('dmask') - 0.25; t < at('dmask') + 0.35; t += Math.PI / 7) tap(t, 400, 0.4, 0.6);
    gam(27.5, 'Eb4', 0.8, -0.5); gam(27.5, 'E4', 0.7, -0.5); gam(27.5, 'A2', 0.8, -0.3);
    gam(28.0, 'A4', 0.85, 0.5); gam(28.12, 'D5', 0.85, 0.5);
    tap(28.45, 900, 0.5, 0.6); tap(at('dhyan') + 0.15, 900, 0.5, 0.6);

    for (const pan of [-0.7, 0.7]) k.noise(29.91, { dur: 0.32, color: 'pink', filter: 'bandpass', f: [[0, 500], [0.2, 1500], [0.32, 700]], q: 0.7, gain: 0.25, a: 0.12, pan });
    k.play('thud', 30.2, { f: 110, gain: 0.3 });
    for (const pan of [-0.7, 0.7]) k.noise(30.35, { dur: 0.36, color: 'pink', filter: 'bandpass', f: [[0, 700], [0.2, 1500], [0.36, 500]], q: 0.7, gain: 0.22, a: 0.12, pan });
    tap(at('twist') + 0.33, 520, 0.9, 0, false); gam(at('twist') + 0.35, 'D4', 0.8); gam(at('twist') + 0.5, 'F4', 0.7);
    slide(31.0, 0.5, 0.12);
    const scale = ['D4', 'F4', 'G4', 'A4', 'C5', 'D5'];
    RING.forEach((r, i) => {
      k.play('stroke', vineT(i), { material: 'brush', dur: 0.4, gain: 0.8, minor: true, pan: r[0] < 640 ? -0.4 : 0.4 });
      gam(vineT(i) + 0.4, scale[i], 0.55, r[0] < 640 ? -0.5 : 0.5, true);
    });
    k.play('stamp', at('sikha'), { gain: 1.0 }); hide(at('sikha') + 0.05, 0.3, 0.35);
    tap(at('dushman') + 0.28, 340, 0.8, 0, false); gam(at('dushman') + 0.15, 'A2', 0.8); gam(at('dushman') + 0.15, 'Eb4', 0.55);
    caw(at('dushman') + 0.25, 0.7, -0.5, true, 0.85); caw(at('dushman') + 0.3, 0.7, 0.5, true, 0.95);

    flaps(WT.aur2, WT.aur2 + 0.6, 0.11, 0.25, 0); tap(WT.aur2 + 0.33, 760, 0.6);
    { let last = -1, prev = 2006; for (let t = at('nafrat'); t < at('fifteen') - 0.05; t += 0.002) { const v = Math.round(2006 + 15 * EO(sm(at('nafrat'), at('fifteen') - 0.05, t))); if (v !== prev && t - last >= 0.083) { tap(t, 1150, 0.4, 0); last = t; } prev = v; } }
    gong(at('fifteen'), 1.1); gam(at('fifteen') + 0.02, 'D5', 0.5, 0.3);
    tap(at('fifteen') + 0.25, 820, 0.6, 0.6); tap(at('fifteen') + 0.35, 900, 0.5, 0);
    k.play('stroke', at('zyada'), { material: 'brush', dur: 0.35, gain: 0.6, minor: true });

    flap(40.86, 0.45, 0.4, false); flap(41.0, 0.5, 0.1, false); flap(41.12, 0.5, -0.1, false);
    k.noise(40.95, { dur: 0.7, color: 'pink', filter: 'bandpass', f: [[0, 180], [0.33, 800], [0.7, 160]], q: 0.8, gain: 0.42, a: 0.28, verb: 0.2 });
    k.play('thud', 41.2, { f: 70, gain: 0.35 });

    flap(SC.dead + 0.05, 0.2, -0.7); tap(SC.dead + 0.3, 700, 0.4, -0.7);
    k.noise(at('mar'), { dur: 0.9, color: 'brown', filter: 'lowpass', f: 300, gain: 0.18, a: 0.4, minor: true });
    k.tone(at('mar') + 0.1, { f: 'D3', dur: 2.2, gain: 0.08, a: 0.2, verb: 0.4 });
    GATHER.forEach(([x], i) => { const t0 = at('jama') + i * 0.38; flap(t0 + 0.1, 0.12, x < 640 ? -0.5 : 0.5); tap(t0 + 0.42, 380, 0.3, x < 640 ? -0.5 : 0.5); });
    tap(at('khatra') + 0.2, 300, 0.7, 0, false); gam(at('khatra') + 0.22, 'D4', 0.65);
    gam(at('kaun') + 0.3, 'D4', 0.6, 0.6); gam(at('kaun') + 0.48, 'F4', 0.6, 0.6);

    swell(SC.end - 0.25, 0.3);
    gam(at('izzat') + 0.05, 'A4', 0.6, 0.4); k.play('pop', at('izzat'), { f: 520, gain: 0.5, pan: 0.4, minor: true });
    slide(at('wo') - 0.2, 0.35, 0.1); tap(at('wo') + 0.28, 520, 0.7, 0.2);
    k.play('typing', WT.wo, { n: 14, rate: 0.065, gain: 0.6, minor: true, pan: 0.2 });
    tap(WT.wo + 1.28, 860, 0.5, 0.6);
    slide(at('shehar'), 0.45, 0.14); tap(at('shehar') + 0.42, 420, 0.9, 0.2, false);
    gam(at('shehar') + 0.45, 'D4', 0.8, -0.2); gam(at('shehar') + 0.6, 'A4', 0.75, 0); gam(at('shehar') + 0.75, 'D5', 0.7, 0.2);
    k.tone(at('shehar') + 0.45, { f: 'D3', dur: 2.0, gain: 0.1, a: 0.01, verb: 0.4 });
    gam(WT.last + 0.5, 'D5', 0.5, 0.2, true);
    void D;
  }
