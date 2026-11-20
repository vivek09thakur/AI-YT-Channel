# AI YouTube Channel Pipeline

GitHub Actions that turn a narration script into finished YouTube videos (landscape + Shorts) with neural TTS, LLM-written
scene code and a pure-Python renderer. Videos are published to the `videos` branch.

| Action | What it makes | Engine |
|---|---|---|
| **Generate story video** (`generate-video.yml`) | 2 minute mythology stories, 1920x1080 + 1080x1920 | `.github/skills/folk-art-video` (folk-art 2D, Pillow) |
| **Daily fact reel** (`generate-daily-fact-reel.yml`) | 60 s vertical fact reels | `.github/skills/daily-fact-reel` (Remotion) |
| **Cleanup old videos** (`cleanup-old-videos.yml`) | keeps only the last week of videos on the `videos` branch | - |

Story video flow: `tts.py` -> `folk/phrases.py` -> `folk/generate_folk.py` (LLM + `check_story.py` validation loop) -> commit
`stories/<slug>` -> `folk/render_folk.py` per aspect -> `publish.py`. See `.github/skills/folk-art-video/README.md`.

LLM keys (any subset; free tiers first): `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `CEREBRAS_API_KEY`, `META_AI_API`,
`OPENROUTER_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`. The only expected failure mode is every configured LLM being out of quota.

Both generate workflows start with a **precheck** job (`pipeline/precheck.py`) that fails fast, before any minutes are spent on
TTS or rendering, if: no LLM key has quota (1-token probe per provider), the TTS service is unreachable (Azure if `AZURE_SPEECH_KEY`
is set, else edge-tts), or the account does not have enough included Actions minutes left this month. The minutes check needs the
secret `BILLING_TOKEN` (fine-grained PAT, Account permissions -> Plan: read; no repository access required) and is skipped with a
warning when it is absent. Optional repo variables: `ACTIONS_INCLUDED_MINUTES` (default 2000), `ACTIONS_ALLOW_OVERAGE=1` to run on paid minutes.

The previous shadow-puppet (HTML/Chrome) kit is kept in `.github/skills/shorts-story-video/` for the old committed stories but is no longer used by the action.
