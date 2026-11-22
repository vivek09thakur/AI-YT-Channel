#!/usr/bin/env python3
"""Stop the current workflow run for an expected reason without marking it failed.

Some conditions are not errors, just "nothing can be done right now": no upload account for the group, the NotebookLM
daily video quota is used up, not enough Actions minutes left. A red run and a pipeline-failure issue would be noise, so
the run cancels itself instead: the job ends as "cancelled" (grey), the reason is in the job summary and in the log,
and the next 30-minute slot simply tries again.

  python pipeline/stop_run.py "reason"          # from a shell step
  import stop_run; stop_run.stop("reason")      # from a pipeline script (pipeline/ is on sys.path)

Needs GITHUB_TOKEN with `actions: write` (the step must set `GITHUB_TOKEN: ${{ github.token }}` and the workflow
`permissions: actions: write`). Outside GitHub Actions the reason is printed and the exit code is 1.
Exit code 1 is also used when the cancel request fails or the cancellation has not reached the job after 3 minutes, so
the run never continues as if everything were fine.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

WAIT_SECONDS = 180


def _summary(reason):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    text = (
        "### Run stopped\n\n"
        f"{reason}\n\n"
        "Expected condition, not a failure: the run cancelled itself and no video was made. "
        "Scheduled slots try again every 30 minutes.\n\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def _cancel(repo, run_id, token):
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/cancel",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "ai-yt-channel stop_run",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, ""
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            body = json.loads(body).get("message", body)
        except json.JSONDecodeError:
            pass
        return e.code, body
    except urllib.error.URLError as e:
        return 0, str(e.reason)


def stop(reason):
    first = reason.strip().splitlines()[0] if reason.strip() else "stopped"
    print(f"::notice title=Run stopped::{first}")
    print(f"run stopped: {reason}", file=sys.stderr)
    _summary(reason)

    run_id, repo = os.environ.get("GITHUB_RUN_ID"), os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not (run_id and repo):
        sys.exit(1)
    if not token:
        print("::error::stop_run: GITHUB_TOKEN is not set on this step, so the run cannot cancel itself (set "
              "GITHUB_TOKEN: ${{ github.token }} and permissions actions: write)", file=sys.stderr)
        sys.exit(1)

    status, msg = _cancel(repo, run_id, token)
    if status == 202:
        print("cancel requested; waiting for the cancellation to reach this job", file=sys.stderr)
    elif status == 409:
        print("run is already being cancelled", file=sys.stderr)
    else:
        hint = " - GITHUB_TOKEN needs `actions: write`" if status == 403 else ""
        print(f"::error::stop_run: could not cancel run {run_id} (HTTP {status}: {msg}){hint}", file=sys.stderr)
        sys.exit(1)

    # the job is torn down by the runner once the cancellation arrives; if it never does, fail rather than continue
    deadline = time.monotonic() + WAIT_SECONDS
    while time.monotonic() < deadline:
        time.sleep(5)
    print(f"::error::stop_run: run {run_id} was not cancelled within {WAIT_SECONDS} s", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print("usage: stop_run.py <reason>", file=sys.stderr)
        sys.exit(2)
    stop(" ".join(sys.argv[1:]))


if __name__ == "__main__":
    main()
