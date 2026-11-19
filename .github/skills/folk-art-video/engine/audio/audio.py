#!/usr/bin/env python3
"""audio.py voice.(mp3|wav) [out_dir] [--story path/story.py]  -> music.wav + sfx.wav stems (voice untouched). Reads CUES / MUSIC from the story.
CUES   = [(frame, "whoosh", gain), ...]        names: whoosh riser thunk chime bell sparkle slice dhol rumble swell heart pop click drip
MUSIC  = dict(stop=frame|None, back=frame|None, sa=146.83, mood="bright"|"dark"|"calm", tempo=76)
         music = tanpura + bansuri phrase + soft tabla; stops on the twist, drone stays, returns later.
Unknown cue names are skipped with a warning (never fatal)."""
import sys, os, importlib.util, subprocess, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from dsp import *
import instruments as I

CUE_ALIASES = {"boom": "thunk", "hit": "thunk", "impact": "thunk", "drum": "dhol", "drums": "dhol", "thunder": "rumble", "sparkles": "sparkle", "twinkle": "sparkle", "shimmer": "sparkle",
               "swoosh": "whoosh", "swish": "whoosh", "rise": "riser", "sword": "slice", "cut": "slice", "heartbeat": "heart", "ding": "chime", "temple_bell": "bell", "gong": "bell",
               "tap": "click", "water": "drip", "splash": "drip", "wind": "swell", "magic": "sparkle", "fire": "rumble", "roar": "rumble", "crowd": "swell", "bow": "slice", "arrow": "whoosh"}
PHRASES = {
    "bright": [("G", 0, 1.1), ("R", 0, .6), ("S", 0, 1.2), ("D", -1, .9), ("P", -1, 1.4), ("G", 0, .8), ("P", 0, 1.1), ("G", 0, .7), ("R", 0, .7), ("S", 0, 1.8)],
    "dark":   [("S", 0, 1.3), ("r", 0, .9), ("S", 0, .8), ("N", -1, 1.1), ("d", -1, 1.4), ("P", -1, 1.6), ("d", -1, .8), ("r", 0, 1.0), ("S", 0, 2.0)],
    "calm":   [("S", 0, 1.6), ("R", 0, 1.0), ("G", 0, 1.4), ("P", 0, 1.8), ("G", 0, 1.0), ("R", 0, 1.2), ("S", 0, 2.4)],
}

def load_story(path):
    spec = importlib.util.spec_from_file_location("story", path); S = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(path))); sys.path.insert(0, os.path.dirname(HERE)); spec.loader.exec_module(S); return S

def main(voice, out=".", story=None):
    story = story or os.path.join(HERE, "..", "story.py")
    S = load_story(story)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", voice], capture_output=True, text=True).stdout.strip())
    n = int(dur * SR); fps = 30
    sfx = np.zeros(n); music = np.zeros(n)
    cues = list(getattr(S, "CUES", []) or []); used = 0; skipped = []
    for cue in cues:
        try:
            fr, name = cue[0], str(cue[1]).strip().lower(); g = float(cue[2]) if len(cue) > 2 else 1.0
            name = CUE_ALIASES.get(name, name)
            if name not in I.LIB: skipped.append(cue); continue
            g = max(0.0, min(2.0, g))
            s = int(float(fr) / fps * SR); w = I.LIB[name](g); e = min(n, s + len(w))
            if 0 <= s < n: sfx[s:e] += w[:e - s]; used += 1
        except Exception as ex:
            skipped.append((cue, str(ex)))
    M = getattr(S, "MUSIC", {}) or {}
    try: sa = float(M.get("sa", 146.83))
    except Exception: sa = 146.83
    if not (60 <= sa <= 400): sa = 146.83
    drone = I.tanpura(dur, sa) * 1.0
    phrase = PHRASES.get(str(M.get("mood", "bright")).lower(), PHRASES["bright"])
    mel = np.zeros(n); t0 = 1.5; k = 0
    while t0 < dur - 1:
        for nm, o, d in phrase:
            if t0 + d > dur: break
            f0 = I.hz(sa * 2, nm, o); w = I.bansuri(d, f0); s = int(t0 * SR); mel[s:s + len(w)] += w[:n - s]; t0 += d * 1.02
        t0 += 2.2; k += 1
    try: tempo = float(M.get("tempo", 76))
    except Exception: tempo = 76
    tempo = max(50, min(120, tempo))
    beat = 60 / tempo; pulse = np.zeros(n); i = 0
    while i * beat < dur:
        s = int(i * beat * SR); kind = "ge" if i % 4 in (0, 2) else "na"; w = I.tabla(kind, 0.8 if kind == "ge" else 0.5); e = min(n, s + len(w)); pulse[s:e] += w[:e - s]; i += 1
    def frame_or_none(v):
        try: return None if v is None else int(v)
        except Exception: return None
    stop = frame_or_none(M.get("stop")); back = frame_or_none(M.get("back")); gate = np.ones(n)
    if stop is not None and 0 < int(stop / fps * SR) < n:
        a = int(stop / fps * SR); fa = min(a, int(0.25 * SR)); gate[a:] = 0.0; gate[a - fa:a] = np.linspace(1, 0, fa)
        if back is not None and a < int(back / fps * SR) < n:
            b = int(back / fps * SR); fb = min(n - b, int(0.4 * SR)); gate[b:] = 1.0; gate[b:b + fb] = np.linspace(0, 1, fb)
    music = (mel * 0.9 + pulse * 0.45) * gate + drone * (0.45 + 0.55 * gate)
    fade = np.minimum(1, np.minimum(np.arange(n) / (1.0 * SR), (n - np.arange(n)) / (1.5 * SR))); music *= fade
    os.makedirs(out, exist_ok=True)
    write_wav(os.path.join(out, "music.wav"), norm(music, 0.8)); write_wav(os.path.join(out, "sfx.wav"), norm(sfx, 0.9) if np.abs(sfx).max() > 0 else sfx)
    print(f"stems: {dur:.2f}s, {used} sfx cues used, {len(skipped)} skipped, music stop={stop} back={back}")
    for s_ in skipped[:10]: print("  skipped cue:", s_)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("voice"); ap.add_argument("out", nargs="?", default="."); ap.add_argument("--story", default=None)
    a = ap.parse_args(); main(a.voice, a.out, a.story)
