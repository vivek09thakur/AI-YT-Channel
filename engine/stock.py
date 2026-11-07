from pathlib import Path
from typing import Callable, List, Optional

from .common import check_cancel, download, env, get_json, log, require_env, temp_path
from .constants import HEIGHT, PEXELS_URL, STOCK_MIN_DURATION, STOCK_PER_QUERY, WIDTH


def _best_file(files: List[dict]) -> Optional[str]:
    candidates = [f for f in files if f.get("link") and f.get("width") and f.get("height")]
    if not candidates:
        return None
    candidates.sort(key=lambda f: f["width"] * f["height"])
    for item in candidates:
        if min(item["width"], item["height"]) >= WIDTH or max(item["width"], item["height"]) >= HEIGHT:
            return item["link"]
    return candidates[-1]["link"]


def search(query: str, per_page: int = STOCK_PER_QUERY, min_duration: int = STOCK_MIN_DURATION) -> List[str]:
    require_env("PEXELS_API_KEY")
    data = get_json(
        PEXELS_URL,
        headers={"Authorization": env("PEXELS_API_KEY")},
        params={"query": query, "per_page": per_page, "orientation": "portrait"},
    )
    urls: List[str] = []
    for video in data.get("videos", []):
        if video.get("duration", 0) < min_duration:
            continue
        link = _best_file(video.get("video_files", []))
        if link:
            urls.append(link)
    log(f'   "{query}" -> {len(urls)} clip(s)', "info")
    return urls


def fetch_clips(terms: List[str], is_cancelled: Optional[Callable[[], bool]] = None) -> List[Path]:
    urls: List[str] = []
    for term in terms:
        check_cancel(is_cancelled)
        for url in search(term):
            if url not in urls:
                urls.append(url)
                break
    if not urls:
        raise RuntimeError("No stock videos found.")
    log(f"[+] Downloading {len(urls)} clip(s)...", "info")
    paths: List[Path] = []
    for url in urls:
        check_cancel(is_cancelled)
        try:
            paths.append(download(url, temp_path(".mp4")))
        except Exception as err:
            log(f"[-] Download failed: {err}", "error")
    if not paths:
        raise RuntimeError("Could not download any stock videos.")
    return paths
