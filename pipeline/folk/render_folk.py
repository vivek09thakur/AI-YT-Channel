#!/usr/bin/env python3
"""render_folk.py --story <kit>/stories/<slug> --voice work/voice.wav --aspect shorts|landscape --out out [--kit ... --workers N --ss 2 --thumb]

Renders one aspect of a folk2d story to <out>/<aspect>.mp4:
  frames (engine/render.py, all cores, errors -> previous frame)  ->  music + sfx stems (audio.py)  ->  mix.py  ->  finish_audio.py
  ->  ffmpeg H.264 CRF 18 + AAC  ->  QA (duration, freeze/black detect as warnings)  ->  optional thumb.jpg (landscape)
Exit 1 only if frames or the mp4 could not be produced at all."""
import argparse, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sh(cmd, env=None, cwd=None, timeout=5400, check=True, quiet=False):
    e = dict(os.environ); e.update(env or {})
    r = subprocess.run([str(c) for c in cmd], env=e, cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    out = (r.stdout or '') + (r.stderr or '')
    if not quiet and out.strip(): print(out.strip()[-4000:], flush=True)
    if check and r.returncode: sys.exit(f'command failed ({r.returncode}): {" ".join(str(c) for c in cmd)}')
    return r.returncode, out


def ffprobe_duration(path):
    _, out = sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], quiet=True)
    try: return float(out.strip().splitlines()[-1])
    except Exception: return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--story', required=True, help='story dir with story.py + phrases.json'); ap.add_argument('--voice', required=True)
    ap.add_argument('--aspect', required=True, choices=['shorts', 'landscape']); ap.add_argument('--out', default='out')
    ap.add_argument('--kit', default=None); ap.add_argument('--workers', type=int, default=max(1, os.cpu_count() or 1)); ap.add_argument('--ss', default='2')
    ap.add_argument('--thumb', action='store_true', help='also write <out>/thumb.jpg (frame at 30 %%)'); ap.add_argument('--frames', default=None, help='debug: render only this range "0-300"')
    a = ap.parse_args()
    t0 = time.time()
    sdir = Path(a.story).resolve(); story = sdir / 'story.py'; phrases = sdir / 'phrases.json'
    kit = Path(a.kit).resolve() if a.kit else sdir.parent.parent
    engine = kit / 'engine'; out = Path(a.out).resolve(); out.mkdir(parents=True, exist_ok=True)
    for p in (story, phrases, engine / 'render.py', Path(a.voice)):
        if not p.exists(): sys.exit(f'missing: {p}')
    ph = json.loads(phrases.read_text(encoding='utf-8')); total = int(ph['total_frames'])
    env = {'FOLK_ASPECT': a.aspect, 'FOLK_PHRASES': str(phrases), 'FOLK_SS': str(a.ss), 'PYTHONPATH': str(engine), 'PYTHONIOENCODING': 'utf-8'}
    work = out / f'work_{a.aspect}'; frames = work / 'frames'; frames.mkdir(parents=True, exist_ok=True)

    # 1. frames
    rng = a.frames or f'0-{total - 1}'
    print(f'[{a.aspect}] rendering frames {rng} with {a.workers} workers (FOLK_SS={a.ss})', flush=True)
    sh([sys.executable, engine / 'render.py', 'frames', rng, '--story', story, '--out', frames, '--workers', a.workers], env=env)
    n = len(list(frames.glob('f*.jpg')))
    want = total if not a.frames else n
    if n < want: sys.exit(f'only {n}/{want} frames were written')
    errs = frames / 'render_errors.json'
    if errs.exists():
        bad = json.loads(errs.read_text(encoding='utf-8'))
        print(f'::warning::{len(bad)} frame(s) failed and were replaced by the previous frame', flush=True)
        if len(bad) > total * 0.05: sys.exit(f'{len(bad)} frames ({len(bad) * 100 // total}%) failed to render; the story is broken')

    # 2. audio: stems -> mix -> finish
    adir = work / 'audio'; adir.mkdir(exist_ok=True)
    sh([sys.executable, engine / 'audio' / 'audio.py', Path(a.voice).resolve(), adir, '--story', story], env=env)
    sh([sys.executable, engine / 'audio' / 'mix.py', Path(a.voice).resolve(), adir / 'music.wav', adir / 'sfx.wav', adir / 'mix.wav'])
    sh([sys.executable, engine / 'audio' / 'finish_audio.py', adir / 'mix.wav', adir / 'final_audio.wav'])

    # 3. encode
    mp4 = out / f'{a.aspect}.mp4'
    sh(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-i', frames / 'f%04d.jpg', '-i', adir / 'final_audio.wav', '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', mp4])
    dur = ffprobe_duration(mp4); vdur = ffprobe_duration(a.voice)
    if dur <= 0: sys.exit('mp4 has no duration')
    if abs(dur - vdur) > 1.0: print(f'::warning::video is {dur:.2f}s but the voice is {vdur:.2f}s', flush=True)

    # 4. QA: freeze / black (warnings only; a frozen frame means a dull shot, not a broken file)
    _, qa = sh(['ffmpeg', '-v', 'info', '-i', mp4, '-vf', 'freezedetect=n=-60dB:d=1.5,blackdetect=d=0.1:pix_th=0.08', '-an', '-f', 'null', '-'], check=False, quiet=True)
    fz = re.findall(r'freeze_start: ([\d.]+)', qa); bl = re.findall(r'black_start:([\d.]+)', qa)
    if fz: print(f'::warning::{len(fz)} frozen span(s) >= 1.5 s at {", ".join(fz[:6])} s', flush=True)
    if bl: print(f'::warning::black frame(s) at {", ".join(bl[:6])} s', flush=True)

    # 5. thumbnail + contact sheet
    if a.thumb:
        sh(['ffmpeg', '-y', '-v', 'error', '-ss', f'{dur * 0.3:.2f}', '-i', mp4, '-frames:v', '1', '-q:v', '2', out / 'thumb.jpg'])
    try:
        qa_dir = work / 'qa'; qa_dir.mkdir(exist_ok=True)
        for i in range(0, n, max(1, n // 42)): shutil.copy(frames / f'f{i:04d}.jpg', qa_dir / f'f{i:04d}.jpg')
        sh([sys.executable, engine / 'sheet.py', qa_dir, out / f'sheet_{a.aspect}.jpg', '7' if a.aspect == 'shorts' else '4'], quiet=True, check=False)
    except Exception as e:
        print(f'(no contact sheet: {e})')
    print(f'[{a.aspect}] done: {mp4} {dur:.2f}s, {n} frames, {time.time() - t0:.0f}s total', flush=True)


if __name__ == '__main__':
    main()
