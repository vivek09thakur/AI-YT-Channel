"""story.py - "Why Jatayu lost his wings fighting Ravana" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Can a giant bird defeat"),
    ("skies", "High in the burning sky,"),
    ("oath", "This noble vulture remembers"),
    ("attack", "With a mighty roar, Jatayu attacks."),
    ("chariot", "His razor-sharp talons shatter Ravana's golden chariot."),
    ("duel", "Enraged, Ravana draws his celestial sword."),
    ("fall", "With one merciless strike,"),
    ("earth", "He plummets from the heavens,"),
    ("truth", "Yet, as Sita weeps for her fallen protector,"),
    ("legacy", "Even in certain defeat,"),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"attack", "duel", "fall"}

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
    cam(c, lf, n, (1.0, 1.1), y=(1100, 1150)); sky(c, "sunset"); sun(c, 820, 480, 110, f, True, 0.25)
    hills(c, 1420, 120, (190, 90, 120), 5, 0.4); ground(c, GY, (170, 110, 80))
    draw_animal(c, "eagle", 320, 1100, 1.2, f)
    draw_char(c, 760, GY, 1.3, "ravana", act(f, "stand", 1, hold="sword", expr="stern"), flip=True)
    title(c, "JATAYU", f, T.start("Can a giant bird defeat"), 560, 130)

def s_skies(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), x=(W / 2, 600)); sky(c, "fire"); sun(c, 200, 420, 120, f, True, 0.2)
    chariot(c, 650, 950, 1.0, f, True, 0.5)
    draw_animal(c, "eagle", 320, 950, 1.3, f)
    draw_char(c, 680, 930, 1.0, "sita", act(f, "cry", 3, expr="sad"), flip=True)
    title(c, "THE CHASE", f, T.start("brave Jatayu spots Ravana"), 560, 110)

def s_oath(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.0), y=(1130, 1130)); sky(c, "dusk"); stars(c, f, 40)
    hills(c, 1430, 120, (80, 60, 100), 4, 0.5); ground(c, GY, (130, 70, 70))
    draw_animal(c, "eagle", W / 2, GY - 100, 1.5, f)
    title(c, "A PROMISE", f, T.start("He vows to protect the house"), 560, 110)

def s_attack(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), kicks=[(0, 12)]); sky(c, "storm"); rain(c, f, 50)
    chariot(c, 700, 1050, 1.1, f, True, 0.5)
    draw_animal(c, "eagle", 420, 980, 1.6, f)
    sparks(c, 560, 1000, f, T.start("With a mighty roar"), 20, 3, (255, 220, 120), 220)
    title(c, "ATTACK", f, T.start("With a mighty roar, Jatayu attacks."), 560, 130)

def s_chariot(c, f, lf, n):
    cam(c, lf, n, (1.15, 1.25), kicks=[(0, 15)]); sky(c, "storm")
    ground(c, GY, (80, 50, 50))
    draw_animal(c, "eagle", 360, 1050, 1.4, f)
    draw_char(c, 780, GY, 1.3, "ravana", act(f, "shout", 2, expr="stern"), flip=True)
    sparks(c, 600, 1200, f, 0, 30, 5, (255, 200, 100), 300)
    title(c, "SHATTERED", f, T.start("His razor-sharp talons"), 560, 110)

def s_duel(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.3), y=(1100, 1080)); sky(c, "fire"); ground(c, GY, (80, 40, 50))
    draw_char(c, 740, GY, 1.5, "ravana", act(f, "strike", 1, hold="sword", expr="stern"), flip=True)
    draw_animal(c, "eagle", 340, 1100, 1.3, f)
    title(c, "FURY", f, T.start("Enraged, Ravana draws"), 560, 120)

def s_fall(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), kicks=[(0, 20)]); sky(c, "storm"); lightning(c, 540, 50, 1100, f, 0, 4)
    draw_char(c, 740, GY, 1.5, "ravana", act(f, "raise", 1, hold="sword", expr="stern"), flip=True)
    draw_animal(c, "eagle", 420, 1150, 1.3, f)
    ring_wave(c, 420, 1150, f, 0, 500, (255, 100, 100))
    title(c, "THE STRIKE", f, T.start("With one merciless strike,"), 560, 130)

def s_earth(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.0)); sky(c, "dusk"); ground(c, GY, (90, 50, 50))
    draw_animal(c, "eagle", W / 2, GY, 1.4, f)
    title(c, "FALLEN", f, T.start("He plummets from the heavens,"), 560, 110)

def s_truth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1)); sky(c, "dawn"); ground(c, GY, (120, 70, 70))
    draw_char(c, 300, GY, 1.3, "sita", act(f, "cry", 1, expr="sad"))
    draw_animal(c, "eagle", 700, GY, 1.2, f)
    title(c, "THE TRUTH", f, T.start("to tell Rama the truth."), 560, 110)

def s_legacy(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05)); sky(c, "heaven"); sun(c, W / 2, 700, 180, f, True, 0.3)
    ground(c, GY, (130, 80, 80))
    draw_animal(c, "eagle", W / 2, GY, 1.5, f)
    title(c, "A HERO'S DUTY", f, T.start("a hero's duty is his ultimate weapon."), 560, 120, GOLD)

FN = dict(intro=s_intro, skies=s_skies, oath=s_oath, attack=s_attack, chariot=s_chariot, duel=s_duel, fall=s_fall, earth=s_earth, truth=s_truth, legacy=s_legacy)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    return [
        (0, "swell", 0.8), (T.start("brave Jatayu spots Ravana"), "whoosh", 0.7),
        (T.start("With a mighty roar, Jatayu attacks."), "dhol", 0.9),
        (T.start("His razor-sharp talons"), "thunk", 1.0),
        (T.start("Enraged, Ravana draws"), "riser", 0.8),
        (T.start("With one merciless strike,"), "slice", 1.0),
        (T.start("He plummets from the heavens,"), "rumble", 0.9),
        (T.start("to tell Rama the truth."), "heart", 0.8),
        (T.start("a hero's duty is his ultimate weapon."), "chime", 1.0)
    ]
CUES = sorted(_cues())
MUSIC = dict(style="bells", sa=146.83)
