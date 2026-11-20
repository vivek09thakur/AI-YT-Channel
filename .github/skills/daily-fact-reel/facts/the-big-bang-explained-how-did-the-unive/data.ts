import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 121.63;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 3.51, t: 'Have you ever {wondered} how the\nentire universe began?' },
  { s: 4.06, e: 8.14, t: 'How did {billions} of galaxies,\nstars, planets, and even human' },
  { s: 8.14, e: 9.98, t: 'beings come into {existence}?' },
  { s: 10.53, e: 14.25, t: 'The answer takes us back\n{approximately} 13.8 billion years,' },
  { s: 14.25, e: 16.43, t: 'to an {event} known as the Big Bang.' },
  { s: 16.98, e: 20.65, t: 'But here\'s something {surprising}:\nthe Big Bang wasn\'t an explosion' },
  { s: 20.65, e: 21.50, t: 'in {empty} space.' },
  { s: 22.05, e: 25.55, t: 'It was the rapid {expansion} of\nspace itself from an extremely hot' },
  { s: 25.55, e: 26.75, t: 'and {dense} early state.' },
  { s: 27.30, e: 31.18, t: 'In the beginning, the universe was\n{incredibly} hot, with energy and' },
  { s: 31.18, e: 33.70, t: 'tiny {particles} filling the\nexpanding space.' },
  { s: 34.25, e: 37.48, t: 'As the universe expanded, it\n{gradually} cooled down.' },
  { s: 38.03, e: 42.50, t: 'Tiny {particles} began combining to\nform atoms, mainly hydrogen and' },
  { s: 42.50, e: 42.98, t: '{helium}.' },
  { s: 43.53, e: 47.05, t: '{Millions} of years later, gravity\npulled enormous clouds of gas' },
  { s: 47.05, e: 50.18, t: '{together}, giving birth to the\nfirst stars and galaxies.' },
  { s: 50.73, e: 54.55, t: 'Inside stars, nuclear fusion\ncreated heavier {elements}.' },
  { s: 55.10, e: 58.25, t: 'When massive stars died and\nexploded as {supernovae}, they' },
  { s: 58.25, e: 60.62, t: 'scattered these elements\n{throughout} space.' },
  { s: 61.17, e: 64.63, t: 'Over {billions} of years, these\nelements became the building' },
  { s: 64.63, e: 67.92, t: 'blocks of new stars, planets, and\n{eventually} our Earth.' },
  { s: 68.47, e: 72.70, t: 'Around 4.5 {billion} years ago, our\nsolar system formed.' },
  { s: 73.25, e: 76.57, t: 'Gradually, Earth developed\n{conditions} that allowed life to' },
  { s: 76.57, e: 76.97, t: '{emerge}.' },
  { s: 77.52, e: 80.29, t: 'Simple life forms {appeared}\nbillions of years ago.' },
  { s: 80.84, e: 84.19, t: 'Through evolution over an\n{incredibly} long period, life' },
  { s: 84.19, e: 85.43, t: 'became more {complex},' },
  { s: 85.65, e: 88.89, t: '{eventually} leading to the\nincredible diversity of living' },
  { s: 88.89, e: 90.22, t: '{organisms} we see today,' },
  { s: 90.44, e: 91.81, t: '{including} humans.' },
  { s: 92.36, e: 95.79, t: 'And here\'s the most {fascinating}\npart: the carbon in your body,' },
  { s: 96.01, e: 99.60, t: 'the oxygen you {breathe}, and the\niron in your blood were created' },
  { s: 99.60, e: 102.40, t: 'through cosmic {processes} involving\nancient stars.' },
  { s: 102.95, e: 106.09, t: 'In a very real sense, we are made\nof {stardust}!' },
  { s: 106.64, e: 110.15, t: 'From the birth of the universe to\nthe {existence} of human beings,' },
  { s: 110.15, e: 112.35, t: 'it\'s a story {spanning} billions of\nyears.' },
  { s: 112.90, e: 115.00, t: 'We are not {separate} from the\nuniverse.' },
  { s: 115.55, e: 118.63, t: 'We are a part of it, and the\n{universe} lives within us!' },
];
export const SPEAK: Record<string, [number, number][]> = {};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.0, e: 4.0, tag: 'The Cosmos' },
  { s: 10.5, e: 16.9, tag: '13.8 Billion Years Ago' },
  { s: 22.0, e: 27.0, tag: 'Rapid Expansion' },
  { s: 43.5, e: 50.2, tag: 'Gravity & Stars' },
  { s: 61.1, e: 67.9, tag: 'Building Blocks' },
  { s: 73.2, e: 77.0, tag: 'Early Earth' },
  { s: 92.3, e: 95.8, tag: 'Human Body' },
  { s: 102.9, e: 106.1, tag: 'Stardust' }
];

export const SFX: [string, number, number][] = [
  ['pop', 10.53, 0.3],
  ['whoosh', 22.05, 0.4],
  ['pop', 43.53, 0.3],
  ['stamp', 55.10, 0.55],
  ['pop', 68.47, 0.3],
  ['pop', 102.95, 0.35]
];
