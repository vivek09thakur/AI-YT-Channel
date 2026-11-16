  const TITLE = 'THE GUARDIAN OF KASHI';
  const HOOK = ['The fierce protector', 'of the sacred city.'];
  const REEL_SUBTITLE = 'The legend of Kala Bhairava';

  const SC = { curse: 0, shiva: 10.0, kashi: 18.0, kotwal: 30.0, protector: 40.0, temple: 60.0, mystery: 82.0 };
  const FADE = 0.9;
  const REEL_FOCUS = {
    curse: [640, 420],
    shiva: [640, 400],
    kashi: [640, 420],
    kotwal: [640, 400],
    protector: [640, 420],
    temple: [640, 420],
    mystery: [640, 400],
  };
  const BEATS = [
    { n: 1, name: 'Curse', t0: 0, t1: SC.shiva, vo: 'After escaping the terrible curse of Brahmahatya... Kala Bhairava was finally free. But his journey was not over.', screen: 'Bhairava freed from curse' },
    { n: 2, name: 'Shiva', t0: SC.shiva, t1: SC.kashi, vo: 'Lord Shiva had chosen a new destiny for him. Bhairava would become the eternal guardian of Kashi...', screen: 'Shiva gives destiny' },
    { n: 3, name: 'Kashi', t0: SC.kashi, t1: SC.kotwal, vo: 'the sacred city of liberation. A city where even death could lead to freedom... required a powerful protector. And that protector would be Kala Bhairava.', screen: 'Kashi city view' },
    { n: 4, name: 'Kotwal', t0: SC.kotwal, t1: SC.protector, vo: 'From that moment onward... Bhairava became known as the Kotwal of Kashi... the divine guardian who watches over the sacred city.', screen: 'Kotwal guardianship' },
    { n: 5, name: 'Protector', t0: SC.protector, t1: SC.temple, vo: 'He protects its boundaries... watches over its devotees... and ensures that the sacred laws of the city remain unbroken. His fierce appearance hides a deeper purpose.', screen: 'Protector of devotees' },
    { n: 6, name: 'Temple', t0: SC.temple, t1: SC.mystery, vo: 'Even today... devotees visit the famous Kala Bhairava Temple in Varanasi...', screen: 'Kala Bhairava Temple' },
    { n: 7, name: 'Mystery', t0: SC.mystery, t1: DURATION, vo: 'That is the story of our next episode.', screen: 'Closing mystery' },
  ];

  function sceneCurse(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.7);
    streaks(c, W, Hh, t, { color: PAL.kumkum, alpha: 0.15, seed: 1 });
    sun(c, 640, 300, 100, PAL.maroon, 3);
    hills(c, W, Hh, 560, 70, PAL.maroon, 2);
    hills(c, W, Hh, 620, 50, PAL.deep, 3);
    figure(c, { x: 640, y: 650, s: 1.1, dir: 1, skin: PAL.ash, cloth: PAL.ink, sash: PAL.kumkum, crown: 'tall', tilak: true, pose: 'stand' });
    c.restore();
  }

  function sceneShiva(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 4 });
    sun(c, 640, 240, 120, PAL.turmeric, 3);
    cloudBank(c, W, 200, t, { seed: 5, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5 });
    hills(c, W, Hh, 560, 60, PAL.brown, 6);
    figure(c, { x: 500, y: 650, s: 1.0, dir: 1, skin: PAL.ash, cloth: PAL.cream, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand' });
    figure(c, { x: 780, y: 650, s: 1.0, dir: -1, skin: PAL.rama, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', tilak: true, pose: 'stand' });
    c.restore();
  }

  function sceneKashi(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 7 });
    sun(c, 640, 220, 110, PAL.marigold, 3);
    skyline(c, 640, 560, 0.6, PAL.brown, t);
    ocean(c, W, Hh, 560, t, [PAL.rama, PAL.peacock, PAL.indigo]);
    hills(c, W, Hh, 660, 30, PAL.deep, 8);
    c.restore();
  }

  function sceneKotwal(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 9 });
    sun(c, 640, 260, 100, PAL.kesari, 3);
    skyline(c, 640, 580, 0.5, PAL.deep, t);
    figure(c, { x: 640, y: 660, s: 1.2, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.kesari });
    c.restore();
  }

  function sceneProtector(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 11 });
    sun(c, 640, 250, 90, PAL.turmeric, 3);
    hills(c, W, Hh, 560, 50, PAL.brown, 12);
    temple(c, { x: 640, y: 580, s: 0.7, col: PAL.brown }, t);
    figure(c, { x: 500, y: 670, s: 0.9, dir: 1, skin: PAL.burnt, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'cap', pose: 'stand' });
    figure(c, { x: 780, y: 670, s: 0.9, dir: -1, skin: PAL.sandal, cloth: PAL.marigold, sash: PAL.lotus, crown: 'long', face: 'woman', pose: 'stand' });
    c.restore();
  }

  function sceneTemple(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 13 });
    sun(c, 640, 220, 100, PAL.turmeric, 3);
    temple(c, { x: 640, y: 580, s: 0.8, col: PAL.brown }, t);
    figure(c, { x: 640, y: 670, s: 1.0, dir: 1, skin: PAL.ash, cloth: PAL.kumkum, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'namaste' });
    c.restore();
  }

  function sceneMystery(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.8);
    streaks(c, W, Hh, t, { color: PAL.lotus, alpha: 0.15, seed: 15 });
    sun(c, 640, 320, 90, PAL.marigold, 3);
    hills(c, W, Hh, 580, 60, PAL.maroon, 16);
    title(c, TITLE, 640, 360, 64, PAL.gold, { glow: PAL.kesari, blur: 30, stroke: PAL.deep, strokeW: 8 });
    c.restore();
  }

  const SCENES = [
    [0, sceneCurse],
    [SC.shiva, sceneShiva],
    [SC.kashi, sceneKashi],
    [SC.kotwal, sceneKotwal],
    [SC.protector, sceneProtector],
    [SC.temple, sceneTemple],
    [SC.mystery, sceneMystery]
  ];
