#!/usr/bin/env python3
"""Pick the next folk-art story and write its 60-80 second narration, looking at what was published before.

usage: pick_story.py --out work [--used site/videos.json] [--provider auto --model X] [--theme "Ramayana"] [--notes "..."]

Reads the videos-branch index (title / topic / date of every published story, newest first) and asks the LLM for the next
subject: always a self-contained episode a first-time viewer can follow (never a saga continuation or a numbered part),
from a tradition not covered lately, told as a cinematic narration of 120-170 words (about 60-80 seconds; the channel's
best-performing Shorts ran 70-90 s). A subject that repeats or nearly repeats a published title is rejected and the LLM is
asked again (pipeline/dedupe.py). Writes <out>/script.txt and <out>/pick.json and puts topic / notes into $GITHUB_OUTPUT.
Exit 1 when no LLM could produce a usable script (nothing to render then).
"""
import argparse, json, os, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / 'notebooklm'))
from generate_story import DEFAULT_MODEL, call_with_fallback  # noqa: E402
from make_meta import parse_answer  # noqa: E402
from dedupe import find_duplicate, load_index  # noqa: E402

WORDS = (120, 170)  # 60-80 s at a cinematic pace; viewers of this channel stay ~25 s, so a shorter video keeps a bigger share
TRADITIONS = ['Ramayana', 'Mahabharata', 'Shiva Purana', 'Devi Bhagavata / Durga', 'Vishnu avatars (Dashavatara)',
              'Krishna and the Bhagavata', 'Ganesha and Kartikeya tales', 'Panchatantra and Jataka fables',
              'Regional folk tales (Bengal, Rajasthan, Kerala, Tamil, Himalayan)', 'Hanuman tales',
              'Rivers, mountains and sacred places (Ganga, Kailash, Varanasi)', 'Festivals and their origin stories']
SYSTEM = ('You are the head writer of a faceless YouTube Shorts channel that tells Indian mythology and folk tales as '
          '60-80 second animated folk-art films. Reply with ONE JSON object only, no markdown fences.')
PROMPT = '''Already published (newest first):
{history}

Traditions to rotate through: {traditions}
{theme}{notes}
Choose the NEXT story. Rules:
- Every video stands alone. Shorts are shown to people who have never seen the channel, so pick ONE self-contained
  episode with a beginning, a turning point and an ending. Never continue a saga, never write a part / chapter / episode
  number, never assume the viewer saw an earlier video, never end with a teaser for the next one.
- Never repeat a published subject, and do not retell a published event from another angle. Do not use the tradition of
  the last two stories. Ramayana, Mahabharata and Krishna episodes may return about twice as often as the other traditions.
- Prefer the moments people wonder and argue about: a mistake, a curse, a boon, a promise, a hidden reason, a little-known
  detail of a famous event. 2-4 characters, visually strong.
- Write the narration: {lo}-{hi} words, present tense, cinematic, short sentences, dramatic pauses with "...", no
  stage directions, no hashtags, no title inside it. Separate paragraphs (scenes) with a blank line; 4-7 paragraphs.
  The first line must make a stranger stay: a question, a contradiction or the stake, not a date or an introduction.
  Close with the moral or the twist.
- Title: under 60 characters, a curiosity hook that still names the character and the event, for example
  "Why Rama's arrow could not kill Ravana" or "The one mistake Ravana made on day one". No "Part", "EP", "Chapter",
  hashtags, emojis or ALL CAPS.

Return JSON: {{"topic": "<title>", "tradition": "<one of the traditions>",
"script": "<narration>", "notes": "<one line for the illustrator: characters with their look and colours, key moments>"}}
'''
SERIAL = re.compile(r'\b(ep|episode|part|chapter|pt)\b\.?\s*[0-9ivx]+|\b[0-9]+\s*(st|nd|rd|th)\s+part\b|:\s*part\b', re.I)
TEASER = re.compile(r'\b(next (part|episode|time|video|chapter)|to be continued|stay tuned|in part [0-9ivx]+)\b', re.I)


def history_lines(used, limit=25):
    return [f"- {e.get('date', '')} {e.get('title') or e.get('topic') or e.get('slug', '')}" for e in used[:limit]]


def check(ans, used=()):
    problems = []
    script = str(ans.get('script') or '').strip()
    n = len(script.split())
    if not (WORDS[0] <= n <= WORDS[1]):
        problems.append(f'script has {n} words, need {WORDS[0]}-{WORDS[1]}')
    if script.count('\n\n') < 3:
        problems.append('split the narration into 4-7 paragraphs separated by blank lines')
    if '#' in script or re.search(r'\[.*?\]|\(.*?\)', script):
        problems.append('no hashtags, brackets or stage directions inside the narration')
    if TEASER.search(script):
        problems.append('the video stands alone: end with the moral or the twist, not a teaser for a next part')
    topic = ' '.join(str(ans.get('topic') or '').split())
    if not topic:
        problems.append('missing topic')
    else:
        if len(topic) > 70:
            problems.append('title too long, keep it under 60 characters')
        if '#' in topic or SERIAL.search(topic):
            problems.append('title must not carry a part / episode / chapter number or hashtags; every video stands alone')
        dup = find_duplicate(used, topic, topic)
        if dup:
            problems.append(f'already on the channel: {dup}; choose a different subject')
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--used', default='')
    ap.add_argument('--provider', default='auto')
    ap.add_argument('--model', default='')
    ap.add_argument('--theme', default='', help='steer the pick toward a tradition or a subject, e.g. "Ramayana" or "Hanuman"')
    ap.add_argument('--notes', default='')
    ap.add_argument('--attempts', type=int, default=5)
    a = ap.parse_args()

    used = load_index(a.used)
    history = history_lines(used)
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
        problems = check(ans, used) if ans else ['reply was not a JSON object']
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
    pick = {'topic': topic, 'tradition': ans.get('tradition', ''), 'notes': notes,
            'words': len(script.split()), 'provider': p, 'model': m, 'previous': len(history)}
    (out / 'pick.json').write_text(json.dumps(pick, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(pick, ensure_ascii=False))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'topic={topic}\nnotes={notes}\n')


if __name__ == '__main__':
    main()
