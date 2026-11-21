#!/usr/bin/env python3
"""Resolve upload accounts for YouTube / Instagram from secrets.

Sources (all optional, combined). Secrets are read from the environment or from ALL_SECRETS (toJSON(secrets)).
  IG_USER_ID + IG_ACCESS_TOKEN                          -> Instagram account "default"
  IG_USER1_ID + IG_USER1_TOKEN, IG_USER2_ID + ...       -> Instagram accounts "user1", "user2", ... (IG_USERn_NAME optional)
  YT_CLIENT_ID + YT_CLIENT_SECRET + YT_REFRESH_TOKEN    -> YouTube account "default"
  YT_USER1_CLIENT_ID + YT_USER1_CLIENT_SECRET + YT_USER1_REFRESH_TOKEN, ...
                                                        -> YouTube accounts "user1", ... (YT_USERn_NAME / YT_USERn_PRIVACY optional)
  YT_ACCOUNTS_JSON / IG_ACCOUNTS_JSON                    -> JSON lists, see README. "enabled": false skips an entry.

  list   --upload auto|off          print {"matrix": [...names only...], "count": N, "summary": [...]}
  select --platform P --name N --env-file FILE
                                    write shell exports for that one account and print ::add-mask:: lines
"""
import argparse
import json
import os
import re
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
# numbered secrets: prefix, suffix per credential key
NUMBERED = {
    "youtube": ("YT_USER", {"client_id": "CLIENT_ID", "client_secret": "CLIENT_SECRET", "refresh_token": "REFRESH_TOKEN",
                            "privacy": "PRIVACY"}),
    "instagram": ("IG_USER", {"user_id": "ID", "access_token": "TOKEN"}),
}


def warn(msg):
    print(f"::warning::{msg}", file=sys.stderr)


def _secrets():
    merged = dict(os.environ)
    raw = os.environ.get("ALL_SECRETS", "")
    if raw:
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                merged.update({k: str(v) for k, v in data.items()})
        except json.JSONDecodeError:
            warn("ALL_SECRETS is not valid JSON - ignored")
    return merged


SECRETS = None


def env(k):
    global SECRETS
    if SECRETS is None:
        SECRETS = _secrets()
    return (SECRETS.get(k) or "").strip()


def numbered(platform):
    """Collect IG_USER<n>_ID / YT_USER<n>_CLIENT_ID ... style accounts, ordered by n."""
    prefix, suffix = NUMBERED[platform]
    if SECRETS is None:
        env("")
    nums = sorted({int(m.group(1)) for k in SECRETS for m in [re.fullmatch(rf"{prefix}(\d+)_[A-Z_]+", k)] if m})
    out = []
    for n in nums:
        acc = {k: env(f"{prefix}{n}_{s}") for k, s in suffix.items()}
        name = env(f"{prefix}{n}_NAME") or f"user{n}"
        missing = [k for k in REQ[platform] if not acc[k]]
        if missing:
            warn(f"{prefix}{n}_* account incomplete - missing {', '.join(f'{prefix}{n}_{suffix[k]}' for k in missing)} - skipped")
            continue
        out.append({"name": name, **{k: v for k, v in acc.items() if v}})
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
