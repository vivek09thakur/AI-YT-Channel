# AI YouTube Channel

GitHub Actions that make short videos by themselves. Finished files land on the `videos` branch. Nothing runs on your PC except two one-time token commands.

## What it makes

| Workflow | Output | How it runs | Needs |
|---|---|---|---|
| NotebookLM short | 60 s vertical explainer on a random topic, auto upload to YouTube and Instagram | Daily 09:00 IST, or by hand | NOTEBOOKLM_MASTER_TOKEN_JSON |
| Generate story video | 2 min folk art story, 16:9 and 9:16 | By hand | GEMINI_API_KEY |
| Generate daily fact reel | 60 s vertical fact reel | By hand | GEMINI_API_KEY |
| Pre-run check only | Tests keys, voice, remaining minutes | By hand | nothing |
| Cleanup old videos | Deletes videos older than 7 days | Weekly | nothing |

## Setup in 3 steps

1. Get the NotebookLM token (throwaway Google account, run once on your PC):

   ```bash
   pip install "notebooklm-py[headless,browser]"
   notebooklm login --master-token --account throwaway@gmail.com
   ```

   Copy the content of `~/.notebooklm/profiles/default/master_token.json`.

2. Repo > Settings > Secrets and variables > Actions > New repository secret > `NOTEBOOKLM_MASTER_TOKEN_JSON` > paste.

3. Actions tab > NotebookLM short > Run workflow. Done. It now runs daily.

Uploads are optional. Follow `pipeline/notebooklm/README.md` (screenshots included) to add Instagram or YouTube accounts.

## All secrets and variables

Add in repo > Settings > Secrets and variables > Actions.

| Name | Type | What | Needed for |
|---|---|---|---|
| NOTEBOOKLM_MASTER_TOKEN_JSON | Secret | content of master_token.json | NotebookLM short |
| IG_USER1_ID, IG_USER1_TOKEN | Secret | Instagram account 1 (2, 3 ... for more) | Instagram upload |
| YT_USER1_CLIENT_ID, YT_USER1_CLIENT_SECRET, YT_USER1_REFRESH_TOKEN | Secret | YouTube account 1 (2, 3 ... for more) | YouTube upload |
| GEMINI_API_KEY | Secret | Gemini key (or MISTRAL_API_KEY / CEREBRAS_API_KEY) | Story video, Fact reel |
| AZURE_SPEECH_KEY | Secret | Azure Speech key | Optional, better voices |
| AZURE_SPEECH_REGION | Variable | e.g. centralindia | With Azure key |
| BILLING_TOKEN | Secret | fine grained PAT, Plan: read | Optional, stops runs when minutes are low |

## Where things are

| Path | What |
|---|---|
| `.github/workflows/` | the workflows |
| `pipeline/notebooklm/` | NotebookLM short scripts, topics.json, setup guide |
| `.github/skills/folk-art-video/` | story video engine |
| `.github/skills/daily-fact-reel/` | fact reel engine |
| `videos` branch | finished videos, `nlm.json` index |

## Costs

Everything used is free: NotebookLM free tier, Meta and YouTube APIs, GitHub Actions (unlimited minutes on a public repo, 2000 per month on a private one).
