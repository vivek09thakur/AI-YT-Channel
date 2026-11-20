import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 69.67;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 3.81, t: 'Have you ever {wondered} what\nhappens when a massive star dies?' },
  { s: 4.36, e: 8.54, t: 'When a giant star runs out of\nfuel, it explodes in a {spectacular}' },
  { s: 8.54, e: 9.19, t: '{supernova}.' },
  { s: 9.74, e: 13.67, t: 'But deep inside, its core can\ncollapse into something {incredibly}' },
  { s: 13.67, e: 15.45, t: 'small and {unbelievably} dense.' },
  { s: 16.00, e: 17.85, t: 'This is called a {neutron} star.' },
  { s: 18.40, e: 22.42, t: 'Imagine {squeezing} the mass of our\nentire Sun into a sphere just 20' },
  { s: 22.42, e: 23.39, t: '{kilometers} wide.' },
  { s: 23.94, e: 27.34, t: 'That\'s roughly the size of a city,\nyet it {contains} more matter than' },
  { s: 27.34, e: 28.97, t: 'hundreds of {thousands} of Earths.' },
  { s: 29.52, e: 33.21, t: 'Neutron stars are so dense that a\nsingle {teaspoon} of their material' },
  { s: 33.21, e: 35.31, t: 'could weigh {billions} of tons on\nEarth.' },
  { s: 35.86, e: 40.21, t: 'Some neutron stars spin {incredibly}\nfast, rotating hundreds of times' },
  { s: 40.21, e: 41.05, t: 'every {second}.' },
  { s: 41.60, e: 43.26, t: 'These are called {pulsars}.' },
  { s: 43.81, e: 47.74, t: 'They shoot beams of radiation into\nspace like cosmic {lighthouses}.' },
  { s: 48.29, e: 51.92, t: 'Even more {fascinating}, some\nneutron stars have magnetic fields' },
  { s: 51.92, e: 54.32, t: '{trillions} of times stronger than\nEarth\'s.' },
  { s: 54.87, e: 57.68, t: 'These extreme objects are known as\n{magnetars}.' },
  { s: 58.23, e: 61.43, t: 'Neutron stars are among the\n{strangest} and most powerful' },
  { s: 61.43, e: 62.83, t: 'objects in the {universe},' },
  { s: 63.05, e: 66.23, t: 'reminding us that space is far\nmore {mysterious} than we can' },
  { s: 66.23, e: 66.67, t: '{imagine}.' },
];
export const SPEAK: Record<string, [number, number][]> = {};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.0, e: 4.0, tag: 'Did you know?' },
  { s: 4.0, e: 15.8, tag: 'Supernova' },
  { s: 15.8, e: 23.7, tag: 'City-Sized Sun' },
  { s: 23.7, e: 35.5, tag: 'Extreme Density' },
  { s: 35.5, e: 47.7, tag: 'Cosmic Pulsars' },
  { s: 47.7, e: 58.0, tag: 'Magnetars' },
  { s: 58.0, e: 69.67, tag: 'The Universe' },
];

export const SFX: [string, number, number][] = [
  ['pop', 3.81, 0.3],
  ['whoosh', 4.36, 0.4],
  ['stamp', 16.0, 0.55],
  ['pop', 23.94, 0.3],
  ['pop', 29.52, 0.3],
  ['whoosh', 41.6, 0.4],
  ['stamp', 54.87, 0.55],
];
