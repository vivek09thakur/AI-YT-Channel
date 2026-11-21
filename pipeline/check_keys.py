#!/usr/bin/env python3
import argparse, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
import requests
from generate_story import DEFAULT_MODEL, OPENAI_COMPAT, GEMINI_BASE, PRIORITY, FALLBACK_MODELS, KEY_ENV, REASONING_BODY
PROBE_MSG = [{'role': 'user', 'content': 'Reply with the single word: ok'}]


def classify(status, body):
    b = body.lower()
    if status == 200:
        return 'ok', 'key valid, quota available'
    if status in (401, 403) or 'api_key_invalid' in b or 'invalid_api_key' in b or 'permission_denied' in b:
        return 'bad', f'invalid key / no access ({status})'
    if status == 429 or status == 402:
        if any(k in b for k in ('insufficient_quota', 'credit', 'billing', 'resource_exhausted', 'quota')):
            if any(k in b for k in ('per minute', 'perminute', 'per_minute', 'requests per min')):
                return 'ratelimit', f'per-minute limit hit ({status}), may work on retry'
            return 'exhausted', f'quota or credits exhausted ({status})'
        return 'ratelimit', f'rate limited right now ({status}), may work on retry'
    if status == 404 or 'not_found' in b or 'no longer available' in b or 'does not exist' in b:
        return 'nomodel', f'model not available ({status})'
    if status in (502, 503, 529) or any(k in b for k in ('high demand', 'overloaded', 'temporarily unavailable')):
        return 'busy', f'model busy right now ({status}); the generation step retries and falls back'
    return 'error', f'HTTP {status}: {body[:120]}'


def probe_once(provider, model, key):
    try:
        if provider == 'gemini':
            # a real 1-token generation so an exhausted free-tier quota (429 RESOURCE_EXHAUSTED) is caught up front
            r = requests.post(f'{GEMINI_BASE}/models/{model}:generateContent', timeout=60, headers={'x-goog-api-key': key},
                              json={'contents': [{'parts': [{'text': PROBE_MSG[0]['content']}]}], 'generationConfig': {'maxOutputTokens': 5}})
            return classify(r.status_code, r.text)
        if provider == 'anthropic':
            r = requests.post('https://api.anthropic.com/v1/messages', timeout=60,
                              headers={'x-api-key': key, 'anthropic-version': '2023-06-01'},
                              json={'model': model, 'max_tokens': 5, 'messages': PROBE_MSG})
        else:
            url, _, extra = OPENAI_COMPAT[provider]
            body = {'model': model, 'max_tokens': 5, 'messages': PROBE_MSG}
            if provider in REASONING_BODY:
                body.update(REASONING_BODY[provider], reasoning_effort='minimal', max_tokens=64)
            r = requests.post(url, timeout=60, headers={'Authorization': f'Bearer {key}', **extra}, json=body)
        state, note = classify(r.status_code, r.text)
        if state == 'ok' and 'error' in r.text[:200] and '"choices"' not in r.text:
            state, note = 'error', r.text[:120]
    except requests.RequestException as e:
        state, note = 'error', f'request failed: {e}'[:120]
    return state, note


def probe(provider, model, allow_fallback=True):
    key = os.environ.get(KEY_ENV[provider], '')
    if not key:
        return None
    candidates = [model] + [m for m in FALLBACK_MODELS.get(provider, []) if m != model] if allow_fallback else [model]
    tried = []; first_busy = None
    for m in candidates:
        state, note = probe_once(provider, m, key)
        if state == 'busy' and first_busy is None:
            first_busy = (m, note)
        if state not in ('nomodel', 'busy'):
            break
        tried.append(m)
    else:
        # every candidate was missing or busy: a busy model is still usable (generate_story retries + falls back)
        if first_busy:
            m, note = first_busy; state = 'busy'; tried = [t for t in tried if t != m]
    if state == 'ok' and first_busy:
        # keep the (busy) default: generate_story retries it and falls back on its own; the key itself is proven good
        note = f'key valid; {first_busy[0]} busy right now (503), {m} answered - generation retries then falls back'
        m = first_busy[0]; tried = [t for t in tried if t != m]
    if tried and state not in ('nomodel', 'busy'):
        note += f" (skipped unavailable or busy: {', '.join(tried)})"
    return {'provider': provider, 'model': m, 'state': state, 'note': note, 'credits': credits(provider, key)}


def credits(provider, key):
    try:
        if provider == 'openrouter':
            j = requests.get('https://openrouter.ai/api/v1/credits', timeout=30,
                             headers={'Authorization': f'Bearer {key}'}).json().get('data', {})
            if 'total_credits' in j:
                return f"${j['total_credits'] - j.get('total_usage', 0):.2f} left of ${j['total_credits']:.2f}"
    except Exception:
        pass
    return {'gemini': 'free tier (no balance API)', 'mistral': 'free tier (no balance API)',
            'cerebras': 'free tier (no balance API)', 'meta': 'pay-as-you-go; see dev.meta.ai → Billing',
            'openai': 'not exposed by API; see platform.openai.com/usage',
            'anthropic': 'not exposed by API; see console.anthropic.com'}.get(provider, '-')


def check_llm(prefer='auto', model=''):
    """probe every provider; returns (markdown lines, chosen row or None)"""
    rows = []
    for p in PRIORITY:
        m = model if (model and p == prefer) else DEFAULT_MODEL[p]
        res = probe(p, m, allow_fallback=not (model and p == prefer))
        rows.append(res or {'provider': p, 'model': m, 'state': 'missing', 'note': f'secret {KEY_ENV[p]} not set', 'credits': '-'})

    icon = {'ok': '✅', 'ratelimit': '⏳', 'busy': '⏳', 'exhausted': '❌', 'bad': '❌', 'nomodel': '❌', 'error': '⚠️', 'missing': '➖'}
    lines = ['### LLM providers', '', '| Provider | Model | Status | Credits | Note |', '|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['provider']} | `{r['model']}` | {icon[r['state']]} {r['state']} | {r['credits']} | {r['note']} |")

    usable = [r for r in rows if r['state'] in ('ok', 'ratelimit', 'busy')]
    chosen = None
    if prefer != 'auto':
        chosen = next((r for r in usable if r['provider'] == prefer), None)
        if not chosen:
            why = next((r for r in rows if r['provider'] == prefer), {}).get('note', '')
            lines.append(f"\n> Requested provider **{prefer}** is not usable ({why}); falling back.")
    if not chosen and usable:
        chosen = usable[0]
    if chosen:
        lines.append(f"\n**Using {chosen['provider']} / `{chosen['model']}`**")
    else:
        lines.append('\n**No usable provider.** Add a working key secret (GEMINI_API_KEY is free: aistudio.google.com/apikey).')
    return lines, chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prefer', default='auto', help='provider chosen by the user, or auto')
    ap.add_argument('--model', default='', help='model override (only applied to the preferred provider)')
    a = ap.parse_args()
    lines, chosen = check_llm(a.prefer, a.model)
    text = '\n'.join(lines)
    print(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).open('a', encoding='utf-8').write(text + '\n\n')
    if not chosen:
        sys.exit(1)
    if os.environ.get('GITHUB_OUTPUT'):
        Path(os.environ['GITHUB_OUTPUT']).open('a', encoding='utf-8').write(f"provider={chosen['provider']}\nmodel={chosen['model']}\n")


if __name__ == '__main__':
    main()
