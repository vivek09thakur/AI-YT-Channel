#!/usr/bin/env python3
"""Pick the next folk-art story and write its 2-minute narration, looking at what was published before.

usage: pick_story.py --out work [--used site/videos.json] [--provider auto --model X] [--theme "Ramayana"] [--notes "..."]

Reads the videos-branch index (title / topic / date of every published story, newest first), asks the LLM for the next
subject - continue the same saga when the last stories form a sequence, otherwise move to a tradition that has not been
covered lately - and for a cinematic narration of about 2 minutes. Writes <out>/script.txt and <out>/pick.json and puts
topic / notes into $GITHUB_OUTPUT. Exit 1 when no LLM could produce a usable script (nothing to render then).
"""
import argparse, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'notebooklm'))
from generate_story import DEFAULT_MODEL, call_with_fallback  # noqa: E402
from make_meta import parse_answer  # noqa: E402

WORDS = (230, 320)  # ~2 minutes at a cinematic pace
TRADITIONS = ['Ramayana', 'Mahabharata', 'Shiva Purana', 'Devi Bhagavata / Durga', 'Vishnu avatars (Dashavatara)',
              'Krishna and the Bhagavata', 'Ganesha and Kartikeya tales', 'Panchatantra and Jataka fables',
              'Regional folk tales (Bengal, Rajasthan, Kerala, Tamil, Himalayan)', 'Hanuman tales',
              'Rivers, mountains and sacred places (Ganga, Kailash, Varanasi)', 'Festivals and their origin stories']
SYSTEM = ('You are the head writer of a faceless YouTube channel that tells Indian mythology and folk tales as 2-minute '
          'animated folk-art films. Reply with ONE JSON object only, no markdown fences.')
PROMPT = '''Already published (newest first):
{history}

Traditions to rotate through: {traditions}
{theme}{notes}
Choose the NEXT story. Rules:
- Never repeat a published subject. If the last one or two stories clearly form a sequence (same saga, numbered parts or
  "what happened next"), continue with the next natural episode of that saga. Otherwise pick a tradition that has not
  appeared recently and choose one self-contained, visually strong episode with 2-4 characters.
- Write the narration: {lo}-{hi} words, present tense, cinematic, short sentences, dramatic pauses with "...", no
  stage directions, no hashtags, no title inside it. Separate paragraphs (scenes) with a blank line; 6-10 paragraphs.
  Open with a hook line, close with the moral or the hint of what comes next.
- Title: under 70 characters, searchable (name the character and the event).

Return JSON: {{"topic": "<title>", "tradition": "<one of the traditions>", "series": "<saga name and part number, or empty>",
"script": "<narration>", "notes": "<one line for the illustrator: characters with their look and colours, key moments>"}}
'''


def load_history(path, limit=25):
    p = Path(path) if path else None
    if not p or not p.exists():
        return []
    try:
        rows = json.loads(p.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return [f"- {e.get('date', '')} {e.get('title') or e.get('topic') or e.get('slug', '')}" for e in rows[:limit] if isinstance(e, dict)]


def check(ans):
    problems = []
    script = str(ans.get('script') or '').strip()
    n = len(script.split())
    if not (WORDS[0] <= n <= WORDS[1]):
        problems.append(f'script has {n} words, need {WORDS[0]}-{WORDS[1]}')
    if script.count('\n\n') < 3:
        problems.append('split the narration into 6-10 paragraphs separated by blank lines')
    if '#' in script or re.search(r'\[.*?\]|\(.*?\)', script):
        problems.append('no hashtags, brackets or stage directions inside the narration')
    if not str(ans.get('topic') or '').strip():
        problems.append('missing topic')
    elif len(ans['topic']) > 90:
        problems.append('title too long')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--used', default='')
    ap.add_argument('--provider', default='auto')
    ap.add_argument('--model', default='')
    ap.add_argument('--theme', default='', help='force a tradition / saga, e.g. "Ramayana" or "continue the Sati saga"')
    ap.add_argument('--notes', default='')
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()

    history = load_history(a.used)
    provider = 'gemini' if a.provider in ('', 'auto') else a.provider
    model = a.model or DEFAULT_MODEL.get(provider, '')
    prompt = PROMPT.format(history='\n'.join(history) or '- (nothing yet - this is the first story)',
                           traditions=', '.join(TRADITIONS),
                           theme=f'Requested theme for this one: {a.theme}\n' if a.theme else '',
                           notes=f'Extra notes: {a.notes}\n' if a.notes else '', lo=WORDS[0], hi=WORDS[1])
    messages = [{'role': 'user', 'content': prompt}]
    ans = {}
    for i in range(1, a.attempts + 1):
        text, _usage, p, m = call_with_fallback(provider, model, SYSTEM, messages, 2500)
        ans = parse_answer(text)
        problems = check(ans) if ans else ['reply was not a JSON object']
        if not problems:
            print(f'story picked by {p} {m} (attempt {i})')
            break
        print(f'attempt {i}: ' + '; '.join(problems), file=sys.stderr)
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'Fix these and return the full JSON again: ' + '; '.join(problems)}]
    else:
        sys.exit('::error::could not get a usable story script from the LLM')

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    script = str(ans['script']).strip() + '\n'
    (out / 'script.txt').write_text(script, encoding='utf-8')
    topic = ' '.join(str(ans['topic']).split())
    notes = ' '.join(str(ans.get('notes') or '').split())
    pick = {'topic': topic, 'tradition': ans.get('tradition', ''), 'series': ans.get('series', ''), 'notes': notes,
            'words': len(script.split()), 'provider': p, 'model': m, 'previous': len(history)}
    (out / 'pick.json').write_text(json.dumps(pick, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(pick, ensure_ascii=False))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'topic={topic}\nnotes={notes}\n')


if __name__ == '__main__':
    main()
