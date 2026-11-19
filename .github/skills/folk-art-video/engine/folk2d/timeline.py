"""folk2d.timeline - reads work/phrases.json (made by the pipeline) so shots are timed to the voice, never the other way round.

Phrase lookup is tolerant: case/punctuation-insensitive substring match, then whole-word fuzzy match (difflib).
A lookup that still fails raises KeyError with the closest phrases listed, so the generator can repair the story.
"""
import json, re, difflib, os

def _norm(s):
    s = str(s).lower().replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

class Timeline:
    def __init__(self, path=None):
        path = path or os.environ.get("FOLK_PHRASES") or "work/phrases.json"
        if not os.path.exists(path):
            raise FileNotFoundError(f"phrases file not found: {path} (set FOLK_PHRASES or run pipeline/folk/phrases.py first)")
        d = json.load(open(path, encoding="utf-8"))
        self.fps = d["fps"]; self.total = d["total_frames"]; self.ph = d["phrases"]; self.duration = d["duration"]
        self._norm = [_norm(p["text"]) for p in self.ph]
        self.misses = []
    def idx(self, sub):
        if isinstance(sub, int):
            if 0 <= sub < len(self.ph): return sub
            raise KeyError(f"phrase index {sub} out of range 0..{len(self.ph) - 1}")
        s = str(sub)
        for i, p in enumerate(self.ph):
            if s in p["text"]: return i
        n = _norm(s)
        if n:
            for i, t in enumerate(self._norm):
                if n in t: return i
            # fuzzy: best phrase by word-overlap ratio
            best, score = None, 0.0
            nw = set(n.split())
            for i, t in enumerate(self._norm):
                tw = set(t.split())
                if not nw or not tw: continue
                r = len(nw & tw) / len(nw)
                r2 = difflib.SequenceMatcher(None, n, t).ratio()
                sc = max(r, r2)
                if sc > score: best, score = i, sc
            if best is not None and score >= 0.6:
                self.misses.append((s, self.ph[best]["text"]))
                return best
        close = difflib.get_close_matches(n, self._norm, n=3, cutoff=0.0)
        raise KeyError(f"no phrase contains: {sub!r}; closest phrases: {close}")
    def span(self, a, b=None):
        """(first_frame, last_frame) from the phrase containing a to the phrase containing b"""
        i = self.idx(a); j = self.idx(b) if b is not None else i
        if j < i: i, j = j, i
        return self.ph[i]["f0"], self.ph[j]["f1"]
    def start(self, sub): return self.ph[self.idx(sub)]["f0"]
    def end(self, sub): return self.ph[self.idx(sub)]["f1"]
    def word(self, sub, n):
        """frame where the n-th word (0-based) of the phrase containing sub is spoken"""
        p = self.ph[self.idx(sub)]
        if not p.get("words"): return p["f0"]
        n = max(0, min(int(n), len(p["words"]) - 1)); return p["words"][n]["f"]
    def text(self, sub): return self.ph[self.idx(sub)]["text"]
    def sub(self, f, hold=10):
        """(text, pop progress 0..1) of the subtitle at frame f"""
        for i, p in enumerate(self.ph):
            nxt = self.ph[i + 1]["f0"] if i + 1 < len(self.ph) else self.total
            if p["f0"] <= f < min(nxt, p["f1"] + hold): return p["text"], min(1.0, (f - p["f0"]) / 6.0)
        return None, 0.0
