#!/usr/bin/env python3
"""Resolve upload accounts for YouTube / Instagram from secrets.

Sources (all optional, combined):
  YT_CLIENT_ID + YT_CLIENT_SECRET + YT_REFRESH_TOKEN   -> YouTube account "default"
  YT_ACCOUNTS_JSON  = [{"name":"main","client_id":"..","client_secret":"..","refresh_token":"..","privacy":"public"}, ...]
  IG_USER_ID + IG_ACCESS_TOKEN                          -> Instagram account "default"
  IG_ACCOUNTS_JSON  = [{"name":"brand","user_id":"..","access_token":".."}, ...]
An entry with "enabled": false is skipped.

  list   --upload auto|off          print {"matrix": [...names only...], "count": N, "summary": [...]}
  select --platform P --name N --env-file FILE
                                    write shell exports for that one account and print ::add-mask:: lines
"""
import argparse
import json
import os
import shlex
import sys

REQ = {
    "youtube": ("client_id", "client_secret", "refresh_token"),
    "instagram": ("user_id", "access_token"),
}
ENV = {
    "youtube": {"client_id": "YT_CLIENT_ID", "client_secret": "YT_CLIENT_SECRET", "refresh_token": "YT_REFRESH_TOKEN",
                "privacy": "YT_ACCOUNT_PRIVACY"},
    "instagram": {"user_id": "IG_USER_ID", "access_token": "IG_ACCESS_TOKEN"},
}


def warn(msg):
    print(f"::warning::{msg}", file=sys.stderr)


def env(k):
    return os.environ.get(k, "").strip()


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
    """Return {platform: [ {name, ...creds} ]} with legacy single secrets as 'default'."""
    out = {"youtube": [], "instagram": []}
    legacy_yt = {k: env(ENV["youtube"][k]) for k in REQ["youtube"]}
    if all(legacy_yt.values()):
        out["youtube"].append({"name": "default", **legacy_yt})
    elif any(legacy_yt.values()):
        warn("YouTube default account incomplete - need YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN")
    legacy_ig = {k: env(ENV["instagram"][k]) for k in REQ["instagram"]}
    if all(legacy_ig.values()):
        out["instagram"].append({"name": "default", **legacy_ig})
    elif any(legacy_ig.values()):
        warn("Instagram default account incomplete - need IG_USER_ID, IG_ACCESS_TOKEN")

    for platform, var in (("youtube", "YT_ACCOUNTS_JSON"), ("instagram", "IG_ACCOUNTS_JSON")):
        for i, a in enumerate(load_json_list(var)):
            if not isinstance(a, dict):
                warn(f"{var}[{i}] is not an object - skipped")
                continue
            if a.get("enabled") is False:
                continue
            name = str(a.get("name") or f"account{i + 1}").strip()
            missing = [k for k in REQ[platform] if not str(a.get(k, "")).strip()]
            if missing:
                warn(f"{var} account '{name}' missing {', '.join(missing)} - skipped")
                continue
            if any(x["name"] == name for x in out[platform]):
                warn(f"{var} duplicate account name '{name}' - skipped")
                continue
            out[platform].append({"name": name, **{k: str(v).strip() for k, v in a.items() if k != "enabled"}})
    return out


def cmd_list(a):
    acc = accounts() if a.upload != "off" else {"youtube": [], "instagram": []}
    matrix = [{"platform": p, "name": x["name"]} for p in ("youtube", "instagram") for x in acc[p]]
    summary = [f"{m['platform']}:{m['name']}" for m in matrix]
    # a non-empty placeholder keeps fromJson() happy when the job is skipped via count == 0
    res = {"matrix": matrix or [{"platform": "none", "name": "none"}], "count": len(matrix), "summary": summary}
    print(json.dumps(res))
    if a.upload == "off":
        print("upload: off (workflow input)", file=sys.stderr)
    elif not matrix:
        print("::notice::no upload accounts configured (set YT_* / IG_* secrets or YT_ACCOUNTS_JSON / IG_ACCOUNTS_JSON)", file=sys.stderr)
    else:
        print("upload accounts: " + ", ".join(summary), file=sys.stderr)


def cmd_select(a):
    acc = accounts()
    match = [x for x in acc.get(a.platform, []) if x["name"] == a.name]
    if not match:
        print(f"::error::no {a.platform} account named '{a.name}'", file=sys.stderr)
        sys.exit(1)
    x = match[0]
    lines = []
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
    print(f"selected {a.platform} account '{a.name}'", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list")
    l.add_argument("--upload", default="auto")
    l.set_defaults(fn=cmd_list)
    s = sub.add_parser("select")
    s.add_argument("--platform", required=True, choices=list(REQ))
    s.add_argument("--name", required=True)
    s.add_argument("--env-file", required=True)
    s.set_defaults(fn=cmd_select)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
