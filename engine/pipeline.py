import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Callable, Optional

from . import llm, stock, subtitles, tts, video, youtube
from .common import check_cancel, clean_dir, ensure_dir, log, split_sentences, temp_path
from .constants import DEFAULT_COLOR, DEFAULT_POSITION, DEFAULT_VOICE, OUTPUT_DIR, STOCK_COUNT, SUBTITLES_DIR, TEMP_DIR

CancelFn = Optional[Callable[[], bool]]


def _to_bool(value) -> bool:
    return value if isinstance(value, bool) else str(value).strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Options:
    subject: str
    paragraphs: int = 1
    voice: str = DEFAULT_VOICE
    model: str = ""
    custom_prompt: str = ""
    position: str = DEFAULT_POSITION
    color: str = DEFAULT_COLOR
    threads: int = field(default_factory=lambda: os.cpu_count() or 2)
    stock_count: int = STOCK_COUNT
    upload: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> "Options":
        casts = {f.name: (_to_bool if f.type is bool else f.type) for f in fields(cls)}
        kwargs = {key: casts[key](value) for key, value in data.items() if key in casts and value not in (None, "")}
        if not str(kwargs.get("subject", "")).strip():
            raise ValueError("subject is required")
        kwargs["paragraphs"] = max(1, kwargs.get("paragraphs", 1))
        return cls(**kwargs)

    def to_dict(self) -> dict:
        return asdict(self)


def run(options: Options, is_cancelled: CancelFn = None) -> Path:
    clean_dir(TEMP_DIR)
    clean_dir(SUBTITLES_DIR)
    ensure_dir(OUTPUT_DIR)
    log(f"[+] Subject: {options.subject}", "info")

    check_cancel(is_cancelled)
    script = llm.generate_script(options.subject, options.paragraphs, options.voice, options.custom_prompt, options.model)
    log(script, "info")

    check_cancel(is_cancelled)
    terms = llm.search_terms(options.subject, script, options.stock_count, options.model)
    clip_paths = stock.fetch_clips(terms, is_cancelled)

    check_cancel(is_cancelled)
    sentences = split_sentences(script)
    log(f"[+] Synthesizing {len(sentences)} sentence(s)...", "info")
    with ThreadPoolExecutor(max_workers=min(4, len(sentences))) as pool:
        audio_parts = list(pool.map(lambda text: tts.synthesize(text, options.voice, temp_path(".mp3")), sentences))
    audio_path, durations = video.concat_audio(audio_parts)
    total_duration = sum(durations)

    check_cancel(is_cancelled)
    srt_path = subtitles.build(audio_path, sentences, durations, options.voice)

    check_cancel(is_cancelled)
    combined = video.combine(clip_paths, total_duration, options.threads)

    check_cancel(is_cancelled)
    output = OUTPUT_DIR / f"{int(time.time())}.mp4"
    video.render(combined, audio_path, srt_path, options.position, options.color, options.threads, output)
    log(f"[+] Video saved: {output}", "success")

    if options.upload:
        title, description, keywords = llm.metadata(options.subject, script, options.model)
        log(f"[+] Title: {title}", "info")
        youtube.upload(output, title, description, keywords)

    return output
