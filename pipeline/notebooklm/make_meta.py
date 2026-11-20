#!/usr/bin/env python3
"""Build meta.json for a NotebookLM short from the CLI's --json outputs.

usage: make_meta.py --topic T --genre G --slug S --format short [--ask ask.json] [--sources sources.json] [--notebook ID] --out meta.json

ask.json is the output of `notebooklm ask --json "<prompt asking for a JSON object with title/description/hashtags>"`.
Everything is best effort: missing or unparsable inputs fall back to the topic text.
"""
import argparse, json, re
from pathlib import Path

ANSWER_KEYS = ('answer', 'text', 'response', 'content', 'message')


def load(path):
    if not path or not Path(path).exists():
        return None
    try:
        return json.loads(Path(path).read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return None


def find_text(obj):
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        for k in ANSWER_KEYS:
            if isinstance(obj.get(k), str):
                return obj[k]
        for v in obj.values():
            t = find_text(v)
            if t:
                return t
    if isinstance(obj, list):
        for v in obj:
            t = find_text(v)
            if t:
                return t
    return ''


def parse_answer(text):
    m = re.search(r'\{.*\}', text, re.S)
    if not m:
        return {}
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}
    return d if isinstance(d, dict) else {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--genre', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--format', default='short')
    ap.add_argument('--ask', default='')
    ap.add_argument('--sources', default='')
    ap.add_argument('--notebook', default='')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    ans = parse_answer(find_text(load(a.ask) or {}))
    title = str(ans.get('title') or a.topic).strip()[:100]
    description = str(ans.get('description') or a.topic).strip()
    tags = ans.get('hashtags') or ans.get('tags') or []
    if isinstance(tags, str):
        tags = re.findall(r'#?\w+', tags)
    tags = ['#' + t.lstrip('#') for t in tags if str(t).strip()][:10]

    sources = []
    src = load(a.sources)
    rows = src.get('sources', src) if isinstance(src, dict) else (src or [])
    for s in rows if isinstance(rows, list) else []:
        if isinstance(s, dict):
            sources.append({'title': s.get('title', ''), 'url': s.get('url', '')})

    meta = {'title': title, 'topic': a.topic, 'genre': a.genre, 'slug': a.slug, 'format': a.format,
            'description': description, 'hashtags': tags, 'notebook_id': a.notebook, 'sources': sources,
            'generator': 'notebooklm video overview'}
    Path(a.out).write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: meta[k] for k in ('title', 'hashtags')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
