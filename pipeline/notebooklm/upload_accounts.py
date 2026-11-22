#!/usr/bin/env python3
"""Resolve upload accounts for YouTube / Instagram from secrets.

Sources (all optional, combined). Secrets arrive as named environment variables: the workflows map each one explicitly
(user1..user5 per platform; extend the env blocks for more). Never pass the whole secrets context as JSON - GitHub holds
such a workflow as potentially malicious and its scheduled runs never start.
  IG_USER_ID + IG_ACCESS_TOKEN                          -> Instagram account "default"
  IG_USER1_ID + IG_USER1_TOKEN, IG_USER2_ID + ...       -> Instagram accounts "user1", "user2", ... (IG_USERn_NAME optional)
  YT_CLIENT_ID + YT_CLIENT_SECRET + YT_REFRESH_TOKEN    -> YouTube account "default"
  YT_CLIENT_ID + YT_CLIENT_SECRET + YT_USERn_REFRESH_TOKEN -> YouTube "usern" (shared OAuth client, one token per channel)
  YT_USER1_CLIENT_ID + YT_USER1_CLIENT_SECRET + YT_USER1_REFRESH_TOKEN, ...
                                                        -> YouTube accounts "user1", ... (YT_USERn_NAME / YT_USERn_PRIVACY optional)
  YT_ACCOUNTS_JSON / IG_ACCOUNTS_JSON                    -> JSON lists, see README. "enabled": false skips an entry.

Which workflow may use an account (optional): IG_USERn_FOR / YT_USERn_FOR / IG_FOR / YT_FOR / JSON "for" = comma list
of groups, e.g. "story" or "nlm,story". Unset or "all" = every workflow. `list --group story` keeps only matching accounts.

  list   --upload auto|off [--group G] [--platforms youtube,instagram]
                                    print {"matrix": ["platform/key", ...], "count": N, "summary": [...]}
  require [--group G]               stop the run (cancelled, reason in the job summary - see pipeline/stop_run.py) when no
                                    YouTube or Instagram account is configured for the group; the daily workflows run this
                                    in precheck so no video is made that cannot be uploaded
  select --platform P --name N --env-file FILE
                                    write shell exports for that one account and print ::add-mask:: lines

IMPORTANT: the matrix is a flat list of "platform/key" strings where key is fixed and non-secret (default, user1,
user2, json1 ...), never a value taken from a secret. GitHub silently drops any job output that contains a masked
value ("Skip output ... since it may contain secret"), and it masks every LINE of a multi-line secret - a
pretty-printed master_token.json makes "{" and "}" masked, so the output must not be a JSON object either.
The optional *_NAME label is only resolved inside the upload job (select) and exported as ACCOUNT_LABEL.
"""
import argparse
import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import stop_run

REQ = {
    "youtube": ("client_id", "client_secret", "refresh_token"),
    "instagram": ("user_id", "access_token"),
}
ENV = {
    "youtube": {"client_id": "YT_CLIENT_ID", "client_secret": "YT_CLIENT_SECRET", "refresh_token": "YT_REFRESH_TOKEN",
                "privacy": "YT_ACCOUNT_PRIVACY"},
    "instagram": {"user_id": "IG_USER_ID", "access_token": "IG_ACCESS_TOKEN"},
}
# credentials that may come from the shared single secret when the numbered one is absent
SHARED = {"youtube": ("client_id", "client_secret")}
# numbered secrets: prefix, suffix per credential key
NUMBERED = {
    "youtube": ("YT_USER", {"client_id": "CLIENT_ID", "client_secret": "CLIENT_SECRET", "refresh_token": "REFRESH_TOKEN",
                            "privacy": "PRIVACY"}),
    "instagram": ("IG_USER", {"user_id": "ID", "access_token": "TOKEN"}),
}


def warn(msg):
    print(f"::warning::{msg}", file=sys.stderr)


def env(k):
    return (os.environ.get(k) or "").strip()


def groups(raw):
    """'nlm, story' -> {'nlm', 'story'}; empty / 'all' -> set() meaning no restriction."""
    s = {g.strip().lower() for g in str(raw or "").replace(";", ",").split(",") if g.strip()}
    return set() if not s or "all" in s else s


def numbered(platform):
    """Collect IG_USER<n>_ID / YT_USER<n>_CLIENT_ID ... style accounts, ordered by n."""
    prefix, suffix = NUMBERED[platform]
    # unused slots are present but empty (the workflows map user1..user5 explicitly), so only a slot with a value counts
    nums = sorted({int(m.group(1)) for k, v in os.environ.items() if v.strip()
                   for m in [re.fullmatch(rf"{prefix}(\d+)_[A-Z_]+", k)] if m})
    out = []
    for n in nums:
        acc = {k: env(f"{prefix}{n}_{s}") for k, s in suffix.items()}
        # one Google Cloud OAuth client serves every channel: YT_CLIENT_ID / YT_CLIENT_SECRET are the shared fallback
        for k in SHARED.get(platform, ()):
            acc[k] = acc[k] or env(ENV[platform][k])
        missing = [k for k in REQ[platform] if not acc[k]]
        if missing:
            warn(f"{prefix}{n}_* account incomplete - missing {', '.join(f'{prefix}{n}_{suffix[k]}' for k in missing)} - skipped")
            continue
        out.append({"name": f"user{n}", "label": env(f"{prefix}{n}_NAME") or f"user{n}",
                    "for": groups(env(f"{prefix}{n}_FOR")), **{k: v for k, v in acc.items() if v}})
    return out


def load_json_list(var):
    raw = env(var)
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        warn(f"{var} is not valid JSON ({e.msg}) - ignored")
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        warn(f"{var} must be a JSON array - ignored")
        return []
    return data


def accounts():
    """Return {platform: [ {name (non-secret key), label, ...creds} ]} with legacy single secrets as 'default'."""
    out = {"youtube": [], "instagram": []}
    legacy_yt = {k: env(ENV["youtube"][k]) for k in REQ["youtube"]}
    if all(legacy_yt.values()):
        out["youtube"].append({"name": "default", "label": "default", "for": groups(env("YT_FOR")), **legacy_yt})
    elif legacy_yt["refresh_token"]:
        warn("YouTube default account incomplete - need YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN")
    legacy_ig = {k: env(ENV["instagram"][k]) for k in REQ["instagram"]}
    if all(legacy_ig.values()):
        out["instagram"].append({"name": "default", "label": "default", "for": groups(env("IG_FOR")), **legacy_ig})
    elif any(legacy_ig.values()):
        warn("Instagram default account incomplete - need IG_USER_ID, IG_ACCESS_TOKEN")

    for platform in ("youtube", "instagram"):
        for x in numbered(platform):
            if any(y["name"] == x["name"] for y in out[platform]):
                warn(f"{platform} duplicate account name '{x['name']}' - skipped")
                continue
            out[platform].append(x)

    for platform, var in (("youtube", "YT_ACCOUNTS_JSON"), ("instagram", "IG_ACCOUNTS_JSON")):
        for i, a in enumerate(load_json_list(var)):
            if not isinstance(a, dict):
                warn(f"{var}[{i}] is not an object - skipped")
                continue
            if a.get("enabled") is False:
                continue
            # matrix key is positional (json1, json2 ...); the JSON "name" is secret content -> label only
            name = f"json{i + 1}"
            label = str(a.get("name") or name).strip()
            missing = [k for k in REQ[platform] if not str(a.get(k, "")).strip()]
            if missing:
                warn(f"{var}[{i}] missing {', '.join(missing)} - skipped")
                continue
            out[platform].append({"name": name, "label": label, "for": groups(a.get("for")),
                                  **{k: str(v).strip() for k, v in a.items() if k not in ("enabled", "name", "for")}})
    return out


def allowed(x, group):
    return not group or not x["for"] or group.lower() in x["for"]


def cmd_list(a):
    acc = accounts() if a.upload != "off" else {"youtube": [], "instagram": []}
    platforms = [p.strip() for p in a.platforms.split(",") if p.strip()]
    skipped = [f"{p}/{x['name']}" for p in platforms for x in acc[p] if not allowed(x, a.group)]
    acc = {p: [x for x in acc[p] if allowed(x, a.group)] if p in platforms else [] for p in acc}
    if skipped:
        print(f"not for group '{a.group}': " + ", ".join(skipped), file=sys.stderr)
    # matrix is a flat list of "platform/key" strings on purpose: GitHub masks every LINE of a multi-line secret
    # (e.g. a pretty-printed master_token.json gives masks "{" and "}") and drops any job output containing a
    # masked value - so the output must not contain braces or anything else that could be a secret line.
    matrix = [f"{p}/{x['name']}" for p in ("youtube", "instagram") for x in acc[p]]
    # a non-empty placeholder keeps fromJson() happy when the job is skipped via count == 0
    res = {"matrix": matrix or ["none/none"], "count": len(matrix), "summary": matrix}
    print(json.dumps(res))
    if a.upload == "off":
        print("upload: off (workflow input)", file=sys.stderr)
    elif not matrix:
        print("::notice::no upload accounts configured (set YT_* / IG_* secrets or YT_ACCOUNTS_JSON / IG_ACCOUNTS_JSON)", file=sys.stderr)
    else:
        print("upload accounts: " + ", ".join(matrix), file=sys.stderr)


def cmd_require(a):
    acc = accounts()
    ok = [f"{p}/{x['name']}" for p in ("youtube", "instagram") for x in acc[p] if allowed(x, a.group)]
    group = a.group or "all"
    if ok:
        print(f"upload accounts for group '{group}': " + ", ".join(ok))
        return
    stop_run.stop(f"No upload account for workflow group '{group}'. Add a YouTube account (YT_CLIENT_ID + YT_CLIENT_SECRET + "
                  f"YT_USERn_REFRESH_TOKEN) or an Instagram account (IG_USERn_ID + IG_USERn_TOKEN); when YT_USERn_FOR / IG_USERn_FOR "
                  f"is set it must include '{group}'. Stopped before making a video that could not be uploaded.")


def cmd_select(a):
    acc = accounts()
    match = [x for x in acc.get(a.platform, []) if x["name"] == a.name]
    if not match:
        print(f"::error::no {a.platform} account named '{a.name}'", file=sys.stderr)
        sys.exit(1)
    x = match[0]
    lines = [f"export ACCOUNT_LABEL={shlex.quote(x.get('label') or a.name)}"]
    for key, var in ENV[a.platform].items():
        val = x.get(key, "")
        if not val:
            continue
        if key not in ("privacy",):
            print(f"::add-mask::{val}")
        lines.append(f"export {var}={shlex.quote(val)}")
    with open(a.env_file, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(a.env_file, 0o600)
    if a.github_output:
        with open(a.github_output, "a") as f:
            f.write(f"label={x.get('label') or a.name}\n")
    print(f"selected {a.platform} account '{a.name}'", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--upload", default="auto")
    l.add_argument("--group", default="", help="workflow group (nlm, story ...); accounts with *_FOR not listing it are skipped")
    l.add_argument("--platforms", default="youtube,instagram")
    l.set_defaults(fn=cmd_list)
    r = sub.add_parser("require")
    r.add_argument("--group", default="")
    r.set_defaults(fn=cmd_require)
    s = sub.add_parser("select")
    s.add_argument("--platform", required=True, choices=list(REQ))
    s.add_argument("--name", required=True)
    s.add_argument("--env-file", required=True)
    s.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT", ""))
    s.set_defaults(fn=cmd_select)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
