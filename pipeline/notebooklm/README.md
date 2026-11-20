# NotebookLM short (auto topic)

Workflow `.github/workflows/notebooklm-short.yml`. Runs daily (09:00 IST) or by hand. Picks a random topic that has not been
published yet from `topics.json` (genres: science, technology, ai, space, physics), has NotebookLM research it on the web,
generates a **Video Overview** (`short` = ~60 s vertical 9:16 by default; `explainer` / `cinematic` = 16:9) and publishes it to
the `videos` branch under `nlm/<slug>-<run>/` with `nlm.json`, `nlm/index.html` and `nlm/README.md`.

Independent of the other workflows: it does not touch `videos/`, `facts/`, `scripts/` or their indexes, and needs no LLM key or TTS.

## One-time setup

Uses [notebooklm-py](https://github.com/teng-lin/notebooklm-py) (unofficial, uses undocumented Google APIs - can break when
Google changes them). CI auth is a durable **master token**, which is a full-account credential: use a **dedicated / throwaway
Google account**, never your main one.

```bash
pip install "notebooklm-py[headless,browser]"
notebooklm login --master-token --account throwaway@gmail.com   # browser opens once; sign in with the throwaway account
# -> writes ~/.notebooklm/profiles/default/master_token.json
```

Store that file's content as the repository secret **`NOTEBOOKLM_MASTER_TOKEN_JSON`** (Settings -> Secrets -> Actions), e.g.
`gh secret set NOTEBOOKLM_MASTER_TOKEN_JSON < ~/.notebooklm/profiles/default/master_token.json`.

If a run fails with an auth error, re-run the `login --master-token` command and update the secret. To revoke: Google Account ->
Security -> Your devices -> remove the session.

## Optional: auto-upload to YouTube / Instagram

The `upload` job runs only for platforms whose secrets exist (the precheck job prints a notice for each one that is skipped);
without any of them the workflow just publishes to the videos branch as before. `upload: off` disables it for one run.
Captions (`caption_youtube.txt`, `caption_instagram.txt` = description + CTA + hashtags) are always generated and shown in the
run summary, so you can also post by hand.

**YouTube** - secrets `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (input `yt_privacy`: public / unlisted / private).
Follow the steps in the header of `yt_get_refresh_token.py` (Google Cloud project -> enable YouTube Data API v3 -> Desktop OAuth
client -> run the helper once with the channel's account). Caveats: refresh tokens from a consent screen left in "Testing" die
after 7 days (set it to "In production"); YouTube forces uploads from an **unverified** OAuth app to private until the app passes
verification; the upload quota is ~6 uploads/day on a default API project.

**Instagram** - secrets `IG_USER_ID`, `IG_ACCESS_TOKEN` (optional repo variable `IG_GRAPH_HOST=graph.instagram.com` for tokens
from "Instagram API with Instagram Login"). Needs a professional (Business / Creator) Instagram account; with Facebook Login it
must be linked to a Facebook Page, the token needs `instagram_content_publish` (+ `pages_show_list`, `instagram_basic`) and the
id comes from `GET /me/accounts?fields=instagram_business_account`. Long-lived tokens expire after 60 days - refresh and update
the secret. Instagram downloads the video from a **public URL**: the videos-branch raw link is used when the repo is public,
otherwise the file is parked for about an hour on tmpfiles.org (a third-party host - the reel is public seconds later anyway;
skip the Instagram secrets if that is not acceptable). Reels limit: 25 posts per 24 h per account.

## Files

| File | Role |
|---|---|
| `topics.json` | curated topic pool per genre (edit freely; add genres by adding keys and extending the workflow's `genre` choice list) |
| `pick_topic.py` | random unpublished topic (reads `nlm.json` from the videos branch to skip used slugs; reuses the oldest when a genre is exhausted) |
| `sweep_notebooks.py` | precheck: lists notebooks on the account and marks leftovers from crashed runs (title matches a topic in `topics.json`) for deletion |
| `make_meta.py` | builds `meta.json` (title / description / hashtags via `notebooklm ask`, CTA, source list, notebook id) + `caption_youtube.txt` / `caption_instagram.txt` |
| `publish_nlm.py` | copies `reel.mp4`, `thumb.jpg`, `meta.json` to the videos branch and rebuilds `nlm.json`, `nlm/index.html`, `nlm/README.md` |
| `upload_youtube.py` | optional: resumable upload via YouTube Data API v3 (refresh token), title + caption + tags from `meta.json` |
| `upload_instagram.py` | optional: Instagram Graph API REELS container -> poll -> publish, caption from `meta.json` |
| `yt_get_refresh_token.py` | one-time local helper to mint `YT_REFRESH_TOKEN` |

## Run flow

Job **precheck** (fails fast, ~1 min):
1. secret `NOTEBOOKLM_MASTER_TOKEN_JSON` present and a JSON object
2. install `notebooklm-py[headless]`, mint a session from the master token, `auth check --test` (token actually works)
3. `usage --json` - stop if the account's compute quota is exhausted
4. `notebooklm list` -> `sweep_notebooks.py` deletes leftover notebooks from crashed / cancelled runs (skipped with `keep_notebook`)
5. detect upload targets from secrets -> outputs `yt` / `ig`; credentials wiped

Job **make**:
1. re-mint a session (sessions are per job), `pick_topic.py` -> topic / slug
2. `notebooklm create --use` -> `source add-research "<topic>" --mode fast|deep --import-all`
3. `notebooklm generate video --format short --wait` - the prompt enforces a three-part script: (1) hook = open with a
   question to the viewer, (2) clear step-by-step explanation in simple language, (3) one-line takeaway + the closing call to
   action from `CTA_LINE` in the workflow `env` ("support us by subscribing ... and following us"). Edit `CTA_LINE` to change the wording.
4. `download video`, ffmpeg thumbnail, `ask` for title (phrased as a question) / description (ends with "Subscribe and follow us for more.") / hashtags
   -> `meta.json` + `caption_youtube.txt` + `caption_instagram.txt`
5. notebook is deleted (`if: always()`, so also after a failed step; skipped with `keep_notebook`), credentials removed from the runner

Job **publish**: videos branch `nlm/<slug>-<run>/` + indexes.
Job **upload** (only when precheck found YouTube and/or Instagram secrets): YouTube Short and/or Instagram Reel with the captions; links in the run summary.

Typical runner time: 10-25 min (NotebookLM generation dominates; research `deep` adds several minutes). Each run spends NotebookLM
compute quota on the throwaway account (research + one video + one chat question).
