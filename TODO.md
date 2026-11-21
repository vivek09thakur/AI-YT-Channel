# TODO

## Open

### Account secrets (repo > Settings > Secrets and variables > Actions)

Tokens come from the account owner's login (Instagram: Meta Business account / app tester; YouTube: OAuth consent on the channel's Google account, shared `YT_CLIENT_ID` / `YT_CLIENT_SECRET`, owner added as GCP test user).

- [ ] **IG_USER2 - Pauranik Katha (`story`)**: `IG_USER2_ID`, `IG_USER2_TOKEN`, `IG_USER2_FOR=story`, `IG_USER2_NAME=Pauranik Katha`
- [ ] **YT_USER3 - stickman channel (`stickman`)**: `YT_USER3_REFRESH_TOKEN`, `YT_USER3_FOR=stickman`, `YT_USER3_NAME=<channel name>`
- [ ] **IG_USER3 - daily fact challenge (`stickman`)**: `IG_USER3_ID`, `IG_USER3_TOKEN`, `IG_USER3_FOR=stickman`, `IG_USER3_NAME=daily fact challenge`
- [ ] Test each new account once with Actions > **Upload video** (group = its group, platform = its platform, `yt_privacy=private` first)

### Repo

- [ ] README: Mermaid diagram of workflow group -> `YT_USERn` / `IG_USERn` (no personal names), under "Which account gets which video"
- [ ] Review the 3 Dependabot alerts (2 high, 1 moderate) on `main` - probably `template/package-lock.json`; bump, re-render a reel, confirm
- [ ] Regenerate any tokens that were ever pasted into chat or committed

## Done

- [x] Folk-art story video pipeline (kit, engine, contract, generator, render, workflow)
- [x] NotebookLM short: precheck, captions, YouTube / Instagram upload, docs
- [x] Multi-account upload with `_FOR` groups and `_NAME` labels
- [x] Robustness: retry cron slots, upload retries, failure issue (`6f85b81`)
- [x] Vercel dashboard for secrets / accounts / runs
- [x] Stickman fact reel: kit, stick rig, fact shape, workflow (2/day, group `stickman`), docs (`f431e12`)
- [x] Upload workflow: platform dropdown fix, group / account naming explained (`440061d`)
- [x] Story video default voice `en-GB-RyanNeural` (`fd28acd`)
