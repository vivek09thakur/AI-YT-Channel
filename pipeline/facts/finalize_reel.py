#!/usr/bin/env python3
"""Finalize a rendered Remotion reel: web-friendly h264 + loudness-normalized AAC, a 9:16 thumbnail, and sanity checks.

usage: finalize_reel.py --in out/reel.mp4 --out final/reel.mp4 --thumb final/thumb.jpg --total 59.0
"""
import argparse, json, subprocess, sys
from pathlib import Path


def sh(*cmd):
    subprocess.run(cmd, check=True)


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height,r_frame_rate',
                        '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video'), {})
    a = next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)
    return float(j['format']['duration']), v.get('width'), v.get('height'), v.get('r_frame_rate'), a is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--thumb', required=True)
    ap.add_argument('--total', type=float, required=True)
    ap.add_argument('--thumb-at', type=float, default=0.3, help='fraction of the video for the thumbnail frame')
    a = ap.parse_args()
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix('.tmp.mp4')
    sh('ffmpeg', '-y', '-v', 'error', '-i', a.src, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '24', '-pix_fmt', 'yuv420p',
       '-movflags', '+faststart', '-c:a', 'copy', str(tmp))
    sh('ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-c:v', 'copy', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '160k',
       '-movflags', '+faststart', str(out))
    tmp.unlink(missing_ok=True)
    sh('ffmpeg', '-y', '-v', 'error', '-ss', f'{a.total * a.thumb_at:.2f}', '-i', str(out), '-frames:v', '1', '-q:v', '3', a.thumb)
    dur, w, h, fr, has_audio = probe(out)
    print(f'{out}: {w}x{h} @{fr} {dur:.2f}s audio={has_audio}')
    problems = []
    if (w, h) != (1080, 1920):
        problems.append(f'size {w}x{h} != 1080x1920')
    if abs(dur - a.total) > 0.6:
        problems.append(f'duration {dur:.2f} != TOTAL {a.total}')
    if not has_audio:
        problems.append('no audio stream')
    if problems:
        sys.exit('final video failed checks: ' + '; '.join(problems))


if __name__ == '__main__':
    main()
