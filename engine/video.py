from pathlib import Path
from typing import List, Tuple

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    TextClip,
    VideoFileClip,
    concatenate_audioclips,
    concatenate_videoclips,
)
from moviepy.video.tools.subtitles import SubtitlesClip

from .common import log, resolve_font, temp_path
from .constants import (
    ASPECT,
    AUDIO_CODEC,
    FONT_SIZE,
    FPS,
    FRAME_EPSILON,
    HEIGHT,
    MAX_CLIP_DURATION,
    PRESET,
    STROKE_COLOR,
    STROKE_WIDTH,
    TOP_OFFSET,
    VIDEO_CODEC,
    WIDTH,
)


def concat_audio(paths: List[Path]) -> Tuple[Path, List[float]]:
    clips = [AudioFileClip(str(path)) for path in paths]
    durations = [clip.duration for clip in clips]
    dest = temp_path(".mp3")
    merged = concatenate_audioclips(clips)
    try:
        merged.write_audiofile(str(dest), logger=None)
    finally:
        merged.close()
        for clip in clips:
            clip.close()
    return dest, durations


def _fit(clip: VideoFileClip) -> VideoFileClip:
    if round(clip.w / clip.h, 4) < ASPECT:
        clip = clip.cropped(width=clip.w, height=round(clip.w / ASPECT), x_center=clip.w / 2, y_center=clip.h / 2)
    else:
        clip = clip.cropped(width=round(ASPECT * clip.h), height=clip.h, x_center=clip.w / 2, y_center=clip.h / 2)
    return clip.resized(new_size=(WIDTH, HEIGHT))


def combine(paths: List[Path], duration: float, threads: int) -> Path:
    if not paths:
        raise ValueError("No clips to combine.")
    per_clip = min(duration / len(paths), MAX_CLIP_DURATION)
    log(f"[+] Combining {len(paths)} clip(s), up to {per_clip:.1f}s each", "info")
    clips = []
    total = 0.0
    while total < duration - FRAME_EPSILON:
        progressed = False
        for path in paths:
            remaining = duration - total
            if remaining <= FRAME_EPSILON:
                break
            clip = VideoFileClip(str(path)).without_audio()
            target = min(per_clip, remaining, clip.duration - FRAME_EPSILON)
            if target <= 0:
                clip.close()
                continue
            if target < clip.duration:
                clip = clip.subclipped(0, target)
            clips.append(_fit(clip).with_fps(FPS))
            total += target
            progressed = True
        if not progressed:
            raise RuntimeError("Source clips too short to reach target duration.")
    dest = temp_path(".mp4")
    final = concatenate_videoclips(clips, method="compose").with_fps(FPS).with_duration(duration)
    try:
        final.write_videofile(str(dest), threads=threads, fps=FPS, codec=VIDEO_CODEC, preset=PRESET, audio=False, logger=None)
    finally:
        final.close()
        for clip in clips:
            clip.close()
    return dest


def render(video_path: Path, audio_path: Path, srt_path: Path, position: str, color: str, threads: int, dest: Path) -> Path:
    font = resolve_font()
    horizontal, vertical = (position.split(",") + ["bottom"])[:2]
    vertical_pos = TOP_OFFSET if vertical == "top" else vertical
    subtitles = SubtitlesClip(
        str(srt_path),
        make_textclip=lambda text: TextClip(
            font=font, text=text, font_size=FONT_SIZE, color=color, stroke_color=STROKE_COLOR, stroke_width=STROKE_WIDTH
        ),
        encoding="utf-8",
    )
    base = VideoFileClip(str(video_path))
    audio = AudioFileClip(str(audio_path))
    duration = min(base.duration, audio.duration)
    result = CompositeVideoClip(
        [base.subclipped(0, duration), subtitles.with_position((horizontal, vertical_pos)).with_duration(duration)]
    ).with_audio(audio.subclipped(0, duration)).with_duration(duration)
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        result.write_videofile(
            str(dest), threads=threads, fps=FPS, codec=VIDEO_CODEC, audio_codec=AUDIO_CODEC, preset=PRESET, logger=None
        )
    finally:
        result.close()
        subtitles.close()
        audio.close()
        base.close()
    return dest
