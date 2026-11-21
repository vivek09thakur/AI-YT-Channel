#!/usr/bin/env python3
"""Publish a video as an Instagram Reel through the Instagram Graph API (no third-party packages).

usage: upload_instagram.py --video-url https://public.host/reel.mp4 --meta final/meta.json --out ig.json

env: IG_USER_ID       Instagram professional (Business / Creator) account id
     IG_ACCESS_TOKEN  long-lived token with instagram_content_publish (Facebook Login) or
                      instagram_business_content_publish (Instagram Login)
     IG_GRAPH_HOST    optional: graph.facebook.com (default) or graph.instagram.com for Instagram-Login tokens

The API downloads the video itself, so --video-url MUST be publicly reachable. Flow: create REELS container -> poll
until FINISHED -> media_publish -> read permalink. Writes {"id", "permalink"} to --out.
"""
import argparse, json, os, sys, time
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

API_VERSION = 'v21.0'
POLL_SECONDS = 10
POLL_TIMEOUT = 15 * 60


def call(host, path, params, method='GET'):
    params = {k: v for k, v in params.items() if v is not None}
    url = f'https://{host}/{API_VERSION}/{path}'
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url + ('?' + data.decode() if method == 'GET' else ''),
                                 data=None if method == 'GET' else data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='replace')
        try:
            err = json.loads(body).get('error', {})
            msg = f"{err.get('message')} (code {err.get('code')}, subcode {err.get('error_subcode')}) {err.get('error_user_msg') or ''}"
        except json.JSONDecodeError:
            msg = body[:500]
        sys.exit(f'::error::Instagram API {e.code} on {path}: {msg}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--video-url', required=True)
    ap.add_argument('--meta', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    user = os.environ.get('IG_USER_ID', '').strip()
    token = os.environ.get('IG_ACCESS_TOKEN', '').strip()
    host = os.environ.get('IG_GRAPH_HOST', '').strip() or 'graph.facebook.com'
    if not user or not token:
        sys.exit('::error::missing env IG_USER_ID / IG_ACCESS_TOKEN')

    meta = json.loads(Path(a.meta).read_text(encoding='utf-8'))
    caption = (meta.get('caption_instagram') or meta.get('description') or meta.get('title') or '')[:2200]

    print('creating reel container')
    container = call(host, f'{user}/media', {
        'media_type': 'REELS', 'video_url': a.video_url, 'caption': caption, 'share_to_feed': 'true',
        'access_token': token}, method='POST')
    cid = container.get('id')
    if not cid:
        sys.exit(f'::error::no container id in response: {container}')

    deadline = time.time() + POLL_TIMEOUT
    while True:
        st = call(host, cid, {'fields': 'status_code,status', 'access_token': token})
        code = st.get('status_code', '')
        print(f'container {cid}: {code} {st.get("status", "")}'.strip())
        if code == 'FINISHED':
            break
        if code in ('ERROR', 'EXPIRED'):
            sys.exit(f'::error::Instagram could not process the video: {st}')
        if time.time() > deadline:
            sys.exit('::error::timed out waiting for Instagram to process the video')
        time.sleep(POLL_SECONDS)

    pub = call(host, f'{user}/media_publish', {'creation_id': cid, 'access_token': token}, method='POST')
    mid = pub.get('id')
    if not mid:
        sys.exit(f'::error::publish returned no media id: {pub}')
    info = call(host, mid, {'fields': 'permalink', 'access_token': token})
    link = info.get('permalink', '')
    print(f'published: {link or mid}')
    Path(a.out).write_text(json.dumps({'id': mid, 'permalink': link}), encoding='utf-8')


if __name__ == '__main__':
    main()
