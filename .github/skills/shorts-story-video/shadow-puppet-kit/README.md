# Shadow Puppet Theatre kit (S9 · Grow With AST)

Black lace-cut puppets on rods behind a lamp-lit cloth screen, drawn in code in the browser.
Voice-over only, every sound synthesized (no audio files in this kit).

Made by Grow With AST (@ast_bts). Code: MIT. Free to use, change and share.

## Folder layout it expects
The scripts read and write next to a video folder, so put the kit here:

```
my_video/
  05_Audio/voice_polished.mp3   <- your voice-over (optional, baked into the player)
  06_Edit/shadow_puppet/        <- this kit
  07_Export/                    <- renders land here
```

If `07_Export/` does not exist next to the kit, renders go to `./out/` inside the kit instead.

## Stories
Two example stories ship with the kit:

- `src/` — "Kauwa kabhi nahi bhoolta" (crows remember faces): the original black lace-cut shadow puppet look. Built when no story name is given.
- `stories/ramayan/` — "RAMAYAN, 2 minute cinematic trailer": the flat 2D mid-century poster look from SKILL.md section 2 (saffron sky with streak lines, striped scalloped clouds, domed pavilion temple, geometric figures, Hindu palette). 124.5 s, narration shown as on-screen lines, synthesized bed. Use it as the template for new stories in that style.

A story folder needs `ref.js` (drawing helpers), `story.js` (`DURATION`, `BEATS`, `explainerFrame(ctx,1280,720,t)`), `sound_score.js` (`scoreSound(k)`), `vertical.js` (`reelFrame(ctx,t)` on a 1080x1920 canvas); optional `storyboard_runner.js` (`PANELS`) and `meta.txt` (`title=...`).

## Make one
1. Easiest: open your coding agent in `my_video/`, paste the prompt and attach your script. It edits the files below for you.
2. By hand, copy `stories/ramayan/` to `stories/<name>/` and edit:
   - `story.js`: `LINES`/`WT` (line or word times in seconds), `SC` (scene changes), `BEATS` and the scene functions. Reuse the helpers in `ref.js`.
   - `storyboard_runner.js`: `PANELS` → `python build.py storyboard <name>` → open `<name>_storyboard.html` and check the key frames first.
   - `sound_score.js`: sound cues on the same times.
   - `vertical.js`: hook line and captions for the 9:16 reel.
3. Build: `python build.py player <name>` (16:9 page with sound) and `python build.py vertical <name>` (9:16).
4. Render (needs Node, ffmpeg and Google Chrome). Once: `npm install` inside the kit (installs `puppeteer-core`). Then:
   - Windows (PowerShell): `$env:STORY='<name>'; node render.mjs render` and `$env:VERTICAL='1'; node render.mjs render`
   - macOS/Linux: `STORY=<name> node render.mjs render` and `STORY=<name> VERTICAL=1 node render.mjs render`
   - Quick check of single frames before a full render: `node render.mjs test 3 12 22` → PNGs in `debug/`.
   Chrome is auto-detected on Windows, macOS and Linux; set `CHROME=<path>` to override, `OUT=<dir>` to change the output folder. Outputs: `<name>.mp4` / `<name>_9x16.mp4` (video + synthesized effects), plus `<name>_video_only.mp4` and `<name>_effects.wav` to mix with your own voice.
Fonts: IM Fell English and Libre Baskerville from Google Fonts (SIL Open Font License).
