#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)], capture_output=True, text=True, check=True).stdout.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', required=True)
    ap.add_argument('--voice', required=True)
    ap.add_argument('--fx', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--fx-gain', type=float, default=0.45, help='effects bed level under the voice')
    ap.add_argument('--thumb', default='')
    ap.add_argument('--thumb-at', type=float, default=0.3, help='fraction of the duration for the thumbnail frame')
    a = ap.parse_args()
    fc = (f'[1:a]aformat=channel_layouts=stereo,apad[v];[2:a]volume={a.fx_gain}[e];'
          f'[v][e]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.video, '-i', a.voice, '-i', a.fx, '-filter_complex', fc,
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', a.out], check=True)
    print(f'{a.out}: {dur(a.out):.1f}s, {Path(a.out).stat().st_size / 1e6:.1f} MB')
    if a.thumb:
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{dur(a.video) * a.thumb_at:.2f}', '-i', a.video, '-frames:v', '1', '-q:v', '3', a.thumb], check=True)
        print('thumbnail', a.thumb)


if __name__ == '__main__':
    main()
