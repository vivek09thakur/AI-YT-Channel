import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 63.69;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 3.24, t: 'Have you ever wondered\nwhy the {Sun} is called a star,' },
  { s: 3.79, e: 6.95, t: 'even though it looks so different\nfrom the stars we see at {night}?' },
  { s: 7.50, e: 9.24, t: 'The answer is {fascinating}!' },
  { s: 9.79, e: 12.30, t: 'The Sun is actually a giant ball\nof extremely {hot gases},' },
  { s: 12.30, e: 15.17, t: 'mainly {hydrogen} and helium' },
  { s: 15.72, e: 20.09, t: 'Deep inside its core, a process\ncalled {nuclear fusion} takes place' },
  { s: 20.64, e: 24.20, t: 'During nuclear fusion,\n{hydrogen atoms} combine to form helium,' },
  { s: 24.20, e: 27.97, t: 'releasing enormous amounts of {energy}\nin the form of heat and light' },
  { s: 28.52, e: 31.04, t: 'This is exactly what\nmakes the Sun a {star}!' },
  { s: 31.59, e: 34.94, t: 'So why do other stars look like\n{tiny dots} in the night sky?' },
  { s: 35.49, e: 38.12, t: "It's because they are\nextremely {far away} from Earth" },
  { s: 38.67, e: 41.80, t: 'In fact, the Sun is also a star,\nbut it appears much {bigger}' },
  { s: 41.80, e: 45.20, t: 'because it is the {closest star}\nto our planet' },
  { s: 45.75, e: 50.89, t: 'Without the Sun, Earth would be\n{dark}, cold, and unable to support life' },
  { s: 51.44, e: 54.25, t: "So remember, the Sun isn't\njust a {source of light}" },
  { s: 54.80, e: 58.21, t: "It's the {nearest star} to Earth\nand the heart of our solar system!" },
  { s: 58.76, e: 60.69, t: "And that's why the Sun\nis a {star}!" }
];

export const SPEAK: Record<string, [number, number][]> = {
  astronomer: [
    [0.80, 6.95],
    [7.50, 9.24]
  ]
};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.0, e: 7.2, tag: 'Cosmic Mystery' },
  { s: 7.2, e: 9.5, tag: 'The Secret' },
  { s: 9.5, e: 15.4, tag: 'Inside the Sun' },
  { s: 15.4, e: 20.3, tag: 'The Solar Core' },
  { s: 20.3, e: 28.2, tag: 'Nuclear Fusion' },
  { s: 28.2, e: 31.3, tag: 'What Is a Star' },
  { s: 31.3, e: 38.4, tag: 'Distant Stars' },
  { s: 38.4, e: 45.5, tag: 'Cosmic Distance' },
  { s: 45.5, e: 51.1, tag: 'Earth in the Dark' },
  { s: 51.1, e: 58.5, tag: 'Heart of System' },
  { s: 58.5, e: 63.69, tag: 'The Takeaway' }
];

export const SFX: [string, number, number][] = [
  ['whoosh', 7.4, 0.4],
  ['pop', 9.8, 0.3],
  ['pop', 12.3, 0.3],
  ['stamp', 17.5, 0.5],
  ['whoosh', 20.8, 0.4],
  ['pop', 24.5, 0.35],
  ['pop', 28.6, 0.35],
  ['whoosh', 35.6, 0.4],
  ['pop', 41.8, 0.35],
  ['stamp', 46.2, 0.55],
  ['pop', 54.9, 0.35]
];
