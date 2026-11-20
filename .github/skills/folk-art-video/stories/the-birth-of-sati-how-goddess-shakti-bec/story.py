import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Before Goddess Parvati was born"),
    ("daksha_wish", "Daksha Prajapati, the son of Brahma"),
    ("penance", "He performed intense penance"),
    ("vision", "Pleased by his devotion"),
    ("request", "Daksha bowed and requested her"),
    ("warning", "The Goddess accepted his wish"),
    ("birth", "Soon, the Goddess was born into Daksha's family"),
    ("childhood", "From childhood"),
    ("conflict", "But her father, Daksha"),
    ("tragedy", "And the very daughter he had prayed for"),
    ("epilogue", "This was the beginning of Sati's story"),
    ("next", "In the next episode"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"intro", "vision", "warning", "conflict", "epilogue"}

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
    rays_burst(c, W / 2, 1150, f, 100, None, 20, (255, 214, 120, 40), 0.9, 0.3)
    mountain(c, 130, 1500, 900, 440, (54, 44, 120), True, 0.35); ground(c, GY, (90, 52, 80))                                             # peak off to the left, clear of Shiva's head and halo
    mandala(c, W / 2, 1150, 420, f, GOLD, 18, 0.9, 0.3)
    t_s = T.start("there was Sati.")
    draw_char(c, 440, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    if f >= t_s:
        k = pop(f, t_s, 12)
        draw_char(c, 860, GY, 1.2 * k, "sita", act(f, "namaste", 2, expr="smile"), flip=True) if k > 0.05 else None
        title(c, "SATI", f, t_s, 560, 140)

def s_daksha_wish(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, 540)); sky(c, "day"); sun(c, 850, 480, 100, f, True, 0.25)
    hills(c, 1420, 120, (190, 110, 80), 5, 0.4); palace(c, 540, 1340, 0.8, 0.5); ground(c, GY, (170, 110, 80))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="stern"))
    title(c, "DAKSHA", f, _starts[1], 560, 120)

def s_penance(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), y=(1130, 1110)); sky(c, "dusk"); sun(c, W / 2, 760, 150, f, True, 0.2)
    hills(c, 1440, 120, (96, 50, 120), 4, 0.5); ground(c, GY, (130, 70, 70))
    draw_char(c, W / 2, GY, 1.5, "king", act(f, "meditate", 1, expr="closed"))
    fire(c, 300, GY, 0.8, f); fire(c, 780, GY, 0.8, f)
    title(c, "PENANCE", f, _starts[2], 560, 120, (255, 200, 120))

def s_vision(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2)); sky(c, "heaven"); stars(c, f, 50)
    rays_burst(c, W / 2, 1150, f, 80, None, 18, (255, 240, 170, 60), 0.9, 0.6)
    ground(c, GY, (100, 60, 90))
    draw_char(c, 360, GY, 1.3, "king", act(f, "kneel", 1, expr="smile"))
    draw_char(c, 720, GY, 1.4, "durga", act(f, "bless", 2, expr="smile"), flip=True)
    title(c, "DIVINE MOTHER", f, _starts[3], 560, 110)

def s_request(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05)); sky(c, "heaven")
    ground(c, GY, (100, 60, 90))
    draw_char(c, 380, GY, 1.3, "king", act(f, "bow", 1, expr="neutral", mouth=talk(f, T.start("Daksha bowed and requested her"), T.end("to be born as his daughterÃ¢Â€Â¦"))))
    draw_char(c, 700, GY, 1.4, "durga", act(f, "stand", 2, expr="smile"), flip=True)

def s_warning(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), kicks=[(_starts[5], 10)]); sky(c, "storm")
    lightning(c, 540, 60, 1000, f, _starts[5], 2)
    ground(c, GY, (70, 50, 70))
    draw_char(c, 380, GY, 1.3, "king", act(f, "kneel", 1, expr="shock"))
    draw_char(c, 700, GY, 1.4, "durga", act(f, "raise", 2, expr="stern", mouth=talk(f, _starts[5], T.total)), flip=True)
    title(c, "A WARNING", f, _starts[5], 560, 120, (255, 110, 110))

def s_birth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1)); sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    t_b = T.start("Sati, the daughter of Daksha")
    draw_char(c, 330, GY, 1.4, "king", act(f, "stand", 1, expr="smile"))
    draw_char(c, 740, GY, 1.3, "queen", act(f, "cradle", 2, expr="smile", hold="newborn" if f >= t_b else None), flip=True)               # the newborn is a swaddled bundle laid across the mother's forearms
    title(c, "BIRTH OF SATI", f, t_b, 560, 110, GOLD)

def s_childhood(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.12), x=(W / 2, 600)); sky(c, "day"); sun(c, 900, 500, 90, f, True, 0.25)
    hills(c, 1420, 110, (80, 160, 120), 6, 0.5); tree(c, 200, GY, 1.2, 1.0); ground(c, GY, (150, 110, 70))
    draw_char(c, 330, GY, 1.3, "girl", act(f, "meditate", 1, expr="smile"))
    draw_char(c, 760, GY, 1.5, "shiva", act(f, "meditate", 2, hold="trident", expr="closed"), flip=True)
    title(c, "DEVOTION", f, _starts[7], 560, 120, (255, 200, 120))

def s_conflict(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(_starts[8], 12)]); sky(c, "storm")
    lightning(c, 300, 60, 1000, f, _starts[8], 3)
    hills(c, 1400, 120, (40, 34, 70), 8, 0.45); ground(c, GY, (60, 44, 60))
    draw_char(c, 300, GY, 1.5, "king", act(f, "shout", 1, expr="stern"))
    draw_char(c, 840, GY, 1.5, "shiva", act(f, "stand", 2, hold="trident", expr="neutral"), flip=True)
    title(c, "HATRED", f, _starts[8], 560, 130, (255, 110, 110))

def s_tragedy(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1080)); sky(c, "dusk"); stars(c, f, 40)
    hills(c, 1430, 120, (60, 30, 60), 9, 0.45); ground(c, GY, (80, 40, 50))
    draw_char(c, 540, GY, 1.5, "sita", act(f, "sad", 1, expr="sad"))
    title(c, "TRAGEDY", f, _starts[9], 560, 130, (255, 150, 80))

def s_epilogue(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.08)); sky(c, "dawn"); sun(c, W / 2, 820, 200, f, True, 0.2)
    hills(c, 1450, 130, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    draw_char(c, 400, GY, 1.4, "sita", act(f, "stand", 1, expr="smile"))
    draw_char(c, 680, GY, 1.5, "shiva", act(f, "bless", 2, hold="trident", expr="smile"), flip=True)
    title(c, "SHIVA PURANA", f, _starts[10], 560, 110, GOLD)

def s_next(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.0)); sky(c, "heaven")
    ground(c, GY, (100, 60, 90))
    draw_char(c, W / 2, GY, 1.5, "sita", act(f, "meditate", 1, expr="smile"))
    title(c, "NEXT EPISODE", f, _starts[11], 560, 120, GOLD)

FN = dict(intro=s_intro, daksha_wish=s_daksha_wish, penance=s_penance, vision=s_vision, request=s_request, warning=s_warning, birth=s_birth, childhood=s_childhood, conflict=s_conflict, tragedy=s_tragedy, epilogue=s_epilogue, next=s_next)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Before Goddess Parvati was bornÃ¢Â€Â¦"), "chime", 0.7), (T.start("there was Sati."), "bell", 0.9),
         (T.start("Daksha Prajapati, the son of Brahma,"), "dhol", 0.8), (T.start("He performed intense penanceÃ¢Â€Â¦"), "riser", 0.7),
         (T.start("Pleased by his devotion,"), "sparkle", 0.9), (T.start("Daksha bowed and requested her"), "pop", 0.7),
         (T.start("The Goddess accepted his wishÃ¢Â€Â¦"), "whoosh", 0.7), (T.start("She told Daksha that if he ever disrespected herÃ¢Â€Â¦"), "thunk", 0.9),
         (T.start("Soon, the Goddess was born into Daksha's familyÃ¢Â€Â¦"), "sparkle", 0.9), (T.start("From childhood,"), "chime", 0.7),
         (T.start("But her father, Daksha,"), "rumble", 0.9), (T.start("And the very daughter he had prayed forÃ¢Â€Â¦"), "heart", 0.8),
         (T.start("This was the beginning of Sati's storyÃ¢Â€Â¦"), "swell", 0.8), (T.start("In the next episodeÃ¢Â€Â¦"), "bell", 0.9)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(style="bells", sa=146.83)

