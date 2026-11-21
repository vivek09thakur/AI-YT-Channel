#!/usr/bin/env python3
"""Cut the NotebookLM end card off a downloaded Video Overview.

Detection (pure ffmpeg, no AI):
  * freezedetect  - the end card is a still frame; take a freeze that runs to the end of the file
  * silencedetect - narration stops before the card; take a silence that runs to the end of the file
Cut point = earliest qualifying start minus a small margin. A tail is accepted only if it ends within
TAIL_SLACK s of the file end and is shorter than --max-outro s, so pauses mid-video are ignored.
If nothing qualifies, fall back to --fallback seconds (0 = leave the file untouched).

Usage: trim_outro.py IN.mp4 OUT.mp4 [--fallback 3] [--max-outro 8] [--margin 0.1] [--report report.json]
"""
import argparse
import json
import re
import subprocess
import sys

TAIL_SLACK = 0.35


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path])
    return float(r.stdout.strip())


def detect(path, dur, max_outro):
    """Return dict name -> start time for tails that run to the end of the file."""
    vf = "freezedetect=n=0.003:d=0.8"
    af = "silencedetect=n=-40dB:d=0.8"
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", vf, "-af", af, "-f", "null", "-"])
    log = r.stderr
    found = {}

    def tail(starts, ends, name):
        # an open-ended segment (start without end) also counts as running to EOF
        pairs = list(zip(starts, ends + [dur] * (len(starts) - len(ends))))
        for s, e in pairs:
            if e >= dur - TAIL_SLACK and 0 < dur - s <= max_outro:
                found[name] = s
                break

    fs = [float(x) for x in re.findall(r"freeze_start:\s*([\d.]+)", log)]
    fe = [float(x) for x in re.findall(r"freeze_end:\s*([\d.]+)", log)]
    ss = [float(x) for x in re.findall(r"silence_start:\s*([\d.]+)", log)]
    se = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", log)]
    tail(fs, fe, "freeze")
    tail(ss, se, "silence")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--fallback", type=float, default=3.0, help="seconds to cut when nothing is detected (0 = keep as is)")
    ap.add_argument("--max-outro", type=float, default=8.0)
    ap.add_argument("--margin", type=float, default=0.1)
    ap.add_argument("--report")
    a = ap.parse_args()

    dur = duration(a.src)
    found = detect(a.src, dur, a.max_outro)
    if found:
        reason = ",".join(f"{k}@{v:.2f}" for k, v in sorted(found.items(), key=lambda kv: kv[1]))
        cut = min(found.values()) - a.margin
    elif a.fallback > 0:
        reason = f"fallback {a.fallback}s"
        cut = dur - a.fallback
    else:
        reason = "nothing detected, no fallback"
        cut = dur

    cut = max(1.0, min(cut, dur))
    trimmed = cut < dur - 0.05
    if trimmed:
        r = run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-to", f"{cut:.3f}",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.dst])
        if r.returncode != 0:
            print(r.stderr, file=sys.stderr)
            sys.exit(1)
        new_dur = duration(a.dst)
    else:
        if a.src != a.dst:
            import shutil
            shutil.copyfile(a.src, a.dst)
        new_dur = dur

    rep = {"input_duration": round(dur, 3), "cut_at": round(cut, 3), "output_duration": round(new_dur, 3),
           "removed": round(dur - new_dur, 3), "trimmed": trimmed, "reason": reason, "detected": found}
    print(json.dumps(rep, indent=2))
    if a.report:
        with open(a.report, "w") as f:
            json.dump(rep, f, indent=2)


if __name__ == "__main__":
    main()
