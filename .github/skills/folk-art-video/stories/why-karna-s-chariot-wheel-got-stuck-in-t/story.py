"""story.py - "Why Karna's Chariot Wheel Got Stuck in the Mud" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Imagine the greatest warrior"),
    ("aim", "Karna raises his mighty bow"),
    ("sink", "Suddenly, the earth groans"),
    ("lift", "Desperate, he steps down"),
    ("krishna", "Arjuna hesitates, but Lord Krishna"),
    ("curse", "Remember the innocent cow"),
    ("drop", "Now, in the exact moment"),
    ("arrow", "An arrow flies through"),
    ("fall", "The unconquerable hero falls"),
    ("title", "Not by superior skill"),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"sink", "arrow", "fall"}

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
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "storm"); stars(c, f, 50, ymax=600)
    hills(c, 1440, 120, (60, 40, 60), 3, 0.5); ground(c, GY, (80, 50, 50))
    draw_char(c, W / 2, GY, 1.5, "karna", act(f, "stand", 1, hold="bow", expr="stern"))
    title(c, "KARNA", f, _starts[0] + 5, 560, 140, GOLD, hold=30)

def s_aim(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1100, 1100)); sky(c, "dusk"); sun(c, 850, 500, 120, f, True, 0.25)
    hills(c, 1430, 110, (90, 50, 70), 5, 0.5); ground(c, GY, (120, 70, 60))
    draw_char(c, 400, GY, 1.4, "karna", act(f, "aim", 1, holdL="bow", expr="stern"))
    draw_char(c, 820, GY, 1.3, "arjuna", act(f, "aim", 2, holdL="bow", expr="stern"), flip=True)
    title(c, "THE DUEL", f, _starts[1] + 5, 540, 120, (255, 200, 120), hold=40)

def s_sink(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), y=(1130, 1110), kicks=[(0, 12)]); sky(c, "storm"); rain(c, f, 60)
    hills(c, 1420, 120, (50, 40, 60), 4, 0.45); ground(c, GY, (70, 50, 50))
    chariot(c, 540, GY + 40, 1.0, f, 1.0)
    draw_char(c, 360, GY, 1.4, "karna", act(f, "stand", 1, hold="bow", expr="sad"))
    title(c, "SINKING", f, _starts[2] + 4, 540, 130, (255, 110, 110), hold=50)

def s_lift(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "storm")
    hills(c, 1420, 120, (50, 40, 60), 4, 0.45); ground(c, GY, (70, 50, 50))
    chariot(c, 640, GY + 50, 1.0, f, 1.0)
    draw_char(c, 400, GY, 1.4, "karna", act(f, "strike", 1, expr="stern"))
    title(c, "DESPERATE", f, _starts[3] + 4, 540, 120, GOLD, hold=40)

def s_krishna(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1110)); sky(c, "day"); sun(c, 200, 450, 100, f, True, 0.25)
    hills(c, 1440, 100, (80, 130, 100), 6, 0.5); ground(c, GY, (140, 100, 70))
    chariot(c, 760, GY, 1.0, f, 1.0)
    draw_char(c, 700, GY, 1.3, "krishna", act(f, "point", 1, hold="flute", expr="smile"))
    draw_char(c, 880, GY, 1.3, "arjuna", act(f, "stand", 2, hold="bow", expr="neutral"), flip=True)
    title(c, "KRISHNA'S WORD", f, _starts[4] + 5, 540, 110, (255, 230, 150), hold=50)

def s_curse(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1100)); sky(c, "dusk")
    hills(c, 1430, 110, (90, 60, 80), 5, 0.5); ground(c, GY, (110, 80, 70))
    draw_animal(c, "cow", 350, GY, 0.9, f)
    draw_char(c, 700, GY, 1.3, "sage", act(f, "point", 1, hold="staff", expr="stern"), flip=True)
    title(c, "THE CURSE", f, _starts[5] + 5, 540, 120, (255, 140, 140), hold=60)

def s_drop(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "storm")
    hills(c, 1420, 120, (50, 40, 60), 4, 0.45); ground(c, GY, (70, 50, 50))
    draw_char(c, 540, GY, 1.4, "karna", act(f, "kneel", 1, expr="sad"))
    title(c, "KARMA", f, _starts[6] + 4, 540, 130, GOLD, hold=40)

def s_arrow(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.35), y=(1110, 1090), kicks=[(10, 15)]); sky(c, "storm"); rain(c, f, 80)
    hills(c, 1420, 120, (50, 40, 60), 4, 0.45); ground(c, GY, (70, 50, 50))
    draw_char(c, 850, GY, 1.3, "arjuna", act(f, "aim", 1, holdL="bow", expr="stern"), flip=True)
    arrow(c, 500, 1150, -0.2, 350, 1.3, 1.0, (255, 230, 150))
    title(c, "THE ARROW", f, _starts[7] + 3, 520, 120, (255, 100, 100), hold=30)

def s_fall(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "dusk")
    hills(c, 1430, 110, (80, 50, 60), 5, 0.5); ground(c, GY, (100, 60, 60))
    draw_char(c, 540, GY, 1.4, "karna", act(f, "bow", 1, expr="sad"))
    title(c, "FALLEN", f, _starts[8] + 4, 540, 130, (220, 180, 180), hold=40)

def s_title(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05), y=(1100, 1130)); sky(c, "dusk"); sun(c, W / 2, 750, 180, f, True, 0.2)
    hills(c, 1450, 130, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    mandala(c, W / 2, 1150, 400, f, GOLD, 16, 0.9, 0.3)
    draw_char(c, W / 2, GY, 1.5, "karna", act(f, "stand", 1, hold="bow", expr="stern"))
    k = pop(f, _starts[9], 14)
    c.text("PAST MISTAKES", W / 2, 540, 130, GOLD, INK, 10, scale=max(0.01, k))
    if f >= T.end("but by the unyielding weight of past mistakes.") - 20:
        follow_button(c, W / 2, 1750, prog(f, T.end("but by the unyielding weight of past mistakes.") - 20, T.total - 10))

FN = dict(intro=s_intro, aim=s_aim, sink=s_sink, lift=s_lift, krishna=s_krishna, curse=s_curse, drop=s_drop, arrow=s_arrow, fall=s_fall, title=s_title)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.8 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Imagine the greatest warrior"), "chime", 0.7),
         (T.start("Karna raises his mighty bow"), "dhol", 0.8), (T.start("Suddenly, the earth groans"), "rumble", 0.9),
         (T.start("Desperate, he steps down"), "thunk", 0.8), (T.start("Arjuna hesitates, but Lord Krishna"), "bell", 0.8),
         (T.start("Remember the innocent cow"), "heart", 0.8), (T.start("Now, in the exact moment"), "whoosh", 0.7),
         (T.start("An arrow flies through"), "slice", 1.0), (T.start("The unconquerable hero falls"), "thunk", 1.0),
         (T.start("Not by superior skill"), "chime", 0.9), (T.start("Not by superior skill") + 20, "swell", 0.8)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
