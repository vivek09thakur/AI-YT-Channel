#!/usr/bin/env python3
"""timing.py voice.mp3 script.txt [--out work] [--fps 30]     -> work/phrases.json (frame timing of every phrase and word)
   timing.py --estimate script.txt [--wps 2.4] [--out work]   -> same, from the script alone (preview before the voiceover exists)

No speech recognition needed: the script is split into phrases, the voice is cut into speech segments with ffmpeg silencedetect,
and phrase boundaries are laid out by text length over the speech time, then snapped to the nearest real pause.
If whisper / faster-whisper is installed you can replace this with exact word timestamps, but check the pauses either way."""
import sys, re, json, os, subprocess, argparse

def split_script(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = []
    for ln in lines:
        parts = re.findall(r'[^।.?!]+[।.?!]+[”"\')]*|[^।.?!]+$', ln) or [ln]
        for s in parts:
            s = s.strip()
            if not s: continue
            words = s.split()
            if len(words) > 15 and "," in s:                       # long sentence: split at the comma nearest the middle
                cs = [m.start() for m in re.finditer(",", s)]
                mid = len(s) / 2; k = min(cs, key=lambda c: abs(c - mid))
                out += [s[:k + 1].strip(), s[k + 1:].strip()]
            else: out.append(s)
    return [o for o in out if o]

def weight(s): return max(1, len(re.sub(r"[\s\W_]+", "", s, flags=re.UNICODE)))

def speech_segments(voice, noise="-35dB", d=0.20):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice], capture_output=True, text=True).stdout.strip())
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", voice, "-af", f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    sil = []
    for i, a in enumerate(st): sil.append((max(0, a), en[i] if i < len(en) else dur))
    seg, cur = [], 0.0
    for a, b in sil:
        if a - cur > 0.05: seg.append((cur, a))
        cur = b
    if dur - cur > 0.05: seg.append((cur, dur))
    return dur, seg, sil

def lay_out(phrases, dur, seg, sil):
    W = [weight(p) for p in phrases]; tot = sum(W); Ts = sum(b - a for a, b in seg)
    def to_real(sp):                                              # position in "speech time" -> real time
        for a, b in seg:
            if sp <= b - a: return a + sp
            sp -= (b - a)
        return seg[-1][1]
    bounds, acc = [0.0], 0
    for w in W[:-1]:
        acc += w; bounds.append(to_real(Ts * acc / tot))
    bounds.append(dur)
    gaps = [(a + b) / 2 for a, b in sil if b - a >= 0.18]
    snapped = [bounds[0]]
    for k in range(1, len(bounds) - 1):
        near = [g for g in gaps if abs(g - bounds[k]) < 0.6 and g > snapped[-1] + 0.15]
        snapped.append(min(near, key=lambda g: abs(g - bounds[k])) if near else max(bounds[k], snapped[-1] + 0.15))
    snapped.append(dur)
    return snapped

def estimate(phrases, wps):
    t, b = 0.0, [0.0]
    for p in phrases:
        t += len(p.split()) / wps + (0.45 if re.search(r"[।.?!][”\"']*$", p) else 0.15); b.append(t)
    return b[-1], b

def build(phrases, bounds, dur, fps):
    out = []
    for i, p in enumerate(phrases):
        t0, t1 = bounds[i], bounds[i + 1]; ws = p.split(); cw = [weight(w) for w in ws]; tc = sum(cw); acc = 0; words = []
        for w, c in zip(ws, cw):
            words.append({"w": w, "f": int(round((t0 + (t1 - t0) * acc / tc) * fps))}); acc += c
        out.append({"i": i, "text": p, "t0": round(t0, 3), "t1": round(t1, 3), "f0": int(round(t0 * fps)), "f1": int(round(t1 * fps)), "words": words})
    return {"fps": fps, "duration": round(dur, 3), "total_frames": int(round(dur * fps)), "phrases": out}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("args", nargs="+"); ap.add_argument("--out", default="work"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--estimate", action="store_true"); ap.add_argument("--wps", type=float, default=2.4); a = ap.parse_args()
    if a.estimate: script = a.args[0]; voice = None
    else: voice, script = a.args[0], a.args[1]
    phrases = split_script(open(script, encoding="utf-8").read())
    if voice:
        dur, seg, sil = speech_segments(voice); bounds = lay_out(phrases, dur, seg, sil)
    else: dur, bounds = estimate(phrases, a.wps)
    d = build(phrases, bounds, dur, a.fps); os.makedirs(a.out, exist_ok=True)
    json.dump(d, open(os.path.join(a.out, "phrases.json"), "w"), ensure_ascii=False, indent=1)
    print(f"{'ESTIMATE' if not voice else 'voice'}: {dur:.2f}s = {d['total_frames']} frames @ {a.fps}fps, {len(phrases)} phrases, {sum(len(p.split()) for p in phrases)} words")
    for p in d["phrases"]: print(f"{p['i']:>2} f{p['f0']:>5}-{p['f1']:<5} {p['t0']:6.2f}s  {p['text'][:60]}")
    print("Check: pauses should sit at sentence ends. If not, fix the script text (it must match what was recorded) and rerun.")
