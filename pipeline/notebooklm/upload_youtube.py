#!/usr/bin/env python3
"""Upload a video to YouTube (Data API v3) using a long-lived OAuth refresh token.

usage: upload_youtube.py --video final/reel.mp4 --meta final/meta.json [--privacy public|unlisted|private] --out yt.json

env: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN  (mint the refresh token once with yt_get_refresh_token.py)
deps: pip install google-api-python-client google-auth

Title / description / tags come from meta.json (title, caption_youtube, hashtags). Writes {"id", "url"} to --out.
Note: YouTube forces videos uploaded by an UNVERIFIED Google Cloud OAuth app to private; see README.
"""
import argparse, json, os, sys, time
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']
CATEGORY_EDUCATION = '27'


def creds_from_env():
    missing = [k for k in ('YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN') if not os.environ.get(k)]
    if missing:
        sys.exit(f'::error::missing env {", ".join(missing)}')
    return Credentials(None, refresh_token=os.environ['YT_REFRESH_TOKEN'], token_uri='https://oauth2.googleapis.com/token',
                       client_id=os.environ['YT_CLIENT_ID'], client_secret=os.environ['YT_CLIENT_SECRET'], scopes=SCOPES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--privacy', default='public', choices=['public', 'unlisted', 'private'])
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    meta = json.loads(Path(a.meta).read_text(encoding='utf-8'))
    title = (meta.get('title') or meta.get('topic') or 'Short')[:100]
    if '#shorts' not in title.lower() and len(title) <= 92:
        title += ' #Shorts'
    description = (meta.get('caption_youtube') or meta.get('description') or '')[:5000]
    tags = [t.lstrip('#') for t in meta.get('hashtags', [])]
    tags = [t for t in tags if t]
    while sum(len(t) + 2 for t in tags) > 480:
        tags.pop()

    body = {
        'snippet': {'title': title, 'description': description, 'tags': tags, 'categoryId': CATEGORY_EDUCATION},
        'status': {'privacyStatus': a.privacy, 'selfDeclaredMadeForKids': False},
    }
    yt = build('youtube', 'v3', credentials=creds_from_env(), cache_discovery=False)
    media = MediaFileUpload(a.video, mimetype='video/mp4', chunksize=8 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)

    resp, attempt = None, 0
    while resp is None:
        try:
            status, resp = req.next_chunk()
            if status:
                print(f'uploading: {int(status.progress() * 100)}%')
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and attempt < 5:
                attempt += 1
                wait = 2 ** attempt
                print(f'retryable HTTP {e.resp.status}, retrying in {wait}s')
                time.sleep(wait)
                continue
            sys.exit(f'::error::YouTube upload failed: {e}')

    vid = resp['id']
    url = f'https://youtube.com/shorts/{vid}'
    print(f'uploaded: {url} (privacy {resp.get("status", {}).get("privacyStatus", a.privacy)})')

    thumb = Path(a.video).with_name('thumb.jpg')
    if thumb.exists():
        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb), mimetype='image/jpeg')).execute()
            print('thumbnail set')
        except HttpError as e:
            print(f'::warning::thumbnail not set ({e.resp.status}) - custom thumbnails need a phone-verified channel')

    Path(a.out).write_text(json.dumps({'id': vid, 'url': url, 'privacy': a.privacy}), encoding='utf-8')


if __name__ == '__main__':
    main()
