# NotebookLM short

Daily auto video: random topic > web research > 60 s vertical video (question hook, explanation, subscribe and follow us) > `videos` branch > optional upload.

## Setup

1. Make a throwaway Google account
2. On your PC:

   ```bash
   pip install "notebooklm-py[headless,browser]"
   notebooklm login --master-token --account throwaway@gmail.com
   ```

3. Copy the content of `~/.notebooklm/profiles/default/master_token.json`
4. Repo Settings > Secrets and variables > Actions > New repository secret > name NOTEBOOKLM_MASTER_TOKEN_JSON, paste
5. Actions tab > NotebookLM short > Run workflow

## YouTube upload (optional)

1. console.cloud.google.com > new project > enable YouTube Data API v3
2. OAuth consent screen > External > add channel account as test user > set In production
3. Credentials > OAuth client ID > Desktop app > copy id and secret
4. Download `yt_get_refresh_token.py`, run:

   ```bash
   pip install google-auth-oauthlib
   python yt_get_refresh_token.py --client-id ID --client-secret SECRET
   ```

5. Add secrets YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Unverified app = videos stay private. Request verification to post public.

## Instagram upload (optional)

Needs a Business or Creator account linked to a Facebook Page.

1. developers.facebook.com > new app > add Instagram product
2. Graph API Explorer > token with instagram_basic, instagram_content_publish, pages_show_list
3. Call `me/accounts?fields=instagram_business_account` > copy the id
4. Access Token Tool > exchange for long lived token (60 days)
5. Add secrets IG_USER_ID, IG_ACCESS_TOKEN

Private repo: video is parked 1 h on tmpfiles.org so Instagram can fetch it.

## Options

| Input | Default | Values |
|---|---|---|
| genre | auto | science, technology, ai, space, physics |
| topic | empty | exact topic |
| research_mode | fast | fast, deep |
| format | short | short, explainer, cinematic |
| style | auto | explainer only |
| publish | true | |
| keep_notebook | false | |
| upload | auto | auto, off |
| yt_privacy | public | public, unlisted, private |
| trim_outro | true | cuts the NotebookLM end card (auto-detect, else last 3 s) |

Closing line: edit `CTA_LINE` in `.github/workflows/notebooklm-short.yml`.
Topics: edit `topics.json`.

## Errors

| Log says | Do |
|---|---|
| secret not set | Setup step 4 |
| auth failed | Setup step 2 to 4 |
| quota exhausted | Wait for reset time in log |
| YouTube video private | App not verified |
