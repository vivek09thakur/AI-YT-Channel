#!/usr/bin/env python3
"""Pick the next topic for the NotebookLM short, looking at what was published before.

usage: pick_topic.py --topics pipeline/notebooklm/topics.json [--genre auto|science|...] [--used nlm.json]
                     [--provider auto --model X] [--topic "override"]

Like pick_story.py / pick_fact.py: the published index (nlm.json from the videos branch, newest first) is shown to an
LLM, which returns one fresh, specific explainer topic in a genre that was not used lately. The reply is checked
(not a repeat or near-repeat of a published title, sensible length, known genre) and retried with the problems
listed, up to --attempts times.

Fallback: when no LLM key is set, or every provider fails, a random unpublished topic from topics.json is used (when a
genre is exhausted the least recently published topic of that genre is reused), so the workflow never stops on the
topic step. --topic skips all of this.

Writes genre / topic / slug / picked to $GITHUB_OUTPUT (when set) and prints them.
"""
import argparse, json, os, random, re, sys, unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

GENRES = ['science', 'technology', 'ai', 'space', 'physics']
STOP = {'the', 'a', 'an', 'of', 'in', 'on', 'to', 'and', 'or', 'is', 'are', 'how', 'why', 'what', 'does', 'do', 'it',
        'its', 'we', 'you', 'your', 'our', 'with', 'for', 'from', 'that', 'this', 'can', 'be'}
SYSTEM = ('You plan topics for a faceless YouTube Shorts channel of 60-second explainers (question hook, clear answer, '
          'one takeaway). Reply with ONE JSON object only, no markdown fences.')
PROMPT = '''Already published (newest first):
{history}

Genres to rotate through: {genres}
{genre}Pick the NEXT topic. Rules:
- Never repeat a published topic, and nothing that is only a rephrasing of one.
- Prefer a genre that has not appeared in the last 3 entries{genre_rule}.
- One specific, verifiable thing that a curious beginner can fully understand in 60 seconds, with a concrete core
  (a mechanism, a number, a comparison). Evergreen, not news; no politics, medical advice or named living people.
- Phrase it as a short explainer title such as "Why ice floats on water" or "How a GPS receiver knows where you are":
  under 70 characters, no quotes, no hashtags, no emojis, no trailing punctuation.

Return JSON: {{"genre": "<one of the genres>", "topic": "<the title>",
"why": "<one line on what makes it surprising or useful>"}}
'''


def slugify(text, limit=40):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    text = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return text[:limit].rstrip('-') or 'topic'


def words(text):
    out = set()
    for w in re.findall(r'[a-z0-9]+', text.lower()):
        if w in STOP:
            continue
        # crude stem so "floats" / "floating" / "floated" meet "float"
        for suffix in ('ing', 'ed', 'es', 's'):
            if w.endswith(suffix) and len(w) - len(suffix) >= 3:
                w = w[:-len(suffix)]
                break
        out.add(w)
    return out


def load_used(path):
    p = Path(path) if path else None
    if not p or not p.exists():
        return []
    try:
        rows = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return [e for e in rows if isinstance(e, dict)]


def history_lines(used, limit=40):
    return [f"- {e.get('date', '')} [{e.get('genre', '')}] {e.get('topic') or e.get('title') or e.get('slug', '')}"
            for e in used[:limit]]


def near_repeat(topic, used):
    mine = words(topic)
    if not mine:
        return ''
    for e in used:
        for key in ('topic', 'title'):
            other = words(str(e.get(key) or ''))
            if other and len(mine & other) / len(mine | other) >= 0.6:
                return str(e.get(key))
    return ''


def check(ans, used, want_genre):
    problems = []
    topic = ' '.join(str(ans.get('topic') or '').split())
    if not topic:
        problems.append('missing topic')
    elif len(topic) > 80:
        problems.append('keep the topic under 70 characters')
    elif re.search(r'[#"`$\\{}\[\]]|[\U0001F300-\U0001FAFF]', topic):
        problems.append('plain words only in the topic: no quotes, hashtags, brackets, braces, $, backslashes or emojis')
    if topic and slugify(topic) in {e.get('slug', '') for e in used}:
        problems.append(f'"{topic}" was published already')
    elif topic:
        dup = near_repeat(topic, used)
        if dup:
            problems.append(f'"{topic}" is too close to the published "{dup}"')
    genre = str(ans.get('genre') or '').strip().lower()
    if genre not in GENRES:
        problems.append(f'genre must be one of {", ".join(GENRES)}')
    elif want_genre and genre != want_genre:
        problems.append(f'genre must be {want_genre}')
    return problems


def pick_with_llm(used, want_genre, provider, model, attempts):
    try:
        from generate_story import DEFAULT_MODEL, KEY_ENV, call_with_fallback
        from make_meta import parse_answer
    except ImportError as e:
        print(f'LLM picker unavailable ({e}); using topics.json', file=sys.stderr)
        return None
    if not any(os.environ.get(v) for v in KEY_ENV.values()):
        print('no LLM key secret is set; using topics.json', file=sys.stderr)
        return None
    provider = 'gemini' if provider in ('', 'auto') else provider
    model = model or DEFAULT_MODEL.get(provider, '')
    prompt = PROMPT.format(history='\n'.join(history_lines(used)) or '- (nothing yet - this is the first short)',
                           genres=', '.join(GENRES),
                           genre=f'Requested genre for this one: {want_genre}\n' if want_genre else '',
                           genre_rule=f' (overridden: use {want_genre})' if want_genre else '')
    messages = [{'role': 'user', 'content': prompt}]
    for i in range(1, attempts + 1):
        try:
            text, _usage, p, m = call_with_fallback(provider, model, SYSTEM, messages, 600)
        except SystemExit as e:
            print(f'LLM topic pick failed: {e}', file=sys.stderr)
            return None
        ans = parse_answer(text)
        problems = check(ans, used, want_genre) if ans else ['reply was not a JSON object']
        if not problems:
            topic = ' '.join(str(ans['topic']).split()).rstrip('.!?')
            print(f'topic picked by {p} {m} (attempt {i}); why: {ans.get("why", "")}')
            return {'genre': str(ans['genre']).strip().lower(), 'topic': topic, 'picked': f'llm {p} {m}'}
        print(f'attempt {i}: ' + '; '.join(problems), file=sys.stderr)
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'Fix these and return the full JSON again: ' + '; '.join(problems)}]
    print('LLM gave no usable topic; using topics.json', file=sys.stderr)
    return None


def pick_from_list(topics, used, want_genre):
    # newest first in the index -> position = recency rank
    used_rank = {}
    for i, e in enumerate(used):
        used_rank.setdefault(e.get('slug', ''), i)
    genre = want_genre or random.choice(sorted(topics))
    pool = topics[genre]
    fresh = [t for t in pool if slugify(t) not in used_rank]
    if fresh:
        topic = random.choice(fresh)
    else:
        topic = max(pool, key=lambda t: used_rank.get(slugify(t), -1))
        print(f'all {genre} topics published already; reusing oldest')
    return {'genre': genre, 'topic': topic, 'picked': 'list topics.json'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', required=True)
    ap.add_argument('--genre', default='auto')
    ap.add_argument('--used', default='')
    ap.add_argument('--provider', default='auto')
    ap.add_argument('--model', default='')
    ap.add_argument('--topic', default='')
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()

    topics = json.loads(Path(a.topics).read_text(encoding='utf-8'))
    want_genre = a.genre if a.genre in topics else ''
    used = load_used(a.used)

    if a.topic.strip():
        out = {'genre': want_genre or 'custom', 'topic': a.topic.strip(), 'picked': 'override'}
    else:
        out = pick_with_llm(used, want_genre, a.provider, a.model, a.attempts) or pick_from_list(topics, used, want_genre)

    out['slug'] = slugify(out['topic'])
    for k in ('genre', 'topic', 'slug', 'picked'):
        print(f'{k}: {out[k]}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            for k in ('genre', 'topic', 'slug', 'picked'):
                f.write(f'{k}={out[k]}\n')


if __name__ == '__main__':
    main()
