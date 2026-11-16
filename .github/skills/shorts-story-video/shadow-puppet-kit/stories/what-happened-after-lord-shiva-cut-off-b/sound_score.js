  function scoreSound(k0) {
    const from = window.SOUND_FROM || 0, live = (t) => t >= from - 0.001;
    const k = { ...k0, tone: (t, p) => live(t) && k0.tone(t, p), noise: (t, p) => live(t) && k0.noise(t, p) };
    
    k.tone(0, { f: 'D2', dur: 10, gain: 0.1, type: 'triangle' });
    k.tone(10, { f: 'A2', dur: 14, gain: 0.1, type: 'triangle' });
    k.tone(24, { f: 'B1', dur: 9, gain: 0.1, type: 'triangle' });
    k.tone(33, { f: 'D2', dur: 23, gain: 0.1, type: 'triangle' });
    k.tone(56, { f: 'G2', dur: 13, gain: 0.1, type: 'triangle' });
    k.tone(69, { f: 'D3', dur: 16, gain: 0.1, type: 'triangle' });
    k.tone(85, { f: 'D2', dur: 16, gain: 0.1, type: 'triangle' });
  }
