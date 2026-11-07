from pathlib import Path
from typing import List
from uuid import uuid4

import srt_equalizer

from .common import ensure_dir, env, log, srt_time
from .constants import ASSEMBLY_LANG, SUBTITLES_DIR, SUBTITLE_MAX_CHARS


def _assemblyai(audio_path: Path, language: str) -> str:
    import assemblyai as aai

    aai.settings.api_key = env("ASSEMBLY_AI_API_KEY")
    config = aai.TranscriptionConfig(language_code=ASSEMBLY_LANG.get(language, language))
    transcript = aai.Transcriber(config=config).transcribe(str(audio_path))
    return transcript.export_subtitles_srt()


def _local(sentences: List[str], durations: List[float]) -> str:
    start = 0.0
    entries = []
    for index, (sentence, duration) in enumerate(zip(sentences, durations), start=1):
        end = start + duration
        entries.append(f"{index}\n{srt_time(start)} --> {srt_time(end)}\n{sentence}\n")
        start = end
    return "\n".join(entries)


def build(audio_path: Path, sentences: List[str], durations: List[float], voice: str) -> Path:
    if env("ASSEMBLY_AI_API_KEY"):
        log("[+] Subtitles via AssemblyAI", "info")
        srt = _assemblyai(audio_path, voice[:2])
    else:
        log("[+] Subtitles via local timings", "info")
        srt = _local(sentences, durations)
    path = ensure_dir(SUBTITLES_DIR) / f"{uuid4().hex}.srt"
    path.write_text(srt, encoding="utf-8")
    srt_equalizer.equalize_srt_file(str(path), str(path), SUBTITLE_MAX_CHARS)
    log("[+] Subtitles ready", "success")
    return path
