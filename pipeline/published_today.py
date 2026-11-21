#!/usr/bin/env python3
"""How many videos of this kind were published today, and is there room for another one? Used by the scheduled
slots: each slot does work only while fewer than --max videos exist for today (UTC), so a failed slot is picked up
by the next one and nothing is produced beyond the daily target.

usage: published_today.py --repo owner/name --index nlm.json|videos.json [--branch videos] [--max 2]
env: GITHUB_TOKEN (to read a private repo), GITHUB_OUTPUT (gets go=true|false and count=N)

Prints the decision; exit code is always 0 (a missing index means nothing published yet -> go=true).
"""
import argparse, datetime, json, os, sys, urllib.error, urllib.request


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--branch', default='videos')
    ap.add_argument('--max', type=int, default=1, help='daily target; go while fewer than this were published today')
    a = ap.parse_args()

    today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    url = f'https://api.github.com/repos/{a.repo}/contents/{a.index}?ref={a.branch}'
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.raw', 'User-Agent': 'published-today'})
    if os.environ.get('GITHUB_TOKEN'):
        req.add_header('Authorization', f"Bearer {os.environ['GITHUB_TOKEN']}")
    entries = []
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            entries = json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f'{a.index} not readable ({e.code}) - treating as nothing published yet')
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f'{a.index} not readable ({e}) - treating as nothing published yet')

    done = [e for e in entries if isinstance(e, dict) and e.get('date') == today]
    go = len(done) < a.max
    titles = '; '.join(str(e.get('title') or e.get('slug')) for e in done) or '-'
    print(f'{len(done)}/{a.max} published today ({today}) in {a.index}: {titles}')
    print('go' if go else 'daily target reached - skip')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'go={"true" if go else "false"}\ncount={len(done)}\n')


if __name__ == '__main__':
    main()
