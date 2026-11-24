import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("grief", "The ashes of grief still linger"),
    ("himalayas", "is quietly burning deep within"),
    ("penance", "Princess Parvati sheds her heavy silks"),
    ("shiva", "Lord Shiva sits deep in eternal meditation"),
    ("winter", "Undeterred, Parvati stands unwavering"),
    ("summer", "Then summer arrives with scorching"),
    ("shaking", "Her unrelenting penance shakes the heavens"),
    ("devotion", "Even the ancient mountains seem"),
    ("discipline", "Day after day, month after month"),
    ("awakening", "Shiva finally opens his third eye"),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"himalayas", "shiva", "summer", "awakening"}

def shot_at(f):
    for n, a, b in SHOTS:
        if a <= f < b: return n, a, b
    return SHOTS[-1]

def cam(c, lf, n, z=(1.0, 1.0), x=(W / 2, W / 2), y=(1130, 1130), roll=0.0, kicks=()):
    p = smooth(lf / max(1, n)); creep = lf * 0.0004
    kx = ky = 0.0
    for f0, amp in kicks:
        d = lf - f0
        if 0 <= d < 9: kx += amp * math.sin(d * 2.4) * (1 - d / 9); ky += amp * 0.6 * math.cos(d * 3.1) * (1 - d / 9)
    c.set_cam(lerp(x[0], x[1], p) + kx, lerp(y[0], y[1], p) + ky, lerp(z[0], z[1], p) + creep, roll)

def pop(f, f0, dur=9): return back(prog(f, f0, f0 + dur))
def title(c, s, f, f0, y=700, size=118, col=GOLD, hold=None):
    if f < f0: return
    a = 1.0 if hold is None else clamp(1 - (f - f0 - hold) / 12)
    if a > 0: c.text(s, W / 2, y, size, col, INK, 9, scale=max(0.01, pop(f, f0)), alpha=a)

def sub(c, f):
    s, t = T.sub(f)
    if s: c.subtitle(s, t)

def s_grief(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1060, 1130)); sky(c, "night"); stars(c, f, 60)
    mountain(c, W/2, 1500, 1000, 500, (40, 40, 80), True, 0.3)
    ground(c, GY, (50, 40, 70))
    draw_char(c, W/2, GY, 1.5, "parvati", act(f, "meditate", 1, expr="sad"))
    title(c, "GRIEF", f, T.start("The ashes of grief"), 560, 120, (180, 180, 220), hold=30)

def s_himalayas(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), y=(1100, 1130)); sky(c, "dawn"); sun(c, 800, 500, 100, f, True, 0.2)
    mountain(c, 540, 1500, 1100, 560, (70, 90, 140), True, 0.4)
    ground(c, GY, (90, 100, 130))
    draw_char(c, W/2, GY, 1.5, "parvati", act(f, "meditate", 2, expr="stern"))
    title(c, "HIMALAYAS", f, T.start("is quietly burning"), 560, 120, GOLD, hold=40)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "day"); sun(c, 200, 400, 90, f, True, 0.25)
    hills(c, 1420, 120, (120, 100, 80), 3, 0.4); ground(c, GY, (140, 110, 80))
    tree(c, 300, GY, 1.2, 0.9); tree(c, 800, GY, 1.3, 0.9)
    draw_char(c, W/2, GY, 1.6, "parvati", act(f, "sit", 3, expr="stern"))
    title(c, "RENUNCIATION", f, T.start("Princess Parvati sheds"), 560, 110, (220, 170, 120), hold=40)

def s_shiva(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(W/2, 540)); sky(c, "heaven"); stars(c, f, 40)
    mountain(c, 540, 1500, 1000, 500, (60, 80, 120), True, 0.35)
    tree(c, 540, GY, 1.4, 0.9)
    ground(c, GY, (100, 110, 140))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "meditate", 4, hold="trident", expr="closed"))
    title(c, "LORD SHIVA", f, T.start("Lord Shiva sits deep"), 560, 130, (150, 220, 255), hold=50)

def s_winter(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "storm"); rain(c, f, 60)
    hills(c, 1420, 120, (100, 120, 150), 5, 0.4); ground(c, GY, (120, 140, 170))
    draw_char(c, W/2, GY, 1.6, "parvati", act(f, "stand", 5, expr="stern"))
    title(c, "ONE FOOT", f, T.start("one foot amidst freezing"), 560, 120, (200, 230, 255), hold=40)

def s_summer(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "fire"); sun(c, W/2, 450, 160, f, True, 0.3)
    ground(c, GY, (180, 110, 70))
    for x in (250, 830): fire(c, x, GY, 1.0, f)
    draw_char(c, W/2, GY, 1.6, "parvati", act(f, "sit", 6, expr="stern"))
    title(c, "FOUR FIRES", f, T.start("Parvati sits calmly"), 560, 120, (255, 180, 100), hold=40)

def s_shaking(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.3), y=(1100, 1070), kicks=[(10, 12)]); sky(c, "storm"); stars(c, f, 50)
    mountain(c, 540, 1500, 1100, 540, (80, 50, 100), True, 0.35)
    ground(c, GY, (100, 70, 90))
    draw_char(c, 540, GY, 1.6, "parvati", act(f, "raise", 7, expr="stern"))
    sparks(c, 540, 1150, f, T.start("Her unrelenting penance"), 20, 4, (255, 220, 120), 250)
    title(c, "THE HEAVENS", f, T.start("Her unrelenting penance"), 560, 120, GOLD, hold=40)

def s_devotion(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(540, 600)); sky(c, "dawn"); sun(c, 850, 500, 110, f, True, 0.25)
    hills(c, 1420, 120, (140, 100, 90), 4, 0.4); ground(c, GY, (150, 120, 90))
    draw_char(c, 300, GY, 1.3, "sage", act(f, "namaste", 8, expr="smile"))
    draw_char(c, 760, GY, 1.5, "parvati", act(f, "stand", 9, expr="smile"), flip=True)
    title(c, "DEVOTION", f, T.start("Even the ancient mountains"), 560, 120, (255, 200, 150), hold=50)

def s_discipline(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "dusk"); sun(c, 200, 500, 100, f, True, 0.2)
    hills(c, 1420, 120, (110, 80, 110), 6, 0.4); ground(c, GY, (130, 90, 100))
    draw_char(c, W/2, GY, 1.6, "parvati", act(f, "meditate", 10, expr="smile"))
    title(c, "UNYIELDING", f, T.start("year after year"), 560, 120, GOLD, hold=40)

def s_awakening(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.4), y=(1110, 1070), kicks=[(20, 15)]); sky(c, "heaven"); sun(c, 540, 400, 180, f, True, 0.3)
    mountain(c, 540, 1500, 1100, 540, (70, 110, 150), True, 0.35)
    ground(c, GY, (120, 150, 180))
    draw_char(c, 540, GY, 1.7, "shiva", act(f, "bless", 11, hold="trident", expr="smile"))
    rays_burst(c, 540, 1150, f, 90, None, 20, (255, 240, 180, 60), 0.9, 0.6)
    ring_wave(c, 540, 1150, f, T.start("Shiva finally opens"), 700)
    title(c, "AWAKENING", f, T.start("Shiva finally opens"), 560, 140, GOLD, hold=None)

FN = dict(grief=s_grief, himalayas=s_himalayas, penance=s_penance, shiva=s_shiva, winter=s_winter, summer=s_summer, shaking=s_shaking, devotion=s_devotion, discipline=s_discipline, awakening=s_awakening)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("The ashes of grief still linger"), "chime", 0.8),
         (T.start("is quietly burning deep within"), "whoosh", 0.7), (T.start("Princess Parvati sheds her heavy silks"), "bell", 0.8),
         (T.start("Lord Shiva sits deep in eternal meditation"), "swell", 0.9), (T.start("Undeterred, Parvati stands unwavering"), "whoosh", 0.7),
         (T.start("Then summer arrives with scorching"), "thunk", 0.8), (T.start("Her unrelenting penance shakes the heavens"), "dhol", 0.9),
         (T.start("Even the ancient mountains seem"), "sparkle", 0.8), (T.start("Day after day, month after month"), "bell", 0.7),
         (T.start("Shiva finally opens his third eye at last"), "riser", 0.9), (T.start("Shiva finally opens his third eye at last") + 15, "chime", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
