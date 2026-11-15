#!/usr/bin/env python3
"""Inline lib/ + src/ into self-contained pages.
   python3 build.py storyboard   -> storyboard.html
   python3 build.py player       -> crow_shadow_play.html
   python3 build.py vertical     -> crow_shadow_play_9x16.html (render-only, 1080x1920)
"""
import sys
from pathlib import Path

HERE = Path(__file__).parent
read = lambda p: (HERE / p).read_text()


VOICE = HERE.parent.parent / '05_Audio' / 'voice_polished.mp3'


def build(shell, parts, libs, out, voice=False):
    body = read(shell)
    scripts = ''
    if voice and VOICE.exists():  # bake the voiceover in so the page plays with it
        import base64
        scripts += f'<script>window.VOICE_DATA_URL = "data:audio/mpeg;base64,{base64.b64encode(VOICE.read_bytes()).decode()}";</script>\n'
    scripts += ''.join(f'<script>\n{read(l)}\n</script>\n' for l in libs)
    scripts += '<script>\n(function () {\n' + '\n'.join(read(p) for p in parts) + '\n})();\n</script>\n'
    (HERE / out).write_text(body + '\n' + scripts)
    print('wrote', out)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'storyboard'
    if what == 'storyboard':
        build('storyboard_shell.html', ['src/ref.js', 'src/story.js', 'src/storyboard_runner.js'], ['lib/harness.js'], 'storyboard.html')
    elif what == 'vertical':
        build('vertical_shell.html', ['src/ref.js', 'src/story.js', 'src/sound_score.js', 'src/vertical.js', 'src/vertical_runner.js'], ['lib/harness.js', 'lib/sound.js'], 'crow_shadow_play_9x16.html')
    else:
        build('player_shell.html', ['src/ref.js', 'src/story.js', 'src/sound_score.js', 'src/player.js'], ['lib/harness.js', 'lib/sound.js'], 'crow_shadow_play.html', voice=True)
