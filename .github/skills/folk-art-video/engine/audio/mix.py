#!/usr/bin/env python3
"""mix.py voice music.wav sfx.wav [out.wav]
Music at exactly -6 dB (50 % level) of the voice's gated loudness, SFX at -6 dB with peaks capped at 0.7 x the voice peak.
The voice is never touched. No ducking, no compression: one gain per stem, plus a peak cap on the SFX stem only."""
import sys
import numpy as np
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dsp import *
import numpy as np

def peak_cap(x, ceiling, block=0.004):
    """gain-only peak limiter for the SFX stem: per-block gain so no hit pokes above the ceiling, smoothed so it does not click"""
    a = np.abs(x).max(0); n = int(block * SR); nb = -(-len(a) // n); pad = np.pad(a, (0, nb * n - len(a)))
    pk = pad.reshape(nb, n).max(1); need = np.minimum(1.0, ceiling / np.maximum(pk, 1e-12))
    need = np.minimum(need, np.minimum(np.r_[1, need[:-1]], np.r_[need[1:], 1]))
    g = np.repeat(need, n)[:len(a)]; k = int(0.01 * SR)
    sm = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(2 * k + 1) / (2 * k + 1), "valid")[:len(a)]
    return x * np.minimum(sm, 1.0)[None, :] * (1.0)

if __name__ == "__main__":
    v = read_wav(sys.argv[1]); m = stereo(read_wav(sys.argv[2])); s = stereo(read_wav(sys.argv[3])); out = sys.argv[4] if len(sys.argv) > 4 else "mix.wav"
    n = v.shape[1]; m = np.pad(m, ((0, 0), (0, max(0, n - m.shape[1]))))[:, :n]; s = np.pad(s, ((0, 0), (0, max(0, n - s.shape[1]))))[:, :n]
    Lv, Lm, Ls = lufs(v), lufs(m), lufs(s)
    m = m * 10 ** ((Lv - 6.0 - Lm) / 20); s = s * 10 ** ((Lv - 6.0 - Ls) / 20)
    vpk = np.abs(v).max(); s = peak_cap(s, 0.7 * vpk); mix = v + m + s
    write_wav(out, mix / max(1.0, np.abs(mix).max()))   # only scaled if it would clip; finish_audio re-measures
    print(f"voice {Lv:.2f} LUFS  peak {20 * np.log10(vpk):.2f} dBFS")
    print(f"music {lufs(m) - Lv:+.2f} dB vs voice (gated)")
    print(f"sfx   {lufs(s) - Lv:+.2f} dB vs voice (gated)   peak {np.abs(s).max() / vpk:.2f} x voice peak")
    print(f"mix   {lufs(mix):.2f} LUFS -> {out}")
