import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("silence", "Silence falls over the entire cosmos"),
    ("arrival", "Lord Shiva arrives at"),
    ("body", "He finds her lifeless body resting gently"),
    ("freeze", "Time freezes across the three worlds."),
    ("rage", "Instead, an ocean"),
    ("tandava", "Shiva lifts Sati upon his mighty shoulder"),
    ("tremble", "The heavens tremble in mortal terror."),
    ("panic", "Fear grips every god in the pantheon as"),
    ("vishnu", "Lord Vishnu steps forward bravely to intervene,"),
    ("sanctuaries", "Sati's sacred body parts scatter across"),
    ("rebirth", "Even in his immense, blinding sorrow,"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"rage", "tandava", "panic", "vishnu"}

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

def s_silence(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1100, 1130)); sky(c, "fire"); stars(c, f, 60)
    mountain(c, 540, 1500, 900, 520, (54, 44, 120), True, 0.4); ground(c, GY, (60, 30, 40))
    fire(c, 540, GY, 1.2, f)
    draw_char(c, 540, GY, 1.5, "queen", act(f, "meditate", 1, expr="closed"))
    title(c, "TRAGEDY", f, T.start("Silence falls"), 560, 130, (255, 150, 100), hold=40)

def s_arrival(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15)); sky(c, "dusk"); sun(c, 820, 560, 100, f, True, 0.25)
    hills(c, 1420, 120, (120, 60, 80), 5, 0.4); ground(c, GY, (100, 50, 50))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "walk", 1, hold="trident", expr="sad"))
    draw_char(c, 200, GY, 1.2, "king", act(f, "kneel", 2, expr="shock"), flip=True)

def s_body(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.3), y=(1150, 1120)); sky(c, "night"); stars(c, f, 40)
    ground(c, GY, (80, 40, 50))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "cradle", 1, expr="sad", hold="newborn"))
    title(c, "SATI", f, T.start("He finds her lifeless"), 560, 140, (255, 180, 200), hold=50)

def s_freeze(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.1), y=(1130, 1130)); sky(c, "dream"); stars(c, f, 80)
    ground(c, GY, (50, 40, 70))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, expr="closed"))
    mandala(c, 540, 1150, 400, f, GOLD, 16, 0.9, 0.2)
    title(c, "TIME FREEZES", f, T.start("Time freezes"), 560, 120, GOLD, hold=50)

def s_rage(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(10, 12)]); sky(c, "storm"); rain(c, f, 80)
    ground(c, GY, (40, 30, 50))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "shout", 1, hold="trident", expr="stern"))
    ring_wave(c, 540, 1150, f, 10, 600, (255, 100, 100))
    title(c, "FURY", f, T.start("blinding, universe-shattering"), 560, 150, (255, 80, 80), hold=40)

def s_tandava(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), kicks=[(5, 15), (35, 15)]); sky(c, "storm"); lightning(c, 540, 50, 1100, f, 5, 3)
    ground(c, GY, (50, 30, 30))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "fight", 1, hold="trident", expr="stern"))
    sparks(c, 540, GY, f, 5, 20, 2, (255, 200, 120), 300)
    title(c, "TANDAVA", f, T.start("Shiva lifts Sati"), 560, 160, GOLD, hold=50)

def s_tremble(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), roll=2.0 * math.sin(lf * 0.1)); sky(c, "fire"); stars(c, f, 50)
    mountain(c, 540, 1500, 900, 520, (70, 40, 40), True, 0.4); ground(c, GY, (60, 30, 30))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "fight", 1, hold="trident", expr="stern"))

def s_panic(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), kicks=[(10, 10)]); sky(c, "storm"); rain(c, f, 60)
    ground(c, GY, (40, 30, 40))
    draw_char(c, 300, GY, 1.3, "indra", act(f, "kneel", 1, expr="shock"), flip=True)
    draw_char(c, 800, GY, 1.3, "devotee", act(f, "kneel", 2, expr="shock"), flip=True)
    title(c, "ANNIHILATION", f, T.start("the entire universe spirals"), 560, 120, (255, 100, 100), hold=40)

def s_vishnu(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "heaven"); sun(c, 540, 500, 120, f, True, 0.3)
    ground(c, GY, (60, 50, 80))
    draw_char(c, 350, GY, 1.4, "vishnu", act(f, "give", 1, hold="chakra", expr="stern"))
    draw_char(c, 750, GY, 1.4, "shiva", act(f, "stand", 2, hold="trident", expr="stern"), flip=True)
    title(c, "INTERVENTION", f, T.start("Lord Vishnu steps forward"), 560, 130, GOLD, hold=50)

def s_sanctuaries(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2)); sky(c, "dawn"); sun(c, 800, 450, 100, f, True, 0.2)
    hills(c, 1420, 120, (80, 120, 100), 5, 0.4); ground(c, GY, (70, 90, 70))
    draw_char(c, 540, GY, 1.4, "shiva", act(f, "bless", 1, hold="trident", expr="smile"))
    rays_burst(c, 540, 1150, f, 90, None, 16, (255, 230, 150, 50), 0.9, 0.5)

def s_rebirth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1130)); sky(c, "heaven"); sun(c, W / 2, 820, 200, f, True, 0.2)
    hills(c, 1450, 130, (70, 90, 110), 7, 0.5); ground(c, GY, (80, 100, 80))
    mandala(c, W / 2, 1180, 450, f, GOLD, 16, 0.9, 0.3)
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "bless", 1, hold="trident", expr="smile"))
    c.text("DIVINE REBIRTH", W / 2, 480, 150, GOLD, INK, 10, scale=max(0.01, pop(f, T.start("Even in his immense"), 14)))
    if f >= T.end("the sacred land") - 20: follow_button(c, W / 2, 1750, prog(f, T.end("the sacred land") - 20, T.total - 10))

FN = dict(silence=s_silence, arrival=s_arrival, body=s_body, freeze=s_freeze, rage=s_rage,
          tandava=s_tandava, tremble=s_tremble, panic=s_panic, vishnu=s_vishnu, sanctuaries=s_sanctuaries, rebirth=s_rebirth)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Silence falls"), "chime", 0.8),
         (T.start("Lord Shiva arrives"), "thunk", 0.9), (T.start("He finds her lifeless"), "heart", 0.9),
         (T.start("Time freezes"), "chime", 0.8), (T.start("Instead, an ocean"), "whoosh", 0.9),
         (T.start("blinding, universe-shattering"), "riser", 0.9), (T.start("Shiva lifts Sati"), "dhol", 1.0),
         (T.start("The heavens tremble"), "rumble", 0.9), (T.start("Fear grips every god"), "thunk", 0.9),
         (T.start("Lord Vishnu steps forward"), "chime", 0.9), (T.start("Sati's sacred body parts"), "sparkle", 0.8),
         (T.start("Even in his immense"), "swell", 0.9), (T.total - 30, "pop", 0.8)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("Instead, an ocean"), back=T.start("Lord Vishnu steps forward"), sa=146.83, mood="dark", tempo=72)
