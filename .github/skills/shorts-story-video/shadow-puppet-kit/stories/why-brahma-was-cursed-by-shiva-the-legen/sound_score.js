/* Sound Score for The Legend of Brahma's Fifth Head */

function scoreSound(k0) {
  const D = DURATION;
  const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
  const k = {
    ...k0,
    tone: (t, p) => live(t) && k0.tone(t, p),
    noise: (t, p) => live(t) && k0.noise(t, p),
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
          gain: 0.05 * g / (i + 1),
          verb: 0.4,
          filter: 'lowpass',
          f2: 600,
          pan: (i - 1) * 0.2,
        });
      });
    }
  };

  const gong = (t, g = 1, f = 98) => {
    k.play('thud', t, { f: 80, gain: 0.7 * g });
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
    k.noise(t + 0.05, {
      dur: 2.6,
      color: 'brown',
      filter: 'lowpass',
      f: [[0, 900], [0.3, 300], [2.6, 80]],
      gain: 0.45 * g,
      a: 0.02,
      verb: 0.5,
    });
  };

  // Background harmonic drones
  drone(0, SC.dispute, ['D2', 'A2', 'D3'], 1);
  drone(SC.dispute, SC.pillar, ['G1', 'D2', 'G2'], 0.9);
  drone(SC.pillar, SC.search, ['C2', 'G2', 'C3'], 1.2);
  drone(SC.search, SC.defeat, ['E2', 'B2', 'E3'], 0.85);
  drone(SC.defeat, SC.truth, ['A1', 'E2', 'A2'], 0.9);
  drone(SC.truth, SC.curse, ['F#1', 'C#2', 'F#2'], 1.3);
  drone(SC.curse, SC.temples, ['B1', 'F#2', 'D3'], 0.95);
  drone(SC.temples, D, ['D2', 'A2', 'D3'], 1.1);

  // Line 0: Introduction to Brahma's five heads
  bell(lineT(0), 'D5', 0.8);
  gong(lineT(0) + 0.1, 0.7, 82);

  // Line 1: Dispute between Brahma and Vishnu
  whoosh(SC.dispute, 0.4);
  bell(lineT(1), 'A4', 0.6, -0.3);
  bell(lineT(1) + 2.5, 'E5', 0.6, 0.3);

  // Line 2 & 3: Shiva manifests as the pillar of light
  riser(SC.pillar, 1.5, 0.7);
  gong(lineT(2), 1.2, 65);
  thunder(SC.pillar + 0.5, 0.8);
  k.play('sparkle', SC.pillar + 0.6, { n: 10, gain: 0.8 });

  // Line 4: The challenge
  bell(lineT(4), 'F#5', 0.7);

  // Line 5: Vishnu travels down, Brahma travels up
  whoosh(SC.search, 0.5);
  k.play('swish', SC.search + 1.2, { dur: 0.5, gain: 0.4, pan: -0.4 });
  k.play('swish', SC.search + 2.5, { dur: 0.5, gain: 0.4, pan: 0.4 });

  // Line 6: Vishnu accepts defeat
  gong(lineT(6), 0.8, 73);
  bell(lineT(6) + 0.1, 'D5', 0.6);

  // Line 7: Brahma falsely claims victory
  k.play('glitch', lineT(7), { gain: 0.4 });

  // Line 8: Ketaki flower presented
  k.play('sparkle', lineT(8), { n: 6, gain: 0.7 });
  bell(lineT(8), 'C#6', 0.6);

  // Line 9: Shiva recognizes the lie - Third eye opens
  riser(SC.truth, 1.0, 0.6);
  thunder(lineT(9), 0.9);

  // Line 10: Bhairava severing the 5th head
  const strikeTime = SC.sever + 2.5;
  riser(strikeTime, 1.4, 0.8);
  k.play('swish', strikeTime - 0.2, { dur: 0.3, gain: 0.9 });
  thunder(strikeTime, 1.4);
  gong(strikeTime, 1.5, 55);
  k.play('impact', strikeTime, { f: 45, gain: 1.3 });

  // Line 11: The curse of no temples
  gong(lineT(11), 1.0, 65);
  bell(lineT(11) + 0.2, 'B4', 0.7);

  // Line 12: Ketaki flower banned
  bell(lineT(12), 'A4', 0.6);
  k.play('thud', lineT(12), { f: 120, gain: 0.4 });

  // Line 13 & 14: Few temples & tradition
  bell(lineT(13), 'D5', 0.5);
  bell(lineT(14), 'F#5', 0.5);

  // Line 15: Moral - Big proclamation
  riser(lineT(15), 1.2, 0.6);
  gong(lineT(15), 1.3, 73);
  k.play('sparkle', lineT(15) + 0.2, { n: 12, gain: 0.9 });

  // Line 16: Closing tag
  bell(lineT(16), 'A5', 0.8);
  bell(lineT(16) + 1.2, 'D6', 0.9);
  gong(lineT(16) + 1.5, 0.9, 73);

  // Gentle closing fade
  k.noise(D - 1.5, { dur: 1.6, color: 'brown', filter: 'lowpass', f: 200, gain: 0.12, a: 0.1 });
}
