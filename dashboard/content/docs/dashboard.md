# Dashboard

A small read-only web app that shows the pipeline as a board: the three workflows on the left and the YouTube and Instagram accounts they post to on the right, plus a Runs page with today's videos and recent runs, and a Secrets page that lists which repo secrets exist. Nothing can be changed from here; secrets, variables and runs are managed on GitHub. The one thing it does besides reading is the `/api/trigger` endpoint, which starts the day's workflows when an outside scheduler asks it to (see [External trigger](#external-trigger)).

The app is the `dashboard/` folder of the pipeline repo on `main`. It runs on Vercel (or locally) and talks to GitHub with a fine-grained personal access token. Nothing is stored in the app itself: secrets live in the repo's Actions secrets, display names and workflow groups live in one repo variable (`DASHBOARD_ACCOUNTS`), and "posted today" comes from the `videos` branch indexes plus the Actions run history.

## What you see

| Page | Meaning |
| --- | --- |
| Board | Workflow tiles on the left (title, posted-today count, next event), account tiles on the right with a green dot when every required secret is set and a red dot when one is missing. A line from a workflow to an account means that workflow posts there; a dashed grey line means the link has not been recorded yet. Click a tile for details. |
| Runs | Today's publishing windows drawn across the day, one row per workflow: green when the video posted (the dot is the run that did it), red when every attempt failed, blue while a run is going, outlined when the window is still ahead, dashed when it passed with no run. Below it a summary of the day (runs so far, next run, accounts ready, videos in the last 7 days), a "Needs a look" list when something is off, then one card per workflow. Each card is a log of today's videos, time first: the title (linking to the file) and where it went, with any failed upload named in red and linked to the job. If nothing posted yet the card says what happens next. The footer has a 7-day posting history and a one-line summary of recent runs (how many succeeded, how many failed, the typical length); open it to see the last six runs with their duration and a link to the log. It is already open when the workflow failed today. |
| Docs | These pages, rendered from `content/docs/*.md`. Open to anyone with the link, no sign-in; the Board, Runs and Secrets pages still need one. |
| Secrets | A sidebar lists the shared secrets by purpose, then one entry per account (red dot = a required secret is missing), then anything else in the repo. Pick one to see its secrets and variables, whether each is set and when it was last updated. Values are never shown; GitHub does not return them. The link to the repo's GitHub settings sits at the foot of the sidebar. |

The menu in the top right switches pages and signs out; the sun or moon button next to it switches between light and dark mode (the choice is kept in the browser, and until you pick one the system setting is followed). Pages refresh themselves every minute.

## Environment variables

Copy `.env.example` to `.env.local` for local use, or set the same names in the Vercel project.

| Name | Required | What it is |
| --- | --- | --- |
| `GITHUB_REPO` | yes | `owner/name` of the repo that holds the workflows, e.g. `vivek09thakur/AI-YT-Channel`. |
| `GITHUB_TOKEN` | yes | Fine-grained personal access token, see below. |
| `AUTH_SECRET` | yes | Long random string that signs the login cookie. `openssl rand -hex 32` or `node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"`. |
| `DASHBOARD_USERS` | yes | Who can sign in, see below. |
| `CRON_SECRET` | for the trigger | Long random string (16+ characters). Vercel's scheduler sends it when it calls `/api/trigger`; the route checks it. Unset = the route answers 503 and starts nothing. |
| `TRIGGER_SECRET` | no | Second key for `/api/trigger`, for another scheduler or a browser test. Same format. |
| `VIDEOS_BRANCH` | no | Branch that holds the published indexes. Default `videos`. |
| `WORKFLOWS_BRANCH` | no | Branch the trigger starts the workflows on. Default `main`. |
| `ACCOUNTS_VARIABLE` | no | Repo variable that stores names and groups. Default `DASHBOARD_ACCOUNTS`. |

### GitHub token

GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token
(<https://github.com/settings/personal-access-tokens/new>, logged in as the repo owner).

- Repository access: only the pipeline repo.
- Repository permissions:
  - Actions: read and write (runs and jobs; write is what lets `/api/trigger` start a run. Read is enough if you do not use the trigger)
  - Secrets: read (names and update dates only)
  - Variables: read (`DASHBOARD_ACCOUNTS`)
  - Contents: read (indexes on the `videos` branch)
  - Issues: read (open `pipeline-failure` issues)
  - Metadata: read (added automatically)

### Users

`DASHBOARD_USERS` is a list of `name:password` entries separated by commas or new lines. Everyone who signs in sees the same read-only pages.

```
DASHBOARD_USERS=vivek:a-strong-password,friend:another-one
```

If a password contains `:` or `,`, use a JSON list instead:

```
DASHBOARD_USERS=[{"user":"vivek","password":"p:w,d"},{"user":"friend","password":"x"}]
```

The older `name:role:password` form still works; the role is ignored.

Sessions last 30 days and are stored in an httpOnly cookie. Removing a user from `DASHBOARD_USERS` or changing their password signs that user out on their next request; changing `AUTH_SECRET` signs everyone out.

## Run locally

Node 20 or newer.

```
cd dashboard
npm install
cp .env.example .env.local   # then fill it in
npm run dev
```

Open <http://localhost:3000>. `npm run lint` and `npm run build` must pass before committing.

## Deploy on Vercel

The app lives in `dashboard/` on `main`, next to the pipeline. `vercel.json` pins the Next.js preset and the Mumbai region (`bom1`, change if you are elsewhere) and declares the schedule that calls `/api/trigger`.

Vercel's Git integration is **not** connected to the repo. It would react to every push on every branch, and the workflows push to `main` (story and fact files) and to `videos` several times a day; each of those showed up as a failed or skipped deployment. Instead the **Deploy dashboard** workflow (`.github/workflows/deploy-dashboard.yml`) uploads this folder with the Vercel CLI and lets Vercel build it. It runs when a push to `main` changes something under `dashboard/`, or by hand from Actions → Deploy dashboard → Run workflow. The root `.vercelignore` limits the upload to `dashboard/` (minus `node_modules`, `.next`, `.env*`).

One-time setup:

1. Vercel → Add New → Project → Create without a Git repository (or import the repo once, then Settings → Git → Disconnect). Framework preset: Next.js. Root Directory: `dashboard`.
2. Settings → Environment Variables: the four required ones above (and any optional ones, plus `CRON_SECRET` for the schedule), for Production.
3. `cd dashboard && npx vercel link` on your PC, pick the project. Copy `orgId` and `projectId` from the `.vercel/project.json` it writes into the `env` block at the top of `deploy-dashboard.yml` (they are ids, not secrets).
4. Vercel → Account settings → Tokens → Create, scoped to the team that owns the project. Add it to the repo as the `VERCEL_TOKEN` secret (Settings → Secrets and variables → Actions). The workflow stops with a clear error when it is missing.
5. Actions → Deploy dashboard → Run workflow. The run's summary shows the deployment URL; Vercel points the project domain at it.

Build errors show on Vercel (the CLI prints the inspect URL in the run log), so run `npm run lint` and `npm run build` before pushing. The free Hobby plan is enough; the app makes a handful of GitHub API calls per page load (well under the 5,000/hour token limit even with the one-minute refresh).

## External trigger

GitHub's cron can stop creating scheduled runs for a repo with no error anywhere (this repo had a day with zero scheduled runs across 55 slots). `/api/trigger` makes publishing independent of it. Vercel's own scheduler calls the route every 15 minutes from 7 to 11 am and from 3 to 6 pm IST (the `schedules` entry in `vercel.json`, [Vercel Schedules](https://vercel.com/docs/schedules), free on Hobby, where a run can arrive up to 15 minutes after its slot). On each call the route reads the `videos` branch indexes and the run list, and for each workflow decides exactly what the guard job would decide for a cron slot:

- inside the workflow's hours only: from the video's due time until 11:00 am (morning video) or 6:00 pm (afternoon video); fact short is due 7:00 am / 3:00 pm, story 7:30 am / 3:30 pm, stickman 8:00 am / 4:00 pm IST (`windowsIST` in `src/lib/model.ts`);
- a run is started only while a video that is due by now is still missing (first due time, then the second; 2 a day), never when a run of that workflow is queued or in progress, and not within 25 minutes of the previous run (the cron retried every 30);
- the run is started with the `auto` input on, so the workflow's own guard job re-checks the index and still skips if a video appeared in the meantime. Started runs show as "manual" on the Runs page because GitHub records them as `workflow_dispatch`.

Request: `GET` or `POST https://<your-dashboard>/api/trigger` with header `Authorization: Bearer <CRON_SECRET or TRIGGER_SECRET>` (also accepted: header `x-trigger-key`, or `?key=`). Add `?dry=1` to see the decision without starting anything, `?workflow=nlm|story|stickman` to look at one workflow, and `?formats=shorts|landscape|both` to pick the story video's format for that call (only used when the story workflow is started; the schedule never sends it, so daily runs make shorts). The answer is JSON: `time`, `date`, `started` (list of workflow ids), and one `results` entry per workflow with `action`, `reason`, `published` and `target`. Wrong key: 401. No secret set: 503. A GitHub error: 502 with the message.

Setup:

1. Vercel → Settings → Environment Variables → add `CRON_SECRET` (any random string, 16+ characters) for Production. Make sure the `GITHUB_TOKEN` there has **Actions: read and write**.
2. Run the Deploy dashboard workflow (or Redeploy on Vercel). Vercel reads `CRON_SECRET` at build time and creates the schedule from `vercel.json`; it appears under the project's **Schedules** tab with its execution history, and can be paused or run now from there.
3. Test: open `https://<your-dashboard>/api/trigger?dry=1&key=<CRON_SECRET>` in a browser; the response says what would start and why not. Or press "Run now" on the schedule and look at the execution history.

Changing `CRON_SECRET` later needs a redeploy (Vercel sends the value the current deployment was built with). To use another scheduler as well or instead, for example [cron-job.org](https://cron-job.org) every 10 minutes 9 am to 10 pm `Asia/Kolkata`, set `TRIGGER_SECRET` and send it as `Authorization: Bearer <TRIGGER_SECRET>`; the route only starts a run when one is due, so two schedulers calling it do no harm.

Anyone with a secret can start runs (which spend Actions minutes and NotebookLM quota), nothing else.

## How accounts map to secrets

The pipeline reads numbered secrets (`YT_USER1_*`, `IG_USER1_*`, …) and the legacy single-account names (`YT_FOR`, `YT_REFRESH_TOKEN`, `IG_FOR`, `IG_USER_ID`, `IG_ACCESS_TOKEN`). The dashboard infers the account list from which secret names exist.

Because secret values cannot be read back, the display name, owner and the list of workflows (`nlm`, `story`, `stickman`) are kept in the `DASHBOARD_ACCOUNTS` repo variable as JSON, maintained by hand (GitHub → Settings → Secrets and variables → Actions → Variables, or `gh variable set DASHBOARD_ACCOUNTS`):

```json
{ "YT_USER1": { "name": "Main channel", "owner": "Vivek", "for": [], "privacy": "" },
  "IG_USER1": { "name": "Facts page", "for": ["nlm", "stickman"] } }
```

`for: []` means every workflow, matching how the pipeline treats an empty or `all` `_FOR` secret. Keep `for` in step with the account's `_FOR` secret; the workflows never read the variable. Only `upload-video.yml` (named `YT_*` / `IG_*` secrets passed to `pipeline/notebooklm/upload_accounts.py`) decides where a video goes. A key that exists only in the variable is shown as a planned account ("Planned, secrets to add") until its secrets are added. An account whose `for` is not recorded is drawn with dashed lines; once a run has posted there the dashboard uses the observed uploads instead.

Upload results come from the job names of each run (`Upload shorts / Upload youtube/user1`). The story workflow uploads `shorts.mp4` to YouTube and Instagram and, when run with `formats=landscape` or `both`, `landscape.mp4` to YouTube only, so a YouTube channel can show two chips for one story; the second is marked "landscape".

## Files

| Path | What it does |
| --- | --- |
| `src/lib/model.ts` | Workflows, platforms, account fields and the secrets catalogue (mirrors the Overview tables). |
| `src/lib/github.ts` | GitHub REST calls: secrets, variables, indexes, runs, jobs, issues, and `dispatchWorkflow` for the trigger. |
| `src/lib/state.ts` | Builds the overview: accounts from secret names, today's posts, per-account upload results, workflow state. |
| `src/lib/trigger.ts`, `src/app/api/trigger/route.ts` | External trigger: the pure "is a run due now" decision, and the route that checks the secret, reads GitHub and starts the workflow. |
| `src/lib/secrets.ts` | Groups secrets and variables into the sections shown on the Secrets page. |
| `src/lib/session.ts`, `src/lib/auth.ts`, `src/proxy.ts` | User list, password check and signed session token; the cookie helpers; redirect to `/login`. |
| `src/app/actions.ts` | Server actions: sign in and sign out. |
| `src/components/` | Board (React Flow) and tiles, account and workflow modals, Runs page, Secrets page with its sidebar, top bar with the menu, docs shell and Markdown renderer. |
| `src/lib/docs.ts`, `src/app/docs/` | The docs pages: page list, Markdown loading and section list, the `/docs` and `/docs/[slug]` routes. |
| `content/docs/`, `public/guide/` | The Markdown sources of these pages and the screenshots they use. Edit the `.md` files and push; the deploy workflow republishes them. |