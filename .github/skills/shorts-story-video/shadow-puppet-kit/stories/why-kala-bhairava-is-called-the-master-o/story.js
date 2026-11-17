// Kala Bhairava - Master of Time animated story video

const TITLE = 'KALA BHAIRAVA';
const HOOK = ['The Master of Time', 'and eternal truth.'];
const REEL_SUBTITLE = 'Lord of Time & Destiny';

const SC = {
  intro: 0,
  bhairavaLord: 3.2,
  divineForce: 8.4,
  kalaMeaning: 16.9,
  impermanence: 29.5,
  beyondTime: 41.8,
  fierceForm: 54.5,
  kashi: 62.0,
  dharmaLesson: 74.0,
  eternalReality: 87.8,
  ultimateLord: 93.4,
  companionDog: 102.3,
  mysteryOutro: 111.4
};

const FADE = 0.9;

const REEL_FOCUS = {
  open: [640, 390],
  intro: [640, 390],
  bhairavaLord: [640, 420],
  divineForce: [640, 410],
  kalaMeaning: [640, 420],
  impermanence: (t) => [lerp(460, 820, sm(29.5, 38.5, t)), 420],
  beyondTime: [640, 410],
  fierceForm: [640, 430],
  kashi: (t) => [lerp(560, 720, sm(62.0, 70.0, t)), 430],
  dharmaLesson: [640, 420],
  eternalReality: [640, 410],
  ultimateLord: [640, 430],
  companionDog: [640, 440],
  mysteryOutro: [640, 420]
};

const BEATS = [
  { n: 1, name: 'The Cosmic Wheel', t0: 0, t1: SC.bhairavaLord, vo: 'What if time itself had a master?', screen: 'A colossal cosmic wheel of time spins across the starry indigo heavens.' },
  { n: 2, name: 'Kala Bhairava Awakens', t0: SC.bhairavaLord, t1: SC.divineForce, vo: 'In Hindu tradition, Kala Bhairava is worshipped as the Lord of Timeâ¦', screen: 'Kala Bhairava stands luminous with crescent moon and trident staff.' },
  { n: 3, name: 'Beyond Birth and Death', t0: SC.divineForce, t1: SC.kalaMeaning, vo: 'the divine force beyond birth, death, and destruction...', screen: 'Lotus of eternity unfurls as cosmic cycles cycle behind him.' },
  { n: 4, name: 'The Dual Meaning of Kala', t0: SC.kalaMeaning, t1: SC.impermanence, vo: 'The word Kala carries a powerful meaning. It represents timeâ¦ and death.', screen: 'Golden sundial and twilight eclipse split into time and mortal ends.' },
  { n: 5, name: 'Impermanence of Worlds', t0: SC.impermanence, t1: SC.beyondTime, vo: 'Kings rise, empires fall, stars are born, worlds disappear.', screen: 'Crown falls from crumbling palace spires into river of ashes.' },
  { n: 6, name: 'Beyond Limitations', t0: SC.beyondTime, t1: SC.fierceForm, vo: 'Kala Bhairava stands beyond these mortal limitations.', screen: 'Unmoving guardian standing steadfast as time stream bends around him.' },
  { n: 7, name: 'The Fierce Aspect', t0: SC.fierceForm, t1: SC.kashi, vo: 'In his fierce form, Bhairava destroys arrogance and illusion.', screen: 'Flames of transformation dispel shadows of ego and ignorance.' },
  { n: 8, name: 'Guardian of Kashi', t0: SC.kashi, t1: SC.dharmaLesson, vo: 'Worshipped as the guardian of Kashi, the sacred city of liberation.', screen: 'The ghats and temple domes of Kashi glowing along the sacred Ganga.' },
  { n: 9, name: 'The Lesson of Dharma', t0: SC.dharmaLesson, t1: SC.eternalReality, vo: 'Do not waste time. Follow dharma and overcome your ego.', screen: 'Devotee walks the golden path towards luminous truth.' },
  { n: 10, name: 'The Eternal Reality', t0: SC.eternalReality, t1: SC.ultimateLord, vo: 'Everything is temporary, but the eternal reality can never be destroyed.', screen: 'Golden radiant sun and sacred lingam anchored in stillness.' },
  { n: 11, name: 'The Title of Bhairava', t0: SC.ultimateLord, t1: SC.companionDog, vo: 'That is why devotees remember him as Kala Bhairavaâ¦', screen: 'Grand poster shot of Lord Bhairava crowned in temple gold.' },
  { n: 12, name: 'The Sacred Companion', t0: SC.companionDog, t1: SC.mysteryOutro, vo: 'Why is a dog always seen beside him?', screen: 'Shiva Bhairava with his devoted canine vehicle, the black dog Shvana.' },
  { n: 13, name: 'The Mystery Continues', t0: SC.mysteryOutro, t1: DURATION, vo: 'That is the mystery we will uncover in the next episode.', screen: 'Temple gate closing at twilight with temple lamps burning.' }
];

// Helper: Custom Dog (Shvana, the sacred vahana of Bhairava)
function hound(c, x, y, s, dir, col) {
  c.save();
  c.translate(x, y);
  c.scale(s * (dir || 1), s);
  c.fillStyle = col || PAL.ink;
  c.strokeStyle = col || PAL.ink;
  // Body
  c.beginPath();
  c.ellipse(0, -42, 48, 26, -0.08, 0, TAU);
  c.fill();
  // Chest and neck
  c.beginPath();
  c.moveTo(20, -56);
  c.quadraticCurveTo(40, -78, 48, -96);
  c.lineTo(34, -100);
  c.quadraticCurveTo(18, -75, 4, -58);
  c.closePath();
  c.fill();
  // Head
  c.beginPath();
  c.ellipse(48, -100, 18, 14, 0.2, 0, TAU);
  c.fill();
  // Snout
  c.beginPath();
  c.moveTo(56, -104);
  c.lineTo(76, -96);
  c.lineTo(60, -88);
  c.closePath();
  c.fill();
  // Pointed ears
  c.beginPath();
  c.moveTo(42, -112);
  c.lineTo(46, -132);
  c.lineTo(54, -114);
  c.closePath();
  c.fill();
  // Eye
  c.fillStyle = PAL.turmeric;
  c.beginPath();
  c.arc(52, -102, 2.8, 0, TAU);
  c.fill();
  c.fillStyle = col || PAL.ink;
  // Legs
  c.lineWidth = 11;
  c.lineCap = 'round';
  // Front legs
  c.beginPath();
  c.moveTo(26, -38);
  c.lineTo(32, -6);
  c.stroke();
  c.beginPath();
  c.moveTo(38, -40);
  c.lineTo(44, -4);
  c.stroke();
  // Back legs
  c.beginPath();
  c.moveTo(-28, -42);
  c.quadraticCurveTo(-44, -20, -38, -6);
  c.stroke();
  c.beginPath();
  c.moveTo(-18, -40);
  c.quadraticCurveTo(-30, -20, -22, -4);
  c.stroke();
  // Upcurled tail
  c.lineWidth = 7;
  c.beginPath();
  c.moveTo(-44, -48);
  c.quadraticCurveTo(-72, -80, -54, -96);
  c.quadraticCurveTo(-42, -104, -34, -90);
  c.stroke();
  // Red collar
  c.strokeStyle = PAL.kumkum;
  c.lineWidth = 4;
  c.beginPath();
  c.moveTo(34, -90);
  c.lineTo(44, -82);
  c.stroke();
  c.restore();
}

// Helper: Trishula (Trident staff)
function trishula(c, x, y, s, col, ang) {
  c.save();
  c.translate(x, y);
  c.rotate(ang || 0);
  c.scale(s, s);
  c.strokeStyle = col || PAL.brass;
  c.fillStyle = col || PAL.brass;
  c.lineWidth = 6;
  // Main long shaft
  c.beginPath();
  c.moveTo(0, 120);
  c.lineTo(0, -180);
  c.stroke();
  // Central spear point
  c.beginPath();
  c.moveTo(-8, -180);
  c.lineTo(0, -230);
  c.lineTo(8, -180);
  c.closePath();
  c.fill();
  // Side prongs
  c.beginPath();
  c.moveTo(0, -165);
  c.quadraticCurveTo(-28, -165, -30, -195);
  c.lineTo(-24, -215);
  c.lineTo(-32, -218);
  c.lineTo(-38, -190);
  c.quadraticCurveTo(-34, -150, 0, -150);
  c.closePath();
  c.fill();

  c.beginPath();
  c.moveTo(0, -165);
  c.quadraticCurveTo(28, -165, 30, -195);
  c.lineTo(24, -215);
  c.lineTo(32, -218);
  c.lineTo(38, -190);
  c.quadraticCurveTo(34, -150, 0, -150);
  c.closePath();
  c.fill();
  // Damaru drum attached to staff
  c.fillStyle = PAL.sandal;
  c.beginPath();
  c.moveTo(-14, -135);
  c.lineTo(14, -135);
  c.lineTo(-14, -105);
  c.lineTo(14, -105);
  c.closePath();
  c.fill();
  c.strokeStyle = PAL.kumkum;
  c.lineWidth = 2.5;
  c.strokeRect(-15, -135, 30, 30);
  c.restore();
}

// Helper: Wheel of Time (Kalachakra)
function timeWheel(c, x, y, r, t, col) {
  c.save();
  c.translate(x, y);
  c.rotate(t * 0.12);
  c.strokeStyle = col || PAL.gold;
  c.fillStyle = col || PAL.gold;
  c.lineWidth = 8;
  c.beginPath();
  c.arc(0, 0, r, 0, TAU);
  c.stroke();
  c.lineWidth = 4;
  c.beginPath();
  c.arc(0, 0, r * 0.82, 0, TAU);
  c.stroke();
  c.beginPath();
  c.arc(0, 0, r * 0.22, 0, TAU);
  c.fill();
  const spokes = 12;
  for (let i = 0; i < spokes; i++) {
    const a = (i * TAU) / spokes;
    c.beginPath();
    c.moveTo(0, 0);
    c.lineTo(Math.cos(a) * r, Math.sin(a) * r);
    c.stroke();
    // Markers on rim
    c.beginPath();
    c.arc(Math.cos(a) * (r * 0.91), Math.sin(a) * (r * 0.91), 5, 0, TAU);
    c.fill();
  }
  c.restore();
}

// Helper: Sacred Ganga River Ghat Steps
function ghatSteps(c, W, y, steps, col) {
  c.save();
  c.fillStyle = col || PAL.brown;
  for (let i = 0; i < steps; i++) {
    const yy = y + i * 16;
    c.fillRect(0, yy, W, 17);
    c.fillStyle = mixc(col || PAL.brown, PAL.cream, 0.08);
    c.fillRect(0, yy, W, 3);
    c.fillStyle = col || PAL.brown;
  }
  c.restore();
}

// Helper: Glowing Lingam
function shivalinga(c, x, y, s, t) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  // Base Yoni
  c.fillStyle = PAL.deep;
  c.beginPath();
  c.roundRect(-70, -20, 140, 28, 8);
  c.fill();
  c.beginPath();
  c.moveTo(50, -10);
  c.lineTo(110, -4);
  c.lineTo(105, 12);
  c.lineTo(40, 10);
  c.closePath();
  c.fill();
  // Cylindrical Lingam
  c.fillStyle = PAL.ink;
  c.beginPath();
  c.arc(0, -68, 38, Math.PI, 0, false);
  c.lineTo(38, -14);
  c.lineTo(-38, -14);
  c.closePath();
  c.fill();
  // Tripundra marks (Three sacred horizontal ash lines)
  c.strokeStyle = PAL.ash;
  c.lineWidth = 3.5;
  [-74, -66, -58].forEach((ly) => {
    c.beginPath();
    c.moveTo(-20, ly);
    c.lineTo(20, ly);
    c.stroke();
  });
  // Central red bindu
  c.fillStyle = PAL.kumkum;
  c.beginPath();
  c.arc(0, -66, 4.5, 0, TAU);
  c.fill();
  // Aura
  const g = c.createRadialGradient(0, -66, 20, 0, -66, 110);
  g.addColorStop(0, H.rgba(PAL.turmeric, 0.45));
  g.addColorStop(1, H.rgba(PAL.turmeric, 0));
  c.fillStyle = g;
  c.fillRect(-120, -180, 240, 240);
  c.restore();
}

// Scene 1: Intro - Cosmic Wheel of Time
function sceneIntro(c, W, Hh, t) {
  c.save();
  cam(c, W, Hh, 0.05 * sm(0, SC.bhairavaLord, t));
  sky(c, W, Hh, NIGHT);
  stars(c, W, Hh, t, 0.85);
  streaks(c, W, Hh, t, { color: PAL.amber, alpha: 0.16, seed: 1 });
  sun(c, 640, 360, 90, PAL.kesari, 3.8);
  timeWheel(c, 640, 360, 260, t, PAL.gold);
  cloudBank(c, W, 220, t, { seed: 12, n: 4, fill: PAL.indigo, line: PAL.maroon, speed: 5 });
  hills(c, W, Hh, 570, 70, PAL.maroon, 11);
  hills(c, W, Hh, 630, 50, PAL.deep, 12);
  c.restore();
}

// Scene 2: Lord of Time Awakens
function sceneBhairavaLord(c, W, Hh, t) {
  const u = sm(SC.bhairavaLord, SC.divineForce, t);
  c.save();
  cam(c, W, Hh, 0.04 * u);
  sky(c, W, Hh, mixStops(NIGHT, WARM, 0.45));
  stars(c, W, Hh, t, 0.5);
  streaks(c, W, Hh, t, { color: PAL.saffron, alpha: 0.18, seed: 2 });
  sun(c, 640, 320, 130, PAL.turmeric, 3.2);
  rays(c, 640, 320, 140, 720, 26, PAL.cream, t, 0.18);
  timeWheel(c, 640, 320, 210, t * 0.7, mixc(PAL.gold, PAL.amber, 0.5));
  hills(c, W, Hh, 560, 60, PAL.maroon, 13);
  hills(c, W, Hh, 620, 45, PAL.brown, 14);

  // Bhairava figure (Shiva avatar, ash skin, trident, crescent halo)
  const by = 670;
  figure(c, {
    x: 640,
    y: by,
    s: 1.35,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    glow: PAL.amber,
    arms: [[-1.2, 0.4], [0.35, 0.8]]
  });
  trishula(c, 715, by - 65, 0.9, PAL.brass, -0.08);

  // Shvana dog beside him
  hound(c, 520, by - 5, 0.75, 1, PAL.ink);
  hills(c, W, Hh, 680, 20, PAL.deep, 15);
  c.restore();
}

// Scene 3: Beyond Birth, Death & Destruction
function sceneDivineForce(c, W, Hh, t) {
  const tt = t - SC.divineForce;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.divineForce, SC.kalaMeaning, t));
  sky(c, W, Hh, DUSK);
  streaks(c, W, Hh, t, { seed: 4, alpha: 0.22 });
  sun(c, 640, 260, 110, PAL.marigold, 3.4);
  rays(c, 640, 260, 120, 800, 32, PAL.turmeric, t, 0.25);
  cloudBank(c, W, 210, t, { seed: 15, n: 5, fill: PAL.sandal, line: PAL.burnt, speed: 7 });

  // Expanding lotuses representing birth, existence, transformation
  const p1 = pop(t, SC.divineForce + 0.4, 0.8);
  const p2 = pop(t, SC.divineForce + 1.2, 0.8);
  const p3 = pop(t, SC.divineForce + 2.0, 0.8);
  if (p1 > 0) lotus(c, 360, 560, 1.1 * p1, PAL.lotus, PAL.cream);
  if (p2 > 0) lotus(c, 640, 530, 1.4 * p2, PAL.gold, PAL.turmeric);
  if (p3 > 0) lotus(c, 920, 560, 1.1 * p3, PAL.vermilion, PAL.kumkum);

  hills(c, W, Hh, 570, 50, PAL.burnt, 16);
  hills(c, W, Hh, 640, 35, PAL.brown, 17);
  figure(c, {
    x: 640,
    y: 670,
    s: 1.25,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.maroon,
    sash: PAL.gold,
    crown: 'bun',
    tilak: true,
    pose: 'stand',
    glow: PAL.turmeric
  });
  trishula(c, 715, 600, 0.85, PAL.gold, 0.05);
  c.restore();
}

// Scene 4: The Word Kala - Time & Death
function sceneKalaMeaning(c, W, Hh, t) {
  const u = sm(SC.kalaMeaning, SC.impermanence, t);
  c.save();
  cam(c, W, Hh, 0.04 * u);
  // Split sky: Left side golden day (Time), Right side dark night (Death)
  sky(c, W, Hh, WARM);
  const g = c.createLinearGradient(W * 0.4, 0, W, 0);
  g.addColorStop(0, H.rgba(PAL.night, 0));
  g.addColorStop(1, H.rgba(PAL.night, 0.75));
  c.fillStyle = g;
  c.fillRect(0, 0, W, Hh);

  streaks(c, W, Hh, t, { seed: 19, alpha: 0.2 });
  // Sun on left, eclipsed moon on right
  sun(c, 340, 240, 95, PAL.turmeric, 2.8);
  rays(c, 340, 240, 105, 500, 18, PAL.cream, t, 0.2);

  c.save();
  c.fillStyle = PAL.cream;
  c.beginPath();
  c.arc(940, 240, 60, 0, TAU);
  c.fill();
  c.fillStyle = PAL.night;
  c.beginPath();
  c.arc(960, 235, 54, 0, TAU);
  c.fill();
  c.restore();

  cloudBank(c, W, 240, t, { seed: 18, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 6 });
  timeWheel(c, 340, 480, 100, t * 0.8, PAL.gold);
  flames(c, 940, 520, 1.1, t, 7, 6);

  hills(c, W, Hh, 580, 50, PAL.brown, 20);
  hills(c, W, Hh, 650, 30, PAL.deep, 21);

  // Central majestic Bhairava maintaining balance
  figure(c, {
    x: 640,
    y: 680,
    s: 1.3,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    pose: 'stand',
    arms: [[-0.8, 0.5], [0.8, 0.5]],
    glow: PAL.kesari
  });
  c.restore();
}

// Scene 5: Impermanence - Kings Rise, Empires Fall
function sceneImpermanence(c, W, Hh, t) {
  const tt = t - SC.impermanence;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.impermanence, SC.beyondTime, t), -20, 10);
  sky(c, W, Hh, DUSK);
  streaks(c, W, Hh, t, { seed: 23, alpha: 0.16 });
  sun(c, 640, 300, 110, PAL.vermilion, 3);
  cloudBank(c, W, 200, t, { seed: 24, n: 6, fill: PAL.smoke, line: PAL.night, speed: 8 });

  // Dilapidated empire skyline sinking
  const collapse = cl(tt / 9.0);
  skyline(c, 360, 560 + collapse * 40, 0.65, PAL.brown, t);
  skyline(c, 920, 570 + collapse * 60, 0.6, mixc(PAL.brown, PAL.ink, 0.3), t);

  // Falling crown representing kings and kingdoms
  const crownFall = cl(sm(30.0, 35.0, t));
  crownOnly(c, 360, 320 + crownFall * 250, 1.2, crownFall * 1.2);

  // Ash-laden hills and river of time
  hills(c, W, Hh, 570, 50, PAL.maroon, 25);
  ocean(c, W, Hh, 610, t, [PAL.deep, PAL.brown, PAL.ink]);
  hills(c, W, Hh, 670, 30, PAL.ink, 26);
  c.restore();
}

// Scene 6: Beyond Limitations - The Timeless Master
function sceneBeyondTime(c, W, Hh, t) {
  const u = sm(SC.beyondTime, SC.fierceForm, t);
  c.save();
  cam(c, W, Hh, 0.06 * u);
  sky(c, W, Hh, WARM);
  stars(c, W, Hh, t, 0.4);
  streaks(c, W, Hh, t, { color: PAL.cream, alpha: 0.24, seed: 27, n: 110 });
  sun(c, 640, 290, 150, PAL.turmeric, 3.4);
  rays(c, 640, 290, 160, 800, 30, PAL.cream, t, 0.3);
  timeWheel(c, 640, 290, 240, t * 0.4, PAL.gold);

  hills(c, W, Hh, 560, 60, mixc(PAL.brown, PAL.saffron, 0.4), 28);
  hills(c, W, Hh, 630, 40, PAL.brown, 29);

  // Bhairava standing tall and unaffected by temporal wind
  figure(c, {
    x: 640,
    y: 680,
    s: 1.45,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    pose: 'stand',
    glow: PAL.turmeric,
    arms: [[-0.5, 0.3], [0.35, 0.8]]
  });
  trishula(c, 730, 605, 0.95, PAL.gold, -0.05);
  hound(c, 510, 675, 0.8, 1, PAL.ink);
  hills(c, W, Hh, 690, 20, PAL.deep, 30);
  c.restore();
}

// Scene 7: Fierce Form - Destroyer of Arrogance & Illusion
function sceneFierceForm(c, W, Hh, t) {
  const tt = t - SC.fierceForm;
  c.save();
  const shake = Math.sin(tt * 20) * 2.5 * sm(0, 3, tt);
  cam(c, W, Hh, 0.05 * sm(SC.fierceForm, SC.kashi, t), shake, 0);
  sky(c, W, Hh, [[0, PAL.night], [0.45, PAL.maroon], [0.85, PAL.vermilion], [1, PAL.kesari]]);
  streaks(c, W, Hh, t, { color: PAL.turmeric, alpha: 0.28, seed: 33 });
  cloudBank(c, W, 220, t, { seed: 34, n: 6, fill: PAL.smoke, line: PAL.night, speed: 10 });

  // Fierce transformation flames
  flames(c, 240, 660, 1.4, t, 11, 7);
  flames(c, 1040, 660, 1.4, t, 12, 7);
  flames(c, 640, 680, 1.1, t, 13, 5);

  hills(c, W, Hh, 570, 60, PAL.maroon, 35);
  hills(c, W, Hh, 630, 40, PAL.deep, 36);

  // Fierce stance with mace/weapon of righteousness
  figure(c, {
    x: 640,
    y: 675,
    s: 1.4,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.ink,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    pose: 'raise',
    mace: true,
    maceA: -1.6,
    glow: PAL.vermilion,
    eyeCol: PAL.kumkum
  });
  trishula(c, 540, 620, 0.9, PAL.brass, 0.12);
  hills(c, W, Hh, 690, 20, PAL.ink, 37);
  c.restore();
}

// Scene 8: Guardian of Kashi - The Eternal City
function sceneKashi(c, W, Hh, t) {
  const tt = t - SC.kashi;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.kashi, SC.dharmaLesson, t), 15, 0);
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 39 });
  sun(c, 840, 230, 110, PAL.turmeric, 3.2);
  cloudBank(c, W, 200, t, { seed: 40, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5 });

  // Iconic temples of Varanasi / Kashi along the bank
  temple(c, { x: 380, y: 510, s: 0.65, col: PAL.brown }, t);
  temple(c, { x: 880, y: 520, s: 0.52, col: PAL.burnt }, t);
  flag(c, 380, 480, 100, PAL.saffron, t, 1);
  flag(c, 880, 490, 85, PAL.kumkum, t, -1);

  // Ghat steps descending to Mother Ganga
  ghatSteps(c, W, 510, 8, PAL.brown);
  ocean(c, W, Hh, 630, t, [PAL.krishna, PAL.peacock, mixc(PAL.peacock, PAL.cream, 0.25)]);

  // Guardian Bhairava standing vigilant at Kashi
  figure(c, {
    x: 640,
    y: 620,
    s: 1.15,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    glow: PAL.gold
  });
  trishula(c, 705, 560, 0.8, PAL.brass, -0.05);
  hound(c, 560, 615, 0.65, 1, PAL.ink);
  c.restore();
}

// Scene 9: Follow Dharma & Overcome Ego
function sceneDharmaLesson(c, W, Hh, t) {
  const tt = t - SC.dharmaLesson;
  c.save();
  cam(c, W, Hh, 0.04 * sm(SC.dharmaLesson, SC.eternalReality, t));
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 44 });
  sun(c, 640, 270, 120, PAL.turmeric, 3.0);
  rays(c, 640, 270, 130, 720, 28, PAL.cream, t, 0.2);

  hills(c, W, Hh, 560, 60, mixc(PAL.brown, PAL.saffron, 0.35), 45);
  hills(c, W, Hh, 620, 40, PAL.brown, 46);

  // Devotee walking toward illumination & dharma
  const walkPh = tt * 1.3;
  figure(c, {
    x: 440,
    y: 675,
    s: 0.95,
    dir: 1,
    skin: PAL.sandal,
    cloth: PAL.cream,
    sash: PAL.turmeric,
    crown: 'bun',
    pose: 'walk',
    ph: walkPh
  });

  // Kala Bhairava bestowing wisdom
  figure(c, {
    x: 820,
    y: 675,
    s: 1.3,
    dir: -1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    pose: 'stand',
    glow: PAL.gold,
    arms: [[-0.8, 0.6], [0.3, 0.8]]
  });
  trishula(c, 740, 605, 0.9, PAL.gold, 0.08);

  // Sacred lotus markers of truth
  lotus(c, 640, 680, 1.0, PAL.lotus, PAL.cream);
  hills(c, W, Hh, 690, 20, PAL.deep, 47);
  c.restore();
}

// Scene 10: Eternal Reality Beyond Time
function sceneEternalReality(c, W, Hh, t) {
  const u = sm(SC.eternalReality, SC.ultimateLord, t);
  c.save();
  cam(c, W, Hh, 0.05 * u);
  sky(c, W, Hh, mixStops(WARM, NIGHT, 0.35));
  stars(c, W, Hh, t, 0.6);
  streaks(c, W, Hh, t, { color: PAL.turmeric, alpha: 0.22, seed: 49 });
  sun(c, 640, 260, 140, PAL.turmeric, 3.5);
  rays(c, 640, 260, 150, 850, 36, PAL.cream, t, 0.3);

  // Centered Eternal Shivalinga illuminated by cosmic light
  shivalinga(c, 640, 580, 1.35, t);

  hills(c, W, Hh, 590, 50, PAL.maroon, 50);
  hills(c, W, Hh, 650, 30, PAL.deep, 51);
  c.restore();
}

// Scene 11: Ultimate Lord of Time (Title Card Scene)
function sceneUltimateLord(c, W, Hh, t) {
  const tt = t - SC.ultimateLord;
  c.save();
  cam(c, W, Hh, 0.04 * sm(SC.ultimateLord, SC.companionDog, t));
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 54, alpha: 0.26 });
  sun(c, 640, 330, 140, PAL.turmeric, 3.2);
  rays(c, 640, 330, 150, 820, 32, PAL.cream, t, 0.22);
  timeWheel(c, 640, 330, 250, t * 0.3, PAL.gold);
  cloudBank(c, W, 220, t, { seed: 55, n: 6, fill: PAL.sandal, line: PAL.saffron, speed: 5 });

  temple(c, { x: 640, y: 640, s: 0.65, col: PAL.brown }, t);
  flag(c, 420, 640, 110, PAL.saffron, t, 1);
  flag(c, 860, 640, 110, PAL.kumkum, t, -1);

  // Lord Kala Bhairava in majestic full stature
  figure(c, {
    x: 640,
    y: 675,
    s: 1.35,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    tilak: true,
    glow: PAL.turmeric,
    arms: [[-0.6, 0.4], [0.35, 0.8]]
  });
  trishula(c, 725, 600, 0.95, PAL.brass, -0.06);
  hound(c, 520, 670, 0.8, 1, PAL.ink);
  hills(c, W, Hh, 695, 20, PAL.deep, 56);
  c.restore();
}

// Scene 12: The Mystery of the Dog Companion
function sceneCompanionDog(c, W, Hh, t) {
  const tt = t - SC.companionDog;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.companionDog, SC.mysteryOutro, t), 20, 0);
  sky(c, W, Hh, DUSK);
  streaks(c, W, Hh, t, { seed: 58, alpha: 0.2 });
  sun(c, 640, 290, 120, PAL.marigold, 3.0);
  rays(c, 640, 290, 130, 700, 24, PAL.turmeric, t, 0.16);

  cloudBank(c, W, 220, t, { seed: 59, n: 5, fill: mixc(PAL.sandal, PAL.burnt, 0.3), line: PAL.burnt, speed: 6 });
  hills(c, W, Hh, 570, 50, PAL.burnt, 60);
  hills(c, W, Hh, 630, 35, PAL.deep, 61);

  // Focused composition: Lord Bhairava and the noble companion Shvana
  figure(c, {
    x: 520,
    y: 670,
    s: 1.35,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.gold,
    crown: 'bun',
    tilak: true,
    glow: PAL.kesari,
    arms: [[-0.4, 0.4], [0.8, 0.6]]
  });
  trishula(c, 440, 595, 0.95, PAL.brass, 0.12);

  // Larger detailed view of the Shvana hound
  hound(c, 740, 665, 1.25, -1, PAL.ink);
  const p = pop(t, SC.companionDog + 1.2, 0.8);
  if (p > 0) lotus(c, 740, 675, 1.0 * p, PAL.lotus, PAL.cream);

  hills(c, W, Hh, 690, 20, PAL.deep, 62);
  c.restore();
}

// Scene 13: Closing Mystery & Teaser for Next Episode
function sceneMysteryOutro(c, W, Hh, t) {
  const u = sm(SC.mysteryOutro, DURATION, t);
  c.save();
  cam(c, W, Hh, 0.04 * u, 0, 10);
  sky(c, W, Hh, mixStops(DUSK, NIGHT, u));
  stars(c, W, Hh, t, 0.7 * u);
  streaks(c, W, Hh, t, { color: PAL.saffron, alpha: 0.18, seed: 65 });
  sun(c, 640, 420, 110, PAL.kesari, 3.4);
  timeWheel(c, 640, 420, 220, t * 0.15, PAL.gold);

  temple(c, { x: 640, y: 640, s: 0.7, col: PAL.deep }, t);
  flag(c, 440, 640, 120, PAL.saffron, t, 1);
  flag(c, 840, 640, 120, PAL.kumkum, t, -1);

  // Mystic silhouette of Bhairava & canine guarding the threshold of time
  figure(c, {
    x: 640,
    y: 670,
    s: 1.2,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.ink,
    sash: PAL.gold,
    crown: 'bun',
    tilak: true,
    glow: PAL.turmeric
  });
  trishula(c, 710, 600, 0.85, PAL.gold, -0.05);
  hound(c, 550, 665, 0.8, 1, PAL.ink);
  hills(c, W, Hh, 690, 20, PAL.ink, 66);
  c.restore();
}

const SCENES = [
  [0, sceneIntro],
  [SC.bhairavaLord, sceneBhairavaLord],
  [SC.divineForce, sceneDivineForce],
  [SC.kalaMeaning, sceneKalaMeaning],
  [SC.impermanence, sceneImpermanence],
  [SC.beyondTime, sceneBeyondTime],
  [SC.fierceForm, sceneFierceForm],
  [SC.kashi, sceneKashi],
  [SC.dharmaLesson, sceneDharmaLesson],
  [SC.eternalReality, sceneEternalReality],
  [SC.ultimateLord, sceneUltimateLord],
  [SC.companionDog, sceneCompanionDog],
  [SC.mysteryOutro, sceneMysteryOutro]
];
