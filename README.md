# AI YouTube Channel

GitHub Actions that make YouTube videos. Output lands on the `videos` branch.

## Setup

Add these in repo Settings > Secrets and variables > Actions.

| Name | Type | Value | Needed for |
|---|---|---|---|
| GEMINI_API_KEY | Secret | Gemini API key (or MISTRAL_API_KEY / CEREBRAS_API_KEY) | Story video, Fact reel |
| NOTEBOOKLM_MASTER_TOKEN_JSON | Secret | Content of master_token.json, see below | NotebookLM short |
| AZURE_SPEECH_KEY | Secret | Azure Speech key | Optional, better voices |
| AZURE_SPEECH_REGION | Variable | e.g. centralindia | Optional, with Azure key |
| BILLING_TOKEN | Secret | Fine grained PAT, Plan: read | Optional, stops runs when minutes are low |
| YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN | Secret | See pipeline/notebooklm/README.md | Optional, YouTube upload |
| IG_USER_ID, IG_ACCESS_TOKEN | Secret | See pipeline/notebooklm/README.md | Optional, Instagram upload |
| IG_USER1_ID, IG_USER1_TOKEN, YT_USER1_... | Secret | See pipeline/notebooklm/README.md | Optional, more accounts (2, 3, ...) |

Get the NotebookLM token (throwaway Google account, run once on your PC):

```bash
pip install "notebooklm-py[headless,browser]"
notebooklm login --master-token --account throwaway@gmail.com
```

Copy the content of `~/.notebooklm/profiles/default/master_token.json` into the secret.

## Make a video

1. Actions tab > pick a workflow > Run workflow
2. Fill the form (topic + script for story / fact reel; nothing for NotebookLM short)
3. Download from the `videos` branch or the run summary

| Workflow | Makes | Runs |
|---|---|---|
| Generate story video | 2 min folk art story, 16:9 + 9:16 | By hand |
| Generate daily fact reel | 60 s vertical fact reel | By hand |
| NotebookLM short | 60 s vertical explainer, random topic, optional YT / IG upload | Daily 09:00 IST or by hand |
| Pre-run check only | Tests keys, voice, minutes | By hand |
| Cleanup old videos | Deletes videos older than 7 days | Weekly |

## More

- Story engine: `.github/skills/folk-art-video/README.md`
- Fact reel engine: `.github/skills/daily-fact-reel/README.md`
- NotebookLM short + uploads: `pipeline/notebooklm/README.md`
