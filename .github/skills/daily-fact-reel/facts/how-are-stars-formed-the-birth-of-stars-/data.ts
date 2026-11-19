import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 61.62;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 4.08, t: 'Have you ever {wondered} how stars\nare born in the vast darkness of' },
  { s: 4.08, e: 4.38, t: '{space}?' },
  { s: 4.93, e: 8.61, t: 'The story begins inside {enormous}\nclouds of gas and dust called' },
  { s: 8.61, e: 9.08, t: '{nebulae}.' },
  { s: 9.63, e: 13.57, t: 'These clouds contain mostly\nhydrogen gas, the main {ingredient}' },
  { s: 13.57, e: 15.06, t: '{needed} to create stars.' },
  { s: 15.61, e: 19.16, t: 'Over {millions} of years, gravity\nslowly pulls the gas and dust' },
  { s: 19.16, e: 22.18, t: 'together, forming a dense and\n{increasingly} hot core.' },
  { s: 22.73, e: 26.09, t: 'As more material gathers, the\n{temperature} and pressure at the' },
  { s: 26.09, e: 27.41, t: 'center {continue} to rise.' },
  { s: 27.96, e: 31.40, t: '{Eventually}, the core becomes hot\nenough to trigger a powerful' },
  { s: 31.40, e: 33.09, t: '{process} called nuclear fusion.' },
  { s: 33.64, e: 37.16, t: 'Hydrogen atoms begin {combining} to\nform helium, releasing enormous' },
  { s: 37.16, e: 39.76, t: '{amounts} of energy in the form of\nheat and light.' },
  { s: 40.31, e: 42.98, t: 'And just like that, a new {star} is\nborn!' },
  { s: 43.53, e: 47.52, t: 'Some stars shine for millions or\neven billions of years, {depending}' },
  { s: 47.52, e: 48.91, t: 'on their {size} and mass.' },
  { s: 49.46, e: 52.76, t: 'Isn\'t it amazing that the stars\n{lighting} up our night sky were' },
  { s: 52.76, e: 54.51, t: 'once just {clouds} of gas and dust?' },
  { s: 55.06, e: 58.62, t: 'Every star has a {beginning}, and it\nall starts with gravity!' },
];
export const SPEAK: Record<string, [number, number][]> = {
  host: [
    [0.80, 4.38],
    [49.46, 54.51],
    [55.06, 58.62],
  ],
};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.0, e: 4.6, tag: 'Cosmic Mystery' },
  { s: 4.6, e: 9.3, tag: 'Stellar Nebula' },
  { s: 9.3, e: 15.3, tag: 'The Ingredient' },
  { s: 15.3, e: 22.4, tag: 'Gravity at Work' },
  { s: 22.4, e: 27.7, tag: 'Rising Pressure' },
  { s: 27.7, e: 33.3, tag: 'Nuclear Fusion' },
  { s: 33.3, e: 40.0, tag: 'Cosmic Engine' },
  { s: 40.0, e: 43.2, tag: 'Star Ignition' },
  { s: 43.2, e: 49.1, tag: 'Stellar Lifespan' },
  { s: 49.1, e: 61.62, tag: 'The Takeaway' },
];

export const SFX: [string, number, number][] = [
  ['whoosh', 0.85, 0.35],
  ['pop', 5.10, 0.30],
  ['pop', 10.10, 0.30],
  ['whoosh', 15.90, 0.40],
  ['stamp', 28.30, 0.55],
  ['pop', 34.00, 0.35],
  ['stamp', 40.40, 0.60],
  ['printer', 44.10, 0.35],
  ['whoosh', 55.20, 0.40],
];
