#!/usr/bin/env python3
"""One-time helper: mint a YouTube refresh token for the upload step (run on your own machine, not in CI).

1. Google Cloud console -> create a project -> enable "YouTube Data API v3"
2. APIs & Services -> OAuth consent screen -> External, add your channel's Google account as a test user
3. Credentials -> Create credentials -> OAuth client ID -> Desktop app -> copy client id + secret
4. download this file, then: pip install google-auth-oauthlib
   python yt_get_refresh_token.py --client-id ... --client-secret ...
   (a browser opens; sign in with the CHANNEL's Google account and allow all requested access)
5. store the printed refresh token + the client id/secret as repo secrets YT_USERn_REFRESH_TOKEN, YT_USERn_CLIENT_ID, YT_USERn_CLIENT_SECRET
   (run once per channel, logged in as that channel's account; the client id/secret are the same for every channel)

Scopes requested: upload + manage (thumbnails) + YouTube Analytics read-only, so the same refresh token also works
for analytics scripts. Enable "YouTube Analytics API" in the project too, or drop the yt-analytics scopes below.

Refresh tokens issued while the consent screen is in "Testing" expire after 7 days; publish the consent screen
(Publishing status -> In production) to make it long-lived. No Google review is needed for your own channel, but
videos uploaded through an unverified app are forced to PRIVATE by YouTube until the app passes verification.
"""
import argparse

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/yt-analytics.readonly',
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--client-id', required=True)
    ap.add_argument('--client-secret', required=True)
    a = ap.parse_args()
    cfg = {'installed': {'client_id': a.client_id, 'client_secret': a.client_secret,
                         'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                         'token_uri': 'https://oauth2.googleapis.com/token',
                         'redirect_uris': ['http://localhost']}}
    flow = InstalledAppFlow.from_client_config(cfg, SCOPES)
    creds = flow.run_local_server(port=0, access_type='offline', prompt='consent')
    print('\nrefresh token =', creds.refresh_token)
    print('add it as repository secret YT_USER1_REFRESH_TOKEN (USER2, USER3 ... for more channels; same client id/secret),')
    print('optionally YT_USER1_FOR = nlm | story to limit which workflow posts there (Settings -> Secrets and variables -> Actions)')


if __name__ == '__main__':
    main()
