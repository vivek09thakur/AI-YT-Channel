"""folk2d.animals - simple folk-art creatures. draw_animal(c, kind, x, y, s, f, flip, par): feet / belly at (x, y), facing right unless flip."""
import math
from .draw import *
from .cast import warn, GOLD, CRIMSON, SAFFRON, CREAM

ANIMALS = ("elephant", "horse", "deer", "dog", "cow", "bull", "lion", "tiger", "monkey", "bird", "eagle", "peacock", "snake", "fish", "swan", "boar", "rabbit", "tortoise", "mouse", "owl")
ALIASES = {"nandi": "bull", "ox": "bull", "buffalo": "bull", "golden deer": "deer", "stag": "deer", "jatayu": "eagle", "garuda": "eagle", "hawk": "eagle", "vulture": "eagle", "crow": "bird",
           "parrot": "bird", "dove": "bird", "sparrow": "bird", "naga": "snake", "serpent": "snake", "cobra": "snake", "vanara": "monkey", "ape": "monkey", "mushak": "mouse", "rat": "mouse",
           "hamsa": "swan", "goose": "swan", "duck": "swan", "varaha": "boar", "pig": "boar", "hare": "rabbit", "turtle": "tortoise", "kurma": "tortoise", "matsya": "fish", "puppy": "dog", "wolf": "dog", "jackal": "dog", "cat": "tiger", "leopard": "tiger"}

def draw_animal(c, kind, x, y, s=1.0, f=0, flip=False, par=1.0, col=None):
    k = str(kind).strip().lower(); k = ALIASES.get(k, k)
    if k not in ANIMALS:
        warn(f"unknown animal {kind!r} (drawn as deer); known: {', '.join(ANIMALS)}"); k = "deer"
    sx = -1 if flip else 1
    def P(px, py): return (x + sx * px * s, y + py * s)
    def poly(pts, fill, ol=INK, w=4): c.poly([P(*q) for q in pts], fill, ol, w * s, par)
    def ell(cx, cy, rx, ry, fill, ol=INK, w=4): c.ell(*P(cx, cy), rx * s, ry * s, fill, ol, w * s, par)
    def line(pts, color, w=4): c.line([P(*q) for q in pts], color, w * s, par)
    def dot(cx, cy, r, fill): c.dots([P(cx, cy)], r * s, fill, par)
    def eye(ex, ey, r=7): ell(ex, ey, r, r, (255, 250, 240), INK, 2); dot(ex + 1.5, ey, r * 0.5, INK)
    sw = math.sin(f * 0.15)
    if k == "elephant":
        col = col or (120, 130, 160); d = shade(col, 0.8)
        for lx in (-110, -40, 50, 120): poly([(lx - 22, -40), (lx + 22, -40), (lx + 26, 0), (lx - 26, 0)], d)
        ell(0, -200, 190, 150, col); ell(150, -300, 95, 88, col)                                  # body, head
        poly([(130, -360), (90, -330), (80, -260), (110, -240)], d); ell(95, -320, 50, 70, d, INK, 3)   # ear
        line([(230, -270), (270, -200), (262, -120 + sw * 14), (230, -70 + sw * 24)], col, 34)      # trunk
        line([(230, -270), (270, -200), (262, -120 + sw * 14), (230, -70 + sw * 24)], d, 6)
        poly([(190, -250), (300, -220), (205, -230)], (250, 246, 230))                            # tusk
        poly([(-60, -350), (90, -350), (120, -240), (-80, -240)], CRIMSON, INK, 4); poly([(-60, -350), (90, -350), (80, -330), (-50, -330)], GOLD, INK, 3)   # saddle cloth
        for i in range(-3, 4): dot(i * 22 + 10, -255, 5, GOLD)
        eye(185, -315, 8); line([(-150, -250), (-200, -160), (-190, -110)], col, 10)
    elif k in ("horse", "deer", "cow", "bull", "dog", "lion", "tiger", "boar"):
        body = dict(horse=(200, 120, 60), deer=(255, 200, 80), cow=(250, 244, 230), bull=(240, 240, 236), dog=(160, 110, 70), lion=(230, 170, 70), tiger=(255, 150, 50), boar=(90, 70, 70))[k]
        col = col or body; d = shade(col, 0.78)
        hb = dict(horse=1.0, deer=0.85, cow=0.8, bull=0.95, dog=0.55, lion=0.8, tiger=0.8, boar=0.6)[k]   # height
        L = 160 * hb; neck = 120 * hb
        for lx, ph in ((-80, 0), (-50, 0.5), (60, 1.0), (90, 1.5)):
            step = math.sin(f * 0.3 + ph) * 10 if k not in ("cow", "bull") else 0
            c.cap(P(lx, -L), P(lx + step, 0), 14 * s * hb + 4, 9 * s * hb + 3, col, INK, 4 * s, par); ell(lx + step, 0, 14 * hb + 4, 6, d, INK, 3)
        ell(0, -L - 40 * hb, 130 * hb + 20, 68 * hb + 14, col)                                    # body
        if k == "tiger":
            for i in range(-3, 4): line([(i * 30, -L - 100 * hb), (i * 30 + 10, -L - 10 * hb)], INK, 8)
        if k == "deer": [dot(i * 36 - 20, -L - 50 * hb + (i % 2) * 24, 6, (255, 246, 220)) for i in range(-2, 4)]
        hx, hy = 150 * hb + 10, -L - neck - 40 * hb
        c.cap(P(90 * hb, -L - 70 * hb), P(hx - 20, hy + 20), 30 * s * hb + 6, 22 * s * hb + 4, col, INK, 4 * s, par)   # neck
        if k == "lion":
            for i in range(12):
                a = i * math.pi / 6; ell(hx + math.cos(a) * 50, hy + math.sin(a) * 50, 30, 30, (160, 90, 40), INK, 3)
        ell(hx, hy, 46 * hb + 10, 36 * hb + 8, col)                                                # head
        ell(hx + 30 * hb + 10, hy + 10, 22 * hb + 6, 16 * hb + 4, d if k != "boar" else (60, 50, 60), INK, 3)   # muzzle
        if k == "horse": line([(hx - 40, hy - 30), (60 * hb, -L - 90 * hb - 30), (-10, -L - 90 * hb)], d, 14)   # mane
        if k in ("cow", "bull"): [line([(hx + sd * 18, hy - 30), (hx + sd * 34, hy - 70)], (250, 240, 200), 8) for sd in (-1, 1)]
        if k == "deer":
            for sd in (-1, 1): line([(hx + sd * 10, hy - 30), (hx + sd * 26, hy - 90), (hx + sd * 44, hy - 130)], (150, 100, 60), 6); line([(hx + sd * 26, hy - 90), (hx + sd * 2, hy - 120)], (150, 100, 60), 5)
        if k == "boar": poly([(hx + 40, hy + 10), (hx + 70, hy - 14), (hx + 50, hy + 16)], (250, 246, 230))
        ell(hx - 10, hy - 36 * hb - 6, 10, 16 if k != "dog" else 20, col, INK, 3)                # ear
        eye(hx + 8, hy - 6, 6 + 4 * hb)
        if k == "dog": line([(-130 * hb - 10, -L - 50 * hb), (-170 * hb, -L - 110 * hb + sw * 20)], col, 12)
        elif k in ("horse",): line([(-130 * hb - 10, -L - 60 * hb), (-190, -L - 40 + sw * 20), (-200, -L + 60)], d, 16)
        elif k == "lion": line([(-140 * hb, -L - 50 * hb), (-200, -L + sw * 20)], col, 8); dot(-205, -L + sw * 20, 14, (160, 90, 40))
        else: line([(-130 * hb - 10, -L - 50 * hb), (-170, -L + 20 + sw * 10)], col, 8)
        if k == "deer": ell(0, -L - 40 * hb, 130 * hb + 20, 68 * hb + 14, None, (255, 230, 140), 3) if col == (255, 200, 80) else None
    elif k == "monkey":
        col = col or (170, 100, 60); d = shade(col, 0.8)
        line([(-30, -60), (-120, -140 + sw * 20), (-150, -260), (-100, -300)], col, 20)
        for lx in (-40, 40): c.cap(P(lx, -120), P(lx * 1.3, 0), 18 * s, 12 * s, col, INK, 4 * s, par)
        ell(0, -170, 80, 90, col); ell(0, -170, 50, 60, shade(col, 1.2), None, 0)
        ell(0, -300, 62, 58, col); ell(0, -290, 40, 36, (240, 180, 130), INK, 3)
        for sd in (-1, 1): ell(sd * 60, -300, 18, 18, col, INK, 3); c.cap(P(sd * 60, -230), P(sd * 110, -140 + sw * 20 * sd), 16 * s, 12 * s, col, INK, 4 * s, par)
        eye(-14, -300, 7); eye(14, -300, 7); line([(-10, -270), (10, -270)], INK, 4)
    elif k in ("bird", "eagle", "peacock", "swan", "owl"):
        col = col or dict(bird=(70, 150, 220), eagle=(150, 90, 50), peacock=(20, 120, 180), swan=(250, 248, 240), owl=(150, 120, 90))[k]
        d = shade(col, 0.8); big = 1.6 if k == "eagle" else 1.0
        if k == "peacock":
            for i in range(-5, 6):
                a = math.radians(-90 + i * 16); r = 320 + 40 * math.sin(f * 0.1 + i)
                line([(0, -120), (math.cos(a) * r, -120 + math.sin(a) * r)], (30, 160, 120), 14); ell(math.cos(a) * r, -120 + math.sin(a) * r, 28, 20, (20, 90, 200), INK, 3); dot(math.cos(a) * r, -120 + math.sin(a) * r, 9, GOLD)
        flap = math.sin(f * 0.35) * 40 * big
        if k != "owl":
            poly([(-20 * big, -160 * big), (-180 * big, -260 * big + flap), (-240 * big, -200 * big + flap * 0.5), (-60 * big, -120 * big)], d)
            poly([(20 * big, -160 * big), (160 * big, -270 * big + flap), (230 * big, -210 * big + flap * 0.5), (60 * big, -120 * big)], col)
        ell(0, -150 * big, 80 * big, 50 * big, col)
        poly([(-70 * big, -150 * big), (-170 * big, -120 * big), (-160 * big, -170 * big)], d)                     # tail
        if k == "swan": line([(60, -170), (90, -260), (70, -300)], col, 26)
        hx, hy = (80 * big, -200 * big) if k != "swan" else (70, -300)
        ell(hx, hy, 34 * big, 32 * big, col); poly([(hx + 30 * big, hy - 6 * big), (hx + 70 * big, hy + 4 * big), (hx + 30 * big, hy + 12 * big)], (255, 190, 60))
        eye(hx + 6 * big, hy - 8 * big, 6 * big)
        if k == "owl": eye(hx - 14, hy - 8, 10); eye(hx + 14, hy - 8, 10)
        for lx in (-14, 14): line([(lx * big, -100 * big), (lx * big, 0)], (255, 190, 60), 5)
    elif k == "snake":
        col = col or (40, 150, 90); d = shade(col, 0.8)
        pts = [(-240 + i * 24, -40 - abs(math.sin(i * 0.3 + f * 0.1)) * 50) for i in range(18)] + [(190, -140), (200, -230)]
        line(pts, INK, 36); line(pts, col, 28)
        for i in range(0, 18, 2): dot(pts[i][0], pts[i][1], 6, GOLD)
        ell(200, -250, 60, 40, col, INK, 4); ell(200, -250, 40, 26, shade(col, 1.2), None, 0)        # hood
        eye(214, -256, 7); line([(240, -240), (275, -230 + sw * 6)], CRIMSON, 4)
    elif k == "fish":
        col = col or (255, 150, 60)
        poly([(-120, -40), (-170, -90 + sw * 10), (-170, 10 + sw * 10)], shade(col, 0.8))
        ell(0, -40, 120, 60, col); poly([(-20, -100), (20, -140), (50, -100)], shade(col, 0.8))
        for i in range(-2, 3): c.arc(*P(i * 30, -40), 20 * s, 30 * s, 230, 310, shade(col, 0.8), 3 * s, par)
        eye(80, -50, 9)
    elif k == "rabbit":
        col = col or (240, 236, 230)
        ell(0, -70, 70, 60, col); ell(60, -140, 40, 36, col)
        for sd in (-10, 14): ell(60 + sd, -200, 12, 40, col, INK, 3)
        eye(72, -146, 6); dot(-70, -60, 18, col)
    elif k == "tortoise":
        col = col or (60, 130, 90)
        for lx in (-80, 80): ell(lx, -20, 24, 18, (160, 150, 90), INK, 3)
        ell(0, -70, 130, 70, col); ell(0, -80, 100, 48, shade(col, 1.2), INK, 3)
        for i in range(-2, 3): line([(i * 36, -125), (i * 36, -40)], shade(col, 0.7), 4)
        ell(140, -60, 30, 24, (160, 150, 90)); eye(150, -66, 5)
    elif k == "mouse":
        col = col or (150, 150, 160)
        ell(0, -40, 50, 36, col); ell(50, -60, 26, 22, col); ell(50, -90, 14, 14, (240, 180, 180), INK, 3)
        line([(-50, -30), (-110, -20 + sw * 10), (-150, -60)], col, 6); eye(58, -64, 5); dot(76, -58, 4, INK)
