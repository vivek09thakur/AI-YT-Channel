// Kala Bhairava - Sound Score

function scoreSound(k0) {
  const D = DURATION;
  const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
  const k = {
    ...k0,
    tone: (t, p) => live(t) && k0.tone(t, p),
    noise: (t, p) => live(t) && k0.noise(t, p)
  };
  const lineT = (i) => LINES[i][0];

  const drone = (t0, t1, notes, g = 1) => {
    for (let t = t0; t < t1; t += 6) {
      notes.forEach((n, i) => {
        k.tone(t, {
          f: n,
          type: i ? 'sine' : 'triangle',
          dur: Math.min(9, t1 - t + 1),
          a: 2.5,
          hold: 3,
          gain: 0.045 * g / (i + 1),
          verb: 0.45,
          filter: 'lowpass',
          f2: 600,
          pan: (i - 1) * 0.2
        });
      });
    }
  };

  const gong = (t, g = 1, f = 90) => {
    k.play('thud', t, { f: 75, gain: 0.7 * g });
    k.tone(t, { f: [[0, f], [3.8, f * 0.97]], dur: 3.8, gain: 0.3 * g, a: 0.01, verb: 0.5 });
    k.tone(t, { f: f * 2.02, dur: 2.4, gain: 0.1 * g, a: 0.01, verb: 0.4 });
    k.tone(t, { f: f * 2.9, dur: 1.4, gain: 0.05 * g, a: 0.01 });
    k.noise(t, { dur: 0.35, color: 'brown', filter: 'lowpass', f: 400, gain: 0.3 * g });
  };

  const bell = (t, n, g = 1, pan = 0) => {
    const f = k.hz(n);
    k.tone(t, { f, dur: 2.4, gain: 0.12 * g, a: 0.003, verb: 0.45, pan });
    k.tone(t, { f: f * 2.76, dur: 0.9, gain: 0.04 * g, a: 0.003, pan });
    k.tone(t, { f: f * 5.4, dur: 0.3, gain: 0.015 * g, a: 0.003, pan });
  };

  const riser = (t, d = 1.2, g = 0.5) => k.play('riser', t - d, { dur: d, gain: g });
  const whoosh = (t, g = 0.5) => k.play('whoosh', t - 0.3, { dur: 0.7, top: 1800, gain: g });
  const thunder = (t, g = 1) => {
    k.play('impact', t, { f: 60, gain: 0.9 * g });
    k.noise(t + 0.05, { dur: 2.6, color: 'brown', filter: 'lowpass', f: [[0, 900], [0.3, 300], [2.6, 80]], gain: 0.45 * g, a: 0.02, verb: 0.5 });
  };
  const fire = (t0, t1, g = 0.3) => {
    k.noise(t0, { dur: t1 - t0, color: 'pink', filter: 'bandpass', f: 500, q: 0.5, gain: g, a: 0.6, hold: t1 - t0 - 1.2, minor: true });
    const r = H.rng(77);
    for (let t = t0; t < t1; t += 0.06 + r() * 0.2) {
      k.noise(t, { dur: 0.012, filter: 'bandpass', f: 1500 + r() * 2500, q: 2, gain: 0.08 * g * 3, minor: true, pan: r() - 0.5 });
    }
  };
  const sea = (t0, t1, g = 0.25) => {
    for (let t = t0; t < t1; t += 3.2) {
      k.noise(t, { dur: 4.2, color: 'brown', filter: 'lowpass', f: [[0, 300], [2, 800], [4.2, 250]], gain: g, a: 1.8, minor: true });
    }
  };

  // Harmonious meditative drones anchored in D minor (Lord of Time theme)
  drone(0, SC.kalaMeaning, ['D2', 'A2', 'D3'], 1.0);
  drone(SC.kalaMeaning, SC.beyondTime, ['B1', 'F#2', 'D3'], 0.9);
  drone(SC.beyondTime, SC.fierceForm, ['D2', 'A2', 'F#3'], 1.0);
  drone(SC.fierceForm, SC.kashi, ['G1', 'D2', 'Bb2'], 1.2);
  drone(SC.kashi, SC.eternalReality, ['D2', 'A2', 'D3'], 1.0);
  drone(SC.eternalReality, D, ['D2', 'A2', 'F#3'], 1.1);

  // Scene 1: Cosmic Intro
  k.noise(0.2, { dur: 2.8, color: 'brown', filter: 'lowpass', f: [[0, 70], [2.8, 380]], gain: 0.2, a: 1.8 });
  gong(lineT(0), 0.7, 72);

  // Scene 2: Bhairava Lord of Time
  riser(SC.bhairavaLord);
  whoosh(SC.bhairavaLord, 0.4);
  gong(lineT(1), 1.2, 82);
  bell(lineT(1) + 0.1, 'D6', 0.8);
  k.play('sparkle', lineT(1) + 0.15, { n: 8, gain: 0.7 });

  // Scene 3: Beyond Birth, Death & Destruction
  bell(lineT(2), 'A5', 0.6, -0.2);
  bell(lineT(3), 'F#5', 0.6, 0.2);

  // Scene 4: Kala Meaning
  riser(SC.kalaMeaning);
  whoosh(SC.kalaMeaning, 0.4);
  gong(lineT(4), 0.8, 72);
  bell(lineT(5), 'D5', 0.6);
  gong(lineT(6), 0.9, 65);

  // Scene 5: Impermanence
  riser(SC.impermanence);
  whoosh(SC.impermanence, 0.4);
  bell(lineT(8), 'A5', 0.5, -0.3);
  bell(lineT(9), 'F#5', 0.5, 0.3);
  bell(lineT(10), 'D6', 0.6, 0);
  k.play('thud', lineT(11), { f: 80, gain: 0.5 });
  gong(lineT(12), 0.7, 72);

  // Scene 6: Beyond Time
  riser(SC.beyondTime);
  whoosh(SC.beyondTime, 0.5);
  gong(lineT(13), 1.1, 92);
  bell(lineT(13) + 0.08, 'D6', 0.8);
  bell(lineT(14), 'A5', 0.6);
  bell(lineT(15), 'F#5', 0.6);

  // Scene 7: Fierce Form
  riser(SC.fierceForm, 1.4, 0.7);
  thunder(SC.fierceForm, 0.9);
  fire(SC.fierceForm, SC.kashi, 0.32);
  gong(lineT(16), 1.3, 62);
  k.tone(lineT(16) + 0.05, { f: [[0, 50], [2, 85]], type: 'sawtooth', dur: 2.2, gain: 0.12, a: 0.8, filter: 'lowpass', f2: 260 });

  // Scene 8: Sacred City of Kashi
  riser(SC.kashi);
  whoosh(SC.kashi, 0.5);
  sea(SC.kashi, SC.dharmaLesson, 0.22);
  bell(lineT(17), 'D5', 0.7, -0.2);
  bell(lineT(18), 'A5', 0.7, 0.2);
  k.play('sparkle', lineT(18) + 0.2, { n: 6, gain: 0.5 });

  // Scene 9: Dharma Lesson
  riser(SC.dharmaLesson);
  whoosh(SC.dharmaLesson, 0.4);
  bell(lineT(20), 'D5', 0.6);
  bell(lineT(21), 'F#5', 0.6);
  bell(lineT(22), 'A5', 0.6);
  bell(lineT(23), 'D6', 0.7);

  // Scene 10: Eternal Reality
  riser(SC.eternalReality);
  whoosh(SC.eternalReality, 0.5);
  gong(lineT(25), 1.1, 82);
  bell(lineT(26), 'D6', 0.8);
  k.play('sparkle', lineT(26) + 0.1, { n: 8, gain: 0.7 });

  // Scene 11: Kala Bhairava Title Card
  riser(SC.ultimateLord, 1.1, 0.6);
  whoosh(SC.ultimateLord, 0.6);
  gong(lineT(27), 1.5, 72);
  [0, 0.14, 0.28].forEach((d, i) => bell(lineT(27) + d, ['D6', 'A6', 'D7'][i], 0.9, (i - 1) * 0.3));
  k.play('sparkle', lineT(27) + 0.2, { n: 12, gain: 0.9 });
  bell(lineT(28), 'F#5', 0.6, -0.2);

  // Scene 12: Companion Shvana Dog
  whoosh(SC.companionDog, 0.4);
  bell(lineT(29), 'A5', 0.6);
  bell(lineT(30), 'D6', 0.7);

  // Scene 13: Mystery Outro
  riser(SC.mysteryOutro, 1.0, 0.5);
  whoosh(SC.mysteryOutro, 0.4);
  gong(lineT(31), 1.2, 72);
  bell(lineT(31) + 0.1, 'D6', 0.8);
  k.noise(D - 1.2, { dur: 1.5, color: 'brown', filter: 'lowpass', f: 200, gain: 0.1, a: 0.1 });
}
