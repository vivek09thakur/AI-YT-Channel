import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = 101.9;

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [
  { s: 0.80, e: 4.76, t: '{Imagine} a place in space where\nnothing can escape, not even' },
  { s: 4.76, e: 5.16, t: '{light}.' },
  { s: 5.71, e: 7.00, t: 'Sounds {impossible}, right?' },
  { s: 7.55, e: 9.24, t: 'But such a place {really} exists.' },
  { s: 9.79, e: 11.13, t: 'It is {called} a Black Hole!' },
  { s: 11.68, e: 15.64, t: 'A black hole is an {extremely}\npowerful region in space where' },
  { s: 15.64, e: 19.87, t: 'gravity is so strong that {anything}\ncoming too close gets pulled' },
  { s: 19.87, e: 20.34, t: '{inside}.' },
  { s: 20.89, e: 22.41, t: 'But how are black holes {formed}?' },
  { s: 22.96, e: 27.02, t: 'When a {massive} star runs out of\nits nuclear fuel, it can no longer' },
  { s: 27.02, e: 29.42, t: '{support} itself against its own\ngravity.' },
  { s: 29.97, e: 32.56, t: 'Its core {collapses} under its\nenormous weight.' },
  { s: 33.11, e: 37.18, t: 'If the {remaining} core is massive\nenough, it collapses into an' },
  { s: 37.18, e: 40.31, t: '{incredibly} dense region, creating\na black hole.' },
  { s: 40.86, e: 42.71, t: 'But here\'s the most {fascinating}\npart.' },
  { s: 43.26, e: 46.34, t: 'A black hole has a {boundary} called\nthe Event Horizon.' },
  { s: 46.89, e: 50.90, t: 'Once {anything} crosses this\nboundary, it cannot escape, not' },
  { s: 50.90, e: 51.66, t: 'even {light}.' },
  { s: 52.21, e: 54.66, t: 'That\'s why black holes appear\n{completely} dark.' },
  { s: 55.21, e: 58.50, t: 'But don\'t imagine them as giant\ncosmic vacuum {cleaners}.' },
  { s: 59.05, e: 62.07, t: 'They don\'t randomly swallow\n{everything} in the universe.' },
  { s: 62.62, e: 66.68, t: '{Objects} can orbit around them,\njust like planets orbit the Sun,' },
  { s: 66.68, e: 69.25, t: 'as long as they stay at a safe\n{distance}.' },
  { s: 69.80, e: 74.34, t: '{Scientists} cannot see black holes\ndirectly, but they can detect them' },
  { s: 74.34, e: 78.21, t: 'by {observing} how they affect\nnearby stars, gas, and light.' },
  { s: 78.76, e: 82.83, t: 'And here\'s something {mind-blowing}:\nsome black holes are millions or' },
  { s: 82.83, e: 85.81, t: 'even {billions} of times more\nmassive than our Sun!' },
  { s: 86.36, e: 90.93, t: 'The universe is full of {mysteries},\nand black holes are among its most' },
  { s: 90.93, e: 92.26, t: '{fascinating} secrets.' },
  { s: 92.81, e: 96.87, t: 'A place where time, space, and\n{gravity} behave in ways that' },
  { s: 96.87, e: 98.90, t: 'challenge {everything} we know!' },
];
export const SPEAK: Record<string, [number, number][]> = {};

export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [
  { s: 0.8, e: 5.16, tag: 'Deep Space' },
  { s: 9.79, e: 11.13, tag: 'Black Hole' },
  { s: 22.96, e: 29.42, tag: 'Star Death' },
  { s: 43.26, e: 46.34, tag: 'Event Horizon' },
  { s: 62.62, e: 69.25, tag: 'Orbit' },
  { s: 78.76, e: 85.81, tag: 'Massive Scale' },
  { s: 92.81, e: 98.90, tag: 'Cosmic Mystery' }
];

export const SFX: [string, number, number][] = [
  ['whoosh', 0.8, 0.4],
  ['pop', 9.79, 0.3],
  ['whoosh', 22.96, 0.4],
  ['stamp', 33.11, 0.55],
  ['pop', 43.26, 0.3],
  ['whoosh', 62.62, 0.4],
  ['pop', 78.76, 0.3]
];
