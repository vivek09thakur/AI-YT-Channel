  const TITLE = "BHAIRAVA'S DOG";
  const HOOK = ["The fierce guardian", "and his faithful companion."];
  const REEL_SUBTITLE = "The Mystery of Kala Bhairava";

  const SC = { cosmos: 0, bhairava: 13.0, tradition: 24.0, guardian: 37.0, reverence: 52.0, lessons: 67.0, future: 85.0 };
  const FADE = 0.9;
  const REEL_FOCUS = {
    cosmos: [640, 400],
    bhairava: [640, 420],
    tradition: [640, 400],
    guardian: [640, 410],
    reverence: [640, 420],
    lessons: [640, 400],
    future: [640, 400],
  };
  const BEATS = [
    { n: 1, name: 'Cosmos', t0: 0, t1: SC.bhairava, vo: 'Have you ever wondered why a fierce form of Lord Shiva is always associated with a dog?', screen: 'Night sky and stars' },
    { n: 2, name: 'Bhairava', t0: SC.bhairava, t1: SC.tradition, vo: 'Kala Bhairava, the mighty guardian of Kashi, is traditionally depicted with a dog as his divine companion and vehicle.', screen: 'Kala Bhairava with dog' },
    { n: 3, name: 'Tradition', t0: SC.tradition, t1: SC.guardian, vo: 'In Hindu tradition, the dog represents loyalty, alertness, protection...', screen: 'Loyalty and alertness' },
    { n: 4, name: 'Guardian', t0: SC.guardian, t1: SC.reverence, vo: 'Bhairava is also known as the protector of sacred places and the destroyer of negative forces.', screen: 'Protector and destroyer' },
    { n: 5, name: 'Reverence', t0: SC.reverence, t1: SC.lessons, vo: 'In many traditions, devotees offer food to dogs as an act of reverence...', screen: 'Devotees and dogs' },
    { n: 6, name: 'Lessons', t0: SC.lessons, t1: SC.future, vo: 'Together, they represent a powerful lesson: true strength is protecting the vulnerable.', screen: 'Strength and humility' },
    { n: 7, name: 'Future', t0: SC.future, t1: 100.67, vo: 'Why do devotees worship him on Ashtami? That is the story of our next episode.', screen: 'Ashtami moon' },
  ];

  function sceneCosmos(c, W, Hh, t) {
    sky(c, W, Hh, NIGHT);
    stars(c, W, Hh, t, 0.7);
    streaks(c, W, Hh, t, { color: PAL.ash, alpha: 0.15, seed: 1 });
    sun(c, 640, 320, 90, PAL.maroon, 4);
    hills(c, W, Hh, 560, 80, PAL.indigo, 1);
    hills(c, W, Hh, 630, 60, PAL.night, 2);
  }

  function sceneBhairava(c, W, Hh, t) {
    sky(c, W, Hh, DUSK);
    streaks(c, W, Hh, t, { color: PAL.gold, alpha: 0.2, seed: 3 });
    sun(c, 640, 280, 110, PAL.kesari, 3);
    hills(c, W, Hh, 580, 70, PAL.maroon, 3);
    
    // Kala Bhairava figure (Shiva form: ash/sandal skin, crescent crown, trident/staff)
    figure(c, {
      x: 640, y: 700, s: 1.2, dir: 1,
      skin: PAL.ash, cloth: PAL.tiger || PAL.maroon, sash: PAL.gold,
      crown: 'tall', tilak: true, pose: 'stand',
      arms: [[-0.8, -0.4], [0.5, 0.6]], glow: PAL.kesari
    });
    
    // Loyal Dog beside him
    c.save();
    c.translate(520, 690);
    c.fillStyle = PAL.brown;
    c.beginPath(); c.ellipse(0, 0, 45, 25, 0, 0, TAU); c.fill(); // body
    c.beginPath(); c.arc(35, -20, 18, 0, TAU); c.fill(); // head
    c.fillRect(25, -5, 8, 30); c.fillRect(-30, -5, 8, 30);
    c.restore();

    hills(c, W, Hh, 680, 40, PAL.deep, 4);
  }

  function sceneTradition(c, W, Hh, t) {
    sky(c, W, Hh, WARM);
    sun(c, 300, 240, 100, PAL.turmeric, 3);
    cloudBank(c, W, 220, t, { seed: 5, n: 4, fill: PAL.sandal, line: PAL.saffron, speed: 4 });
    hills(c, W, Hh, 550, 60, PAL.burnt, 5);
    
    // Temple pavilion in background
    temple(c, { x: 640, y: 550, s: 0.7, col: PAL.brown }, t);
    
    // Dog symbol of loyalty
    c.save();
    c.translate(640, 660);
    c.fillStyle = PAL.sandal;
    c.beginPath(); c.arc(0, -40, 40, 0, TAU); c.fill();
    lotus(c, 0, -40, 1.2, PAL.lotus, PAL.cream);
    c.restore();

    hills(c, W, Hh, 670, 30, PAL.deep, 6);
  }

  function sceneGuardian(c, W, Hh, t) {
    sky(c, W, Hh, DUSK);
    streaks(c, W, Hh, t, { seed: 7, alpha: 0.18 });
    sun(c, 980, 260, 120, PAL.vermilion, 3);
    skyline(c, 640, 580, 0.6, PAL.maroon, t);
    hills(c, W, Hh, 600, 50, PAL.deep, 7);

    figure(c, {
      x: 640, y: 700, s: 1.1, dir: 1,
      skin: PAL.ash, cloth: PAL.burnt, sash: PAL.gold,
      crown: 'tall', tilak: true, pose: 'aim', draw: 0.6, glow: PAL.vermilion
    });
    hills(c, W, Hh, 680, 25, PAL.ink, 8);
  }

  function sceneReverence(c, W, Hh, t) {
    sky(c, W, Hh, WARM);
    sun(c, 640, 220, 130, PAL.turmeric, 3);
    cloudBank(c, W, 200, t, { seed: 9, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5 });
    hills(c, W, Hh, 580, 60, PAL.brown, 9);

    // Devotee offering food
    figure(c, {
      x: 480, y: 700, s: 0.9, dir: 1,
      skin: PAL.burnt, cloth: PAL.turmeric, sash: PAL.gold,
      crown: 'cap', pose: 'kneel'
    });
    
    // Dog receiving
    c.save();
    c.translate(720, 690);
    c.fillStyle = PAL.brown;
    c.beginPath(); c.ellipse(0, 0, 40, 22, 0, 0, TAU); c.fill();
    c.beginPath(); c.arc(30, -16, 15, 0, TAU); c.fill();
    c.restore();

    hills(c, W, Hh, 670, 30, PAL.deep, 10);
  }

  function sceneLessons(c, W, Hh, t) {
    sky(c, W, Hh, WARM);
    streaks(c, W, Hh, t, { seed: 11, alpha: 0.2 });
    sun(c, 640, 300, 100, PAL.marigold, 3);
    hills(c, W, Hh, 560, 70, PAL.burnt, 11);

    figure(c, {
      x: 520, y: 700, s: 1.0, dir: 1,
      skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold,
      crown: 'tall', tilak: true, pose: 'stand'
    });

    figure(c, {
      x: 760, y: 700, s: 0.9, dir: -1,
      skin: PAL.kesari, cloth: PAL.cream, sash: PAL.tulsi,
      crown: 'bun', pose: 'stand'
    });

    hills(c, W, Hh, 670, 30, PAL.deep, 12);
  }

  function sceneFuture(c, W, Hh, t) {
    sky(c, W, Hh, NIGHT);
    stars(c, W, Hh, t, 0.8);
    sun(c, 640, 320, 140, PAL.gold, 3.5);
    rays(c, 640, 320, 140, 600, 20, PAL.cream, t, 0.15);
    hills(c, W, Hh, 580, 80, PAL.indigo, 13);
    
    lotus(c, 640, 520, 1.8, PAL.lotus, PAL.cream);

    hills(c, W, Hh, 680, 30, PAL.night, 14);
  }

  const SCENES = [
    [0, sceneCosmos],
    [SC.bhairava, sceneBhairava],
    [SC.tradition, sceneTradition],
    [SC.guardian, sceneGuardian],
    [SC.reverence, sceneReverence],
    [SC.lessons, sceneLessons],
    [SC.future, sceneFuture]
  ];
