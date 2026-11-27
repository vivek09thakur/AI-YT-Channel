"""story.py - "Why Ganga Married King Shantanu on One Condition" in folk2d."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()
GY = 1560

SHOT_DEFS = [
    ("intro", "Would you marry someone"),
    ("meeting", "King Shantanu falls hopelessly"),
    ("ultimatum", "She agrees to be his queen"),
    ("marriage", "The king agrees"),
    ("river1", "Yet his heart shatters"),
    ("silence", "He stays silent"),
    ("eighth", "When she lifts their eighth son"),
    ("reveal", "She smiles, holding"),
    ("truth", "These weren't murders"),
    ("departure", "She vanishes into the mist")
]

_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"ultimatum", "river1", "eighth", "reveal", "departure"}

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
    cam(c, lf, n, (1.0, 1.1), y=(1060, 1130)); sky(c, "night"); stars(c, f, 60); moon(c, 200, 400, 70)
    hills(c, 1480, 110, (50, 40, 90), 3, 0.5); ground(c, GY, (70, 50, 70))
    draw_char(c, W / 2, GY, 1.5, "king", act(f, "meditate", 1, expr="sad"))
    title(c, "ONE CONDITION", f, T.start("Would you marry someone"), 560, 100, (255, 180, 180))

def s_meeting(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), x=(W / 2, 600)); sky(c, "dusk"); sun(c, 800, 500, 100, f, True, 0.25)
    river(c, 1400, 200, f); ground(c, GY, (140, 100, 70))
    draw_char(c, 360, GY, 1.4, "king", act(f, "stand", 1, expr="smile"))
    draw_char(c, 720, GY, 1.4, "queen", act(f, "stand", 2, expr="smile"), flip=True)
    title(c, "THE RIVERBANK", f, T.start("King Shantanu falls hopelessly"), 560, 110, GOLD)

def s_ultimatum(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.2), y=(1100, 1130)); sky(c, "heaven"); river(c, 1400, 200, f); ground(c, GY, (100, 120, 150))
    draw_char(c, 360, GY, 1.4, "king", act(f, "kneel", 1, expr="shock"))
    draw_char(c, 720, GY, 1.4, "queen", act(f, "point", 2, expr="stern"), flip=True)
    title(c, "THE ULTIMATUM", f, T.start("She agrees to be his queen"), 560, 110, (255, 120, 120))

def s_marriage(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05)); sky(c, "day"); sun(c, 200, 400, 90, f, True, 0.2); palace(c, 540, 1340, 0.8, 0.5); ground(c, GY, (160, 120, 70))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="smile"))
    draw_char(c, 680, GY, 1.4, "queen", act(f, "stand", 2, expr="smile"), flip=True)
    title(c, "BOUND BY LOVE", f, T.start("The king agrees"), 560, 110, GOLD)

def s_river1(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2), x=(500, 600)); sky(c, "storm"); river(c, 1400, 220, f); ground(c, GY, (60, 70, 90))
    draw_char(c, 300, GY, 1.3, "king", act(f, "stand", 1, expr="sad"))
    draw_char(c, 700, GY, 1.3, "queen", act(f, "walk", 2, hold="newborn", expr="neutral"), flip=True)
    title(c, "SILENT GRIEF", f, T.start("Yet his heart shatters"), 560, 110, (255, 150, 150))

def s_silence(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05)); sky(c, "night"); stars(c, f, 40); river(c, 1400, 200, f); ground(c, GY, (50, 60, 80))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="sad"))
    draw_char(c, 680, GY, 1.4, "queen", act(f, "walk", 2, hold="newborn", expr="neutral"), flip=True)
    title(c, "SEVEN TIMES", f, T.start("He stays silent"), 560, 110, (200, 200, 220))

def s_eighth(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.25), y=(1130, 1100), kicks=[(T.start("When she lifts their eighth son") - _starts[6], 12)]); sky(c, "dusk"); river(c, 1400, 200, f); ground(c, GY, (100, 80, 70))
    draw_char(c, 320, GY, 1.4, "king", act(f, "shout", 1, expr="shock"))
    draw_char(c, 720, GY, 1.4, "queen", act(f, "raise", 2, hold="newborn", expr="smile"), flip=True)
    title(c, "THE EIGHTH SON", f, T.start("When she lifts their eighth son"), 560, 110, GOLD)

def s_reveal(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15)); sky(c, "heaven"); sun(c, W / 2, 500, 120, f, True, 0.25); ground(c, GY, (120, 140, 180))
    draw_char(c, 540, GY, 1.5, "queen", act(f, "cradle", 1, hold="newborn", expr="smile"))
    rays_burst(c, 540, 1150, f, 80, None, 18, (255, 240, 170, 50), 0.9, 0.6)
    title(c, "THE REVELATION", f, T.start("She smiles, holding"), 560, 110, GOLD)

def s_truth(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15)); sky(c, "dusk"); hills(c, 1440, 120, (90, 60, 110), 4, 0.5); ground(c, GY, (110, 80, 90))
    draw_char(c, 400, GY, 1.4, "king", act(f, "stand", 1, expr="sad"))
    draw_char(c, 680, GY, 1.4, "queen", act(f, "bless", 2, hold="newborn", expr="smile"), flip=True)
    title(c, "MERCIFUL RELEASE", f, T.start("These weren't murders"), 560, 110, (220, 200, 255))

def s_departure(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.2)); sky(c, "heaven"); river(c, 1400, 200, f); ground(c, GY, (90, 110, 140))
    draw_char(c, 400, GY, 1.4, "king", act(f, "kneel", 1, expr="sad"))
    draw_char(c, 750, GY, 1.4, "queen", act(f, "fly", 2, expr="smile"), flip=True)
    c.glow(750, 1150, 180, (200, 230, 255), 0.6, 1.0)
    title(c, "LEGACY", f, T.start("She vanishes into the mist"), 560, 120, GOLD, hold=None)
    if f >= T.start("a child destined to shape the Mahabharata"):
        follow_button(c, W / 2, 1750, prog(f, T.start("a child destined to shape the Mahabharata"), T.total - 10))

FN = dict(intro=s_intro, meeting=s_meeting, ultimatum=s_ultimatum, marriage=s_marriage, river1=s_river1, silence=s_silence, eighth=s_eighth, reveal=s_reveal, truth=s_truth, departure=s_departure)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

def _cues():
    C = [(0, "swell", 0.8), (T.start("King Shantanu falls hopelessly"), "chime", 0.7), (T.start("but drops a chilling ultimatum:"), "thunk", 0.9),
         (T.start("or she will vanish forever."), "whoosh", 0.7), (T.start("Yet his heart shatters into pieces when"), "heart", 0.9),
         (T.start("and drowns their first newborn child."), "drip", 0.8), (T.start("as she repeats this unthinkable act seven more times."), "riser", 0.7),
         (T.start("When she lifts their eighth son toward the water,"), "dhol", 1.0), (T.start("his vow and screams why."), "slice", 0.9),
         (T.start("and reveals the shocking truth."), "sparkle", 0.9), (T.start("a heavy curse for celestial beings."), "chime", 0.8),
         (T.start("She vanishes into the mist,"), "whoosh", 0.8), (T.start("a child destined to shape the Mahabharata."), "swell", 1.0)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("Yet his heart shatters into pieces when"), back=T.start("She smiles, holding the crying baby alive,"), sa=146.83, mood="calm", tempo=72)
