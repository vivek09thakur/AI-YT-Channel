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

Everything runs in GitHub Actions. On your computer you only need the GitHub CLI to add secrets and start runs. Replace OWNER/REPO with the path of this repo as shown in the browser address bar.

1. Install and log in to the GitHub CLI

   ```bash
   winget install GitHub.cli
   gh auth login
   gh repo view OWNER/REPO
   ```

2. Add at least one LLM key (needed for story videos and fact reels, free tiers first)

   ```bash
   gh secret set GEMINI_API_KEY -R OWNER/REPO
   gh secret set MISTRAL_API_KEY -R OWNER/REPO
   gh secret set CEREBRAS_API_KEY -R OWNER/REPO
   ```

   Each command asks you to paste the value.

3. Optional: better voices and a minutes guard

   ```bash
   gh secret set AZURE_SPEECH_KEY -R OWNER/REPO
   gh variable set AZURE_SPEECH_REGION -R OWNER/REPO --body centralindia
   gh secret set BILLING_TOKEN -R OWNER/REPO
   gh variable set ACTIONS_INCLUDED_MINUTES -R OWNER/REPO --body 2000
   ```

4. NotebookLM short (needed only for that workflow)

   Use a throwaway Google account. A browser opens once.

   ```bash
   pip install "notebooklm-py[headless,browser]"
   notebooklm login --master-token --account throwaway@gmail.com
   gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO < ~/.notebooklm/profiles/default/master_token.json
   ```

   On Windows PowerShell the last line is

   ```powershell
   Get-Content "$env:USERPROFILE\.notebooklm\profiles\default\master_token.json" -Raw | gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO
   ```

5. Optional: auto upload of NotebookLM shorts

   Setup steps for the Google and Meta side are in `pipeline/notebooklm/README.md`. Then:

   ```bash
   gh secret set YT_CLIENT_ID -R OWNER/REPO
   gh secret set YT_CLIENT_SECRET -R OWNER/REPO
   gh secret set YT_REFRESH_TOKEN -R OWNER/REPO
   gh secret set IG_USER_ID -R OWNER/REPO
   gh secret set IG_ACCESS_TOKEN -R OWNER/REPO
   ```

6. Check the setup

   ```bash
   gh secret list -R OWNER/REPO
   gh variable list -R OWNER/REPO
   gh workflow run "Pre-run check only" -R OWNER/REPO
   gh run watch -R OWNER/REPO
   ```

7. Start a run

   From the Actions tab, or from the terminal

   ```bash
   gh workflow run "Generate story video" -R OWNER/REPO -f topic="Shiva drinks the poison" -f script_file=my_script.txt
   gh workflow run "Generate daily fact reel" -R OWNER/REPO -f topic="Why the sky is blue" -f script="Sentence one. Sentence two."
   gh workflow run "NotebookLM short (auto topic)" -R OWNER/REPO
   gh run list -R OWNER/REPO --limit 5
   ```

8. Get the video

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
