#!/usr/bin/env python3
"""Pick the next fact for the stickman reel and write its narration, looking at what was published before.

usage: pick_fact.py --out work [--used site/stickman.json] [--provider auto --model X] [--theme "space"] [--notes "..."]

Reads the videos-branch index stickman.json (title / topic / date of every published reel, newest first), asks the LLM for a
fresh surprising fact (rotating through categories) and a 30-45 s narration in the fixed shape
  hook question -> the answer right away -> 2-4 explanation lines -> subscribe / follow line.
Writes <out>/script.txt and <out>/pick.json and puts topic / fact / notes into $GITHUB_OUTPUT.
Exit 1 when no LLM could produce a usable script (nothing to render then).
"""
import argparse, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'notebooklm'))
from generate_story import DEFAULT_MODEL, call_with_fallback  # noqa: E402
from make_meta import parse_answer  # noqa: E402

WORDS = (70, 120)  # ~30-45 s at a brisk pace
CATEGORIES = ['space and planets', 'human body', 'animals', 'oceans and weather', 'world geography', 'history',
              'inventions and technology', 'food and everyday things', 'maths and numbers', 'language and words',
              'sports records', 'art, music and movies', 'India (places, records, culture)']
SYSTEM = ('You write 30-45 second "did you know" fact reels for a faceless channel with stick-figure animation. '
          'Reply with ONE JSON object only, no markdown fences.')
PROMPT = '''Already published (newest first):
{history}

Categories to rotate through: {categories}
{theme}{notes}
Pick the NEXT fact. Rules:
- Never repeat a published fact or topic. Prefer a category that has not appeared in the last 5 entries.
- ONE surprising, verifiable, true fact with a concrete core (a number, a name, a place, a comparison).
- Write the narration as plain paragraphs separated by blank lines, in exactly this order:
  1. hook question, one sentence ending with "?" (e.g. "Did you know which planet spins backwards?")
  2. the answer right away, one short sentence ending with "!" (e.g. "It's Venus!")
  3. two to four explanation lines (one sentence each, present tense, concrete numbers or everyday comparisons)
  4. the closing line: "If you like knowing facts like this, subscribe and follow for more."
- {lo}-{hi} words in total. No hashtags, no emojis, no brackets, no stage directions, no title, no "[pause]".
- Title: under 60 characters, phrased as the question or "Did you know ..." so it is searchable.

Return JSON: {{"topic": "<title>", "category": "<one of the categories>", "question": "<the hook question>",
"fact": "<the answer in 3-8 words>", "script": "<narration>",
"notes": "<one line for the illustrator: the objects, places, numbers and comparisons to draw>"}}
'''


def load_history(path, limit=30):
    p = Path(path) if path else None
    if not p or not p.exists():
        return []
    try:
        rows = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return [f"- {e.get('date', '')} [{e.get('category', '')}] {e.get('title') or e.get('topic') or e.get('slug', '')} -> {e.get('fact') or e.get('answer', '')}"
            for e in rows[:limit] if isinstance(e, dict)]


def check(ans):
    problems = []
    script = str(ans.get('script') or '').strip()
    paras = [p.strip() for p in re.split(r'\n\s*\n', script) if p.strip()]
    n = len(script.split())
    if not (WORDS[0] <= n <= WORDS[1]):
        problems.append(f'script has {n} words, need {WORDS[0]}-{WORDS[1]}')
    if len(paras) < 5:
        problems.append('need 5-7 paragraphs: hook question, answer, 2-4 explanation lines, subscribe/follow line')
    else:
        if not paras[0].rstrip().endswith('?'):
            problems.append('the first paragraph must be the hook question and end with "?"')
        if not re.search(r'subscribe|follow', paras[-1], re.I):
            problems.append('the last paragraph must ask to subscribe and follow')
    if '#' in script or re.search(r'\[.*?\]|\(.*?\)', script):
        problems.append('no hashtags, brackets or stage directions inside the narration')
    if not str(ans.get('topic') or '').strip():
        problems.append('missing topic')
    elif len(ans['topic']) > 80:
        problems.append('title too long')
    if not str(ans.get('fact') or '').strip():
        problems.append('missing fact')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--used', default='')
    ap.add_argument('--provider', default='auto')
    ap.add_argument('--model', default='')
    ap.add_argument('--theme', default='', help='force a category / subject, e.g. "space" or "Indian history"')
    ap.add_argument('--notes', default='')
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()

    history = load_history(a.used)
    provider = 'gemini' if a.provider in ('', 'auto') else a.provider
    model = a.model or DEFAULT_MODEL.get(provider, '')
    prompt = PROMPT.format(history='\n'.join(history) or '- (nothing yet - this is the first fact)',
                           categories=', '.join(CATEGORIES),
                           theme=f'Requested theme for this one: {a.theme}\n' if a.theme else '',
                           notes=f'Extra notes: {a.notes}\n' if a.notes else '', lo=WORDS[0], hi=WORDS[1])
    messages = [{'role': 'user', 'content': prompt}]
    ans = {}
    for i in range(1, a.attempts + 1):
        text, _usage, p, m = call_with_fallback(provider, model, SYSTEM, messages, 1500)
        ans = parse_answer(text)
        problems = check(ans) if ans else ['reply was not a JSON object']
        if not problems:
            print(f'fact picked by {p} {m} (attempt {i})')
            break
        print(f'attempt {i}: ' + '; '.join(problems), file=sys.stderr)
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'Fix these and return the full JSON again: ' + '; '.join(problems)}]
    else:
        sys.exit('::error::could not get a usable fact script from the LLM')

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    script = str(ans['script']).strip() + '\n'
    (out / 'script.txt').write_text(script, encoding='utf-8')
    topic = ' '.join(str(ans['topic']).split())
    fact = ' '.join(str(ans['fact']).split())
    notes = ' '.join(str(ans.get('notes') or '').split())
    notes = f"Fact: {fact}. {notes}".strip()
    pick = {'topic': topic, 'category': ans.get('category', ''), 'question': ans.get('question', ''), 'fact': fact,
            'notes': notes, 'words': len(script.split()), 'provider': p, 'model': m, 'previous': len(history)}
    (out / 'pick.json').write_text(json.dumps(pick, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(pick, ensure_ascii=False))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'topic={topic}\nfact={fact}\nnotes={notes}\n')


if __name__ == '__main__':
    main()
