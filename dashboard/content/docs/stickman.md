# Stickman fact reel

Autonomous GitHub Action (`.github/workflows/generate-stickman-reel.yml`) that produces a 30-45 s vertical "did you know" fact reel (1080x1920, 30 fps) twice a day with no human input: the LLM picks a surprising fact, writes the narration, the scene code is generated against the Remotion stickman kit in `template/`, checked, rendered, published to the `videos` branch and uploaded to every account tagged for group **`stickman`**.

Look: black-outline stick figures with coloured shirts and guaranteed motion, flat colourful backgrounds, simple props (planets, clocks, bars, cards, stamps), caption card at the bottom, subscribe/follow CTA at the end. Voice `en-GB-RyanNeural`.

It is fully separate from the story and NotebookLM pipelines:

| | Story video | Stickman fact reel |
|---|---|---|
| Workflow | `generate-video.yml` | `generate-stickman-reel.yml` |
| Scripts | `pipeline/folk/*.py` | `pipeline/stick/*.py` |
| LLM contract | `pipeline/prompt/CONTRACT.md` | `pipeline/prompt/CONTRACT_STICKMAN.md` |
| Scene code on main | `.github/skills/shorts-story-video/...` | `.github/skills/stickman-reel/facts/<slug>/` |
| Narration script (on `videos` branch) | `scripts/<slug>-<run>.txt` | `scripts/stickman/<slug>-<run>.txt` |
| Output on `videos` branch | `videos/`, `videos.json`, `index.html` | `stickman/`, `stickman.json`, `stickman/index.html` |
| Upload group | `myth` | `stickman` |

Shared, read-only: `pipeline/tts.py` (with `[pause N]` support), `pipeline/check_keys.py`, `pipeline/precheck.py`, `pipeline/published_today.py`, `pipeline/folk/captions.py` (with `--base-tags`), the LLM client from `pipeline/generate_story.py`.

## Schedule and guard

Crons every 30 minutes on :27 / :57 from 8:27 to 10:57 am and from 4:27 to 5:57 pm IST (GitHub delays or drops slots on the hour / half hour; the dashboard's `/api/trigger` tries every 15 minutes in the same hours). Each slot first runs `published_today.py --index stickman.json --max 2 --due "02:30 10:30"`: it does work only while a reel that is due by then (8:00 am / 4:00 pm IST) is missing, so the workflow keeps trying every half hour until the reel is published, the second reel is never made early and the day never exceeds two reels. Failures open/comment one issue via `report-failure.yml`.

## Run it by hand

Actions → **Generate stickman fact reel** → Run workflow. Every input is optional:

- `topic` / `script` / `script_file` – give your own fact; leave empty and `pick_fact.py` chooses one not published before
- `theme` – steer the automatic pick ("space", "Indian history")
- `voice`, `page_name`, `provider`, `model`, `notes`, `upload` (`auto` / `off`), `yt_privacy`, `cta`

Script format: paragraphs separated by blank lines: hook question ending with "?", the answer, 2-4 explanation lines, a last line asking to subscribe and follow; 70-120 words.

## Pipeline

1. **guard** – daily target check on `stickman.json`.
2. **precheck** – at least one upload account for group `stickman` (YouTube or Instagram; when both are missing the run cancels itself, grey Cancelled with the reason in the run summary; skipped for `upload=off`), keys and tool checks (out of Actions minutes = same cancel).
3. **author** – `pick_fact.py` (auto mode) → `tts.py` (narration.json) → `prepare.mjs` (fonts, sfx, pad) → `make_rms.py` → LLM writes `meta.json`, `data.ts`, `scenes.tsx` → `generate_stick_reel.py` checks: scenes tile the narration and cut on line boundaries, at least one `<Stick>` per scene, allowed imports and SFX names, `tsc`, headless-Chrome stills, flat-frame and **motion** check (two stills per scene must differ), up to 3 fix rounds. Scene code is committed to main under `facts/<slug>/`.
4. **render** – `npx remotion render … --gl swangle`; `finalize_reel.py` (h264, loudnorm, thumbnail, probe checks).
5. **publish** – `publish_reel.py` copies to `stickman/<slug>-<run>/` on the `videos` branch and rebuilds `stickman.json`, `stickman/index.html`, `stickman/README.md`; `captions.py --base-tags` writes the title/description/tags.
6. **upload** – `upload-video.yml` with group `stickman` (accounts whose `YT_USERn_FOR` / `IG_USERn_FOR` contain `stickman`).
7. **report** – success closes the failure issue, failure comments on it.

## Check or re-render locally

```bash
cd .github/skills/stickman-reel/template
npm ci
cp ../facts/<slug>/{data.ts,scenes.tsx,brand.ts} src/
node prepare.mjs <TOTAL>          # TOTAL = narration.json duration
cp <voice.mp3> public/voice.mp3 && python tools/make_rms.py public/voice.mp3 src/rms.json
npx tsc --noEmit
# run every check without an LLM:
python ../../../../pipeline/stick/generate_stick_reel.py --check-only --topic "<q>" --narration <narration.json> --project . --kit .. --slug <slug>
npx remotion render src/index.ts StoryVideo out/reel.mp4 --codec h264 --crf 20
```

On Windows set `BROWSER` to the Chrome executable before `--check-only` and add `--browser-executable` to the render command.
