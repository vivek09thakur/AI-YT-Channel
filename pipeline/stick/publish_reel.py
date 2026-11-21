#!/usr/bin/env python3
"""Publish a stickman fact reel to the videos branch under stickman/<slug>-<run>/ and rebuild stickman.json + stickman/index.html + stickman/README.md.

Completely separate from publish.py (videos/, videos.json, index.html, README.md are never touched). The JSON index is
also the history the fact picker reads and the daily-target guard counts.

usage: publish_reel.py --root site --src final --slug my-fact --run 12 --repo owner/name [--run-url URL] [--branch videos]
"""
import argparse, datetime, html, json, shutil
from pathlib import Path

FILES = ('reel.mp4', 'voice.mp3', 'thumb.jpg', 'narration.json', 'meta.json')


def fmt_dur(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Stickman fact reels</title>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&display=swap" rel="stylesheet">
<style>
  :root{--cream:#FFF6E0;--beige:#FFD93D;--ink:#141414;--red:#FF4D4D;--card:#FFFFFF;--night:#1B1F3B;--teal:#1FB8A6}
  *{box-sizing:border-box}
  body{margin:0;background:var(--beige);min-height:100vh;color:var(--ink);font-family:"Baloo 2",system-ui,sans-serif}
  header{text-align:center;padding:52px 20px 24px}
  h1{font-family:"Baloo 2",sans-serif;font-weight:800;font-size:clamp(34px,6vw,64px);margin:0;color:var(--ink)}
  header p{margin:10px 0 0;opacity:.75}
  main{max-width:1180px;margin:0 auto;padding:0 20px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:24px}
  .card{background:var(--card);border-radius:18px;overflow:hidden;box-shadow:0 10px 30px rgba(43,29,20,.18);display:flex;flex-direction:column;border:3px solid var(--ink)}
  .card img{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;background:var(--night)}
  .body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
  .title{font-family:"Baloo 2",sans-serif;font-weight:800;font-size:20px;margin:0}
  .meta{font-size:13px;opacity:.75;margin:0}
  .btn{margin-top:auto;text-align:center;text-decoration:none;padding:11px 14px;border-radius:12px;font-weight:700;font-size:14px;background:var(--red);color:#fff;border:2px solid var(--ink)}
  .small{display:flex;gap:12px;font-size:12px}
  .small a{color:var(--teal)}
  .empty{grid-column:1/-1;text-align:center;opacity:.7;padding:60px 0}
  footer{text-align:center;opacity:.7;padding:0 20px 40px;font-size:13px}
</style></head>
<body>
<header><h1>Stickman fact reels</h1><p>9:16 stick-figure fact reels (1080x1920, 30 fps). Newest first.</p></header>
<main>
%CARDS%
</main>
<footer>Each card links to the workflow run that made it. Scene code lives on main under .github/skills/stickman-reel/facts/.</footer>
</body></html>
'''

CARD = '''<article class="card">
  <img src="{rel}/thumb.jpg" alt="{title}" loading="lazy">
  <div class="body">
    <h2 class="title">{title}</h2>
    <p class="meta">{topic}</p>
    <p class="meta">{dur} &middot; {date} &middot; <a href="{run_url}">run #{run}</a></p>
    <a class="btn" href="{rel}/reel.mp4" download>Download reel ({mb})</a>
    <div class="small"><a href="{rel}/voice.mp3">voice</a><a href="{rel}/narration.json">timings</a><a href="{raw}/{dir}/reel.mp4">raw link</a></div>
  </div>
</article>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--src', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--run', required=True)
    ap.add_argument('--repo', required=True)
    ap.add_argument('--run-url', default='')
    ap.add_argument('--branch', default='videos')
    a = ap.parse_args()
    root, src = Path(a.root), Path(a.src)
    name = f'{a.slug}-{a.run}'
    dst = root / 'stickman' / name
    dst.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    meta = json.loads((src / 'meta.json').read_text(encoding='utf-8')) if (src / 'meta.json').exists() else {}
    narr = json.loads((src / 'narration.json').read_text(encoding='utf-8')) if (src / 'narration.json').exists() else {}
    entry = {'dir': f'stickman/{name}', 'slug': a.slug, 'run': a.run, 'run_url': a.run_url, 'title': meta.get('title', a.slug),
             'topic': meta.get('topic', ''), 'question': meta.get('question', ''), 'fact': meta.get('fact', ''), 'category': meta.get('category', ''), 'duration': narr.get('duration', 0), 'voice': narr.get('voice', ''), 'page_name': meta.get('page_name', ''),
             'date': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),
             'reel_bytes': (dst / 'reel.mp4').stat().st_size if (dst / 'reel.mp4').exists() else 0}
    idx = root / 'stickman.json'
    entries = json.loads(idx.read_text(encoding='utf-8')) if idx.exists() else []
    entries = [e for e in entries if e['dir'] != entry['dir']]
    entries.insert(0, entry)
    idx.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding='utf-8')

    raw = f'https://github.com/{a.repo}/raw/{a.branch}'
    cards = [CARD.format(dir=e['dir'], rel=e['dir'].split('/', 1)[1], title=html.escape(e['title']), topic=html.escape(e['topic']),
                         dur=fmt_dur(e['duration'] or 0), date=e['date'], run=e['run'], run_url=e['run_url'] or '#',
                         mb=f"{e['reel_bytes'] / 1e6:.0f} MB", raw=raw) for e in entries] or ['<p class="empty">No fact reels yet.</p>']
    (root / 'stickman').mkdir(exist_ok=True)
    (root / 'stickman' / 'index.html').write_text(PAGE.replace('%CARDS%', '\n'.join(cards)), encoding='utf-8')
    md = ['# Stickman fact reels', '', 'Newest first. 9:16, 1080x1920, 30 fps. Open `stickman/index.html` for the overview page.', '',
          '| Date | Title | Fact | Length | Reel | Run |', '|---|---|---|---|---|---|']
    for e in entries:
        t, tp = e['title'].replace('|', '\\|'), str(e.get('fact') or e.get('topic', '')).replace('|', '\\|')
        md.append(f"| {e['date']} | **{t}** | {tp} | {fmt_dur(e['duration'] or 0)} | [download]({raw}/{e['dir']}/reel.mp4) ({e['reel_bytes'] / 1e6:.0f} MB) | [#{e['run']}]({e['run_url']}) |")
    (root / 'stickman' / 'README.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    (root / '.nojekyll').write_text('', encoding='utf-8')
    print(f'published {entry["dir"]}; {len(entries)} fact reels listed')


if __name__ == '__main__':
    main()
