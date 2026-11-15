#!/usr/bin/env python3
"""Topic + timed narration -> story code (story.js, sound_score.js, lines.js, meta.txt) via an LLM, validated by
building the pages and running headless-Chrome frame tests; errors are fed back for up to --attempts rounds.

    python pipeline/generate_story.py --topic "Shiva: the Neelkanth" --narration work/narration.json \
        --kit .github/skills/shorts-story-video/shadow-puppet-kit --slug shiva-neelkanth --provider openai

Env: OPENAI_API_KEY or ANTHROPIC_API_KEY (per --provider). Prints token usage per call.
"""
import argparse, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

try:
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass
import requests

HERE = Path(__file__).parent
DEFAULT_MODEL = {'openai': 'gpt-4.1', 'anthropic': 'claude-sonnet-4-20250514'}
FILE_RE = re.compile(r'^=== FILE: (\S+) ===\s*$', re.M)


def read(p):
    return Path(p).read_text(encoding='utf-8-sig')


def js_str(s):
    return json.dumps(s, ensure_ascii=False)


# ---------------------------------------------------------------- LLM
def call_llm(provider, model, system, messages, max_tokens):
    """messages: [{'role': 'user'|'assistant', 'content': str}] -> (text, usage dict)."""
    for attempt in range(4):
        try:
            if provider == 'openai':
                r = requests.post('https://api.openai.com/v1/chat/completions', timeout=600,
                                  headers={'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'},
                                  json={'model': model, 'temperature': 0.4, 'max_tokens': max_tokens,
                                        'messages': [{'role': 'system', 'content': system}] + messages})
                r.raise_for_status(); j = r.json()
                return j['choices'][0]['message']['content'], j.get('usage', {})
            if provider == 'anthropic':
                r = requests.post('https://api.anthropic.com/v1/messages', timeout=600,
                                  headers={'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01'},
                                  json={'model': model, 'max_tokens': max_tokens, 'temperature': 0.4, 'system': system, 'messages': messages})
                r.raise_for_status(); j = r.json()
                u = j.get('usage', {})
                return ''.join(b.get('text', '') for b in j['content']), {'prompt_tokens': u.get('input_tokens'), 'completion_tokens': u.get('output_tokens')}
            sys.exit(f'unknown provider {provider}')
        except requests.HTTPError as e:
            body = e.response.text[:500]
            if e.response.status_code in (429, 500, 502, 503, 529) and attempt < 3:
                wait = 20 * (attempt + 1); print(f'  {e.response.status_code}, retry in {wait}s: {body}', file=sys.stderr); time.sleep(wait); continue
            sys.exit(f'LLM error {e.response.status_code}: {body}')
        except requests.RequestException as e:
            if attempt < 3:
                time.sleep(15); continue
            sys.exit(f'LLM request failed: {e}')


def parse_files(text):
    parts = FILE_RE.split(text)
    files = {}
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip('\n')
        body = re.sub(r'^```[a-zA-Z]*\n', '', body); body = re.sub(r'\n```\s*$', '', body)
        files[parts[i]] = body + '\n'
    return files


# ---------------------------------------------------------------- kit side
def write_lines_js(narr, kinds, path):
    dur = round(narr['duration'], 2)
    rows = []
    for L in narr['lines']:
        k = kinds.get(str(L['i']))
        rows.append(f"    [{L['t0']}, {js_str(L['text'])}, {js_str(k) if k else 'null'}, {L['t1']}],")
    path.write_text('  // generated from the voice track: [start, text, kind, end]\n'
                    f'  const DURATION = {dur};\n  const LINES = [\n' + '\n'.join(rows) + '\n  ];\n', encoding='utf-8')


def run(cmd, cwd, env=None, timeout=900):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def validate(kit, slug, duration):
    """Build both pages and probe frames across the timeline in both layouts. Returns '' or an error report."""
    report = []
    for what in ('player', 'vertical'):
        rc, out = run([sys.executable, 'build.py', what, slug], kit)
        if rc:
            report.append(f'build {what} failed:\n{out[-2000:]}')
    if report:
        return '\n'.join(report)
    n = 14
    probes = [round(duration * (i + 0.5) / n, 2) for i in range(n)]
    for vertical in (False, True):
        env = {'STORY': slug}
        if vertical:
            env['VERTICAL'] = '1'
        rc, out = run(['node', 'render.mjs', 'test', *map(str, probes if not vertical else probes[::3])], kit, env)
        m = re.search(r'errors (\[.*\])\s*$', out, re.S)
        errs = []
        if m:
            try:
                errs = json.loads(m.group(1))
            except json.JSONDecodeError:
                errs = [m.group(1)[:1500]]
        if rc or not m or errs:
            tail = out[-2500:] if (rc or not m) else ''
            report.append(f'{"9:16 reel" if vertical else "16:9 stage"} test: exit {rc}\n' + '\n'.join(f'- {e}' for e in dict.fromkeys(errs)) + ('\n' + tail if tail else ''))
        else:
            slow = re.search(r'frame ms (\[.*?\])', out)
            if slow:
                ms = json.loads(slow.group(1)); worst = max(ms, key=lambda x: x[1])
                if worst[1] > 400:
                    report.append(f'frame at t={worst[0]} took {worst[1]} ms (limit 400 ms): simplify that scene (fewer loops/objects).')
    return '\n\n'.join(report)


def check_contract(files, narr):
    """Cheap static checks before spending a browser round."""
    errs = []
    s = files.get('story.js', '')
    for name in ('const TITLE', 'const HOOK', 'const SC', 'const FADE', 'const BEATS', 'const SCENES'):
        if name not in s:
            errs.append(f'story.js must define {name}')
    for bad in ('const DURATION', 'const LINES', 'function lineAt', 'function drawLines', 'function stageFrame', 'function explainerFrame', 'function reelFrame', 'const pop ', 'const fade ', 'function cam(', 'const WARM', 'const DUSK', 'const NIGHT', 'const stars'):
        if bad in s:
            errs.append(f'story.js must NOT define {bad.strip()} (already provided by the shared layer)')
    if 'function scoreSound' not in files.get('sound_score.js', ''):
        errs.append('sound_score.js must define function scoreSound(k0)')
    n = len(narr['lines'])
    seen = set()
    for m in re.finditer(r'(?:LINES\[|lineT\(\s*)(\d+)', s + files.get('sound_score.js', '')):
        idx = int(m.group(1))
        if idx >= n and idx not in seen:
            seen.add(idx)
            errs.append(f'line index {idx} does not exist (there are {n} lines, indices 0..{n - 1})')
    try:
        meta = json.loads(files.get('meta.json', '{}'))
        if not meta.get('title'):
            errs.append('meta.json needs a title')
        for k, v in (meta.get('kinds') or {}).items():
            if not k.isdigit() or int(k) >= n or v not in ('big', 'title', 'tag'):
                errs.append(f'meta.json kinds: bad entry {k!r}: {v!r}')
    except json.JSONDecodeError as e:
        errs.append(f'meta.json is not valid JSON: {e}')
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--narration', required=True)
    ap.add_argument('--kit', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--provider', default='openai', choices=['openai', 'anthropic'])
    ap.add_argument('--model', default='')
    ap.add_argument('--notes', default='', help='extra style/story notes from the user')
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()
    model = a.model or DEFAULT_MODEL[a.provider]
    kit = Path(a.kit).resolve()
    narr = json.loads(read(a.narration))
    sdir = kit / 'stories' / a.slug
    sdir.mkdir(parents=True, exist_ok=True)

    ex = kit / 'stories' / 'ramayan'
    system = read(HERE / 'prompt' / 'CONTRACT.md')
    system += '\n\n## ref.js (drawing helpers, available to you)\n```js\n' + read(kit / 'stories' / '_shared' / 'ref.js') + '```\n'
    system += '\n## narration.js (shared layer, available to you; do not redefine)\n```js\n' + read(kit / 'stories' / '_shared' / 'narration.js') + '```\n'
    system += '\n## EXAMPLE story.js (Ramayan trailer; copy its structure and quality)\n```js\n' + read(ex / 'story.js') + '```\n'
    system += '\n## EXAMPLE sound_score.js\n```js\n' + read(ex / 'sound_score.js') + '```\n'

    narr_txt = '\n'.join(f"{L['i']:3d}  {L['t0']:7.2f} - {L['t1']:7.2f}  {L['text']}" for L in narr['lines'])
    user = (f"TOPIC: {a.topic}\n\nNARRATION (index, start s, end s, text). DURATION = {narr['duration']} s.\n{narr_txt}\n\n"
            + (f"NOTES FROM THE CHANNEL OWNER:\n{a.notes}\n\n" if a.notes.strip() else '')
            + 'Write meta.json, story.js and sound_score.js for this narration.')
    messages = [{'role': 'user', 'content': user}]
    total_in = total_out = 0
    for attempt in range(1, a.attempts + 1):
        print(f'--- attempt {attempt}/{a.attempts} ({a.provider} {model})')
        text, usage = call_llm(a.provider, model, system, messages, 24000 if a.provider == 'anthropic' else 16000)
        total_in += usage.get('prompt_tokens') or 0; total_out += usage.get('completion_tokens') or 0
        print(f'    tokens in {usage.get("prompt_tokens")} out {usage.get("completion_tokens")}')
        files = parse_files(text)
        missing = [f for f in ('meta.json', 'story.js', 'sound_score.js') if f not in files]
        errs = [f'missing block for {m}' for m in missing] or check_contract(files, narr)
        if not errs:
            meta = json.loads(files['meta.json'])
            (sdir / 'story.js').write_text(files['story.js'], encoding='utf-8')
            (sdir / 'sound_score.js').write_text(files['sound_score.js'], encoding='utf-8')
            write_lines_js(narr, meta.get('kinds') or {}, sdir / 'lines.js')
            (sdir / 'meta.txt').write_text(f"title={meta['title']}\nparts=ref,lines,narration,story,sound_score,vertical\n", encoding='utf-8')
            (sdir / 'meta.json').write_text(json.dumps({**meta, 'topic': a.topic, 'voice': narr.get('voice'), 'duration': narr['duration'], 'provider': a.provider, 'model': model}, indent=1, ensure_ascii=False), encoding='utf-8')
            report = validate(kit, a.slug, narr['duration'])
            if not report:
                print(f'OK: stories/{a.slug} builds and renders without errors. tokens total in {total_in} out {total_out}')
                (sdir / 'tokens.json').write_text(json.dumps({'attempts': attempt, 'input_tokens': total_in, 'output_tokens': total_out}), encoding='utf-8')
                return
            errs = [report]
        print('    problems:\n' + '\n'.join(f'      {e[:400]}' for e in errs))
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'The build/test reported these problems. Return all three files again, complete and corrected:\n\n' + '\n'.join(errs)}]
    sys.exit(f'gave up after {a.attempts} attempts; last files are in stories/{a.slug} for inspection')


if __name__ == '__main__':
    main()
