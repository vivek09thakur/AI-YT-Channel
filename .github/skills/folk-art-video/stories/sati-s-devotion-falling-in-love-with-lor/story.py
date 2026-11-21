import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("palace", "A majestic royal palace"),
    ("sati_pray", "Princess Sati closes her eyes"),
    ("father", "Her proud father Daksha"),
    ("forest", "She walks deep into the silent"),
    ("penance", "Days turn into long, unforgiving seasons"),
    ("beasts", "Wild beasts gather quietly"),
    ("earth", "Finally, the solid earth trembles"),
    ("shiva_appears", "Lord Shiva suddenly appears"),
    ("union", "Their divine union will soon"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"forest", "earth", "shiva_appears", "union"}

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

def s_palace(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1100, 1130)); sky(c, "dawn"); sun(c, 200, 420, 100, f, True, 0.25)
    palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    draw_char(c, 540, GY, 1.4, "queen", act(f, "stand", 1, expr="smile"))
    draw_char(c, 330, GY, 1.4, "king", act(f, "stand", 2, expr="stern"))
    draw_char(c, 740, GY, 1.3, "princess", act(f, "meditate", 3, expr="closed"), flip=True)
    title(c, "DEVOTION", f, _starts[0] + 10, 560, 120, GOLD, hold=50)

def s_sati_pray(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "day"); sun(c, 800, 500, 120, f, True, 0.2)
    hills(c, 1420, 110, (190, 90, 120), 5, 0.4); ground(c, GY, (170, 110, 80))
    mandala(c, 540, 1150, 420, f, GOLD, 16, 0.9, 0.3)
    draw_char(c, 540, GY, 1.5, "princess", act(f, "meditate", 1, expr="closed"))
    draw_char(c, 540, GY - 180, 0.6, "shiva", act(f, "meditate", 2, expr="closed", hold="trident"), par=0.9)
    title(c, "SHIVA", f, T.start("the luminous image of"), 560, 140, GOLD, hold=40)

def s_father(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, 600)); sky(c, "day")
    palace(c, 540, 1340, 0.7, 0.5); ground(c, GY, (170, 120, 70))
    draw_char(c, 360, GY, 1.4, "king", act(f, "point", 1, hold="sword", expr="stern"))
    draw_char(c, 720, GY, 1.3, "warrior", act(f, "stand", 2, hold="sword", expr="stern"), flip=True)
    draw_char(c, 540, GY, 1.3, "princess", act(f, "stand", 3, expr="sad"))
    title(c, "CHOICE", f, T.start("Sati wants only"), 560, 120, (255, 180, 100), hold=40)

def s_forest(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), y=(1130, 1100)); sky(c, "dusk"); stars(c, f, 40)
    hills(c, 1430, 120, (60, 50, 90), 7, 0.45); ground(c, GY, (100, 70, 70))
    for x in (120, 380, 780, 960): tree(c, x, GY, 1.2, 1.0, (40, 120, 80))
    draw_char(c, 540, GY, 1.4, "princess", act(f, "walk", 1, expr="neutral"))
    title(c, "FOREST", f, _starts[3], 560, 120, (200, 220, 255), hold=40)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1100)); sky(c, "dawn")
    hills(c, 1420, 110, (120, 80, 100), 5, 0.4); ground(c, GY, (140, 90, 70))
    for x in (200, 880): tree(c, x, GY, 1.2, 1.0, (50, 90, 70))
    draw_char(c, 540, GY, 1.5, "princess", act(f, "meditate", 1, expr="closed"))
    title(c, "PENANCE", f, _starts[4], 560, 120, (255, 150, 50), hold=40)

def s_beasts(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1100)); sky(c, "night"); stars(c, f, 50)
    ground(c, GY, (80, 60, 60))
    draw_char(c, 540, GY, 1.5, "princess", act(f, "meditate", 1, expr="closed"))
    draw_animal(c, "tiger", 320, GY, 0.8, f, False)
    draw_animal(c, "snake", 780, GY, 0.9, f, True)
    title(c, "DEVOTION", f, _starts[5], 560, 120, GOLD, hold=40)

def s_earth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), y=(1130, 1100), kicks=[(10, 8)]); sky(c, "storm")
    hills(c, 1420, 110, (70, 50, 80), 5, 0.4); ground(c, GY, (90, 70, 70))
    draw_char(c, 540, GY, 1.5, "princess", act(f, "meditate", 1, expr="closed"))
    ring_wave(c, 540, 1560, f, _starts[6], 400, (255, 200, 150))
    title(c, "TREMORS", f, _starts[6], 560, 120, (255, 200, 100), hold=40)

def s_shiva_appears(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "heaven"); sun(c, 540, 500, 150, f, True, 0.3)
    hills(c, 1420, 110, (100, 120, 160), 5, 0.4); ground(c, GY, (120, 110, 100))
    draw_char(c, 360, GY, 1.4, "princess", act(f, "namaste", 1, expr="smile"))
    draw_char(c, 720, GY, 1.5, "shiva", act(f, "bless", 2, hold="trident", expr="smile"), flip=True)
    rays_burst(c, 720, 1150, f, 80, None, 18, (255, 240, 180, 50), 0.9, 0.6)
    title(c, "LORD SHIVA", f, _starts[7], 560, 140, GOLD, hold=50)

def s_union(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1100, 1130)); sky(c, "heaven"); stars(c, f, 70)
    hills(c, 1420, 110, (120, 100, 150), 5, 0.4); ground(c, GY, (140, 120, 120))
    mandala(c, 540, 1150, 480, f, GOLD, 18, 0.9, 0.3)
    draw_char(c, 420, GY, 1.4, "princess", act(f, "namaste", 1, expr="smile"))
    draw_char(c, 660, GY, 1.5, "shiva", act(f, "bless", 2, hold="trident", expr="smile"), flip=True)
    title(c, "DIVINE UNION", f, _starts[8], 560, 150, GOLD, hold=None)

FN = dict(
    palace=s_palace,
    sati_pray=s_sati_pray,
    father=s_father,
    forest=s_forest,
    penance=s_penance,
    beasts=s_beasts,
    earth=s_earth,
    shiva_appears=s_shiva_appears,
    union=s_union,
)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

CUES = [
    (0, "swell", 0.8),
    (T.start("Princess Sati closes her eyes"), "chime", 0.7),
    (T.start("Her proud father Daksha"), "thunk", 0.8),
    (T.start("She walks deep into the silent"), "whoosh", 0.7),
    (T.start("Days turn into long, unforgiving seasons"), "riser", 0.7),
    (T.start("Wild beasts gather quietly"), "bell", 0.8),
    (T.start("Finally, the solid earth trembles"), "rumble", 0.9),
    (T.start("Lord Shiva suddenly appears"), "sparkle", 1.0),
    (T.start("Their divine union will soon"), "swell", 0.9),
]
MUSIC = dict(style="bells")
