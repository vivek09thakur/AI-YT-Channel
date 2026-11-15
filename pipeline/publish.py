#!/usr/bin/env python3
"""Add a finished video to the `videos` branch checkout and regenerate the overview page.

    python pipeline/publish.py --root <checkout of videos branch> --src <dir with landscape.mp4 shorts.mp4 voice.mp3 narration.json meta.json thumb.jpg> \
        --slug shiva-neelkanth --run 123 --repo owner/name --run-url https://github.com/owner/name/actions/runs/123

Layout on the branch:
    videos/<slug>-<run>/landscape.mp4 | shorts.mp4 | voice.mp3 | thumb.jpg | narration.json | meta.json
    videos.json        all entries, newest first
    index.html         overview page with one card per video and two download buttons (works on GitHub Pages or locally)
    README.md          the same list as Markdown with raw download links (renders directly on github.com)
"""
import argparse, datetime, html, json, shutil
from pathlib import Path


def fmt_dur(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


def mb(p):
    return f'{p.stat().st_size / 1e6:.0f} MB'


PAGE = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI YT Channel: generated videos</title>
<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Libre+Baskerville:wght@400;700&display=swap" rel="stylesheet">
<style>
  :root{--amber:#f7a234;--saffron:#f08a24;--deep:#2f1207;--ink:#241006;--cream:#fff3d6;--gold:#e9b949;--kumkum:#c8102e}
  *{box-sizing:border-box}
  body{margin:0;background:linear-gradient(180deg,#f7a234 0%,#f08a24 40%,#b4471a 80%,#5e2a10 100%);min-height:100vh;color:var(--ink);font-family:"Libre Baskerville",Georgia,serif}
  header{text-align:center;padding:56px 20px 28px}
  h1{font-family:"IM Fell English",serif;font-weight:400;letter-spacing:.12em;font-size:clamp(40px,7vw,80px);margin:0;color:var(--cream);text-shadow:0 3px 0 var(--deep),0 0 30px rgba(255,127,17,.8)}
  header p{margin:10px 0 0;color:var(--cream);font-style:italic;opacity:.9}
  main{max-width:1180px;margin:0 auto;padding:0 20px 80px;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:26px}
  .card{background:var(--cream);border-radius:18px;overflow:hidden;box-shadow:0 14px 40px rgba(36,16,6,.35);display:flex;flex-direction:column}
  .card img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:var(--deep)}
  .body{padding:18px 20px 20px;display:flex;flex-direction:column;gap:10px;flex:1}
  .title{font-family:"IM Fell English",serif;font-size:26px;letter-spacing:.04em;margin:0;color:var(--deep)}
  .meta{font-size:13px;color:#6a4a30;margin:0}
  .btns{display:flex;gap:10px;margin-top:auto;padding-top:8px;flex-wrap:wrap}
  .btn{flex:1;min-width:140px;text-align:center;text-decoration:none;padding:12px 14px;border-radius:12px;font-weight:700;font-size:14px;letter-spacing:.02em;border:2px solid var(--deep);transition:transform .12s}
  .btn:hover{transform:translateY(-2px)}
  .land{background:var(--deep);color:var(--cream)}
  .short{background:var(--kumkum);color:var(--cream);border-color:var(--kumkum)}
  .small{display:flex;gap:14px;font-size:12px}
  .small a{color:#6a4a30}
  .empty{grid-column:1/-1;text-align:center;color:var(--cream);font-style:italic;padding:60px 0}
  footer{text-align:center;color:var(--cream);opacity:.8;padding:0 20px 40px;font-size:13px}
</style></head>
<body>
<header><h1>GENERATED VIDEOS</h1><p>Flat 2D poster-style story videos with Indian English narration. Newest first.</p></header>
<main>
%CARDS%
</main>
<footer>Landscape = 1280x720 for YouTube. Shorts = 1080x1920 for YouTube Shorts / Reels. Each card links to the workflow run that made it.</footer>
</body></html>
'''

CARD = '''<article class="card">
  <img src="{dir}/thumb.jpg" alt="{title}" loading="lazy">
  <div class="body">
    <h2 class="title">{title}</h2>
    <p class="meta">{topic}</p>
    <p class="meta">{dur} &middot; {voice} &middot; {date} &middot; <a href="{run_url}">run #{run}</a></p>
    <div class="btns">
      <a class="btn land" href="{dir}/landscape.mp4" download>Download landscape ({land_mb})</a>
      <a class="btn short" href="{dir}/shorts.mp4" download>Download Shorts ({short_mb})</a>
    </div>
    <div class="small"><a href="{dir}/voice.mp3">voice only</a><a href="{dir}/narration.json">timings</a><a href="{raw}/{dir}/landscape.mp4">raw link (landscape)</a><a href="{raw}/{dir}/shorts.mp4">raw link (shorts)</a></div>
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
    dst = root / 'videos' / name
    dst.mkdir(parents=True, exist_ok=True)
    for f in ('landscape.mp4', 'shorts.mp4', 'voice.mp3', 'thumb.jpg', 'narration.json', 'meta.json'):
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    meta = json.loads((src / 'meta.json').read_text(encoding='utf-8')) if (src / 'meta.json').exists() else {}
    narr = json.loads((src / 'narration.json').read_text(encoding='utf-8')) if (src / 'narration.json').exists() else {}
    entry = {'dir': f'videos/{name}', 'slug': a.slug, 'run': a.run, 'run_url': a.run_url, 'title': meta.get('title', a.slug.upper()),
             'topic': meta.get('topic', ''), 'duration': narr.get('duration', 0), 'voice': narr.get('voice', ''),
             'date': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d'),
             'landscape_bytes': (dst / 'landscape.mp4').stat().st_size if (dst / 'landscape.mp4').exists() else 0,
             'shorts_bytes': (dst / 'shorts.mp4').stat().st_size if (dst / 'shorts.mp4').exists() else 0}
    idx = root / 'videos.json'
    entries = json.loads(idx.read_text(encoding='utf-8')) if idx.exists() else []
    entries = [e for e in entries if e['dir'] != entry['dir']]
    entries.insert(0, entry)
    idx.write_text(json.dumps(entries, indent=1, ensure_ascii=False), encoding='utf-8')

    raw = f'https://github.com/{a.repo}/raw/{a.branch}'
    cards = [CARD.format(dir=e['dir'], title=html.escape(e['title']), topic=html.escape(e['topic']), dur=fmt_dur(e['duration'] or 0), voice=html.escape(e['voice']),
                         date=e['date'], run=e['run'], run_url=e['run_url'] or '#', land_mb=f"{e['landscape_bytes'] / 1e6:.0f} MB", short_mb=f"{e['shorts_bytes'] / 1e6:.0f} MB", raw=raw)
             for e in entries] or ['<p class="empty">No videos yet.</p>']
    (root / 'index.html').write_text(PAGE.replace('%CARDS%', '\n'.join(cards)), encoding='utf-8')
    (root / '.nojekyll').write_text('', encoding='utf-8')

    md = ['# Generated videos', '', 'Newest first. Landscape = YouTube 16:9, Shorts = 9:16. Open `index.html` (or enable GitHub Pages on this branch) for the overview page.', '',
          '| Date | Title | Topic | Length | Landscape | Shorts | Run |', '|---|---|---|---|---|---|---|']
    for e in entries:
        md.append(f"| {e['date']} | **{e['title']}** | {e['topic']} | {fmt_dur(e['duration'] or 0)} | [download]({raw}/{e['dir']}/landscape.mp4) ({e['landscape_bytes'] / 1e6:.0f} MB) | [download]({raw}/{e['dir']}/shorts.mp4) ({e['shorts_bytes'] / 1e6:.0f} MB) | [#{e['run']}]({e['run_url']}) |")
    (root / 'README.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    print(f'published {entry["dir"]}; {len(entries)} videos listed')


if __name__ == '__main__':
    main()
