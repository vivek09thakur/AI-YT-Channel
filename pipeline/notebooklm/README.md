# NotebookLM short

Every day at 09:00 IST (or by hand) this workflow:

- picks a random unused topic from `topics.json`
- lets NotebookLM research it on the web
- makes a 60 s vertical video: question hook, clear explanation, "subscribe and follow us" line
- cuts the NotebookLM end card
- writes a title, description and hashtags
- saves everything to the `videos` branch under `nlm/`
- uploads to every YouTube and Instagram account you configured (optional)

Where to add secrets: repo > Settings > Secrets and variables > Actions > New repository secret.

---

## 1. NotebookLM token (required)

Use a throwaway Google account, not your main one.

- On your PC run:

  ```bash
  pip install "notebooklm-py[headless,browser]"
  notebooklm login --master-token --account throwaway@gmail.com
  ```

- A browser opens, log in with the throwaway account
- Print the token file as ONE line and copy the output:

  ```bash
  python -c "import json,os;print(json.dumps(json.load(open(os.path.expanduser('~/.notebooklm/profiles/default/master_token.json')))))"
  ```

- Add secret `NOTEBOOKLM_MASTER_TOKEN_JSON` and paste that single line

Why one line: GitHub masks every line of a multi-line secret. A pretty-printed JSON gives masks like `{` and `}`, and GitHub then silently drops any job output containing them, which breaks the upload job. The Precheck warns if the secret is multi-line.

Check it worked: Actions tab > NotebookLM short > Run workflow. The first job, Precheck, must be green.

---

## 2. Instagram upload (optional)

Free. Takes about 10 minutes. Everything below is on developers.facebook.com unless the step says phone.

### 2.1 Instagram account

- Phone: Instagram > Settings and activity > Account type and tools > Switch to professional account > Creator
- Personal accounts cannot use the API

### 2.2 Create the Meta app

- Go to developers.facebook.com > My Apps > Create App
- App details: any name, your email, Next
- Use cases: left filter **Content management** > tick **Manage messaging and content on Instagram** > Next

  ![Use case](docs/meta-01-use-case.jpg)

- Business: I don't want to connect a business portfolio yet > Next
- Requirements: Next > Create app

  ![Dashboard](docs/meta-02-dashboard.jpg)

### 2.3 Permissions

- Dashboard > click **Customize the Manage messaging & content on Instagram use case**
- On **Permissions and features** click Add on these two only:
  - `instagram_business_basic`
  - `instagram_business_content_publish`

  ![Permissions](docs/meta-03-permissions.jpg)

### 2.4 Add the Instagram account as tester

- Left sidebar > App roles > Roles > Add people
- Pick **Instagram Tester** (last option) > type the Instagram username > Add

  ![Add tester](docs/meta-05a-add-tester.jpg)

- Phone: Instagram > Settings and activity > Apps and websites > Tester invites > Accept

### 2.5 Business portfolio and configuration

- Use cases > Customize > **API setup with Unified login**
- It says a business portfolio is mandatory: click **+ Business portfolio** > Create new > any name > Create (free, no company needed)

  ![Business portfolio](docs/meta-04-business-portfolio.jpg)

- Section **1. Configure your app** > Create configuration > **Create from template**. The template token never expires.

  ![Config template](docs/meta-05-config-template.jpg)

### 2.6 Get ID and token

- Section **2. Generate access tokens**: the account is listed with a number under it. That number is the user ID.
- Click **Generate token** > Continue with Instagram > log in as that account > pick the portfolio > tick the account > Allow > copy the token

  ![Generate token](docs/meta-06-generate-token.jpg)

### 2.7 Add secrets

| Secret | Value |
|---|---|
| IG_USER1_ID | the number under the account |
| IG_USER1_TOKEN | the token |
| IG_USER1_NAME | optional label, shown in the upload summary (job name stays `user1`) |
| IG_USER1_FOR | optional: which workflow may post here, `nlm`, `story` or `nlm,story` (unset = all, see section 4) |

Skip sections 3 (webhooks) and 4 (App Review). Tester accounts can post without review.

Private repo note: Instagram must fetch the video from a public URL, so the file is parked 1 hour on tmpfiles.org. Public repo: the videos branch raw URL is used directly.

---

## 3. YouTube upload (optional)

- console.cloud.google.com > New project (free, no card) > APIs and services > Library > enable **YouTube Data API v3** and **YouTube Analytics API**
- OAuth consent screen > External > fill name and email > add the channel Google account as **Test user**
- Scopes > Manually add scopes > paste, one per line, then Add to table > Update:

  ```
  https://www.googleapis.com/auth/youtube.upload
  https://www.googleapis.com/auth/youtube
  https://www.googleapis.com/auth/yt-analytics.readonly
  https://www.googleapis.com/auth/yt-analytics-monetary.readonly
  ```

- Credentials > Create credentials > OAuth client ID > **Desktop app** > copy client ID and client secret
- On your PC:

  ```bash
  pip install google-auth-oauthlib
  python pipeline/notebooklm/yt_get_refresh_token.py --client-id ID --client-secret SECRET
  ```

- A browser opens, log in with the channel account, allow. The script prints the refresh token. The same token covers upload, thumbnails and YouTube Analytics (read-only).

| Secret | Value |
|---|---|
| YT_CLIENT_ID | client ID (shared by every channel, it identifies the Google Cloud app) |
| YT_CLIENT_SECRET | client secret (shared) |
| YT_USER1_REFRESH_TOKEN | printed by the script while logged in as channel 1 |
| YT_USER1_FOR | optional: which workflow may post here, `nlm`, `story` or `nlm,story` (unset = all, see section 4) |
| YT_USER1_PRIVACY | optional: public, unlisted, private |
| YT_USER1_NAME | optional label, shown in the upload summary |

Second channel: run the script again logged in as that channel, add `YT_USER2_REFRESH_TOKEN` (+ `YT_USER2_FOR`). `YT_USERn_CLIENT_ID` / `YT_USERn_CLIENT_SECRET` are only needed when a channel uses a different Google Cloud project.

Known limits:

- Unverified Google app: uploads are forced to private. Submit the app for verification to post public.
- Consent screen left in Testing: refresh token dies after 7 days. Set it to In production.
- Default quota is about 6 uploads per day.

---

## 4. More accounts

- Repeat the secrets with 2, 3, 4 ... (`IG_USER2_ID`, `IG_USER2_TOKEN`, `YT_USER2_CLIENT_ID` ...)
- Each account uploads in its own job. One bad token does not stop the others.
- Incomplete sets are skipped with a warning in the Precheck job.
- Old style single secrets `IG_USER_ID`, `IG_ACCESS_TOKEN`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` still work as account "default" (`IG_FOR` / `YT_FOR` restrict them).

### One channel per workflow

Each workflow uploads with a **group** name: NotebookLM short = `nlm`, Generate story video = `story`. An account takes every group unless its `*_FOR` secret says otherwise. Example: facts channel + Instagram page for NotebookLM, a second channel for folk-art stories:

| Secret | Value |
|---|---|
| YT_CLIENT_ID / YT_CLIENT_SECRET | the one OAuth client |
| YT_USER1_REFRESH_TOKEN | token minted while logged in as the stories channel |
| YT_USER1_FOR | `story` |
| YT_USER2_REFRESH_TOKEN | token minted while logged in as the facts channel |
| YT_USER2_FOR | `nlm` |
| IG_USER1_ID / IG_USER1_TOKEN | Instagram page |
| IG_USER1_FOR | `nlm` |

The "Detect upload accounts" job log lists which accounts were skipped for the group.

---

## 5. Run options

Actions tab > NotebookLM short > Run workflow.

| Input | Default | Values |
|---|---|---|
| genre | auto | science, technology, ai, space, physics |
| topic | empty | exact topic instead of random |
| research_mode | fast | fast, deep |
| format | short | short (9:16), explainer, cinematic (16:9) |
| style | auto | explainer only |
| publish | true | false = artifact only |
| keep_notebook | false | true = keep notebook in NotebookLM |
| upload | auto | off = skip all uploads |
| yt_privacy | public | public, unlisted, private |
| trim_outro | true | false = keep the NotebookLM end card |

Change the wording:

- Closing line: `CTA_LINE` in `.github/workflows/notebooklm-short.yml`
- End card trim fallback seconds: `OUTRO_TRIM` in the same file
- Topics: `topics.json`

---

## 6. Jobs

| Job | What it checks or does |
|---|---|
| Precheck | token present and valid, NotebookLM quota, deletes leftover notebooks |
| Make | topic, research, video, trim, thumbnail, captions |
| Publish | copies to `videos` branch, updates `nlm.json` |
| Upload | calls `upload-video.yml` with group `nlm`: detects accounts, one job per account (`instagram / user1` ...) |

### Upload an already made video (no NotebookLM quota)

If a run made and published the video but the upload failed or was skipped, do not use "Re-run all jobs" (that remakes the video and uses quota, and it runs the OLD workflow file).

- Open the `videos` branch > `nlm/README.md` and copy the folder name, e.g. `nlm/how-deepfakes-are-made-and-detected-5`
- Actions tab > **Upload video (YouTube / Instagram)** > Run workflow > paste the folder, video `reel.mp4`, group `nlm`
- One upload job per allowed account runs, nothing else

Same workflow for a story video: folder `videos/<slug>-<run>`, video `shorts.mp4` (group `story`, short) or `landscape.mp4` (platforms `youtube`, kind `video`).

---

## 7. Errors

| Log says | Do |
|---|---|
| secret NOTEBOOKLM_MASTER_TOKEN_JSON is not set | Section 1 |
| NotebookLM auth failed | Section 1 again, token expired |
| quota exhausted | wait for the reset time printed in the log |
| daily Video Overview quota reached (RateLimitError on CREATE_ARTIFACT) | the free account only gets a few videos per day; wait for the daily reset (about 13:30 IST) or use another throwaway account. The daily schedule makes one video per day, extra manual runs eat into this |
| research imported no sources | re-run, or pick another topic |
| no public URL for the video | tmpfiles.org down, re-run |
| YouTube video is private | Google app not verified |
| account incomplete - skipped | one of the numbered secrets is missing |
| Upload job shows "Waiting for pending jobs" and the run fails, or "Upload targets sanity" fails | a multi-line secret (usually NOTEBOOKLM_MASTER_TOKEN_JSON) made GitHub drop the upload matrix. Re-save it as one line (Section 1), then use the upload workflow above for that video |
| reel.mp4 not found on the videos branch | wrong folder name, copy it from `nlm/README.md` on the `videos` branch |
