#!/usr/bin/env python3
"""Add upload captions to a folk-art story's meta.json (same fields the NotebookLM shorts have).

usage: captions.py --meta final/meta.json [--script work/script.txt] [--topic T] [--cta "..."] [--provider auto --model ...]

Asks the LLM (same fallback chain as the story writer) for a YouTube description + hashtags from the narration;
falls back to the meta.json description / topic words when no LLM answers. Writes into meta.json:
  description, hashtags, cta, caption_youtube, caption_instagram, slug, format
and caption_youtube.txt / caption_instagram.txt next to it. Never fails the run.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'notebooklm'))
from make_meta import build_caption, dedupe, parse_answer  # noqa: E402

BASE_TAGS = ['#folktale', '#mythology', '#indianmythology', '#animation', '#storytelling']
SYSTEM = 'You write YouTube metadata. Reply with ONE JSON object only, no markdown.'
PROMPT = '''Title: {title}
Narration:
{script}

Return JSON: {{"description": "<2-3 sentence hook for the video description, no hashtags, no emojis>",
"hashtags": ["<8-12 lowercase hashtags about this video, its subject and its characters, each starting with #>"]}}'''


def ask_llm(provider, model, title, script):
    try:
        from generate_story import DEFAULT_MODEL, call_with_fallback
    except ImportError as e:
        print(f'LLM unavailable ({e}); using fallback captions', file=sys.stderr)
        return {}
    if provider in ('', 'auto'):
        provider = 'gemini'
    model = model or DEFAULT_MODEL.get(provider, '')
    try:
        text, _usage, p, m = call_with_fallback(provider, model, SYSTEM,
                                                [{'role': 'user', 'content': PROMPT.format(title=title, script=script[:6000])}], 800)
        print(f'captions by {p} {m}')
        return parse_answer(text)
    except SystemExit as e:
        print(f'::warning::no LLM for captions ({str(e)[:200]}); using fallback', file=sys.stderr)
        return {}


def fallback_tags(title):
    words = [w for w in re.findall(r'[A-Za-z]{4,}', title) if w.lower() not in ('the', 'how', 'became', 'story', 'from', 'with')]
    return ['#' + w.lower() for w in words[:6]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--meta', required=True)
    ap.add_argument('--script', default='')
    ap.add_argument('--topic', default='')
    ap.add_argument('--slug', default='')
    ap.add_argument('--cta', default='')
    ap.add_argument('--provider', default='auto')
    ap.add_argument('--model', default='')
    ap.add_argument('--base-tags', default='', help='comma list of hashtags always appended (default: folk tale set)')
    a = ap.parse_args()
    base_tags = [t.strip() for t in a.base_tags.split(',') if t.strip()] or BASE_TAGS

    out = Path(a.meta)
    meta = json.loads(out.read_text(encoding='utf-8')) if out.exists() else {}
    title = str(meta.get('title') or a.topic or a.slug or 'Story').strip()[:100]
    script = Path(a.script).read_text(encoding='utf-8') if a.script and Path(a.script).exists() else ''

    ans = ask_llm(a.provider, a.model, title, script or meta.get('description', ''))
    description = str(ans.get('description') or meta.get('description') or a.topic or title).strip()
    tags = ans.get('hashtags') or ans.get('tags') or []
    if isinstance(tags, str):
        tags = re.findall(r'#?\w+', tags)
    tags = ['#' + re.sub(r'\W+', '', str(t).lstrip('#').lower()) for t in tags]
    tags = [t for t in dedupe(tags + fallback_tags(title) + base_tags) if t != '#'][:15]

    cta = a.cta.strip()
    meta.update({
        'title': title, 'topic': meta.get('topic') or a.topic or title, 'slug': a.slug or meta.get('slug', ''),
        'format': meta.get('format', 'story'), 'description': description, 'hashtags': tags, 'cta': cta,
        'caption_youtube': build_caption(description, cta, tags, ['#shorts'], limit=4900),
        'caption_instagram': build_caption(description, cta, tags, ['#reels', '#explore'], limit=2100, max_tags=30),
    })
    out.write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
    (out.parent / 'caption_youtube.txt').write_text(meta['caption_youtube'] + '\n', encoding='utf-8')
    (out.parent / 'caption_instagram.txt').write_text(meta['caption_instagram'] + '\n', encoding='utf-8')
    print(json.dumps({'title': title, 'hashtags': tags}, ensure_ascii=False))


if __name__ == '__main__':
    main()
