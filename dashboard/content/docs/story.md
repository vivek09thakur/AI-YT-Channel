# Story video

Pure-Python 2D animation engine (`.github/skills/folk-art-video/`) used by the **Generate story video** action. Every frame is a function of the frame number,
drawn with Pillow in a flat Indian folk-art style; an LLM writes `story.py` per narration, the pipeline validates and renders it.
Same story code renders as a 1080x1920 Short and a 1920x1080 landscape video (`FOLK_ASPECT`).

```
engine/folk2d/      draw.py (canvas, camera, aspect, fonts)  world.py (skies, set pieces, fx)  cast.py (characters, poses, props)
                    animals.py  timeline.py (phrases.json lookup)
engine/render.py    frames "0-N" --story story.py --out frames --workers N     (errors -> previous frame, never aborts)
engine/audio/       audio.py (music + sfx stems from CUES/MUSIC)  mix.py  finish_audio.py  dsp.py  instruments.py
example/            story_ramayan.py = the exemplar the LLM copies; story_karna.py = original kit example
fonts/              Poppins-Bold.ttf (OFL), used on the runner
stories/<slug>/     generated: story.py meta.json phrases.json narration.json sheet.jpg tokens.json
```

## Pipeline (`pipeline/folk/`)

0. `pick_story.py` (auto mode: no topic / script given, or the daily schedule) reads `videos.json` from the `videos` branch,
   asks the LLM for the next story - always a self-contained episode a first-time viewer can follow (no saga continuation, no
   part / episode numbers, no teaser ending), from a tradition not used by the last two stories, with a curiosity-hook title -
   and writes the 120-170 word narration (60-80 s; `work/script.txt`, `work/pick.json`). `theme` input steers it. A subject
   that repeats or nearly repeats a published title (`pipeline/dedupe.py`: same slug, or 60 % of the meaningful title words
   shared) is rejected and the LLM is asked again.
   The workflow runs the same check against the index right after the slug is known (before any TTS / render minutes are
   spent, also for a hand-given topic) and once more against a fresh index just before publishing, so a story that is
   already on the channel is never posted twice; the run fails with `already on the channel: ...` and nothing is uploaded.
1. `tts.py` narration -> `phrases.py` splits it into <= 9-word phrases with frame timings -> `work/phrases.json`
2. `generate_folk.py` sends `prompt/CONTRACT_FOLK.md` + the example + the phrase brief to the LLM, parses `story.py`/`meta.json`,
   runs `check_story.py` and feeds the problems back (3 attempts, provider fallback via `generate_story.call_with_fallback`).
3. `check_story.py`: AST whitelist (only math/random/folk2d, no files/env/subprocess), then a subprocess with API keys scrubbed
   renders ~600 sampled frames in both aspects: shots join 0..total, every shot draws a character, no exceptions, no blank
   frames, unknown outfit/pose/prop/animal/cue names, CUES/MUSIC sanity, `stories/<slug>/sheet.jpg`.
4. `render_folk.py --aspect shorts|landscape`: all frames on all cores -> stems -> mix -> `-14 LUFS` -> H.264 mp4 -> QA.
5. `captions.py` adds `description`, `hashtags`, `caption_youtube`, `caption_instagram` to `meta.json` (LLM, falls back to the story
   description). The workflow then publishes to the `videos` branch and calls `upload-video.yml` with group `story`:
   `shorts.mp4` -> YouTube Short + Instagram Reel, `landscape.mp4` -> YouTube video, the same files to every account whose
   `YT_USERn_FOR` / `IG_USERn_FOR` secret contains `story` (today: YT_USER1 IExplainHinduism, IG_USER2 Pauranik Katha;
   see [NotebookLM short, section 4](/docs/notebooklm#4-more-accounts)). The run page shows one `youtube / userN` / `instagram / userN` job per target.

Schedule: stories are due at 7:30 am and 3:30 pm IST. GitHub delays or drops cron slots on the hour / half hour, so every
slot sits on :17 / :47 and the workflow is tried every 30 minutes from 7:47 to 10:47 am and from 3:47 to 5:47 pm (the
dashboard's `/api/trigger` tries every 15 minutes in the same hours); a slot only runs while a story that is due by then is
missing (`DUE_UTC`, at most `DAILY_TARGET` = 2 a day, from `videos.json` on the `videos` branch), so the retries keep going
until the story is published, the second story is never made before its time and a third is never made.

## Local use

```powershell
$env:PYTHONPATH = ".github/skills/folk-art-video/engine"
python pipeline/tts.py --script my_script.txt --voice en-GB-RyanNeural --out work   # past scripts: videos branch, scripts/
python pipeline/folk/phrases.py --narration work/narration.json --out work/phrases.json
python pipeline/folk/check_story.py --story stories/x/story.py --phrases work/phrases.json --kit .github/skills/folk-art-video --sheet work/sheet.jpg
python pipeline/folk/render_folk.py --story .github/skills/folk-art-video/stories/x --voice work/voice.wav --aspect shorts --out out
```

Env knobs: `FOLK_ASPECT` (shorts|landscape), `FOLK_SS` (supersampling, 2 = production, 1 = quick), `FOLK_PHRASES` (path),
`FOLK_LZ` (landscape world scale, 0.7), `FOLK_STRICT=1` (frame errors fatal), `FOLK_DEVANAGARI=1` (require a Devanagari-capable font).

Speed: about 0.25 s per frame per core at `FOLK_SS=2`; a 75 s video (2250 frames) takes ~9 min on 10 cores, ~25 min on a 4-core runner.
