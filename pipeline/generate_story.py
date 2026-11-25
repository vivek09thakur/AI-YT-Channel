#!/usr/bin/env python3
import argparse, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

try:
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass
import requests

HERE = Path(__file__).parent
DEFAULT_MODEL = {
    'gemini': 'gemini-3.8-flash',
    'mistral': 'mistral-large-latest',
    'cerebras': 'qwen-3-coder-480b',
    'meta': 'muse-spark-1.3',
    'openrouter': 'anthropic/claude-sonnet-4',
    'openai': 'gpt-4.1',
    'anthropic': 'claude-sonnet-4-20250514',
}

OPENAI_COMPAT = {
    'gemini': ('https://generativelanguage.googleapis.com/v1beta/openai/chat/completions', 'GEMINI_API_KEY', {}),
    'mistral': ('https://api.mistral.ai/v1/chat/completions', 'MISTRAL_API_KEY', {}),
    'cerebras': ('https://api.cerebras.ai/v1/chat/completions', 'CEREBRAS_API_KEY', {}),
    'meta': ('https://api.meta.ai/v1/chat/completions', 'META_AI_API', {}),
    'openai': ('https://api.openai.com/v1/chat/completions', 'OPENAI_API_KEY', {}),
    'openrouter': ('https://openrouter.ai/api/v1/chat/completions', 'OPENROUTER_API_KEY',
                   {'HTTP-Referer': 'https://github.com/vivek09thakur/AI-YT-Channel', 'X-Title': 'AI-YT-Channel'}),
}
NO_RETRY = ('insufficient_quota', 'credit_balance_exhausted', 'billing', 'invalid_api_key', 'Insufficient credits',
            'API_KEY_INVALID', 'PERMISSION_DENIED')
PRIORITY = ['gemini', 'mistral', 'cerebras', 'meta', 'openrouter', 'openai', 'anthropic']
FALLBACK_MODELS = {
    # gemini-3.7-flash routes to 3.8-flash (same quota) and 2.5-flash is retired for new users -> only distinct models listed
    'gemini': ['gemini-3.8-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite'],
    'cerebras': ['qwen-3-coder-480b', 'qwen-3-235b-a22b-instruct-2507', 'gpt-oss-120b', 'llama-3.3-70b'],
    'meta': ['muse-spark-1.3', 'muse-wonder-1.0', 'muse-ember-1.0'],
}
# Reasoning models: thinking tokens count against max_tokens and temperature is not a supported knob.
REASONING_BODY = {'meta': {'reasoning_effort': 'low'}}
KEY_ENV = {p: OPENAI_COMPAT[p][1] for p in OPENAI_COMPAT} | {'anthropic': 'ANTHROPIC_API_KEY'}
RETRY_WAITS = (15, 30, 45)  # per model; a 503 storm then costs 1.5 min before the next fallback model is tried
# seconds to wait for the model's reply (per request); small text jobs set LLM_TIMEOUT=120 so a stalled stream fails fast
LLM_TIMEOUT = int(os.environ.get('LLM_TIMEOUT', '600'))


class Unavailable(Exception):
    pass


FILE_RE = re.compile(r'^=== FILE: (\S+) ===\s*$', re.M)


def read(p):
    return Path(p).read_text(encoding='utf-8-sig')


def js_str(s):
    return json.dumps(s, ensure_ascii=False)

GEMINI_BASE = 'https://generativelanguage.googleapis.com/v1beta'


def call_gemini(model, system, messages, max_tokens):
    key = os.environ.get('GEMINI_API_KEY')
    if not key:
        raise Unavailable('GEMINI_API_KEY is not set')
    contents = [{'role': 'model' if m['role'] == 'assistant' else 'user', 'parts': [{'text': m['content']}]} for m in messages]

    body = {'system_instruction': {'parts': [{'text': system}]}, 'contents': contents,
            'generationConfig': {'maxOutputTokens': max_tokens + 8000, 'thinkingConfig': {'thinkingLevel': 'low'}}}
    url = f'{GEMINI_BASE}/models/{model}:streamGenerateContent?alt=sse'
    for cfg in (body, {**body, 'generationConfig': {'maxOutputTokens': max_tokens + 8000}}):
        r = requests.post(url, timeout=(30, LLM_TIMEOUT), headers={'x-goog-api-key': key}, json=cfg, stream=True)
        if r.status_code == 400 and 'thinking' in r.text.lower() and cfg is body:
            continue
        r.raise_for_status()
        text, usage, finish = [], {}, None
        for line in r.iter_lines(decode_unicode=True):
            if not line or not line.startswith('data:'):
                continue
            chunk = json.loads(line[5:].strip())
            for cand in chunk.get('candidates', []):
                finish = cand.get('finishReason', finish)
                for part in cand.get('content', {}).get('parts', []):
                    if part.get('text') and not part.get('thought'):
                        text.append(part['text'])
            if 'usageMetadata' in chunk:
                u = chunk['usageMetadata']
                usage = {'prompt_tokens': u.get('promptTokenCount'), 'completion_tokens': u.get('candidatesTokenCount'),
                         'thinking_tokens': u.get('thoughtsTokenCount')}
        if finish is None:
            raise Unavailable('Gemini stream ended without a finishReason (connection dropped mid-answer)')
        if finish not in ('STOP', 'MAX_TOKENS'):
            raise Unavailable(f'Gemini stopped with finishReason={finish}')
        return ''.join(text), usage
    raise RuntimeError('unreachable')


def call_llm(provider, model, system, messages, max_tokens):
    for attempt in range(len(RETRY_WAITS) + 1):
        try:
            if provider == 'gemini':
                return call_gemini(model, system, messages, max_tokens)
            if provider in OPENAI_COMPAT:
                url, key, extra = OPENAI_COMPAT[provider]
                if not os.environ.get(key):
                    raise Unavailable(f'{key} is not set')
                body = {'model': model, 'max_tokens': max_tokens, 'messages': [{'role': 'system', 'content': system}] + messages}
                if provider in REASONING_BODY:
                    body.update(REASONING_BODY[provider]); body['max_tokens'] = max_tokens * 2
                else:
                    body['temperature'] = 0.4
                r = requests.post(url, timeout=LLM_TIMEOUT,
                                  headers={'Authorization': f'Bearer {os.environ[key]}', **extra}, json=body)
                r.raise_for_status(); j = r.json()
                if 'error' in j:
                    raise Unavailable(f'LLM error: {json.dumps(j["error"])[:500]}')
                return j['choices'][0]['message']['content'], j.get('usage', {})
            if provider == 'anthropic':
                if not os.environ.get('ANTHROPIC_API_KEY'):
                    raise Unavailable('ANTHROPIC_API_KEY is not set')
                r = requests.post('https://api.anthropic.com/v1/messages', timeout=LLM_TIMEOUT,
                                  headers={'x-api-key': os.environ['ANTHROPIC_API_KEY'], 'anthropic-version': '2023-06-01'},
                                  json={'model': model, 'max_tokens': max_tokens, 'temperature': 0.4, 'system': system, 'messages': messages})
                r.raise_for_status(); j = r.json()
                u = j.get('usage', {})
                return ''.join(b.get('text', '') for b in j['content']), {'prompt_tokens': u.get('input_tokens'), 'completion_tokens': u.get('output_tokens')}
            raise Unavailable(f'unknown provider {provider}')
        except requests.HTTPError as e:
            body = e.response.text[:500]
            retryable = e.response.status_code in (429, 500, 502, 503, 529) and not any(k in body for k in NO_RETRY)
            if retryable and attempt < len(RETRY_WAITS):
                wait = RETRY_WAITS[attempt]; print(f'  {e.response.status_code}, retry in {wait}s: {body}', file=sys.stderr); time.sleep(wait); continue
            raise Unavailable(f'LLM error {e.response.status_code}: {body}')
        except requests.RequestException as e:
            if attempt < len(RETRY_WAITS):
                time.sleep(15); continue
            raise Unavailable(f'LLM request failed: {e}')


DEAD = set()  # (provider, model) that returned quota-exhausted / not-found in this process; skipped on later attempts
DEAD_MARKS = ('404', 'no longer available', 'quota', 'billing', 'credit', 'resource_exhausted', 'not_found')


def candidates(provider, model):
    seen, out = set(), []
    def add(p, m):
        if (p, m) not in seen and (p, m) not in DEAD and os.environ.get(KEY_ENV.get(p, '')):
            seen.add((p, m)); out.append((p, m))
    add(provider, model)
    for m in FALLBACK_MODELS.get(provider, []):
        add(provider, m)
    for p in PRIORITY:
        if p != provider:
            add(p, DEFAULT_MODEL[p])
    return out


def call_with_fallback(provider, model, system, messages, max_tokens):
    errors = []
    for p, m in candidates(provider, model):
        if (p, m) != (provider, model):
            print(f'--- falling back to {p} {m}')
        try:
            text, usage = call_llm(p, m, system, messages, 24000 if p == 'anthropic' else max_tokens)
            return text, usage, p, m
        except Unavailable as e:
            msg = str(e)
            if any(k in msg.lower() for k in DEAD_MARKS):
                DEAD.add((p, m))
            print(f'    {p} {m} unavailable: {msg[:300]}', file=sys.stderr); errors.append(f'{p} {m}: {msg[:200]}')
    sys.exit('no LLM could answer:\n  ' + '\n  '.join(errors))


def parse_files(text):
    parts = FILE_RE.split(text)
    files = {}
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1].strip('\n')
        body = re.sub(r'^```[a-zA-Z]*\n', '', body); body = re.sub(r'\n```\s*$', '', body)
        files[parts[i]] = body + '\n'
    return files


def write_lines_js(narr, kinds, path):
    dur = round(narr['duration'], 2)
    rows = []
    for L in narr['lines']:
        k = kinds.get(str(L['i']))
        rows.append(f"    [{L['t0']}, {js_str(L['text'])}, {js_str(k) if k else 'null'}, {L['t1']}],")
    path.write_text(f'  const DURATION = {dur};\n  const LINES = [\n' + '\n'.join(rows) + '\n  ];\n', encoding='utf-8')


def run(cmd, cwd, env=None, timeout=900):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, encoding='utf-8', errors='replace')
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def validate(kit, slug, duration):
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
        found = re.findall(r'errors (\[.*\])\s*$', out, re.M)
        m = found[-1] if found else None
        errs = []
        if m:
            try:
                errs = json.loads(m)
            except json.JSONDecodeError:
                errs = [m[:1500]]
        if rc or not m or errs:
            tail = out[-2500:] if (rc or not m) else ''
            report.append(f'{"9:16 reel" if vertical else "16:9 stage"} test: exit {rc}\n' + '\n'.join(f'- {e}' for e in dict.fromkeys(errs)) + ('\n' + tail if tail else ''))
        else:
            slow = re.search(r'frame ms (\[\[.*?\]\]|\[\])', out)
            if slow:
                ms = json.loads(slow.group(1))
                worst = max(ms[1:], key=lambda x: x[1]) if len(ms) > 1 else None
                if worst and worst[1] > 500:
                    report.append(f'frame at t={worst[0]} took {worst[1]} ms (limit 500 ms): simplify that scene (fewer loops/objects).')
    return '\n\n'.join(report)


def check_contract(files, narr):
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
    errs += check_scenes(s)
    return errs


SUBJECT_CALLS = re.compile(r'\b(figure|ravana|vanara|animal|elephant)\s*\(')


def scene_bodies(s):
    """Yield (name, body) for each `function sceneX(...) { ... }` in story.js (brace matched)."""
    for m in re.finditer(r'function\s+(scene\w*)\s*\([^)]*\)\s*\{', s):
        depth, i = 1, m.end()
        while i < len(s) and depth:
            depth += {'{': 1, '}': -1}.get(s[i], 0)
            i += 1
        yield m.group(1), s[m.start():i]


def check_scenes(s):
    """Every scene must draw a character/subject (last scene may be a title card) and must not bury it under hills."""
    errs = []
    scenes = list(scene_bodies(s))
    # names in SCENES order, so the last one may be exempt
    order = re.findall(r'\[\s*[^,\[\]]+,\s*(scene\w*)\s*\]', s)
    last = order[-1] if order else None
    num = r'(-?\d+(?:\.\d+)?)'
    for name, body in scenes:
        if name == last:
            continue
        subjects = list(SUBJECT_CALLS.finditer(body))
        if not subjects:
            errs.append(f'{name} draws no character or subject: every scene must call figure/ravana/vanara/animal/elephant (only the final title-card scene is exempt)')
            continue
        # feet y of subjects given as numeric literals; hills drawn afterwards may only cover a thin strip at the feet
        feet = []
        for m in subjects:
            tail = body[m.end():m.end() + 400]
            if m.group(1) in ('figure', 'ravana', 'animal'):
                ym = re.search(r'\by\s*:\s*' + num + r'\s*[,}]', tail)
            else:
                ym = re.match(r'\s*c\s*,\s*[^,]+,\s*' + num + r'\s*,', tail)
            if ym and float(ym.group(1)) <= 730:
                feet.append((float(ym.group(1)), m.start()))
        for hm in re.finditer(r'\bhills\s*\(\s*c\s*,\s*W\s*,\s*Hh\s*,\s*' + num + r'\s*,\s*' + num + r'\s*,', body):
            hy, amp = float(hm.group(1)), float(hm.group(2))
            top = hy - amp * 1.3
            buried = [fy for fy, pos in feet if pos < hm.start() and top < fy - 24]
            if buried:
                errs.append(f'{name}: hills(y={hy:g}, amp={amp:g}) is drawn after a character whose feet are at y={min(buried):g}; it climbs to y~{top:g} and hides them. Draw hills before characters, or keep a foreground strip thin (amp <= 16, y >= feet).')
                break
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--narration', required=True)
    ap.add_argument('--kit', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--provider', default='gemini', choices=list(DEFAULT_MODEL))
    ap.add_argument('--model', default='')
    ap.add_argument('--notes', default='', help='extra style/story notes from the user')
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()
    model = a.model or DEFAULT_MODEL[a.provider]
    provider = a.provider
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
    files = {}
    for attempt in range(1, a.attempts + 1):
        print(f'--- attempt {attempt}/{a.attempts} ({provider} {model})')
        # always start from the preferred model: a 503 fallback on one attempt should not downgrade the rest
        text, usage, used_provider, used_model = call_with_fallback(provider, model, system, messages, 16000)
        total_in += usage.get('prompt_tokens') or 0; total_out += usage.get('completion_tokens') or 0
        print(f'    tokens in {usage.get("prompt_tokens")} out {usage.get("completion_tokens")}')
        new = parse_files(text)
        files = {**files, **new}
        missing = [f for f in ('meta.json', 'story.js', 'sound_score.js') if f not in files]
        errs = [f'missing block for {m}' for m in missing] or check_contract(files, narr)
        if not new:
            errs = ['your reply contained no `=== FILE: name ===` blocks; reply with the three files only, no prose'] + errs
        if not errs:
            meta = json.loads(files['meta.json'])
            (sdir / 'story.js').write_text(files['story.js'], encoding='utf-8')
            (sdir / 'sound_score.js').write_text(files['sound_score.js'], encoding='utf-8')
            write_lines_js(narr, meta.get('kinds') or {}, sdir / 'lines.js')
            title = ' '.join(str(meta['title']).split())
            (sdir / 'meta.txt').write_text(f"title={title}\nparts=ref,lines,narration,story,sound_score,vertical\n", encoding='utf-8')
            (sdir / 'meta.json').write_text(json.dumps({**meta, 'topic': a.topic, 'voice': narr.get('voice'), 'duration': narr['duration'], 'provider': used_provider, 'model': used_model}, indent=1, ensure_ascii=False), encoding='utf-8')
            report = validate(kit, a.slug, narr['duration'])
            if not report:
                print(f'OK: stories/{a.slug} builds and renders without errors. tokens total in {total_in} out {total_out}')
                (sdir / 'tokens.json').write_text(json.dumps({'attempts': attempt, 'input_tokens': total_in, 'output_tokens': total_out}), encoding='utf-8')
                return
            errs = [report]
        print('    problems:\n' + '\n'.join(f'      {e[:400]}' for e in errs))
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'The build/test reported these problems. Return ALL THREE files again (meta.json, story.js, sound_score.js), each complete inside its own `=== FILE: name ===` block, no prose:\n\n' + '\n'.join(errs)}]
    sys.exit(f'gave up after {a.attempts} attempts; last files are in stories/{a.slug} for inspection')


if __name__ == '__main__':
    main()
