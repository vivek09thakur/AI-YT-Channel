function scoreSound(k0) {
  const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
  const k = { ...k0, tone: (t, p) => live(t) && k0.tone(t, p), noise: (t, p) => live(t) && k0.noise(t, p) };
  
  const drone = (t0, t1, notes, g = 1) => { for (let t = t0; t < t1; t += 6) notes.forEach((n, i) => { k.tone(t, { f: n, type: i ? 'sine' : 'triangle', dur: Math.min(9, t1 - t + 1), a: 2.5, hold: 3, gain: 0.05 * g / (i + 1), verb: 0.4, filter: 'lowpass', f2: 600 }); }); };
  const gong = (t, g = 1, f = 98) => {
    k.play('thud', t, { f: 80, gain: 0.7 * g });
    k.tone(t, { f: [[0, f], [3.8, f * 0.97]], dur: 3.8, gain: 0.3 * g, a: 0.01, verb: 0.5 });
  };
  const bell = (t, n, g = 1) => { const f = k.hz(n); k.tone(t, { f, dur: 2.4, gain: 0.12 * g, a: 0.003, verb: 0.45 }); };

  drone(0, DURATION, ['D2', 'A2', 'D3'], 1);
  gong(0, 0.8, 73);
  
  Object.values(SC).forEach(st => {
    gong(st, 0.6, 85);
    bell(st + 0.2, 'D5', 0.5);
  });
}
