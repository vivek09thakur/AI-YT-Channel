#!/usr/bin/env python3
"""Discover which LLM API keys are configured, probe each with a ~10-token request, report status and (where the
provider exposes it) remaining credits, then pick the provider to use.

    python pipeline/check_keys.py --prefer gemini [--model X]

Writes a Markdown table to $GITHUB_STEP_SUMMARY (if set) and `provider=... model=...` lines to $GITHUB_OUTPUT.
Exit 1 if no usable provider is found. Only OpenRouter has a balance API; for the others the probe only tells
us valid / quota exhausted / invalid.
"""
import argparse, json, os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
import requests
from generate_story import DEFAULT_MODEL, OPENAI_COMPAT

# order used for automatic fallback: free tiers first
PRIORITY = ['gemini', 'mistral', 'cerebras', 'meta', 'openrouter', 'openai', 'anthropic']
KEY_ENV = {p: OPENAI_COMPAT[p][1] for p in OPENAI_COMPAT} | {'anthropic': 'ANTHROPIC_API_KEY'}
PROBE_MSG = [{'role': 'user', 'content': 'Reply with the single word: ok'}]


def classify(status, body):
    b = body.lower()
    if status == 200:
        return 'ok', 'key valid, quota available'
    if status in (401, 403) or 'api_key_invalid' in b or 'invalid_api_key' in b or 'permission_denied' in b:
        return 'bad', f'invalid key / no access ({status})'
    if status == 429 or status == 402:
        if any(k in b for k in ('insufficient_quota', 'credit', 'billing', 'resource_exhausted', 'quota')):
            return 'exhausted', f'quota or credits exhausted ({status})'
        return 'ratelimit', f'rate limited right now ({status}), may work on retry'
    return 'error', f'HTTP {status}: {body[:120]}'


def probe(provider, model):
    key = os.environ.get(KEY_ENV[provider], '')
    if not key:
        return None
    try:
        if provider == 'anthropic':
            r = requests.post('https://api.anthropic.com/v1/messages', timeout=60,
                              headers={'x-api-key': key, 'anthropic-version': '2023-06-01'},
                              json={'model': model, 'max_tokens': 5, 'messages': PROBE_MSG})
        else:
            url, _, extra = OPENAI_COMPAT[provider]
            r = requests.post(url, timeout=60, headers={'Authorization': f'Bearer {key}', **extra},
                              json={'model': model, 'max_tokens': 5, 'messages': PROBE_MSG})
        state, note = classify(r.status_code, r.text)
        if state == 'ok' and 'error' in r.text[:200] and '"choices"' not in r.text:
            state, note = 'error', r.text[:120]
    except requests.RequestException as e:
        state, note = 'error', f'request failed: {e}'[:120]
    return {'provider': provider, 'model': model, 'state': state, 'note': note, 'credits': credits(provider, key)}


def credits(provider, key):
    """Human-readable balance where the API exposes one."""
    try:
        if provider == 'openrouter':
            j = requests.get('https://openrouter.ai/api/v1/credits', timeout=30,
                             headers={'Authorization': f'Bearer {key}'}).json().get('data', {})
            if 'total_credits' in j:
                return f"${j['total_credits'] - j.get('total_usage', 0):.2f} left of ${j['total_credits']:.2f}"
    except Exception:
        pass
    return {'gemini': 'free tier (no balance API)', 'mistral': 'free tier (no balance API)',
            'cerebras': 'free tier (no balance API)', 'meta': 'free preview (no balance API)',
            'openai': 'not exposed by API; see platform.openai.com/usage',
            'anthropic': 'not exposed by API; see console.anthropic.com'}.get(provider, '-')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prefer', default='auto', help='provider chosen by the user, or auto')
    ap.add_argument('--model', default='', help='model override (only applied to the preferred provider)')
    a = ap.parse_args()

    rows = []
    for p in PRIORITY:
        model = a.model if (a.model and p == a.prefer) else DEFAULT_MODEL[p]
        res = probe(p, model)
        rows.append(res or {'provider': p, 'model': model, 'state': 'missing', 'note': f'secret {KEY_ENV[p]} not set', 'credits': '-'})

    icon = {'ok': '✅', 'ratelimit': '⏳', 'exhausted': '❌', 'bad': '❌', 'error': '⚠️', 'missing': '➖'}
    lines = ['### LLM providers', '', '| Provider | Model | Status | Credits | Note |', '|---|---|---|---|---|']
    for r in rows:
        lines.append(f"| {r['provider']} | `{r['model']}` | {icon[r['state']]} {r['state']} | {r['credits']} | {r['note']} |")

    usable = [r for r in rows if r['state'] in ('ok', 'ratelimit')]
    chosen = None
    if a.prefer != 'auto':
        chosen = next((r for r in usable if r['provider'] == a.prefer), None)
        if not chosen:
            why = next((r for r in rows if r['provider'] == a.prefer), {}).get('note', '')
            lines.append(f"\n> Requested provider **{a.prefer}** is not usable ({why}); falling back.")
    if not chosen and usable:
        chosen = usable[0]
    if chosen:
        lines.append(f"\n**Using {chosen['provider']} / `{chosen['model']}`**")
    else:
        lines.append('\n**No usable provider.** Add a working key secret (GEMINI_API_KEY is free: aistudio.google.com/apikey).')

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
