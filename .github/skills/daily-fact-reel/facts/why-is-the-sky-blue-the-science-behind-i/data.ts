import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 59.11;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 4.62, t: 'Have you ever {wondered} why the sky\nlooks blue instead of purple,' },
  { s: 4.62, e: 5.46, t: '{green}, or red?' },
  { s: 6.01, e: 8.70, t: 'The answer lies in something\ncalled Rayleigh {Scattering}!' },
  { s: 9.25, e: 12.77, t: 'Sunlight may look white, but it is\nactually made up of {different}' },
  { s: 12.77, e: 15.08, t: 'colours, each with a different\n{wavelength}.' },
  { s: 15.63, e: 19.67, t: 'When sunlight enters Earth\'s\n{atmosphere}, it collides with tiny' },
  { s: 19.67, e: 21.30, t: 'gas {molecules} in the air.' },
  { s: 21.85, e: 25.96, t: 'These molecules scatter shorter\n{wavelengths} of light, like blue,' },
  { s: 25.96, e: 29.36, t: 'much more strongly than longer\n{wavelengths}, like red.' },
  { s: 29.91, e: 34.08, t: 'That\'s why blue light {spreads}\nacross the sky, making it appear' },
  { s: 34.08, e: 35.22, t: '{blue} to our eyes!' },
  { s: 35.77, e: 37.06, t: 'But here\'s something {interesting}…' },
  { s: 37.96, e: 41.75, t: 'During sunrise and sunset,\n{sunlight} travels through more' },
  { s: 41.75, e: 42.50, t: '{atmosphere}.' },
  { s: 43.05, e: 46.89, t: 'Much of the blue light gets\n{scattered} away, allowing more red' },
  { s: 46.89, e: 49.10, t: 'and {orange} light to reach our\neyes.' },
  { s: 49.65, e: 53.42, t: 'So, the next time you look at a\nblue sky, {remember} — you\'re' },
  { s: 53.42, e: 56.11, t: '{witnessing} the science of light in\naction!' },
];
export const SPEAK: Record<string, [number, number][]> = {
  narrator: [[0.8, 56.11]]
};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0, e: 5.8, tag: 'Did you know?' },
  { s: 5.8, e: 15.4, tag: 'Sunlight' },
  { s: 15.4, e: 35.6, tag: 'Rayleigh Scattering' },
  { s: 35.6, e: 49.3, tag: 'Sunsets' },
  { s: 49.3, e: 59.11, tag: 'The Takeaway' }
];

export const SFX: [string, number, number][] = [
  ['pop', 6.01, 0.3],
  ['whoosh', 15.63, 0.4],
  ['pop', 21.85, 0.3],
  ['whoosh', 37.96, 0.4],
  ['stamp', 49.65, 0.55]
];
