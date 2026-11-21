# AI YouTube Channel

GitHub Actions that make short videos by themselves. Finished files land on the `videos` branch. Nothing runs on your PC except two one-time token commands.

## What it makes

| Workflow | Output | How it runs | Needs |
|---|---|---|---|
| NotebookLM short | 60 s vertical explainer on a random topic, auto upload to YouTube and Instagram | Daily 09:00 IST (+ retry slot 15:30 IST if nothing was published), or by hand | NOTEBOOKLM_MASTER_TOKEN_JSON |
| Upload video | Uploads an already made video from the `videos` branch to every account of a group (no NotebookLM quota) | By hand, or called by the two workflows above/below | IG_USERn_* / YT_* |
| Generate story video | 2 min folk art story picked from what was published before (continues a saga or switches tradition), script, 16:9 and 9:16, captions, auto upload (shorts to YouTube + Instagram, landscape to YouTube) | Daily 11:00 IST (+ retry slot 17:00 IST), or by hand (own topic/script optional) | GEMINI_API_KEY |
| Generate stickman fact reel | 35 s vertical "did you know" fact with animated stick figures, hook question + answer + why, auto upload | Daily 13:00 and 19:00 IST (+ retry slot 22:00 IST), 2 a day, or by hand (own fact/script optional) | GEMINI_API_KEY |
| Pre-run check only | Tests keys, voice, remaining minutes | By hand | nothing |
| Report failure | Opens / updates one `pipeline-failure` issue when a daily run fails, closes it on the next success | Called by the daily workflows | nothing |
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

## Which account gets which video

Every workflow uploads with a **group** name. An account joins a group through its `*_FOR` secret; an account without `_FOR` joins all groups. One run makes one video and the same file goes to every account in the group.

| Workflow | Group | File(s) | Goes to |
|---|---|---|---|
| NotebookLM short | `nlm` | `reel.mp4` | every YT / IG account with `_FOR` = `nlm` |
| Generate story video | `story` | `shorts.mp4` (YT Short + IG Reel), `landscape.mp4` (YT video) | every YT / IG account with `_FOR` = `story` |
| Generate stickman fact reel | `stickman` | `reel.mp4` | every YT / IG account with `_FOR` = `stickman` |

Current mapping (secret -> value):

```
YT_USER1_FOR = story      # IExplainHinduism (YouTube)
YT_USER2_FOR = nlm        # crocodile.explains (YouTube)
YT_USER3_FOR = stickman   # third channel (planned)
IG_USER1_FOR = nlm        # crocodile.explains (Instagram)
IG_USER2_FOR = story      # Pauranik Katha (Instagram, planned)
IG_USER3_FOR = stickman   # facts channel (Instagram, planned)
```

Several groups: `nlm,story`. To check what a run will do, open the run > **Upload video / targets** job: the log lists each account as `youtube/user1 (IExplainHinduism)` or `instagram/user2: not for group nlm`. The name in brackets comes from the optional `YT_USERn_NAME` / `IG_USERn_NAME` secret; set it to the channel / page name so you can tell accounts apart in the logs and run summary (otherwise you only see `user1`, `user2`).

Manual upload (Actions > Upload video > Run workflow): **Accounts to use** is the group above; `all` posts to every account. **Where to upload** picks the platform(s). So "stickman + youtube" = only the YouTube channel whose `YT_USERn_FOR` is `stickman`.

## All secrets and variables

Add in repo > Settings > Secrets and variables > Actions.

| Name | Type | What | Needed for |
|---|---|---|---|
| NOTEBOOKLM_MASTER_TOKEN_JSON | Secret | content of master_token.json | NotebookLM short |
| IG_USER1_ID, IG_USER1_TOKEN | Secret | Instagram account 1 (2, 3 ... for more) | Instagram upload |
| YT_CLIENT_ID, YT_CLIENT_SECRET | Secret | Google Cloud OAuth client (one for all channels) | YouTube upload |
| YT_USER1_REFRESH_TOKEN | Secret | YouTube channel 1 (2, 3 ... for more) | YouTube upload |
| IG_USERn_FOR, YT_USERn_FOR | Secret | optional: `nlm`, `story`, `stickman` or a comma list = which workflow may post to that account (unset = all) | One channel per workflow, see above |
| IG_USERn_NAME, YT_USERn_NAME | Secret | optional: display name (e.g. `crocodile.explains`) shown in logs and the run summary instead of `usern` | Telling accounts apart |
| GEMINI_API_KEY | Secret | Gemini key (or MISTRAL_API_KEY / CEREBRAS_API_KEY) | Story video, Stickman fact reel |
| AZURE_SPEECH_KEY | Secret | Azure Speech key | Optional, better voices |
| AZURE_SPEECH_REGION | Variable | e.g. centralindia | With Azure key |
| BILLING_TOKEN | Secret | fine grained PAT, Plan: read | Optional, stops runs when minutes are low |

## Where things are

| Path | What |
|---|---|
| `.github/workflows/` | the workflows |
| `pipeline/notebooklm/` | NotebookLM short scripts, topics.json, setup guide |
| `.github/skills/folk-art-video/` | story video engine |
| `.github/skills/stickman-reel/` | stickman fact reel engine (`pipeline/stick/` scripts) |
| `videos` branch | finished videos, `nlm.json` + `videos.json` + `stickman.json` indexes (also drive the 2-a-day guard) |

## Costs

Everything used is free: NotebookLM free tier, Meta and YouTube APIs, GitHub Actions (unlimited minutes on a public repo, 2000 per month on a private one).
