#!/usr/bin/env python3
"""Build meta.json for a NotebookLM short from the CLI's --json outputs.

usage: make_meta.py --topic T --genre G --slug S --format short [--ask ask.json] [--sources sources.json] [--notebook ID] [--cta "..."] --out meta.json

ask.json is the output of `notebooklm ask --json "<prompt asking for a JSON object with title/description/hashtags>"`.
Everything is best effort: missing or unparsable inputs fall back to the topic text.
Also writes caption_youtube.txt / caption_instagram.txt next to --out (description + CTA + hashtags, platform limits applied).
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
        # strict=False: models often put real newlines inside the "script" string (paragraph breaks), which strict JSON rejects
        d = json.loads(m.group(0), strict=False)
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
    ap.add_argument('--cta', default='', help='closing call-to-action line appended to captions')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    ans = parse_answer(find_text(load(a.ask) or {}))
    title = str(ans.get('title') or a.topic).strip()[:100]
    description = str(ans.get('description') or a.topic).strip()
    tags = ans.get('hashtags') or ans.get('tags') or []
    if isinstance(tags, str):
        tags = re.findall(r'#?\w+', tags)
    tags = dedupe('#' + re.sub(r'\W+', '', str(t).lstrip('#').lower()) for t in tags if re.sub(r'\W+', '', str(t)))
    tags = [t for t in tags if t != '#'][:15]

    sources = []
    src = load(a.sources)
    rows = src.get('sources', src) if isinstance(src, dict) else (src or [])
    for s in rows if isinstance(rows, list) else []:
        if isinstance(s, dict):
            sources.append({'title': s.get('title', ''), 'url': s.get('url', '')})

    cta = a.cta.strip()
    caption_youtube = build_caption(description, cta, tags, ['#shorts'], limit=4900)
    caption_instagram = build_caption(description, cta, tags, ['#reels', '#explore', '#learnsomethingnew'], limit=2100, max_tags=30)

    meta = {'title': title, 'topic': a.topic, 'genre': a.genre, 'slug': a.slug, 'format': a.format,
            'description': description, 'hashtags': tags, 'cta': cta,
            'caption_youtube': caption_youtube, 'caption_instagram': caption_instagram,
            'notebook_id': a.notebook, 'sources': sources, 'generator': 'notebooklm video overview'}
    out = Path(a.out)
    out.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
    (out.parent / 'caption_youtube.txt').write_text(caption_youtube + '\n', encoding='utf-8')
    (out.parent / 'caption_instagram.txt').write_text(caption_instagram + '\n', encoding='utf-8')
    print(json.dumps({k: meta[k] for k in ('title', 'hashtags')}, ensure_ascii=False))


def dedupe(items):
    seen, out = set(), []
    for x in items:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def build_caption(description, cta, tags, platform_tags, limit, max_tags=20):
    """description, blank line, CTA, blank line, hashtags - trimmed to the platform's caption limit."""
    all_tags = dedupe(list(tags) + platform_tags)[:max_tags]
    parts = [description]
    if cta and 'subscrib' not in description.lower():
        parts.append(cta)
    if all_tags:
        parts.append(' '.join(all_tags))
    text = '\n\n'.join(p for p in parts if p)
    while len(text) > limit and all_tags:
        all_tags.pop()
        parts[-1] = ' '.join(all_tags)
        text = '\n\n'.join(p for p in parts if p)
    return text[:limit]


if __name__ == '__main__':
    main()
