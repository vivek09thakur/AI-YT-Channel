#!/usr/bin/env python3
"""generate_folk.py --topic T --narration work/narration.json --phrases work/phrases.json --kit .github/skills/folk-art-video --slug x
                    [--provider gemini --model ... --notes ... --attempts 3]

Asks the LLM for story.py (+ meta.json) following prompt/CONTRACT_FOLK.md, validates it with folk/check_story.py and feeds the
problems back until it passes. Writes <kit>/stories/<slug>/{story.py, meta.json, phrases.json, narration.json, sheet.jpg, tokens.json}.
Exit 1 only when the model could not produce a passing story (or no LLM could answer)."""
import argparse, json, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from generate_story import DEFAULT_MODEL, call_with_fallback, parse_files, read  # noqa: E402
import check_story  # noqa: E402

REQUIRED = ('meta.json', 'story.py')


def brief(topic, narr, ph, notes):
    rows = '\n'.join(f"{p['i']:3d}  f{p['f0']:5d}-{p['f1']:5d}  {p['text']}" for p in ph['phrases'])
    return (f"TOPIC: {topic}\n\nPHRASES (index, first frame - last frame, text). 30 fps, total_frames = {ph['total_frames']} ({ph['duration']} s). "
            f"Phrase index i can also be used as T.start({{i}}).\n{rows}\n\n"
            + (f"NOTES FROM THE CHANNEL OWNER:\n{notes}\n\n" if notes.strip() else '')
            + 'Write meta.json and story.py for this narration.')


def check_meta(txt):
    try:
        m = json.loads(txt)
    except Exception as e:
        return None, [f'meta.json is not valid JSON: {e}']
    errs = []
    if not isinstance(m, dict) or not str(m.get('title', '')).strip(): errs.append('meta.json needs a non-empty "title"')
    if not str(m.get('description', '')).strip(): errs.append('meta.json needs a non-empty "description"')
    return m, errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True); ap.add_argument('--narration', required=True); ap.add_argument('--phrases', required=True)
    ap.add_argument('--kit', required=True); ap.add_argument('--slug', required=True)
    ap.add_argument('--provider', default='gemini', choices=list(DEFAULT_MODEL)); ap.add_argument('--model', default='')
    ap.add_argument('--notes', default=''); ap.add_argument('--attempts', type=int, default=3); ap.add_argument('--step', type=int, default=15)
    a = ap.parse_args()
    model = a.model or DEFAULT_MODEL[a.provider]
    kit = Path(a.kit).resolve(); narr = json.loads(read(a.narration)); ph = json.loads(read(a.phrases))
    sdir = kit / 'stories' / a.slug; sdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(a.phrases, sdir / 'phrases.json'); shutil.copy(a.narration, sdir / 'narration.json')

    system = read(HERE.parent / 'prompt' / 'CONTRACT_FOLK.md')
    system += '\n```python\n' + read(kit / 'example' / 'story_ramayan.py') + '```\n'
    messages = [{'role': 'user', 'content': brief(a.topic, narr, ph, a.notes)}]
    files = {}; total_in = total_out = 0
    for attempt in range(1, a.attempts + 1):
        print(f'--- attempt {attempt}/{a.attempts} ({a.provider} {model})', flush=True)
        text, usage, used_provider, used_model = call_with_fallback(a.provider, model, system, messages, 16000)
        total_in += usage.get('prompt_tokens') or 0; total_out += usage.get('completion_tokens') or 0
        print(f'    tokens in {usage.get("prompt_tokens")} out {usage.get("completion_tokens")}', flush=True)
        new = parse_files(text); files = {**files, **new}
        errs = [f'missing block for {m}' for m in REQUIRED if m not in files]
        if not new: errs = ['your reply contained no `=== FILE: name ===` blocks; reply with meta.json and story.py only, no prose'] + errs
        meta = None
        if not errs:
            meta, errs = check_meta(files['meta.json'])
            (sdir / 'story.py').write_text(files['story.py'], encoding='utf-8')
            res = check_story.check(sdir / 'story.py', sdir / 'phrases.json', kit, a.step, sdir / 'sheet.jpg')
            for w in res['warnings']: print('    warning:', w, flush=True)
            errs += res['problems']
            if not errs:
                title = ' '.join(str(meta['title']).split())
                (sdir / 'meta.json').write_text(json.dumps({**meta, 'title': title, 'topic': a.topic, 'voice': narr.get('voice'), 'duration': narr['duration'],
                                                            'engine': 'folk-art-video', 'provider': used_provider, 'model': used_model}, indent=1, ensure_ascii=False), encoding='utf-8')
                (sdir / 'tokens.json').write_text(json.dumps({'attempts': attempt, 'input_tokens': total_in, 'output_tokens': total_out}), encoding='utf-8')
                print(f"OK: stories/{a.slug}/story.py passes ({res['frames']} sampled frames). tokens total in {total_in} out {total_out}")
                return
        print('    problems:\n' + '\n'.join(f'      {e[:600]}' for e in errs), flush=True)
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'The validator reported these problems. Fix them and return BOTH files again (meta.json, story.py), each complete inside its own `=== FILE: name ===` block, no prose:\n\n' + '\n'.join(errs)}]
    sys.exit(f'gave up after {a.attempts} attempts; last files are in stories/{a.slug} for inspection')


if __name__ == '__main__':
    main()
