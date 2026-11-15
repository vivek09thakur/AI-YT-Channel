#!/bin/zsh
# debug/shot.sh 5.6 10.9 ...  -> debug/f_<t>.png
cd "${0:A:h}/.." && python3 -c "
import build; build.build('debug/frame_shell.html', ['src/ref.js','src/story.js','debug/frame_runner.js'], ['lib/harness.js'], 'debug/frame.html')" >/dev/null
for t in "$@"; do
  timeout 25 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --user-data-dir="$(mktemp -d)" --no-first-run --disable-gpu --hide-scrollbars --window-size=1280,720 --virtual-time-budget=6000 --screenshot="$PWD/debug/f_$t.png" "file://$PWD/debug/frame.html#$t" >/dev/null 2>&1
done
