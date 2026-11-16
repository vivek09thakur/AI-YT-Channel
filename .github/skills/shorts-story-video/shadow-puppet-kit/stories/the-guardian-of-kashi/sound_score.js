  function scoreSound(k0) {
    const D = DURATION;
    const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
    const k = { ...k0, tone: (t, p) => live(t) && k0.tone(t, p), noise: (t, p) => live(t) && k0.noise(t, p) };
    
    const drone = (t0, t1, notes, g = 1) => { for (let t = t0; t < t1; t += 6) notes.forEach((n, i) => { k.tone(t, { f: n, type: i ? 'sine' : 'triangle', dur: Math.min(9, t1 - t + 1), a: 2.5, hold: 3, gain: 0.05 * g / (i + 1), verb: 0.4, filter: 'lowpass', f2: 600, pan: (i - 1) * 0.2 }); }); };
    const gong = (t, g = 1, f = 98) => {
      k.play('thud', t, { f: 80, gain: 0.7 * g });
      k.tone(t, { f: [[0, f], [3.8, f * 0.97]], dur: 3.8, gain: 0.3 * g, a: 0.01, verb: 0.5 });
    };
    const bell = (t, n, g = 1, pan = 0) => { const f = k.hz(n); k.tone(t, { f, dur: 2.4, gain: 0.12 * g, a: 0.003, verb: 0.45, pan }); };
    const riser = (t, d = 1.2, g = 0.5) => k.play('riser', t - d, { dur: d, gain: g });
    const whoosh = (t, g = 0.5) => k.play('whoosh', t - 0.3, { dur: 0.7, top: 1800, gain: g });

    drone(0, D, ['D2', 'A2', 'D3'], 1);
    gong(0, 0.6, 73);
    riser(SC.shiva); whoosh(SC.shiva, 0.4); bell(SC.shiva, 'D5', 0.6);
    riser(SC.kashi); whoosh(SC.kashi, 0.4); bell(SC.kashi, 'A5', 0.6);
    riser(SC.kotwal); whoosh(SC.kotwal, 0.4); gong(SC.kotwal, 0.8, 65);
    riser(SC.protector); whoosh(SC.protector, 0.4); bell(SC.protector, 'F#5', 0.6);
    riser(SC.temple); whoosh(SC.temple, 0.4); gong(SC.temple, 0.9, 73);
    riser(SC.mystery); whoosh(SC.mystery, 0.5); gong(SC.mystery, 1.2, 73);
  }
