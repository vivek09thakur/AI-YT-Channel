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

## Make one
1. Easiest: download the "Shadow Puppet Theatre" prompt from the website, open Claude Code in `my_video/`, paste the prompt and attach your script. Claude edits the files below for you.
2. By hand:
   - `src/story.js`: `WT` (word times in seconds from a word-level transcript), `SC` (scene changes), `BEATS` and the scene functions. Reuse the puppets already built (crow, person, masks, net, cards, medallions, counter, stamp …) and the helpers in `src/ref.js`.
   - `src/storyboard_runner.js`: `PANELS` → `python3 build.py storyboard` → open `storyboard.html` and check the key frames first.
   - `src/sound_score.js`: sound cues on the same word times.
   - `src/vertical.js`: hook line and `CAPS` captions for the 9:16 reel.
3. Build: `python3 build.py player` (16:9 page with sound) and `python3 build.py vertical` (9:16).
4. Render (needs Node, ffmpeg, Google Chrome and `puppeteer-core`): `NODE_PATH=<dir>/node_modules node render.mjs render` (16:9) and `VERTICAL=1 NODE_PATH=… node render.mjs render` (9:16). Change `executablePath` in `render.mjs` if Chrome is not in `/Applications`. Then mix your voice with `05_Audio/effects.wav` in any editor.

The example story inside is "Kauwa kabhi nahi bhoolta" (crows remember faces, University of Washington research). Replace it with your own.
Fonts: IM Fell English and Libre Baskerville from Google Fonts (SIL Open Font License).
