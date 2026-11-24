"""story.py - "The Birth of Parvati: The Return of Sati" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("grief", "The ashes of Sati grow cold"),
    ("shiva", "Lord Shiva sits in deep"),
    ("balance", "The gods tremble"),
    ("himavan", "High in the Himalayas"),
    ("prayer", "They yearn for a child"),
    ("birth", "From the ethereal realms"),
    ("parvati", "They name her Parvati"),
    ("childhood", "Even as a child"),
    ("animals", "Animals of"),
    ("maiden", "As the seasons turn"),
    ("memory", "Deep inside her soul"),
    ("cave", "One day"),
    ("approach", "Parvati steps forward"),
    ("awakening", "The air grows still"),
    ("title", "Love is not merely born"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"birth", "memory", "approach", "title"}

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

def s_grief(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "storm"); stars(c, f, 60); rain(c, f, 50)
    mountain(c, 300, 1500, 900, 520, (40, 40, 70), True, 0.35); ground(c, GY, (50, 50, 70))
    t1 = T.start("and the universe plunges")
    draw_char(c, W / 2, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="sad"))
    if f >= t1: title(c, "WINTER OF GRIEF", f, t1, 560, 100, (180, 200, 250))

def s_shiva(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "night"); stars(c, f, 80); moon(c, 820, 480, 80)
    mountain(c, 540, 1520, 1000, 500, (44, 50, 90), True, 0.4); ground(c, GY, (60, 65, 90))
    draw_char(c, W / 2, GY, 1.6, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    title(c, "KAILASH", f, T.start("unmoving meditation upon Mount Kailash"), 560, 130, GOLD, hold=50)

def s_balance(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, W / 2 + 50)); sky(c, "storm"); rain(c, f, 70)
    mountain(c, 540, 1520, 1000, 500, (50, 40, 60), True, 0.4); ground(c, GY, (70, 50, 60))
    draw_char(c, 400, GY, 1.3, "god", act(f, "shout", 1, expr="shock"), flip=True)
    draw_char(c, 680, GY, 1.3, "goddess", act(f, "plead", 2, expr="sad"))
    title(c, "SHAKTI LOST", f, T.start("for without the divine balance"), 560, 110, (255, 120, 120), hold=40)

def s_himavan(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "dawn"); sun(c, 820, 560, 110, f, True, 0.25)
    mountain(c, 540, 1480, 900, 440, (120, 90, 110), True, 0.35); ground(c, GY, (140, 100, 90))
    draw_char(c, 360, GY, 1.4, "king", act(f, "namaste", 1, expr="smile"))
    draw_char(c, 720, GY, 1.35, "queen", act(f, "namaste", 2, expr="smile"), flip=True)
    title(c, "HIMALAYAS", f, T.start("High in the Himalayas"), 560, 130, GOLD, hold=50)

def s_prayer(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100)); sky(c, "heaven"); sun(c, W / 2, 600, 140, f, True, 0.2)
    mountain(c, 540, 1500, 950, 460, (130, 100, 120), True, 0.4); ground(c, GY, (150, 110, 100))
    draw_char(c, 420, GY, 1.4, "king", act(f, "give", 1, expr="smile"))
    draw_char(c, 660, GY, 1.35, "queen", act(f, "give", 2, expr="smile"), flip=True)
    rays_burst(c, 540, 1150, f, 80, None, 18, (255, 240, 180, 50), 0.9, 0.6)
    title(c, "DIVINE BLESSING", f, T.start("They yearn for a child"), 560, 110, (255, 230, 150), hold=40)

def s_birth(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.05), y=(1100, 1130)); sky(c, "heaven"); stars(c, f, 50)
    mountain(c, 540, 1500, 950, 460, (110, 90, 140), True, 0.4); ground(c, GY, (120, 100, 130))
    draw_char(c, 540, GY, 1.4, "queen", act(f, "cradle", 1, expr="smile", hold="newborn"))
    c.glow(540, 1250, 180, (255, 230, 150), 0.7, 1.0)
    sparks(c, 540, 1250, f, _starts[5], 20, 5, (255, 230, 150), 200)
    title(c, "REBIRTH", f, T.start("the essence of Goddess Sati stirs once more"), 560, 130, GOLD, hold=50)

def s_parvati(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    mountain(c, 540, 1480, 900, 440, (100, 140, 120), True, 0.35); ground(c, GY, (140, 120, 90))
    draw_char(c, 360, GY, 1.4, "king", act(f, "bless", 1, expr="smile"))
    draw_char(c, 720, GY, 1.35, "queen", act(f, "give", 2, expr="smile", hold="newborn"), flip=True)
    title(c, "PARVATI", f, T.start("They name her Parvati"), 560, 140, (255, 200, 220), hold=60)

def s_childhood(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), x=(W / 2, 580)); sky(c, "day"); sun(c, 800, 480, 90, f, True, 0.25)
    tree(c, 200, GY, 1.2, 1.0); tree(c, 880, GY, 1.1, 1.0); ground(c, GY, (120, 150, 100))
    draw_char(c, 540, GY, 1.1, "girl", act(f, "walk", 1, expr="smile", hold="lotus"))
    title(c, "DAUGHTER OF THE MOUNTAINS", f, T.start("Even as a child, Parvati is unlike any other"), 560, 100, GOLD, hold=40)

def s_animals(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.0)); sky(c, "day"); sun(c, 200, 500, 90, f, True, 0.25)
    tree(c, 800, GY, 1.3, 1.0); ground(c, GY, (110, 140, 90))
    draw_char(c, 440, GY, 1.1, "girl", act(f, "stand", 1, expr="smile", hold="lotus"))
    draw_animal(c, "deer", 240, GY, 0.6, f)
    draw_animal(c, "lion", 780, GY, 0.7, f, True)
    title(c, "WILD HARMONY", f, T.start("Animals of"), 560, 120, (255, 230, 150), hold=40)

def s_maiden(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "dusk"); sun(c, 860, 520, 100, f, True, 0.2)
    mountain(c, 540, 1500, 900, 440, (90, 110, 140), True, 0.4); ground(c, GY, (100, 120, 130))
    draw_char(c, 540, GY, 1.35, "woman", act(f, "stand", 1, expr="smile", hold="lotus"))
    title(c, "GRACE", f, T.start("little Parvati grows into a graceful maiden"), 560, 130, GOLD, hold=50)

def s_memory(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1080)); sky(c, "heaven"); stars(c, f, 60)
    mountain(c, 540, 1500, 950, 460, (70, 70, 110), True, 0.4); ground(c, GY, (90, 90, 120))
    draw_char(c, 540, GY, 1.35, "woman", act(f, "meditate", 1, expr="closed"))
    rays_burst(c, 540, 1150, f, 90, None, 16, (200, 220, 255, 50), 0.9, 0.5)
    title(c, "ANCIENT MEMORY", f, T.start("Deep inside her soul, an ancient memory awakens"), 560, 110, (180, 220, 255), hold=50)

def s_cave(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "dusk"); sun(c, 200, 500, 90, f, True, 0.25)
    cave(c, 760, GY, 1.1, 1.0); ground(c, GY, (100, 110, 120))
    draw_char(c, 340, GY, 1.3, "king", act(f, "point", 1, expr="neutral"))
    draw_char(c, 540, GY, 1.3, "woman", act(f, "walk", 2, expr="neutral", hold="lotus"))
    title(c, "THE HIDDEN CAVE", f, T.start("her father leads her to"), 560, 120, GOLD, hold=40)

def s_approach(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), x=(W / 2, 600)); sky(c, "night"); stars(c, f, 50); moon(c, 200, 420, 70)
    cave(c, 780, GY, 1.1, 1.0); ground(c, GY, (70, 80, 100))
    draw_char(c, 680, GY, 1.3, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    draw_char(c, 420, GY, 1.3, "woman", act(f, "give", 2, expr="smile", hold="lotus"))
    title(c, "THE MEETING", f, T.start("Parvati steps forward"), 560, 130, (255, 230, 150), hold=50)

def s_awakening(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.35), y=(1100, 1050), kicks=[(T.start("The air grows still") - _starts[13], 10)])
    sky(c, "dawn"); sun(c, 540, 560, 140, f, True, 0.25)
    mountain(c, 540, 1500, 950, 460, (140, 100, 120), True, 0.4); ground(c, GY, (150, 110, 100))
    draw_char(c, 380, GY, 1.3, "woman", act(f, "give", 1, expr="smile", hold="lotus"))
    draw_char(c, 700, GY, 1.35, "shiva", act(f, "stand", 2, hold="trident", expr="smile"), flip=True)
    rays_burst(c, 540, 1150, f, 100, None, 20, (255, 240, 180, 70), 0.9, 0.6)
    ring_wave(c, 540, 1150, f, T.start("The air grows still"), 600)
    title(c, "AWAKENING", f, T.start("The air grows still"), 560, 120, GOLD, hold=50)

def s_title(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1130)); sky(c, "heaven"); sun(c, W / 2, 780, 220, f, True, 0.2); stars(c, f, 40)
    mountain(c, 540, 1520, 1000, 500, (120, 90, 130), True, 0.4); ground(c, GY, (140, 110, 110))
    mandala(c, W / 2, 1180, 450, f, GOLD, 16, 0.9, 0.3)
    draw_char(c, 420, GY, 1.4, "shiva", act(f, "bless", 1, hold="trident", expr="smile"))
    draw_char(c, 660, GY, 1.35, "woman", act(f, "namaste", 2, expr="smile"), flip=True)
    k = pop(f, _starts[14], 14)
    c.text("PARVATI & SHIVA", W / 2, 480, 150, GOLD, INK, 10, scale=max(0.01, k))
    if f >= T.end("it is") + 20: follow_button(c, W / 2, 1750, prog(f, T.end("it is") + 20, T.total - 10))

FN = dict(grief=s_grief, shiva=s_shiva, balance=s_balance, himavan=s_himavan, prayer=s_prayer,
          birth=s_birth, parvati=s_parvati, childhood=s_childhood, animals=s_animals, maiden=s_maiden,
          memory=s_memory, cave=s_cave, approach=s_approach, awakening=s_awakening, title=s_title)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("The ashes of Sati grow cold"), "rumble", 0.9),
         (T.start("Lord Shiva sits in deep"), "bell", 0.7), (T.start("The gods tremble"), "whoosh", 0.7),
         (T.start("High in the Himalayas"), "chime", 0.8), (T.start("They yearn for a child"), "sparkle", 0.9),
         (T.start("From the ethereal realms"), "riser", 0.7), (T.start("They name her Parvati"), "chime", 1.0),
         (T.start("Even as a child, Parvati is unlike any other"), "pop", 0.7), (T.start("Animals of"), "dhol", 0.8),
         (T.start("As the seasons turn"), "swell", 0.7), (T.start("Deep inside her soul, an ancient memory awakens"), "heart", 0.9),
         (T.start("One day"), "whoosh", 0.7), (T.start("Parvati steps forward"), "chime", 0.9),
         (T.start("The air grows still"), "thunk", 1.0), (T.start("Love is not merely born of the flesh;"), "swell", 0.8)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("Deep inside her soul, an ancient memory awakens"), back=T.start("One day"), sa=146.83, mood="calm", tempo=72)
