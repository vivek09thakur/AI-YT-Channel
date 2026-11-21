# Stickman fact reel: rules for the scene writer

You write the two story files of a Remotion project that turns a recorded English "did you know" fact narration into a 9:16 animated
reel (1080x1920, 30 fps). Look: **black-outline stick figures** (round head, dot eyes, line mouth, tube limbs, coloured
shirt) on **bright flat colour backgrounds** with colourful props, bold rounded type and lots of motion. The narration is
already recorded and timed; you receive every line with its start/end second. Your job:
captions, scene tags, speaker windows, sound effects and one animated scene per beat, so that **what is on screen shows
what the voice says at that moment** and the figures are **always moving**.

Return exactly three blocks, nothing else (no prose before or after):

```
=== FILE: meta.json ===
{ "title": "...", "description": "...", "question": "...", "fact": "...", "category": "..." }
=== FILE: data.ts ===
...complete file...
=== FILE: scenes.tsx ===
...complete file...
```

`meta.json`: `title` short English title (max 60 chars, phrased as the hook question), `description` 1-2 sentences for
the upload (the fact in plain words), `question` / `fact` / `category` copied from the brief.

## data.ts (must keep this exact shape)

```ts
import rms from './rms.json';
export const RMS: number[] = rms as number[];
export const TOTAL = <DURATION from the brief>;   // never change this number

export type Cap = { s: number; e: number; t: string; who?: string };
export const CAPS: Cap[] = [ ... ];
export const SPEAK: Record<string, [number, number][]> = { host: [[...], [...]] };
export const SCENE_TAGS: { s: number; e: number; tag: string }[] = [ ... ];
export const SFX: [string, number, number][] = [ ... ];
```

- **CAPS**: one caption per narration line, in order. `s`/`e` = that line's start/end seconds from the brief (you may
  tighten `e` by up to 0.3 s; never start a caption before its line starts). `t` = the line's exact words (do not
  paraphrase, drop or add words; a trailing full stop may go). Mark 1-2 key words per caption with `{word}` (rendered
  red). Insert `\n` to break into at most 2 lines of <= 34 characters each (count without braces). A line longer than
  68 characters is split into two captions at a comma, each with its own time range inside the line. If the captions
  break these rules the pipeline rebuilds CAPS mechanically, so put your effort into the scenes.
- **SPEAK**: the host's speaking windows `[start, end]` in seconds (leave out any silence longer than 1 s so the mouth
  stays closed there). The mouth animates only inside these windows and only while the voice is loud, so +0.2 s
  slack is fine. Pass `talk={mouthOpen('host', t)}` to the host `Stick`.
- **SCENE_TAGS**: 1-3 words naming the beat of each scene ('Did you know?', 'Venus!', 'One day', 'Why?', 'Follow').
  One tag per scene; a gap is allowed.
- **SFX**: `[name, second, volume]` with name in `pop | whoosh | stamp | ding | boing | drum | tada | printer`.
  `pop` 0.3 when a card/icon pops in, `tada` 0.6 on the answer reveal, `ding` 0.4 for a tick or a number landing,
  `boing` 0.4 for a bounce, `stamp` 0.55 for a stamp, `drum` 0.5 for a build-up, `whoosh` 0.4 for a slide. A soft tick on every cut and the ambient pad are added automatically. 8-20 entries.

## scenes.tsx (structure)

```tsx
import React from 'react';
import { Stage } from './chrome';
import { C } from './theme';
import { SP, useT, sp, ramp, shake, mouthOpen, Flat, Spot, Sky, Space, Room, Stage3, Ground, GROUND, Desk, Board } from './kit';
import { Stick, Walker, Crowd } from './figures';
import { pop, Big, Label, Card, Counter, Bubble, Thought, QMark, Exclaim, Bulb, Check, Cross, Heart, Star, Arrow, Draw,
         Sun, Planet, Earth, Moon, Clock, Bars, Sign, Confetti, LikeIcon, FollowIcon, CommentIcon, Stamp } from './props';

const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);          // f local frame, t absolute second, lf(sec) local frame of an absolute second
  return (
    <Stage dur={dur}>
      <Spot color={C.yellow} />             // a background first (full 540x960)
      <Ground color={C.orange} />           // ground line at y = GROUND (620) when the figure stands
      <Stick x={270} y={GROUND} pose="wave" face="happy" shirt={C.blue} talk={mouthOpen('host', t)} />
      <Big x={270} y={190} text="DID YOU KNOW?" k={pop(f, lf(0.8))} color={C.red} />
    </Stage>
  );
};
// ...more scenes...
export const SCENES: { s: number; e: number; C: React.FC<SP> }[] = [ { s: 0.0, e: 2.3, C: S0 }, ... ];
```

Hard rules (checked by a script; failing any of them means a rewrite):

1. Only these imports: `react`, `remotion`, `./theme`, `./chrome`, `./figures`, `./props`, `./kit`, `./data`. No images, no `staticFile`.
2. Every scene body returns `<Stage dur={dur}>` whose children are **SVG elements only** (rect, path, circle, g, text,
   or the kit components, which are SVG). HTML (`div`, `span`) inside Stage renders nothing.
3. `SCENES` is in time order, contiguous (each `e` equals the next `s`), starts at 0.0 and the last `e` is exactly `TOTAL`.
4. One cut per 2-5 s. No scene longer than 10 s, none shorter than 1.2 s. Cut at narration line boundaries only.
5. **Every scene contains at least one `<Stick>`, `<Walker>` or `<Crowd>`** (the host), and **every scene visibly moves**:
   the script renders two frames per scene (30 % and 70 % in) and rejects a scene whose pixels barely change. Use a
   pose that animates by itself (walk, run, jump, dance, cheer, wave, think, shrug, explain, point), change the pose on a
   beat (`pose={t < 12.4 ? 'explain' : 'cheer'}`), move the figure (`x={100 + 200 * ramp(f, 0, 20)}` or `<Walker>`),
   and pop props during the scene with `k={pop(f, lf(sec))}` (not all at frame 0).
6. **Fact shape** (one scene per narration line, the first line may take two):
   - hook scene (the question): host enters/waves or `think`, `Big` "DID YOU KNOW?" + `QMark`, the subject drawn as a
     prop (Planet, Clock, Earth...) popping in while the question is asked;
   - answer scene (starts at the answer line): `Stamp` or `Big` with the answer words, `Confetti` or `Exclaim`, host `cheer`;
   - explanation scenes: show the fact (Counter for numbers, Bars for comparisons, Planet/Earth/Sun/Moon/Clock, Arrow,
     Board with a drawing, Card with a Label), host `explain` / `pointup` / `shrug` / `point`;
   - final CTA scene (the subscribe/follow line) holding until `TOTAL`: `LikeIcon`, `CommentIcon`, `FollowIcon` popping
     in sequence, `Big` "FOLLOW FOR MORE", host `dance`, `Crowd` cheering, `Heart`.
7. Layout: design space 540x960. Keep content between y≈115 and y≈720 (tag chip above, caption card below). Figures
   stand at `y={GROUND}` (620) with `s` 0.9-1.1 (one host) or 0.6-0.8 (two figures at x≈150 and x≈390, `flip` on the
   right one). Props and text go in y 150-480. Never put text under y 700 or over the figure's head.
8. Text: `Big` for headlines (size 36-60, <= 16 chars), `Label` for short notes (size 20-30, <= 32 chars), `Counter` for
   numbers. Never repeat the caption sentence inside the scene; show a keyword, a number or a drawing instead.
9. Colours: use `C.*` only (yellow, orange, red, pink, purple, blue, sky, teal, green, lime, brown, navy, night, cream,
   paper, white, ink, grey). Change the background colour on most cuts. Outline strokes use `C.outline` (#141414).
10. Absolute times come from the brief: `pop(f, lf(12.4))` pops a prop at 12.4 s; `t > 17.8` toggles a state.
11. The host keeps the same `shirt` colour in every scene. Other figures (crowd, a second character) use other colours.
12. TypeScript must compile with `tsc --noEmit`: `look={[0, 0]}` is a tuple, `Walker` needs `from`, `to`, `s0`, `s1`, `t`.
13. Copy the STRUCTURE and ENERGY of the example below; write new content for the new fact.

## Content rules

Facts must match the narration. No politics, no real-person shaming, no medical or financial advice, respect religious
and cultural topics. Do not copy another channel's characters. Captions must equal the narration words.

## Process (do this in your head before writing)

1. Read all lines; map them to the fact shape above (one line per scene, two for the hook if it is short).
2. For each scene choose: background, host pose and where it changes, the one prop that shows the line and the second
   it pops, the tag.
3. Write CAPS from the lines, SPEAK, SCENE_TAGS, SFX.
4. Write the scene components and the SCENES list; check contiguity and that the last `e` equals TOTAL.
