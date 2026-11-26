"""story.py - "Why Hanuman forgot his own divine powers" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "What happens when the strongest being"),
    ("child", "As a child, young Hanuman flies toward the sun,"),
    ("strike", "The gods panic, and Indra hurls his thunderbolt,"),
    ("vayu", "Vayu, the wind god, is heartbroken."),
    ("boons", "To restore balance,"),
    ("curse", "Yet, a group"),
    ("forget", "he will completely forget"),
    ("shore", "Years later, sitting quietly on a shore,"),
    ("awakening", "Sometimes, your greatest strength only awakens when"),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"strike", "vayu", "curse", "shore"}

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
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "night"); stars(c, f, 80); moon(c, 220, 480, 80)
    mountain(c, 300, 1500, 900, 520, (54, 44, 120), True, 0.35); ground(c, GY, (90, 52, 80))
    draw_char(c, W / 2, GY, 1.4, "hanuman", act(f, "stand", 1, expr="smile"))
    title(c, "STRENGTH", f, _starts[0] + 10, 560, 130)

def s_child(c, f, lf, n):
    t_m = T.start("mistaking it for a ripe golden fruit.")
    cam(c, lf, n, (1.1, 1.3), y=(1130, 900)); sky(c, "dawn"); sun(c, W / 2, 400, 140, f, True, 0.3)
    hills(c, 1440, 120, (190, 90, 120), 5, 0.4); ground(c, GY, (170, 110, 80))
    q = ease_io(prog(f, _starts[1], T.end("As a child, young Hanuman flies toward the sun,")))
    hx = lerp(540, 540, q); hy = lerp(GY, 600, q)
    draw_char(c, hx, hy, 1.3, "hanuman", act(f, "fly", 1, expr="smile"))
    rays_burst(c, W / 2, 400, f, 120, None, 18, (255, 220, 120, 50), 0.9, 0.5)
    if f >= t_m: title(c, "GOLDEN FRUIT", f, t_m, 560, 100, GOLD, hold=40)

def s_strike(c, f, lf, n):
    t_s = T.start("striking the little monkey down.")
    cam(c, lf, n, (1.2, 1.0), y=(800, GY), kicks=[(t_s - _starts[2], 14)]); sky(c, "storm")
    lightning(c, 540, 60, 980, f, _starts[2] + 5, 4); ground(c, GY, (60, 44, 60))
    draw_char(c, 800, GY, 1.3, "indra", act(f, "point", 1, expr="stern"), flip=True)
    q = prog(f, t_s, T.end("striking the little monkey down."))
    draw_char(c, lerp(600, 540, q), lerp(600, GY, q), 1.2, "hanuman", act(f, "cry", 2, expr="shock"))
    if f >= t_s: ring_wave(c, 540, GY, f, t_s, 400); sparks(c, 540, GY, f, t_s, 20, 3, (255, 100, 100), 200)

def s_vayu(c, f, lf, n):
    t_d = T.start("bringing creation to the brink of suffocation.")
    cam(c, lf, n, (1.0, 1.15), x=(W / 2, 600)); sky(c, "storm"); rain(c, f, 50)
    ground(c, GY, (50, 40, 60))
    draw_char(c, 330, GY, 1.5, "shiva", act(f, "stand", 1, hold="trident", expr="sad"))
    draw_char(c, 700, GY, 1.4, "sage", act(f, "shout", 2, expr="sad"), flip=True)
    if f >= t_d: title(c, "SUFFOCATION", f, t_d, 560, 110, (255, 120, 120), hold=40)

def s_boons(c, f, lf, n):
    t_b = T.start("Brahma and the gods shower Hanuman")
    cam(c, lf, n, (1.0, 1.2), y=(1130, 1100)); sky(c, "heaven"); sun(c, W / 2, 500, 120, f, True, 0.2)
    ground(c, GY, (140, 110, 80))
    draw_char(c, 540, GY, 1.5, "hanuman", act(f, "sit", 1, expr="smile"))
    draw_char(c, 260, GY, 1.3, "king", act(f, "bless", 2, expr="smile"))
    draw_char(c, 820, GY, 1.3, "sage", act(f, "bless", 3, expr="smile"), flip=True)
    if f >= t_b:
        rays_burst(c, 540, 1100, f, 80, None, 18, (255, 240, 170, 60), 0.9, 0.6)
        title(c, "BOONS", f, t_b, 560, 120, GOLD, hold=50)

def s_curse(c, f, lf, n):
    t_p = T.start("They place a gentle curse upon him...")
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, 540)); sky(c, "day"); sun(c, 800, 450, 90, f, True, 0.2)
    ground(c, GY, (150, 120, 80)); tree(c, 200, GY, 1.2, 1.0)
    draw_char(c, 400, GY, 1.3, "hanuman", act(f, "stand", 1, expr="smile"))
    draw_char(c, 700, GY, 1.3, "sage", act(f, "point", 2, expr="stern"), flip=True)
    if f >= t_p: title(c, "THE CURSE", f, t_p, 560, 120, (255, 180, 120), hold=50)

def s_forget(c, f, lf, n):
    t_u = T.start("his immense powers until someone reminds him")
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "dream"); stars(c, f, 40)
    ground(c, GY, (80, 70, 100))
    draw_char(c, 540, GY, 1.5, "hanuman", act(f, "meditate", 1, expr="closed"))
    if f >= t_u: title(c, "FORGOTTEN", f, t_u, 560, 110, (200, 200, 240), hold=50)

def s_shore(c, f, lf, n):
    t_n = T.start("he needs this exact memory")
    cam(c, lf, n, (1.0, 1.15)); sky(c, "dusk"); sun(c, 200, 500, 100, f, True, 0.2)
    ocean(c, 1500, f); ground(c, GY + 100, (170, 140, 90))
    draw_char(c, 420, GY + 100, 1.4, "hanuman", act(f, "sit", 1, expr="sad"))
    if f >= t_n:
        draw_char(c, 700, GY + 100, 1.3, "sage", act(f, "point", 2, expr="smile"), flip=True)
        title(c, "REMEMBER", f, t_n, 560, 110, GOLD, hold=50)

def s_awakening(c, f, lf, n):
    t_y = T.start("you finally remember who you truly are.")
    cam(c, lf, n, (1.0, 1.25), y=(1130, 1080)); sky(c, "heaven"); sun(c, W / 2, 600, 160, f, True, 0.25)
    ground(c, GY, (160, 120, 80)); mandala(c, W / 2, 1150, 400, f, GOLD, 16, 0.9, 0.3)
    draw_char(c, W / 2, GY, 1.6, "hanuman", act(f, "fly", 1, hold="mace", expr="smile"))
    rays_burst(c, W / 2, 1150, f, 90, None, 20, (255, 240, 170, 60), 0.9, 0.6)
    if f >= t_y: title(c, "TRUE SELF", f, t_y, 520, 130, GOLD)

FN = dict(intro=s_intro, child=s_child, strike=s_strike, vayu=s_vayu, boons=s_boons, curse=s_curse, forget=s_forget, shore=s_shore, awakening=s_awakening)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("As a child, young Hanuman flies toward the sun,"), "whoosh", 0.8),
         (T.start("The gods panic, and Indra hurls his thunderbolt,"), "thunk", 0.9), (T.start("striking the little monkey down."), "slice", 1.0),
         (T.start("Vayu, the wind god, is heartbroken."), "rumble", 0.9), (T.start("bringing creation to the brink of suffocation."), "riser", 0.8),
         (T.start("Brahma and the gods shower Hanuman"), "sparkle", 0.9), (T.start("They place a gentle curse upon him..."), "chime", 0.8),
         (T.start("he will completely forget"), "heart", 0.8), (T.start("Years later, sitting quietly on a shore,"), "whoosh", 0.7),
         (T.start("to leap across the ocean."), "dhol", 0.9), (T.start("Sometimes, your greatest strength only awakens when"), "riser", 0.8),
         (T.start("you finally remember who you truly are."), "chime", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
