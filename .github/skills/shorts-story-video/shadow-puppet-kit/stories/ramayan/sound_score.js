  
  function scoreSound(k0) {
    const D = DURATION;
    const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
    const k = { ...k0, tone: (t, p) => live(t) && k0.tone(t, p), noise: (t, p) => live(t) && k0.noise(t, p) };
    const lineT = (i) => LINES[i][0];
    
    const drone = (t0, t1, notes, g = 1) => { for (let t = t0; t < t1; t += 6) notes.forEach((n, i) => { k.tone(t, { f: n, type: i ? 'sine' : 'triangle', dur: Math.min(9, t1 - t + 1), a: 2.5, hold: 3, gain: 0.05 * g / (i + 1), verb: 0.4, filter: 'lowpass', f2: 600, pan: (i - 1) * 0.2 }); }); };
    const gong = (t, g = 1, f = 98) => {
      k.play('thud', t, { f: 80, gain: 0.7 * g });
      k.tone(t, { f: [[0, f], [3.8, f * 0.97]], dur: 3.8, gain: 0.3 * g, a: 0.01, verb: 0.5 });
      k.tone(t, { f: f * 2.02, dur: 2.4, gain: 0.1 * g, a: 0.01, verb: 0.4 });
      k.tone(t, { f: f * 2.9, dur: 1.4, gain: 0.05 * g, a: 0.01 });
      k.noise(t, { dur: 0.35, color: 'brown', filter: 'lowpass', f: 400, gain: 0.3 * g });
    };
    const bell = (t, n, g = 1, pan = 0) => { const f = k.hz(n); k.tone(t, { f, dur: 2.4, gain: 0.12 * g, a: 0.003, verb: 0.45, pan }); k.tone(t, { f: f * 2.76, dur: 0.9, gain: 0.04 * g, a: 0.003, pan }); k.tone(t, { f: f * 5.4, dur: 0.3, gain: 0.015 * g, a: 0.003, pan }); };
    const riser = (t, d = 1.2, g = 0.5) => k.play('riser', t - d, { dur: d, gain: g });
    const whoosh = (t, g = 0.5) => k.play('whoosh', t - 0.3, { dur: 0.7, top: 1800, gain: g });
    const thunder = (t, g = 1) => { k.play('impact', t, { f: 60, gain: 0.9 * g }); k.noise(t + 0.05, { dur: 2.6, color: 'brown', filter: 'lowpass', f: [[0, 900], [0.3, 300], [2.6, 80]], gain: 0.45 * g, a: 0.02, verb: 0.5 }); };
    const step = (t, pan = 0) => k.play('thud', t, { f: 150, gain: 0.18, pan, minor: true });
    const fire = (t0, t1, g = 0.3) => { k.noise(t0, { dur: t1 - t0, color: 'pink', filter: 'bandpass', f: 500, q: 0.5, gain: g, a: 0.6, hold: t1 - t0 - 1.2, minor: true }); const r = H.rng(77); for (let t = t0; t < t1; t += 0.05 + r() * 0.2) k.noise(t, { dur: 0.012, filter: 'bandpass', f: 1500 + r() * 2500, q: 2, gain: 0.08 * g * 3, minor: true, pan: r() - 0.5 }); };
    const sea = (t0, t1, g = 0.25) => { for (let t = t0; t < t1; t += 3.2) k.noise(t, { dur: 4.2, color: 'brown', filter: 'lowpass', f: [[0, 300], [2, 900], [4.2, 250]], gain: g, a: 1.8, minor: true }); };

    drone(0, SC.ayodhya, ['D2', 'A2', 'D3'], 1);
    drone(SC.ayodhya, SC.exile, ['D2', 'A2', 'F#3'], 1);
    drone(SC.exile, SC.ravana, ['B1', 'F#2', 'D3'], 0.9);
    drone(SC.ravana, SC.dharma, ['G1', 'D2', 'Bb2'], 1.2);
    drone(SC.dharma, SC.battle, ['D2', 'A2', 'D3'], 1);
    drone(SC.battle, 112.0, ['G1', 'D2', 'Eb3'], 1.1);
    drone(112.0, D, ['D2', 'A2', 'F#3'], 1.1);

    k.noise(0.2, { dur: 3, color: 'brown', filter: 'lowpass', f: [[0, 80], [3, 400]], gain: 0.25, a: 2 });
    gong(lineT(0), 0.6, 73); gong(lineT(1), 0.8, 73);
    k.noise(4.4, { dur: 2.4, color: 'pink', filter: 'bandpass', f: [[0, 200], [2.4, 1200]], q: 1, gain: 0.12, a: 1.8, minor: true }); 
    
    riser(SC.dawn); whoosh(SC.dawn, 0.4);
    bell(lineT(2), 'D5', 0.6, -0.3); bell(lineT(3), 'F#5', 0.5, 0.3);
    k.tone(13.8, { f: [[0, 60], [1.4, 45]], type: 'sawtooth', dur: 1.8, gain: 0.08, a: 0.6, filter: 'lowpass', f2: 300 }); gong(14.0, 0.6, 65); 
    
    riser(SC.ayodhya); whoosh(SC.ayodhya, 0.5);
    bell(lineT(5), 'A5', 0.6); [0, 0.25, 0.5, 0.75].forEach((d, i) => bell(21.5 + d, ['D6', 'F#6', 'A6', 'D7'][i], 0.5, (i - 1.5) * 0.3)); k.play('sparkle', 21.6, { n: 8, gain: 0.8 });
    
    riser(SC.rama); whoosh(SC.rama, 0.5);
    gong(lineT(8), 1.2, 110); bell(lineT(8) + 0.05, 'D6', 0.9); k.play('sparkle', lineT(8) + 0.1, { n: 6, gain: 0.6 });
    bell(lineT(9), 'A5', 0.5); bell(lineT(10), 'F#5', 0.5); bell(lineT(11), 'D5', 0.5);
    
    riser(SC.exile); whoosh(SC.exile, 0.4);
    k.tone(40.1, { f: [[0, 220], [2.2, 440]], type: 'sine', dur: 2.6, gain: 0.05, a: 0.4, verb: 0.5 }); 
    k.noise(42.4, { dur: 3, color: 'brown', filter: 'lowpass', f: 250, gain: 0.15, a: 1, minor: true }); 
    for (let t = 44.8; t < SC.walk; t += 0.47) step(t, -0.2);
    
    whoosh(SC.walk, 0.3);
    for (let t = SC.walk; t < SC.ravana - 0.2; t += 0.47) { step(t, 0.1); step(t + 0.12, -0.25); step(t + 0.22, 0.3); }
    sea(SC.walk, SC.ravana, 0.12);
    bell(lineT(16), 'F#5', 0.6, 0.2); bell(lineT(18), 'B4', 0.6, -0.3);
    
    riser(SC.ravana, 1.4, 0.6); thunder(SC.ravana, 0.5);
    k.noise(60.6, { dur: 2, color: 'pink', filter: 'bandpass', f: 180, q: 3, gain: 0.1, a: 1.2, minor: true });
    k.tone(62.9, { f: [[0, 40], [2, 70]], type: 'sawtooth', dur: 2.6, gain: 0.12, a: 0.8, filter: 'lowpass', f2: 240 }); gong(lineT(22), 1.4, 65); gong(lineT(22) + 0.08, 0.8, 49);
    k.play('impact', 65.4, { f: 90, gain: 0.5 }); bell(65.5, 'Bb4', 0.4);
    thunder(69.9, 1); thunder(72.4, 1.2); k.noise(72.4, { dur: 1.6, color: 'brown', filter: 'lowpass', f: 60, gain: 0.5, a: 0.02 });
    fire(72.4, SC.dharma + 0.5, 0.25);
    
    riser(SC.dharma); whoosh(SC.dharma, 0.5);
    k.noise(76.8, { dur: 2.4, color: 'pink', filter: 'bandpass', f: [[0, 300], [2.4, 1100]], q: 2, gain: 0.08, a: 2, minor: true }); 
    bell(lineT(28), 'D5', 0.7); bell(lineT(29), 'F#5', 0.7); bell(lineT(30), 'A5', 0.7); k.play('sparkle', 82.8, { n: 6, gain: 0.5 });
    
    whoosh(SC.forest, 0.5); whoosh(SC.shore, 0.5); sea(SC.shore, SC.lanka, 0.3);
    whoosh(SC.leap, 0.6); k.play('riser', SC.leap, { dur: 2.4, gain: 0.5 }); k.noise(SC.leap + 0.2, { dur: 2.6, color: 'pink', filter: 'bandpass', f: [[0, 400], [1.3, 2200], [2.6, 500]], q: 0.8, gain: 0.3, a: 1.0, pan: -0.5 });
    thunder(SC.lanka, 0.6); fire(SC.lanka, SC.army + 0.5, 0.4);
    
    riser(SC.army); whoosh(SC.army, 0.5);
    for (let t = SC.army + 0.3; t < SC.battle; t += 0.235) step(t, (Math.floor(t * 4) % 3 - 1) * 0.4);
    sea(SC.army, SC.battle, 0.2);
    for (let t = 97.7; t < 100.6; t += 0.3) k.play('thud', t, { f: 110, gain: 0.25, minor: true, pan: (t - 97.7) / 2.9 * 1.2 - 0.6 }); 
    for (let t = 100.8; t < 103.0; t += 0.08) k.play('swish', t, { dur: 0.25, gain: 0.25, minor: true, pan: Math.sin(t * 7) * 0.6 }); 
    
    riser(SC.battle, 1.4, 0.7); thunder(SC.battle, 0.7);
    gong(lineT(38), 0.6, 65); gong(lineT(39), 0.7, 65); gong(lineT(40), 0.8, 73);
    k.tone(109.7, { f: [[0, 110], [1.6, 440]], type: 'triangle', dur: 2.0, gain: 0.08, a: 1.4, verb: 0.4 }); k.play('riser', 109.9, { dur: 1.7, gain: 0.6 });
    k.tone(111.6, { f: [[0, 900], [0.25, 180]], type: 'sawtooth', dur: 0.3, gain: 0.12, a: 0.003, filter: 'bandpass', f2: 900, q: 2 }); k.play('swish', 111.6, { dur: 0.45, gain: 0.8 }); 
    k.play('impact', 112.05, { f: 50, gain: 1.2 }); gong(112.05, 1.4, 55); k.play('sparkle', 112.1, { n: 10, gain: 0.8 });
    
    riser(SC.title, 1.0, 0.5); whoosh(SC.title, 0.5);
    gong(lineT(45), 1.5, 73); [0, 0.12, 0.24].forEach((d, i) => bell(lineT(45) + d, ['D6', 'A6', 'D7'][i], 1, (i - 1) * 0.4)); k.play('sparkle', lineT(45) + 0.2, { n: 12, gain: 1 });
    bell(lineT(46), 'F#5', 0.6, -0.3); bell(lineT(47), 'A5', 0.6, 0.3); bell(lineT(48), 'D6', 0.7, 0); gong(lineT(48), 0.8, 73);
    k.noise(D - 1.4, { dur: 1.6, color: 'brown', filter: 'lowpass', f: 200, gain: 0.12, a: 0.1 });
  }
