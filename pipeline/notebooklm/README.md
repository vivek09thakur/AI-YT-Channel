# Welcome to NotebookLM short 👋

This workflow makes one short video a day, fully automatic. It picks a topic, researches it on the web with NotebookLM, generates a 60 second vertical video and saves it to the `videos` branch. Optionally it uploads the video to YouTube and Instagram.

Every video follows the same structure: a question to hook the viewer, a clear explanation, and a closing line asking to subscribe and follow us.

## Get started

1. Create a throwaway Google account

   Do not use your main account.

2. Log in once on your computer

   ```bash
   pip install "notebooklm-py[headless,browser]"
   notebooklm login --master-token --account throwaway@gmail.com
   ```

   A browser opens. Sign in with the throwaway account.

3. Save the token as a repository secret

   ```bash
   gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO < ~/.notebooklm/profiles/default/master_token.json
   ```

   On Windows PowerShell

   ```powershell
   Get-Content "$env:USERPROFILE\.notebooklm\profiles\default\master_token.json" -Raw | gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON -R OWNER/REPO
   ```

4. Run the workflow

   Open the Actions tab, choose NotebookLM short, click Run workflow. It also runs by itself every day at 09:00 IST.

That is all. Videos appear under `nlm/` on the `videos` branch with a thumbnail, a meta.json and ready to paste captions.

## Secrets

| Secret | Needed for |
|---|---|
| NOTEBOOKLM_MASTER_TOKEN_JSON | Everything |
| YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN | YouTube upload |
| IG_USER_ID, IG_ACCESS_TOKEN | Instagram upload |

Upload secrets are optional. If they are missing, the upload is skipped and the run still succeeds.

## Upload to YouTube

1. Go to console.cloud.google.com and create a project
2. Enable YouTube Data API v3
3. OAuth consent screen: type External, add the channel account as a test user, set Publishing status to In production
4. Credentials: create an OAuth client ID of type Desktop app
5. Get the refresh token

   ```bash
   pip install google-auth-oauthlib
   python pipeline/notebooklm/yt_get_refresh_token.py --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
   ```

6. Save the secrets

   ```bash
   gh secret set YT_CLIENT_ID -R OWNER/REPO
   gh secret set YT_CLIENT_SECRET -R OWNER/REPO
   gh secret set YT_REFRESH_TOKEN -R OWNER/REPO
   ```

Note: YouTube keeps videos from an unverified app private. Request verification in the consent screen to upload as public.

## Upload to Instagram

You need a professional Instagram account (Business or Creator) linked to a Facebook Page.

1. Go to developers.facebook.com, create an app and add the Instagram product
2. In Graph API Explorer generate a token with instagram_basic, instagram_content_publish and pages_show_list
3. Call `me/accounts?fields=instagram_business_account` and copy the id
4. Exchange the token for a long lived token in the Access Token Tool
5. Save the secrets

   ```bash
   gh secret set IG_USER_ID -R OWNER/REPO
   gh secret set IG_ACCESS_TOKEN -R OWNER/REPO
   ```

Note: long lived tokens last 60 days, then update the secret. Instagram needs a public link to the video. If the repo is private the file is parked for one hour on tmpfiles.org. Skip these secrets if you do not want that.

## Options when you run it by hand

| Input | Default | Meaning |
|---|---|---|
| genre | auto | science, technology, ai, space or physics |
| topic | empty | Use this exact topic instead of a random one |
| research_mode | fast | fast or deep |
| format | short | short, explainer or cinematic |
| style | auto | Visual style, explainer only |
| publish | true | Save to the videos branch |
| keep_notebook | false | Keep the notebook in NotebookLM |
| upload | auto | auto or off |
| yt_privacy | public | public, unlisted or private |

## Change the closing line

Open `.github/workflows/notebooklm-short.yml` and edit this line under `env`

```yaml
CTA_LINE: "If you learned something new, support us by subscribing to the channel and following us for more."
```

## Add topics

Edit `topics.json`. Each genre is a list of topics. Topics already published are skipped automatically.

## If something fails

- Secret not set: repeat step 3 of Get started
- Auth failed: repeat step 2 and 3 of Get started
- Quota exhausted: wait for the reset time shown in the log, or use a second throwaway account
- YouTube video is private: the app is not verified, see Upload to YouTube
- Instagram video URL error: check the log line that shows which URL was used

## Learn more

- notebooklm-py on GitHub: https://github.com/teng-lin/notebooklm-py
- YouTube Data API: https://developers.google.com/youtube/v3
- Instagram content publishing: https://developers.facebook.com/docs/instagram-platform/content-publishing
