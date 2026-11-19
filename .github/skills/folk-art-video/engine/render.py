#!/usr/bin/env python3
"""render.py frames "0-1799" [--story story.py] [--out frames] [--workers N]   (RESUME=1 skips frames that exist)
   render.py stills "10,90,200" [--out stills]                                (quick look at single frames)

Aspect comes from the FOLK_ASPECT env var (shorts | landscape), supersampling from FOLK_SS.
A frame whose render raises is NOT fatal: the error is logged, the frame is re-drawn as the nearest earlier
good frame (or a plain dark frame) and the run continues; the error list is written to <out>/render_errors.json.
Set FOLK_STRICT=1 to make any frame error fatal (the pipeline's check step does this).
"""
import sys, os, importlib.util, argparse, time, json, traceback
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def load(path):
    path = os.path.abspath(path)
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("story", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
def parse(s):
    out = []
    for part in str(s).split(","):
        part = part.strip()
        if not part: continue
        if "-" in part: a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else: out.append(int(part))
    return out
_S = None; _OUT = "frames"; _STORY = "story.py"; _STRICT = os.environ.get("FOLK_STRICT") == "1"
def _init(story, out):
    global _STORY, _OUT
    _STORY, _OUT = story, out
def _fallback(f, err):
    """nearest earlier rendered frame, else a dark frame"""
    from PIL import Image
    for g in range(f - 1, max(-1, f - 40), -1):
        p = os.path.join(_OUT, f"f{g:04d}.jpg")
        if os.path.exists(p):
            try: return Image.open(p).convert("RGB")
            except Exception: pass
    from folk2d.draw import OW, OH
    return Image.new("RGB", (OW, OH), (16, 10, 30))
def work(f):
    global _S
    if _S is None: _S = load(_STORY)
    p = os.path.join(_OUT, f"f{f:04d}.jpg")
    if os.environ.get("RESUME") and os.path.exists(p): return (f, None)
    try:
        img = _S.render_frame(f)
        img.save(p, quality=93); return (f, None)
    except Exception as e:
        err = f"frame {f}: {type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"
        if _STRICT: raise RuntimeError(err) from e
        _fallback(f, err).save(p, quality=93); return (f, err)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode"); ap.add_argument("frames"); ap.add_argument("--story", default="story.py"); ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 1))); ARGS = ap.parse_args()
    _OUT = ARGS.out or ("frames" if ARGS.mode == "frames" else "stills"); os.makedirs(_OUT, exist_ok=True)
    _STORY = os.path.abspath(ARGS.story)
    fr = parse(ARGS.frames); t = time.time(); errors = []
    def note(res, i):
        f, err = res
        if err:
            errors.append(err)
            if len(errors) <= 5: print("  ! " + err.splitlines()[0], flush=True)
        if i % 100 == 0: print(f"{i + 1}/{len(fr)} ({time.time() - t:.0f}s)", flush=True)
    if ARGS.workers > 1 and len(fr) > 4:
        with Pool(ARGS.workers, initializer=_init, initargs=(_STORY, _OUT)) as pool:
            for i, res in enumerate(pool.imap(work, fr, chunksize=4)): note(res, i)
    else:
        for i, f in enumerate(fr): note(work(f), i)
    if errors:
        json.dump(errors, open(os.path.join(_OUT, "render_errors.json"), "w"), indent=1)
        print(f"WARNING: {len(errors)} frame(s) failed and were replaced by the previous frame (see {_OUT}/render_errors.json)")
    print(f"done {len(fr)} frames in {time.time() - t:.0f}s -> {_OUT}/")
