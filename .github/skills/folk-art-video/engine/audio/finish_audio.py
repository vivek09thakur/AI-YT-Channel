#!/usr/bin/env python3
"""finish_audio.py mix.wav out.wav : ONE linear gain to about -14 LUFS (keeps the voice:music:sfx ratio), then a -1 dBFS peak limiter."""
import sys, subprocess
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsp import *
x = read_wav(sys.argv[1]); L = lufs(x); g = 10 ** ((-14.0 - L) / 20)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", "alimiter=limit=0.891:level=false:attack=3:release=60", "-ar", "48000", sys.argv[2]],
               input=(x * g).T.astype("<f4").tobytes(), check=True)
print(f"mix was {L:.2f} LUFS -> gain {20 * np.log10(g):+.2f} dB, limited at -1 dBFS")
