#!/usr/bin/env python3
"""Narration -> Indian English voice track with per-line timestamps.

    python pipeline/tts.py --script script.txt --voice en-IN-PrabhatNeural --out work

Writes work/voice.wav, work/voice.mp3 and work/narration.json:
    {"voice": ..., "duration": 123.4, "lines": [{"i": 0, "text": ..., "t0": 0.8, "t1": 3.2, "para": true}, ...]}

Engines: Azure Speech when AZURE_SPEECH_KEY (+ AZURE_SPEECH_REGION) are set, else edge-tts (free, no key).
Both give the same Microsoft neural voices (en-IN-NeerjaNeural, en-IN-PrabhatNeural, ...).
"""
import argparse, asyncio, json, os, re, subprocess, sys
from pathlib import Path

try:  # use the OS certificate store (corporate proxies); no-op if truststore is not installed
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass

SR = 48000
LEAD_IN, GAP, PARA_GAP, ELLIPSIS_GAP, TAIL = 0.8, 0.55, 1.1, 0.35, 3.0
MAX_WORDS = 22  # longer sentences are split at commas so captions stay readable


def split_script(text):
    """Paragraphs -> sentences -> [{'text', 'para'}]; para marks the first line of a paragraph."""
    out = []
    for para in re.split(r'\n\s*\n|\s*(?<!\w)[/|](?!\w)\s*', text.strip()):
        para = ' '.join(para.split())
        if not para:
            continue
        parts = re.split(r'(?<=[.!?…])\s+|(?<=\.\.\.)\s+', para)
        first = True
        for s in parts:
            s = s.strip()
            if not s:
                continue
            chunks = [s]
            if len(s.split()) > MAX_WORDS and ',' in s:
                chunks, cur = [], []
                for piece in re.split(r'(?<=,)\s+', s):
                    cur.append(piece)
                    if len(' '.join(cur).split()) >= MAX_WORDS // 2:
                        chunks.append(' '.join(cur)); cur = []
                if cur:
                    chunks.append(' '.join(cur))
            for c in chunks:
                out.append({'text': c, 'para': first}); first = False
    return out


def ffprobe_dur(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def to_pcm(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True)
    return r.stdout


def trim_silence(pcm, thresh=400):
    """Strip leading/trailing near-silence so timestamps match the audible speech."""
    import array
    a = array.array('h'); a.frombytes(pcm)
    n = len(a); i, j = 0, n
    while i < n and abs(a[i]) < thresh: i += 1
    while j > i and abs(a[j - 1]) < thresh: j -= 1
    i = max(0, i - SR // 20); j = min(n, j + SR // 10)
    return a[i:j].tobytes()


async def edge_line(text, voice, rate, path):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(str(path))


def azure_line(text, voice, rate, path):
    import requests
    key, region = os.environ['AZURE_SPEECH_KEY'], os.environ.get('AZURE_SPEECH_REGION', 'centralindia')
    ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-IN"><voice name="{voice}"><prosody rate="{rate}">{text}</prosody></voice></speak>'
    r = requests.post(f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1', data=ssml.encode('utf-8'), timeout=60,
                      headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/ssml+xml', 'X-Microsoft-OutputFormat': 'riff-48khz-16bit-mono-pcm', 'User-Agent': 'ai-yt-channel'})
    r.raise_for_status()
    path.write_bytes(r.content)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--voice', default='en-IN-PrabhatNeural')
    ap.add_argument('--rate', default='-6%', help='speaking rate, e.g. -6%% for a cinematic pace')
    ap.add_argument('--out', default='work')
    a = ap.parse_args()
    out = Path(a.out); (out / 'lines').mkdir(parents=True, exist_ok=True)
    lines = split_script(Path(a.script).read_text(encoding='utf-8-sig'))
    if not lines:
        sys.exit('script is empty')
    engine = 'azure' if os.environ.get('AZURE_SPEECH_KEY') else 'edge'
    print(f'{len(lines)} lines, voice {a.voice}, engine {engine}')

    pcm_parts, t, meta = [], 0.0, []
    silence = lambda sec: b'\x00\x00' * int(sec * SR)
    pcm_parts.append(silence(LEAD_IN)); t += LEAD_IN
    for i, L in enumerate(lines):
        f = out / 'lines' / f'{i:03d}.{"wav" if engine == "azure" else "mp3"}'
        for attempt in range(3):
            try:
                if engine == 'azure':
                    azure_line(L['text'], a.voice, a.rate, f)
                else:
                    asyncio.run(edge_line(L['text'], a.voice, a.rate, f))
                if f.stat().st_size > 0:
                    break
            except Exception as e:  # network hiccups: retry
                print(f'  retry line {i}: {e}', file=sys.stderr)
        else:
            sys.exit(f'TTS failed for line {i}: {L["text"]!r}')
        pcm = trim_silence(to_pcm(f))
        dur = len(pcm) / 2 / SR
        if i > 0:
            gap = PARA_GAP if L['para'] else GAP
            if lines[i - 1]['text'].endswith(('...', '…')):
                gap += ELLIPSIS_GAP
            pcm_parts.append(silence(gap)); t += gap
        meta.append({'i': i, 'text': L['text'], 't0': round(t, 2), 't1': round(t + dur, 2), 'para': L['para']})
        pcm_parts.append(pcm); t += dur
        print(f'  {i:3d} {meta[-1]["t0"]:7.2f}-{meta[-1]["t1"]:7.2f}  {L["text"][:70]}')
    pcm_parts.append(silence(TAIL)); t += TAIL

    raw = out / 'voice.pcm'; raw.write_bytes(b''.join(pcm_parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', str(raw), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', str(out / 'voice.wav')], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(out / 'voice.wav'), '-c:a', 'libmp3lame', '-b:a', '160k', str(out / 'voice.mp3')], check=True)
    raw.unlink()
    (out / 'narration.json').write_text(json.dumps({'voice': a.voice, 'engine': engine, 'duration': round(t, 2), 'lines': meta}, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'voice {t:.1f}s -> {out / "voice.mp3"}')


if __name__ == '__main__':
    main()
