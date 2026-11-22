#!/usr/bin/env python3
"""How many videos of this kind were published today, and is there room for another one? Used by the scheduled
slots: each slot does work only while fewer than the current target exist for today (UTC), so a dropped or failed
slot is picked up by the next one and nothing is produced beyond the daily target.

The target is --max, or with --due the number of due times that have already passed today (at least 1, never more
than --max): with --due "03:37 09:37" a slot before 09:37 UTC makes at most 1 video, later slots at most 2, so
30-minute retry slots never make the second video ahead of its time.

usage: published_today.py --repo owner/name --index nlm.json|videos.json [--branch videos] [--max 2] [--due "HH:MM HH:MM"]
env: GITHUB_TOKEN (to read a private repo), GITHUB_OUTPUT (gets go=true|false, count=N and target=N)

Prints the decision; exit code is always 0 (a missing index means nothing published yet -> go=true).
"""
import argparse, datetime, json, os, sys, urllib.error, urllib.request


def due_times(spec):
    times = []
    for t in spec.replace(',', ' ').split():
        try:
            times.append(datetime.datetime.strptime(t, '%H:%M').strftime('%H:%M'))
        except ValueError:
            raise argparse.ArgumentTypeError(f'--due expects HH:MM (UTC) times, got {t!r}')
    return sorted(times)


def current_target(max_per_day, due, now_hhmm):
    """How many videos should exist by now: the due times already passed, at least 1, at most max_per_day."""
    if not due:
        return max_per_day
    passed = sum(1 for t in due if t <= now_hhmm)
    return max(1, min(max_per_day, passed))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--index', required=True)
    ap.add_argument('--branch', default='videos')
    ap.add_argument('--max', type=int, default=1, help='daily target; go while fewer than this were published today')
    ap.add_argument('--due', type=due_times, default=[],
                    help='UTC times "HH:MM HH:MM" when the 1st, 2nd, ... video of the day is due; the target becomes the number of these already passed')
    a = ap.parse_args()

    now = datetime.datetime.now(datetime.timezone.utc)
    today = now.strftime('%Y-%m-%d')
    target = current_target(a.max, a.due, now.strftime('%H:%M'))
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
    go = len(done) < target
    titles = '; '.join(str(e.get('title') or e.get('slug')) for e in done) or '-'
    if a.due:
        print(f'{target} of {a.max} due by {now:%H:%M} UTC (due at {", ".join(a.due)} UTC)')
    print(f'{len(done)}/{target} published today ({today}) in {a.index}: {titles}')
    print('go' if go else ('daily target reached - skip' if target >= a.max else 'nothing due yet - skip'))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as f:
            f.write(f'go={"true" if go else "false"}\ncount={len(done)}\ntarget={target}\n')


if __name__ == '__main__':
    main()
