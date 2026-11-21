"""story.py - "The Birth of Sati" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Before Goddess Parvati was born"),
    ("daksha_wish", "Daksha Prajapati, the son of Brahma"),
    ("penance", "He performed intense penance"),
    ("appearance", "Pleased by his devotion"),
    ("request", "Daksha bowed and requested her"),
    ("warning", "The Goddess accepted his wish"),
    ("birth", "Soon, the Goddess was born into Daksha's family"),
    ("childhood", "From childhood"),
    ("conflict", "But her father, Daksha"),
    ("tragedy", "This was the beginning of Sati's story"),
    ("outro", "In the next episode"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"appearance", "birth", "conflict", "outro"}

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

def s_intro(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "night"); stars(c, f, 80); moon(c, 220, 480, 80)
    mountain(c, 300, 1500, 900, 520, (54, 44, 120), True, 0.35); ground(c, GY, (90, 52, 80))
    mandala(c, W / 2, 1150, 420, f, GOLD, 18, 0.9, 0.3)
    draw_char(c, W / 2, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    title(c, "SHIVA & SATI", f, T.start("Before Goddess Parvati was born"), 560, 110)

def s_daksha_wish(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), x=(W / 2, 600)); sky(c, "dawn"); sun(c, 820, 560, 110, f, True, 0.25)
    hills(c, 1420, 120, (190, 90, 120), 5, 0.4); palace(c, 700, GY, 0.9, 0.75); ground(c, GY, (170, 110, 80))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="smile"))
    title(c, "DAKSHA", f, T.start("Daksha Prajapati, the son of Brahma"), 560, 120)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "dusk"); sun(c, W / 2, 760, 170, f, True, 0.2)
    hills(c, 1440, 120, (96, 50, 120), 4, 0.5); ground(c, GY, (130, 70, 70))
    draw_char(c, W / 2, GY, 1.5, "king", act(f, "meditate", 1, expr="closed"))
    title(c, "PENANCE", f, T.start("He performed intense penance"), 560, 120)

def s_appearance(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1110)); sky(c, "heaven"); sun(c, W / 2, 600, 150, f, True, 0.2)
    ground(c, GY, (150, 110, 70))
    draw_char(c, 400, GY, 1.4, "king", act(f, "kneel", 1, expr="smile"))
    draw_char(c, 700, GY, 1.4, "durga", act(f, "bless", 2, expr="smile"), flip=True)
    title(c, "THE GODDESS", f, T.start("Pleased by his devotion"), 560, 120)

def s_request(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1110)); sky(c, "dawn"); ground(c, GY, (150, 110, 70))
    draw_char(c, 400, GY, 1.4, "king", act(f, "bow", 1, expr="smile"))
    draw_char(c, 700, GY, 1.4, "durga", act(f, "bless", 2, expr="smile"), flip=True)
    title(c, "A WISH", f, T.start("Daksha bowed and requested her"), 560, 120)

def s_warning(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1110)); sky(c, "storm"); ground(c, GY, (100, 70, 70))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="shock"))
    draw_char(c, 700, GY, 1.4, "durga", act(f, "raise", 2, expr="stern"), flip=True)
    title(c, "WARNING", f, T.start("The Goddess accepted his wish"), 560, 120)

def s_birth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1080, 1150)); sky(c, "day"); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    draw_char(c, 400, GY, 1.4, "king", act(f, "bless", 1, expr="smile"))
    draw_char(c, 700, GY, 1.3, "queen", act(f, "give", 2, expr="smile"), flip=True)
    title(c, "BIRTH OF SATI", f, T.start("Soon, the Goddess was born into Daksha's family"), 560, 120)

def s_childhood(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(500, 600)); sky(c, "day"); ground(c, GY, (150, 110, 70))
    draw_char(c, 540, GY, 1.4, "girl", act(f, "stand", 1, expr="smile"))
    title(c, "DEVOTION", f, T.start("From childhood"), 560, 120)

def s_conflict(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1130, 1100)); sky(c, "storm"); ground(c, GY, (60, 44, 60))
    draw_char(c, 400, GY, 1.4, "king", act(f, "shout", 1, expr="stern"))
    draw_char(c, 700, GY, 1.4, "shiva", act(f, "meditate", 2, expr="closed"), flip=True)
    title(c, "CONFLICT", f, T.start("But her father, Daksha"), 560, 120)

def s_tragedy(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1110)); sky(c, "dusk"); ground(c, GY, (80, 40, 50))
    draw_char(c, 540, GY, 1.5, "durga", act(f, "stand", 1, expr="sad"))
    title(c, "SATI'S STORY", f, T.start("This was the beginning of Sati's story"), 560, 120)

def s_outro(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1130)); sky(c, "dusk"); ground(c, GY, (110, 60, 70))
    draw_char(c, 540, GY, 1.5, "girl", act(f, "meditate", 1, expr="smile"))
    title(c, "NEXT EPISODE", f, T.start("In the next episode"), 560, 120)

FN = dict(intro=s_intro, daksha_wish=s_daksha_wish, penance=s_penance, appearance=s_appearance, request=s_request, warning=s_warning, birth=s_birth, childhood=s_childhood, conflict=s_conflict, tragedy=s_tragedy, outro=s_outro)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

CUES = [(0, "swell", 0.8), (T.start("Before Goddess Parvati was born"), "chime", 0.7), (T.start("Daksha Prajapati, the son of Brahma"), "bell", 0.8), (T.start("He performed intense penance"), "rumble", 0.8), (T.start("Pleased by his devotion"), "sparkle", 0.9), (T.start("Daksha bowed and requested her"), "pop", 0.7), (T.start("The Goddess accepted his wish"), "whoosh", 0.7), (T.start("Soon, the Goddess was born into Daksha's family"), "bell", 0.8), (T.start("From childhood"), "chime", 0.7), (T.start("But her father, Daksha"), "thunk", 0.9), (T.start("This was the beginning of Sati's story"), "swell", 0.8), (T.start("In the next episode"), "pop", 0.8)]
MUSIC = dict(style="bells", sa=146.83)
