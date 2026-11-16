/* The Legend of Brahma's Fifth Head and Shiva's Curse */

const TITLE = "THE FIFTH HEAD";
const HOOK = ["Why Brahma lost his fifth head", "and was cursed by Shiva"];
const REEL_SUBTITLE = "A 2 minute legend";

const SC = {
  brahma: 0,
  dispute: 8.5,
  pillar: 16.3,
  stretch: 23.0,
  challenge: 27.8,
  search: 34.6,
  defeat: 42.2,
  falsehood: 51.0,
  ketaki: 56.9,
  truth: 62.0,
  sever: 66.1,
  curse: 76.0,
  flowerCurse: 85.4,
  temples: 91.5,
  shunned: 96.5,
  moral: 102.8,
};

const FADE = 0.9;

const BEATS = [
  { n: 1, name: 'Five Heads of Brahma', t0: 0, t1: SC.dispute, vo: 'Lord Brahma, creator of the universe, once had five heads.', screen: 'Golden cosmic realm, Brahma with five radiating heads.' },
  { n: 2, name: 'The Dispute', t0: SC.dispute, t1: SC.pillar, vo: 'Brahma and Lord Vishnu began arguing about who was the most powerful.', screen: 'Vishnu and Brahma face each other in pride and power.' },
  { n: 3, name: 'The Infinite Pillar', t0: SC.pillar, t1: SC.stretch, vo: 'Lord Shiva appeared as an endless pillar of divine light.', screen: 'The Jyotirlinga pierces cosmic darkness in blinding fire.' },
  { n: 4, name: 'Beyond Heavens and Earth', t0: SC.stretch, t1: SC.challenge, vo: 'Stretching beyond the heavens and deep into the earth.', screen: 'Cosmic scale of the endless lingam spanning all realms.' },
  { n: 5, name: 'The Challenge', t0: SC.challenge, t1: SC.search, vo: 'Shiva challenged both gods to find the beginning and end.', screen: 'Shiva in ethereal halo bids them seek the borders of light.' },
  { n: 6, name: 'The Cosmic Search', t0: SC.search, t1: SC.defeat, vo: 'Vishnu dove downward while Brahma flew upward.', screen: 'Vishnu as boar Varaha descends; Brahma soars atop hamsa.' },
  { n: 7, name: 'Vishnu Accepts Defeat', t0: SC.defeat, t1: SC.falsehood, vo: 'Vishnu returns humbly, admitting the pillar is endless.', screen: 'Vishnu bows with folded hands before the divine pillar.' },
  { n: 8, name: 'Brahma False Claim', t0: SC.falsehood, t1: SC.ketaki, vo: 'Brahma falsely claimed that he had reached the top.', screen: 'Brahma boasting in arrogance before the radiant light.' },
  { n: 9, name: 'The Ketaki Flower', t0: SC.ketaki, t1: SC.truth, vo: 'He even presented a Ketaki flower as false evidence.', screen: 'A pale golden flower falls into Brahma hand as false witness.' },
  { n: 10, name: 'The Eye of Shiva', t0: SC.truth, t1: SC.sever, vo: 'Lord Shiva immediately recognized Brahma lie.', screen: 'Shiva third eye opens in cosmic fire seeing through the deceit.' },
  { n: 11, name: 'Bhairava Severing', t0: SC.sever, t1: SC.curse, vo: 'Bhairava manifested and severed Brahma fifth head.', screen: 'Fierce Bhairava strikes; the proud upper head is cut away.' },
  { n: 12, name: 'The Curse of No Temples', t0: SC.curse, t1: SC.flowerCurse, vo: 'Brahma is cursed to not be worshipped in temples on Earth.', screen: 'Brahma with four heads bowed in repentance beneath a fading shrine.' },
  { n: 13, name: 'The Forbidden Flower', t0: SC.flowerCurse, t1: SC.temples, vo: 'The Ketaki flower is forever banned from Shiva worship.', screen: 'The flower cast away from the Shiva lingam in sorrow.' },
  { n: 14, name: 'Few Temples', t0: SC.temples, t1: SC.shunned, vo: 'Why Brahma has very few temples dedicated to him.', screen: 'A lone temple in Pushkar desert amidst swirling golden sands.' },
  { n: 15, name: 'Tradition Upheld', t0: SC.shunned, t1: SC.moral, vo: 'Ketaki avoided in worship of Shiva.', screen: 'Belpatra and water on the lingam, Ketaki petal discarded.' },
  { n: 16, name: 'Truth Triumphs', t0: SC.moral, t1: DURATION, vo: 'Moral: Even the creator must respect truth.', screen: 'Triumphant golden title and moral proclamation.' },
];

/* Helper: Custom multi-headed Brahma */
function brahmaFigure(c, o) {
  const x = o.x, y = o.y, s = o.s || 1, heads = o.heads || 5;
  c.save();
  c.translate(x, y);
  c.scale(s, s);

  // Lotus base
  lotus(c, 0, 10, 1.2, PAL.lotus, PAL.cream);

  // Body: seated/standing figure
  figure(c, {
    x: 0,
    y: 0,
    s: 1,
    dir: 1,
    skin: PAL.sandal,
    cloth: PAL.saffron,
    sash: PAL.turmeric,
    crown: 'tall',
    hair: PAL.ash,
    beard: true,
    pose: o.pose || 'namaste',
    tilak: true,
    glow: o.glow || PAL.amber,
  });

  // White sage beard
  c.fillStyle = PAL.ash;
  c.beginPath();
  c.moveTo(-10, -170);
  c.quadraticCurveTo(0, -135, 12, -165);
  c.quadraticCurveTo(0, -130, -10, -170);
  c.fill();

  // Flanking heads
  const drawSideHead = (dx, dy, dir, crownH) => {
    c.save();
    c.translate(dx, dy);
    c.scale(0.82 * dir, 0.82);
    // Face
    c.fillStyle = mixc(PAL.sandal, PAL.ink, 0.1);
    c.beginPath();
    c.arc(0, 0, 22, 0, TAU);
    c.fill();
    c.beginPath();
    c.moveTo(18, -6);
    c.lineTo(32, 2);
    c.lineTo(18, 6);
    c.closePath();
    c.fill();
    // Eye
    c.fillStyle = PAL.cream;
    c.beginPath();
    c.ellipse(8, -4, 8, 3.5, 0, 0, TAU);
    c.fill();
    c.fillStyle = PAL.ink;
    c.beginPath();
    c.arc(10, -4, 2.8, 0, TAU);
    c.fill();
    // Beard
    c.fillStyle = PAL.ash;
    c.beginPath();
    c.moveTo(-6, 8);
    c.quadraticCurveTo(12, 34, 18, 12);
    c.quadraticCurveTo(6, 26, -6, 8);
    c.fill();
    // Crown
    c.fillStyle = PAL.gold;
    c.beginPath();
    c.moveTo(-20, -16);
    c.lineTo(20, -16);
    c.lineTo(14, -42);
    c.lineTo(0, -crownH);
    c.lineTo(-14, -42);
    c.closePath();
    c.fill();
    c.restore();
  };

  // Left & right heads
  drawSideHead(-42, -180, -1, 65);
  drawSideHead(42, -180, 1, 65);
  drawSideHead(-78, -175, -1, 55);

  // 5th head on top (arrogant head)
  if (heads >= 5) {
    c.save();
    const drop = o.severY || 0, rot = o.severR || 0;
    c.translate(0, -260 + drop);
    c.rotate(rot);
    if (o.severAlpha != null) c.globalAlpha = o.severAlpha;
    // Glow around 5th head
    if (!o.severY) {
      sun(c, 0, 0, 30, PAL.gold, 2.5);
    }
    drawSideHead(0, 0, 1, 75);
    // Neck connection or glow
    c.fillStyle = PAL.kumkum;
    c.fillRect(-8, 18, 16, 5);
    c.restore();
  }

  c.restore();
}

/* Helper: Jyotirlinga (Pillar of Cosmic Fire) */
function jyotirlinga(c, x, y0, y1, w, t, pulse) {
  c.save();
  const pl = pulse || 1;
  const rad = w * pl;
  // Deep outer glow
  const gOut = c.createLinearGradient(x - rad * 4, 0, x + rad * 4, 0);
  gOut.addColorStop(0, H.rgba(PAL.saffron, 0));
  gOut.addColorStop(0.3, H.rgba(PAL.vermilion, 0.45));
  gOut.addColorStop(0.5, H.rgba(PAL.turmeric, 0.7));
  gOut.addColorStop(0.7, H.rgba(PAL.vermilion, 0.45));
  gOut.addColorStop(1, H.rgba(PAL.saffron, 0));
  c.fillStyle = gOut;
  c.fillRect(x - rad * 4, y0, rad * 8, y1 - y0);

  // Inner core
  const gIn = c.createLinearGradient(x - rad, 0, x + rad, 0);
  gIn.addColorStop(0, PAL.turmeric);
  gIn.addColorStop(0.3, PAL.cream);
  gIn.addColorStop(0.5, '#ffffff');
  gIn.addColorStop(0.7, PAL.cream);
  gIn.addColorStop(1, PAL.turmeric);
  c.fillStyle = gIn;
  c.fillRect(x - rad, y0, rad * 2, y1 - y0);

  // Flaming tongues up and down
  c.save();
  for (let i = 0; i < 24; i++) {
    const yy = y0 + ((i * 35 + t * 90) % (y1 - y0));
    const flw = Math.sin(i * 1.7 + t * 6) * rad * 1.4;
    c.fillStyle = i % 2 === 0 ? PAL.kesari : PAL.cream;
    c.globalAlpha = 0.5;
    c.beginPath();
    c.arc(x + flw * 0.4, yy, rad * 0.6, 0, TAU);
    c.fill();
  }
  c.restore();

  // Shiva Trishul watermark inside pillar
  c.save();
  c.globalAlpha = 0.4 + 0.3 * Math.sin(t * 3);
  trishul(c, x, (y0 + y1) * 0.5, 0.9, PAL.deep);
  c.restore();

  c.restore();
}

/* Helper: Trishul (Trident) */
function trishul(c, x, y, s, col) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  c.strokeStyle = col || PAL.gold;
  c.fillStyle = col || PAL.gold;
  c.lineWidth = 6;
  // Shaft
  c.beginPath();
  c.moveTo(0, 80);
  c.lineTo(0, -80);
  c.stroke();
  // Center spear
  c.beginPath();
  c.moveTo(-7, -80);
  c.lineTo(7, -80);
  c.lineTo(0, -135);
  c.closePath();
  c.fill();
  // Outer prongs
  [-1, 1].forEach((dir) => {
    c.beginPath();
    c.moveTo(0, -60);
    c.quadraticCurveTo(dir * 38, -60, dir * 35, -115);
    c.quadraticCurveTo(dir * 42, -80, dir * 18, -48);
    c.closePath();
    c.fill();
  });
  // Damaru
  c.fillStyle = PAL.brass;
  c.beginPath();
  c.moveTo(-16, -20);
  c.lineTo(16, -20);
  c.lineTo(-16, 12);
  c.lineTo(16, 12);
  c.closePath();
  c.fill();
  c.restore();
}

/* Helper: Ketaki Flower */
function drawKetaki(c, x, y, s, rot) {
  c.save();
  c.translate(x, y);
  c.rotate(rot || 0);
  c.scale(s, s);
  // Radiant golden-cream fragrant flower petals
  for (let i = 0; i < 7; i++) {
    const a = (i - 3) * 0.22;
    c.save();
    c.rotate(a);
    c.fillStyle = i % 2 === 0 ? PAL.sandal : PAL.cream;
    c.beginPath();
    c.moveTo(0, 0);
    c.quadraticCurveTo(8, -35, 0, -75);
    c.quadraticCurveTo(-8, -35, 0, 0);
    c.fill();
    c.strokeStyle = PAL.gold;
    c.lineWidth = 1.2;
    c.stroke();
    c.restore();
  }
  // Golden center
  c.fillStyle = PAL.turmeric;
  c.beginPath();
  c.arc(0, -10, 8, 0, TAU);
  c.fill();
  c.restore();
}

/* Helper: Varaha / Boar form diving down */
function boarAvatar(c, x, y, s) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  // Dark blue-grey divine boar form
  c.fillStyle = PAL.krishna;
  // Body
  c.beginPath();
  c.ellipse(0, 0, 65, 38, 0.4, 0, TAU);
  c.fill();
  // Snout down
  c.beginPath();
  c.moveTo(35, 10);
  c.lineTo(75, 45);
  c.lineTo(55, 55);
  c.lineTo(25, 25);
  c.closePath();
  c.fill();
  // Tusks
  c.strokeStyle = PAL.cream;
  c.lineWidth = 6;
  c.beginPath();
  c.moveTo(60, 48);
  c.quadraticCurveTo(75, 30, 80, 20);
  c.stroke();
  // Legs
  c.fillStyle = PAL.rama;
  c.fillRect(-35, 15, 14, 40);
  c.fillRect(5, 18, 14, 40);
  // Divine tilak & gold crown
  crownOnly(c, -10, -32, 0.55, 0.3);
  c.restore();
}

/* Helper: Hamsa (Divine Swan) soaring up */
function hamsa(c, x, y, s) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  c.fillStyle = PAL.cream;
  // Body
  c.beginPath();
  c.ellipse(0, 0, 50, 26, -0.4, 0, TAU);
  c.fill();
  // Wings
  c.beginPath();
  c.moveTo(-20, -10);
  c.quadraticCurveTo(0, -65, 30, -75);
  c.quadraticCurveTo(15, -30, 5, -5);
  c.closePath();
  c.fill();
  // Neck & Head pointing up
  c.beginPath();
  c.moveTo(30, -10);
  c.quadraticCurveTo(55, -35, 65, -60);
  c.quadraticCurveTo(60, -70, 50, -65);
  c.quadraticCurveTo(40, -40, 20, 5);
  c.closePath();
  c.fill();
  // Beak
  c.fillStyle = PAL.saffron;
  c.beginPath();
  c.moveTo(62, -68);
  c.lineTo(80, -76);
  c.lineTo(60, -60);
  c.closePath();
  c.fill();
  c.restore();
}

/* Helper: Shiva Third Eye */
function thirdEye(c, x, y, s, open) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  const op = cl(open);
  c.fillStyle = PAL.cream;
  c.beginPath();
  c.ellipse(0, 0, 40, 20 * op, 0, 0, TAU);
  c.fill();
  // Golden fiery pupil
  c.fillStyle = PAL.vermilion;
  c.beginPath();
  c.arc(0, 0, 14 * op, 0, TAU);
  c.fill();
  c.fillStyle = PAL.turmeric;
  c.beginPath();
  c.arc(0, 0, 7 * op, 0, TAU);
  c.fill();
  // Radiant burst
  if (op > 0.4) {
    rays(c, 0, 0, 25, 140 * op, 18, PAL.kesari, 0, 0.6 * op);
  }
  c.restore();
}

/* Helper: Lingam for temple/worship */
function shivalingam(c, x, y, s) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  // Yoni base
  c.fillStyle = PAL.ink;
  c.beginPath();
  c.ellipse(0, 20, 75, 26, 0, 0, TAU);
  c.fill();
  c.fillRect(35, 12, 50, 16);
  // Lingam stone
  c.fillStyle = PAL.deep;
  c.beginPath();
  c.moveTo(-35, 20);
  c.lineTo(-35, -45);
  c.arc(0, -45, 35, Math.PI, 0, false);
  c.lineTo(35, 20);
  c.closePath();
  c.fill();
  // Vibhuti & Kumkum
  c.fillStyle = PAL.ash;
  c.fillRect(-20, -50, 40, 4);
  c.fillRect(-20, -44, 40, 4);
  c.fillRect(-20, -38, 40, 4);
  c.fillStyle = PAL.kumkum;
  c.beginPath();
  c.arc(0, -44, 4, 0, TAU);
  c.fill();
  c.restore();
}

/* Helper: Bhairava figure */
function bhairavaFigure(c, x, y, s, t) {
  c.save();
  c.translate(x, y);
  c.scale(s, s);
  // Dark wrathful skin, glowing red aura
  sun(c, 0, -110, 110, PAL.vermilion, 2.5);
  figure(c, {
    x: 0,
    y: 0,
    s: 1.1,
    dir: 1,
    skin: PAL.indigo,
    cloth: PAL.maroon,
    sash: PAL.kumkum,
    crown: 'king',
    hair: PAL.vermilion,
    pose: 'raise',
    glow: PAL.vermilion,
  });
  // Sword in hand
  c.save();
  c.translate(45, -160);
  c.rotate(0.3 + Math.sin(t * 8) * 0.1);
  c.fillStyle = PAL.ash;
  c.fillRect(-6, -90, 12, 100);
  c.beginPath();
  c.moveTo(-8, -90);
  c.lineTo(8, -90);
  c.lineTo(0, -125);
  c.closePath();
  c.fill();
  c.fillStyle = PAL.gold;
  c.fillRect(-18, 10, 36, 10);
  c.restore();
  c.restore();
}

/* ========================================================
   SCENE FUNCTIONS
======================================================== */

// Scene 1: Brahma with five heads in the cosmic lotus realm
function sceneBrahma(c, W, Hh, t) {
  const u = sm(0, SC.dispute, t);
  c.save();
  cam(c, W, Hh, 0.05 * u, 0, 15);
  sky(c, W, Hh, WARM);
  stars(c, W, Hh, t, 0.4);
  streaks(c, W, Hh, t, { color: PAL.cream, alpha: 0.22, seed: 10 });
  sun(c, 640, 240, 140, PAL.turmeric, 3.2);
  rays(c, 640, 240, 150, 780, 26, PAL.cream, t, 0.25);
  cloudBank(c, W, 220, t, { seed: 11, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5 });
  hills(c, W, Hh, 540, 70, PAL.maroon, 1);
  hills(c, W, Hh, 600, 50, PAL.deep, 2);

  // Five-headed Brahma seated majestically
  brahmaFigure(c, {
    x: 640,
    y: 620,
    s: 1.35,
    heads: 5,
    pose: 'stand',
    glow: PAL.turmeric,
  });

  hills(c, W, Hh, 680, 25, PAL.ink, 3);
  c.restore();
}

// Scene 2: Dispute between Brahma and Vishnu
function sceneDispute(c, W, Hh, t) {
  const tt = t - SC.dispute;
  c.save();
  cam(c, W, Hh, 0.04 * sm(SC.dispute, SC.pillar, t));
  sky(c, W, Hh, mixStops(WARM, DUSK, sm(SC.dispute, SC.dispute + 6, t)));
  streaks(c, W, Hh, t, { seed: 12, alpha: 0.18 });
  sun(c, 640, 280, 110, PAL.kesari, 2.8);
  cloudBank(c, W, 200, t, { seed: 13, n: 6, fill: PAL.sandal, line: PAL.burnt, speed: 6 });
  hills(c, W, Hh, 530, 60, PAL.brown, 4);
  hills(c, W, Hh, 590, 40, PAL.deep, 5);

  // Vishnu on left (Rama blue, regal crown, Sudarshana aura)
  const vishnuX = 380 + Math.sin(tt * 1.5) * 6;
  figure(c, {
    x: vishnuX,
    y: 640,
    s: 1.15,
    dir: 1,
    skin: PAL.rama,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'king',
    tilak: true,
    pose: 'stand',
    arms: [[-1.2, 0.5], [0.3, 0.7]],
    glow: PAL.rama,
  });
  // Sudarshana Chakra hovering above Vishnu hand
  sun(c, vishnuX - 45, 500, 18, PAL.gold, 2.5);
  rays(c, vishnuX - 45, 500, 12, 35, 12, PAL.turmeric, t * 8, 0.8);

  // Brahma on right (five heads, golden aura, asserting superiority)
  const brahmaX = 900 - Math.sin(tt * 1.5) * 6;
  brahmaFigure(c, {
    x: brahmaX,
    y: 640,
    s: 1.15,
    heads: 5,
    pose: 'stand',
    glow: PAL.amber,
  });

  hills(c, W, Hh, 680, 20, PAL.ink, 6);
  c.restore();
}

// Scene 3: The Endless Pillar of Divine Light appears
function scenePillar(c, W, Hh, t) {
  const tt = t - SC.pillar;
  const pulse = 1 + 0.15 * Math.sin(tt * 4);
  c.save();
  cam(c, W, Hh, 0.06 * sm(SC.pillar, SC.stretch, t), 0, 0);
  sky(c, W, Hh, NIGHT);
  stars(c, W, Hh, t, 0.6);
  streaks(c, W, Hh, t, { color: PAL.turmeric, alpha: 0.3, seed: 15, n: 110 });

  // Blinding pillar piercing through the center
  jyotirlinga(c, 640, -50, Hh + 50, 55, t, pulse);

  // Both gods stunned on either side
  figure(c, {
    x: 260,
    y: 650,
    s: 0.95,
    dir: 1,
    skin: PAL.rama,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'king',
    pose: 'namaste',
    tilak: true,
  });

  brahmaFigure(c, {
    x: 1020,
    y: 650,
    s: 0.95,
    heads: 5,
    pose: 'namaste',
  });

  hills(c, W, Hh, 670, 30, PAL.ink, 7);
  c.restore();
}

// Scene 4: Pillar stretching beyond heavens and deep into earth
function sceneStretch(c, W, Hh, t) {
  const tt = t - SC.stretch;
  c.save();
  cam(c, W, Hh, 0.08 * sm(SC.stretch, SC.challenge, t), 0, -20);
  sky(c, W, Hh, [[0, PAL.night], [0.35, PAL.indigo], [0.7, PAL.maroon], [1, PAL.deep]]);
  stars(c, W, Hh, t, 0.8);
  streaks(c, W, Hh, t, { color: PAL.cream, alpha: 0.25, seed: 16 });

  // Lingam runs through upper clouds and lower underworld
  cloudBank(c, W, 180, t, { seed: 17, n: 6, fill: PAL.indigo, line: PAL.lotus, speed: 8 });
  jyotirlinga(c, 640, -100, Hh + 100, 75, t, 1.1 + 0.1 * Math.sin(tt * 5));

  // Earth / underworld crags at bottom
  hills(c, W, Hh, 580, 80, PAL.maroon, 8);
  hills(c, W, Hh, 640, 50, PAL.deep, 9);
  flames(c, 300, 680, 1.2, t, 20, 6);
  flames(c, 980, 680, 1.2, t, 21, 6);

  c.restore();
}

// Scene 5: Shiva challenges them
function sceneChallenge(c, W, Hh, t) {
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.challenge, SC.search, t));
  sky(c, W, Hh, [[0, PAL.night], [0.4, PAL.maroon], [0.75, PAL.burnt], [1, PAL.saffron]]);
  streaks(c, W, Hh, t, { seed: 19, alpha: 0.2 });

  // Central pillar glowing
  jyotirlinga(c, 640, -20, Hh + 20, 50, t, 1.05);

  // Shiva silhouette manifest inside the halo
  sun(c, 640, 280, 95, PAL.cream, 3);
  rays(c, 640, 280, 100, 600, 24, PAL.turmeric, t, 0.35);
  figure(c, {
    x: 640,
    y: 360,
    s: 0.85,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    pose: 'raise',
    tilak: true,
    glow: PAL.cream,
  });
  trishul(c, 685, 290, 0.7, PAL.gold);

  // Vishnu listening on left, Brahma listening on right
  figure(c, {
    x: 240,
    y: 650,
    s: 0.95,
    dir: 1,
    skin: PAL.rama,
    cloth: PAL.turmeric,
    crown: 'king',
    pose: 'namaste',
    tilak: true,
  });

  brahmaFigure(c, {
    x: 1040,
    y: 650,
    s: 0.95,
    heads: 5,
    pose: 'stand',
  });

  hills(c, W, Hh, 680, 25, PAL.ink, 10);
  c.restore();
}

// Scene 6: Vishnu dives downward, Brahma soars upward
function sceneSearch(c, W, Hh, t) {
  const u = sm(SC.search, SC.defeat, t);
  c.save();
  cam(c, W, Hh, 0.04 * u);
  sky(c, W, Hh, [[0, PAL.night], [0.5, PAL.indigo], [1, PAL.maroon]]);
  stars(c, W, Hh, t, 0.7);

  // Endless central pillar
  jyotirlinga(c, 640, -50, Hh + 50, 45, t, 1.0);

  // Brahma soaring upward on swan (right side)
  const bY = lerp(580, 100, EO(u));
  c.save();
  hamsa(c, 900, bY + 30, 1.1);
  brahmaFigure(c, {
    x: 900,
    y: bY,
    s: 0.65,
    heads: 5,
    pose: 'raise',
  });
  c.restore();

  // Vishnu descending downward as Varaha (left side)
  const vY = lerp(160, 600, EO(u));
  c.save();
  boarAvatar(c, 380, vY, 1.2);
  c.restore();

  hills(c, W, Hh, 690, 20, PAL.deep, 11);
  c.restore();
}

// Scene 7: Vishnu accepts defeat with humility
function sceneDefeat(c, W, Hh, t) {
  const tt = t - SC.defeat;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.defeat, SC.falsehood, t));
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 22, alpha: 0.2 });
  jyotirlinga(c, 780, -20, Hh + 20, 50, t, 1.05);

  // Vishnu returning in human avatar, bowing with humility
  figure(c, {
    x: 420,
    y: 640,
    s: 1.25,
    dir: 1,
    skin: PAL.rama,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'king',
    pose: 'kneel',
    tilak: true,
    glow: PAL.rama,
  });

  // Lotus flowers blooming at Vishnu feet for his honesty
  [320, 420, 520].forEach((lx) => {
    lotus(c, lx, 650, 0.8, PAL.lotus, PAL.cream);
  });

  hills(c, W, Hh, 670, 30, PAL.brown, 12);
  hills(c, W, Hh, 700, 18, PAL.deep, 13);
  c.restore();
}

// Scene 8: Brahma desperate to win, falsely claiming victory
function sceneFalsehood(c, W, Hh, t) {
  const tt = t - SC.falsehood;
  c.save();
  cam(c, W, Hh, 0.06 * sm(SC.falsehood, SC.ketaki, t));
  sky(c, W, Hh, DUSK);
  streaks(c, W, Hh, t, { color: PAL.saffron, alpha: 0.22, seed: 23 });
  jyotirlinga(c, 360, -20, Hh + 20, 48, t, 1.0);

  // Brahma boasting, arms raised in false pride
  brahmaFigure(c, {
    x: 820,
    y: 630,
    s: 1.3,
    heads: 5,
    pose: 'raise',
    glow: PAL.amber,
  });

  // Dark omen clouds gathering
  cloudBank(c, W, 180, t, { seed: 24, n: 6, fill: PAL.maroon, line: PAL.ink, speed: 8 });

  hills(c, W, Hh, 680, 25, PAL.deep, 14);
  c.restore();
}

// Scene 9: Brahma presents the Ketaki flower as false evidence
function sceneKetaki(c, W, Hh, t) {
  const tt = t - SC.ketaki;
  c.save();
  cam(c, W, Hh, 0.06 * sm(SC.ketaki, SC.truth, t), 0, 25);
  sky(c, W, Hh, [[0, PAL.night], [0.5, PAL.maroon], [1, PAL.burnt]]);
  streaks(c, W, Hh, t, { color: PAL.gold, alpha: 0.2, seed: 25 });

  // Brahma standing proudly on the right
  brahmaFigure(c, {
    x: 480,
    y: 640,
    s: 1.15,
    heads: 5,
    pose: 'stand',
  });

  // Large spotlight on the Ketaki flower floating into view
  const popFl = pop(t, SC.ketaki + 0.3, 0.8);
  sun(c, 840, 380, 75 * popFl, PAL.gold, 3);
  drawKetaki(c, 840, 380, 1.6 * popFl, Math.sin(tt * 2) * 0.15);

  // False testimony glow
  c.save();
  c.globalAlpha = 0.3 * popFl;
  rays(c, 840, 380, 80, 420, 16, PAL.cream, t, 0.4);
  c.restore();

  hills(c, W, Hh, 680, 25, PAL.ink, 15);
  c.restore();
}

// Scene 10: Lord Shiva recognizes the lie - Third eye opens
function sceneTruth(c, W, Hh, t) {
  const tt = t - SC.truth;
  const eyeOpen = sm(SC.truth, SC.truth + 1.8, t);
  c.save();
  cam(c, W, Hh, 0.07 * eyeOpen);
  sky(c, W, Hh, [[0, PAL.night], [0.45, PAL.maroon], [0.8, PAL.vermilion], [1, PAL.burnt]]);
  streaks(c, W, Hh, t, { color: PAL.vermilion, alpha: 0.3, seed: 26 });

  // Giant cosmic Third Eye of Shiva piercing through the sky
  sun(c, 640, 260, 160, PAL.vermilion, 3);
  thirdEye(c, 640, 260, 2.8, eyeOpen);

  // Flaming background
  flames(c, 180, 700, 1.4, t, 31, 7);
  flames(c, 1100, 700, 1.4, t, 32, 7);

  // Brahma shrinking back in panic
  brahmaFigure(c, {
    x: 640,
    y: 670,
    s: 0.95,
    heads: 5,
    pose: 'kneel',
  });

  hills(c, W, Hh, 690, 20, PAL.ink, 16);
  c.restore();
}

// Scene 11: Bhairava severs Brahma's fifth head
function sceneSever(c, W, Hh, t) {
  const tt = t - SC.sever;
  const strikeTime = SC.sever + 2.5;
  const severed = t >= strikeTime;
  const cutU = cl((t - strikeTime) / 2.5);
  const flash = Math.exp(-Math.max(0, t - strikeTime) * 3) * (t >= strikeTime ? 1 : 0);

  c.save();
  const shake = t >= strikeTime && t < strikeTime + 1.2 ? Math.sin((t - strikeTime) * 35) * 8 : 0;
  cam(c, W, Hh, 0.08 * sm(SC.sever, SC.curse, t), shake, shake * 0.5);
  sky(c, W, Hh, [[0, PAL.night], [0.4, PAL.indigo], [0.75, PAL.maroon], [1, PAL.vermilion]]);
  streaks(c, W, Hh, t, { color: PAL.kumkum, alpha: 0.32, seed: 27, n: 100 });

  // Bhairava charging from the left
  bhairavaFigure(c, 420, 640, 1.25, t);

  // Brahma on the right
  const headDrop = severed ? cutU * 280 : 0;
  const headRot = severed ? cutU * 1.8 : 0;
  const headAlpha = severed ? 1 - cutU * 0.8 : 1;

  brahmaFigure(c, {
    x: 880,
    y: 640,
    s: 1.2,
    heads: 5,
    severY: headDrop,
    severR: headRot,
    severAlpha: headAlpha,
    pose: 'kneel',
  });

  // Thunderous lightning bolt striking at sever moment
  if (t >= strikeTime && t < strikeTime + 0.6) {
    bolt(c, 880, 0, 480, 40, PAL.cream);
  }

  // Blinding impact flash
  if (flash > 0.02) {
    c.fillStyle = H.rgba(PAL.cream, flash * 0.7);
    c.fillRect(0, 0, W, Hh);
  }

  hills(c, W, Hh, 690, 20, PAL.ink, 17);
  c.restore();
}

// Scene 12: Shiva curses Brahma - No wide worship in temples
function sceneCurse(c, W, Hh, t) {
  const tt = t - SC.curse;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.curse, SC.flowerCurse, t));
  sky(c, W, Hh, DUSK);
  streaks(c, W, Hh, t, { seed: 28, alpha: 0.18 });

  // Shiva standing tall in judgment on left
  figure(c, {
    x: 380,
    y: 630,
    s: 1.25,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    pose: 'raise',
    tilak: true,
    glow: PAL.turmeric,
  });
  trishul(c, 435, 540, 0.85, PAL.gold);

  // Brahma now with only 4 heads, head bowed in deep humility
  brahmaFigure(c, {
    x: 880,
    y: 630,
    s: 1.15,
    heads: 4,
    pose: 'kneel',
  });

  // Faded, dark abandoned shrine in distance
  temple(c, { x: 1100, y: 560, s: 0.45, col: mixc(PAL.brown, PAL.ink, 0.5) }, t);

  hills(c, W, Hh, 670, 30, PAL.brown, 18);
  hills(c, W, Hh, 700, 18, PAL.deep, 19);
  c.restore();
}

// Scene 13: The Ketaki flower is forbidden from Shiva worship
function sceneFlowerCurse(c, W, Hh, t) {
  const tt = t - SC.flowerCurse;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.flowerCurse, SC.temples, t));
  sky(c, W, Hh, [[0, PAL.maroon], [0.5, PAL.burnt], [1, PAL.deep]]);
  streaks(c, W, Hh, t, { seed: 29, alpha: 0.16 });

  // Shiva Lingam in center
  shivalingam(c, 640, 520, 1.4);

  // Ketaki flower drifting away and drooping
  const driftX = lerp(640, 920, sm(SC.flowerCurse, SC.flowerCurse + 4, t));
  const driftY = lerp(420, 620, sm(SC.flowerCurse, SC.flowerCurse + 4, t));
  drawKetaki(c, driftX, driftY, 1.1, Math.PI * 0.4 + Math.sin(tt * 2) * 0.2);

  // Red prohibition circle / solemn aura
  c.save();
  c.strokeStyle = PAL.kumkum;
  c.lineWidth = 6;
  c.beginPath();
  c.arc(driftX, driftY - 20, 48, 0, TAU);
  c.stroke();
  c.beginPath();
  c.moveTo(driftX - 34, driftY + 14);
  c.lineTo(driftX + 34, driftY - 54);
  c.stroke();
  c.restore();

  hills(c, W, Hh, 680, 25, PAL.ink, 20);
  c.restore();
}

// Scene 14: Brahma has very few temples (Pushkar desert shrine)
function sceneTemples(c, W, Hh, t) {
  const tt = t - SC.temples;
  c.save();
  cam(c, W, Hh, 0.04 * sm(SC.temples, SC.shunned, t));
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 30, alpha: 0.2 });
  sun(c, 640, 280, 120, PAL.turmeric, 3);
  cloudBank(c, W, 220, t, { seed: 31, n: 5, fill: PAL.sandal, line: PAL.saffron, speed: 5 });

  // Sole lonely Brahma temple (Pushkar style)
  temple(c, { x: 640, y: 600, s: 0.72, col: PAL.brown }, t);
  flag(c, 640 - 200, 600, 110, PAL.saffron, t, 1);
  flag(c, 640 + 200, 600, 110, PAL.kumkum, t, -1);

  // Brahma inside shrine in prayer (4 heads)
  brahmaFigure(c, {
    x: 640,
    y: 600,
    s: 0.62,
    heads: 4,
    pose: 'namaste',
  });

  // Sand dunes / desert hills
  hills(c, W, Hh, 620, 40, PAL.turmeric, 21);
  hills(c, W, Hh, 670, 25, PAL.burnt, 22);
  c.restore();
}

// Scene 15: Ketaki traditionally avoided in Shiva worship
function sceneShunned(c, W, Hh, t) {
  const tt = t - SC.shunned;
  c.save();
  cam(c, W, Hh, 0.05 * sm(SC.shunned, SC.moral, t));
  sky(c, W, Hh, mixStops(WARM, DUSK, 0.4));
  streaks(c, W, Hh, t, { seed: 32, alpha: 0.18 });

  // Shiva Lingam with sacred Bilva leaves and water offerings
  shivalingam(c, 640, 520, 1.3);

  // Green Bilva leaves on lingam
  for (let k = -1; k <= 1; k++) {
    c.fillStyle = PAL.tulsi;
    c.beginPath();
    c.ellipse(640 + k * 18, 470, 10, 6, k * 0.4, 0, TAU);
    c.fill();
  }

  // Dropped Ketaki flower on the ground outside the sanctum
  drawKetaki(c, 920, 620, 0.85, 0.6);

  // Devotee offering prayers
  figure(c, {
    x: 360,
    y: 640,
    s: 0.95,
    dir: 1,
    skin: PAL.burnt,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'bun',
    pose: 'namaste',
  });

  hills(c, W, Hh, 680, 25, PAL.deep, 23);
  c.restore();
}

// Scene 16: Moral - Truth Triumphs Over Pride
function sceneMoral(c, W, Hh, t) {
  const u = sm(SC.moral, DURATION, t);
  c.save();
  cam(c, W, Hh, 0.05 * u, 0, 10);
  sky(c, W, Hh, WARM);
  streaks(c, W, Hh, t, { seed: 33, n: 120, alpha: 0.28 });
  sun(c, 640, 360, 140, PAL.turmeric, 3.2);
  rays(c, 640, 360, 150, 850, 32, PAL.cream, t, 0.25);
  cloudBank(c, W, 260, t, { seed: 34, n: 6, fill: PAL.sandal, line: PAL.saffron, speed: 5 });

  // Divine Trinity harmony restored under truth
  // Vishnu on left
  figure(c, {
    x: 320,
    y: 620,
    s: 0.95,
    dir: 1,
    skin: PAL.rama,
    cloth: PAL.turmeric,
    sash: PAL.kumkum,
    crown: 'king',
    pose: 'namaste',
    tilak: true,
  });

  // Shiva in center
  figure(c, {
    x: 640,
    y: 620,
    s: 1.1,
    dir: 1,
    skin: PAL.ash,
    cloth: PAL.burnt,
    sash: PAL.kumkum,
    crown: 'bun',
    pose: 'stand',
    tilak: true,
    glow: PAL.turmeric,
  });
  trishul(c, 690, 530, 0.8, PAL.gold);

  // Four-headed Brahma on right, bowed in humility
  brahmaFigure(c, {
    x: 960,
    y: 620,
    s: 0.95,
    heads: 4,
    pose: 'namaste',
  });

  hills(c, W, Hh, 660, 40, PAL.brown, 24);
  hills(c, W, Hh, 700, 20, PAL.deep, 25);
  c.restore();
}

const SCENES = [
  [0, sceneBrahma],
  [SC.dispute, sceneDispute],
  [SC.pillar, scenePillar],
  [SC.stretch, sceneStretch],
  [SC.challenge, sceneChallenge],
  [SC.search, sceneSearch],
  [SC.defeat, sceneDefeat],
  [SC.falsehood, sceneFalsehood],
  [SC.ketaki, sceneKetaki],
  [SC.truth, sceneTruth],
  [SC.sever, sceneSever],
  [SC.curse, sceneCurse],
  [SC.flowerCurse, sceneFlowerCurse],
  [SC.temples, sceneTemples],
  [SC.shunned, sceneShunned],
  [SC.moral, sceneMoral],
];
