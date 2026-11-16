  const TITLE = 'THE CURSE OF BHAIRAVA';
  const HOOK = ['What happened after Shiva', "cut off Brahma's fifth head?"];
  const REEL_SUBTITLE = 'A story from Hindu mythology';

  const SC = { start: 0.0, consequence: 10.5, skull: 24.0, wander: 33.0, kashi: 56.5, liberation: 69.0, end: 85.0 };
  const FADE = 0.9;
  const REEL_FOCUS = {
    start: [640, 400],
    consequence: [640, 400],
    skull: [640, 400],
    wander: [640, 400],
    kashi: [640, 400],
    liberation: [640, 400],
    end: [640, 400],
  };
  const BEATS = [
    { n: 1, name: 'The Severing', t0: 0, t1: SC.consequence, vo: 'After Lord Shiva severed Brahma\'s fifth head...', screen: 'Shiva as Bhairava' },
    { n: 2, name: 'Brahmahatya', t0: SC.consequence, t1: SC.skull, vo: 'The sin of Brahmahatya followed him.', screen: 'The chasing spirit' },
    { n: 3, name: 'The Skull', t0: SC.skull, t1: SC.wander, vo: 'The skull stuck to his hand.', screen: 'Bhairava with skull' },
    { n: 4, name: 'The Ascetic', t0: SC.wander, t1: SC.kashi, vo: 'He wandered as a beggar.', screen: 'Wandering ascetic' },
    { n: 5, name: 'Kashi', t0: SC.kashi, t1: SC.liberation, vo: 'He reached the holy city of Kashi.', screen: 'Kashi skyline' },
    { n: 6, name: 'Liberation', t0: SC.liberation, t1: SC.end, vo: 'The skull fell and he was freed.', screen: 'Kapala Mochana' },
    { n: 7, name: 'Conclusion', t0: SC.end, t1: DURATION, vo: 'Kashi holds eternal grace.', screen: 'Title card' },
  ];

  function sceneStart(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.7);
    sun(c, 640, 300, 80, PAL.kumkum, 3);
    figure(c, { x: 640, y: 580, s: 1.2, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.kumkum });
    c.restore();
  }

  function sceneConsequence(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, DUSK);
    hills(c, W, Hh, 550, 60, PAL.maroon, 1);
    figure(c, { x: 500, y: 580, s: 1.0, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true });
    figure(c, { x: 800, y: 580, s: 1.0, dir: -1, skin: PAL.ink, cloth: PAL.kumkum, sash: PAL.gold, crown: 'none', face: 'woman' });
    c.restore();
  }

  function sceneSkull(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, NIGHT);
    figure(c, { x: 640, y: 580, s: 1.2, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, arms: [[-0.5, 0.3], [1.5, 1.5]] });
    c.fillStyle = PAL.sandal; c.beginPath(); c.arc(710, 500, 22, 0, TAU); c.fill();
    c.restore();
  }

  function sceneWander(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM);
    sun(c, 200, 250, 70, PAL.turmeric, 2);
    hills(c, W, Hh, 550, 40, PAL.burnt, 2);
    figure(c, { x: 640 + Math.sin(t) * 40, y: 580, s: 1.1, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'walk', ph: t });
    c.restore();
  }

  function sceneKashi(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM);
    sun(c, 640, 200, 100, PAL.turmeric, 3);
    skyline(c, 640, 560, 0.6, PAL.gold, t);
    ocean(c, W, Hh, 560, t, [PAL.rama, PAL.peacock]);
    c.restore();
  }

  function sceneLiberation(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM);
    rays(c, 640, 300, 100, 600, 20, PAL.cream, t, 0.3);
    temple(c, { x: 640, y: 560, s: 0.8, col: PAL.gold }, t);
    figure(c, { x: 640, y: 580, s: 1.1, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, glow: PAL.gold });
    c.restore();
  }

  function sceneEnd(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM);
    sun(c, 640, 350, 120, PAL.turmeric, 3);
    temple(c, { x: 640, y: 580, s: 0.9, col: PAL.brown }, t);
    c.restore();
  }

  const SCENES = [
    [SC.start, sceneStart],
    [SC.consequence, sceneConsequence],
    [SC.skull, sceneSkull],
    [SC.wander, sceneWander],
    [SC.kashi, sceneKashi],
    [SC.liberation, sceneLiberation],
    [SC.end, sceneEnd]
  ];
