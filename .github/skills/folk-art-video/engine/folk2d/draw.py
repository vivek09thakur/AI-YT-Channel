"""folk2d.draw - Pillow canvas, easing and primitives.

Design space is always 1080x1920 (9:16). The OUTPUT frame is chosen by FOLK_ASPECT:
  shorts    -> 1080x1920, world drawn 1:1
  landscape -> 1920x1080, world drawn at LZ (default 0.7) around the camera centre, so a wider slice of the
               world is visible; screen-glued elements (par == 0: titles, borders, buttons) are fitted to the
               frame height instead so nothing designed for the portrait frame falls off the top or bottom.
Everything is drawn at SS x for anti-aliasing and reduced in finish().
"""
import math, os, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1080, 1920
SS = int(os.environ.get("FOLK_SS", "2"))
INK = (38, 22, 46)

ASPECT = os.environ.get("FOLK_ASPECT", "shorts").strip().lower()
if ASPECT in ("landscape", "wide", "16:9", "16x9", "horizontal", "yt", "youtube"):
    ASPECT = "landscape"; OW, OH = 1920, 1080
    LZ = float(os.environ.get("FOLK_LZ", "0.7"))
else:
    ASPECT = "shorts"; OW, OH = 1080, 1920; LZ = 1.0
UZ = OH / H                                        # scale for screen-glued (par == 0) elements
# extra world width (design units) each side that a wide frame can reveal; 0 for portrait
XPAD = max(0, int((OW / LZ - W) / 2 * 1.25))
# design-space x range covered by the screen for par == 0 elements
UX0, UX1 = W / 2 - OW / 2 / UZ, W / 2 + OW / 2 / UZ

# ---------- easing / keyframes ----------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def smooth(t): t = clamp(t); return t * t * t * (t * (t * 6 - 15) + 10)
def ease_out(t): t = clamp(t); return 1 - (1 - t) ** 3
def ease_in(t): t = clamp(t); return t ** 3
def ease_io(t): t = clamp(t); return 3 * t * t - 2 * t ** 3
def back(t, s=1.70158): t = clamp(t) - 1; return t * t * ((s + 1) * t + s) + 1      # overshoot then settle
def spring(t, k=9.0, d=5.0): t = clamp(t); return 1 - math.exp(-d * t) * math.cos(k * t) if t < 1 else 1.0
def prog(f, a, b): return clamp((f - a) / max(1.0, (b - a)))
def kf(f, keys, ease=smooth):
    """keyframes [(frame, value), ...] -> value at f (values may be numbers or tuples)"""
    if f <= keys[0][0]: return keys[0][1]
    for (f0, v0), (f1, v1) in zip(keys, keys[1:]):
        if f <= f1:
            t = ease((f - f0) / max(1e-9, f1 - f0))
            if isinstance(v0, (tuple, list)): return tuple(lerp(a, b, t) for a, b in zip(v0, v1))
            return lerp(v0, v1, t)
    return keys[-1][1]
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def mixc(a, b, t): return tuple(int(lerp(x, y, t)) for x, y in zip(a, b))
def shade(c, k): return tuple(int(clamp(v * k, 0, 255)) for v in c)

# ---------- outline style ----------
# FOLK_OUTLINE=none (default): pure flat colour, no outlines at all - shapes are separated only by their fills.
# FOLK_OUTLINE=soft: thin lines in a darker tint of the fill.   FOLK_OUTLINE=ink: the classic thick dark-plum line.
# FOLK_OUTLINE_W scales every outline/stroke width.
OUTLINE = os.environ.get("FOLK_OUTLINE", "none").strip().lower()
OLW_K = float(os.environ.get("FOLK_OUTLINE_W", {"none": "0.4", "soft": "0.45"}.get(OUTLINE, "1.0")))
def resolve_ol(fill, ol, olw):
    """-> (outline colour or None, outline width in the caller's units). fill=None marks text, which keeps a thin dark edge."""
    if not ol or olw <= 0: return None, 0
    if OUTLINE == "none" and fill is not None: return None, 0
    if OUTLINE == "soft" and fill is not None and tuple(ol[:3]) == INK:
        ol = mixc(shade(tuple(fill[:3]), 0.6), INK, 0.3)
    return tuple(ol[:3]), olw * OLW_K

# ---------- fonts ----------
_FONT_CACHE = {}
_FONT_PATH = {}
KIT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NEED_DEVANAGARI = os.environ.get("FOLK_DEVANAGARI", "0") == "1"
def _has_devanagari(f):
    """a font without the glyph draws its .notdef box for both characters, so the two renders are identical"""
    try:
        def r(ch):
            im = Image.new("L", (90, 90), 0); ImageDraw.Draw(im).text((8, 8), ch, font=f, fill=255); return im.tobytes()
        return r("\u0915") != r("\ue000") and r("\u0923") != r("\ue000")
    except Exception: return False
def _font_candidates(bold):
    cands = [os.environ.get("FOLK_FONT", "")]
    kit = os.path.join(KIT_DIR, "fonts")
    pat = ["*Bold*.ttf", "*Bold*.otf", "*.ttf", "*.otf"] if bold else ["*Regular*.ttf", "*Regular*.otf", "*.ttf", "*.otf"]
    for p in pat: cands += sorted(glob.glob(os.path.join(kit, p)))
    names = ["NotoSansDevanagari-Bold", "NotoSansDevanagari[wdth,wght]", "NotoSerifDevanagari-Bold", "Mukta-Bold", "Hind-Bold", "Poppins-Bold",
             "NotoSans-Bold", "DejaVuSans-Bold", "FreeSansBold", "FreeSerifBold", "NirmalaB", "segoeuib", "arialbd"] if bold else \
            ["NotoSansDevanagari-Regular", "Mukta-Regular", "Hind-Regular", "Poppins-Regular", "NotoSans-Regular", "DejaVuSans", "FreeSans", "FreeSerif", "Nirmala", "segoeui", "arial"]
    dirs = ["/usr/share/fonts", os.path.expanduser("~/.fonts"), os.path.expanduser("~/.local/share/fonts"), os.path.expanduser("~/Library/Fonts"),
            os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")]
    for n in names:
        for d in dirs:
            if os.path.isdir(d): cands += glob.glob(os.path.join(d, "**", n + ".*"), recursive=True)
    return [p for p in cands if p and os.path.isfile(p)]
def font(size, bold=True):
    """first usable font (bundled kit font first; set FOLK_FONT=/path/font.ttf to force one, FOLK_DEVANAGARI=1 to require Devanagari glyphs)"""
    size = max(4, int(size))
    key = (size, bold)
    if key in _FONT_CACHE: return _FONT_CACHE[key]
    if bold in _FONT_PATH and _FONT_PATH[bold]:
        f = ImageFont.truetype(_FONT_PATH[bold], size); _FONT_CACHE[key] = f; return f
    for p in _font_candidates(bold):
        try:
            f = ImageFont.truetype(p, size)
            if NEED_DEVANAGARI and not _has_devanagari(f): continue
            _FONT_PATH[bold] = p; _FONT_CACHE[key] = f; return f
        except Exception: pass
    _FONT_PATH[bold] = None
    try: f = ImageFont.load_default(size)
    except Exception: f = ImageFont.load_default()
    _FONT_CACHE[key] = f; return f

_GRAD = {}; _VIG = {}
class Canvas:
    def __init__(self):
        self.img = Image.new("RGBA", (OW * SS, OH * SS), (0, 0, 0, 255))
        self.d = ImageDraw.Draw(self.img, "RGBA")
        self.cam = dict(x=W / 2, y=H / 2, zoom=1.0, roll=0.0)

    # ----- camera: parallax factor p (1 = world, 0 = glued to screen)
    @staticmethod
    def Z(par): return UZ if par == 0 else LZ
    def T(self, x, y, par=1.0):
        c = self.cam
        z = 1 + (c['zoom'] - 1) * par
        cx = W / 2 + (c['x'] - W / 2) * par; cy = H / 2 + (c['y'] - H / 2) * par
        dx, dy = (x - cx) * z, (y - cy) * z
        if c['roll']:
            r = math.radians(c['roll']); dx, dy = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
        k = self.Z(par)
        return ((OW / 2 + dx * k) * SS, (OH / 2 + dy * k) * SS)
    def S(self, v, par=1.0): return v * (1 + (self.cam['zoom'] - 1) * par) * SS * self.Z(par)
    def set_cam(self, x=W / 2, y=H / 2, zoom=1.0, roll=0.0): self.cam.update(x=x, y=y, zoom=zoom, roll=roll)

    # ----- background
    def gradient(self, stops):
        key = tuple((p, tuple(c)) for p, c in stops)
        if key not in _GRAD:
            ys = np.linspace(0, 1, OH * SS)
            arr = np.zeros((OH * SS, 1, 3), np.uint8)
            for ch in range(3):
                arr[:, 0, ch] = np.interp(ys, [s[0] for s in stops], [s[1][ch] for s in stops])
            _GRAD[key] = Image.fromarray(arr).resize((OW * SS, OH * SS))
        self.img.paste(_GRAD[key], (0, 0))
    def glow(self, x, y, r, color, alpha=0.8, par=1.0):
        px, py = self.T(x, y, par); pr = max(2, int(self.S(r, par)))
        n = 96; yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
        d = np.clip(1 - np.sqrt(xx * xx + yy * yy), 0, 1)
        a = Image.fromarray((255 * alpha * d ** 2).astype(np.uint8)).resize((2 * pr, 2 * pr), Image.BICUBIC)
        self.img.paste(Image.new("RGB", a.size, tuple(color[:3])), (int(px - pr), int(py - pr)), a)
    def shadow(self, x, y, rx, ry, alpha=0.3, color=(24, 12, 34), par=1.0):
        """soft elliptical ground shadow (world coords)"""
        px, py = self.T(x, y, par); a_ = max(2, int(self.S(rx, par))); b_ = max(2, int(self.S(ry, par)))
        n = 64; yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
        d = np.clip(1 - np.sqrt(xx * xx + yy * yy), 0, 1)
        m = Image.fromarray((255 * alpha * np.sqrt(d)).astype(np.uint8)).resize((2 * a_, 2 * b_), Image.BICUBIC)
        self.img.paste(Image.new("RGB", m.size, tuple(color[:3])), (int(px - a_), int(py - b_)), m)
    def vignette(self, strength=0.45):
        if strength not in _VIG:
            n = 128; yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
            d = np.clip((np.sqrt(xx * xx * 0.8 + yy * yy * 0.6) - 0.55) / 0.9, 0, 1)
            m = Image.fromarray((255 * strength * d ** 1.5).astype(np.uint8)).resize((OW * SS, OH * SS), Image.BICUBIC)
            _VIG[strength] = m
        self.img.paste(Image.new("RGB", (OW * SS, OH * SS), (10, 6, 24)), (0, 0), _VIG[strength])
    def flash(self, a, color=(255, 255, 255)):
        if a > 0.01: self.d.rectangle([0, 0, OW * SS, OH * SS], fill=tuple(color[:3]) + (int(255 * clamp(a)),))

    # ----- primitives (all take world coords)
    def poly(self, pts, fill, ol=INK, olw=5, par=1.0):
        P = [self.T(x, y, par) for x, y in pts]
        if len(P) < 2: return
        ol, olw = resolve_ol(fill, ol, olw)
        if fill is not None and len(P) >= 3:
            if len(fill) == 4 and fill[3] < 255: self._blend_poly(P, fill)
            else: self.d.polygon(P, fill=fill)
        if ol: self.d.line(P + [P[0]], fill=ol, width=max(1, int(self.S(olw, par))), joint="curve")
    def _blend_poly(self, P, fill):
        """translucent fill: Pillow does not blend RGBA colours on RGBA images, so composite a bbox-sized layer"""
        x0, y0 = int(min(p[0] for p in P)) - 1, int(min(p[1] for p in P)) - 1
        x1, y1 = int(max(p[0] for p in P)) + 2, int(max(p[1] for p in P)) + 2
        x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, self.img.width), min(y1, self.img.height)
        if x1 <= x0 or y1 <= y0: return
        lay = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        ImageDraw.Draw(lay).polygon([(x - x0, y - y0) for x, y in P], fill=tuple(fill))
        self.img.alpha_composite(lay, (x0, y0))
    def ell(self, cx, cy, rx, ry, fill, ol=INK, olw=5, par=1.0):
        x, y = self.T(cx, cy, par); a, b = abs(self.S(rx, par)), abs(self.S(ry, par))
        ol, olw = resolve_ol(fill, ol, olw)
        self.d.ellipse([x - a, y - b, x + a, y + b], fill=fill, outline=ol, width=max(1, int(self.S(olw, par))) if ol else 0)
    def clip_ell(self, clip_pts, cx, cy, rx, ry, fill, par=1.0):
        """ellipse clipped to a polygon (L-mode mask over the polygon's bbox) - lets an oversized pupil sit in the eye corner"""
        P = [self.T(x, y, par) for x, y in clip_pts]
        if len(P) < 3: return
        x0, y0 = max(int(min(p[0] for p in P)) - 1, 0), max(int(min(p[1] for p in P)) - 1, 0)
        x1, y1 = min(int(max(p[0] for p in P)) + 2, self.img.width), min(int(max(p[1] for p in P)) + 2, self.img.height)
        if x1 <= x0 or y1 <= y0: return
        mask = Image.new("L", (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in P], fill=255)
        lay = Image.new("RGBA", mask.size, (0, 0, 0, 0))
        x, y = self.T(cx, cy, par); a, b = abs(self.S(rx, par)), abs(self.S(ry, par))
        ImageDraw.Draw(lay).ellipse([x - a - x0, y - b - y0, x + a - x0, y + b - y0], fill=tuple(fill[:3]) + (255,))
        lay.putalpha(ImageChops.multiply(lay.getchannel("A"), mask))
        self.img.alpha_composite(lay, (x0, y0))
    def rrect(self, x0, y0, x1, y1, rad, fill, ol=INK, olw=5, par=1.0):
        a = self.T(x0, y0, par); b = self.T(x1, y1, par)
        box = [min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])]
        rad = min(self.S(rad, par), (box[2] - box[0]) / 2, (box[3] - box[1]) / 2)
        ol, olw = resolve_ol(fill, ol, olw)
        self.d.rounded_rectangle(box, radius=max(0, rad), fill=fill, outline=ol, width=max(1, int(self.S(olw, par))) if ol else 0)
    def line(self, pts, color, w=4, par=1.0):
        if len(pts) < 2: return
        self.d.line([self.T(x, y, par) for x, y in pts], fill=color, width=max(1, int(self.S(w, par))), joint="curve")
    def arc(self, cx, cy, rx, ry, a0, a1, color, w=4, par=1.0):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in np.linspace(a0, a1, 24)]
        self.line(pts, color, w, par)
    def cap(self, p1, p2, r1, r2, fill, ol=INK, olw=5, par=1.0):
        """tapered capsule between two world points (limbs)"""
        def shape(ra, rb, col):
            (x1, y1), (x2, y2) = self.T(*p1, par), self.T(*p2, par)
            ra, rb = abs(self.S(ra, par)), abs(self.S(rb, par))
            ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2; nx, ny = math.cos(ang), math.sin(ang)
            self.d.polygon([(x1 + nx * ra, y1 + ny * ra), (x2 + nx * rb, y2 + ny * rb), (x2 - nx * rb, y2 - ny * rb), (x1 - nx * ra, y1 - ny * ra)], fill=col)
            self.d.ellipse([x1 - ra, y1 - ra, x1 + ra, y1 + ra], fill=col); self.d.ellipse([x2 - rb, y2 - rb, x2 + rb, y2 + rb], fill=col)
        ol, olw = resolve_ol(fill, ol, olw)
        if ol: shape(r1 + olw, r2 + olw, ol)
        shape(r1, r2, fill)
    def dots(self, pts, r, color, par=1.0):
        for x, y in pts:
            a, b = self.T(x, y, par); rr = abs(self.S(r, par)); self.d.ellipse([a - rr, b - rr, a + rr, b + rr], fill=color)

    # ----- text
    def _blit_text(self, s, px, py, size_px, fill, ol, olw_px, scale=1.0, alpha=1.0, bold=True):
        """draw a text block centred at screen pixel (px, py); sizes already in output pixels * SS"""
        if not s or size_px < 2: return
        f = font(size_px, bold)
        tw = max(int(OW * SS), int(f.getlength(s) + size_px * 2))
        tmp = Image.new("RGBA", (tw, int(size_px * 3)), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        td.text((tw / 2, size_px * 1.5), s, font=f, fill=tuple(fill[:3]) + (255,), anchor="mm", stroke_width=int(olw_px) if ol else 0, stroke_fill=(tuple(ol[:3]) if ol else tuple(fill[:3])) + (255,))
        bb = tmp.getbbox()
        if not bb: return
        tmp = tmp.crop(bb)
        if scale != 1.0: tmp = tmp.resize((max(1, int(tmp.width * scale)), max(1, int(tmp.height * scale))), Image.LANCZOS)
        if alpha < 1: tmp.putalpha(tmp.getchannel("A").point(lambda v: int(v * clamp(alpha))))
        self.img.paste(tmp, (int(px - tmp.width / 2), int(py - tmp.height / 2)), tmp)
    def text(self, s, x, y, size, fill=(255, 240, 210), ol=INK, olw=6, scale=1.0, alpha=1.0, par=0.0, bold=True, anchor="mm"):
        k = self.Z(par)
        px, py = self.T(x, y, par)
        ol, olw = resolve_ol(None, ol, olw)          # text keeps a dark edge for legibility, just thinner
        self._blit_text(str(s), px, py, size * k * SS, fill, ol, olw * k * SS, scale, alpha, bold)
    def wrap(self, s, size, maxw):
        """wrap s into lines no wider than maxw (same units as size)"""
        f = font(size * SS); words = str(s).split(); lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if f.getlength(t) / SS <= maxw or not cur: cur = t
            else: lines.append(cur); cur = w
        if cur: lines.append(cur)
        return lines
    def subtitle(self, s, t=1.0, top=150, size=64, maxw=900):
        """Compact, readable caption plate in SCREEN space; prefer 1 line, max 2.
        shorts: plate near the top (top=150 px); landscape: plate anchored above the bottom edge."""
        if not s: return
        s = str(s).strip()
        if ASPECT == "landscape":
            size = int(size * 0.72); maxw = max(maxw, 1500)
            sizes = [size] + [v for v in (44, 40, 36, 32, 28, 24) if v < size]
        else:
            sizes = [size] + [v for v in (60, 56, 52, 48, 44, 40, 36, 32, 28) if v < size]
        lines = [s]
        for candidate in sizes:
            size = candidate
            lines = self.wrap(s, size, maxw)
            if len(lines) <= 2: break
        if len(lines) > 2:                                   # extremely long caption: force 2 lines, shrink to fit
            words = s.split(); mid = len(words) // 2
            lines = [" ".join(words[:mid]), " ".join(words[mid:])]
            f = font(size * SS)
            while size > 14 and max(f.getlength(l) / SS for l in lines) > maxw:
                size -= 2; f = font(size * SS)
        f = font(size * SS)
        text_w = max((f.getlength(line) / SS for line in lines), default=0)
        plate_w = min(maxw + 36, max(340, text_w + 76))
        lh = size * 1.24; hh = lh * len(lines) + 34
        sc = 0.96 + 0.04 * back(t); a = clamp(t * 2.5)
        cy = (OH - 70 - hh / 2) if ASPECT == "landscape" else (top + hh / 2)
        x0, x1 = OW / 2 - plate_w / 2 * sc, OW / 2 + plate_w / 2 * sc
        y0 = cy - hh / 2 * sc
        lay = Image.new("RGBA", (OW * SS, OH * SS), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, (y0 + hh * sc) * SS], radius=30 * SS, fill=(14, 10, 40, int(190 * a)))
        self.img.alpha_composite(lay)
        for i, ln in enumerate(lines):
            self._blit_text(ln, OW / 2 * SS, (y0 + (17 + lh * (i + 0.5)) * sc) * SS, size * SS, (255, 246, 226), (20, 12, 44), 5 * SS * OLW_K, scale=sc, alpha=a)
    def finish(self):
        im = self.img.reduce(SS).convert("RGB") if SS > 1 else self.img.convert("RGB")
        return grade(im) if GRADE != "none" else im

# ---------- colour grade ----------
# FOLK_GRADE=series (default): cinematic "series" look - desaturated, darker midtones, plum shadows / amber highlights,
# fine film grain. FOLK_GRADE=none keeps the raw bright colours.  FOLK_GRADE_K scales the strength (1.0 default).
GRADE = os.environ.get("FOLK_GRADE", "series").strip().lower()
GRADE_K = clamp(float(os.environ.get("FOLK_GRADE_K", "1.0")), 0.0, 2.0)
_GRAIN = None
_LUT = None
_MASKS = None
def _lut():
    global _LUT
    if _LUT is None:
        xs = np.linspace(0, 1, 256)
        y = xs ** (1 + 0.10 * GRADE_K)                                         # darker midtones
        y = 0.5 + (y - 0.5) * (1 + 0.10 * GRADE_K)                             # a little more contrast
        y = y * (1 - 0.06 * GRADE_K) + 0.02 * GRADE_K                           # lift blacks slightly, pull whites off peak
        _LUT = [int(round(v * 255)) for v in np.clip(y, 0, 1)] * 3            # one 8-bit curve per RGB channel for Image.point
    return _LUT
def _masks():
    """8-bit luma -> shadow / highlight blend weights (the sh*0.22K and hi*0.14K terms of the split tone)"""
    global _MASKS
    if _MASKS is None:
        l = np.arange(256) / 255.0
        sh = np.clip(1 - l * 1.6, 0, 1) * 0.22 * GRADE_K
        hi = np.clip(l * 1.6 - 0.6, 0, 1) * 0.14 * GRADE_K
        _MASKS = ([int(round(v * 255)) for v in sh], [int(round(v * 255)) for v in hi])
    return _MASKS
def _grain(w, h):
    global _GRAIN
    if _GRAIN is None or _GRAIN.size[1] < h + 256 or _GRAIN.size[0] < w + 256:
        g = np.random.RandomState(7).normal(0, 1, (h + 256, w + 256)) * 0.018 * GRADE_K * 255 + 128
        _GRAIN = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "L").convert("RGB")        # noise stored around 128
    return _GRAIN
def grade(im):
    """series tone: desaturate, tone curve, split tone, grain.
    Same maths as the original float pipeline but run through Pillow's C ops (blend / point / composite / add),
    ~15x faster; per-pixel results differ only by 8-bit rounding (<= 2 levels)."""
    im = Image.blend(im.convert("L").convert("RGB"), im, 1 - 0.22 * GRADE_K)                        # desaturate
    im = im.point(_lut())
    lum = im.convert("L")
    sh, hi = _masks()
    im = Image.composite(Image.new("RGB", im.size, (41, 20, 66)), im, lum.point(sh))               # plum shadows
    im = Image.composite(Image.new("RGB", im.size, (255, 219, 158)), im, lum.point(hi))            # amber highlights
    w, h = im.size
    ox, oy = np.random.randint(0, 256, 2)[::-1]
    return ImageChops.add(im, _grain(w, h).crop((ox, oy, ox + w, oy + h)), 1.0, -128)
