#!/usr/bin/env python3
"""LLM writes src/data.ts + src/scenes.tsx for the daily fact reel kit; mechanical checks, tsc and headless stills gate it.

usage:
  generate_fact_reel.py --topic T --narration work/narration.json --project work/reel --kit .github/skills/daily-fact-reel \
                   --slug my-fact [--page-name NAME] [--notes ...] [--provider auto|gemini|...] [--model M] [--attempts 3] [--chrome PATH]

--project is a copy of <kit>/template with node_modules installed, public/voice.mp3 + public/fonts + public/sfx prepared
and src/rms.json generated. On success the story files are written to the project and copied to <kit>/facts/<slug>/.
"""
import argparse, json, os, re, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from generate_story import DEFAULT_MODEL, call_with_fallback, parse_files, read, run  # noqa: E402

ALLOWED_IMPORTS = {'react', 'remotion', './theme', './chrome', './figures', './kit', './data'}
SFX_NAMES = {'tick', 'pop', 'stamp', 'printer', 'whoosh', 'pad'}
PUNCT = '।,.!?“”"\'‘’…()[]{}:;—-'
CAP_LINE_MAX = 38  # contract says 34; a little slack
BENGALI = re.compile(r'[\u0980-\u09FF]')
NUM = r'(-?\d+(?:\.\d+)?)'
CAP_RE = re.compile(r'\{\s*s:\s*' + NUM + r'\s*,\s*e:\s*' + NUM + r'\s*,\s*t:\s*(?P<q>[\'"`])(?P<t>(?:\\.|(?!(?P=q)).)*)(?P=q)', re.S)
SCENE_RE = re.compile(r'\{\s*s:\s*' + NUM + r'\s*,\s*e:\s*' + NUM + r'\s*,\s*C:\s*(\w+)\s*,?\s*\}')
TAG_RE = re.compile(r'\{\s*s:\s*' + NUM + r'\s*,\s*e:\s*' + NUM + r'\s*,\s*tag:')
SFX_RE = re.compile(r'\[\s*[\'"](\w+)[\'"]\s*,\s*' + NUM + r'\s*,\s*' + NUM + r'\s*\]')
NPX = 'npx.cmd' if os.name == 'nt' else 'npx'
NODE = 'node'


def words(s):
    s = re.sub(r'\{([^}]*)\}', r'\1', s).replace('\\n', ' ')
    return [w.strip(PUNCT).lower() for w in s.split() if w.strip(PUNCT)]


def english_only(src, narr, fname):
    """The narration is English (no Bengali letters) -> no Bengali text may appear in the generated file."""
    if any(BENGALI.search(L['text']) for L in narr['lines']):
        return []
    hits = [l.strip()[:60] for l in src.splitlines() if BENGALI.search(l)]
    return [f'{fname}: Bengali text found but the narration is English; write every tag/label/caption in English: ' + ' | '.join(hits[:4])] if hits else []


def block(src, name):
    """Text of `export const NAME ... ;` up to the next top-level export."""
    m = re.search(r'export const ' + name + r'\b', src)
    if not m:
        return ''
    rest = src[m.end():]
    n = re.search(r'\nexport ', rest)
    return rest[:n.start()] if n else rest


def check_data(src, narr):
    errs = []
    total = narr['duration']
    for need in ("import rms from './rms.json'", 'export const RMS', 'export const TOTAL', 'export const CAPS',
                 'export const SPEAK', 'export const SCENE_TAGS', 'export const SFX'):
        if need not in src:
            errs.append(f'data.ts: missing `{need}`')
    m = re.search(r'export const TOTAL\s*=\s*' + NUM, src)
    if m and abs(float(m.group(1)) - total) > 0.051:
        errs.append(f'data.ts: TOTAL must be {total} (got {m.group(1)})')
    caps = [(float(a), float(b), t) for a, b, _, t in CAP_RE.findall(block(src, 'CAPS'))]
    lines = narr['lines']
    if not caps:
        errs.append('data.ts: CAPS is empty or not parseable (use `{ s: 1.2, e: 3.4, t: \'...\' }` literals)')
    elif not (0.8 * len(lines) <= len(caps) <= 2 * len(lines) + 2):
        errs.append(f'data.ts: {len(caps)} captions for {len(lines)} narration lines; write one caption per line (split a long line in two at most)')
    prev_e = -1
    for i, (s, e, t) in enumerate(caps):
        if s < 0 or e > total + 0.01 or e <= s:
            errs.append(f'data.ts: caption {i} has s={s} e={e}; need 0 <= s < e <= TOTAL={total}')
        if s < prev_e - 0.05:
            errs.append(f'data.ts: caption {i} starts at {s} before the previous one ends ({prev_e}); captions must not overlap')
        prev_e = e
        rows = t.split('\\n')
        if len(rows) > 2:
            errs.append(f'data.ts: caption {i} has {len(rows)} lines; max 2 (`\\n` once)')
        for r in rows:
            plain = re.sub(r'[{}]', '', r)
            if len(plain) > CAP_LINE_MAX:
                errs.append(f'data.ts: caption {i} line "{plain[:34]}…" is {len(plain)} chars; max 34 per line, break with \\n or split the caption')
        if t.count('{') != t.count('}') or t.count('{') > 3:
            errs.append(f'data.ts: caption {i}: use 1-2 balanced {{key}} marks')
        if '{' not in t and len(words(t)) > 4:
            errs.append(f'data.ts: caption {i} has no {{key word}}; mark one')
    if caps:
        narr_words = [w for L in lines for w in words(L['text'])]
        cap_words = [w for _, _, t in caps for w in words(t)]
        nset, cset = set(narr_words), set(cap_words)
        miss = [w for w in nset if w not in cset]
        extra = [w for w in cset if w not in nset]
        if len(miss) > max(1, 0.1 * len(nset)):
            errs.append('data.ts: captions drop narration words: ' + ' '.join(miss[:12]) + ' (captions must contain the exact narration text)')
        if len(extra) > max(1, 0.1 * len(cset)):
            errs.append('data.ts: captions contain words that are not in the narration: ' + ' '.join(extra[:12]))
        # every narration line should be covered by a caption that starts within its time span
        for L in lines:
            if not any(L['t0'] - 0.35 <= s <= L['t1'] for s, _, _ in caps):
                errs.append(f"data.ts: no caption starts inside line {L['i']} ({L['t0']}-{L['t1']}s: {L['text'][:40]}…)")
    for s, e in ((float(a), float(b)) for a, b in TAG_RE.findall(block(src, 'SCENE_TAGS'))):
        if e > total + 0.01 or e <= s:
            errs.append(f'data.ts: SCENE_TAG {s}-{e} outside 0..{total}')
    for name, s, v in SFX_RE.findall(block(src, 'SFX')):
        if name not in SFX_NAMES:
            errs.append(f'data.ts: SFX "{name}" does not exist (tick, pop, stamp, printer, whoosh)')
        if float(s) > total or float(v) > 1:
            errs.append(f'data.ts: SFX {name} at {s}s vol {v}: second must be <= TOTAL and volume <= 1')
    return errs


def check_scenes(src, narr):
    errs = []
    total = narr['duration']
    for mod in re.findall(r'^\s*import\s[^;]*?from\s+[\'"]([^\'"]+)[\'"]', src, re.M):
        if mod not in ALLOWED_IMPORTS:
            errs.append(f'scenes.tsx: import "{mod}" is not allowed (only react, remotion, ./theme, ./chrome, ./figures, ./kit, ./data)')
    if re.search(r'\bstaticFile\b|\bImg\b|<img', src):
        errs.append('scenes.tsx: no images/staticFile; draw everything with SVG')
    scenes = [(float(a), float(b), c) for a, b, c in SCENE_RE.findall(block(src, 'SCENES'))]
    if len(scenes) < 3:
        errs.append('scenes.tsx: SCENES must list at least 3 `{ s, e, C }` entries (plain number literals)')
        return errs
    if abs(scenes[0][0]) > 0.011:
        errs.append(f'scenes.tsx: first scene must start at 0 (got {scenes[0][0]})')
    if abs(scenes[-1][1] - total) > 0.011:
        errs.append(f'scenes.tsx: last scene must end at TOTAL={total} (got {scenes[-1][1]})')
    bounds = sorted({round(x, 2) for L in narr['lines'] for x in (L['t0'], L['t1'])})
    for i, (s, e, c) in enumerate(scenes):
        if e - s < 1.0:
            errs.append(f'scenes.tsx: scene {i} ({c}) lasts {e - s:.2f}s; minimum 1.2 s')
        if e - s > 12 and i != len(scenes) - 1:
            errs.append(f'scenes.tsx: scene {i} ({c}) lasts {e - s:.1f}s; split it (max 10 s)')
        if i and abs(scenes[i - 1][1] - s) > 0.011:
            errs.append(f'scenes.tsx: gap/overlap between scene {i - 1} (ends {scenes[i - 1][1]}) and scene {i} (starts {s}); e of one must equal s of the next')
        if 0 < i and min(abs(s - b) for b in bounds) > 0.75:
            errs.append(f'scenes.tsx: cut at {s}s is inside a narration line; cut at a line boundary (one of {", ".join(str(b) for b in bounds if abs(b - s) < 3) or "the line start/end times"})')
        comp = re.search(r'(?:export\s+)?const\s+' + c + r'\b[^=]*=\s*(.*?)(?=\n(?:export\s+)?const\s+\w+\s*[:=]|\nexport const SCENES|\Z)', src, re.S)
        if not comp:
            errs.append(f'scenes.tsx: scene component {c} is not defined')
            continue
        body = comp.group(1)
        if '<Stage' not in body and '<Relatives' not in body and not re.search(r'<[A-Z]\w*\s+\{\.\.\.p\}', body):
            errs.append(f'scenes.tsx: {c} does not render <Stage dur={{dur}}>; every scene must wrap its SVG in Stage')
        if re.search(r'<(div|span|p|h\d|img)\b', body):
            errs.append(f'scenes.tsx: {c} uses HTML elements inside Stage; only SVG elements render there')
    if len(scenes) < max(3, int(total / 8)):
        errs.append(f'scenes.tsx: only {len(scenes)} scenes for {total}s; aim for one cut every 3-6 s')
    return errs


def tsc(project):
    rc, out = run([NPX, 'tsc', '--noEmit', '-p', 'tsconfig.json'], project, timeout=300)
    if rc:
        return ['tsc --noEmit failed:\n' + '\n'.join(l for l in out.splitlines() if 'error' in l.lower())[:3000]]
    return []


def stills(project, narr, scenes, chrome, max_stills=14):
    """Render the middle frame of each scene; flag blank frames; build a contact sheet in project/debug."""
    from PIL import Image, ImageStat
    fps = 30
    picks = scenes if len(scenes) <= max_stills else [scenes[int(i * len(scenes) / max_stills)] for i in range(max_stills)]
    frames = sorted({min(int(round(narr['duration'] * fps)) - 1, int(round(((s + e) / 2) * fps))) for s, e, _ in picks})
    outdir = project / 'out' / 'stills'
    shutil.rmtree(outdir, ignore_errors=True)
    env = {'BROWSER': chrome} if chrome else {}
    rc, out = run([NODE, 'tools/stills.mjs', str(outdir), *map(str, frames)], project, env, timeout=1200)
    if rc:
        return [f'rendering stills failed (exit {rc}); the composition throws at runtime:\n' + out[-3000:]]
    errs, tiles = [], []
    for f in frames:
        p = outdir / f'f_{f:05d}.png'
        if not p.exists():
            errs.append(f'still for frame {f} was not produced'); continue
        im = Image.open(p).convert('L')
        body = im.crop((0, 230, im.width, 1440))  # scene zone only (no chrome, no captions)
        sd = ImageStat.Stat(body).stddev[0]
        who = next((c for s, e, c in scenes if s <= f / fps < e), '?')
        if sd < 6:
            errs.append(f'scene {who} at t={f / fps:.1f}s renders as a flat colour (stddev {sd:.1f}); it is missing <Stage> or its content is off-screen')
        tiles.append(Image.open(p).convert('RGB').resize((270, 480)))
    if tiles:
        sheet = Image.new('RGB', (270 * min(7, len(tiles)), 480 * ((len(tiles) + 6) // 7)), 'white')
        for i, t in enumerate(tiles):
            sheet.paste(t, (270 * (i % 7), 480 * (i // 7)))
        (project / 'debug').mkdir(exist_ok=True)
        sheet.save(project / 'debug' / 'sheet.png')
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--narration', required=True)
    ap.add_argument('--project', required=True)
    ap.add_argument('--kit', required=True)
    ap.add_argument('--slug', required=True)
    ap.add_argument('--page-name', default='')
    ap.add_argument('--notes', default='')
    ap.add_argument('--provider', default='gemini')
    ap.add_argument('--model', default='')
    ap.add_argument('--attempts', type=int, default=3)
    ap.add_argument('--chrome', default=os.environ.get('BROWSER', ''))
    ap.add_argument('--skip-stills', action='store_true')
    a = ap.parse_args()
    provider = a.provider if a.provider != 'auto' else 'gemini'
    model = a.model or DEFAULT_MODEL[provider]
    project, kit = Path(a.project).resolve(), Path(a.kit).resolve()
    narr = json.loads(read(a.narration))
    tsrc = kit / 'template' / 'src'

    system = read(HERE.parent / 'prompt' / 'CONTRACT_FACT_REEL.md')
    for f, label in (('theme.ts', 'theme.ts (colours, T, bn, clamp, SPRING)'), ('figures.tsx', 'figures.tsx (Person, Mini, Bubble: props and look)'),
                     ('kit.tsx', 'kit.tsx (presets, useT, sp, breathe, blinkAt, backgrounds, Doc, Eye, Megaphone, StepCard, Relatives)'),
                     ('chrome.tsx', 'chrome.tsx (Stage + Overlay: read-only, shows where tag/captions are drawn)')):
        system += f'\n\n## {label}\n```tsx\n' + read(tsrc / f) + '```\n'
    system += '\n\n## EXAMPLE data.ts (from an earlier 59 s Bengali video; copy the SHAPE only, write the new content in English)\n```ts\n' + read(tsrc / 'data.ts') + '```\n'
    system += '\n## EXAMPLE scenes.tsx (same video; copy the structure and quality, adapt the scenes to the new fact, all text in English)\n```tsx\n' + read(tsrc / 'scenes.tsx') + '```\n'

    narr_txt = '\n'.join(f"{L['i']:3d}  {L['t0']:7.2f} - {L['t1']:7.2f}  {L['text']}" for L in narr['lines'])
    user = (f"TOPIC: {a.topic}\nDURATION (TOTAL) = {narr['duration']} s. The voice ends at {narr.get('audio_duration', narr['lines'][-1]['t1'])} s.\n"
            + (f"PAGE NAME: {a.page_name}\n" if a.page_name else '')
            + f"\nNARRATION (index, start s, end s, text):\n{narr_txt}\n\n"
            + (f"NOTES FROM THE CHANNEL OWNER:\n{a.notes}\n\n" if a.notes.strip() else '')
            + 'Write meta.json, data.ts and scenes.tsx for this narration.')
    messages = [{'role': 'user', 'content': user}]
    total_in = total_out = 0
    for attempt in range(1, a.attempts + 1):
        print(f'--- attempt {attempt}/{a.attempts} ({provider} {model})')
        text, usage, provider, model = call_with_fallback(provider, model, system, messages, 16000)
        total_in += usage.get('prompt_tokens') or 0; total_out += usage.get('completion_tokens') or 0
        print(f'    tokens in {usage.get("prompt_tokens")} out {usage.get("completion_tokens")}')
        files = parse_files(text)
        errs = [f'missing block for {m}' for m in ('meta.json', 'data.ts', 'scenes.tsx') if m not in files]
        meta = {}
        if not errs:
            try:
                meta = json.loads(files['meta.json'])
            except json.JSONDecodeError as e:
                errs.append(f'meta.json is not valid JSON: {e}')
        if not errs:
            errs = (check_data(files['data.ts'], narr) + check_scenes(files['scenes.tsx'], narr)
                + english_only(files['data.ts'], narr, 'data.ts') + english_only(files['scenes.tsx'], narr, 'scenes.tsx'))
        if not errs:
            (project / 'src' / 'data.ts').write_text(files['data.ts'], encoding='utf-8')
            (project / 'src' / 'scenes.tsx').write_text(files['scenes.tsx'], encoding='utf-8')
            (project / 'src' / 'brand.ts').write_text(f'export const PAGE_NAME: string = {json.dumps(a.page_name, ensure_ascii=False)};\n', encoding='utf-8')
            errs = tsc(project)
            if not errs and not a.skip_stills:
                scenes = [(float(s), float(e), c) for s, e, c in SCENE_RE.findall(block(files['scenes.tsx'], 'SCENES'))]
                errs = stills(project, narr, scenes, a.chrome)
        if not errs:
            out = kit / 'facts' / a.slug
            out.mkdir(parents=True, exist_ok=True)
            for f in ('data.ts', 'scenes.tsx', 'brand.ts'):
                shutil.copy2(project / 'src' / f, out / f)
            shutil.copy2(a.narration, out / 'narration.json')
            meta = {**meta, 'topic': a.topic, 'page_name': a.page_name, 'voice': narr.get('voice'), 'duration': narr['duration'],
                    'provider': provider, 'model': model, 'attempts': attempt, 'input_tokens': total_in, 'output_tokens': total_out}
            (out / 'meta.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
            (project / 'meta.json').write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding='utf-8')
            print(f'OK: facts/{a.slug} passes checks, tsc and stills. tokens total in {total_in} out {total_out}')
            return
        print('    problems:\n' + '\n'.join(f'      {e[:400]}' for e in errs))
        messages += [{'role': 'assistant', 'content': text},
                     {'role': 'user', 'content': 'The checks reported these problems. Return all three files again, complete and corrected:\n\n' + '\n'.join(errs)}]
    sys.exit(f'gave up after {a.attempts} attempts')


if __name__ == '__main__':
    main()
