#!/usr/bin/env python3
"""precheck.py --need-minutes N [--prefer auto --model X --voice en-US-AndrewNeural] [--no-cancel]

Pre-run gate for the video workflows. Checks, in order:
  1. AI quota      - every LLM provider key is probed with a 1-token request (check_keys.check_llm); picks the provider.
                     A probe that only times out is retried, and if nothing better answers the run still goes ahead
                     with a warning: generation retries and falls back across keys on its own, so a slow network
                     must not fail the run before it starts. Rejected or exhausted keys still fail it.
  2. runner quota  - GitHub Actions minutes used this month vs the plan's included minutes (needs BILLING_TOKEN,
                     a fine-grained PAT with Account permissions -> Plan: read; ACTIONS_INCLUDED_MINUTES defaults to 2000).
                     Skipped as "free" in a public repository: standard hosted runners are not billed there.
  3. TTS quota     - Azure Speech if AZURE_SPEECH_KEY is set (tiny synth), else an edge-tts probe (free, no quota)
Writes a summary table to GITHUB_STEP_SUMMARY, provider/model to GITHUB_OUTPUT, exits 1 when the run cannot succeed.
Out of Actions minutes is not an error but a budget condition: the run then cancels itself (stop_run) instead of failing,
unless --no-cancel is given (the check-only workflow, which should just show the result).
"""
import argparse, asyncio, datetime, html, json, os, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
import requests
import stop_run
from check_keys import check_llm

ICON = {'ok': '✅', 'warn': '⚠️', 'skip': '➖', 'fail': '❌'}
GH_API = 'https://api.github.com'
SKU_MULT = {'windows': 2, 'macos': 10}   # billing multipliers; linux = 1


def repo_is_public():
    """True / False, or None when it cannot be told. Standard GitHub-hosted runners are free in public repositories,
    so the account's included minutes do not apply there; counting them would cancel runs that cost nothing."""
    ev = os.environ.get('GITHUB_EVENT_PATH', '')
    try:
        if ev and Path(ev).is_file():
            repo = json.loads(Path(ev).read_text(encoding='utf-8')).get('repository') or {}
            if 'private' in repo:
                return not repo['private']
    except (OSError, ValueError):
        pass
    name = os.environ.get('GITHUB_REPOSITORY', '')
    token = os.environ.get('GITHUB_TOKEN') or os.environ.get('BILLING_TOKEN') or ''
    if not name:
        return None
    hdr = {'Accept': 'application/vnd.github+json'}
    if token:
        hdr['Authorization'] = f'Bearer {token}'
    try:
        r = requests.get(f'{GH_API}/repos/{name}', headers=hdr, timeout=30)
        if r.status_code == 200:
            return not r.json().get('private', True)
    except requests.RequestException:
        pass
    return None


def actions_minutes(need):
    """-> (state, headline, detail)"""
    if repo_is_public():
        return 'ok', 'free', 'public repository: standard GitHub-hosted runners are not billed, included minutes do not apply'
    token = os.environ.get('BILLING_TOKEN', '')
    owner = os.environ.get('GITHUB_REPOSITORY_OWNER') or os.environ.get('GITHUB_ACTOR', '')
    included = int(os.environ.get('ACTIONS_INCLUDED_MINUTES') or 2000)
    if not token:
        return 'skip', 'not checked', 'add secret BILLING_TOKEN (fine-grained PAT, Account permissions -> Plan: read) to enable'
    if not owner:
        return 'skip', 'not checked', 'GITHUB_REPOSITORY_OWNER not set'
    hdr = {'Authorization': f'Bearer {token}', 'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        r = requests.get(f'{GH_API}/users/{owner}/settings/billing/usage', params={'year': now.year, 'month': now.month}, headers=hdr, timeout=30)
        if r.status_code == 200:
            used = paid = 0.0
            for it in r.json().get('usageItems', []):
                if str(it.get('product', '')).lower() != 'actions' or 'minute' not in str(it.get('unitType', '')).lower():
                    continue
                sku = str(it.get('sku', '')).lower()
                mult = next((m for k, m in SKU_MULT.items() if k in sku), 1)
                used += float(it.get('quantity', 0)) * mult
                paid += float(it.get('netAmount', 0))
        else:
            # legacy billing platform
            r2 = requests.get(f'{GH_API}/users/{owner}/settings/billing/actions', headers=hdr, timeout=30)
            if r2.status_code != 200:
                why = 'token lacks Plan: read permission' if r.status_code in (401, 403) else f'HTTP {r.status_code}'
                return 'warn', 'not checked', f'billing API: {why} ({r.text[:80].strip()})'
            j = r2.json(); used = float(j.get('total_minutes_used', 0)); included = int(j.get('included_minutes') or included); paid = float(j.get('total_paid_minutes_used', 0))
    except requests.RequestException as e:
        return 'warn', 'not checked', f'billing API request failed: {e}'[:160]
    left = included - used
    head = f'{left:.0f} of {included} min left this month, need ~{need}'
    if left >= need:
        return 'ok', head, f'{used:.0f} min used' + (f'; ${paid:.2f} overage already billed' if paid else '')
    if paid or os.environ.get('ACTIONS_ALLOW_OVERAGE') == '1':
        return 'warn', head, 'included minutes exhausted; run continues on paid minutes (spending limit must allow it)'
    return 'fail', head, 'not enough included Actions minutes; wait for the monthly reset, pick one format, or set repo variable ACTIONS_ALLOW_OVERAGE=1'


def tts(voice):
    key = os.environ.get('AZURE_SPEECH_KEY', '')
    if key:
        region = os.environ.get('AZURE_SPEECH_REGION', 'eastus')
        lang = '-'.join(voice.split('-')[:2])
        ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}"><voice name="{voice}">{html.escape("ok")}</voice></speak>'
        try:
            r = requests.post(f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1', data=ssml.encode(), timeout=60,
                              headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/ssml+xml',
                                       'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm', 'User-Agent': 'ai-yt-channel'})
        except requests.RequestException as e:
            return 'fail', 'Azure Speech unreachable', str(e)[:160]
        if r.status_code == 200 and r.content:
            return 'ok', f'Azure Speech ({region}) `{voice}`', 'key valid, quota available'
        if r.status_code == 401:
            return 'fail', 'Azure Speech key rejected', 'check AZURE_SPEECH_KEY / AZURE_SPEECH_REGION'
        if r.status_code in (403, 429):
            kind = 'quota exhausted' if r.status_code == 403 or 'quota' in r.text.lower() else 'rate limited'
            return 'fail', f'Azure Speech {kind} ({r.status_code})', r.text[:160].strip()
        return 'fail', f'Azure Speech HTTP {r.status_code}', r.text[:160].strip()
    try:
        import edge_tts
    except ImportError:
        return 'fail', 'edge-tts not installed', 'pip install edge-tts'
    tmp = Path(tempfile.mkdtemp()) / 'probe.mp3'
    try:
        asyncio.run(edge_tts.Communicate('ok', voice).save(str(tmp)))
        if tmp.exists() and tmp.stat().st_size > 0:
            return 'ok', f'edge-tts `{voice}`', 'free service, no quota; probe synthesised'
        return 'fail', 'edge-tts returned empty audio', 'service may be blocking the runner right now'
    except Exception as e:
        return 'fail', 'edge-tts probe failed', f'{type(e).__name__}: {e}'[:160]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--need-minutes', type=int, required=True, help='estimated Actions minutes this run will consume')
    ap.add_argument('--prefer', default='auto'); ap.add_argument('--model', default='')
    ap.add_argument('--voice', default='en-US-AndrewNeural')
    ap.add_argument('--no-cancel', action='store_true',
                    help='report-only mode: out of Actions minutes fails the job instead of cancelling the run')
    a = ap.parse_args()

    llm_lines, chosen = check_llm(a.prefer, a.model)
    runner = actions_minutes(a.need_minutes)
    voice = tts(a.voice)

    # unreachable = the probe timed out, not a rejected key: warn and let generation (which retries and falls back) try
    ai_state = 'fail' if not chosen else 'warn' if chosen['state'] == 'unreachable' else 'ok'
    ai_head = f"{chosen['provider']} / `{chosen['model']}`" if chosen else 'no usable LLM provider'
    ai_detail = 'probe got no answer; generation will retry it and fall back to other keys' if ai_state == 'warn' else 'see table below'
    rows = [('AI quota', ai_state, ai_head, ai_detail),
            ('Runner quota', *runner), ('TTS quota', *voice)]
    lines = ['## Pre-run check', '', '| Check | Status | Result | Detail |', '|---|---|---|---|']
    lines += [f'| {n} | {ICON[s]} {s} | {h} | {d} |' for n, s, h, d in rows]
    text = '\n'.join(lines) + '\n\n' + '\n'.join(llm_lines)
    print(text)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        Path(os.environ['GITHUB_STEP_SUMMARY']).open('a', encoding='utf-8').write(text + '\n\n')
    failed = {n for n, s, _, _ in rows if s == 'fail'}
    budget_stop = failed == {'Runner quota'} and not a.no_cancel
    for n, s, h, d in rows:
        if s == 'warn':
            print(f'::warning title={n}::{h} - {d}')
        elif s == 'fail' and not budget_stop:
            print(f'::error title={n}::{h} - {d}')
    if budget_stop:
        # a budget limit, not something broken: cancel the run instead of failing it
        stop_run.stop(f'Not enough GitHub Actions minutes left for this run: {runner[1]} ({runner[2]}).')
    if failed:
        sys.exit(1)
    if os.environ.get('GITHUB_OUTPUT'):
        Path(os.environ['GITHUB_OUTPUT']).open('a', encoding='utf-8').write(f"provider={chosen['provider']}\nmodel={chosen['model']}\n")


if __name__ == '__main__':
    main()
