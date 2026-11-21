import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 35.95;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 4.22, t: 'Did you know which planet in our\nsolar system spins {backwards}?' },
  { s: 5.32, e: 6.22, t: "It's {Venus}!" },
  { s: 7.32, e: 10.87, t: 'On Venus, the Sun rises in the\n{west} and sets in the {east}.' },
  { s: 11.97, e: 16.00, t: 'One day on Venus lasts\n{243} Earth days.' },
  { s: 16.55, e: 18.38, t: 'That is longer than its\nwhole {year}!' },
  { s: 19.48, e: 23.23, t: 'Scientists think a giant {collision}\nlong ago flipped it upside down.' },
  { s: 24.33, e: 28.16, t: 'Its thick clouds trap so much heat\nthat Venus is {hotter} than Mercury.' },
  { s: 29.26, e: 30.90, t: 'If you like knowing\n{facts} like this,' },
  { s: 30.90, e: 32.95, t: '{subscribe} and {follow}\nfor more.' },
];
export const SPEAK: Record<string, [number, number][]> = {
  host: [[0.7, 4.4], [5.2, 6.4], [7.2, 11.0], [11.9, 16.2], [16.4, 18.6], [19.4, 23.4], [24.2, 28.4], [29.1, 33.1]],
};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.0, e: 5.32, tag: 'Did you know?' },
  { s: 5.32, e: 7.32, tag: 'Venus!' },
  { s: 7.32, e: 11.97, tag: 'Backwards spin' },
  { s: 11.97, e: 16.55, tag: 'One day' },
  { s: 16.55, e: 19.48, tag: 'Day vs year' },
  { s: 19.48, e: 24.33, tag: 'Why?' },
  { s: 24.33, e: 29.26, tag: 'Hot!' },
  { s: 29.26, e: 35.95, tag: 'Follow' },
];

export const SFX: [string, number, number][] = [
  ['whoosh', 0.1, 0.4], ['pop', 0.8, 0.35], ['pop', 1.6, 0.3], ['pop', 2.0, 0.3], ['pop', 2.4, 0.3], ['boing', 3.2, 0.35],
  ['tada', 5.35, 0.6], ['stamp', 5.6, 0.55],
  ['whoosh', 7.6, 0.3], ['pop', 12.2, 0.3], ['ding', 15.6, 0.4],
  ['pop', 16.8, 0.3], ['boing', 17.3, 0.4],
  ['stamp', 21.0, 0.6], ['boing', 21.6, 0.4],
  ['pop', 24.6, 0.3], ['pop', 27.0, 0.3], ['stamp', 27.3, 0.5],
  ['pop', 29.5, 0.3], ['pop', 30.2, 0.3], ['pop', 30.9, 0.3], ['ding', 31.9, 0.4],
];
