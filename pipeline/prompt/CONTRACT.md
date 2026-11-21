You write the scene code for a short animated story video. The video is drawn entirely in code on an HTML canvas
(1280x720) in a flat 2D vector, mid-century poster style rooted in Indian mythology art: amber/saffron skies with thin
horizontal streak lines, scalloped striped clouds, domed pavilion temples, geometric figures with almond eyes, a warm
Hindu palette (saffron, turmeric, kumkum red, marigold, Rama blue, peacock teal, temple gold, sandalwood cream, lotus
pink, tulsi green, maroon, indigo for night). The voice narration is already recorded; its per-line timestamps are given.
Your job: make pictures that match what is being said, at the moment it is said, for any story (any god, hero, epic,
folk tale or history), reusing the drawing helpers provided.

## What you must output

Exactly these blocks, nothing else outside them:

=== FILE: meta.json ===
{"title": "SHORT TITLE IN CAPS", "hook": ["two short lines", "for the 9:16 hook"], "subtitle": "A 2 minute story",
 "kinds": {"<line index>": "big" | "title" | "tag"}}
=== FILE: story.js ===
<JavaScript, see contract>
=== FILE: sound_score.js ===
<JavaScript, see contract>

`kinds` marks special narration lines (indices from the NARRATION list): `big` = a name said alone, shown as a large
glowing word (e.g. "Rama." "Shiva."); `title` = the one line that is the title card (if the script says the title near
the end, use that line; otherwise omit); `tag` = closing taglines after the title. Every other line is a normal caption.
Do not invent lines; do not change the times.

## Runtime contract

All files are concatenated inside one IIFE in this order: ref.js (helpers, given below), lines.js (generated:
`const DURATION`, `const LINES = [[t0, text, kind, t1], ...]`), narration.js (given below: `lineAt`, `drawLines`,
`stageFrame`, `explainerFrame`, helpers `pop`, `fade`, `cam`, `stars`, `WARM`, `DUSK`, `NIGHT`, `mixStops`), then
YOUR story.js, YOUR sound_score.js, then the shared 9:16 reel. So:

- story.js MUST define: `const TITLE` (string), `const HOOK` (array of 1–2 short strings), `const REEL_SUBTITLE`,
  `const SC` (scene start times), `const FADE = 0.9`, `const BEATS` (array of {n, name, t0, t1, vo, screen}),
  `const REEL_FOCUS` (see below), the scene functions `(c, W, Hh, t) => void`, and
  `const SCENES = [[0, sceneA], [SC.x, sceneB], ...]` sorted by time,
  first entry at 0. Do NOT define DURATION, LINES, lineAt, drawLines, stageFrame, explainerFrame, reelFrame, pop, fade,
  cam, stars, WARM, DUSK, NIGHT, mixStops: they exist already (redeclaring a const is a fatal error).
- The 9:16 Short is a full-frame crop of each 1280x720 scene: the frame shows the full 720 height and a 405 px wide
  window centred on a focus point. `REEL_FOCUS` maps each `SC` key (and `open` for the scene at t = 0) to `[x, y]` or
  to `(t) => [x, y]` in scene coordinates, so the window follows the subject (hero, sun, temple) and pans with moving
  characters. Keep the main subject of every scene inside x ± 200 of its focus, and put the hero near x ≈ 640 or set the
  focus explicitly. Captions sit in the bottom 400 px of the Short, so keep feet/ground near y 650–720 as in the example.
  Omitted keys default to `[640, 400]`.
- Each scene paints the whole 1280x720 frame opaquely (start with `sky(...)`), using only helpers from ref.js,
  narration.js, `H` (harness: `H.rng(seed)`, `H.rgba(col, a)`, `H.ease.{inOut,out,in,back}`, `H.vignette`) and standard
  canvas 2D. Animate with `t` (seconds). Scenes are called for any `t` inside their range and 0.9 s before it (crossfade),
  so never assume `t >= SC.x`; use `sm(a, b, t)`, `cl(x)`, `fade(t, t0, d)`, `pop(t, t0, d)`.
- Scene changes (`SC`) should sit in the breath just before the line they illustrate starts (0.2–0.5 s before `t0`),
  and there should be a new scene or a clear new action every 6–12 s. Last scene = title card composition if the script
  has a title line, else a calm closing shot. The video ends at DURATION (about 3 s after the last spoken word).
- sound_score.js MUST define `function scoreSound(k0)` exactly like the example (same `live(t)` guard, same helpers
  `drone`, `gong`, `bell`, `riser`, `whoosh`, `thunder`, `step`, `fire`, `sea`). Allowed `k.play` names: pop, tick, click,
  tock, blip, whoosh, swish, riser, thud, impact, stamp, ding, success, error, buzz, sparkle, glitch, shutter, count,
  paper, slap, tape, press, roller, erase, key, typing, typebar, bell, boot, crtOn, neon, coin, jump, hurt, powerup,
  select, text. Anything else throws. Keep the bed quiet (gains as in the example): a voice plays over it.
- Use `LINES[i][0]` to time cues to narration lines (indices are the NARRATION indices). Never hard-code an index that
  does not exist.
- Code must be plain ES2020 that runs in Chrome; no imports, no top-level await, no DOM access, no external assets, no
  fonts other than `FF`. Keep story.js under ~700 lines. Comment each scene with one line saying what it shows.

## Visual rules (from the style guide)

- One warm palette per video; use `PAL.*` colours only. Night = indigo/maroon, never flat black (black `PAL.ink` only
  for silhouettes and demons).
- Gods and heroes: `figure(...)` with `skin: PAL.rama` (blue) for Vishnu avatars/Krishna/Rama, `PAL.ash` or
  `PAL.sandal` for Shiva (add `tilak: true`, a crescent with `finial`/`crownOnly`), `PAL.sandal` for goddesses
  (`face: 'woman'`), `PAL.kesari` + `face: 'monkey'` + `tail: true` for Hanuman/vanaras, `PAL.burnt` for mortals.
  Demons: `ravana(...)` or dark `figure` with `skin: PAL.maroon`/`PAL.ink`, mace, glow red.
- EVERY scene must show a character or the story's named subject (`figure`, `ravana`, `vanara`, `animal`, `elephant`,
  or a primitive-built subject helper). The only exception is the final title-card scene. A scene of sky + sun + hills
  alone is a failure: the viewer sees an empty poster. The opening scene (t = 0) must already show the hero or subject.
- Draw order inside a scene: sky -> sun/rays/clouds -> far hills -> buildings -> near hills -> ground band ->
  CHARACTERS AND SUBJECTS LAST. Never call `hills(...)` (or paint any ground shape) after a figure or animal whose feet
  sit at or below that hill's baseline: it will bury them. If you want a foreground hill at y 680–720, draw it first and
  put the feet on it (y ≈ 690–705).
- Scale and contrast: a solo hero uses `s: 1.4–1.8`; two figures `s: 1.1–1.3`; crowds `0.7–0.9`. Animals via `animal`
  use `s: 1.3–2.0` when they are the subject. Pale skins (`PAL.ash`, `PAL.sandal`, `PAL.cream`) need a dark backdrop:
  a DUSK/NIGHT sky, or a `PAL.maroon`/`PAL.deep` hill band directly behind the torso, plus `glow`. Never put a pale
  figure directly on an orange/yellow sky with nothing behind it.
- Animals: `animal(c, { x, y, s, dir, kind, col, pose, ph, collar })` draws a flat four-legged silhouette, origin at the
  feet, facing `+x` when `dir: 1`. `kind`: `dog` (Bhairava's vahana), `deer` (golden deer, forest), `bull` (Nandi: use
  `col: PAL.cream`), `lion` (Durga's vahana: `col: PAL.turmeric`), `horse`. `pose`: `stand`, `walk` (pass `ph: t * 4`),
  `sit` (dog/lion). `collar` is a gold band by default; pass `false` for wild animals. Height ≈ `110*s` (dog) to
  `190*s` (horse). Do not improvise animals from loose ellipses.
- `figure` geometry: origin at the feet, slender 8-head proportions, about `290*s` px tall with a tall crown and
  `100*s` wide at the shoulders (arms reach about `105*s` beyond); knee-length dhoti for men, long skirt for
  `face: 'woman'`. Faces and shoots
  toward `+x` when `dir: 1` (`pose: 'aim'` with `bow: true, draw: 0..1` puts the bow in the extended hand and the arrow
  flies toward `dir`). Crowns: `bun`, `long` (flowing hair, goddesses), `tall`, `king`, `cap`, `none`.
- Lean on composition and light instead of detail: sun behind the hero (`sun` + `rays`), temple (`temple`), hills in
  depth-stacked bands (`hills` from far/light to near/dark), clouds (`cloudBank`), flags (`flag`), lotus for divinity,
  flames for destruction, `ocean` and `bridge` for sea crossings, `elephant` for royalty, `vanara` for armies,
  `crownOnly` for kingship, `bolt` for lightning, `title` for big words (but captions/title are already handled).
  But composition never replaces the subject: light and hills frame a character, they do not stand in for one.
- Movement: slow camera push (`cam`), parallax hills, walking figures (`pose: 'walk'` with `t`), rising suns, rays
  rotating, things popping in (`pop`) as their word is spoken. Avoid frantic motion; this is a poster coming alive.
- Respect the subject: no gore, no mocking, iconography consistent with the tradition (Shiva: trishul-like staff via
  `arms` + a drawn trident, snake optional, crescent, Nandi via `animal({ kind: 'bull', col: PAL.cream })`; Bhairava:
  `animal({ kind: 'dog' })` beside him; Krishna: flute via a thin rect, peacock feather via `PAL.peacock` leaf shape;
  Durga: `animal({ kind: 'lion', col: PAL.turmeric })`; Ganesha: draw the elephant head with `elephant`-style primitives
  at figure scale). When you draw something new, build it from primitives in a helper function inside story.js.

## Fix loop

If you are given build/test errors, return ALL three files again in full, corrected. Do not explain.
