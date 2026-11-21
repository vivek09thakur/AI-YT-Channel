---
name: stickman-reel
description: Remotion kit that turns an English "did you know" fact narration (MP3 + narration.json) into a 9:16 animated stickman fact reel with black-outline stick figures, colourful props and synced captions. Used by generate-stickman-reel.yml; can also be driven by hand.
---

# Stickman fact reel kit

Turns a **voice MP3 + `narration.json`** (from `pipeline/tts.py`) into a vertical video (1080×1920, 30 fps) in a stickman fact style: black-outline stick figures with coloured shirts, flat bright backgrounds, simple props, a caption card at the bottom, a small tag chip at the top and a subscribe/follow ending. In the Action the two story files (`src/data.ts`, `src/scenes.tsx`) are written by an LLM following `pipeline/prompt/CONTRACT_STICKMAN.md`; this file is the human cheat-sheet for the same kit.

All code is in `template/` (a ready Remotion project). The files in `src/data.ts` and `src/scenes.tsx` are an EXAMPLE (Venus fact); replace their contents completely for a new reel.

## Procedure
1. `cd template && npm ci`.
2. Voice: `cp <voice.mp3> public/voice.mp3`; `node prepare.mjs <TOTAL>` (fonts → `public/fonts`, procedural SFX + ambient pad → `public/sfx`); `python tools/make_rms.py public/voice.mp3 src/rms.json`.
3. Timing from `narration.json`: one line per paragraph with `t0`, `t1` (and `pause_before` if the script used `[pause N]`). `TOTAL` = the `duration` field (last `t1` + ≈1.5 s, rounded).
4. Write `src/data.ts` (`TOTAL`, `CAPS`, `SPEAK`, `SCENE_TAGS`, `SFX`) and `src/scenes.tsx` (one component per scene + `SCENES`).
5. `npx tsc --noEmit`; render one still per scene (`npx remotion still src/index.ts StoryVideo out/f.png --frame N --props '{"still":true}'`) and look at them; or run every automated check without an LLM: `python pipeline/stick/generate_stick_reel.py --check-only --topic "<q>" --narration <narration.json> --project template --kit . --slug <slug>`.
6. `npx remotion render src/index.ts StoryVideo out/reel.mp4 --codec h264 --crf 20 --overwrite`; `python pipeline/stick/finalize_reel.py --in out/reel.mp4 --out final.mp4 --thumb thumb.jpg --total <TOTAL>`.

## Hard rules (checked by `generate_stick_reel.py`)
- Scenes tile `[0, TOTAL]` with no gaps; cuts on voice pauses, 8–14 cuts per 35 s.
- Every scene has at least one `<Stick>` (or `Walker`/`Crowd`) and visible motion: poses animate by themselves, but also move the figure (walk, bob, turn, pop props in) – two stills at 30 % / 70 % of a scene must differ.
- Imports only from `./kit`, `./figures`, `./props`, `./theme`, `./chrome`, `./data`, `react`, `remotion`.
- SFX names: tick, pop, stamp, printer, whoosh, ding, boing, drum, tada, pad.
- Content stays between y≈115 and y≈720 in the 540×960 design space; captions ≤ 2 lines (~30 chars), 1–2 `{key}` words.

## Kit cheat-sheet
- **Scene** `({t0, dur}) => <Stage dur={dur} bg={C.yellow}>…svg children…</Stage>`; `const {f, t, lf} = useT(t0)` → local frame, absolute seconds, `lf(sec)` local frame of an absolute second. `sp(frame)` spring, `pop(f, at)` spring from a local frame, `ramp(f, a, b)` 0→1, `breathe(f)`, `blinkAt(f)`, `shake(f, at)`.
- **Figures** (`./figures`): `<Stick x y s flip pose face shirt talk look blink seed tilt hold />` – poses `stand walk run jump sit think point shrug wave cheer facepalm explain cross dance pointup lean`, faces `neutral happy laugh surprised sad think wink angry sleepy`; `talk={mouthOpen('host', t)}`; stand on `y={GROUND}` (620). `<Walker from to s0 s1 t rest restAfter shirt … />` walks between absolute seconds. `<Crowd x y n s shirts pose face />`.
- **Backgrounds** (`./kit`): `Flat`, `Spot`, `Sky {f}`, `Space {f}`, `Room`, `Stage3`, `Ground`, `Desk`, `Board`.
- **Props** (`./props`): `Big`, `Label`, `Card`, `Counter`, `Bubble`, `Thought`, `QMark`, `Exclaim`, `Bulb`, `Check`, `Cross`, `Heart`, `Star`, `Arrow`, `Draw`, `Sun`, `Planet`, `Earth`, `Moon`, `Clock`, `Bars`, `Sign`, `Confetti`, `LikeIcon`, `FollowIcon`, `CommentIcon`, `Stamp` (`Countdown`, `Choices` exist for quiz-style scenes but are not used in the fact shape). Most take `k` (0–1 pop scale, use `pop(f, at)`).
- **Colours** `C` in `./theme`: yellow, orange, red, pink, purple, blue, teal, green, sky, cream, paper, white, ink, night, brown, outline; `PALETTE` for shirts.
- **Captions** `CAPS` `{s, e, t, who?}` with `{word}` = highlighted key word; **tags** `SCENE_TAGS` `{s, e, tag}` 1–3 words; **mouths** `SPEAK` `{host: [[s, e], …]}` combined with voice loudness from `rms.json`; **SFX** `[name, second, volume]` – tick per cut and the pad are added automatically.
- `PAGE_NAME` in `src/brand.ts` shows a small pill at the top; empty = none.

## Look
Fonts Baloo 2 (600/700/800) and Patrick Hand. Thick black outlines (`C.outline`), white inner limbs, flat fills, no gradients except background spots, no photos, no copyrighted music (procedural SFX only).

## Content rules
One hook question answered right away; facts must be true and uncontroversial; no politics, religion-shaming, medical or financial claims; no real people's likeness. The reel ends on the subscribe + follow CTA.
