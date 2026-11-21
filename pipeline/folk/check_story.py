#!/usr/bin/env python3
"""check_story.py --story stories/x/story.py --phrases work/phrases.json --kit .github/skills/folk-art-video [--sheet out.png] [--json out.json] [--step 15]

Validates an LLM-written folk2d story without trusting it:
  1. static: only whitelisted imports / no file, process, network or env access (AST), required module names present
  2. dynamic (subprocess per aspect, API keys scrubbed from the env, FOLK_SS=1): import, shot coverage, every shot draws a
     character or animal, sampled frames render without exceptions and are not flat, unknown outfit/pose/prop/animal/cue
     names, CUES / MUSIC sanity, contact sheet of shot midpoints.
Prints the problems and exits 1 if there are any (so the generator can feed them back to the model)."""
import argparse, ast, json, os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ALLOWED_IMPORTS = {'math', 'random', 'folk2d', 'folk2d.timeline', 'folk2d.world', 'folk2d.cast', 'folk2d.animals', 'folk2d.draw'}
FORBIDDEN_NAMES = {'open', 'exec', 'eval', 'compile', '__import__', 'input', 'breakpoint', 'globals', 'locals', 'vars', 'getattr', 'setattr', 'delattr', 'exit', 'quit'}
FORBIDDEN_ATTRS = {'__builtins__', '__subclasses__', '__globals__', '__code__', '__loader__', '__spec__', 'environ', 'system', 'popen'}
REQUIRED = ['T', 'SHOT_DEFS', 'SHOTS', 'FN', 'render_frame', 'CUES', 'MUSIC']
SECRET_MARKS = ('KEY', 'TOKEN', 'SECRET', 'PASSWORD', 'PASSWD', 'CREDENTIAL', 'API', 'GITHUB_', 'AZURE', 'AWS_', 'ACTIONS_')


def static_check(src):
    problems = []
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [f'story.py does not parse: {e.msg} (line {e.lineno}): {str(e.text or "").strip()[:120]}']
    defined = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name not in ALLOWED_IMPORTS: problems.append(f'import {a.name} is not allowed (only math, random, folk2d)')
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ''
            if mod not in ALLOWED_IMPORTS: problems.append(f'from {mod} import ... is not allowed (only math, random, folk2d)')
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in FORBIDDEN_NAMES:
            problems.append(f'use of {node.id}() is not allowed (line {node.lineno})')
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRS:
            problems.append(f'attribute .{node.attr} is not allowed (line {node.lineno})')
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): defined.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name): defined.add(n.id)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name): defined.add(node.target.id)
    for r in REQUIRED:
        if r not in defined: problems.append(f'story.py must define {r} at module level (see the example)')
    return sorted(set(problems), key=problems.index)


def scrubbed_env(extra):
    env = {k: v for k, v in os.environ.items() if not any(m in k.upper() for m in SECRET_MARKS)}
    env.update(extra)
    return env


def dynamic_check(story, phrases, kit, aspect, step, sheet):
    engine = str(Path(kit) / 'engine')
    env = scrubbed_env({'FOLK_ASPECT': aspect, 'FOLK_SS': '1', 'FOLK_PHRASES': str(phrases), 'PYTHONPATH': engine, 'PYTHONIOENCODING': 'utf-8', 'FOLK_STRICT': '1'})
    cmd = [sys.executable, str(HERE / '_probe.py'), '--story', str(story), '--step', str(step)] + (['--sheet', str(sheet)] if sheet else [])
    try:
        r = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=1500)
    except subprocess.TimeoutExpired:
        return {'problems': [f'[{aspect}] rendering the sample frames took more than 25 minutes; the story is far too slow (fewer stars/dots/particles, no loops over hundreds of shapes)'], 'warnings': [], 'frames': 0}
    out = (r.stdout or '').strip().splitlines()
    for line in reversed(out):
        if line.startswith('{'):
            try: return json.loads(line)
            except Exception: break
    tail = ((r.stdout or '') + (r.stderr or '')).strip().splitlines()[-25:]
    return {'problems': [f'[{aspect}] probe crashed (exit {r.returncode}):\n' + '\n'.join(tail)], 'warnings': [], 'frames': 0}


def check(story, phrases, kit, step=15, sheet=None, aspects=('shorts', 'landscape')):
    story = Path(story).resolve(); src = story.read_text(encoding='utf-8')
    problems = static_check(src)
    if problems: return {'problems': problems, 'warnings': [], 'frames': 0}
    warnings = []; frames = 0
    for aspect in aspects:
        res = dynamic_check(story, Path(phrases).resolve(), Path(kit).resolve(), aspect, step, sheet if aspect == 'shorts' else None)
        problems += [p for p in res.get('problems', []) if p not in problems]
        warnings += [w for w in res.get('warnings', []) if w not in warnings]
        frames += res.get('frames', 0)
        if res.get('problems') and aspect == 'shorts' and any('import' in p or 'crashed' in p for p in res['problems']): break   # no point rendering landscape
    return {'problems': problems, 'warnings': warnings, 'frames': frames}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--story', required=True); ap.add_argument('--phrases', required=True); ap.add_argument('--kit', required=True)
    ap.add_argument('--sheet', default=None); ap.add_argument('--json', default=None); ap.add_argument('--step', type=int, default=15)
    ap.add_argument('--aspects', default='shorts,landscape')
    a = ap.parse_args()
    t = time.time()
    res = check(a.story, a.phrases, a.kit, a.step, a.sheet, tuple(x for x in a.aspects.split(',') if x))
    res['seconds'] = round(time.time() - t, 1)
    if a.json: Path(a.json).write_text(json.dumps(res, indent=1), encoding='utf-8')
    for w in res['warnings']: print('  warning:', w)
    if res['problems']:
        print(f"{len(res['problems'])} problem(s) after checking {res['frames']} frames in {res['seconds']}s:")
        for p in res['problems']: print('  -', p)
        sys.exit(1)
    print(f"OK: story renders cleanly ({res['frames']} sampled frames, both aspects, {res['seconds']}s)")


if __name__ == '__main__':
    main()
