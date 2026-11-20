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

## Files

| File | Role |
|---|---|
| `topics.json` | curated topic pool per genre (edit freely; add genres by adding keys and extending the workflow's `genre` choice list) |
| `pick_topic.py` | random unpublished topic (reads `nlm.json` from the videos branch to skip used slugs; reuses the oldest when a genre is exhausted) |
| `make_meta.py` | builds `meta.json` (title / description / hashtags via `notebooklm ask`, source list, notebook id) |
| `publish_nlm.py` | copies `reel.mp4`, `thumb.jpg`, `meta.json` to the videos branch and rebuilds `nlm.json`, `nlm/index.html`, `nlm/README.md` |

## Run flow

1. install `notebooklm-py[headless]`, mint a session from the master token, `auth check --test`, `usage --json` (fails fast if the account's compute quota is exhausted)
2. `pick_topic.py` -> topic / slug
3. `notebooklm create --use` -> `source add-research "<topic>" --mode fast|deep --import-all`
4. `notebooklm generate video --format short --wait` - the prompt enforces a three-part script: (1) hook = open with a
   question to the viewer, (2) clear step-by-step explanation in simple language, (3) one-line takeaway + the closing call to
   action from `CTA_LINE` in the workflow `env` ("support us by subscribing ... and following us"). Edit `CTA_LINE` to change the wording.
5. `download video`, ffmpeg thumbnail, `ask` for title (phrased as a question) / description (ends with "Subscribe and follow us for more.") / hashtags -> `meta.json`
6. notebook is deleted (unless `keep_notebook`), credentials removed from the runner
7. publish job: videos branch `nlm/<slug>-<run>/` + indexes

Typical runner time: 10-25 min (NotebookLM generation dominates; research `deep` adds several minutes). Each run spends NotebookLM
compute quota on the throwaway account (research + one video + one chat question).
