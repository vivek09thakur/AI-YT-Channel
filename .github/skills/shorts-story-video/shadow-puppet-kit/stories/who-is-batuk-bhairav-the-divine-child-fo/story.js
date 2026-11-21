const TITLE = 'BATUK BHAIRAV';
const HOOK = ['The child form of Lord Shiva,', 'protector of the fearless.'];
const REEL_SUBTITLE = 'A story of divine courage';

const SC = { child: 0, form: 7.8, fierce: 14.2, protect: 25.5, worship: 34.0, days: 47.5, title: 62.0 };
const FADE = 0.9;
const REEL_FOCUS = {
  open: [640, 400],
  child: [640, 420],
  form: [640, 420],
  fierce: [640, 400],
  protect: [640, 420],
  worship: [640, 420],
  days: [640, 420],
  title: [640, 450],
};
const BEATS = [
  { n: 1, name: 'Child Form', t0: 0, t1: SC.form, vo: 'Did you know that Lord Shiva has a form in which he appears as a young child? This divine form is known as Batuk Bhairav.', screen: 'Young Shiva child with dog under night sky' },
  { n: 2, name: 'Fierce Manifestation', t0: SC.form, t1: SC.protect, vo: 'Batuk Bhairav is considered the child form of Lord Bhairav, a fierce manifestation of Lord Shiva symbolizing protection and courage.', screen: 'Shiva cosmic glow and protection symbols' },
  { n: 3, name: 'Protection', t0: SC.protect, t1: SC.worship, vo: 'According to Hindu beliefs, Lord Shiva manifested to destroy evil. Batuk Bhairav represents the gentler, childlike aspect of this energy.', screen: 'Batuk Bhairav with gentle light and dog' },
  { n: 4, name: 'Worship', t0: SC.worship, t1: SC.days, vo: 'Worshipping him protects devotees from fear, negative energies, and obstacles, bringing courage, peace, and prosperity.', screen: 'Devotee praying with oil lamp and divine glow' },
  { n: 5, name: 'Auspicious Days', t0: SC.days, t1: SC.title, vo: 'Devotees worship Batuk Bhairav on Sundays, Tuesdays, and Ashtami, remembering that divine protection is always with the faithful.', screen: 'Temple pavilion at dusk with flags' },
  { n: 6, name: 'Title', t0: SC.title, t1: DURATION, vo: 'Jai Batuk Bhairav!', screen: 'Title card BATUK BHAIRAV' },
];

function sceneChild(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.7);
  sun(c, 640, 420, 100, PAL.kesari, 3.5);
  cloudBank(c, W, 260, t, { seed: 1, n: 4, fill: PAL.maroon, line: PAL.night, speed: 4 });
  hills(c, W, Hh, 560, 60, PAL.maroon, 1);
  hills(c, W, Hh, 630, 40, PAL.deep, 2);
  // Young divine child (Batuk Bhairav) with a dog vahana
  figure(c, { x: 640, y: 700, s: 1.1, dir: 1, skin: PAL.sandal, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', tilak: true, glow: PAL.kesari, pose: 'stand', arms: [[-0.3, 0.5], [0.3, 0.5]] });
  animal(c, { x: 530, y: 700, s: 0.9, kind: 'dog', col: PAL.cream, pose: 'sit' });
  c.restore();
}

function sceneForm(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 5 });
  sun(c, 640, 300, 120, PAL.turmeric, 3);
  rays(c, 640, 300, 120, 700, 20, PAL.cream, t, 0.2);
  hills(c, W, Hh, 580, 50, PAL.brown, 3);
  figure(c, { x: 640, y: 700, s: 1.3, dir: 1, skin: PAL.sandal, cloth: PAL.kumkum, sash: PAL.gold, crown: 'tall', tilak: true, glow: PAL.turmeric, pose: 'stand' });
  c.restore();
}

function sceneFierce(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 12, color: PAL.lotus });
  sun(c, 640, 340, 90, PAL.vermilion, 3);
  cloudBank(c, W, 240, t, { seed: 4, n: 5, fill: PAL.maroon, line: PAL.night, speed: 6 });
  hills(c, W, Hh, 600, 70, PAL.deep, 4);
  figure(c, { x: 640, y: 700, s: 1.35, dir: 1, skin: PAL.ash, cloth: PAL.ink, sash: PAL.kumkum, crown: 'tall', tilak: true, glow: PAL.vermilion, pose: 'stand', arms: [[-0.6, -0.6], [0.6, -0.6]] });
  animal(c, { x: 780, y: 700, s: 1.0, kind: 'dog', col: PAL.ash, pose: 'stand', ph: t * 3 });
  c.restore();
}

function sceneProtect(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 8 });
  sun(c, 640, 280, 110, PAL.turmeric, 3);
  hills(c, W, Hh, 580, 60, PAL.burnt, 5);
  figure(c, { x: 640, y: 700, s: 1.25, dir: 1, skin: PAL.sandal, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', tilak: true, glow: PAL.kesari, pose: 'stand' });
  animal(c, { x: 510, y: 700, s: 0.95, kind: 'dog', col: PAL.cream, pose: 'sit' });
  c.restore();
}

function sceneWorship(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 9 });
  sun(c, 640, 320, 100, PAL.marigold, 3);
  hills(c, W, Hh, 560, 50, PAL.brown, 6);
  temple(c, { x: 640, y: 560, s: 0.65, col: PAL.brown }, t);
  figure(c, { x: 640, y: 700, s: 1.2, dir: 1, skin: PAL.sandal, cloth: PAL.kumkum, sash: PAL.gold, crown: 'bun', tilak: true, pose: 'namaste' });
  c.restore();
}

function sceneDays(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 15 });
  sun(c, 640, 300, 100, PAL.turmeric, 3);
  hills(c, W, Hh, 550, 60, PAL.burnt, 7);
  skyline(c, 640, 550, 0.5, PAL.deep, t);
  [-300, 300].forEach((dx, i) => flag(c, 640 + dx, 550, 110, i ? PAL.saffron : PAL.kumkum, t, i ? -1 : 1));
  figure(c, { x: 640, y: 700, s: 1.2, dir: 1, skin: PAL.sandal, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', tilak: true, glow: PAL.turmeric, pose: 'stand' });
  c.restore();
}

function sceneTitle(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 20, n: 100, alpha: 0.25 });
  sun(c, 640, 400, 120, PAL.turmeric, 3);
  hills(c, W, Hh, 580, 60, PAL.burnt, 8);
  temple(c, { x: 640, y: 600, s: 0.6, col: PAL.brown }, t);
  figure(c, { x: 640, y: 700, s: 1.2, dir: 1, skin: PAL.sandal, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'tall', tilak: true, glow: PAL.kesari, pose: 'stand' });
  c.restore();
}

const SCENES = [
  [0, sceneChild],
  [SC.form, sceneForm],
  [SC.fierce, sceneFierce],
  [SC.protect, sceneProtect],
  [SC.worship, sceneWorship],
  [SC.days, sceneDays],
  [SC.title, sceneTitle]
];
