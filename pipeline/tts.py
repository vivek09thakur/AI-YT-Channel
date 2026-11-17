#!/usr/bin/env python3
import argparse, asyncio, html, json, os, re, subprocess, sys
from pathlib import Path

try:
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass

SR = 48000
LEAD_IN, GAP, PARA_GAP, ELLIPSIS_GAP, TAIL = 0.8, 0.55, 1.1, 0.35, 3.0
MAX_WORDS = 22


def split_script(text):
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


FALLBACK_VOICES = {
    'en': ['en-US-AndrewNeural', 'en-US-GuyNeural', 'en-GB-RyanNeural', 'en-US-ChristopherNeural'],
    'hi': ['hi-IN-MadhurNeural', 'hi-IN-SwaraNeural'],
}


def voice_chain(voice):
    chain = [voice] + [v for v in FALLBACK_VOICES.get(voice.split('-')[0], []) if v != voice]
    return chain


def synth_line(engine, text, voice, rate, path, line_no):
    import random, time
    voices = voice_chain(voice) if engine == 'edge' else [voice]
    attempts = 0
    for v in voices:
        for k in range(4):
            attempts += 1
            try:
                if engine == 'azure':
                    azure_line(text, v, rate, path)
                else:
                    asyncio.run(edge_line(text, v, rate, path))
                if path.exists() and path.stat().st_size > 0:
                    if v != voice:
                        print(f'  line {line_no}: used fallback voice {v}', file=sys.stderr)
                    return v
                raise RuntimeError('empty audio file')
            except Exception as e:
                wait = min(30, 2 ** k + random.uniform(0, 1.5))
                print(f'  retry line {line_no} ({v}, attempt {attempts}): {e}; waiting {wait:.1f}s', file=sys.stderr)
                if path.exists():
                    path.unlink()
                time.sleep(wait)
    return None


async def edge_whole(text, voice, rate, path):
    """One request for the whole script; returns word boundaries [(start_s, end_s, word)]."""
    import edge_tts
    words, audio = [], bytearray()
    async for chunk in edge_tts.Communicate(text, voice, rate=rate, boundary='WordBoundary').stream():
        if chunk['type'] == 'audio':
            audio += chunk['data']
        elif chunk['type'] == 'WordBoundary':
            words.append((chunk['offset'] / 1e7, (chunk['offset'] + chunk['duration']) / 1e7, chunk['text']))
    if not audio or not words:
        raise RuntimeError('no audio or no word boundaries received')
    path.write_bytes(audio)
    return words


def map_words_to_lines(words, lines):
    """Walk the word boundaries along the joined script and return per-line (start_s, end_s)."""
    joined, spans, pos = '', [], 0
    for L in lines:
        if joined:
            joined += ' '; pos += 1
        spans.append((pos, pos + len(L['text']))); joined += L['text']; pos += len(L['text'])
    low, cursor, bounds = joined.lower(), 0, [None] * len(lines)
    li = 0
    for s, e, w in words:
        w = w.strip().lower()
        if not w:
            continue
        idx = low.find(w, cursor)
        if idx < 0 or idx - cursor > 120:
            continue
        cursor = idx + len(w)
        while li < len(spans) - 1 and idx >= spans[li + 1][0]:
            li += 1
        b = bounds[li]
        bounds[li] = (s if b is None else b[0], e)
    missing = [i for i, b in enumerate(bounds) if b is None]
    if missing:
        raise RuntimeError(f'no word timestamps for lines {missing[:5]}')
    return bounds


def synth_whole(lines, voice, rate, out):
    """Whole-script synthesis with retries + fallback voices; returns (voice_used, [pcm per line]) or None."""
    import random, time
    text = ' '.join(L['text'] for L in lines)
    path = out / 'voice_raw.mp3'
    attempts = 0
    for v in voice_chain(voice):
        for k, base in enumerate((3, 8, 20, 40)):
            attempts += 1
            try:
                words = asyncio.run(edge_whole(text, v, rate, path))
                bounds = map_words_to_lines(words, lines)
                pcm = to_pcm(path)
                total = len(pcm) / 2 / SR
                cuts = [0.0] + [(bounds[i][1] + bounds[i + 1][0]) / 2 for i in range(len(bounds) - 1)] + [total]
                parts = []
                for i in range(len(lines)):
                    a, b = int(cuts[i] * SR) * 2, int(cuts[i + 1] * SR) * 2
                    seg = trim_silence(pcm[a:b])
                    if len(seg) < SR * 2 // 5:
                        raise RuntimeError(f'line {i} segment too short ({len(seg) / 2 / SR:.2f}s)')
                    parts.append(seg)
                if v != voice:
                    print(f'  whole script: used fallback voice {v}', file=sys.stderr)
                return v, parts
            except Exception as e:
                wait = base + random.uniform(0, 2)
                print(f'  retry whole script ({v}, attempt {attempts}): {e}; waiting {wait:.1f}s', file=sys.stderr)
                if path.exists():
                    path.unlink()
                time.sleep(wait)
    return None


def azure_line(text, voice, rate, path):
    import requests
    key, region = os.environ['AZURE_SPEECH_KEY'], os.environ.get('AZURE_SPEECH_REGION', 'eastus')
    lang = '-'.join(voice.split('-')[:2])
    ssml = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{lang}"><voice name="{voice}"><prosody rate="{rate}">{html.escape(text, quote=False)}</prosody></voice></speak>'
    r = requests.post(f'https://{region}.tts.speech.microsoft.com/cognitiveservices/v1', data=ssml.encode('utf-8'), timeout=60,
                      headers={'Ocp-Apim-Subscription-Key': key, 'Content-Type': 'application/ssml+xml', 'X-Microsoft-OutputFormat': 'riff-48khz-16bit-mono-pcm', 'User-Agent': 'ai-yt-channel'})
    r.raise_for_status()
    path.write_bytes(r.content)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--script', required=True)
    ap.add_argument('--voice', default='en-US-AndrewNeural')
    ap.add_argument('--rate', default='-6%', help='speaking rate, e.g. -6%% for a cinematic pace')
    ap.add_argument('--out', default='work')
    ap.add_argument('--mode', default='auto', choices=['auto', 'whole', 'lines'],
                    help='edge engine only: whole = one request for the full script (default, avoids throttling), lines = one request per line')
    a = ap.parse_args()
    out = Path(a.out); (out / 'lines').mkdir(parents=True, exist_ok=True)
    lines = split_script(Path(a.script).read_text(encoding='utf-8-sig'))
    if not lines:
        sys.exit('script is empty')
    engine = 'azure' if os.environ.get('AZURE_SPEECH_KEY') else 'edge'
    print(f'{len(lines)} lines, voice {a.voice}, engine {engine}')

    voice_used, whole = a.voice, None
    if engine == 'edge' and a.mode in ('auto', 'whole'):
        whole = synth_whole(lines, a.voice, a.rate, out)
        if whole:
            voice_used, whole = whole
            print(f'  whole-script synthesis ok ({voice_used})')
        elif a.mode == 'whole':
            sys.exit('TTS failed (whole-script mode)')
        else:
            print('  whole-script synthesis failed; falling back to per-line requests', file=sys.stderr)

    pcm_parts, t, meta = [], 0.0, []
    silence = lambda sec: b'\x00\x00' * int(sec * SR)
    pcm_parts.append(silence(LEAD_IN)); t += LEAD_IN
    for i, L in enumerate(lines):
        if whole:
            pcm = whole[i]
        else:
            f = out / 'lines' / f'{i:03d}.{"wav" if engine == "azure" else "mp3"}'
            if not synth_line(engine, L['text'], a.voice, a.rate, f, i):
                sys.exit(f'TTS failed for line {i}: {L["text"]!r}')
            if engine == 'edge' and i + 1 < len(lines):
                import time; time.sleep(0.6)
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
    (out / 'narration.json').write_text(json.dumps({'voice': voice_used, 'engine': engine, 'duration': round(t, 2), 'lines': meta}, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'voice {t:.1f}s -> {out / "voice.mp3"}')


if __name__ == '__main__':
    main()
