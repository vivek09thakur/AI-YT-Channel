"""The Birth of Sati: How Goddess Shakti Became Daksha's Daughter.
Told in folk-art animation style timed to narration.
"""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("prologue", "Before Goddess Parvati was born"),
    ("sati_intro", "there was Sati"),
    ("shiva_destiny", "to change the life of Lord Shiva"),
    ("daksha_desire", "Daksha Prajapati, the son of Brahma"),
    ("penance", "He performed intense penance"),
    ("darshan", "Pleased by his devotion"),
    ("boon_request", "Daksha bowed and requested her"),
    ("warning", "The Goddess accepted his wish"),
    ("birth", "Soon, the Goddess was born"),
    ("childhood", "From childhood"),
    ("devotion", "Her heart was devoted to him alone"),
    ("hatred", "But her father, Daksha"),
    ("conflict", "a conflict that shook the heavens"),
    ("epilogue", "This was the beginning of Sati's story"),
    ("next_ep", "In the next episode"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"darshan", "birth", "conflict", "epilogue"}

def shot_at(f):
    for n, a, b in SHOTS:
        if a <= f < b:
            return n, a, b
    return SHOTS[-1]

def cam(c, lf, n, z=(1.0, 1.0), x=(W / 2, W / 2), y=(1130, 1130), roll=0.0, kicks=()):
    p = smooth(lf / max(1, n))
    creep = lf * 0.0003
    kx = ky = 0.0
    for f0, amp in kicks:
        d = lf - f0
        if 0 <= d < 10:
            decay = 1 - d / 10
            kx += amp * math.sin(d * 2.2) * decay
            ky += amp * 0.6 * math.cos(d * 2.8) * decay
    c.set_cam(lerp(x[0], x[1], p) + kx, lerp(y[0], y[1], p) + ky, lerp(z[0], z[1], p) + creep, roll)

def pop(f, f0, dur=9):
    return back(prog(f, f0, f0 + dur))

def title(c, s, f, f0, y=680, size=110, col=GOLD, hold=None):
    if f < f0:
        return
    a = 1.0 if hold is None else clamp(1 - (f - f0 - hold) / 12)
    if a > 0:
        c.text(s, W / 2, y, size, col, INK, 8, scale=max(0.01, pop(f, f0)), alpha=a)

def talk(f, a, b):
    return 0.5 * abs(math.sin(f * 0.65)) if a <= f < b else 0.0

def sub(c, f):
    s, t = T.sub(f)
    if s:
        c.subtitle(s, t)

# ----------------- Shot Renderers -----------------

def s_prologue(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1140))
    sky(c, "night")
    stars(c, f, 80)
    moon(c, 240, 520, 75)
    mountain(c, 540, 1480, 1000, 520, (50, 40, 90), True, 0.4)
    hills(c, 1460, 100, (65, 45, 110), 3, 0.5)
    ground(c, GY, (85, 55, 95))
    mandala(c, W / 2, 1100, 360, f, GOLD, 14, 0.9, 0.2)
    draw_char(c, W / 2, GY, 1.45, "parvati", act(f, "bless", 1, expr="smile"))
    title(c, "PARVATI", f, _starts[0] + 8, 620, 110, hold=45)

def s_sati_intro(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.18), y=(1120, 1100))
    sky(c, "heaven")
    sun(c, W / 2, 600, 130, f, True, 0.2)
    rays_burst(c, W / 2, 1100, f, 80, None, 18, (255, 230, 150, 55), 0.9, 0.4)
    hills(c, 1440, 110, (140, 80, 120), 5, 0.4)
    temple(c, 880, GY, 0.85, 0.7)
    ground(c, GY, (140, 90, 80))
    draw_char(c, W / 2, GY, 1.55, "sita", act(f, "namaste", 2, expr="smile"))
    title(c, "SATI", f, _starts[1] + 5, 640, 140, GOLD, hold=50)

def s_shiva_destiny(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(W / 2, 580), y=(1130, 1110))
    sky(c, "night")
    stars(c, f, 95)
    moon(c, 840, 480, 80)
    mountain(c, 300, 1480, 900, 560, (40, 35, 80), True, 0.35)
    mountain(c, 860, 1500, 800, 480, (50, 45, 95), True, 0.4)
    ground(c, GY, (60, 50, 85))
    mandala(c, 540, 1160, 400, f, (180, 210, 255), 16, 0.9, -0.2)
    draw_char(c, 540, GY, 1.55, "shiva", act(f, "meditate", 3, hold="trident", expr="closed"))
    title(c, "LORD SHIVA", f, _starts[2] + 12, 620, 110, (200, 225, 255), hold=60)

def s_daksha_desire(c, f, lf, n):
    t_shakti = T.start("the divine Goddess Shakti as his daughter")
    cam(c, lf, n, (1.02, 1.12), y=(1120, 1120))
    sky(c, "dawn")
    sun(c, 240, 520, 100, f, True, 0.25)
    palace(c, 780, 1340, 0.75, 0.5)
    hills(c, 1440, 100, (180, 100, 100), 4, 0.5)
    ground(c, GY, (160, 110, 75))
    draw_char(c, 380, GY, 1.45, "king", act(f, "think" if f < t_shakti else "plead", 4, expr="stern" if f < t_shakti else "neutral"))
    title(c, "DAKSHA PRAJAPATI", f, _starts[3] + 6, 600, 84, hold=45)
    if f >= t_shakti:
        c.glow(760, 1150, 220, (255, 210, 130), 0.7, 1.0)
        rays_burst(c, 760, 1150, f, 60, None, 14, (255, 220, 140, 60), 0.9, 0.5)
        draw_char(c, 760, GY, 1.35, "durga", act(f, "bless", 5, expr="smile"), flip=True)
        title(c, "GODDESS SHAKTI", f, t_shakti + 4, 620, 92, (255, 230, 160), hold=45)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.08, 1.22), y=(1150, 1120))
    sky(c, "dusk")
    hills(c, 1430, 120, (120, 60, 80), 6, 0.45)
    ground(c, GY, (120, 70, 60))
    tree(c, 180, GY, 1.15, 0.9)
    fire(c, 360, GY, 0.85, f)
    fire(c, 720, GY, 0.85, f)
    draw_char(c, 540, GY, 1.45, "sage", act(f, "meditate", 6, expr="closed"))
    ring_wave(c, 540, 1250, f, _starts[4] + 15, 450, GOLD, 1.0, 35)
    title(c, "INTENSE PENANCE", f, _starts[4] + 8, 620, 96, (255, 210, 140), hold=55)

def s_darshan(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(W / 2, 600), kicks=[(0, 12)])
    sky(c, "heaven")
    rays_burst(c, 720, 1080, f, 120, None, 22, (255, 235, 170, 70), 0.9, 0.5)
    mandala(c, 720, 1080, 440, f, GOLD, 18, 0.9, 0.3)
    hills(c, 1450, 100, (160, 90, 140), 5, 0.4)
    ground(c, GY, (145, 95, 110))
    draw_char(c, 280, GY, 1.35, "king", act(f, "kneel", 7, expr="shock"))
    draw_char(c, 740, GY, 1.6, "durga", act(f, "bless", 8, expr="smile"), flip=True)
    sparks(c, 740, 1100, f, _starts[5] + 5, 24, 7, (255, 235, 170), 260)
    title(c, "DIVINE MOTHER", f, _starts[5] + 8, 620, 100, GOLD, hold=50)

def s_boon_request(c, f, lf, n):
    t_wife = T.start("the wife of Lord Shiva")
    cam(c, lf, n, (1.05, 1.14), y=(1130, 1120))
    sky(c, "heaven")
    hills(c, 1440, 100, (150, 90, 130), 4, 0.45)
    ground(c, GY, (135, 85, 95))
    draw_char(c, 320, GY, 1.35, "king", act(f, "bow", 9, expr="smile", mouth=talk(f, _starts[6], _starts[6] + 45)))
    draw_char(c, 760, GY, 1.5, "durga", act(f, "bless", 10, expr="smile"), flip=True)
    if f >= t_wife:
        c.glow(540, 920, 180, (200, 220, 255), 0.6, 1.0)
        draw_char(c, 540, 1120, 0.75, "shiva", act(f, "stand", 11, hold="trident", expr="smile"))
        title(c, "FOR LORD SHIVA", f, t_wife + 4, 640, 94, (200, 225, 255), hold=40)

def s_warning(c, f, lf, n):
    t_abandon = T.start("she would abandon that body")
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100), kicks=[(t_abandon - _starts[7], 10)])
    sky(c, "storm" if f >= t_abandon else "dusk")
    lightning(c, 680, 50, 950, f, t_abandon + 5, 4, life=10) if f >= t_abandon else None
    hills(c, 1420, 120, (90, 45, 75), 7, 0.45)
    ground(c, GY, (95, 55, 65))
    draw_char(c, 280, GY, 1.35, "king", act(f, "plead", 12, expr="sad" if f >= t_abandon else "neutral"))
    draw_char(c, 740, GY, 1.6, "durga", act(f, "point" if f < t_abandon else "raise", 13, expr="stern", mouth=talk(f, _starts[7] + 20, T.end(18))), flip=True)
    if f < t_abandon:
        title(c, "THE WARNING", f, _starts[7] + 8, 620, 110, (255, 200, 120), hold=45)
    else:
        ring_wave(c, 740, 1150, f, t_abandon, 500, (255, 120, 100))
        title(c, "STRICT CONDITION", f, t_abandon + 4, 620, 90, (255, 130, 110), hold=45)

def s_birth(c, f, lf, n):
    t_joy = T.start("Her birth brought joy to the family")
    cam(c, lf, n, (1.0, 1.1), y=(1120, 1140))
    sky(c, "day")
    sun(c, 860, 460, 110, f, True, 0.25)
    palace(c, 540, 1340, 0.85, 0.5)
    ground(c, GY, (160, 120, 75))
    draw_char(c, 240, GY, 1.35, "king", act(f, "bless", 14, expr="smile"))
    draw_char(c, 820, GY, 1.3, "queen", act(f, "give", 15, expr="smile"), flip=True)
    k = pop(f, _starts[8] + 6, 12)
    c.glow(540, 1280, 200 * k, (255, 230, 150), 0.7, 1.0)
    draw_char(c, 540, GY - 120, 0.65 * k, "child", act(f, "raise", 16, expr="smile")) if k > 0.05 else None
    sparks(c, 540, 1280, f, _starts[8] + 8, 20, 8, (255, 230, 150), 220)
    title(c, "SATI IS BORN", f, _starts[8] + 12, 620, 110, GOLD, hold=50)
    if f >= t_joy:
        rays_burst(c, 540, 1280, f, 60, None, 14, (255, 240, 180, 50), 0.9, 0.5)

def s_childhood(c, f, lf, n):
    t_yogi = T.start("the supreme yogi who lived beyond")
    cam(c, lf, n, (1.0, 1.14), x=(480, 560), y=(1130, 1110))
    sky(c, "dawn")
    hills(c, 1440, 110, (160, 95, 125), 5, 0.45)
    tree(c, 160, GY, 1.1, 0.9)
    tree(c, 920, GY, 1.0, 0.9)
    ground(c, GY, (145, 105, 80))
    lotus(c, 540, GY - 20, 50, (255, 160, 190))
    draw_char(c, 360, GY, 1.25, "sita", act(f, "namaste", 17, expr="smile"))
    c.glow(740, 1120, 180, (200, 220, 255), 0.5, 1.0)
    draw_char(c, 740, GY, 1.35, "shiva", act(f, "meditate", 18, hold="trident", expr="closed"), flip=True)
    if f >= t_yogi:
        mandala(c, 740, 1120, 320, f, (180, 210, 255), 14, 0.9, -0.2)
        title(c, "SUPREME YOGI", f, t_yogi + 6, 620, 94, (200, 225, 255), hold=45)

def s_devotion(c, f, lf, n):
    cam(c, lf, n, (1.08, 1.2), y=(1120, 1100))
    sky(c, "night")
    stars(c, f, 85)
    moon(c, W / 2, 460, 90)
    hills(c, 1450, 100, (65, 45, 95), 4, 0.5)
    ground(c, GY, (75, 55, 85))
    rays_burst(c, W / 2, 1140, f, 80, None, 18, (255, 230, 160, 50), 0.9, 0.3)
    mandala(c, W / 2, 1140, 420, f, GOLD, 16, 0.9, 0.25)
    draw_char(c, W / 2, GY, 1.5, "sita", act(f, "namaste", 19, expr="smile"))
    title(c, "DEVOTION", f, _starts[10] + 6, 620, 120, GOLD, hold=50)

def s_hatred(c, f, lf, n):
    t_hate = T.start("would one day develop a deep hatred toward Shiva")
    cam(c, lf, n, (1.1, 1.28), y=(1120, 1090), kicks=[(t_hate - _starts[11], 12)])
    sky(c, "fire" if f >= t_hate else "storm")
    hills(c, 1420, 130, (80, 30, 45), 8, 0.45)
    ground(c, GY, (90, 45, 50))
    for x in (180, 900):
        fire(c, x, GY, 0.8 if f >= t_hate else 0.4, f)
    draw_char(c, 360, GY, 1.5, "king", act(f, "shout" if f >= t_hate else "stand", 20, expr="stern", mouth=talk(f, t_hate, T.end(31))))
    draw_char(c, 760, GY, 1.35, "shiva", act(f, "meditate", 21, hold="trident", expr="closed"), flip=True)
    if f >= t_hate:
        lightning(c, 360, 60, 950, f, t_hate + 4, 9, life=10)
        ring_wave(c, 360, 1200, f, t_hate, 480, (255, 100, 80))
        title(c, "PRIDE AND HATRED", f, t_hate + 6, 620, 88, (255, 120, 90), hold=55)

def s_conflict(c, f, lf, n):
    t_shake = T.start("a conflict that shook the heavens")
    cam(c, lf, n, (1.15, 1.32), y=(1110, 1080), kicks=[(t_shake - _starts[12], 14)])
    sky(c, "storm")
    rain(c, f, 80)
    lightning(c, 540, 40, 1000, f, _starts[12] + 8, 5, life=12)
    hills(c, 1420, 120, (50, 35, 65), 7, 0.45)
    ground(c, GY, (70, 40, 55))
    draw_char(c, 280, GY, 1.35, "king", act(f, "fight", 22, expr="stern"))
    draw_char(c, 540, GY, 1.45, "sita", act(f, "plead", 23, expr="sad"))
    draw_char(c, 800, GY, 1.45, "shiva", act(f, "stand", 24, hold="trident", expr="stern"), flip=True)
    if f >= t_shake:
        sparks(c, 540, 1150, f, t_shake, 24, 11, (255, 180, 120), 280)
        title(c, "THE GREAT CONFLICT", f, t_shake + 4, 620, 84, (255, 140, 110), hold=45)

def s_epilogue(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1130, 1120))
    sky(c, "dusk")
    sun(c, W / 2, 700, 170, f, True, 0.2)
    hills(c, 1440, 110, (110, 60, 100), 5, 0.45)
    ground(c, GY, (120, 75, 80))
    for i, r in enumerate((380, 520)):
        mandala(c, W / 2, 1160, r, f * (1 if i % 2 == 0 else -1), GOLD, 14 + i * 4, 0.9, 0.25)
    draw_char(c, 360, GY, 1.45, "sita", act(f, "namaste", 25, expr="smile"))
    draw_char(c, 720, GY, 1.5, "shiva", act(f, "bless", 26, hold="trident", expr="smile"), flip=True)
    title(c, "STORY OF SATI", f, _starts[13] + 8, 620, 105, GOLD, hold=55)

def s_next_ep(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), y=(1130, 1110))
    sky(c, "dawn")
    sun(c, 820, 520, 120, f, True, 0.25)
    mountain(c, 540, 1480, 950, 500, (120, 70, 110), True, 0.4)
    ground(c, GY, (140, 90, 80))
    mandala(c, 380, 1180, 360, f, GOLD, 14, 0.9, 0.25)
    draw_char(c, 380, GY, 1.45, "sita", act(f, "meditate", 27, expr="closed"))
    c.glow(760, 1120, 160, (200, 220, 255), 0.5, 1.0)
    draw_char(c, 760, GY, 1.35, "shiva", act(f, "bless", 28, hold="trident", expr="smile"), flip=True)
    title(c, "NEXT EPISODE", f, _starts[14] + 4, 600, 96, (255, 230, 160), hold=40)
    title(c, "SATI'S PENANCE", f, _starts[14] + 50, 680, 88, GOLD)
    follow_button(c, W / 2, 1750, prog(f, _starts[14] + 70, T.total - 10))

FN = dict(
    prologue=s_prologue,
    sati_intro=s_sati_intro,
    shiva_destiny=s_shiva_destiny,
    daksha_desire=s_daksha_desire,
    penance=s_penance,
    darshan=s_darshan,
    boon_request=s_boon_request,
    warning=s_warning,
    birth=s_birth,
    childhood=s_childhood,
    devotion=s_devotion,
    hatred=s_hatred,
    conflict=s_conflict,
    epilogue=s_epilogue,
    next_ep=s_next_ep,
)

def render_frame(f):
    c = Canvas()
    name, a, b = shot_at(f)
    lf = f - a
    n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.36)
    if name in FLASH_SHOTS:
        c.flash(0.8 * max(0.0, 1.0 - lf / 6.0))
    sub(c, f)
    return c.finish()

# ----------------- Audio & Cues -----------------

def _cues():
    C = [
        (0, "swell", 0.8),
        (T.start(0), "chime", 0.8),
        (T.start(1), "bell", 0.9),
        (T.start(3), "swell", 0.7),
        (T.start(4), "whoosh", 0.7),
        (T.start(6), "sparkle", 0.85),
        (T.start(7), "dhol", 0.8),
        (T.start(8), "swell", 0.75),
        (T.start(10), "bell", 1.0),
        (T.start(10) + 4, "sparkle", 0.9),
        (T.start(11), "whoosh", 0.65),
        (T.start(14), "chime", 0.8),
        (T.start(15), "bell", 0.8),
        (T.start(16), "rumble", 0.8),
        (T.start(17), "thunk", 0.85),
        (T.start(19), "slice", 0.9),
        (T.start(21), "sparkle", 0.95),
        (T.start(22), "chime", 0.85),
        (T.start(23), "bell", 0.8),
        (T.start(25), "riser", 0.75),
        (T.start(27), "heart", 0.8),
        (T.start(28), "chime", 0.85),
        (T.start(29), "sparkle", 0.8),
        (T.start(30), "thunk", 0.9),
        (T.start(31), "rumble", 0.95),
        (T.start(33), "riser", 0.8),
        (T.start(34), "dhol", 1.0),
        (T.start(35), "swell", 0.8),
        (T.start(36), "bell", 0.9),
        (T.start(37), "pop", 0.7),
        (T.start(38), "chime", 0.85),
    ]
    return sorted(C)

CUES = _cues()
MUSIC = dict(
    stop=T.start(30),
    back=T.start(35),
    sa=146.83,
    mood="bright",
    tempo=74,
)
