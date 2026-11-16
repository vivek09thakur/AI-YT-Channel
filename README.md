# AI-YT-Channel

Turns a topic + narration script into two finished story videos (YouTube 16:9 and Shorts 9:16) with Indian English voice-over, rendered entirely inside a GitHub Action. Visual style: flat 2D mid-century Indian mythology poster (see `.github/skills/shorts-story-video/`).

## How to generate a video

1. Add repository secrets (Settings → Secrets and variables → Actions):
   - an LLM key for the provider you pick. **Free options:** `GEMINI_API_KEY` (default; [aistudio.google.com/apikey](https://aistudio.google.com/apikey), Gemini 2.5 Flash free tier), `MISTRAL_API_KEY` ([console.mistral.ai](https://console.mistral.ai), free experiment tier), `CEREBRAS_API_KEY` ([cloud.cerebras.ai](https://cloud.cerebras.ai), free tier). Paid: `OPENROUTER_API_KEY` (any model, `:free` variants are free but rate‑limited), `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`.
   - optional `AZURE_SPEECH_KEY` + variable `AZURE_SPEECH_REGION` for Azure neural voices; without them the free `edge-tts` engine is used (same `en-IN` voices)
2. Actions → **Generate story video** → *Run workflow*:
   - `topic` – short title/theme, e.g. `Shiva drinks the Halahala poison`
   - `script` – the narration. One sentence per caption; separate paragraphs with a blank line, ` / ` or `|` (the web form is single-line, so ` / ` is handy there). Or set `script_file` to a path in the repo, e.g. `scripts/ramayan.txt`.
   - `voice` – `en-IN-PrabhatNeural` (male, default), `en-IN-NeerjaNeural`, `en-IN-NeerjaExpressiveNeural`
   - `provider` / `model` – `auto` (default: probes every configured key and uses the first working one, free tiers first), or force `gemini` (`gemini-3.8-flash`, free), `mistral` (`mistral-large-latest`, free), `cerebras` (`qwen-3-coder-480b`, free), `meta` (Llama API, secret `META_AI_API`), `openrouter`, `openai`, `anthropic`. The run summary shows a table of every key: valid / quota exhausted / invalid, and the OpenRouter balance (the only provider that exposes credits via API).
   - `notes` – optional art direction hints for the scene writer
3. Wait ~25–35 min. The run summary shows download links. Outputs land in three places:
   - workflow artifacts `video-landscape` / `video-shorts` (30 days)
   - branch **`videos`**: `videos/<slug>-<run>/{landscape.mp4, shorts.mp4, voice.mp3, thumb.jpg}` plus `index.html` (overview page with two download buttons per video) and a `README.md` table. Enable GitHub Pages on the `videos` branch to browse it.
   - the generated story code is committed back to `main` under `.github/skills/shorts-story-video/shadow-puppet-kit/stories/<slug>/` together with `scripts/<slug>.txt`, so the video can be re-rendered or hand-tuned later.

CLI equivalent:

```sh
gh workflow run generate-video.yml -f topic="Ramayan trailer" -f script_file=scripts/ramayan.txt -f voice=en-IN-PrabhatNeural
```

## Pipeline

| Step | Tool | What it does |
|---|---|---|
| `pipeline/check_keys.py` | – | Probes every configured LLM key (~10 tokens each), reports status/credits, picks the provider |
| `pipeline/tts.py` | edge-tts / Azure | Speaks each line, inserts cinematic pauses, writes `voice.wav`, `voice.mp3`, `narration.json` (per-line timestamps) |
| `pipeline/generate_story.py` | OpenAI / Anthropic | Writes `story.js` + `sound_score.js` for the kit following `pipeline/prompt/CONTRACT.md`, then builds and test-renders frames; feeds errors back to the model (up to 3 attempts) |
| `shadow-puppet-kit/render.mjs` | headless Chrome + ffmpeg | Renders 16:9 and 9:16 video-only MP4s and the effects track |
| `pipeline/mux.py` | ffmpeg | Mixes voice over effects, encodes AAC, grabs a thumbnail |
| `pipeline/publish.py` | – | Updates the `videos` branch overview |

Any story works, not only Ramayan: the model writes new scenes on top of the shared drawing helpers (`stories/_shared/`) using `stories/ramayan/` as the style reference. Token use per run is roughly 25–30k input + 10–15k output, up to ~90k if a fix attempt is needed.

## Notes

- Each video adds ~80 MB to the `videos` branch; prune old folders occasionally.
- Generated scenes are LLM-authored. If a video looks off, re-run with hints in `notes`, or edit the committed `stories/<slug>/story.js` and re-run the render jobs.
- `edge-tts` uses an unofficial endpoint; set the Azure secret for a supported path.

## Local run

```sh
pip install -r pipeline/requirements.txt
cd .github/skills/shorts-story-video/shadow-puppet-kit && npm ci && cd -
python pipeline/tts.py --script scripts/ramayan.txt --voice en-IN-PrabhatNeural --out work
OPENAI_API_KEY=... python pipeline/generate_story.py --topic "Ramayan" --narration work/narration.json \
  --kit .github/skills/shorts-story-video/shadow-puppet-kit --slug ramayan2 --provider openai
```
