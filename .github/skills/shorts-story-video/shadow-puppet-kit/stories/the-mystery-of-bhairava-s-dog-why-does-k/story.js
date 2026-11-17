const TITLE = "BHAIRAVA'S DOG";
const HOOK = ["The fierce guardian", "and his loyal companion."];
const REEL_SUBTITLE = "The Mystery of Bhairava's Dog";

const SC = { start: 0, guardian: 14.0, tradition: 25.0, protector: 39.7, offering: 47.9, fierce: 60.7, lesson: 68.6, future: 85.3 };
const FADE = 0.9;
const REEL_FOCUS = {
  start: [640, 420],
  guardian: [640, 420],
  tradition: [640, 430],
  protector: [640, 420],
  offering: [640, 430],
  fierce: [640, 420],
  lesson: [640, 430],
  future: [640, 400],
};
const BEATS = [
  { n: 1, name: 'Introduction', t0: 0, t1: SC.guardian, vo: 'Have you ever wondered why a fierce form of Lord Shiva is always associated with a dog?', screen: 'Shiva form and dog' },
  { n: 2, name: 'Kala Bhairava', t0: SC.guardian, t1: SC.tradition, vo: 'Kala Bhairava, the mighty guardian of Kashi, is traditionally depicted with a dog as his divine companion and vehicle.', screen: 'Kala Bhairava with dog' },
  { n: 3, name: 'Tradition', t0: SC.tradition, t1: SC.protector, vo: 'In Hindu tradition, the dog represents loyalty, alertness, protection, and unwavering devotion.', screen: 'Loyal dog symbol' },
  { n: 4, name: 'Protector', t0: SC.protector, t1: SC.offering, vo: 'Bhairava is also known as the protector of sacred places and the destroyer of negative forces.', screen: 'Protector Bhairava' },
  { n: 5, name: 'Offering', t0: SC.offering, t1: SC.fierce, vo: 'In many traditions, devotees offer food to dogs as an act of reverence to Kala Bhairava.', screen: 'Devotees offering food' },
  { n: 6, name: 'Fierce and Humble', t0: SC.fierce, t1: SC.lesson, vo: 'The fierce Bhairava teaches us courageâ¦ while his loyal companion reminds us of humility and faithfulness.', screen: 'Courage and humility' },
  { n: 7, name: 'The Lesson', t0: SC.lesson, t1: SC.future, vo: 'Together, they represent a powerful lesson: true strength is not only about defeating evilâ¦ it is also about protecting the vulnerable.', screen: 'Strength and protection' },
  { n: 8, name: 'Next Episode', t0: SC.future, t1: DURATION, vo: 'That is the story of our next episode.', screen: 'Title card' }
];

function sceneStart(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.7);
  sun(c, 640, 320, 100, PAL.maroon, 3);
  cloudBank(c, W, 240, t, { seed: 1, n: 4, fill: PAL.indigo, line: PAL.night, speed: 3 });
  hills(c, W, Hh, 540, 60, PAL.maroon, 1);
  hills(c, W, Hh, 620, 40, PAL.deep, 2);
  figure(c, { x: 560, y: 690, s: 1.3, dir: 1, skin: PAL.ash, cloth: PAL.tiger || PAL.maroon, sash: PAL.gold, crown: 'bun', tilak: true, pose: 'stand', glow: PAL.kesari });
  animal(c, { x: 740, y: 690, s: 1.2, kind: 'dog', col: PAL.sandal, pose: 'sit' });
  c.restore();
}

function sceneGuardian(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK);
  sun(c, 640, 280, 110, PAL.saffron, 3);
  cloudBank(c, W, 220, t, { seed: 2, n: 5, fill: PAL.burnt, line: PAL.saffron, speed: 4 });
  hills(c, W, Hh, 560, 70, PAL.burnt, 3);
  skyline(c, 640, 560, 0.5, PAL.deep, t);
  hills(c, W, Hh, 660, 30, PAL.deep, 4);
  figure(c, { x: 580, y: 700, s: 1.35, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.turmeric });
  animal(c, { x: 730, y: 700, s: 1.25, kind: 'dog', col: PAL.sandal, pose: 'stand' });
  c.restore();
}

function sceneTradition(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM);
  sun(c, 640, 300, 100, PAL.turmeric, 3);
  cloudBank(c, W, 250, t, { seed: 3, n: 4, fill: PAL.sandal, line: PAL.saffron, speed: 5 });
  hills(c, W, Hh, 580, 50, PAL.brown, 5);
  hills(c, W, Hh, 670, 30, PAL.deep, 6);
  animal(c, { x: 640, y: 700, s: 1.8, kind: 'dog', col: PAL.sandal, pose: 'stand', collar: PAL.gold });
  c.restore();
}

function sceneProtector(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK);
  sun(c, 640, 260, 120, PAL.kesari, 3);
  rays(c, 640, 260, 120, 600, 20, PAL.turmeric, t, 0.2);
  hills(c, W, Hh, 550, 80, PAL.maroon, 7);
  hills(c, W, Hh, 650, 40, PAL.deep, 8);
  figure(c, { x: 640, y: 700, s: 1.4, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.kesari });
  c.restore();
}

function sceneOffering(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM);
  sun(c, 640, 320, 90, PAL.marigold, 3);
  hills(c, W, Hh, 600, 50, PAL.brown, 9);
  hills(c, W, Hh, 680, 25, PAL.deep, 10);
  figure(c, { x: 450, y: 700, s: 1.1, dir: 1, skin: PAL.burnt, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', pose: 'kneel' });
  animal(c, { x: 750, y: 700, s: 1.3, kind: 'dog', col: PAL.sandal, pose: 'sit' });
  c.restore();
}

function sceneFierce(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT);
  sun(c, 640, 300, 100, PAL.maroon, 3);
  hills(c, W, Hh, 560, 60, PAL.indigo, 11);
  hills(c, W, Hh, 660, 35, PAL.deep, 12);
  figure(c, { x: 540, y: 700, s: 1.3, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'bun', tilak: true, pose: 'stand', glow: PAL.vermilion });
  animal(c, { x: 740, y: 700, s: 1.2, kind: 'dog', col: PAL.sandal, pose: 'sit' });
  c.restore();
}

function sceneLesson(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK);
  sun(c, 640, 280, 110, PAL.saffron, 3);
  hills(c, W, Hh, 570, 50, PAL.burnt, 13);
  hills(c, W, Hh, 670, 30, PAL.deep, 14);
  figure(c, { x: 560, y: 700, s: 1.3, dir: 1, skin: PAL.ash, cloth: PAL.maroon, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.turmeric });
  animal(c, { x: 720, y: 700, s: 1.25, kind: 'dog', col: PAL.sandal, pose: 'stand' });
  c.restore();
}

function sceneFuture(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM);
  sun(c, 640, 350, 140, PAL.turmeric, 3);
  rays(c, 640, 350, 140, 700, 24, PAL.cream, t, 0.2);
  hills(c, W, Hh, 600, 50, PAL.brown, 15);
  hills(c, W, Hh, 680, 30, PAL.deep, 16);
  temple(c, { x: 640, y: 680, s: 0.7, col: PAL.brown }, t);
  c.restore();
}

const SCENES = [
  [0, sceneStart],
  [SC.guardian, sceneGuardian],
  [SC.tradition, sceneTradition],
  [SC.protector, sceneProtector],
  [SC.offering, sceneOffering],
  [SC.fierce, sceneFierce],
  [SC.lesson, sceneLesson],
  [SC.future, sceneFuture]
];
