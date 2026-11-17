# usage: python3 tools/make_rms.py public/voice.mp3 src/rms.json   (needs numpy: pip install numpy --break-system-packages)
import subprocess, sys, json, numpy as np
src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','30000','-f','f32le','-'], capture_output=True, check=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
n = len(a)//1000
r = np.array([np.sqrt(np.mean(a[i*1000:(i+1)*1000]**2)) for i in range(n)])
r = r / max(r.max(), 1e-9)
json.dump([round(float(x),3) for x in r], open(out,'w'))
print(n, 'frames written to', out)
