"""folk2d.world - folk-art backdrops, ornaments and FX. Everything is flat shapes with a thin self-tinted outline (see draw.resolve_ol)."""
import math, random
from .draw import *

SKY = {
    "night":   [(0, (10, 12, 48)), (0.55, (38, 28, 100)), (1, (104, 58, 142))],
    "dusk":    [(0, (44, 30, 104)), (0.5, (196, 78, 110)), (1, (255, 168, 78))],
    "day":     [(0, (60, 130, 226)), (0.6, (140, 196, 250)), (1, (255, 232, 176))],
    "dawn":    [(0, (70, 60, 150)), (0.55, (250, 140, 120)), (1, (255, 214, 130))],
    "dream":   [(0, (30, 20, 80)), (0.5, (110, 50, 140)), (1, (230, 110, 150))],
    "storm":   [(0, (22, 26, 54)), (0.6, (54, 62, 100)), (1, (96, 104, 140))],
    "heaven":  [(0, (34, 40, 130)), (0.55, (90, 90, 200)), (1, (240, 200, 255))],
    "fire":    [(0, (50, 14, 40)), (0.6, (190, 50, 40)), (1, (255, 170, 50))],
}
GOLD = (255, 196, 60); SAFFRON = (255, 150, 48); CREAM = (255, 240, 208); CRIMSON = (188, 34, 62)
EMERALD = (26, 150, 104); AZURE = (70, 140, 224); PLUM = (84, 44, 124); TEAL = (20, 128, 134)

def sky(c, kind="night"):
    if isinstance(kind, str):
        k = kind.strip().lower()
        if k not in SKY: k = "night"
        c.gradient(SKY[k])
    else: c.gradient(kind)

def stars(c, f, n=70, seed=3, par=0.05, ymax=1100):
    r = random.Random(seed)
    n = int(n * (W + 2 * XPAD) / W)
    for i in range(n):
        x, y, s = r.uniform(-XPAD, W + XPAD), r.uniform(60 - XPAD * 0.3, ymax), r.uniform(2.5, 7)
        tw = 0.6 + 0.4 * math.sin(f * 0.12 + i * 1.7)
        c.d.regular_polygon((*c.T(x, y, par), c.S(s * tw, par) * 1.6), 4, rotation=45, fill=(255, 244, 200, int(230 * tw)))

def sun(c, x, y, r, f=0, rays=True, par=0.3, col=(255, 190, 70)):
    c.glow(x, y, r * 3.2, (255, 170, 80), 0.75, par)
    if rays:
        n = 24
        for i in range(n):
            a = math.radians(i * 360 / n + f * 0.6); w = math.radians(5.5)
            r0, r1 = r * 1.15, r * (1.75 if i % 2 else 2.25)
            c.poly([(x + r0 * math.cos(a - w), y + r0 * math.sin(a - w)), (x + r1 * math.cos(a), y + r1 * math.sin(a)), (x + r0 * math.cos(a + w), y + r0 * math.sin(a + w))], (255, 214, 110), INK, 4, par)
    c.ell(x, y, r, r, col, INK, 7, par); c.ell(x, y, r * 0.72, r * 0.72, (255, 214, 100), INK, 4, par); c.ell(x, y, r * 0.38, r * 0.38, (255, 240, 170), None, 0, par)

def moon(c, x, y, r, par=0.08):
    c.glow(x, y, r * 3, (200, 200, 255), 0.5, par); c.ell(x, y, r, r, (250, 244, 214), INK, 6, par)
    c.ell(x + r * 0.35, y - r * 0.15, r * 0.88, r * 0.88, (38, 28, 100), None, 0, par)

def cloud(c, x, y, s=1.0, par=0.6, fill=(250, 236, 255), shadow=(190, 170, 230)):
    puffs = [(-90, 10, 55), (-35, -20, 70), (35, -10, 62), (90, 14, 50), (0, 25, 70)]
    for dx, dy, rr in puffs: c.ell(x + dx * s, y + dy * s + 8 * s, rr * s + 5 * s, rr * s + 5 * s, INK, None, 0, par)
    for dx, dy, rr in puffs: c.ell(x + dx * s, y + dy * s + 8 * s, rr * s, rr * s, shadow, None, 0, par)
    for dx, dy, rr in puffs: c.ell(x + dx * s, y + dy * s, rr * s, rr * s, fill, None, 0, par)
    for dx, dy, rr in puffs[:4]: c.arc(x + dx * s, y + dy * s + 4 * s, rr * s * 0.55, rr * s * 0.55, 200, 330, shadow, 4 * s, par)

def hills(c, base, amp, color, seed=1, par=0.4, ol=INK, step=36, wl=420):
    r = random.Random(seed); ph = [r.uniform(0, 6.3) for _ in range(3)]
    pts = []
    for x in range(-400 - XPAD, W + 401 + XPAD, step):
        y = base - amp * (0.55 * math.sin(x / wl + ph[0]) + 0.3 * math.sin(x / (wl * 0.43) + ph[1]) + 0.15 * math.sin(x / (wl * 0.2) + ph[2]))
        pts.append((x, y))
    c.poly(pts + [(W + 400 + XPAD, H + 400), (-400 - XPAD, H + 400)], color, ol, 6, par)

def mountain(c, x, y, w, h, color=(70, 60, 140), snow=True, par=0.5):
    pk = (x, y - h)
    c.poly([(x - w / 2, y), pk, (x + w / 2, y)], color, INK, 6, par)
    c.poly([(x, y - h), (x + w / 2, y), (x + w * 0.08, y)], shade(color, 0.82), None, 0, par)
    if snow:
        c.poly([pk, (x - w * 0.14, y - h * 0.72), (x - w * 0.04, y - h * 0.78), (x + w * 0.04, y - h * 0.7), (x + w * 0.14, y - h * 0.72)], (250, 246, 255), INK, 5, par)

def ground(c, y, color=(120, 70, 60), band=(255, 170, 60), par=1.0):
    x0, x1 = -600 - XPAD, W + 600 + XPAD
    c.poly([(x0, y), (x1, y), (x1, H + 900), (x0, H + 900)], color, INK, 6, par)
    c.poly([(x0, y), (x1, y), (x1, y + 26), (x0, y + 26)], band, INK, 4, par)
    for x in range(x0 + 40, x1, 70): c.dots([(x, y + 13)], 4.5, (130, 50, 40), par)

def tree(c, x, y, s=1.0, par=1.0, leaf=(34, 150, 96), trunk=(120, 76, 56)):
    c.poly([(x - 20 * s, y), (x - 11 * s, y - 190 * s), (x + 11 * s, y - 190 * s), (x + 20 * s, y)], trunk, INK, 5, par)
    for dx, dy, rr in [(-70, -230, 70), (0, -290, 88), (72, -228, 68), (0, -200, 70)]:
        c.ell(x + dx * s, y + dy * s, rr * s, rr * s, leaf, INK, 5, par)
    for dx, dy in [(-30, -250), (30, -310), (50, -220), (-60, -210)]:
        c.dots([(x + dx * s, y + dy * s)], 6 * s, (255, 200, 80), par)

def hut(c, x, y, s=1.0, par=1.0, wall=(214, 150, 100), roof=(150, 100, 60)):
    c.rrect(x - 110 * s, y - 130 * s, x + 110 * s, y, 8, wall, INK, 5, par)
    c.poly([(x - 150 * s, y - 120 * s), (x, y - 250 * s), (x + 150 * s, y - 120 * s)], roof, INK, 6, par)
    for i in range(-3, 4): c.line([(x + i * 36 * s, y - 128 * s - (1 - abs(i) / 4) * 0 ), (x + i * 20 * s, y - 232 * s + abs(i) * 14 * s)], shade(roof, 0.7), 3, par)
    c.rrect(x - 26 * s, y - 92 * s, x + 26 * s, y, 20, (96, 54, 44), INK, 5, par)
    c.dots([(x - 80 * s, y - 70 * s), (x + 80 * s, y - 70 * s)], 7 * s, (255, 200, 80), par)

def temple(c, x, y, s=1.0, par=0.7, col=(240, 200, 150)):
    for i in range(4): c.rrect(x - (150 - i * 16) * s, y - (i + 1) * 26 * s, x + (150 - i * 16) * s, y - i * 26 * s, 4, shade(col, 1 - i * 0.04), INK, 5, par)
    c.rrect(x - 90 * s, y - 330 * s, x + 90 * s, y - 104 * s, 6, col, INK, 6, par)
    c.poly([(x - 100 * s, y - 330 * s), (x - 60 * s, y - 420 * s), (x - 24 * s, y - 500 * s), (x, y - 590 * s), (x + 24 * s, y - 500 * s), (x + 60 * s, y - 420 * s), (x + 100 * s, y - 330 * s)], shade(col, 0.93), INK, 6, par)
    c.line([(x, y - 590 * s), (x, y - 640 * s)], (104, 70, 44), 5, par); c.poly([(x, y - 640 * s), (x + 56 * s, y - 622 * s), (x, y - 604 * s)], SAFFRON, INK, 4, par)
    c.rrect(x - 34 * s, y - 250 * s, x + 34 * s, y - 104 * s, 30, (110, 50, 60), INK, 5, par)

def throne(c, x, y, s=1.0, par=0.8):
    """Indra's cloud-throne: cusped arch, pillars, lotus cushion"""
    for sx in (-1, 1):
        c.rrect(x + sx * 190 * s - 26 * s, y - 520 * s, x + sx * 190 * s + 26 * s, y, 10, (255, 196, 70), INK, 6, par)
        c.ell(x + sx * 190 * s, y - 520 * s, 38 * s, 22 * s, (255, 220, 110), INK, 5, par)
    pts = [(x - 190 * s, y - 520 * s), (x - 190 * s, y - 640 * s), (x - 90 * s, y - 700 * s), (x, y - 790 * s), (x + 90 * s, y - 700 * s), (x + 190 * s, y - 640 * s), (x + 190 * s, y - 520 * s)]
    c.poly(pts, (150, 40, 90), INK, 6, par); c.poly([(x - 150 * s, y - 540 * s), (x, y - 740 * s), (x + 150 * s, y - 540 * s)], (255, 196, 70), INK, 5, par)
    c.rrect(x - 160 * s, y - 120 * s, x + 160 * s, y, 18, (255, 196, 70), INK, 6, par)
    c.rrect(x - 130 * s, y - 190 * s, x + 130 * s, y - 112 * s, 24, (200, 40, 80), INK, 5, par)
    c.dots([(x + i * 40 * s, y - 150 * s) for i in range(-3, 4)], 6 * s, (255, 224, 140), par)

def lotus(c, x, y, r, fill=(255, 150, 190), par=1.0):
    for a in (-60, -30, 0, 30, 60):
        t = math.radians(a - 90)
        pts = [(x, y), (x + r * 0.5 * math.cos(t - 0.35), y + r * 0.5 * math.sin(t - 0.35)), (x + r * math.cos(t), y + r * math.sin(t)), (x + r * 0.5 * math.cos(t + 0.35), y + r * 0.5 * math.sin(t + 0.35))]
        c.poly(pts, fill, INK, 4, par)

def mandala(c, x, y, r, f=0, col=GOLD, n=12, par=1.0, spin=0.5, fill_to=None):
    """ring of petals / beads; fill_to (0..n) lights beads one by one (counters)"""
    for i in range(n):
        a = math.radians(i * 360 / n + f * spin - 90); px, py = x + r * math.cos(a), y + r * math.sin(a)
        lit = fill_to is None or i < fill_to
        rb = min(r * 0.07, 30); c.ell(px, py, rb, rb, col if lit else (60, 46, 110), INK, 4, par)
        if lit: c.ell(px - rb * 0.3, py - rb * 0.3, rb * 0.3, rb * 0.3, (255, 250, 220), None, 0, par)

def bead_ring(c, x, y, r, n, lit, par=0.0, col=GOLD):
    mandala(c, x, y, r, 0, col, n, par, 0, fill_to=lit)

def border(c, y, f=0, col=GOLD, par=0.0, up=False):
    """folk ornament strip (kolam diamonds + dots) across the frame"""
    lo, hi = (UX0, UX1) if par == 0 else (-XPAD - 200, W + XPAD + 200)
    for i in range(int(lo // 90) - 1, int(hi // 90) + 2):
        x = i * 90 + (f * 0.4) % 90
        c.poly([(x, y), (x + 36, y - 28 * (-1 if up else 1)), (x + 72, y), (x + 36, y + 28 * (-1 if up else 1))], col, INK, 4, par)
        c.dots([(x + 36, y)], 7, CRIMSON, par)

def sparks(c, x, y, f, f0, n=14, seed=1, col=(255, 220, 120), reach=170, par=1.0, life=26):
    t = (f - f0) / life
    if t < 0 or t >= 1: return
    r = random.Random(seed)
    for i in range(n):
        a = r.uniform(0, 6.28); d = reach * ease_out(t) * r.uniform(0.5, 1)
        sz = max(0.5, 9 * (1 - t) * r.uniform(0.6, 1.2))
        c.d.regular_polygon((*c.T(x + math.cos(a) * d, y + math.sin(a) * d - 30 * t, par), max(1.0, c.S(sz, par) * 1.6)), 4, rotation=45, fill=col + (int(255 * (1 - t)),))

def ring_wave(c, x, y, f, f0, r=300, col=(255, 230, 150), par=1.0, life=24):
    t = (f - f0) / life
    if 0 <= t <= 1:
        rr = r * ease_out(t); a = c.T(x, y, par); s = c.S(rr, par)
        c.d.ellipse([a[0] - s, a[1] - s, a[0] + s, a[1] + s], outline=col + (int(255 * (1 - t)),), width=max(2, int(c.S(10 * (1 - t) + 2, par))))

def drop(c, x, y, r=14, col=(210, 30, 50), par=1.0):
    c.poly([(x, y - r * 2), (x + r * 0.9, y - r * 0.3), (x, y + r), (x - r * 0.9, y - r * 0.3)], col, INK, 3, par); c.ell(x, y - r * 0.2, r * 0.9, r * 0.9, col, INK, 3, par)

def rays_burst(c, x, y, f, r0=120, r1=None, n=18, col=(255, 230, 150, 70), par=0.2, spin=0.4):
    if r1 is None: r1 = 1400 + XPAD
    for i in range(n):
        if i % 2: continue
        a = math.radians(i * 360 / n + f * spin); w = math.radians(360 / n * 0.5)
        P = [c.T(x + r0 * math.cos(a), y + r0 * math.sin(a), par), c.T(x + r1 * math.cos(a - w), y + r1 * math.sin(a - w), par), c.T(x + r1 * math.cos(a + w), y + r1 * math.sin(a + w), par)]
        c.d.polygon(P, fill=col)

def swirl(c, x, y, f, s=1.0, par=0.0, col=(255, 230, 150)):
    """thought / dream swirl bubble"""
    for i, (dx, dy, r) in enumerate([(-60, 60, 10), (-30, 25, 16), (0, -20, 24)]): c.ell(x + dx * s, y + dy * s, r * s, r * s, col, INK, 4, par)

def paper_plane(c, x, y, s=1.0, rot=-20, par=0.0):
    r = math.radians(rot)
    def R(px, py): return (x + (px * math.cos(r) - py * math.sin(r)) * s, y + (px * math.sin(r) + py * math.cos(r)) * s)
    c.poly([R(-90, 10), R(110, 0), R(-30, 70)], (255, 244, 214), INK, 5, par); c.poly([R(-90, 10), R(110, 0), R(-30, -50)], (240, 214, 170), INK, 5, par)
    c.line([R(-90, 10), R(-30, 70)], (214, 190, 150), 4, par)

def follow_button(c, x, y, t, label="Follow", done="Following", par=0.0):
    k = prog(t, 0.55, 0.75); lab = done if k > 0.5 else label
    col = mixc((255, 130, 60), (60, 190, 120), ease_io(k)); sc = 1 + 0.08 * math.sin(k * math.pi)
    c.rrect(x - 190 * sc, y - 64 * sc, x + 190 * sc, y + 64 * sc, 60 * sc, col, INK, 6, par)
    c.text(lab, x, y, 62 * sc, (255, 250, 236), INK, 4)

# ---------- extra set pieces ----------
def river(c, y, h=120, f=0, par=1.0, col=(60, 140, 210), foam=(200, 230, 255)):
    """water band across the frame with drifting wave lines"""
    x0, x1 = -600 - XPAD, W + 600 + XPAD
    c.poly([(x0, y), (x1, y), (x1, y + h), (x0, y + h)], col, INK, 5, par)
    for row in range(3):
        yy = y + 20 + row * (h - 30) / 3
        for x in range(x0, x1, 140):
            xx = x + (f * (1.2 + row * 0.4) + row * 47) % 140
            c.arc(xx, yy, 26, 8, 200, 340, foam, 3, par)

def ocean(c, y, f=0, par=1.0, col=(30, 90, 170), deep=(16, 50, 120)):
    """sea filling the frame below y with rolling wave crests"""
    x0, x1 = -600 - XPAD, W + 600 + XPAD
    c.poly([(x0, y), (x1, y), (x1, H + 900), (x0, H + 900)], deep, INK, 5, par)
    for row in range(4):
        yy = y + row * 70; step = 180 + row * 30; ph = (f * (1.5 - row * 0.25) + row * 60) % step
        pts = []
        for x in range(x0, x1 + step, step // 6):
            k = ((x + ph) % step) / step
            pts.append((x, yy - 26 * abs(math.sin(k * math.pi)) * (1 if k < 0.6 else 0.6)))
        c.poly(pts + [(x1 + step, yy + 90), (x0, yy + 90)], mixc(col, deep, row / 4), INK, 4, par)
        for x in range(x0, x1, step):
            xx = x + ph + step * 0.5; c.arc(xx, yy - 20, 34, 10, 190, 350, (220, 240, 255), 4, par)

def palace(c, x, y, s=1.0, par=0.7, col=(240, 214, 160), dome=(255, 196, 60)):
    """many-domed palace / fort (Ayodhya, Lanka: pass col/dome for mood)"""
    c.rrect(x - 420 * s, y - 220 * s, x + 420 * s, y, 8, shade(col, 0.9), INK, 6, par)
    for i in range(-5, 6): c.rrect(x + i * 76 * s - 22 * s, y - 250 * s, x + i * 76 * s + 22 * s, y - 220 * s, 4, shade(col, 0.9), INK, 4, par)
    for dx, h, w in ((-300, 440, 90), (300, 440, 90), (0, 560, 130), (-150, 380, 70), (150, 380, 70)):
        c.rrect(x + (dx - w) * s, y - h * s, x + (dx + w) * s, y - 200 * s, 6, col, INK, 6, par)
        c.ell(x + dx * s, y - h * s, (w + 14) * s, (w + 14) * s * 0.9, dome, INK, 6, par)
        c.line([(x + dx * s, y - (h + w + 10) * s), (x + dx * s, y - (h + w + 60) * s)], (104, 70, 44), 5, par); c.poly([(x + dx * s, y - (h + w + 60) * s), (x + (dx + 40) * s, y - (h + w + 46) * s), (x + dx * s, y - (h + w + 32) * s)], SAFFRON, INK, 4, par)
        for k in range(-1, 2): c.rrect(x + (dx + k * 40 - 12) * s, y - (h - 60) * s, x + (dx + k * 40 + 12) * s, y - (h - 110) * s, 12, (110, 50, 60), INK, 4, par)
    c.rrect(x - 70 * s, y - 180 * s, x + 70 * s, y, 60, (110, 50, 60), INK, 6, par)
    for i in range(-4, 5): c.dots([(x + i * 90 * s, y - 120 * s)], 9 * s, dome, par)

def fire(c, x, y, s=1.0, f=0, par=1.0, n=5):
    """folk flame cluster with glow; use for yagna fire, burning Lanka, torches"""
    c.glow(x, y - 80 * s, 260 * s, (255, 150, 50), 0.7, par)
    for i in range(n):
        ph = f * 0.35 + i * 1.9; dx = (i - (n - 1) / 2) * 44 * s; h = (150 + 50 * math.sin(ph)) * s * (1 - abs(i - (n - 1) / 2) * 0.18)
        wob = 14 * s * math.sin(ph * 1.3)
        c.poly([(x + dx - 34 * s, y), (x + dx - 20 * s + wob, y - h * 0.5), (x + dx + wob * 1.5, y - h), (x + dx + 20 * s + wob, y - h * 0.55), (x + dx + 34 * s, y)], (255, 130, 40), INK, 4, par)
        c.poly([(x + dx - 16 * s, y), (x + dx + wob * 0.8, y - h * 0.55), (x + dx + 16 * s, y)], (255, 230, 120), None, 0, par)
    for i in range(6):
        t = ((f * 0.04 + i * 0.37) % 1.0); c.dots([(x + math.sin(i * 2.1 + f * 0.1) * 60 * s, y - (120 + 220 * t) * s)], 5 * s * (1 - t), (255, 210, 120), par)

def rain(c, f, n=120, seed=5, par=0.9, col=(200, 220, 255, 170), slant=0.25):
    r = random.Random(seed)
    for i in range(n):
        x0 = r.uniform(-XPAD - 200, W + XPAD + 200); sp = r.uniform(26, 44); L = r.uniform(40, 90)
        y0 = (r.uniform(0, H) + f * sp) % (H + 400) - 200
        a, b = c.T(x0, y0, par), c.T(x0 - L * slant, y0 + L, par)
        c.d.line([a, b], fill=col, width=max(1, int(c.S(3, par))))

def lightning(c, x, y0, y1, f, f0, seed=1, par=0.8, life=8):
    """jagged bolt visible for `life` frames after f0 (pair with flash + 'thunk'/'rumble' cue)"""
    if not (f0 <= f < f0 + life): return
    r = random.Random(seed + int(f0)); pts = [(x, y0)]
    n = 7
    for i in range(1, n + 1):
        pts.append((x + r.uniform(-90, 90), y0 + (y1 - y0) * i / n))
    a = 1 - (f - f0) / life
    c.line(pts, (255, 255, 255), 14 * a + 4, par); c.line(pts, (220, 230, 255), 5, par)
    c.glow(pts[-1][0], pts[-1][1], 180, (220, 230, 255), 0.6 * a, par)

def arrow(c, x, y, ang=0, L=260, s=1.0, par=1.0, glow_col=None):
    """arrow centred at x,y pointing along ang (deg, 0 = right, -90 = up)"""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    if glow_col: c.glow(x + ux * L * 0.4, y + uy * L * 0.4, 70 * s, glow_col, 0.8, par)
    c.line([(x - ux * L / 2, y - uy * L / 2), (x + ux * L / 2 - ux * 30 * s, y + uy * L / 2 - uy * 30 * s)], (200, 160, 90), 6 * s, par)
    tip = (x + ux * L / 2, y + uy * L / 2); b = (x + ux * (L / 2 - 44 * s), y + uy * (L / 2 - 44 * s))
    c.poly([tip, (b[0] + nx * 12 * s, b[1] + ny * 12 * s), (b[0] - nx * 12 * s, b[1] - ny * 12 * s)], (236, 240, 250), INK, 3 * s, par)
    t = (x - ux * L / 2, y - uy * L / 2)
    for sd in (-1, 1): c.poly([t, (t[0] + ux * 40 * s + nx * sd * 16 * s, t[1] + uy * 40 * s + ny * sd * 16 * s), (t[0] + ux * 50 * s, t[1] + uy * 50 * s)], CRIMSON, INK, 3 * s, par)

def chariot(c, x, y, s=1.0, f=0, flip=False, par=1.0, col=(255, 196, 60)):
    """war chariot (no horse: draw_animal 'horse' in front); rider stands at (x - 20*s, y - 110*s)"""
    sx = -1 if flip else 1
    for wx in (-90, 90):
        c.ell(x + wx * s * sx, y - 70 * s, 76 * s, 76 * s, (150, 90, 50), INK, 6 * s, par)
        for i in range(6):
            a = math.radians(i * 30 + f * 6); c.line([(x + wx * s * sx + math.cos(a) * 70 * s, y - 70 * s + math.sin(a) * 70 * s), (x + wx * s * sx - math.cos(a) * 70 * s, y - 70 * s - math.sin(a) * 70 * s)], (120, 70, 40), 5 * s, par)
        c.ell(x + wx * s * sx, y - 70 * s, 16 * s, 16 * s, GOLD, INK, 4 * s, par)
    c.rrect(x - 170 * s, y - 250 * s, x + 170 * s, y - 110 * s, 20, col, INK, 6 * s, par)
    c.poly([(x - 170 * s, y - 250 * s), (x - 140 * s, y - 320 * s), (x + 140 * s, y - 320 * s), (x + 170 * s, y - 250 * s)], shade(col, 0.9), INK, 5 * s, par)
    for i in range(-3, 4): c.dots([(x + i * 44 * s, y - 180 * s)], 8 * s, CRIMSON, par)
    c.line([(x + sx * 170 * s, y - 130 * s), (x + sx * 330 * s, y - 150 * s)], (150, 90, 50), 10 * s, par)
    c.line([(x - sx * 100 * s, y - 320 * s), (x - sx * 100 * s, y - 520 * s)], (150, 90, 50), 7 * s, par)
    c.poly([(x - sx * 100 * s, y - 520 * s), (x - sx * 100 * s + sx * 130 * s, y - 480 * s), (x - sx * 100 * s, y - 430 * s)], SAFFRON, INK, 4 * s, par)

def boat(c, x, y, s=1.0, f=0, par=1.0, col=(150, 90, 50)):
    bob = math.sin(f * 0.1) * 8 * s; y = y + bob
    c.poly([(x - 220 * s, y - 60 * s), (x + 220 * s, y - 60 * s), (x + 150 * s, y + 30 * s), (x - 150 * s, y + 30 * s)], col, INK, 6, par)
    c.poly([(x - 220 * s, y - 60 * s), (x - 290 * s, y - 150 * s), (x - 200 * s, y - 30 * s)], col, INK, 5, par)
    c.line([(x - 200 * s, y - 60 * s), (x + 200 * s, y - 60 * s)], GOLD, 6 * s, par)
    c.line([(x, y - 60 * s), (x, y - 380 * s)], (120, 70, 40), 9 * s, par)
    c.poly([(x, y - 380 * s), (x + 190 * s, y - 100 * s), (x + 10 * s, y - 100 * s)], (250, 240, 214), INK, 5, par)

def bridge(c, x0, x1, y, f=0, built=1.0, par=1.0):
    """stone causeway (Rama Setu) from x0 to x1; built 0..1 grows it left to right"""
    n = 14; L = (x1 - x0) * clamp(built)
    for i in range(int(n * clamp(built)) + (1 if built > 0 else 0)):
        bx = x0 + (x1 - x0) * i / n
        if bx > x0 + L + 1: break
        r = random.Random(i)
        c.ell(bx + 40, y + 10, 64, 34, (150, 140, 130), INK, 5, par)
        c.ell(bx + 40 + r.uniform(-20, 20), y - 20, 50, 28, (190, 180, 170), INK, 5, par)
        c.dots([(bx + 40 + r.uniform(-30, 30), y - 40)], 8, (230, 224, 210), par)

def cave(c, x, y, s=1.0, par=0.9, col=(70, 50, 70)):
    c.ell(x, y - 160 * s, 360 * s, 300 * s, col, INK, 7, par)
    c.poly([(x - 360 * s, y), (x + 360 * s, y), (x + 360 * s, y + 60 * s), (x - 360 * s, y + 60 * s)], col, None, 0, par)
    c.ell(x, y - 60 * s, 170 * s, 190 * s, (18, 12, 30), INK, 6, par)
    c.poly([(x - 170 * s, y), (x + 170 * s, y), (x + 170 * s, y + 30 * s), (x - 170 * s, y + 30 * s)], (18, 12, 30), None, 0, par)
    for i in range(-3, 4): c.poly([(x + i * 44 * s - 10 * s, y - 240 * s), (x + i * 44 * s, y - 180 * s + abs(i) * 14 * s), (x + i * 44 * s + 10 * s, y - 240 * s)], shade(col, 0.8), INK, 3, par)

def flag(c, x, y, s=1.0, f=0, par=1.0, col=SAFFRON, pole=(150, 90, 50)):
    c.line([(x, y), (x, y - 420 * s)], pole, 8 * s, par)
    w = math.sin(f * 0.25) * 14 * s
    c.poly([(x, y - 420 * s), (x + 220 * s, y - 380 * s + w), (x, y - 300 * s)], col, INK, 4, par)
    c.ell(x, y - 430 * s, 12 * s, 12 * s, GOLD, INK, 3, par)

def pillar(c, x, y, h=600, s=1.0, par=0.8, col=(240, 214, 160)):
    c.rrect(x - 40 * s, y - h * s, x + 40 * s, y, 6, col, INK, 5, par)
    c.rrect(x - 60 * s, y - h * s - 40 * s, x + 60 * s, y - h * s, 8, shade(col, 0.9), INK, 5, par)
    c.rrect(x - 60 * s, y - 36 * s, x + 60 * s, y, 8, shade(col, 0.9), INK, 5, par)
    for k in range(3): c.line([(x - 30 * s, y - h * s * (0.25 + k * 0.25)), (x + 30 * s, y - h * s * (0.25 + k * 0.25))], shade(col, 0.8), 3 * s, par)

def crowd(c, y, f=0, n=9, x0=-200, x1=W + 200, par=0.85, seed=2, cols=((200, 60, 60), (60, 120, 200), (230, 170, 60), (60, 160, 110))):
    """silhouette crowd of simple people along a line (far background army / villagers)"""
    r = random.Random(seed)
    for i in range(n):
        x = x0 + (x1 - x0) * (i + 0.5) / n + r.uniform(-30, 30); s = r.uniform(0.5, 0.7); col = cols[i % len(cols)]
        bob = math.sin(f * 0.12 + i) * 3
        c.rrect(x - 40 * s, y - 180 * s + bob, x + 40 * s, y, 20, col, INK, 4, par)
        c.ell(x, y - 230 * s + bob, 40 * s, 44 * s, (200, 150, 110), INK, 4, par)
        c.ell(x, y - 262 * s + bob, 44 * s, 20 * s, shade(col, 0.8), INK, 3, par)

def pop_text(c, s, x, y, t, size=120, fill=(255, 230, 140), ol=INK, par=0.0):
    """title that pops in with overshoot (t 0..1) - handy for names / numbers"""
    if t <= 0: return
    c.text(s, x, y, size, fill, ol, 8, scale=0.6 + 0.4 * back(t), alpha=clamp(t * 3), par=par)
