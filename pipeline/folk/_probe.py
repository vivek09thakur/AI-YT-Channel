"""_probe.py (run by check_story.py in a subprocess with secrets scrubbed) - imports the story and renders sampled frames.
Prints one JSON line: {"problems": [...], "warnings": [...], "frames": n}. Must never crash itself; every failure becomes a problem."""
import argparse, importlib.util, json, os, sys, traceback

ap = argparse.ArgumentParser(); ap.add_argument('--story', required=True); ap.add_argument('--step', type=int, default=15); ap.add_argument('--sheet', default=None)
a = ap.parse_args()
ASPECT = os.environ.get('FOLK_ASPECT', 'shorts'); TAG = f'[{ASPECT}] '
problems, warnings = [], []
FINAL = {'problems': problems, 'warnings': warnings, 'frames': 0}


def done():
    print(json.dumps(FINAL)); sys.exit(0)


def tb(e, limit=6):
    lines = traceback.format_exception(type(e), e, e.__traceback__, limit=limit)
    story_base = os.path.basename(a.story)
    keep = [l.rstrip() for l in lines if story_base in l or 'folk2d' in l or not l.startswith('  File')]
    return '\n'.join(keep[-8:])[:1200]


try:
    import numpy as np
    import folk2d
    from folk2d import cast, animals, timeline
    from folk2d.draw import OW, OH
    ENGINE = os.path.dirname(os.path.abspath(folk2d.__file__ if not hasattr(folk2d, '__path__') else list(folk2d.__path__)[0]))
    sys.path.insert(0, os.path.join(ENGINE, 'audio'))
    import instruments as INSTR
    _sp = importlib.util.spec_from_file_location('folk_audio', os.path.join(ENGINE, 'audio', 'audio.py')); _am = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_am)
    CUE_ALIASES = _am.CUE_ALIASES
except Exception as e:
    problems.append('engine failed to import (pipeline bug, not the story): ' + tb(e)); done()

# ---- import the story
try:
    spec = importlib.util.spec_from_file_location('story', a.story); S = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.abspath(a.story))); spec.loader.exec_module(S)
except KeyError as e:
    problems.append(f'phrase lookup failed while importing story.py: {e}. Use verbatim substrings of the phrases in the brief.'); done()
except Exception as e:
    problems.append('story.py failed to import: ' + tb(e)); done()

T = getattr(S, 'T', None)
if not isinstance(T, timeline.Timeline): problems.append('T must be `Timeline()` from folk2d.timeline'); done()
total = T.total
for miss, actual in T.misses:
    problems.append(f'phrase lookup {miss!r} did not match any phrase exactly (nearest: {actual!r}); copy the phrase text verbatim from the brief')

# ---- shots
shots = getattr(S, 'SHOTS', None)
if not isinstance(shots, (list, tuple)) or not shots: problems.append('SHOTS is empty or not a list'); done()
try:
    shots = [(str(n), int(x), int(y)) for n, x, y in shots]
except Exception:
    problems.append('SHOTS must be a list of (name, first_frame, last_frame_exclusive)'); done()
if shots[0][1] != 0: problems.append(f'first shot {shots[0][0]!r} must start at frame 0 (starts at {shots[0][1]})')
if shots[-1][2] != total: problems.append(f'last shot {shots[-1][0]!r} must end at T.total={total} (ends at {shots[-1][2]})')
for i, (n, x, y) in enumerate(shots):
    if y <= x: problems.append(f'shot {n!r} is empty or reversed ({x}..{y}); check SHOT_DEFS order against the narration order')
    if i and x != shots[i - 1][2]: problems.append(f'shots {shots[i - 1][0]!r} and {n!r} do not join ({shots[i - 1][2]} vs {x})')
    if n not in getattr(S, 'FN', {}): problems.append(f'FN has no entry for shot {n!r}')
if len(shots) < 3: problems.append(f'only {len(shots)} shots; use 8-16 shots so the picture changes with the narration')
if problems: done()

# ---- cues / music
LIB = set(INSTR.LIB)
cues = getattr(S, 'CUES', None)
if not isinstance(cues, (list, tuple)): problems.append('CUES must be a list of (frame, name, gain)')
else:
    bad = {}
    for c in cues:
        try:
            fr, name = int(c[0]), str(c[1]).strip().lower(); canon = CUE_ALIASES.get(name, name)
            if canon not in LIB: bad.setdefault(f'unknown cue name {name!r} (use: {" ".join(sorted(LIB))})', 0)
            if not 0 <= fr <= total: bad.setdefault(f'cue frame {fr} outside 0..{total}', 0)
        except Exception:
            bad.setdefault(f'malformed cue {c!r}', 0)
    problems += list(bad)
    if len(cues) < max(4, len(shots) // 2): warnings.append(f'only {len(cues)} sound cues; aim for one per phrase start')
M = getattr(S, 'MUSIC', None)
if not isinstance(M, dict): problems.append('MUSIC must be a dict(stop=, back=, sa=, mood=, tempo=)')
elif str(M.get('mood', 'bright')).lower() not in ('bright', 'dark', 'calm'): problems.append(f'MUSIC mood {M.get("mood")!r} must be bright, dark or calm')

# ---- count characters per frame by wrapping the drawing functions the story sees
COUNT = {'n': 0}
real_char, real_animal = cast.draw_char, animals.draw_animal
def wrap_char(*args, **kw):
    COUNT['n'] += 1; return real_char(*args, **kw)
def wrap_animal(*args, **kw):
    COUNT['n'] += 1; return real_animal(*args, **kw)
for mod in (S, cast, animals, folk2d):
    if getattr(mod, 'draw_char', None) is real_char: mod.draw_char = wrap_char
    if getattr(mod, 'draw_animal', None) is real_animal: mod.draw_animal = wrap_animal

# ---- sample frames
sample = []
for n, x, y in shots:
    sample += [x, (x + y) // 2, max(x, y - 1)]
sample += list(range(0, total, max(1, a.step)))
sample = sorted(set(f for f in sample if 0 <= f < total))
shot_of = {}
for n, x, y in shots:
    for f in sample:
        if x <= f < y: shot_of[f] = n
chars = {n: [] for n, _, _ in shots}
errors = {}; flat = []; slow = []; mids = {}
import time
for f in sample:
    COUNT['n'] = 0; t0 = time.time()
    try:
        img = S.render_frame(f)
    except Exception as e:
        key = tb(e).splitlines()[-1][:160]
        errors.setdefault(key, []).append(f); continue
    dt = time.time() - t0
    if dt > 6: slow.append((f, dt))
    try:
        if img is None or img.size != (OW, OH): problems.append(f'render_frame({f}) must return c.finish() ({OW}x{OH} image), got {None if img is None else img.size}'); break
        arr = np.asarray(img.convert('L').resize((96, 54 if OW > OH else 96)), dtype=np.float32)
        near_cut = any(x <= f < x + 8 for _, x, _ in shots)      # a white flash on a cut is fine
        if arr.std() < 6 and not (near_cut and arr.mean() > 150): flat.append(f)
    except Exception as e:
        problems.append(f'render_frame({f}) returned something that is not a PIL image: {e}'); break
    chars[shot_of[f]].append(COUNT['n'])
    for n, x, y in shots:
        if f == (x + y) // 2: mids[n] = img
FINAL['frames'] = len(sample)
for key, fs in errors.items():
    fs = sorted(fs); problems.append(f'{TAG}render_frame raised at frames {fs[:6]}{"..." if len(fs) > 6 else ""} (shot {shot_of.get(fs[0])!r}): {key}')
    full = None
    try: S.render_frame(fs[0])
    except Exception as e: full = tb(e)
    if full: problems[-1] += '\n' + full
if flat: problems.append(f'{TAG}frames {flat[:8]} are nearly blank / single-colour; every frame needs a sky, ground, characters')
if slow: warnings.append(f'{TAG}slow frames (>6s at FOLK_SS=1): {[(f, round(d, 1)) for f, d in slow[:5]]}; simplify the shot')
for i, (n, x, y) in enumerate(shots):
    cs = chars[n]
    if not cs: continue
    empty = sum(1 for c in cs if c == 0)
    if empty and i < len(shots) - 1: problems.append(f'shot {n!r} draws no character or animal in {empty} of {len(cs)} sampled frames; every shot must call draw_char/draw_animal in every frame')
    elif empty == len(cs): problems.append(f'final shot {n!r} never draws a character; show the hero on the title card')
if cast.WARNINGS:
    seen = []
    for w in cast.WARNINGS:
        if w not in seen: seen.append(w)
    problems += [f'{w}' for w in seen[:12]]

# ---- contact sheet of shot midpoints
if a.sheet and mids:
    try:
        from PIL import Image, ImageDraw
        ims = [mids[n] for n, _, _ in shots if n in mids]; cols = 4 if OW < OH else 3
        tw = 270 if OW < OH else 480; th = int(tw * OH / OW); rows = (len(ims) + cols - 1) // cols
        sheet = Image.new('RGB', (tw * cols, th * rows), (20, 14, 30)); d = ImageDraw.Draw(sheet)
        for i, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th)); d.text(((i % cols) * tw + 6, (i // cols) * th + 4), shots[i][0], fill=(255, 255, 255))
        os.makedirs(os.path.dirname(os.path.abspath(a.sheet)), exist_ok=True); sheet.save(a.sheet, quality=85)
    except Exception as e:
        warnings.append(f'could not write contact sheet: {e}')
done()
