"""story.py - "Why Krishna Stole the Clothes of the Gopis" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Why does the supreme playful god steal"),
    ("vrindavan", "Deep in the forests of Vrindavan,"),
    ("yamuna", "They bathe in the Yamuna at dawn,"),
    ("tree", "Krishna watches them from"),
    ("lesson", "He decides to teach them a lesson about modesty,"),
    ("stealing", "Quietly, he gathers their sarees"),
    ("shivering", "leaving the maidens shivering in the cool morning waters."),
    ("reveal", "Panic turns to laughter"),
    ("purity", "True purity is not about what we wear,"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"vrindavan", "tree", "stealing", "reveal"}

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
def talk(f, a, b): return 0.5 * abs(math.sin(f * 0.6)) if a <= f < b else 0.0

def sub(c, f):
    s, t = T.sub(f)
    if s: c.subtitle(s, t)

def s_intro(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "heaven"); stars(c, f, 60)
    hills(c, 1480, 110, (50, 120, 80), 3, 0.5); ground(c, GY, (40, 90, 60))
    draw_char(c, W / 2, GY, 1.5, "krishna", act(f, "bless", 1, hold="flute", expr="smile"))
    title(c, "PLAYFUL GOD", f, T.start(0), 560, 110, GOLD, hold=50)

def s_vrindavan(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, 540)); sky(c, "dawn"); sun(c, 800, 500, 100, f, True, 0.25)
    hills(c, 1440, 120, (60, 140, 90), 5, 0.4); tree(c, 200, GY, 1.3, 0.9); tree(c, 880, GY, 1.1, 0.9); ground(c, GY, (80, 150, 90))
    draw_char(c, 400, GY, 1.3, "woman", act(f, "sit", 3, expr="smile"))
    draw_char(c, 680, GY, 1.3, "girl", act(f, "meditate", 3, expr="smile"), flip=True)
    title(c, "VRINDAVAN", f, T.start("Deep in the forests of Vrindavan,"), 560, 120, (255, 230, 150), hold=60)

def s_yamuna(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1130, 1110)); sky(c, "dawn"); river(c, 1400, 300, f)
    ground(c, GY + 100, (90, 160, 100))
    draw_char(c, 360, GY + 100, 1.3, "woman", act(f, "cradle", 4, expr="smile"))
    draw_char(c, 720, GY + 100, 1.2, "girl", act(f, "namaste", 5, expr="smile"), flip=True)
    title(c, "YAMUNA VOW", f, T.start("They bathe in the Yamuna at dawn,"), 560, 110, GOLD, hold=50)

def s_tree(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(540, 540), y=(1100, 1050))
    sky(c, "day"); sun(c, 200, 400, 90, f, True, 0.25)
    tree(c, 540, GY, 1.6, 1.0); ground(c, GY, (70, 140, 80))
    draw_char(c, 540, 950, 1.4, "krishna", act(f, "sit", 7, hold="flute", expr="smile"))
    title(c, "WATCHING", f, T.start("Krishna watches them from"), 560, 120, (255, 220, 150), hold=50)

def s_lesson(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1)); sky(c, "heaven"); mandala(c, W / 2, 1150, 380, f, GOLD, 16, 0.9, 0.3)
    ground(c, GY, (60, 120, 70))
    draw_char(c, W / 2, GY, 1.5, "krishna", act(f, "stand", 9, hold="flute", expr="stern"))
    title(c, "SURRENDER", f, T.start("He decides to teach them a lesson about modesty,"), 560, 110, GOLD, hold=60)

def s_stealing(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "dusk"); tree(c, 300, GY, 1.4, 1.0)
    ground(c, GY, (70, 130, 80))
    draw_char(c, 360, GY, 1.4, "krishna", act(f, "walk", 11, hold="bowl", expr="smile"))
    title(c, "THE SAREES", f, T.start("Quietly, he gathers their sarees"), 560, 110, (255, 200, 120), hold=50)

def s_shivering(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1)); sky(c, "dusk"); river(c, 1400, 300, f)
    ground(c, GY + 100, (80, 140, 90))
    draw_char(c, 440, GY + 100, 1.3, "woman", act(f, "cry", 13, expr="sad"))
    draw_char(c, 680, GY + 100, 1.25, "girl", act(f, "cry", 13, expr="shock"), flip=True)
    title(c, "SHIVERING", f, T.start("leaving the maidens shivering in the cool morning waters."), 560, 100, (200, 220, 250), hold=50)

def s_reveal(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(540, 540)); sky(c, "dawn"); sun(c, 800, 500, 120, f, True, 0.25)
    tree(c, 300, GY, 1.3, 1.0); ground(c, GY, (80, 150, 90))
    draw_char(c, 300, GY, 1.4, "krishna", act(f, "stand", 16, hold="flute", expr="smile"))
    draw_char(c, 720, GY, 1.3, "woman", act(f, "namaste", 16, expr="smile"), flip=True)
    title(c, "KNOWING SMILE", f, T.start("finding the mischievous cowherd waiting with a gentle,"), 560, 110, GOLD, hold=60)

def s_purity(c, f, lf, n):
    t_end = T.start("but standing completely naked of ego before the divine.")
    cam(c, lf, n, (1.0, 1.15), y=(1100, 1130)); sky(c, "heaven")
    mandala(c, W / 2, 1150, 420, f, GOLD, 18, 0.9, 0.3)
    ground(c, GY, (60, 120, 70))
    draw_char(c, W / 2, GY, 1.6, "krishna", act(f, "bless", 18, hold="flute", expr="smile"))
    title(c, "PURE EGOLESS", f, T.start("True purity is not about what we wear,"), 560, 100, GOLD, hold=None)
    if f >= t_end + 20:
        follow_button(c, W / 2, 1750, prog(f, t_end + 20, T.total - 10))

FN = dict(intro=s_intro, vrindavan=s_vrindavan, yamuna=s_yamuna, tree=s_tree, lesson=s_lesson, stealing=s_stealing, shivering=s_shivering, reveal=s_reveal, purity=s_purity)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8),
         (T.start("Why does the supreme playful god steal"), "chime", 0.8),
         (T.start("Deep in the forests of Vrindavan,"), "bell", 0.7),
         (T.start("They bathe in the Yamuna at dawn,"), "whoosh", 0.7),
         (T.start("Krishna watches them from"), "pop", 0.8),
         (T.start("He decides to teach them a lesson about modesty,"), "riser", 0.8),
         (T.start("Quietly, he gathers their sarees"), "thunk", 0.8),
         (T.start("leaving the maidens shivering in the cool morning waters."), "heart", 0.8),
         (T.start("Panic turns to laughter"), "dhol", 0.9),
         (T.start("finding the mischievous cowherd waiting with a gentle,"), "sparkle", 0.9),
         (T.start("True purity is not about what we wear,"), "swell", 0.9),
         (T.start("but standing completely naked of ego before the divine."), "bell", 1.0)]
    return sorted(C)

CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
