import json
import logging
import os
import re
import shutil
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterable, Iterator, List, Optional
from uuid import uuid4

import requests
from dotenv import load_dotenv

from .constants import ENV_FILE, FONT_CANDIDATES, HTTP_TIMEOUT, TEMP_DIR

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

load_dotenv(ENV_FILE)

LogFn = Callable[[str, str], None]
LEVELS = {"info": logging.INFO, "success": logging.INFO, "warning": logging.WARNING, "error": logging.ERROR}

_logger = logging.getLogger("engine")
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False

_sinks: List[LogFn] = []
_sinks_lock = threading.Lock()
SESSION = requests.Session()


class Cancelled(Exception):
    pass


def log(message: str, level: str = "info") -> None:
    _logger.log(LEVELS.get(level, logging.INFO), message)
    with _sinks_lock:
        sinks = list(_sinks)
    for sink in sinks:
        sink(message, level)


@contextmanager
def log_sink(fn: LogFn) -> Iterator[None]:
    with _sinks_lock:
        _sinks.append(fn)
    try:
        yield
    finally:
        with _sinks_lock:
            _sinks.remove(fn)


def env(name: str, default: str = "") -> str:
    return (os.getenv(name) or default).strip().strip('"')


def require_env(*names: str) -> None:
    missing = [name for name in names if not env(name)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_dir(path: Path) -> None:
    ensure_dir(path)
    for entry in path.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            entry.unlink(missing_ok=True)


def temp_path(suffix: str) -> Path:
    return ensure_dir(TEMP_DIR) / f"{uuid4().hex}{suffix}"


def check_cancel(is_cancelled: Optional[Callable[[], bool]]) -> None:
    if is_cancelled and is_cancelled():
        raise Cancelled("Generation cancelled.")


def get_json(url: str, **kwargs) -> dict:
    response = SESSION.get(url, timeout=kwargs.pop("timeout", HTTP_TIMEOUT), **kwargs)
    response.raise_for_status()
    return response.json()


def post_json(url: str, payload: dict, **kwargs) -> dict:
    response = SESSION.post(url, json=payload, timeout=kwargs.pop("timeout", HTTP_TIMEOUT), **kwargs)
    response.raise_for_status()
    return response.json()


def download(url: str, dest: Path) -> Path:
    with SESSION.get(url, stream=True, timeout=HTTP_TIMEOUT) as response:
        response.raise_for_status()
        with open(dest, "wb") as handle:
            for chunk in response.iter_content(chunk_size=1 << 20):
                handle.write(chunk)
    return dest


def parse_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        data = json.loads(match.group()) if match else {}
    return data if isinstance(data, dict) else {}


def clean_strings(values: Iterable) -> List[str]:
    return [str(value).strip() for value in values if str(value).strip()]


def split_sentences(text: str) -> List[str]:
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+|\n+", text) if part.strip()]


def resolve_font() -> str:
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return str(candidate)
    raise RuntimeError("No bold system font found. Install DejaVu Sans (apt install fonts-dejavu-core).")


def srt_time(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, rest = divmod(total_ms, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    secs, ms = divmod(rest, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
