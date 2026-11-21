#!/usr/bin/env python3
"""phrases.py --narration work/narration.json --out work/phrases.json [--fps 30] [--max-words 9]

Turns the exact per-line timings written by pipeline/tts.py into the phrases.json the folk engine's Timeline reads:
  {fps, duration, total_frames, phrases:[{i, text, t0, t1, f0, f1, words:[{w, f}]}]}
Every narration line keeps its measured [t0, t1]; long lines are split into caption-sized phrases at commas / clause
breaks (<= max-words words each) and the line's time is shared between the pieces by character weight.
The phrase text is always the exact narration text, so subtitles match the voice word for word.
"""
import argparse, json, os, re

STOP = {"the", "a", "an", "of", "to", "in", "and", "or", "but", "as", "at", "by", "for", "on", "with", "is", "was", "were", "be", "his", "her", "its", "their"}

def weight(s): return max(1, len(re.sub(r"[\s\W_]+", "", s)))

def split_line(text, max_words):
    words = text.split()
    if len(words) <= max_words: return [text]
    # candidate break points: after a comma / semicolon / colon / dash / ellipsis
    breaks = [i + 1 for i, w in enumerate(words[:-1]) if re.search(r"[,;:\u2014\u2013]$|\.\.\.$|\u2026$", w)]
    best = None
    for b in breaks:
        if 2 <= b <= len(words) - 2:
            # do not break right after a stop word (keeps "of" with its noun)
            if words[b - 1].lower().strip(",;:") in STOP: continue
            if best is None or abs(b - len(words) / 2) < abs(best - len(words) / 2): best = b
    if best is None:
        # no punctuation: break near the middle, before a stop word if possible
        mid = len(words) // 2; cands = [i for i in range(max(2, mid - 3), min(len(words) - 2, mid + 4)) if words[i].lower() in STOP]
        best = min(cands, key=lambda i: abs(i - mid)) if cands else mid
    left, right = " ".join(words[:best]), " ".join(words[best:])
    return split_line(left, max_words) + split_line(right, max_words)

def build(narr, fps=30, max_words=9):
    dur = float(narr["duration"]); out = []; i = 0
    for L in narr["lines"]:
        t0, t1 = float(L["t0"]), float(L["t1"]); text = re.sub(r"\s+", " ", L["text"]).strip()
        if not text or t1 <= t0: continue
        parts = split_line(text, max_words); W = [weight(p) for p in parts]; tot = sum(W); acc = 0.0
        for p, w in zip(parts, W):
            p0 = t0 + (t1 - t0) * acc / tot; acc += w; p1 = t0 + (t1 - t0) * acc / tot
            ws = p.split(); cw = [weight(x) for x in ws]; tc = sum(cw); a2 = 0; words = []
            for x, c in zip(ws, cw):
                words.append({"w": x, "f": int(round((p0 + (p1 - p0) * a2 / tc) * fps))}); a2 += c
            out.append({"i": i, "line": L.get("i", 0), "text": p, "t0": round(p0, 3), "t1": round(p1, 3), "f0": int(round(p0 * fps)), "f1": int(round(p1 * fps)), "words": words}); i += 1
    # guarantee strictly increasing, non-overlapping frames
    for a, b in zip(out, out[1:]):
        if b["f0"] < a["f1"]: b["f0"] = a["f1"]
        if b["f1"] <= b["f0"]: b["f1"] = b["f0"] + 1
    return {"fps": fps, "duration": round(dur, 3), "total_frames": int(round(dur * fps)), "phrases": out}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--narration", default="work/narration.json"); ap.add_argument("--out", default="work/phrases.json")
    ap.add_argument("--fps", type=int, default=30); ap.add_argument("--max-words", type=int, default=9); a = ap.parse_args()
    narr = json.load(open(a.narration, encoding="utf-8")); d = build(narr, a.fps, a.max_words)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(d, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{d['duration']:.2f}s = {d['total_frames']} frames @ {a.fps}fps, {len(d['phrases'])} phrases from {len(narr['lines'])} lines")
    for p in d["phrases"]: print(f"{p['i']:>3} f{p['f0']:>5}-{p['f1']:<5} {p['text'][:70].encode('ascii', 'replace').decode()}")
