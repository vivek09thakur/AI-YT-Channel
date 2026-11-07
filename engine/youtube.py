import random
import time
from pathlib import Path
from typing import List

from .common import log
from .constants import CLIENT_SECRET_FILE, TOKEN_FILE, YT_CATEGORY, YT_PRIVACY, YT_RETRIES, YT_RETRY_CODES, YT_SCOPES


def _service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), YT_SCOPES) if TOKEN_FILE.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                raise RuntimeError(f"Missing {CLIENT_SECRET_FILE.name} for YouTube OAuth.")
            creds = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), YT_SCOPES).run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())
    return build("youtube", "v3", credentials=creds, cache_discovery=False)


def upload(video_path: Path, title: str, description: str, keywords: List[str], privacy: str = YT_PRIVACY) -> str:
    from googleapiclient.errors import HttpError
    from googleapiclient.http import MediaFileUpload

    body = {
        "snippet": {"title": title[:100], "description": description[:5000], "tags": keywords, "categoryId": YT_CATEGORY},
        "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False},
    }
    request = _service().videos().insert(
        part="snippet,status", body=body, media_body=MediaFileUpload(str(video_path), chunksize=-1, resumable=True)
    )
    retries = 0
    while True:
        try:
            _, response = request.next_chunk()
            if response and "id" in response:
                log(f"[+] Uploaded to YouTube: {response['id']}", "success")
                return response["id"]
        except HttpError as err:
            if err.resp.status not in YT_RETRY_CODES:
                raise
            log(f"[!] Retriable upload error {err.resp.status}", "warning")
        except (OSError, ConnectionError) as err:
            log(f"[!] Retriable upload error: {err}", "warning")
        retries += 1
        if retries > YT_RETRIES:
            raise RuntimeError("YouTube upload failed after retries.")
        time.sleep(random.random() * (2**retries))
