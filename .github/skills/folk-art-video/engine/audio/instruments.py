"""Indian-flavoured synth voices + SFX, numpy only. Every function returns a mono float array."""
import numpy as np
from dsp import *
NOTE = {"S": 0, "r": 1, "R": 2, "g": 3, "G": 4, "m": 5, "P": 7, "d": 8, "D": 9, "n": 10, "N": 11}
def hz(sa, n, octv=0): return sa * 2 ** ((NOTE[n] + 12 * octv) / 12)

def tanpura(dur, sa=146.83, gain=1.0):
    t = t_(dur); x = np.zeros_like(t)
    for k, (n, o) in enumerate([("P", -1), ("S", 0), ("S", 0), ("S", -1)]):
        f = hz(sa, n, o); ph = (t * 1.0 - k * 0.5) % 2.0; e = np.exp(-ph * 1.3) * (ph < 2)
        for h, a in ((1, 1), (2, .6), (3, .45), (4, .3), (5, .22), (6, .15)): x += a * e * np.sin(2 * np.pi * f * h * t + 0.3 * h)
    return x / 9 * gain
def bansuri(dur, f0, vib=5.0, gain=1.0):
    t = t_(dur); f = f0 * (1 + 0.006 * np.sin(2 * np.pi * vib * t) * np.minimum(1, t / 0.25))
    ph = 2 * np.pi * np.cumsum(f) / SR; x = np.sin(ph) + 0.25 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    x += 0.05 * bandpass(noise(len(t)), 1500, 6000); return x * env(len(t), 0.07, 0.1, 0.8, 0.18) * 0.22 * gain
def tabla(kind="na", gain=1.0):
    if kind == "ge": t = t_(0.4); f = 110 * np.exp(-t * 8) + 55; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * 0.9 * gain
    t = t_(0.25); x = np.sin(2 * np.pi * 420 * t) * np.exp(-t * 28) + 0.5 * np.sin(2 * np.pi * 840 * t) * np.exp(-t * 35); return x * 0.5 * gain
def dhol(gain=1.0):
    t = t_(0.7); f = 150 * np.exp(-t * 14) + 48; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    x += 0.4 * lowpass(noise(len(t), 1), 2500) * np.exp(-t * 40); return x * gain
def whoosh(dur=0.7, up=False, gain=1.0):
    n = int(dur * SR); x = noise(n, 5); sweep = np.linspace(0.15, 1, n) if up else np.linspace(1, 0.15, n)
    out = np.zeros(n); k = 6
    for i in range(k):
        a, b = int(i * n / k), int((i + 1) * n / k); lo = 300 + 4500 * sweep[(a + b) // 2]; out[a:b] = bandpass(x[a:b], lo * 0.6, lo * 1.4) if b - a > 64 else 0
    return out * np.sin(np.linspace(0, np.pi, n)) ** 1.5 * 0.9 * gain
def thunk(gain=1.0):
    t = t_(0.35); f = 140 * np.exp(-t * 20) + 50; return (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * lowpass(noise(len(t), 2), 800)) * np.exp(-t * 14) * gain
def chime(f0=1046.5, dur=2.2, gain=1.0):
    t = t_(dur); x = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * d) for r, a, d in ((1, 1, 1.6), (2.76, .5, 2.4), (5.4, .3, 3.5), (8.9, .15, 5)))
    return x * 0.5 * gain
def bell(f0=392, dur=3.0, gain=1.0):
    t = t_(dur); x = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t * d) for r, a, d in ((1, 1, .9), (2.0, .6, 1.2), (2.4, .4, 1.5), (3.0, .3, 1.8), (4.2, .2, 2.5)))
    return x * 0.45 * gain
def sparkle(gain=1.0):
    out = np.zeros(int(1.1 * SR))
    for i, f in enumerate((2093, 2637, 3136, 3951, 4186)):
        s = int(i * 0.07 * SR); t = t_(0.5); seg = np.sin(2 * np.pi * f * t) * np.exp(-t * 9) * 0.35; out[s:s + len(seg)] += seg[:len(out) - s]
    return out * gain
def slice_(gain=1.0):
    t = t_(0.28); x = bandpass(noise(len(t), 3), 3500, 12000) * np.exp(-t * 30) + 0.5 * np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 18)
    return x * 0.8 * gain
def rumble(dur=1.6, gain=1.0):
    n = int(dur * SR); return lowpass(noise(n, 4), 120) * np.hanning(n) * 4.0 * gain
def swell(dur=2.4, gain=1.0):
    t = t_(dur); x = sum(np.sin(2 * np.pi * f * t) for f in (146.83, 220.0, 293.66, 369.99, 440.0)) * (t / dur) ** 2 * np.minimum(1, (dur - t) / 0.4 + 0.0)
    return x * 0.18 * gain
def heart(gain=1.0):
    def b(): t = t_(0.18); return np.sin(2 * np.pi * 58 * t) * np.exp(-t * 22)
    out = np.zeros(int(0.7 * SR)); a = b(); out[:len(a)] += a; s = int(0.24 * SR); out[s:s + len(a)] += 0.7 * a; return out * gain
def pop(gain=1.0):
    t = t_(0.12); return np.sin(2 * np.pi * (400 + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 35) * 0.7 * gain
def click(gain=1.0):
    t = t_(0.05); return bandpass(noise(len(t), 9), 1800, 6000) * np.exp(-t * 90) * gain
def drip(gain=1.0):
    t = t_(0.3); return np.sin(2 * np.pi * (900 - 500 * t) * t) * np.exp(-t * 16) * 0.6 * gain
LIB = dict(whoosh=lambda g=1: whoosh(0.7, False, g), riser=lambda g=1: whoosh(1.1, True, g), thunk=thunk, chime=chime, bell=bell, sparkle=sparkle, slice=slice_, dhol=dhol,
           rumble=rumble, swell=swell, heart=heart, pop=pop, click=click, drip=drip)
