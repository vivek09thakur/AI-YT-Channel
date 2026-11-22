"""story.py - Sati's Choice: Choosing Shiva Over Kings"""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("palace", "The palace of Daksha echoes"),
    ("suitors", "Kings and princes from every corner"),
    ("sati_walk", "Sati walks among them like a silent flame."),
    ("refusal", "Her father points to the mightiest king of all."),
    ("shock", "The court gasps in absolute shock."),
    ("defiance", "Sati lifts her chin with quiet defiance."),
    ("vision", "In her mind, the grand thrones dissolve into mist."),
    ("wisdom", "True royalty wears no gold,"),
    ("escape", "She leaves the assembly hall before"),
    ("kailash", "The path to the ascetic lord"),
    ("title", "But Sati has already made her eternal choice..."),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"shock", "vision", "escape", "kailash", "title"}

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

def s_palace(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1100, 1130)); sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    palace(c, 540, 1340, 0.9, 0.6, (180, 120, 60), (255, 200, 120)); ground(c, GY, (170, 120, 70))
    for x in (200, 880): pillar(c, x, GY, 900, 0.8)
    draw_char(c, 540, GY, 1.4, "king", act(f, "stand", 1, expr="stern"))
    title(c, "DAKSHA", f, _starts[0] + 6, 560, 110, GOLD, hold=50)

def s_suitors(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), x=(540, 600)); sky(c, "day"); ground(c, GY, (170, 120, 70))
    for x in (150, 400, 700, 950): pillar(c, x, GY, 900, 0.7)
    draw_char(c, 300, GY, 1.3, "warrior", act(f, "stand", 1, hold="sword", expr="smile"), flip=True)
    draw_char(c, 780, GY, 1.3, "warrior", act(f, "hips", 2, hold="talwar", expr="smile"))
    title(c, "SUITORS", f, _starts[1] + 10, 560, 110, (255, 200, 120), hold=40)

def s_sati_walk(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(400, 640)); sky(c, "day"); ground(c, GY, (170, 120, 70))
    for x in (150, 950): pillar(c, x, GY, 900, 0.7)
    q = prog(f, _starts[2], _starts[2] + max(1, n))
    draw_char(c, lerp(300, 700, q), GY, 1.4, "queen", act(f, "walk", 1, expr="neutral"))
    title(c, "SATI", f, _starts[2] + 4, 560, 130, GOLD, hold=50)

def s_refusal(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.15), x=(540, 500)); sky(c, "day"); ground(c, GY, (170, 120, 70))
    draw_char(c, 300, GY, 1.4, "king", act(f, "point", 1, expr="stern"))
    draw_char(c, 780, GY, 1.4, "queen", act(f, "stand", 2, expr="stern"), flip=True)

def s_shock(c, f, lf, n):
    cam(c, lf, n, (1.15, 1.25), kicks=[(0, 12)]); sky(c, "dusk"); ground(c, GY, (150, 100, 80))
    draw_char(c, 400, GY, 1.3, "king", act(f, "shout", 1, expr="shock"))
    draw_char(c, 700, GY, 1.3, "warrior", act(f, "kneel", 2, expr="shock"), flip=True)
    title(c, "SHOCK", f, _starts[4] + 4, 560, 140, (255, 120, 80), hold=30)

def s_defiance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(540, 540)); sky(c, "day"); ground(c, GY, (170, 120, 70))
    draw_char(c, 540, GY, 1.5, "queen", act(f, "raise", 1, expr="stern"))
    title(c, "DEFIANCE", f, _starts[5] + 4, 560, 110, GOLD, hold=40)

def s_vision(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "heaven"); stars(c, f, 50); mountain(c, 540, 1500, 900, 600, (60, 100, 160), True, 0.4); ground(c, GY, (40, 60, 100))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    rays_burst(c, 540, 1150, f, 80, None, 18, (200, 230, 255, 50), 0.9, 0.6)
    title(c, "KAILASH", f, _starts[6] + 10, 560, 130, (150, 200, 255), hold=50)

def s_wisdom(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.1)); sky(c, "heaven"); mountain(c, 540, 1500, 900, 600, (60, 100, 160), True, 0.4); ground(c, GY, (40, 60, 100))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    title(c, "TRUE POWER", f, _starts[7] + 6, 560, 110, GOLD, hold=50)

def s_escape(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(540, 400)); sky(c, "day"); ground(c, GY, (170, 120, 70))
    q = prog(f, _starts[8], _starts[8] + max(1, n))
    draw_char(c, lerp(540, 200, q), GY, 1.4, "queen", act(f, "walk", 1, expr="smile"))

def s_kailash(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1100, 1130)); sky(c, "heaven"); stars(c, f, 60)
    mountain(c, 300, 1500, 900, 550, (60, 100, 160), True, 0.3)
    mountain(c, 800, 1520, 800, 480, (80, 120, 180), True, 0.4)
    ground(c, GY, (40, 60, 100))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    title(c, "CHOICE", f, _starts[9] + 10, 560, 120, (200, 230, 255), hold=50)

def s_title(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1130)); sky(c, "heaven"); stars(c, f, 60)
    mountain(c, 540, 1500, 900, 600, (60, 100, 160), True, 0.4); ground(c, GY, (40, 60, 100))
    k = pop(f, _starts[10], 14)
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="smile"))
    c.text("SATI", W / 2, 480, 150, GOLD, INK, 10, scale=max(0.01, k))
    if f >= T.total - 20: follow_button(c, W / 2, 1750, prog(f, T.total - 20, T.total - 10))

FN = dict(palace=s_palace, suitors=s_suitors, sati_walk=s_sati_walk, refusal=s_refusal, shock=s_shock, defiance=s_defiance, vision=s_vision, wisdom=s_wisdom, escape=s_escape, kailash=s_kailash, title=s_title)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Kings and princes from every corner"), "dhol", 0.8),
         (T.start("Sati walks among them like a silent flame."), "chime", 0.9),
         (T.start("The court gasps in absolute shock."), "thunk", 1.0),
         (T.start("Sati lifts her chin with quiet defiance."), "riser", 0.7),
         (T.start("In her mind, the grand thrones dissolve into mist."), "whoosh", 0.8),
         (T.start("True royalty wears no gold,"), "bell", 0.9),
         (T.start("She leaves the assembly hall before"), "dhol", 0.8),
         (T.start("The path to the ascetic lord"), "swell", 0.8),
         (T.start("But Sati has already made her eternal choice..."), "chime", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
