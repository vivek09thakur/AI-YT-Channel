#!/usr/bin/env python3
"""Inline lib/ + src/ into self-contained pages.
   python build.py storyboard [story]  -> <story>_storyboard.html
   python build.py player     [story]  -> <story>_play.html
   python build.py vertical   [story]  -> <story>_9x16.html (render-only, 1080x1920)

   story = a folder under stories/ holding ref.js, story.js, sound_score.js, vertical.js
   (and optionally storyboard_runner.js). Default: the bundled crow story in src/.
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
read = lambda p: (HERE / p).read_text(encoding='utf-8')


VOICE = HERE.parent.parent / '05_Audio' / 'voice_polished.mp3'

DEFAULT_PARTS = ['ref', 'story', 'sound_score', 'vertical']
GENERATED_PARTS = ['ref', 'lines', 'narration', 'story', 'sound_score', 'vertical']

STORIES = {
    'crow': {'dir': 'src', 'out': 'crow_shadow_play', 'title': 'Kauwa Shadow Play', 'parts': DEFAULT_PARTS},
}


def story_cfg(name):
    if name in STORIES:
        return STORIES[name]
    d = HERE / 'stories' / name
    if not d.is_dir():
        sys.exit(f'unknown story {name!r}: expected stories/{name}/')
    meta = {}
    mf = d / 'meta.txt'  # optional: title=...  parts=ref,lines,narration,story,sound_score,vertical  (one key=value per line)
    if mf.exists():
        meta = dict(l.split('=', 1) for l in mf.read_text(encoding='utf-8').splitlines() if '=' in l)
    parts = [p.strip() for p in meta['parts'].split(',')] if 'parts' in meta else DEFAULT_PARTS
    return {'dir': f'stories/{name}', 'out': name, 'title': meta.get('title', name), 'parts': parts}


def resolve(cfg, part):
    """<story dir>/<part>.js, else stories/_shared/<part>.js."""
    own = f"{cfg['dir']}/{part}.js"
    if (HERE / own).exists():
        return own
    shared = f'stories/_shared/{part}.js'
    if (HERE / shared).exists():
        return shared
    sys.exit(f'missing part {part}.js for story {cfg["out"]!r} (looked in {cfg["dir"]} and stories/_shared)')


def build(shell, parts, libs, out, voice=False, title=None):
    body = read(shell)
    if title:
        body = body.replace('Kauwa Shadow Play', title)
    scripts = ''
    if voice and VOICE.exists():  # bake the voiceover in so the page plays with it
        import base64
        scripts += f'<script>window.VOICE_DATA_URL = "data:audio/mpeg;base64,{base64.b64encode(VOICE.read_bytes()).decode()}";</script>\n'
    scripts += ''.join(f'<script>\n{read(l)}\n</script>\n' for l in libs)
    scripts += '<script>\n(function () {\n' + '\n'.join(read(p) for p in parts) + '\n})();\n</script>\n'
    (HERE / out).write_text(body + '\n' + scripts, encoding='utf-8')
    print('wrote', out)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'storyboard'
    cfg = story_cfg(sys.argv[2] if len(sys.argv) > 2 else 'crow')
    S, O, T = cfg['dir'], cfg['out'], cfg['title']
    parts = {p: resolve(cfg, p) for p in cfg['parts']}
    core = [parts[p] for p in cfg['parts'] if p not in ('sound_score', 'vertical')]
    sound = [parts[p] for p in cfg['parts'] if p == 'sound_score']
    reel = [parts[p] for p in cfg['parts'] if p == 'vertical']
    if what == 'storyboard':
        runner = f'{S}/storyboard_runner.js' if (HERE / S / 'storyboard_runner.js').exists() else 'src/storyboard_runner.js'
        build('storyboard_shell.html', core + [runner], ['lib/harness.js'], f'{O}_storyboard.html' if O != 'crow_shadow_play' else 'storyboard.html', title=T)
    elif what == 'vertical':
        build('vertical_shell.html', core + sound + reel + ['src/vertical_runner.js'], ['lib/harness.js', 'lib/sound.js'], f'{O}_9x16.html', title=T)
    else:
        build('player_shell.html', core + sound + ['src/player.js'], ['lib/harness.js', 'lib/sound.js'], f'{O}.html' if O != 'crow_shadow_play' else 'crow_shadow_play.html', voice=True, title=T)
