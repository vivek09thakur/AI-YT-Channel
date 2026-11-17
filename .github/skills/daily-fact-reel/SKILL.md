---
name: bhul-bill-video-builder
description: Builds a 9:16 animated Bangla story video (MP4) from the user's voice MP3 and its SRT, with code-made flat vector characters, synced captions and scene tags. Use when the user sends an MP3 + SRT. It does not write stories.
---

# Bangla story video builder

Turns **a voice MP3 + its SRT** into a finished vertical video (1080×1920, 30 fps) for Facebook Reels / YouTube Shorts / Instagram, in a flat-vector story style: animated scenes with simple code-made characters, Bangla caption cards with red key words, and a big scene tag. There is no built-in ending card; the video ends with the story's last scene.

**This skill only builds videos. It never writes stories or scripts.** If the user sends only a topic or idea, reply (in Bengali) that this skill needs the voice **MP3** and the **SRT** file, and ask for them.
The user may be non-technical: reply in Bengali, short and plain. Deliver the finished file with SendUserFile (or the platform's file tool).

All code is bundled in this skill folder under `template/` (a ready Remotion project). `$SKILL` below means the directory that contains this SKILL.md (find it with `find / -name SKILL.md -path "*bhul-bill-video-builder*" 2>/dev/null | head -1`, then take its directory).

## Inputs
1. Voice MP3. 2. SRT (the exact words of the voice). The SRT is the source of truth for caption wording; never show speech-to-text output. If the SRT is missing, ask for it.
3. Optional from the user: their page/channel name (a small watermark pill at the top), preferred characters or scene ideas, an ending line. If a page name is given, set `PAGE_NAME` in `src/brand.ts`; otherwise leave it empty (no watermark).

## Procedure
0. **Check the environment:** `node -v` (≥18), `ffmpeg -version`, `python3 -c "import numpy"` (else `pip install numpy --break-system-packages`), and a Chromium for Remotion: `ls /opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell` or `which chromium chromium-browser google-chrome`; else `npx remotion browser ensure`. If no browser can run, tell the user plainly (Bengali) that this environment cannot render video and stop. `nproc` is the maximum `--concurrency`.
1. **Create the project:** `mkdir -p ~/bhulbill && cd ~/bhulbill && cp -r "$SKILL"/template/. .` then `npm install`.
2. **Fonts and sounds:** `npm i @fontsource/hind-siliguri @fontsource/noto-serif-bengali`; `mkdir -p public/fonts` and copy `hind-siliguri-bengali-600-normal.woff2`, `hind-siliguri-bengali-700-normal.woff2`, `noto-serif-bengali-bengali-800-normal.woff2` from `node_modules/@fontsource/*/files/` into `public/fonts/`. `node gen-sfx.mjs` (writes `public/sfx/*.wav`; the ambient pad is 66 s: for a video longer than 66 s raise `const dur=66` first). Copy the voice to `public/voice.mp3`. `python3 tools/make_rms.py public/voice.mp3 src/rms.json`.
3. **Timing:** `ffmpeg -i public/voice.mp3 -af silencedetect=noise=-35dB:d=0.12 -f null - 2>&1 | grep silence_`. SRT blocks split sentences in the middle, so take real boundaries from the pauses: a silence ≥ 0.4 s is a sentence/comma boundary; a caption ends at `silence_start` and the next one starts at `silence_end`. `TOTAL` = voice duration + 1.5 s (round up); the last scene must end at `TOTAL`.
4. **Plan and write the two story files** (everything else is shared and normally unchanged):
   - `src/data.ts`: `TOTAL`, `CAPS` (captions), `SPEAK` (who speaks when), `SCENE_TAGS`, `SFX`. The file in the template is an EXAMPLE from an earlier video: replace its contents completely.
   - `src/scenes.tsx`: one component per scene and the `SCENES` list. The template contains many example scenes (S0-S11); copy and adapt, do not keep unrelated ones.
   From the SRT, split the narration into scenes (a new scene at each change of place, time, speaker or idea, cutting inside voice pauses), decide the characters, and make each scene show what the sentence says. End on the story's final lesson/outcome scene and hold it ~1.5 s after the voice ends. Do not add any receipt/bill card.
5. **Verify before rendering:** `npx tsc --noEmit`; then `npx remotion still src/index.ts StoryVideo out/f_<n>.png --frame <n> --browser-executable=<browser>` for one frame in every scene and caption; tile the stills into one contact sheet (PIL) and LOOK at it. Fix overlaps (tag chip vs content, content vs caption zone, text overflow, wrong key-word colour). Never render blind.
6. **Render:** `nohup npx remotion render src/index.ts StoryVideo out/reel.mp4 --codec h264 --crf 20 --overwrite --concurrency <nproc, max 2> --browser-executable=<browser> > out/render.log 2>&1 &` then poll `tail -c 200 out/render.log` until "Encoded N/N" (~5 min per 60 s on 2 cores). Do not end your turn while it runs.
7. **Deliver:** `ffmpeg -y -i out/reel.mp4 -c:v libx264 -preset veryfast -crf 24 -pix_fmt yuv420p -movflags +faststart tmp.mp4 && ffmpeg -y -i tmp.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 160k -movflags +faststart final.mp4`. `ffprobe` must show 1080×1920, duration = TOTAL, 30 fps; look at 3-4 frames of the final file. Send `final.mp4` with one line on what is imperfect and one suggested next step.

## Writing scenes (kit cheat-sheet, all in `src/kit.tsx`)
- Design space is **540×960** (rendered ×2). `<Stage dur={dur} bg?>` wraps a scene; its children MUST be SVG elements (Stage adds the `<svg>`; forgetting this renders blank scenes). The optional page-name pill, scene tag chip, captions, vignette and grain come from `Overlay` automatically.
- Keep scene content between y≈115 and y≈720 (tag chip is at the top, captions at the bottom ≈ y 730-800).
- A scene is `({t0, dur}) => ...`; `const {f, t, lf} = useT(t0)` gives local frame `f`, absolute seconds `t`, and `lf(sec)` = local frame of an absolute second (use `sp(lf(sec))` for springs).
- **People:** `<Person x y s flip pose='sit'|'stand' {...TANVIR} blink={blinkAt(f)} mouth={mouthOpen('tanvir', t)} smile sad arm='raise' hand elbow glasses mustache lungi long />`. Presets `TANVIR, SHUVO, CHACHA, FATHER`; invent more the same way (skin, ear, shirt, pants, hair) and keep a character's look identical across videos. `<Mini x y s color flip bob />` faceless crowd figure. `<Bubble x y text delay w tail dark />` speech bubble ("?", "…", "হা হা", "!").
- **Backgrounds/props:** `RoomNight({f})`, `DeskNight`, `DeskTop`, `RoomDay`, `RoomLiving`; tea shop and street lane are in example scenes S1/S2. Draw new props as simple SVG shapes with the `#2A1A12` outline and flat colours from `C`.
- **Cards/infographics:** `Doc`, `Eye`, `Megaphone`, `StepCard`, `Relatives`; gauges, counters, month grids, fail/pass stamps are in the example scenes S4-S7 and S9-S10 — adapt them. Bengali numerals via `bn()`. Dark quote cards on `C.night`/`C.navy`.
- **Pacing:** cut on voice pauses; 8-16 cuts per 60 s; every scene has some motion (breathe, blink, spring pops); one idea per card, 1-3 s; use a dark scene for the emotional drop; show each caption's key idea visually (prop, number, icon) instead of only a talking person.
- **Mouths:** list a speaker's time windows in `SPEAK` (`{tanvir:[[s,e]], ...}`); `mouthOpen(who,t)` also checks the voice loudness from `rms.json`, so the mouth moves only when sound is present.
- **Captions:** `CAPS` entries `{s, e, t, who?}`; `{word}` = red key word, `\n` = line break (max 2 lines, ≈26 chars per line), 1-2 key words per caption, `who` adds a speaker tag for quotes.
- **Scene tags:** `SCENE_TAGS` `{s,e,tag}`: 1-3 Bengali words, shown in a large chip (27 px, red border). Never shrink it.
- **SFX:** `SFX` entries `[file, second, volume]` (files: tick, pop, stamp, printer, whoosh, pad). A soft tick on every cut and the ambient pad are added automatically. Add a stamp thud when a stamp graphic lands.

## Look and brand
Cream `#E6DDCB`, beige `#DDCFB7`, ink `#2B1D14`, accent red `#C8451E`, caption card `#F6EFE8`, night `#1C1917`, navy `#22284A`, maroon `#3B1B22`, teal `#2C483B`, receipt paper `#F6EBD9`, outline `#2A1A12`. Fonts: Hind Siliguri 600/700 (captions, tags) and Noto Serif Bengali 800 (headings, the page-name pill). Check that Bengali conjuncts (শিক্ষা, প্রস্তুত, সম্পর্ক) render correctly in the stills. Sound is procedural only (pad + SFX); no copyrighted music.

## Content rules
Build only what the SRT says. Do not add politics, hatred, shaming of real people, or medical/financial advice presented as fact; handle sensitive topics gently. Do not copy another page's characters, scenes or designs. Never promise income or reach.

## QA before sending
Caption wording equals the SRT; conjuncts correct; tag chip big and not overlapped; nothing but the chrome in the top 115 / bottom 160 px zones; the last scene ends exactly at the end of the video; 1080×1920, 30 fps; audio length = video length.

## Known gaps
Characters have limited motion (no walking or big gestures); no female character preset yet.
