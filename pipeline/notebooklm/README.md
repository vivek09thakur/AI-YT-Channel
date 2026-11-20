# NotebookLM short

Workflow file: `.github/workflows/notebooklm-short.yml`

What it does, every day at 09:00 IST or when you run it by hand:

1. Picks a topic that was not published yet from `topics.json`
2. NotebookLM researches it on the web
3. NotebookLM makes a 60 second vertical video (question hook, clear explanation, subscribe and follow us at the end)
4. Video, thumbnail and captions are saved to the `videos` branch under `nlm/`
5. Optional: the video is uploaded to YouTube and Instagram

It does not touch the other workflows or their folders.

## Setup in 3 steps

Step 1. Create a new throwaway Google account. Do not use your main account.

Step 2. On your own computer, run these commands. A browser opens once. Sign in with the throwaway account.

```bash
pip install "notebooklm-py[headless,browser]"
notebooklm login --master-token --account throwaway@gmail.com
```

Step 3. Save the token file as a repository secret.

```bash
gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO < ~/.notebooklm/profiles/default/master_token.json
```

On Windows PowerShell:

```powershell
Get-Content "$env:USERPROFILE\.notebooklm\profiles\default\master_token.json" -Raw | gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO
```

Done. Run the workflow from the Actions tab once to test it.

## Secrets

| Secret | Needed | What it is | How to get it |
|---|---|---|---|
| NOTEBOOKLM_MASTER_TOKEN_JSON | Yes | Content of master_token.json | Setup step 2 and 3 above |
| YT_CLIENT_ID | Only for YouTube upload | Google OAuth client id | See YouTube upload section |
| YT_CLIENT_SECRET | Only for YouTube upload | Google OAuth client secret | See YouTube upload section |
| YT_REFRESH_TOKEN | Only for YouTube upload | Long lived token for the channel | See YouTube upload section |
| IG_USER_ID | Only for Instagram upload | Instagram professional account id | See Instagram upload section |
| IG_ACCESS_TOKEN | Only for Instagram upload | Long lived Instagram token | See Instagram upload section |

Set any secret with:

```bash
gh secret set SECRET_NAME -R OWNER/REPO
```

If a secret for a platform is missing, that upload is skipped and the run still succeeds.

## Repository variables (optional)

| Variable | Default | When to set |
|---|---|---|
| IG_GRAPH_HOST | graph.facebook.com | Set to graph.instagram.com if your token comes from Instagram Login instead of Facebook Login |

## Workflow inputs

| Input | Default | Meaning |
|---|---|---|
| genre | auto | Topic pool: auto, science, technology, ai, space, physics |
| topic | empty | Exact topic to use instead of a random one |
| research_mode | fast | fast or deep. Deep is slower and uses more quota |
| format | short | short is vertical 60 s. explainer and cinematic are 16:9 |
| style | auto | Visual style, used only with format explainer |
| publish | true | Save to the videos branch |
| keep_notebook | false | Keep the notebook in NotebookLM after the run |
| upload | auto | auto uploads to every platform that has secrets. off skips upload |
| yt_privacy | public | public, unlisted or private for the YouTube upload |

## Change the closing line

The subscribe and follow us sentence is one line in the workflow file, under `env`:

```yaml
CTA_LINE: "If you learned something new, support us by subscribing to the channel and following us for more."
```

Edit the text, commit, done. It is spoken at the end of every video and added to the captions.

## YouTube upload

Steps, all on your own computer:

| Step | Where | What to do |
|---|---|---|
| 1 | console.cloud.google.com | Create a project |
| 2 | APIs and Services, Library | Enable YouTube Data API v3 |
| 3 | APIs and Services, OAuth consent screen | Type External. Add the channel Google account as a test user. Then set Publishing status to In production |
| 4 | APIs and Services, Credentials | Create OAuth client ID, type Desktop app. Copy client id and client secret |
| 5 | Terminal | Run the helper below. Sign in with the channel account and allow upload |
| 6 | Terminal | Save the three secrets |

```bash
pip install google-auth-oauthlib
python pipeline/notebooklm/yt_get_refresh_token.py --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

gh secret set YT_CLIENT_ID -R OWNER/REPO
gh secret set YT_CLIENT_SECRET -R OWNER/REPO
gh secret set YT_REFRESH_TOKEN -R OWNER/REPO
```

Good to know:

| Topic | Fact |
|---|---|
| Private videos | YouTube sets videos from an unverified OAuth app to private. Request app verification in the consent screen to upload as public |
| Token expiry | If the consent screen stays in Testing the refresh token dies after 7 days. In production it lasts |
| Quota | About 6 uploads per day on a default API project |

## Instagram upload

Needs an Instagram professional account (Business or Creator) linked to a Facebook Page.

| Step | Where | What to do |
|---|---|---|
| 1 | developers.facebook.com | Create an app, add the Instagram product |
| 2 | Graph API Explorer | Generate a user token with permissions instagram_basic, instagram_content_publish, pages_show_list |
| 3 | Graph API Explorer | Call `me/accounts?fields=instagram_business_account` and copy the instagram_business_account id |
| 4 | Access Token Tool | Exchange for a long lived token (valid 60 days) |
| 5 | Terminal | Save the two secrets |

```bash
gh secret set IG_USER_ID -R OWNER/REPO
gh secret set IG_ACCESS_TOKEN -R OWNER/REPO
```

Good to know:

| Topic | Fact |
|---|---|
| Token expiry | Long lived tokens last 60 days. Refresh and update the secret |
| Public URL | Instagram downloads the video from a public link. If the repo is private the file is parked for about one hour on tmpfiles.org, a third party host. Skip the Instagram secrets if you do not want that |
| Limit | 25 reels per account per day |

## Files in this folder

| File | Role |
|---|---|
| topics.json | Topic list per genre. Edit freely |
| pick_topic.py | Picks a random topic that is not in nlm.json yet |
| sweep_notebooks.py | Finds leftover notebooks from crashed runs so precheck can delete them |
| make_meta.py | Writes meta.json, caption_youtube.txt and caption_instagram.txt |
| publish_nlm.py | Copies the result to the videos branch and rebuilds nlm.json, nlm/index.html, nlm/README.md |
| upload_youtube.py | Uploads the video to YouTube |
| upload_instagram.py | Publishes the video as an Instagram Reel |
| yt_get_refresh_token.py | One time helper to get YT_REFRESH_TOKEN |

## Jobs

| Job | What it does | Fails when |
|---|---|---|
| precheck | Checks the token secret exists and works, checks quota, deletes leftover notebooks, detects upload targets | Secret missing or invalid, quota exhausted |
| make | Picks topic, researches, generates video, downloads it, writes captions, deletes the notebook | NotebookLM errors |
| publish | Saves to the videos branch | Git push problems |
| upload | YouTube and or Instagram, only when their secrets exist | Platform API errors |

Typical run time: 10 to 25 minutes.

## Troubleshooting

| Problem | Fix |
|---|---|
| precheck says secret not set | Run setup step 3 again |
| precheck says auth failed | Run setup step 2 again and update the secret |
| quota exhausted | Wait for the reset time printed in the log or use a second throwaway account |
| YouTube video is private | App is not verified, see YouTube section |
| Instagram error about video URL | Public link not reachable, check the log line that says which URL was used |
