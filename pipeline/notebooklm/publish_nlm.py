#!/usr/bin/env python3
"""Publish a NotebookLM short to the videos branch under nlm/<slug>-<run>/ and rebuild nlm.json + nlm/index.html + nlm/README.md.

Separate from publish.py and publish_fact_reel.py: videos/, facts/, videos.json, facts.json, index.html and README.md are never touched.

usage: publish_nlm.py --root site --src final --slug my-topic --run 12 --repo owner/name [--run-url URL] [--branch videos]
"""
import argparse, datetime, html, json, shutil
from pathlib import Path

FILES = ('reel.mp4', 'thumb.jpg', 'meta.json')


def fmt_dur(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>NotebookLM shorts</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&display=swap" rel="stylesheet">
<style>
  :root{--bg:#0F1115;--card:#1A1D24;--ink:#E8EAF0;--mute:#9AA0AE;--accent:#4F8CFF;--line:#2A2F3A}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);min-height:100vh;color:var(--ink);font-family:Inter,system-ui,sans-serif}
  header{text-align:center;padding:52px 20px 24px}
  h1{font-weight:800;font-size:clamp(32px,6vw,56px);margin:0}
  header p{margin:10px 0 0;color:var(--mute)}
  main{max-width:1180px;margin:0 auto;padding:0 20px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:24px}
  .card{background:var(--card);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;border:1px solid var(--line)}
  .card img{width:100%;aspect-ratio:9/16;object-fit:cover;display:block;background:#000}
  .body{padding:14px 16px 16px;display:flex;flex-direction:column;gap:8px;flex:1}
  .title{font-weight:700;font-size:18px;margin:0}
  .meta{font-size:13px;color:var(--mute);margin:0}
  .genre{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--accent)}
  .btn{margin-top:auto;text-align:center;text-decoration:none;padding:11px 14px;border-radius:10px;font-weight:700;font-size:14px;background:var(--accent);color:#fff}
  .small{display:flex;gap:12px;font-size:12px}
  .small a{color:var(--mute)}
  .empty{grid-column:1/-1;text-align:center;color:var(--mute);padding:60px 0}
  footer{text-align:center;color:var(--mute);padding:0 20px 40px;font-size:13px}
</style></head>
<body>
<header><h1>NotebookLM shorts</h1><p>Auto-researched 9:16 Video Overviews. Newest first.</p></header>
<main>
%CARDS%
</main>
<footer>Each card links to the workflow run that made it. Topics come from pipeline/notebooklm/topics.json on main.</footer>
</body></html>
'''

CARD = '''<article class="card">
  <img src="{rel}/thumb.jpg" alt="{title}" loading="lazy">
  <div class="body">
    <span class="genre">{genre}</span>
    <h2 class="title">{title}</h2>
    <p class="meta">{topic}</p>
    <p class="meta">{dur} &middot; {date} &middot; <a href="{run_url}">run #{run}</a></p>
    <a class="btn" href="{rel}/reel.mp4" download>Download ({mb})</a>
    <div class="small"><a href="{rel}/meta.json">meta</a><a href="{raw}/{dir}/reel.mp4">raw link</a></div>
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
    ap.add_argument('--duration', type=float, default=0)
    a = ap.parse_args()
    root, src = Path(a.root), Path(a.src)
    name = f'{a.slug}-{a.run}'
    dst = root / 'nlm' / name
    dst.mkdir(parents=True, exist_ok=True)
    for f in FILES:
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    meta = json.loads((src / 'meta.json').read_text(encoding='utf-8')) if (src / 'meta.json').exists() else {}
    entry = {'dir': f'nlm/{name}', 'slug': a.slug, 'run': a.run, 'run_url': a.run_url, 'title': meta.get('title', a.slug),
             'topic': meta.get('topic', ''), 'genre': meta.get('genre', ''), 'format': meta.get('format', 'short'),
             'duration': a.duration, 'date': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),
             'reel_bytes': (dst / 'reel.mp4').stat().st_size if (dst / 'reel.mp4').exists() else 0}
    idx = root / 'nlm.json'
    entries = json.loads(idx.read_text(encoding='utf-8')) if idx.exists() else []
    entries = [e for e in entries if e['dir'] != entry['dir']]
    entries.insert(0, entry)
    idx.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding='utf-8')

    raw = f'https://github.com/{a.repo}/raw/{a.branch}'
    cards = [CARD.format(dir=e['dir'], rel=e['dir'].split('/', 1)[1], title=html.escape(e['title']), topic=html.escape(e['topic']),
                         genre=html.escape(e.get('genre', '')), dur=fmt_dur(e['duration'] or 0), date=e['date'], run=e['run'],
                         run_url=e['run_url'] or '#', mb=f"{e['reel_bytes'] / 1e6:.0f} MB", raw=raw) for e in entries] \
        or ['<p class="empty">No shorts yet.</p>']
    (root / 'nlm').mkdir(exist_ok=True)
    (root / 'nlm' / 'index.html').write_text(PAGE.replace('%CARDS%', '\n'.join(cards)), encoding='utf-8')
    md = ['# NotebookLM shorts', '', 'Newest first. Auto-researched 9:16 Video Overviews. Open `nlm/index.html` for the overview page.', '',
          '| Date | Genre | Title | Length | Video | Run |', '|---|---|---|---|---|---|']
    for e in entries:
        t = e['title'].replace('|', '\\|')
        md.append(f"| {e['date']} | {e.get('genre', '')} | **{t}** | {fmt_dur(e['duration'] or 0)} | [download]({raw}/{e['dir']}/reel.mp4) ({e['reel_bytes'] / 1e6:.0f} MB) | [#{e['run']}]({e['run_url']}) |")
    (root / 'nlm' / 'README.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    (root / '.nojekyll').write_text('', encoding='utf-8')
    print(f'published {entry["dir"]}; {len(entries)} shorts listed')


if __name__ == '__main__':
    main()
