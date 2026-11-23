import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("arena", "The sacrificial arena falls dead silent."),
    ("daksha", "Daksha stands tall on his elevated platform."),
    ("insults", "He hurls insults at the ascetic lord"),
    ("sati", "Sati listens."),
    ("defend", "She tries to defend her divine husband."),
    ("blasphemy", "He utters the ultimate blasphemy"),
    ("awakening", "Something inside Sati breaks."),
    ("step", "She steps forward."),
    ("truth", "If a body born of"),
    ("fire", "She sits in deep meditation."),
    ("panic", "Panic erupts among the gods."),
    ("cosmos", "A grief so immense begins"),
    ("wrath", "When a wife's honor is trampled,"),
    ("shiva", "This is the tragic fire that awakens"),
    ("vengeance", "From the ashes of devotion,"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"arena", "blasphemy", "awakening", "fire", "wrath", "vengeance"}

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

def s_arena(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), y=(1100, 1130)); sky(c, "dusk"); sun(c, 800, 500, 100, f, True, 0.2)
    temple(c, 540, GY, 1.0, 0.7); ground(c, GY, (120, 60, 60))
    crowd(c, GY, f, 12, -200, W + 200, 0.9, 3, ((150, 40, 60), (180, 120, 40), (80, 50, 110)))
    draw_char(c, 540, GY, 1.4, "queen", act(f, "stand", 1, expr="stern"))
    title(c, "THE SACRIFICE", f, T.start("The sacrificial arena falls dead silent."), 560, 110, GOLD, hold=30)

def s_daksha(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(W / 2, 540)); sky(c, "day"); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    pillar(c, 300, GY, 600, 1.0); pillar(c, 780, GY, 600, 1.0)
    draw_char(c, 540, GY, 1.5, "king", act(f, "shout", 1, hold="staff", expr="stern", mouth=talk(f, T.start("Daksha stands tall"), T.end("He hurls insults at the ascetic lord"))))
    title(c, "DAKSHA", f, T.start("Daksha stands tall"), 560, 130, (255, 180, 80), hold=40)

def s_insults(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100), kicks=[(10, 10)]); sky(c, "storm"); ground(c, GY, (90, 50, 50))
    draw_char(c, 360, GY, 1.4, "king", act(f, "shout", 1, hold="staff", expr="stern"))
    draw_char(c, 720, GY, 1.4, "shiva", act(f, "meditate", 2, hold="trident", expr="closed"))
    title(c, "BLASPHEMY", f, T.start("He hurls insults"), 560, 120, (255, 100, 100), hold=40)

def s_sati(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.3), x=(W / 2, 450)); sky(c, "dusk"); ground(c, GY, (110, 60, 60))
    draw_char(c, 540, GY, 1.5, "queen", act(f, "cry", 1, expr="sad", mouth=talk(f, T.start("Sati listens."), T.end("Every word is a poisoned dagger piercing her heart."))))
    title(c, "HEARTBREAK", f, T.start("Every word"), 560, 110, (255, 180, 180), hold=40)

def s_defend(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "dawn"); ground(c, GY, (130, 70, 70))
    draw_char(c, 540, GY, 1.5, "queen", act(f, "plead", 1, expr="stern", mouth=talk(f, T.start("She tries to defend"), T.end("his cosmic grace, his boundless love..."))))
    title(c, "DEFENCE", f, T.start("She tries to defend"), 560, 120, GOLD, hold=40)

def s_blasphemy(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(5, 12)]); sky(c, "storm"); ground(c, GY, (70, 40, 40))
    draw_char(c, 300, GY, 1.4, "king", act(f, "shout", 1, expr="stern"))
    draw_char(c, 780, GY, 1.4, "queen", act(f, "cry", 2, expr="sad"))
    lightning(c, 540, 50, 900, f, 5, 2)
    title(c, "ULTIMATE INSULT", f, T.start("He utters the ultimate blasphemy"), 560, 110, (255, 90, 90), hold=40)

def s_awakening(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.4), y=(1130, 1080), kicks=[(10, 15)]); sky(c, "fire"); ground(c, GY, (120, 40, 40))
    draw_char(c, 540, GY, 1.6, "durga", act(f, "stand", 1, expr="stern"))
    rays_burst(c, 540, 1150, f, 100, None, 18, (255, 200, 100, 60), 0.9, 0.5)
    title(c, "AWAKENING", f, T.start("Something inside Sati breaks."), 560, 130, GOLD, hold=50)

def s_step(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2)); sky(c, "fire"); ground(c, GY, (100, 40, 40))
    draw_char(c, 540, GY, 1.5, "durga", act(f, "walk", 1, expr="stern"))
    title(c, "THE GODDESS", f, T.start("She steps forward."), 560, 110, (255, 220, 150), hold=40)

def s_truth(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "storm"); ground(c, GY, (90, 40, 40))
    draw_char(c, 540, GY, 1.5, "durga", act(f, "raise", 1, expr="stern", mouth=talk(f, T.start("She raises her hand"), T.end("this body must be cast away..."))))
    title(c, "CHILLING TRUTH", f, T.start("She raises her hand"), 560, 110, (255, 120, 120), hold=40)

def s_fire(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), y=(1130, 1060)); sky(c, "fire"); ground(c, GY, (140, 50, 40))
    fire(c, 540, GY, 1.2, f)
    draw_char(c, 540, GY, 1.5, "durga", act(f, "meditate", 1, expr="closed"))
    ring_wave(c, 540, 1150, f, T.start("A mystical fire ignites"), 600, (255, 200, 100))
    title(c, "MYSTICAL FIRE", f, T.start("A mystical fire ignites"), 560, 120, GOLD, hold=60)

def s_panic(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(5, 10)]); sky(c, "storm"); ground(c, GY, (80, 40, 50))
    crowd(c, GY, f, 14, -200, W + 200, 0.9, 5, ((150, 40, 60), (180, 120, 40)))
    fire(c, 540, GY, 1.0, f)
    draw_char(c, 540, GY, 1.4, "devotee", act(f, "cry", 1, expr="sad"))
    title(c, "PANIC", f, T.start("Panic erupts among the gods."), 560, 110, (255, 110, 110), hold=40)

def s_cosmos(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1)); sky(c, "night"); stars(c, f, 80); ground(c, GY, (50, 40, 80))
    mountain(c, 540, 1500, 1000, 500, (60, 50, 120), True, 0.4)
    draw_char(c, 540, GY, 1.4, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    title(c, "COSMIC GRIEF", f, T.start("A grief so immense begins"), 560, 120, GOLD, hold=50)

def s_wrath(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), kicks=[(10, 14)]); sky(c, "fire"); ground(c, GY, (130, 40, 40))
    fire(c, 540, GY, 1.4, f)
    draw_char(c, 540, GY, 1.5, "durga", act(f, "stand", 1, expr="stern"))
    title(c, "UNIVERSE BURNS", f, T.start("When a wife's honor is trampled,"), 560, 120, (255, 90, 90), hold=50)

def s_shiva(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "night"); stars(c, f, 60); ground(c, GY, (40, 40, 90))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "shout", 1, hold="trident", expr="stern"))
    rays_burst(c, 540, 1150, f, 90, None, 18, (120, 180, 255, 60), 0.9, 0.5)
    title(c, "SHIVA'S WRATH", f, T.start("This is the tragic fire that awakens"), 560, 120, (180, 220, 255), hold=50)

def s_vengeance(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), kicks=[(15, 16)]); sky(c, "storm"); ground(c, GY, (90, 40, 50))
    draw_char(c, 540, GY, 1.6, "shiva", act(f, "fight", 1, hold="trident", expr="stern"))
    lightning(c, 300, 50, 950, f, 10, 3); lightning(c, 780, 50, 950, f, 20, 4)
    title(c, "VENGEANCE", f, T.start("From the ashes of devotion,"), 560, 130, GOLD, hold=None)

FN = dict(arena=s_arena, daksha=s_daksha, insults=s_insults, sati=s_sati, defend=s_defend, blasphemy=s_blasphemy, awakening=s_awakening, step=s_step, truth=s_truth, fire=s_fire, panic=s_panic, cosmos=s_cosmos, wrath=s_wrath, shiva=s_shiva, vengeance=s_vengeance)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("The sacrificial arena falls dead silent."), "bell", 0.8),
         (T.start("Daksha stands tall on his elevated platform."), "dhol", 0.8),
         (T.start("He hurls insults at the ascetic lord"), "thunk", 0.9),
         (T.start("Sati listens."), "heart", 0.8), (T.start("Every word is a poisoned dagger piercing her heart."), "slice", 0.9),
         (T.start("She tries to defend her divine husband."), "chime", 0.8),
         (T.start("He utters the ultimate blasphemy"), "rumble", 1.0),
         (T.start("Something inside Sati breaks."), "whoosh", 0.9), (T.start("She steps forward."), "thunk", 0.8),
         (T.start("She raises her hand and speaks a final,"), "riser", 0.8),
         (T.start("She sits in deep meditation."), "swell", 0.9), (T.start("A mystical fire ignites from within her own soul."), "sparkle", 1.0),
         (T.start("Panic erupts among the gods."), "dhol", 0.9), (T.start("A grief so immense begins"), "heart", 0.8),
         (T.start("When a wife's honor is trampled,"), "rumble", 1.0),
         (T.start("This is the tragic fire that awakens"), "swell", 0.9),
         (T.start("From the ashes of devotion,"), "dhol", 1.0), (T.start("From the ashes of devotion,") + 20, "slice", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("She sits in deep meditation."), back=T.start("A mystical fire ignites from within her own soul."), sa=146.83, mood="dark", tempo=72)
