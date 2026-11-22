"""story.py - "Sati at Daksha's Yajna" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("grounds", "A grand canopy"),
    ("kailash", "From the high and silent mountains,"),
    ("shiva", "She speaks her heartfelt wish"),
    ("arrival", "Undeterred, Sati steps through"),
    ("assembly", "The festive music falters and dies."),
    ("daksha", "King Daksha stands tall before the crackling sacred fire."),
    ("mockery", "He mocks the wild ascetic husband who sits"),
    ("fury", "Sati feels the blistering heat of the ritual fire,"),
    ("tragedy", "Every wide eye in the grand assembly turns"),
    ("climax", "The stage is finally set for"),
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"arrival", "assembly", "daksha", "fury", "climax"}

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

def s_grounds(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1080, 1150))
    sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    flag(c, 120, GY, 1.0, f, 0.9); flag(c, 960, GY, 1.0, f, 0.9)
    draw_char(c, 330, GY, 1.4, "king", act(f, "stand", 1, expr="stern"))
    draw_char(c, 740, GY, 1.3, "queen", act(f, "stand", 2, expr="neutral"), flip=True)
    title(c, "YAJNA", f, _starts[0] + 10, 560, 130, GOLD, hold=50)

def s_kailash(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), x=(W / 2, 600))
    sky(c, "heaven"); stars(c, f, 40)
    mountain(c, 300, 1500, 900, 520, (54, 44, 120), True, 0.35); ground(c, GY, (90, 52, 80))
    draw_char(c, 380, GY, 1.4, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    draw_char(c, 700, GY, 1.3, "sita", act(f, "sit", 2, expr="sad"), flip=True)
    title(c, "KAILASH", f, _starts[1] + 10, 560, 110, (200, 220, 250), hold=40)

def s_shiva(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1110))
    sky(c, "dream"); stars(c, f, 60)
    mountain(c, 540, 1500, 900, 520, (54, 44, 120), True, 0.35); ground(c, GY, (90, 52, 80))
    draw_char(c, 540, GY, 1.5, "shiva", act(f, "meditate", 1, hold="trident", expr="closed"))
    draw_char(c, 340, GY, 1.3, "sita", act(f, "plead", 2, expr="sad"))
    title(c, "WARNING", f, _starts[2] + 10, 560, 110, GOLD, hold=40)

def s_arrival(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(400, 600))
    sky(c, "day"); palace(c, 800, 1340, 0.8, 0.6); ground(c, GY, (170, 120, 70))
    draw_char(c, 300 + lf * 0.8, GY, 1.4, "sita", act(f, "walk", 1, expr="stern"))
    title(c, "UNINVITED", f, _starts[3] + 10, 560, 120, CRIMSON, hold=40)

def s_assembly(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), y=(1100, 1080))
    sky(c, "dusk"); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (150, 100, 70))
    draw_char(c, 400, GY, 1.4, "sita", act(f, "stand", 1, expr="shock"))
    draw_char(c, 750, GY, 1.3, "priest", act(f, "stand", 2, expr="stern"), flip=True)
    title(c, "SILENCE", f, _starts[4] + 10, 560, 110, GOLD, hold=40)

def s_daksha(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.2), kicks=[(10, 10)])
    sky(c, "storm"); fire(c, 540, GY, 1.0, f); ground(c, GY, (80, 40, 50))
    draw_char(c, 300, GY, 1.4, "sita", act(f, "stand", 1, expr="sad"))
    draw_char(c, 780, GY, 1.5, "king", act(f, "shout", 2, expr="stern"), flip=True)
    title(c, "DAKSHA", f, _starts[5] + 10, 560, 130, (255, 90, 90), hold=40)

def s_mockery(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), y=(1110, 1090))
    sky(c, "storm"); fire(c, 540, GY, 0.9, f); ground(c, GY, (80, 40, 50))
    draw_char(c, 780, GY, 1.5, "king", act(f, "shout", 1, expr="stern"), flip=True)
    draw_char(c, 300, GY, 1.4, "sita", act(f, "stand", 2, expr="sad"))
    title(c, "INSULT", f, _starts[6] + 10, 560, 110, CRIMSON, hold=40)

def s_fury(c, f, lf, n):
    cam(c, lf, n, (1.2, 1.4), kicks=[(5, 15)])
    sky(c, "fire"); fire(c, 540, GY, 1.2, f); ground(c, GY, (90, 30, 30))
    draw_char(c, 540, GY, 1.6, "sita", act(f, "raise", 1, expr="stern"))
    ring_wave(c, 540, 1150, f, _starts[7], 500, (255, 180, 100))
    title(c, "FURY", f, _starts[7] + 10, 520, 150, (255, 120, 80), hold=40)

def s_tragedy(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1))
    sky(c, "dusk"); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (150, 100, 70))
    draw_char(c, 350, GY, 1.4, "king", act(f, "stand", 1, expr="shock"))
    draw_char(c, 730, GY, 1.3, "priest", act(f, "stand", 2, expr="sad"), flip=True)
    title(c, "TRAGEDY", f, _starts[8] + 10, 560, 110, GOLD, hold=40)

def s_climax(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), kicks=[(10, 20)])
    sky(c, "fire"); fire(c, 540, GY, 1.5, f); ground(c, GY, (100, 20, 20))
    draw_char(c, 540, GY, 1.7, "sita", act(f, "raise", 1, expr="stern"))
    rays_burst(c, 540, 1150, f, 100, None, 20, (255, 200, 100, 60), 0.9, 0.5)
    title(c, "SACRIFICE", f, _starts[9] + 10, 480, 160, GOLD, hold=None)

FN = dict(grounds=s_grounds, kailash=s_kailash, shiva=s_shiva, arrival=s_arrival, assembly=s_assembly,
          daksha=s_daksha, mockery=s_mockery, fury=s_fury, tragedy=s_tragedy, climax=s_climax)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("Drums beat a rhythmic pulse"), "dhol", 0.9),
         (T.start("From the high and silent mountains,"), "chime", 0.7),
         (T.start("Sati hears faint whispers of"), "sparkle", 0.8),
         (T.start("She speaks her heartfelt wish"), "bell", 0.8),
         (T.start("Shiva slowly closes his dark, knowing eyes,"), "rumble", 0.9),
         (T.start("Undeterred, Sati steps through"), "whoosh", 0.7),
         (T.start("The festive music falters and dies."), "thunk", 0.8),
         (T.start("King Daksha stands tall before the crackling sacred fire."), "dhol", 1.0),
         (T.start("He mocks the wild ascetic husband who sits"), "riser", 0.7),
         (T.start("Sati feels the blistering heat of the ritual fire,"), "fire", 0.9),
         (T.start("The fierce blood of the primordial mother boils instantly"), "rumble", 1.0),
         (T.start("Every wide eye in the grand assembly turns"), "chime", 0.7),
         (T.start("The stage is finally set for"), "swell", 0.9),
         (T.start("and the terrifying fury of the awakening cosmos."), "dhol", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("Undeterred, Sati steps through"), back=T.start("King Daksha stands tall before the crackling sacred fire."), sa=146.83, mood="dark", tempo=72)
