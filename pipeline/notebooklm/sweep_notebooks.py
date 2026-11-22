#!/usr/bin/env python3
"""Decide which leftover NotebookLM notebooks to delete before a run.

usage: sweep_notebooks.py --notebooks notebooks.json --topics topics.json

notebooks.json is the output of `notebooklm list --json`. A notebook is a leftover of an earlier (crashed / cancelled)
workflow run when its title exactly matches a topic in topics.json - those are printed as `DELETE <id>` lines for the
workflow to act on. Anything else is only reported (`KEEP <id> <title>`), so a notebook created by hand on the same
account is never touched. Topics picked by the LLM (pick_topic.py) are not in topics.json, so a leftover with such a
title shows up as KEEP; this is rare because the make job deletes its own notebook even when it fails.
"""
import argparse, json
from pathlib import Path


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return None


def rows(obj):
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for k in ('notebooks', 'items', 'results', 'data'):
            if isinstance(obj.get(k), list):
                return obj[k]
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--notebooks', required=True)
    ap.add_argument('--topics', required=True)
    a = ap.parse_args()

    topics = set()
    t = load(a.topics) or {}
    for pool in (t.values() if isinstance(t, dict) else t):
        for x in (pool if isinstance(pool, list) else []):
            topics.add(str(x).strip().lower())

    nbs = rows(load(a.notebooks))
    print(f'notebooks on account: {len(nbs)}')
    for nb in nbs:
        if not isinstance(nb, dict):
            continue
        nid = str(nb.get('id') or nb.get('notebook_id') or '').strip()
        title = str(nb.get('title') or nb.get('name') or '').strip()
        if not nid:
            continue
        if title.lower() in topics:
            print(f'DELETE {nid} {title}')
        else:
            print(f'KEEP {nid} {title}')


if __name__ == '__main__':
    main()
