#!/usr/bin/env python3
"""Pick a random, not-yet-published topic for the NotebookLM short workflow.

usage: pick_topic.py --topics pipeline/notebooklm/topics.json [--genre auto|science|...] [--used nlm.json] [--topic "override"]

Writes genre / topic / slug to $GITHUB_OUTPUT (when set) and prints them. Topics already present in the published index
(nlm.json from the videos branch, matched by slug) are skipped; when a genre is exhausted the least recently published
topic of that genre is reused.
"""
import argparse, json, os, random, re, unicodedata
from pathlib import Path


def slugify(text, limit=40):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return text[:limit].rstrip('-') or 'topic'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', required=True)
    ap.add_argument('--genre', default='auto')
    ap.add_argument('--used', default='')
    ap.add_argument('--topic', default='')
    a = ap.parse_args()

    topics = json.loads(Path(a.topics).read_text(encoding='utf-8'))
    genres = sorted(topics)
    genre = a.genre if a.genre in topics else ''

    if a.topic.strip():
        topic, genre = a.topic.strip(), genre or 'custom'
    else:
        used = []
        if a.used and Path(a.used).exists():
            try:
                used = json.loads(Path(a.used).read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                used = []
        # newest first in the index -> position = recency rank
        used_rank = {}
        for i, e in enumerate(used):
            used_rank.setdefault(e.get('slug', ''), i)

        genre = genre or random.choice(genres)
        pool = topics[genre]
        fresh = [t for t in pool if slugify(t) not in used_rank]
        if fresh:
            topic = random.choice(fresh)
        else:
            topic = max(pool, key=lambda t: used_rank.get(slugify(t), -1))
            print(f'all {genre} topics published already; reusing oldest')

    slug = slugify(topic)
    out = {'genre': genre, 'topic': topic, 'slug': slug}
    for k, v in out.items():
        print(f'{k}: {v}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            for k, v in out.items():
                f.write(f'{k}={v}\n')


if __name__ == '__main__':
    main()
