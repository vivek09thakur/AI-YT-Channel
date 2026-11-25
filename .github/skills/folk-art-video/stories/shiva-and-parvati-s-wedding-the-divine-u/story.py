import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("himalayas", "The Himalayas glow under"),
    ("penance", "The great penance is finally over"),
    ("procession", "From every corner of the cosmos"),
    ("arrival", "Shiva arrives atop his faithful bull"),
    ("groom", "The unusual groom smiles gently"),
    ("menavati", "Queen Menavati gasps at"),
    ("transformation", "Sensing her mother's sudden dread"),
    ("beauty", "He transforms into Sundareswarar"),
    ("blessing", "Overwhelmed with joy"),
    ("wedding", "In the presence of sacred fires"),
    ("harmony", "Mountains sing, rivers dance"),
    ("title", "True love conquers all differences"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"transformation", "wedding", "title"}

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

def s_himalayas(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130))
    sky(c, "night"); stars(c, f, 90); moon(c, 220, 480, 80)
    mountain(c, 300, 1500, 900, 520, (54, 44, 120), True, 0.35); mountain(c, 900, 1520, 800, 440, (64, 50, 130), True, 0.4); hills(c, 1480, 110, (74, 44, 130), 3, 0.5); ground(c, GY, (90, 52, 80))
    draw_char(c, W / 2, GY, 1.5, "parvati", act(f, "meditate", 1, expr="closed"))
    title(c, "HIMALAYAS", f, T.start("The Himalayas glow"), 560, 110)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1100))
    sky(c, "dawn"); sun(c, 820, 560, 110, f, True, 0.25)
    hills(c, 1420, 120, (190, 90, 120), 5, 0.4); ground(c, GY, (170, 110, 80))
    draw_char(c, W / 2, GY, 1.5, "parvati", act(f, "meditate", 1, expr="smile"))
    rays_burst(c, W / 2, 1150, f, 60, None, 14, (255, 240, 180, 50), 0.9, 0.6)

def s_procession(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(540, 600))
    sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    hills(c, 1440, 100, (80, 160, 120), 6, 0.5); ground(c, GY, (170, 120, 70))
    crowd(c, GY, f, 12, -200, 1200, 0.85, 4, ((150, 40, 60), (60, 60, 120), (170, 110, 40)))
    draw_char(c, 540, GY, 1.3, "sage", act(f, "walk", 1, expr="smile"))
    title(c, "THE PROCESSION", f, T.start("From every corner"), 560, 100)

def s_arrival(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(500, 580))
    sky(c, "day"); hills(c, 1420, 110, (80, 160, 120), 6, 0.5); ground(c, GY, (150, 110, 70))
    draw_animal(c, "bull", 400, GY, 0.9, f)
    draw_char(c, 400, GY, 1.4, "shiva", act(f, "sit", 1, hold="trident", expr="neutral"))
    title(c, "NANDI", f, T.start("Shiva arrives atop"), 560, 110)

def s_groom(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1100))
    sky(c, "day"); hills(c, 1420, 110, (80, 160, 120), 6, 0.5); ground(c, GY, (150, 110, 70))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "stand", 1, hold="trident", expr="smile"))

def s_menavati(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(540, 600))
    sky(c, "day"); palace(c, 540, 1340, 0.8, 0.5); ground(c, GY, (170, 120, 70))
    draw_char(c, 300, GY, 1.3, "queen", act(f, "shout", 1, expr="shock"), flip=True)
    draw_char(c, 780, GY, 1.4, "shiva", act(f, "stand", 2, hold="trident", expr="neutral"))
    title(c, "SHOCK", f, T.start("Queen Menavati gasps"), 560, 100)

def s_transformation(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(10, 10)])
    sky(c, "storm"); ground(c, GY, (60, 44, 60))
    draw_char(c, 540, GY, 1.5, "parvati", act(f, "meditate", 1, expr="closed"))
    sparks(c, 540, 1150, f, T.start("Sensing her mother"), 20, 3, (255, 200, 120), 260)

def s_beauty(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1080))
    sky(c, "heaven"); sun(c, 540, 500, 180, f, True, 0.3)
    hills(c, 1430, 120, (96, 50, 120), 4, 0.5); ground(c, GY, (130, 70, 70))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "bless", 1, expr="smile"))
    rays_burst(c, 540, 1150, f, 90, None, 18, (255, 240, 170, 60), 0.9, 0.6)
    title(c, "SUNDARESWARAR", f, T.start("He transforms into"), 560, 110, GOLD)

def s_blessing(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15))
    sky(c, "heaven"); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    draw_char(c, 300, GY, 1.3, "queen", act(f, "bow", 1, expr="smile"), flip=True)
    draw_char(c, 780, GY, 1.5, "shiva", act(f, "bless", 2, expr="smile"))
    title(c, "JOY", f, T.start("Overwhelmed with joy"), 560, 100)

def s_wedding(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(540, 540))
    sky(c, "dawn"); temple(c, 540, GY, 1.1, 0.8); ground(c, GY, (170, 120, 70))
    draw_char(c, 420, GY, 1.4, "shiva", act(f, "stand", 1, expr="smile"))
    draw_char(c, 660, GY, 1.4, "parvati", act(f, "stand", 2, expr="smile"), flip=True)
    fire(c, 540, GY, 0.8, f)
    title(c, "THE UNION", f, T.start("In the presence of sacred"), 560, 110, GOLD)

def s_harmony(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2))
    sky(c, "heaven"); sun(c, 540, 500, 200, f, True, 0.3)
    hills(c, 1420, 110, (80, 160, 120), 6, 0.5); ground(c, GY, (150, 110, 70))
    draw_char(c, 420, GY, 1.4, "shiva", act(f, "bless", 1, expr="smile"))
    draw_char(c, 660, GY, 1.4, "parvati", act(f, "bless", 2, expr="smile"), flip=True)
    mandala(c, 540, 1150, 450, f, GOLD, 18, 0.9, 0.3)
    title(c, "ETERNAL BALANCE", f, T.start("Mountains sing"), 560, 100, GOLD)

def s_title(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05))
    sky(c, "heaven"); sun(c, 540, 820, 240, f, True, 0.2); stars(c, f, 50, ymax=600)
    hills(c, 1450, 130, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    k = pop(f, _starts[11], 14)
    draw_char(c, 420, GY, 1.4, "shiva", act(f, "bless", 1, expr="smile"))
    draw_char(c, 660, GY, 1.4, "parvati", act(f, "bless", 2, expr="smile"), flip=True)
    c.text("DIVINE UNION", W / 2, 480, 180, GOLD, INK, 12, scale=max(0.01, k))
    if f >= T.end("binding the universe in sacred harmony") - 20: follow_button(c, W / 2, 1750, prog(f, T.end("binding the universe in sacred harmony") - 20, T.total - 10))

FN = dict(himalayas=s_himalayas, penance=s_penance, procession=s_procession, arrival=s_arrival, groom=s_groom, menavati=s_menavati, transformation=s_transformation, beauty=s_beauty, blessing=s_blessing, wedding=s_wedding, harmony=s_harmony, title=s_title)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("The Himalayas glow"), "chime", 0.7), (T.start("The great penance"), "sparkle", 0.7),
         (T.start("From every corner"), "dhol", 0.8), (T.start("Shiva arrives atop"), "thunk", 0.8),
         (T.start("Queen Menavati gasps"), "heart", 0.9), (T.start("Sensing her mother"), "rumble", 0.9),
         (T.start("He transforms into"), "riser", 0.9), (T.start("Overwhelmed with joy"), "bell", 0.9),
         (T.start("In the presence of sacred"), "chime", 0.8), (T.start("Mountains sing"), "swell", 0.8),
         (T.start("True love conquers"), "bell", 0.9)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
