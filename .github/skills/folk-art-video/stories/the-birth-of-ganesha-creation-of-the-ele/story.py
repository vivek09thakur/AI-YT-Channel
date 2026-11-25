"""story.py - "The Birth of Ganesha" in folk2d. Every shot is a pure function of the frame number, timed to phrases.json."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("chamber", "Goddess Parvati sits alone"),
    ("mold", "She takes turmeric paste"),
    ("life", "She breathes life into the clay"),
    ("guard", "Parvati smiles with fierce"),
    ("shiva", "Soon, Lord Shiva himself"),
    ("block", "The divine boy steps forward"),
    ("fight", "Shiva is stunned"),
    ("clash", "Enraged by this unknown"),
    ("grief", "Goddess Parvati rushes out"),
    ("quest", "Realizing his terrible mistake"),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"shiva", "clash", "grief", "quest"}

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

def s_chamber(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.12), y=(1130, 1110)); sky(c, "heaven"); moon(c, 840, 420, 70); stars(c, f, 40, ymax=600)
    mountain(c, 540, 1500, 1000, 500, (54, 70, 100), True, 0.4); ground(c, GY, (70, 90, 80))
    temple(c, 540, GY, 0.9, 0.5); hut(c, 540, GY, 0.8, 0.6)
    draw_char(c, 540, GY, 1.4, "parvati", act(f, "sit", 1, expr="neutral"))
    title(c, "KAILASH", f, T.start("Goddess Parvati sits alone"), 560, 130, GOLD, hold=40)

def s_mold(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1110, 1090)); sky(c, "dawn"); sun(c, W / 2, 720, 130, f, True, 0.2)
    hills(c, 1440, 120, (90, 130, 100), 4, 0.5); ground(c, GY, (120, 140, 90))
    draw_char(c, 540, GY, 1.5, "parvati", act(f, "give", 2, expr="smile"))
    k = pop(f, T.start("She takes turmeric paste"), 15)
    c.glow(540, 1200, 160 * k, (255, 220, 100), 0.7, 1.0)
    sparks(c, 540, 1200, f, T.start("She takes turmeric paste"), 15, 3, (255, 230, 120), 180)
    title(c, "TURMERIC", f, T.start("She takes turmeric paste"), 560, 120, (255, 220, 120), hold=40)

def s_life(c, f, lf, n):
    t_b = T.start("She breathes life into the clay"); t_r = T.start("and a radiant young prince")
    cam(c, lf, n, (1.2, 1.1), y=(1100, 1130)); sky(c, "dawn"); sun(c, W / 2, 600, 150, f, True, 0.3)
    hills(c, 1440, 120, (110, 140, 110), 5, 0.5); ground(c, GY, (140, 150, 100))
    draw_char(c, 420, GY, 1.4, "parvati", act(f, "bless", 1, expr="smile"))
    if f >= t_b:
        k = pop(f, t_b, 15)
        draw_char(c, 700, GY, 1.1 * k, "child", act(f, "stand" if f < t_r else "namaste", 2, expr="smile"))
        c.glow(700, 1250, 180 * k, (255, 240, 150), 0.8, 1.0)
        sparks(c, 700, 1250, f, t_b, 20, 5, (255, 240, 160), 220)
    if f >= t_r: title(c, "AWAKENING", f, t_r, 520, 120, GOLD, hold=40)

def s_guard(c, f, lf, n):
    t_p = T.start("Parvati smiles with fierce")
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1120)); sky(c, "day"); sun(c, 200, 450, 100, f, True, 0.25)
    hills(c, 1440, 120, (90, 150, 110), 6, 0.5); palace(c, 540, 1340, 0.8, 0.5); ground(c, GY, (160, 130, 90))
    draw_char(c, 360, GY, 1.4, "parvati", act(f, "give", 1, expr="smile"))
    draw_char(c, 720, GY, 1.2, "child", act(f, "stand", 2, hold="sword", expr="stern"))
    if f >= t_p: title(c, "GUARDIAN", f, t_p, 520, 120, (255, 200, 120), hold=50)

def s_shiva(c, f, lf, n):
    t_m = T.start("his majestic trident gleaming")
    cam(c, lf, n, (1.0, 1.2), y=(1130, 1100)); sky(c, "heaven"); stars(c, f, 30, ymax=500)
    hills(c, 1440, 120, (60, 70, 110), 7, 0.45); ground(c, GY, (80, 90, 100))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "walk", 1, hold="trident", expr="stern"))
    if f >= t_m:
        rays_burst(c, 540, 1150, f, 80, None, 18, (255, 240, 180, 50), 0.9, 0.5)
        title(c, "LORD SHIVA", f, t_m, 520, 130, (180, 220, 255), hold=50)

def s_block(c, f, lf, n):
    t_b = T.start("blocking the path with quiet courage")
    cam(c, lf, n, (1.1, 1.2), y=(1120, 1100)); sky(c, "dusk"); sun(c, 850, 500, 100, f, True, 0.25)
    hills(c, 1440, 120, (100, 80, 110), 4, 0.5); ground(c, GY, (120, 100, 90))
    draw_char(c, 330, GY, 1.2, "child", act(f, "stand", 1, hold="sword", expr="stern"))
    draw_char(c, 800, GY, 1.5, "shiva", act(f, "walk", 2, hold="trident", expr="stern"), flip=True)
    if f >= t_b: title(c, "STANDOFF", f, t_b, 520, 120, GOLD, hold=40)

def s_fight(c, f, lf, n):
    t_d = T.start("but the boy defeats them all")
    cam(c, lf, n, (1.1, 1.3), y=(1100, 1080), kicks=[(T.start("and his divine attendants rush forward") - _starts[6], 10)])
    sky(c, "storm"); lightning(c, 300, 60, 900, f, _starts[6], 3)
    hills(c, 1440, 120, (80, 60, 90), 8, 0.45); ground(c, GY, (100, 70, 70))
    draw_char(c, 300, GY, 1.2, "child", act(f, "fight", 1, hold="sword", expr="stern"))
    draw_char(c, 760, GY, 1.3, "warrior", act(f, "strike", 2, expr="shock"), flip=True)
    draw_char(c, 900, GY, 1.3, "warrior", act(f, "strike", 3, expr="shock"), flip=True)
    if f >= t_d: sparks(c, 540, 1200, f, t_d, 20, 4, (255, 220, 120), 240); title(c, "VALOR", f, t_d, 520, 120, (255, 200, 100), hold=40)

def s_clash(c, f, lf, n):
    t_d = T.start("Shiva draws his shiny blade")
    t_s = T.start("strikes off the boy's head")
    cam(c, lf, n, (1.2, 1.4), y=(1090, 1070), kicks=[(t_s - _starts[7], 18)], roll=1.5 * math.sin(lf * 0.05))
    sky(c, "fire"); lightning(c, 540, 40, 950, f, t_d, 5); fire(c, 540, GY, 1.0, f)
    hills(c, 1430, 130, (90, 40, 50), 9, 0.45); ground(c, GY, (90, 50, 50))
    draw_char(c, 320, GY, 1.2, "child", act(f, "stand", 1, hold="sword", expr="shock"))
    draw_char(c, 780, GY, 1.5, "shiva", act(f, "strike", 2, hold="sword", expr="stern"), flip=True)
    if f >= t_s:
        ring_wave(c, 540, 1200, f, t_s, 600, (255, 100, 100))
        sparks(c, 540, 1200, f, t_s, 30, 6, (255, 200, 100), 320)
        title(c, "COSMIC WRATH", f, t_s, 520, 140, (255, 90, 90), hold=None)

def s_grief(c, f, lf, n):
    t_s = T.start("screaming in unbearable grief")
    t_b = T.start("in a pool of blood")
    cam(c, lf, n, (1.1, 1.0), y=(1110, 1130)); sky(c, "storm"); rain(c, f, 80)
    hills(c, 1440, 120, (60, 40, 60), 3, 0.45); ground(c, GY, (70, 40, 40))
    draw_char(c, 420, GY, 1.4, "parvati", act(f, "cry", 1, expr="sad"))
    draw_char(c, 720, GY, 1.1, "child", act(f, "meditate", 2, expr="closed"))
    if f >= t_s: title(c, "GRIEF", f, t_s, 520, 130, (255, 150, 150), hold=50)

def s_quest(c, f, lf, n):
    t_v = T.start("the Lord of Kailash vows")
    t_q = T.start("a divine quest that will shake")
    cam(c, lf, n, (1.0, 1.25), y=(1130, 1090)); sky(c, "heaven"); stars(c, f, 60); moon(c, 840, 420, 70)
    hills(c, 1440, 120, (54, 70, 120), 4, 0.5); ground(c, GY, (80, 90, 110))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "bless", 1, hold="trident", expr="stern"))
    if f >= t_v: rays_burst(c, 540, 1150, f, 90, None, 20, (255, 240, 180, 60), 0.9, 0.6)
    if f >= t_q:
        ring_wave(c, 540, 1150, f, t_q, 700, GOLD, 1.0, 50)
        title(c, "NEW QUEST", f, t_q, 520, 140, GOLD, hold=None)
    if f >= T.total - 40: follow_button(c, W / 2, 1750, prog(f, T.total - 40, T.total - 10))

FN = dict(chamber=s_chamber, mold=s_mold, life=s_life, guard=s_guard, shiva=s_shiva, block=s_block, fight=s_fight, clash=s_clash, grief=s_grief, quest=s_quest)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Goddess Parvati sits alone"), "chime", 0.8),
         (T.start("She takes turmeric paste"), "sparkle", 0.8), (T.start("She breathes life into the clay"), "riser", 0.7),
         (T.start("Parvati smiles with fierce"), "bell", 0.8), (T.start("Soon, Lord Shiva himself"), "whoosh", 0.8),
         (T.start("The divine boy steps forward"), "thunk", 0.8), (T.start("Shiva is stunned"), "dhol", 0.9),
         (T.start("Enraged by this unknown"), "rumble", 0.9), (T.start("strikes off the boy's head"), "slice", 1.0),
         (T.start("Goddess Parvati rushes out"), "heart", 0.9), (T.start("Realizing his terrible mistake"), "chime", 0.8),
         (T.start("a divine quest that will shake"), "swell", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
