# TODO

## Open

### Account secrets (repo > Settings > Secrets and variables > Actions)

Tokens come from the account owner's login (Instagram: Meta Business account / app tester; YouTube: OAuth consent on the channel's Google account, shared `YT_CLIENT_ID` / `YT_CLIENT_SECRET`, owner added as GCP test user).

- [ ] **IG_USER2 - Pauranik Katha (`story`)**: `IG_USER2_ID`, `IG_USER2_TOKEN`, `IG_USER2_FOR=story`, `IG_USER2_NAME=Pauranik Katha`
- [ ] **YT_USER3 - stickman channel (`stickman`)**: `YT_USER3_REFRESH_TOKEN`, `YT_USER3_FOR=stickman`, `YT_USER3_NAME=<channel name>`
- [ ] **IG_USER3 - daily fact challenge (`stickman`)**: `IG_USER3_ID`, `IG_USER3_TOKEN`, `IG_USER3_FOR=stickman`, `IG_USER3_NAME=daily fact challenge`
- [ ] Test each new account once with Actions > **Upload video** (group = its group, platform = its platform, `yt_privacy=private` first)

### Repo

- [ ] **Add the `VERCEL_TOKEN` repo secret** so the Deploy dashboard workflow can deploy: Vercel → Account settings → Tokens → Create (scope: the team), then repo Settings → Secrets and variables → Actions → `VERCEL_TOKEN`. Then Actions → Deploy dashboard → Run workflow once; after it is green, Vercel → Settings → Git → Disconnect (the workflow is the only deploy path from then on, so bot pushes to `main` / `videos` no longer show up on Vercel)
- [ ] Fill the `DASHBOARD_ACCOUNTS` repo variable with each account's name and workflow groups so the board draws solid arrows (`gh variable set DASHBOARD_ACCOUNTS`, format in `dashboard/README.md`)
- [ ] Rotate the dashboard credentials: new fine-grained PAT (`Actions` read and write for the trigger; read-only `Secrets`, `Variables`, `Contents`, `Issues`) and a new `DASHBOARD_USERS` password; update `dashboard/.env.local` and the Vercel project (`vercel env add GITHUB_TOKEN production --sensitive --force`, same for `DASHBOARD_USERS`), then revoke the old PAT
- [ ] Regenerate any other tokens that were ever pasted into chat or committed

## Done

- [x] External trigger switched on: `CRON_SECRET` set on Vercel, schedule `daily-videos` active, first run started by it on 23 Nov 9:19 am (NotebookLM run 11)
- [x] Dashboard moved into `dashboard/` on `main` (one branch for everything); deployed by the Deploy dashboard workflow (Vercel CLI, Root Directory `dashboard`, root `.vercelignore`) instead of Vercel's Git integration, which reacted to every bot push; the separate `dashboard` branch is gone (old copies in local `dashboard-branch-backup` and `dashboard-full-backup` branches)
- [x] Dashboard deployed on Vercel (env vars in Production)
- [x] Dashboard: read-only board of workflows -> accounts with today's posts and upload results, runs page, secrets page with a section sidebar, password login, `/api/trigger` for Vercel's scheduler
- [x] README: Mermaid diagram of workflow group -> `YT_USERn` / `IG_USERn`
- [x] README / account guide: full secrets and variables reference, schedules, routing, costs, known limits (`ca1888d`)
- [x] Fresh `main` history (single root commit, same tree); old history in local `main-backup` + `E:\Projects\AI-YT-Channel-old-history.bundle`
- [x] Folk-art story video pipeline (kit, engine, contract, generator, render, workflow)
- [x] NotebookLM short: precheck, captions, YouTube / Instagram upload, docs
- [x] Multi-account upload with `_FOR` groups and `_NAME` labels
- [x] Robustness: retry cron slots, upload retries, failure issue (`6f85b81`)
- [x] Stickman fact reel: kit, stick rig, fact shape, workflow (2/day, group `stickman`), docs (`f431e12`)
- [x] Upload workflow: platform dropdown fix, group / account naming explained (`440061d`)
- [x] Story video default voice `en-GB-RyanNeural` (`fd28acd`)
