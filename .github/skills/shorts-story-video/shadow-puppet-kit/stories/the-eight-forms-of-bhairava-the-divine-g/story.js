const TITLE = 'ASHTA BHAIRAVA';
const HOOK = ['The Divine Guardians', 'of the Eight Directions'];
const REEL_SUBTITLE = 'The Eight Forms of Bhairava';

const SC = {
  intro: 0,
  ashta: 8.5,
  asitanga: 22.0,
  ruru: 26.5,
  chanda: 31.0,
  krodha: 36.0,
  unmatta: 40.5,
  kapala: 45.0,
  bhishana: 49.5,
  samhara: 54.5,
  kashi: 62.0,
  matrikas: 70.5,
  purpose: 76.0,
  wisdom: 87.0,
  batuk: 98.0,
  mystery: 111.0,
  outro: 118.0
};
const FADE = 0.9;
const REEL_FOCUS = {
  intro: [640, 400],
  ashta: [640, 400],
  asitanga: [640, 400],
  ruru: [640, 400],
  chanda: [640, 400],
  krodha: [640, 400],
  unmatta: [640, 400],
  kapala: [640, 400],
  bhishana: [640, 400],
  samhara: [640, 400],
  kashi: [640, 400],
  matrikas: [640, 400],
  purpose: [640, 400],
  wisdom: [640, 400],
  batuk: [640, 400],
  mystery: [640, 400],
  outro: [640, 400]
};

const BEATS = [
  { n: 1, name: 'Intro', t0: 0, t1: SC.ashta, vo: 'Did you know that Lord Shiva\'s fierce form...', screen: 'Shiva fierce form' },
  { n: 2, name: 'Ashta Bhairavas', t0: SC.ashta, t1: SC.asitanga, vo: 'These divine manifestations are known as the Ashta Bhairavas.', screen: 'Eight forms' },
  { n: 3, name: 'Asitanga', t0: SC.asitanga, t1: SC.ruru, vo: 'Asitanga Bhairava, guardian of the East.', screen: 'Asitanga' },
  { n: 4, name: 'Ruru', t0: SC.ruru, t1: SC.chanda, vo: 'Ruru Bhairava, South-East.', screen: 'Ruru' },
  { n: 5, name: 'Chanda', t0: SC.chanda, t1: SC.krodha, vo: 'Chanda Bhairava, South.', screen: 'Chanda' },
  { n: 6, name: 'Krodha', t0: SC.krodha, t1: SC.unmatta, vo: 'Krodha Bhairava, South-West.', screen: 'Krodha' },
  { n: 7, name: 'Unmatta', t0: SC.unmatta, t1: SC.kapala, vo: 'Unmatta Bhairava, West.', screen: 'Unmatta' },
  { n: 8, name: 'Kapala', t0: SC.kapala, t1: SC.bhishana, vo: 'Kapala Bhairava, North-West.', screen: 'Kapala' },
  { n: 9, name: 'Bhishana', t0: SC.bhishana, t1: SC.samhara, vo: 'Bhishana Bhairava, North.', screen: 'Bhishana' },
  { n: 10, name: 'Samhara', t0: SC.samhara, t1: SC.kashi, vo: 'Samhara Bhairava, North-East.', screen: 'Samhara' },
  { n: 11, name: 'Kashi', t0: SC.kashi, t1: SC.matrikas, vo: 'Circle of protection around Kashi.', screen: 'Kashi' },
  { n: 12, name: 'Matrikas', t0: SC.matrikas, t1: SC.purpose, vo: 'Ashta Matrikas.', screen: 'Matrikas' },
  { n: 13, name: 'Purpose', t0: SC.purpose, t1: SC.wisdom, vo: 'Protect and destroy evil.', screen: 'Purpose' },
  { n: 14, name: 'Wisdom', t0: SC.wisdom, t1: SC.batuk, vo: 'Divine power has many forms.', screen: 'Wisdom' },
  { n: 15, name: 'Batuk', t0: SC.batuk, t1: SC.mystery, vo: 'Batuk Bhairava.', screen: 'Batuk' },
  { n: 16, name: 'Mystery', t0: SC.mystery, t1: SC.outro, vo: 'Childlike form.', screen: 'Mystery' },
  { n: 17, name: 'Outro', t0: SC.outro, t1: DURATION, vo: 'Next episode.', screen: 'Outro' }
];

function sceneIntro(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.7);
  sun(c, 640, 300, 100, PAL.kumkum, 3);
  hills(c, W, Hh, 540, 80, PAL.maroon, 1);
  hills(c, W, Hh, 620, 60, PAL.deep, 2);
  figure(c, { x: 640, y: 700, s: 1.4, skin: PAL.ash, cloth: PAL.ink, sash: PAL.kumkum, crown: 'tall', tilak: true, pose: 'stand', glow: PAL.kumkum });
  c.restore();
}

function sceneAshta(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK); streaks(c, W, Hh, t, { seed: 3 });
  sun(c, 640, 250, 120, PAL.saffron, 3);
  hills(c, W, Hh, 580, 70, PAL.burnt, 3);
  temple(c, { x: 640, y: 580, s: 0.8, col: PAL.brown }, t);
  for(let i=0; i<8; i++) {
    const a = i * Math.PI / 4 + t * 0.2;
    const x = 640 + Math.cos(a) * 250, y = 520 + Math.sin(a) * 100;
    animal(c, { x, y, s: 0.6, kind: 'dog', col: PAL.ink });
  }
  c.restore();
}

function makeBhairavaScene(formName, color) {
  return function(c, W, Hh, t) {
    c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.5);
    sun(c, 640, 320, 90, color, 3);
    hills(c, W, Hh, 600, 60, PAL.deep, 4);
    figure(c, { x: 640, y: 700, s: 1.5, skin: PAL.ash, cloth: color, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'stand', glow: color });
    animal(c, { x: 450, y: 700, s: 1.0, kind: 'dog', col: PAL.ink });
    animal(c, { x: 830, y: 700, s: 1.0, kind: 'dog', col: PAL.ink });
    c.restore();
  };
}

const sceneAsitanga = makeBhairavaScene('Asitanga', PAL.saffron);
const sceneRuru = makeBhairavaScene('Ruru', PAL.turmeric);
const sceneChanda = makeBhairavaScene('Chanda', PAL.kumkum);
const sceneKrodha = makeBhairavaScene('Krodha', PAL.vermilion);
const sceneUnmatta = makeBhairavaScene('Unmatta', PAL.rama);
const sceneKapala = makeBhairavaScene('Kapala', PAL.peacock);
const sceneBhishana = makeBhairavaScene('Bhishana', PAL.maroon);
const sceneSamhara = makeBhairavaScene('Samhara', PAL.indigo);

function sceneKashi(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 5 });
  sun(c, 640, 280, 110, PAL.turmeric, 3);
  skyline(c, 640, 560, 0.7, PAL.brown, t);
  ocean(c, W, Hh, 560, t, [PAL.rama, PAL.peacock]);
  for(let i=0; i<8; i++) {
    const a = i * Math.PI / 4;
    const x = 640 + Math.cos(a) * 350, y = 520 + Math.sin(a) * 120;
    figure(c, { x, y, s: 0.7, skin: PAL.ash, cloth: PAL.saffron, sash: PAL.gold, crown: 'bun', tilak: true });
  }
  c.restore();
}

function sceneMatrikas(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK);
  sun(c, 640, 300, 100, PAL.lotus, 3);
  hills(c, W, Hh, 600, 60, PAL.maroon, 6);
  for(let i=0; i<8; i++) {
    const x = 200 + i * 125, y = 680;
    figure(c, { x, y, s: 0.75, skin: PAL.sandal, cloth: PAL.lotus, sash: PAL.gold, crown: 'long', face: 'woman', pose: 'stand' });
  }
  c.restore();
}

function scenePurpose(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.6);
  sun(c, 640, 250, 130, PAL.kumkum, 3);
  hills(c, W, Hh, 580, 70, PAL.deep, 7);
  flames(c, 640, 650, 1.5, t, 1, 9);
  figure(c, { x: 640, y: 700, s: 1.4, skin: PAL.ash, cloth: PAL.vermilion, sash: PAL.gold, crown: 'tall', tilak: true, pose: 'raise', glow: PAL.kumkum });
  c.restore();
}

function sceneWisdom(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 8 });
  sun(c, 640, 320, 100, PAL.saffron, 3);
  hills(c, W, Hh, 560, 60, PAL.burnt, 8);
  temple(c, { x: 640, y: 560, s: 0.7, col: PAL.brown }, t);
  figure(c, { x: 640, y: 700, s: 1.2, skin: PAL.ash, cloth: PAL.turmeric, sash: PAL.kumkum, crown: 'bun', tilak: true, pose: 'namaste' });
  c.restore();
}

function sceneBatuk(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, WARM); streaks(c, W, Hh, t, { seed: 9 });
  sun(c, 640, 280, 140, PAL.turmeric, 3);
  hills(c, W, Hh, 600, 50, PAL.burnt, 9);
  figure(c, { x: 640, y: 700, s: 1.0, skin: PAL.sandal, cloth: PAL.saffron, sash: PAL.gold, crown: 'bun', tilak: true, pose: 'stand', glow: PAL.turmeric });
  animal(c, { x: 520, y: 700, s: 0.8, kind: 'dog', col: PAL.ink });
  c.restore();
}

function sceneMystery(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, DUSK); stars(c, W, Hh, t, 0.5);
  sun(c, 640, 300, 110, PAL.marigold, 3);
  hills(c, W, Hh, 580, 60, PAL.maroon, 10);
  temple(c, { x: 640, y: 580, s: 0.75, col: PAL.brown }, t);
  figure(c, { x: 640, y: 700, s: 1.0, skin: PAL.ash, cloth: PAL.saffron, sash: PAL.gold, crown: 'bun', tilak: true, pose: 'stand' });
  c.restore();
}

function sceneOutro(c, W, Hh, t) {
  c.save(); sky(c, W, Hh, NIGHT); stars(c, W, Hh, t, 0.8);
  sun(c, 640, 350, 90, PAL.saffron, 3);
  hills(c, W, Hh, 620, 50, PAL.deep, 11);
  figure(c, { x: 640, y: 700, s: 1.2, skin: PAL.ash, cloth: PAL.ink, sash: PAL.saffron, crown: 'tall', tilak: true, pose: 'namaste', glow: PAL.saffron });
  c.restore();
}

const SCENES = [
  [0, sceneIntro],
  [SC.ashta, sceneAshta],
  [SC.asitanga, sceneAsitanga],
  [SC.ruru, sceneRuru],
  [SC.chanda, sceneChanda],
  [SC.krodha, sceneKrodha],
  [SC.unmatta, sceneUnmatta],
  [SC.kapala, sceneKapala],
  [SC.bhishana, sceneBhishana],
  [SC.samhara, sceneSamhara],
  [SC.kashi, sceneKashi],
  [SC.matrikas, sceneMatrikas],
  [SC.purpose, scenePurpose],
  [SC.wisdom, sceneWisdom],
  [SC.batuk, sceneBatuk],
  [SC.mystery, sceneMystery],
  [SC.outro, sceneOutro]
];
