import os
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

import uvicorn
from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import (  # noqa: E402
    COLORS,
    DEFAULT_COLOR,
    DEFAULT_POSITION,
    DEFAULT_VOICE,
    POSITIONS,
    VOICES,
    Cancelled,
    Options,
    default_model,
    list_models,
    log,
    log_sink,
    run,
)

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8080"))
STATIC_DIR = Path(__file__).resolve().parent / "static"
MAX_JOBS = 50
MODELS_TTL = 600
FINAL_STATES = {"completed", "failed", "cancelled"}


@dataclass
class Job:
    id: str
    options: Options
    state: str = "queued"
    cancel_requested: bool = False
    result: Optional[Path] = None
    error: str = ""
    events: List[dict] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def push(self, message: str, level: str) -> None:
        self.events.append({"id": len(self.events) + 1, "message": message, "level": level, "timestamp": time.time()})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "state": self.state,
            "cancelRequested": self.cancel_requested,
            "resultPath": str(self.result) if self.result else None,
            "errorMessage": self.error or None,
            "createdAt": self.created_at,
        }


app = FastAPI(title="AI YT Channel", docs_url=None, redoc_url=None)
jobs: Dict[str, Job] = {}
jobs_lock = threading.Lock()
worker_lock = threading.Lock()
models_cache: dict = {"at": 0.0, "models": [], "warning": "", "loading": False}


def _get_job(job_id: str) -> Job:
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found.")
    return job


def _choices(mapping: dict) -> List[dict]:
    return [{"value": value, "label": label} for value, label in mapping.items()]


def _refresh_models() -> None:
    try:
        models_cache.update(models=list_models(), warning="")
    except Exception as err:
        models_cache.update(models=[], warning=f"Could not list Gemini models: {err}")
    finally:
        models_cache.update(at=time.time(), loading=False)


def _models() -> tuple[List[str], str]:
    if not models_cache["loading"] and time.time() - models_cache["at"] > MODELS_TTL:
        models_cache["loading"] = True
        threading.Thread(target=_refresh_models, daemon=True).start()
    return models_cache["models"] or [default_model()], models_cache["warning"]


def _execute(job: Job) -> None:
    with worker_lock:
        if job.cancel_requested:
            job.state = "cancelled"
            return
        job.state = "running"
        try:
            with log_sink(job.push):
                job.result = run(job.options, lambda: job.cancel_requested)
            job.state = "completed"
        except Cancelled:
            job.state = "cancelled"
        except Exception as err:
            job.error = str(err)
            job.state = "failed"
            job.push(f"[-] {err}", "error")
            log(f"[-] Job {job.id} failed: {err}", "error")


def _prune() -> None:
    finished = sorted((j for j in jobs.values() if j.state in FINAL_STATES), key=lambda j: j.created_at)
    for job in finished[: max(0, len(jobs) - MAX_JOBS)]:
        jobs.pop(job.id, None)


@app.get("/api/config")
def config():
    models, warning = _models()
    return {
        "models": models,
        "model": default_model(),
        "voices": _choices(VOICES),
        "voice": DEFAULT_VOICE,
        "positions": _choices(POSITIONS),
        "position": DEFAULT_POSITION,
        "colors": _choices(COLORS),
        "color": DEFAULT_COLOR,
        "warning": warning,
    }


@app.post("/api/generate")
def generate(payload: dict = Body(default_factory=dict)):
    try:
        options = Options.from_dict(payload)
    except (ValueError, TypeError) as err:
        raise HTTPException(400, str(err)) from err
    job = Job(id=uuid4().hex, options=options)
    with jobs_lock:
        _prune()
        jobs[job.id] = job
    threading.Thread(target=_execute, args=(job,), daemon=True).start()
    return {"jobId": job.id}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    return {"job": _get_job(job_id).to_dict()}


@app.get("/api/jobs/{job_id}/events")
def job_events(job_id: str, after: int = 0):
    return {"events": _get_job(job_id).events[after:]}


@app.post("/api/jobs/{job_id}/cancel")
def job_cancel(job_id: str):
    _get_job(job_id).cancel_requested = True
    return {"message": "Cancellation requested."}


@app.get("/api/jobs/{job_id}/download")
def job_download(job_id: str, inline: int = 0):
    job = _get_job(job_id)
    if not job.result or not job.result.exists():
        raise HTTPException(404, "Result not available.")
    return FileResponse(
        job.result,
        media_type="video/mp4",
        filename=job.result.name,
        content_disposition_type="inline" if inline else "attachment",
    )


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
_models()

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
