"""numpy-only DSP helpers + WAV io"""
import numpy as np, wave, subprocess
SR = 48000
def t_(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, d=0.2, s=0.0, r=0.1):
    e = np.ones(n); na, nd, nr = int(a * SR), int(d * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, max(na, 1)); 
    if nd: e[na:na + nd] = np.linspace(1, s, nd)[:max(0, n - na)]
    e[na + nd:] = s
    if nr: e[-nr:] *= np.linspace(1, 0, nr)[:len(e[-nr:])]
    return e
def noise(n, seed=0): return np.random.RandomState(seed).randn(n)
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def lowpass(x, hi): return bandpass(x, 0, hi)
def norm(x, peak=1.0): m = np.abs(x).max(); return x * (peak / m) if m > 0 else x
def stereo(x): return np.vstack([x, x]) if x.ndim == 1 else x
def write_wav(path, x):
    x = np.clip(stereo(x), -1, 1); pcm = (x.T * 32767).astype("<i2")
    with wave.open(path, "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
def read_wav(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64).reshape(-1, 2).T
def lufs(x):
    """integrated loudness (BS.1770 gated) via ffmpeg ebur128; float samples are piped, nothing is clipped"""
    import re
    x = stereo(x).astype("<f4")
    r = subprocess.run(["ffmpeg", "-nostats", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-filter_complex", "ebur128", "-f", "null", "-"],
                       input=x.T.tobytes(), capture_output=True).stderr.decode(errors="ignore")
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r); return float(m[-1]) if m else -70.0
