#!/usr/bin/env python3
"""Remove videos older than --keep-days from a checkout of the videos branch and rebuild its overview.

Reads videos.json (written by publish.py), drops entries whose date is older than the cutoff, deletes their
videos/<slug>-<run>/ folders (plus orphan folders not listed in videos.json, dated by git), then regenerates
index.html and README.md with the same templates publish.py uses. Narration scripts under scripts/ (any depth,
written by the publish jobs) are removed on the same cutoff, dated by their last commit. Does not touch main or any story code.
"""
import argparse, datetime, html, json, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publish import CARD, PAGE, _links, fmt_dur  # noqa: E402  templates only; publish.py is not modified


def dir_date(root, rel):
    """Last commit date of a folder on the videos branch (fallback for folders missing from videos.json)."""
    try:
        out = subprocess.run(['git', '-C', str(root), 'log', '-1', '--format=%cI', '--', rel], capture_output=True, text=True, check=True).stdout.strip()
        return datetime.datetime.fromisoformat(out).date() if out else None
    except (subprocess.CalledProcessError, ValueError):
        return None


def write_overview(root, entries, raw):
    """Same output as publish.py's overview (keep in sync with publish.main)."""
    cards = []
    for e in entries:
        btns, raw_links, _ = _links(e, raw)
        cards.append(CARD.format(dir=e['dir'], title=html.escape(e['title']), topic=html.escape(e['topic']), dur=fmt_dur(e['duration'] or 0), voice=html.escape(e['voice']),
                                 date=e['date'], run=e['run'], run_url=e['run_url'] or '#', btns=btns, raw_links=raw_links))
    cards = cards or ['<p class="empty">No videos yet.</p>']
    (root / 'index.html').write_text(PAGE.replace('%CARDS%', '\n'.join(cards)), encoding='utf-8')
    md = ['# Generated videos', '', 'Newest first. Landscape = YouTube 16:9, Shorts = 9:16. Open `index.html` (or enable GitHub Pages on this branch) for the overview page.', '',
          '| Date | Title | Topic | Length | Landscape | Shorts | Run |', '|---|---|---|---|---|---|---|']
    for e in entries:
        t, tp = e['title'].replace('|', '\\|'), e['topic'].replace('|', '\\|')
        _, _, (land, short) = _links(e, raw)
        md.append(f"| {e['date']} | **{t}** | {tp} | {fmt_dur(e['duration'] or 0)} | {land} | {short} | [#{e['run']}]({e['run_url']}) |")
    (root / 'README.md').write_text('\n'.join(md) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='checkout of the videos branch')
    ap.add_argument('--repo', required=True, help='owner/name, for raw download links')
    ap.add_argument('--keep-days', type=int, default=7)
    ap.add_argument('--branch', default='videos')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--summary', default='', help='optional path to write a JSON result for the workflow summary')
    a = ap.parse_args()
    root = Path(a.root)
    today = datetime.datetime.now(datetime.timezone.utc).date()
    cutoff = today - datetime.timedelta(days=a.keep_days)

    idx = root / 'videos.json'
    entries = json.loads(idx.read_text(encoding='utf-8')) if idx.exists() else []
    keep, drop = [], []
    for e in entries:
        try:
            d = datetime.date.fromisoformat(e.get('date', ''))
        except ValueError:
            d = dir_date(root, e['dir'])
        (keep if d is None or d >= cutoff else drop).append(e)

    listed = {e['dir'] for e in entries}
    vdir = root / 'videos'
    orphans = []
    if vdir.is_dir():
        for p in sorted(vdir.iterdir()):
            rel = f'videos/{p.name}'
            if p.is_dir() and rel not in listed:
                d = dir_date(root, rel)
                if d is not None and d < cutoff:
                    orphans.append(rel)

    to_delete = [e['dir'] for e in drop] + orphans
    sdir = root / 'scripts'
    old_scripts = []
    if sdir.is_dir():
        for p in sorted(sdir.rglob('*.txt')):
            rel = p.relative_to(root).as_posix()
            d = dir_date(root, rel)
            if d is not None and d < cutoff:
                old_scripts.append(rel)
    to_delete += old_scripts
    freed = 0
    for rel in to_delete:
        p = root / rel
        if p.exists():
            freed += sum(f.stat().st_size for f in p.rglob('*') if f.is_file()) if p.is_dir() else p.stat().st_size
            if not a.dry_run:
                shutil.rmtree(p) if p.is_dir() else p.unlink()
    if not a.dry_run and (drop or orphans):
        idx.write_text(json.dumps(keep, indent=1, ensure_ascii=False), encoding='utf-8')
        write_overview(root, keep, f'https://github.com/{a.repo}/raw/{a.branch}')

    tag = 'DRY RUN: would remove' if a.dry_run else 'removed'
    print(f'cutoff {cutoff} (keep {a.keep_days} days); kept {len(keep)}, {tag} {len(to_delete)} ({freed / 1e6:.0f} MB)')
    for rel in to_delete:
        print('  -', rel)
    if a.summary:
        Path(a.summary).write_text(json.dumps({'cutoff': str(cutoff), 'kept': len(keep), 'removed': to_delete, 'freed_mb': round(freed / 1e6), 'dry_run': a.dry_run}), encoding='utf-8')


if __name__ == '__main__':
    main()
