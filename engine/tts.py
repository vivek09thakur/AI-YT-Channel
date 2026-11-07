import base64
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from .common import SESSION, log
from .constants import HTTP_TIMEOUT, TTS_CHUNK, TTS_ENDPOINTS, TTS_WORKERS, VOICES


def _chunks(text: str, size: int) -> List[str]:
    chunks: List[str] = []
    current = ""
    for word in text.split():
        if len(current) + len(word) + 1 <= size:
            current = f"{current} {word}".strip()
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks


def _request(endpoint: str, text: str, voice: str) -> bytes:
    response = SESSION.post(endpoint, json={"text": text, "voice": voice}, timeout=HTTP_TIMEOUT)
    response.raise_for_status()
    data = response.json()
    encoded = data.get("data") or str(data.get("audio", "")).split(",")[-1]
    if not encoded or encoded == "error":
        raise RuntimeError(data.get("error") or "TTS returned no audio.")
    return base64.b64decode(encoded)


def synthesize(text: str, voice: str, dest: Path) -> Path:
    if voice not in VOICES:
        raise ValueError(f"Unknown voice: {voice}")
    if not text.strip():
        raise ValueError("Empty text for TTS.")
    parts = _chunks(text, TTS_CHUNK)
    last_error: Exception = RuntimeError("No TTS endpoint available.")
    for endpoint in TTS_ENDPOINTS:
        try:
            with ThreadPoolExecutor(max_workers=min(TTS_WORKERS, len(parts))) as pool:
                audio = b"".join(pool.map(lambda part: _request(endpoint, part, voice), parts))
            dest.write_bytes(audio)
            return dest
        except Exception as err:
            last_error = err
            log(f"[!] TTS endpoint failed ({endpoint}): {err}", "warning")
    raise RuntimeError(f"TTS failed: {last_error}")
