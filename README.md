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

Everything runs in GitHub Actions. There is nothing to install or clone. You only add a few secrets in the repo settings and start a workflow.

Where to add things: open the repo on GitHub, go to Settings, then Secrets and variables, then Actions. Secrets go under the Secrets tab with New repository secret. Variables go under the Variables tab with New repository variable.

1. Add one LLM key

   Needed for story videos and fact reels. Add any one of these as a secret, free tiers first: GEMINI_API_KEY, MISTRAL_API_KEY, CEREBRAS_API_KEY. The value is the API key from that provider.

2. Optional: better voices

   Secret AZURE_SPEECH_KEY with your Azure Speech key, and variable AZURE_SPEECH_REGION with the region, for example centralindia. Without them the free edge-tts voices are used.

3. Optional: minutes guard

   Secret BILLING_TOKEN with a fine grained personal access token that has Plan read permission. Precheck then stops a run when your Actions minutes are almost used up. Variable ACTIONS_INCLUDED_MINUTES with your plan minutes, default 2000.

4. NotebookLM short

   Needed only for that workflow. Use a throwaway Google account. On your computer run once

   ```bash
   pip install "notebooklm-py[headless,browser]"
   notebooklm login --master-token --account throwaway@gmail.com
   ```

   A browser opens, sign in with the throwaway account. Then open the file `.notebooklm/profiles/default/master_token.json` in your home folder, copy its whole content and add it as secret NOTEBOOKLM_MASTER_TOKEN_JSON.

5. Optional: auto upload of NotebookLM shorts

   Secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN for YouTube and IG_USER_ID, IG_ACCESS_TOKEN for Instagram. How to get the values is in `pipeline/notebooklm/README.md`. If a platform has no secrets its upload is skipped.

6. Check the setup

   Actions tab, choose Pre-run check only, click Run workflow. It reports which keys work, if the voice service is reachable and how many minutes are left.

7. Start a run

   Actions tab, choose a workflow, click Run workflow, fill in the form. NotebookLM short also runs by itself every day at 09:00 IST.

8. Get the video

   Open the `videos` branch. Each run has its own folder with the mp4 files, a thumbnail and a meta.json. The run summary of the workflow also shows direct download links.
## Secrets

Add them under Settings, Secrets and variables, Actions, Secrets tab.

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

Add them under Settings, Secrets and variables, Actions, Variables tab.

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
