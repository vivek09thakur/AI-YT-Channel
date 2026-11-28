"""story.py - The sacrifice of Ekalavya in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "What is the true price"),
    ("devotion", "Young Ekalavya bows before a clay"),
    ("mastery", "Through sheer willpower"),
    ("encounter", "One day"),
    ("hound", "A barking hound interrupts"),
    ("arrows", "and with a blur of arrows"),
    ("demand", "Stunned by this impossible talent"),
    ("sacrifice", "Without a moment of hesitation"),
    ("legacy", "Skill without a guru is dangerous"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"devotion", "encounter", "hound", "demand", "sacrifice", "legacy"}

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
        if 0 <= d < 9:
            kx += amp * math.sin(d * 2.4) * (1 - d / 9)
            ky += amp * 0.6 * math.cos(d * 3.1) * (1 - d / 9)
    c.set_cam(lerp(x[0], x[1], p) + kx, lerp(y[0], y[1], p) + ky, lerp(z[0], z[1], p) + creep, roll)

def pop(f, f0, dur=9):
    return back(prog(f, f0, f0 + dur))

def title(c, s, f, f0, y=660, size=110, col=GOLD, hold=None):
    if f < f0:
        return
    a = 1.0 if hold is None else clamp(1.0 - (f - f0 - hold) / 12.0)
    if a > 0:
        c.text(s, W / 2, y, size, col, INK, 8, scale=max(0.01, pop(f, f0)), alpha=a)

def talk(f, a, b):
    return 0.5 * abs(math.sin(f * 0.6)) if a <= f < b else 0.0

def sub(c, f):
    s, t = T.sub(f)
    if s:
        c.subtitle(s, t)

def draw_clay_statue(c, x, y, s=1.1, par=1.0):
    c.rrect(x - 60 * s, y - 24 * s, x + 60 * s, y, 6 * s, (120, 85, 60), INK, 3, par)
    c.rrect(x - 45 * s, y - 48 * s, x + 45 * s, y - 24 * s, 6 * s, (140, 95, 70), INK, 3, par)
    draw_char(c, x, y - 48 * s, s, "sage", act(0, "meditate", 99, expr="closed"), par=par)
    c.glow(x, y - 200 * s, 120 * s, (255, 200, 100), 0.35, par)

# ---------------- Shot functions ----------------

def s_intro(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.2), y=(1120, 1100))
    sky(c, "night")
    stars(c, f, 60, seed=12, ymax=700)
    moon(c, 840, 500, 80)
    hills(c, 1440, 110, (40, 30, 60), 3, 0.45)
    for x in (120, 960):
        tree(c, x, GY, 1.2, 0.9, (25, 60, 45), (45, 30, 25))
    ground(c, GY, (55, 40, 50))
    rays_burst(c, W / 2, 1120, f, 80, None, 16, (255, 210, 120, 40), 0.9, 0.3)
    draw_char(c, W / 2, GY, 1.5, "warrior", act(f, "aim", 1, holdL="bow", expr="stern"))
    title(c, "THE PRICE", f, T.start("What is the true price"), 650, 120, GOLD, hold=45)

def s_devotion(c, f, lf, n):
    t_sol = T.start("mastering archery in total solitude")
    cam(c, lf, n, (1.0, 1.15), x=(500, 560), y=(1150, 1120))
    sky(c, "dawn")
    sun(c, 240, 520, 100, f, True, 0.25)
    hills(c, 1420, 100, (140, 90, 80), 4, 0.45)
    tree(c, 160, GY, 1.15, 0.9, (60, 120, 70), (80, 50, 40))
    tree(c, 980, GY, 1.1, 0.9, (55, 115, 65), (80, 50, 40))
    ground(c, GY, (140, 100, 70))
    draw_clay_statue(c, 800, GY, 1.15)
    bowing = f < t_sol
    if bowing:
        draw_char(c, 420, GY, 1.35, "warrior", act(f, "bow", 2, expr="closed"))
        title(c, "DEVOTION", f, _starts[1] + 10, 640, 110, (255, 220, 160), hold=50)
    else:
        draw_char(c, 360, GY, 1.4, "warrior", act(f, "aim", 3, holdL="bow", expr="stern"))
        title(c, "SOLITUDE", f, t_sol + 6, 640, 110, GOLD, hold=50)
        c.glow(800, 1150, 160, (255, 215, 130), 0.5, 1.0)

def s_mastery(c, f, lf, n):
    t_p = T.start("he surpasses even the greatest princes")
    cam(c, lf, n, (1.05, 1.25), x=(520, 560), y=(1130, 1100))
    sky(c, "dusk")
    sun(c, 540, 680, 160, f, True, 0.2)
    hills(c, 1430, 120, (110, 60, 80), 6, 0.45)
    ground(c, GY, (130, 75, 65))
    mandala(c, 360, 1180, 360, f, GOLD, 14, 0.9, 0.4)
    draw_char(c, 360, GY, 1.5, "warrior", act(f, "aim", 1, holdL="bow", expr="stern"))
    draw_char(c, 820, GY, 1.25, "arjuna", act(f, "stand" if f < t_p else "think", 2, hold="bow", expr="shock" if f >= t_p else "stern"), flip=True)
    if f < t_p:
        title(c, "WILLPOWER", f, _starts[2] + 4, 650, 110, GOLD, hold=35)
    else:
        title(c, "GREATER SKILL", f, t_p + 4, 650, 100, (255, 200, 140), hold=45)
        sparks(c, 360, 1150, f, t_p, 16, 4, (255, 220, 120), 180)

def s_encounter(c, f, lf, n):
    t_a = T.start("the forest archer in action")
    cam(c, lf, n, (1.0, 1.15), x=(480, 560), y=(1140, 1120))
    sky(c, "day")
    sun(c, 880, 480, 95, f, True, 0.25)
    hills(c, 1420, 90, (80, 130, 90), 5, 0.4)
    tree(c, 100, GY, 1.25, 0.9)
    tree(c, 560, GY, 1.0, 0.8)
    ground(c, GY, (140, 115, 75))
    draw_char(c, 240, GY, 1.35, "sage", act(f, "point" if f >= t_a else "walk", 1, expr="stern", mouth=talk(f, T.start("Drona and his royal"), T.end("the forest archer in action"))))
    draw_char(c, 440, GY, 1.2, "arjuna", act(f, "walk", 2, hold="bow", expr="shock"))
    draw_char(c, 880, GY, 1.35, "warrior", act(f, "aim", 3, holdL="bow", expr="stern"), flip=True)
    if f >= t_a:
        title(c, "DISCOVERY", f, t_a + 4, 650, 110, GOLD, hold=40)

def s_hound(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100), kicks=[(10, 8)])
    sky(c, "storm")
    hills(c, 1420, 100, (60, 50, 70), 5, 0.4)
    tree(c, 920, GY, 1.15, 0.9, (40, 70, 55), (60, 40, 30))
    ground(c, GY, (90, 70, 65))
    draw_animal(c, "dog", 340, GY, 1.15, f, flip=False)
    draw_char(c, 760, GY, 1.5, "warrior", act(f, "aim", 4, holdL="bow", expr="stern"), flip=True)
    c.glow(340, 1380, 90, (255, 120, 80), 0.45 + 0.15 * math.sin(f * 0.4), 1.0)
    title(c, "INTERRUPTION", f, _starts[4] + 6, 650, 100, (255, 150, 120), hold=40)

def s_arrows(c, f, lf, n):
    t_b = T.start("he seals the dog's mouth without shedding")
    t_d = T.start("a single drop of blood")
    cam(c, lf, n, (1.15, 1.35), x=(540, 480), y=(1120, 1080), kicks=[(t_b - _starts[5], 12)])
    sky(c, "dusk")
    hills(c, 1430, 100, (90, 55, 75), 4, 0.45)
    ground(c, GY, (110, 75, 65))
    draw_animal(c, "dog", 300, GY, 1.15, f, flip=False)
    draw_char(c, 840, GY, 1.5, "warrior", act(f, "aim", 5, holdL="bow", expr="stern"), flip=True)
    for i in range(7):
        t0 = _starts[5] + i * 4
        q = prog(f, t0, t0 + 7)
        if 0 < q < 1:
            arrow(c, lerp(750, 350, ease_in(q)), lerp(1200, 1380, q) - 30 * math.sin(q * math.pi), 195, 120, 1.0, 1.0, (255, 220, 120))
    if f >= t_b:
        for i in range(5):
            ang = 175 + i * 6
            arrow(c, 345 - i * 4, 1375 + i * 3, ang, 85, 0.85, 1.0, (255, 215, 100))
        sparks(c, 340, 1380, f, t_b, 16, 7, (255, 230, 140), 160)
        ring_wave(c, 340, 1380, f, t_b, 350, (255, 215, 120))
    if f >= t_d:
        title(c, "NO BLOOD", f, t_d + 4, 650, 120, GOLD, hold=35)
    else:
        title(c, "PERFECTION", f, _starts[5] + 6, 650, 110, (255, 220, 150), hold=30)

def s_demand(c, f, lf, n):
    t_fee = T.start("Drona demands a terrible fee")
    t_th = T.start("He asks for Ekalavya's right thumb")
    cam(c, lf, n, (1.1, 1.25), x=(540, 520), y=(1130, 1100), kicks=[(t_th - _starts[6], 14)])
    sky(c, "fire" if f >= t_th else "storm")
    hills(c, 1420, 110, (60, 35, 55), 6, 0.4)
    ground(c, GY, (85, 50, 60))
    draw_char(c, 320, GY, 1.45, "sage", act(f, "point" if f >= t_th else "raise", 6, expr="stern", mouth=talk(f, t_fee, T.end("He asks for Ekalavya's right thumb"))))
    draw_char(c, 780, GY, 1.4, "warrior", act(f, "stand" if f < t_th else "think", 7, expr="shock" if f >= t_fee else "stern"), flip=True)
    if f >= t_fee and f < t_th:
        title(c, "GURU DAKSHINA", f, t_fee + 4, 650, 95, (255, 200, 120), hold=45)
    if f >= t_th:
        title(c, "THE RIGHT THUMB", f, t_th + 4, 640, 110, CRIMSON, hold=50)
        c.glow(320, 1100, 260, (255, 80, 60), 0.45, 1.0)
        lightning(c, 540, 60, 900, f, t_th + 2, 8)

def s_sacrifice(c, f, lf, n):
    t_sev = T.start("the loyal hunter draws his knife and severs it")
    t_off = T.start("offering it to the master")
    cam(c, lf, n, (1.15, 1.35), x=(540, 500), y=(1120, 1080), kicks=[(t_sev + 15 - _starts[7], 18)])
    sky(c, "fire")
    hills(c, 1430, 120, (70, 30, 45), 7, 0.4)
    ground(c, GY, (80, 40, 45))
    if f < t_sev:
        draw_char(c, 680, GY, 1.45, "warrior", act(f, "stand", 1, hold="dagger", expr="closed"), flip=True)
        draw_char(c, 300, GY, 1.35, "sage", act(f, "stand", 2, expr="stern"))
        title(c, "NO HESITATION", f, _starts[7] + 4, 650, 100, GOLD, hold=35)
    elif f < t_off:
        draw_char(c, 680, GY, 1.45, "warrior", act(f, "strike", 3, hold="dagger", expr="closed"), flip=True)
        draw_char(c, 300, GY, 1.35, "sage", act(f, "stand", 2, expr="shock"))
        sparks(c, 680, 1250, f, t_sev + 10, 24, 9, (255, 100, 100), 220)
        ring_wave(c, 680, 1250, f, t_sev + 10, 400, (255, 80, 80))
        title(c, "SEVERED", f, t_sev + 8, 650, 130, (255, 100, 100), hold=30)
    else:
        draw_char(c, 680, GY, 1.4, "warrior", act(f, "kneel", 4, expr="closed"), flip=True)
        draw_char(c, 320, GY, 1.35, "sage", act(f, "bless", 2, expr="shock"))
        c.glow(500, 1380, 120, GOLD, 0.8, 1.0)
        sparks(c, 500, 1380, f, t_off, 18, 11, GOLD, 160)
        title(c, "SUPREME SACRIFICE", f, t_off + 4, 650, 90, GOLD, hold=35)

def s_legacy(c, f, lf, n):
    t_ch = T.start("but genius without a thumb changes")
    t_hist = T.start("the history of war forever")
    cam(c, lf, n, (1.05, 1.2), y=(1110, 1130))
    sky(c, "heaven" if f >= t_hist else "dusk")
    sun(c, W / 2, 700, 200, f, True, 0.2)
    hills(c, 1430, 120, (100, 55, 90), 8, 0.45)
    ground(c, GY, (120, 75, 70))
    mandala(c, W / 2, 1150, 420, f, GOLD, 18, 0.9, 0.3)
    rays_burst(c, W / 2, 1150, f, 80, None, 18, (255, 230, 160, 50), 0.9, 0.5)
    draw_char(c, W / 2, GY, 1.6, "warrior", act(f, "stand" if f < t_ch else "bless", 1, hold="bow", expr="smile"))
    if f < t_ch:
        title(c, "GENIUS", f, _starts[8] + 4, 650, 120, (255, 220, 160), hold=35)
    elif f < t_hist:
        title(c, "UNBROKEN", f, t_ch + 4, 650, 120, GOLD, hold=35)
    else:
        title(c, "IMMORTAL", f, t_hist + 4, 640, 130, GOLD)
        follow_button(c, W / 2, 1750, prog(f, t_hist + 15, T.total - 10))

FN = dict(
    intro=s_intro,
    devotion=s_devotion,
    mastery=s_mastery,
    encounter=s_encounter,
    hound=s_hound,
    arrows=s_arrows,
    demand=s_demand,
    sacrifice=s_sacrifice,
    legacy=s_legacy,
)

def render_frame(f):
    c = Canvas()
    name, a, b = shot_at(f)
    lf = f - a
    n = max(1, b - a)
    FN[name](c, f, lf, n)
    c.vignette(0.35)
    if name in FLASH_SHOTS:
        c.flash(0.75 * max(0.0, 1.0 - lf / 6.0))
    sub(c, f)
    return c.finish()

# ---------------- Audio cues ----------------

def _cues():
    C = [
        (0, "swell", 0.8),
        (T.start("What is the true price"), "heart", 0.8),
        (T.start("Young Ekalavya bows before a clay"), "bell", 0.9),
        (T.start("mastering archery in total solitude"), "chime", 0.8),
        (T.start("Through sheer willpower"), "swell", 0.7),
        (T.start("he surpasses even the greatest princes"), "dhol", 0.9),
        (T.start("One day"), "whoosh", 0.7),
        (T.start("Drona and his royal students discover"), "bell", 0.7),
        (T.start("A barking hound interrupts"), "rumble", 0.8),
        (T.start("and with a blur of arrows"), "slice", 0.9),
        (T.start("he seals the dog's mouth without shedding"), "sparkle", 0.9),
        (T.start("a single drop of blood"), "chime", 0.8),
        (T.start("Stunned by this impossible talent"), "thunk", 0.8),
        (T.start("Drona demands a terrible fee"), "rumble", 0.9),
        (T.start("He asks for Ekalavya's right thumb"), "heart", 1.0),
        (T.start("Without a moment of hesitation"), "riser", 0.8),
        (T.start("the loyal hunter draws his knife and severs it"), "slice", 1.0),
        (T.start("the loyal hunter draws his knife and severs it") + 15, "thunk", 0.9),
        (T.start("offering it to the master"), "sparkle", 0.8),
        (T.start("Skill without a guru is dangerous"), "chime", 0.8),
        (T.start("but genius without a thumb changes"), "swell", 0.9),
        (T.start("the history of war forever"), "bell", 1.0),
    ]
    return sorted(C)

CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)
