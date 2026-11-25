#!/usr/bin/env python3
"""Is this video already on the channel? Used by the story picker (so the LLM is asked for another subject) and by the
story workflow (so a run stops before rendering, and again before publishing, instead of posting a repeat).

usage: dedupe.py --index site/videos.json --slug <slug> [--title "<title>"] [--title "<other title>"]

Exit 0 when nothing in the index matches. Exit 1 with a ::error:: line when the slug was published before, or when a
given title / topic names a published story: 60 % of the meaningful words shared, or a short title contained in a longer
published one (the part before a ":" subtitle is compared too, so "Birth of Ganesha" matches "The Birth of Ganesha: ...").
A missing or unreadable index passes (first video).
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

STOP = {'a', 'an', 'and', 'the', 'of', 'to', 'in', 'on', 'for', 'with', 'how', 'why', 'what', 'who', 'is', 'was', 'his',
        'her', 'its', 'from', 'by', 'at', 'as', 'that', 'this', 'into', 'story', 'tale', 'legend', 'true', 'real',
        'hidden', 'secret', 'untold', 'shorts', 'short', 'ep', 'part', 'chapter', 'episode'}
THRESHOLD = 0.6


def slugify(text, limit=40):
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return text[:limit].rstrip('-')


def words(text):
    out = set()
    for w in re.findall(r'[a-z0-9]+', str(text).lower()):
        if w in STOP or w.isdigit():
            continue
        # crude stem so "curses" / "cursed" / "cursing" meet "curse"
        for suffix in ('ing', 'ed', 'es', 's'):
            if w.endswith(suffix) and len(w) - len(suffix) >= 3:
                w = w[:-len(suffix)]
                break
        out.add(w)
    return out


def load_index(path):
    p = Path(path) if path else None
    if not p or not p.exists():
        return []
    try:
        rows = json.loads(p.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, OSError):
        return []
    return [e for e in rows if isinstance(e, dict)] if isinstance(rows, list) else []


def _variants(text):
    """the whole title and its head before a ':' / ' - ' subtitle, as word sets (subtitles dilute the overlap)"""
    text = str(text or '')
    heads = {text} | {p for p in re.split(r'\s*[:|]\s*|\s+-\s+', text, maxsplit=1)[:1]}
    return [w for w in (words(h) for h in heads) if len(w) >= 2]


def similar(a, b):
    """True when two titles name the same story: 60 % of the words shared, or one short title inside the other"""
    for x in _variants(a):
        for y in _variants(b):
            common = len(x & y)
            if common / len(x | y) >= THRESHOLD or common / min(len(x), len(y)) >= 0.75:
                return True
    return False


def find_duplicate(used, slug='', *titles):
    """'' when the slug / titles are new, otherwise one line naming what they repeat."""
    slug = slugify(slug) if slug else ''
    for e in used:
        if slug and slugify(e.get('slug') or '') == slug:
            return f'slug "{slug}" was published on {e.get("date", "?")} as "{e.get("title") or e.get("topic") or slug}"'
    for t in titles:
        if len(words(t)) < 2:
            continue
        for e in used:
            for key in ('title', 'topic'):
                if e.get(key) and similar(t, e[key]):
                    return f'"{t}" is too close to "{e[key]}" published on {e.get("date", "?")}'
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--index', required=True, help='videos.json from the videos branch')
    ap.add_argument('--slug', default='')
    ap.add_argument('--title', action='append', default=[], help='title / topic to compare (repeatable)')
    a = ap.parse_args()
    used = load_index(a.index)
    dup = find_duplicate(used, a.slug, *[t for t in a.title if t.strip()])
    if dup:
        sys.exit(f'::error::already on the channel: {dup}. Pick another subject (or a clearly different title) and run again.')
    print(f'not published before ({len(used)} videos in the index)')


if __name__ == '__main__':
    main()
