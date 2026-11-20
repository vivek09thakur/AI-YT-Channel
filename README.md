# AI YouTube Channel

GitHub Actions that create finished YouTube videos from a script or from a topic. Nothing runs on your computer. Every video is saved to the `videos` branch of this repo, ready to download and post.

## What it makes

| Workflow | Output | How it starts |
|---|---|---|
| Generate story video | 2 minute folk art story, landscape and Shorts | By hand, you give the narration |
| Generate daily fact reel | 60 second vertical fact reel | By hand, you give the narration |
| NotebookLM short | 60 second vertical explainer on a random topic, optional upload to YouTube and Instagram | Daily at 09:00 IST, or by hand |
| Cleanup old videos | Removes videos older than 7 days from the videos branch | Weekly on Monday, or by hand |
| Pre-run check only | Checks keys, voice service and remaining Actions minutes without rendering | By hand |

## Get started

1. Fork or clone this repo

2. Add the secrets

   At least one LLM key is needed for story videos and fact reels. The NotebookLM token is needed for NotebookLM shorts.

   ```bash
   gh secret set GEMINI_API_KEY -R OWNER/REPO
   gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO < ~/.notebooklm/profiles/default/master_token.json
   ```

   See the Secrets section for the full list.

3. Run a workflow

   Open the Actions tab, pick a workflow, click Run workflow and fill in the form.

4. Get the video

   Open the `videos` branch. Each run has its own folder with the mp4 files, a thumbnail and a meta.json. The run summary also shows direct download links.

## Secrets

Add them under Settings, Secrets and variables, Actions, or with `gh secret set NAME -R OWNER/REPO`.

| Secret | Used by | Required | Notes |
|---|---|---|---|
| GEMINI_API_KEY | Story, Fact reel | One LLM key is required | Free tier, tried first |
| MISTRAL_API_KEY | Story, Fact reel | One LLM key is required | Free tier |
| CEREBRAS_API_KEY | Story, Fact reel | One LLM key is required | Free tier |
| META_AI_API | Story, Fact reel | One LLM key is required | Free tier |
| OPENROUTER_API_KEY | Story, Fact reel | One LLM key is required | Paid |
| OPENAI_API_KEY | Story, Fact reel | One LLM key is required | Paid |
| ANTHROPIC_API_KEY | Story, Fact reel | One LLM key is required | Paid |
| AZURE_SPEECH_KEY | Story, Fact reel | No | Better voices. Without it the free edge-tts voices are used |
| BILLING_TOKEN | Story, Fact reel, Pre-run check | No | Fine grained PAT with Plan read permission. Lets precheck stop a run when Actions minutes are low |
| NOTEBOOKLM_MASTER_TOKEN_JSON | NotebookLM short | Yes for that workflow | How to get it: `pipeline/notebooklm/README.md` |
| YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN | NotebookLM short | No | Enables YouTube upload |
| IG_USER_ID, IG_ACCESS_TOKEN | NotebookLM short | No | Enables Instagram upload |

## Variables

Add them under Settings, Secrets and variables, Actions, Variables tab, or with `gh variable set NAME -R OWNER/REPO`.

| Variable | Default | Meaning |
|---|---|---|
| ACTIONS_INCLUDED_MINUTES | 2000 | Free Actions minutes in your plan, used by precheck |
| ACTIONS_ALLOW_OVERAGE | empty | Set to 1 to keep running on paid minutes |
| AZURE_SPEECH_REGION | empty | Region of your Azure Speech resource, for example centralindia |
| IG_GRAPH_HOST | graph.facebook.com | Set to graph.instagram.com for Instagram Login tokens |

## Run a story video

Form fields when you run Generate story video:

| Field | Default | Meaning |
|---|---|---|
| topic | | Title of the story |
| script | | Narration text. Blank line or " / " starts a new paragraph |
| script_file | | Path to a .txt in the repo instead of script |
| formats | both | both, shorts or landscape. One format halves render time |
| voice | en-US-AndrewNeural | Neural voice |
| provider | auto | LLM to use. auto picks the first working key |
| model | | Model override |
| notes | | Hints for the illustrator, like characters or colours |

Generate daily fact reel has the same fields plus page_name, a small channel name shown at the top of the reel.

## Run a NotebookLM short

Runs by itself every day. By hand you can choose genre, exact topic, research depth, format, publish, keep_notebook, upload and yt_privacy. Full guide: `pipeline/notebooklm/README.md`.

## How a run works

1. precheck job: checks keys, voice service, Actions minutes. Fails fast before any render time is spent
2. generate job: voice is generated, the LLM writes the scene code, the video is rendered
3. publish job: files are pushed to the `videos` branch and the overview pages are rebuilt

Narration scripts are kept on the videos branch under `scripts/` and removed by the cleanup workflow together with their videos.

## Folders

| Folder | Content |
|---|---|
| .github/workflows | The five workflows |
| .github/skills/folk-art-video | Story video engine, Python and Pillow |
| .github/skills/daily-fact-reel | Fact reel engine, Remotion |
| pipeline | Shared scripts: precheck, tts, publish, cleanup |
| pipeline/notebooklm | NotebookLM short scripts and guide |
| .github/skills/shorts-story-video | Old HTML engine, kept for old stories, not used |

## Learn more

- Story engine: `.github/skills/folk-art-video/README.md`
- Fact reel engine: `.github/skills/daily-fact-reel/README.md`
- NotebookLM short: `pipeline/notebooklm/README.md`
