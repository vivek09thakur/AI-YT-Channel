# Daily fact reel action

Standalone GitHub Action (`.github/workflows/generate-daily-fact-reel.yml`) that turns an English fact script into a 9:16 animated reel (1080x1920, 30 fps) using the Remotion kit in `template/` (from the `bhul-bill-video-builder` skill, see `SKILL.md`).

It is fully separate from the story-video pipeline:

| | Story video | Daily fact reel |
|---|---|---|
| Workflow | `generate-video.yml` | `generate-daily-fact-reel.yml` |
| Scripts | `pipeline/*.py` | `pipeline/facts/*.py` |
| LLM contract | `pipeline/prompt/CONTRACT.md` | `pipeline/prompt/CONTRACT_FACT_REEL.md` |
| Scene code on main | `.github/skills/shorts-story-video/...` | `.github/skills/daily-fact-reel/facts/<slug>/` |
| Script copy on main | `scripts/<slug>.txt` | `scripts/facts/<slug>.txt` |
| Output on `videos` branch | `videos/`, `videos.json`, `index.html` | `facts/`, `facts.json`, `facts/index.html` |

Shared, read-only: `pipeline/tts.py`, `pipeline/check_keys.py`, `pipeline/generate_story.py` (imported for the LLM client only). `cleanup-old-videos` never touches `facts/`.

## Run it

Actions → **Generate daily fact reel** → Run workflow:

- `topic` – title of the fact (slug + overview page)
- `script` – English narration (or `script_file` = path of a `.txt` in the repo)
- `voice` – neural voice (default `en-US-AndrewNeural`)
- `page_name` – optional channel pill at the top
- `provider` / `model` / `notes` – same meaning as in the story-video action

## Pipeline

1. **author** – TTS → `narration.json`; `prepare.mjs` (fonts, sfx, pad); `make_rms.py`; LLM writes `meta.json`, `data.ts`, `scenes.tsx`; checked by `generate_fact_reel.py` (timing/caption rules, English-only, `tsc`, headless-Chrome stills, up to 3 fix rounds); scene code committed to main.
2. **render** – `npx remotion render … --gl swangle`; `finalize_reel.py` (h264, loudnorm, thumbnail, probe checks).
3. **publish** – `publish_fact_reel.py` copies to `facts/<slug>-<run>/` on the `videos` branch and rebuilds `facts.json`, `facts/index.html`, `facts/README.md`.

## Re-render locally

```bash
cd .github/skills/daily-fact-reel/template
npm ci
cp ../facts/<slug>/{data.ts,scenes.tsx,brand.ts} src/
node prepare.mjs <TOTAL>          # TOTAL = narration.json duration
cp <voice.mp3> public/voice.mp3 && python tools/make_rms.py public/voice.mp3 src/rms.json
npx remotion render src/index.ts StoryVideo out/reel.mp4 --codec h264 --crf 20
```
