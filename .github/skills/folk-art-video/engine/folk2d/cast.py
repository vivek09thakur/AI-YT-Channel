"""folk2d.cast - frontal folk-art puppet characters (cutout rig). One call = one pose at one frame.
Local units: feet at (0,0), head top ~ -425 at scale 1. Angles in degrees, 0 = hanging straight down, positive = swing outward/up."""
import math
from .draw import *

GOLD = (255, 196, 60); CRIMSON = (188, 34, 62); SAFFRON = (255, 150, 48); CREAM = (255, 240, 208)
BEAD = (232, 96, 44); BELT = (86, 198, 206); PUPIL = (28, 18, 30); MOUTH = (74, 30, 64)      # bead strands, waist belt, eyes, lips
WARNINGS = []                      # unknown outfit / pose / prop names end up here (checked by the pipeline)
def warn(msg):
    if msg not in WARNINGS: WARNINGS.append(msg)
def O(**k):
    base = dict(skin=(226, 170, 122), hair=(40, 26, 30), top=None, top2=GOLD, bottom=(250, 244, 230), bottom2=SAFFRON, sash=None, crown="none",
                crownc=GOLD, beard=None, mous=False, tilak="none", jewel=GOLD, kundal=False, armor=False, halo=None, aura=None, build=1.0, eye=(255, 252, 240),
                female=False, heads=1, monkey=False, fangs=False, old=False, belt=None, bead=None, moon=False)
    base.update(k); return base

OUTFITS = {
    "karna":   O(skin=(214, 158, 110), hair=(30, 20, 26), crown="band", armor=True, kundal=True, aura=(255, 190, 70), bottom=(255, 120, 50), bottom2=GOLD, mous=True, tilak="u", sash=(190, 40, 60), build=1.08),
    "indra":   O(skin=(196, 150, 230), hair=(40, 26, 50), crown="mukut", crownc=GOLD, top=(190, 36, 80), top2=GOLD, bottom=(60, 90, 200), bottom2=GOLD, kundal=True, aura=(150, 160, 255), tilak="three", sash=(255, 220, 120), build=1.05),
    "brahmin": O(skin=(210, 156, 112), hair=(236, 232, 226), crown="jata", beard=(236, 232, 226), mous=True, top=None, bottom=(244, 238, 222), bottom2=(190, 120, 60), tilak="three", sash=(230, 220, 200), build=0.94),
    "surya":   O(skin=(255, 170, 70), hair=(120, 50, 20), crown="mukut", crownc=(255, 120, 40), top=(255, 120, 40), bottom=(255, 90, 40), bottom2=GOLD, halo=(255, 214, 90), aura=(255, 170, 60), kundal=True, tilak="dot", build=1.05),
    "krishna": O(skin=(92, 150, 232), hair=(30, 24, 60), crown="mukut", crownc=GOLD, top=None, bottom=(255, 214, 70), bottom2=CRIMSON, tilak="u", kundal=True, sash=(255, 150, 60), halo=(255, 230, 140)),
    "villager": O(skin=(190, 140, 100), hair=(40, 30, 30), crown="turban", crownc=(230, 80, 60), top=(250, 244, 230), bottom=(250, 244, 230), bottom2=(120, 130, 220), mous=True),
    # ---- Ramayana / Shaiva / Shakta roster
    "rama":     O(skin=(96, 150, 210), hair=(30, 22, 40), crown="mukut", crownc=GOLD, top=None, bottom=(255, 200, 70), bottom2=CRIMSON, tilak="u", kundal=True, sash=(255, 150, 60), halo=(255, 230, 140), build=1.04),
    "sita":     O(skin=(236, 190, 150), hair=(30, 20, 26), crown="band", crownc=GOLD, top=(200, 40, 80), top2=GOLD, bottom=(255, 120, 60), bottom2=GOLD, tilak="dot", sash=(255, 210, 90), female=True, build=0.96),
    "lakshmana": O(skin=(226, 176, 128), hair=(30, 22, 40), crown="mukut", crownc=GOLD, top=None, bottom=(120, 160, 90), bottom2=GOLD, tilak="u", sash=(255, 190, 70)),
    "hanuman":  O(skin=(240, 150, 80), hair=(170, 80, 40), crown="mukut", crownc=GOLD, top=None, bottom=(220, 40, 50), bottom2=GOLD, tilak="dot", monkey=True, aura=(255, 190, 90), build=1.1),
    "ravana":   O(skin=(90, 70, 120), hair=(20, 14, 30), crown="mukut", crownc=(255, 170, 40), top=(40, 24, 60), top2=GOLD, bottom=(120, 20, 50), bottom2=GOLD, mous=True, beard=(20, 14, 30), tilak="three", kundal=True, heads=3, fangs=True, aura=(150, 40, 120), build=1.2),
    "demon":    O(skin=(70, 110, 90), hair=(20, 30, 30), crown="none", top=(50, 30, 40), top2=CRIMSON, bottom=(90, 40, 60), bottom2=(200, 120, 40), mous=True, fangs=True, build=1.15),
    "shiva":    O(skin=(172, 98, 162), hair=(74, 32, 96), crown="jata", top=None, sash=(214, 184, 88), bottom=(214, 184, 88), bottom2=(86, 198, 206), tilak="three", halo=(255, 230, 160), aura=(190, 170, 230), kundal=False, moon=True, build=1.06),
    "parvati":  O(skin=(236, 190, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(200, 60, 100), top2=GOLD, bottom=(60, 150, 110), bottom2=GOLD, tilak="dot", sash=(255, 220, 110), female=True, halo=(255, 230, 160), build=0.96),
    "durga":    O(skin=(236, 184, 140), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(220, 30, 60), top2=GOLD, bottom=(255, 150, 50), bottom2=GOLD, tilak="dot", sash=(255, 220, 110), female=True, halo=(255, 220, 120), aura=(255, 150, 60), build=1.0),
    "ganesha":  O(skin=(240, 160, 110), hair=(120, 60, 40), crown="mukut", crownc=GOLD, top=None, bottom=(255, 200, 70), bottom2=CRIMSON, tilak="u", halo=(255, 230, 140), build=1.0),
    "vishnu":   O(skin=(80, 120, 220), hair=(30, 22, 50), crown="mukut", crownc=GOLD, top=None, bottom=(255, 200, 70), bottom2=CRIMSON, tilak="u", kundal=True, halo=(255, 230, 140), aura=(170, 190, 255), build=1.06),
    "lakshmi":  O(skin=(240, 196, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(220, 60, 90), top2=GOLD, bottom=(255, 120, 80), bottom2=GOLD, tilak="dot", female=True, halo=(255, 230, 140), build=0.96),
    "sage":     O(skin=(200, 150, 110), hair=(230, 226, 220), crown="jata", beard=(230, 226, 220), mous=True, top=None, bottom=(255, 150, 60), bottom2=(190, 90, 40), tilak="three", old=True, build=0.94),
    "king":     O(skin=(214, 160, 114), hair=(40, 26, 30), crown="mukut", crownc=GOLD, top=(150, 40, 90), top2=GOLD, bottom=(250, 240, 220), bottom2=GOLD, mous=True, tilak="u", kundal=True, sash=(255, 210, 90), build=1.06),
    "queen":    O(skin=(236, 190, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(60, 120, 180), top2=GOLD, bottom=(200, 50, 90), bottom2=GOLD, tilak="dot", female=True, sash=(255, 220, 110), build=0.96),
    "warrior":  O(skin=(200, 150, 108), hair=(40, 26, 30), crown="band", armor=True, top=(90, 60, 50), bottom=(160, 60, 50), bottom2=GOLD, mous=True, tilak="u", build=1.08),
    "woman":    O(skin=(220, 170, 128), hair=(30, 20, 26), crown="none", top=(60, 150, 110), top2=GOLD, bottom=(220, 80, 60), bottom2=GOLD, tilak="dot", female=True, build=0.95),
    "child":    O(skin=(226, 176, 130), hair=(40, 26, 30), crown="none", top=(250, 230, 120), bottom=(120, 140, 220), bottom2=GOLD, tilak="dot", build=0.7),
    "devotee":  O(skin=(200, 150, 108), hair=(40, 26, 30), crown="none", top=(250, 244, 230), bottom=(250, 244, 230), bottom2=(200, 120, 60), tilak="three", mous=True),
    "arjuna":   O(skin=(214, 164, 118), hair=(30, 22, 40), crown="mukut", crownc=GOLD, top=None, bottom=(60, 90, 200), bottom2=GOLD, tilak="u", kundal=True, sash=(255, 190, 70), build=1.05),
    "bhima":    O(skin=(200, 140, 100), hair=(30, 22, 30), crown="band", top=None, bottom=(200, 60, 50), bottom2=GOLD, mous=True, tilak="u", build=1.25),
    "duryodhana": O(skin=(190, 140, 110), hair=(30, 20, 26), crown="mukut", crownc=(220, 160, 60), top=(60, 30, 70), top2=GOLD, bottom=(120, 30, 60), bottom2=GOLD, mous=True, tilak="u", kundal=True, build=1.1),
    "kali":     O(skin=(40, 40, 90), hair=(10, 8, 16), crown="mukut", crownc=GOLD, top=(20, 16, 40), top2=CRIMSON, bottom=(180, 30, 50), bottom2=GOLD, tilak="dot", female=True, fangs=True, aura=(200, 40, 80), halo=(255, 200, 100), build=1.05),
    "bhairava": O(skin=(60, 60, 110), hair=(10, 8, 16), crown="jata", top=None, bottom=(40, 20, 50), bottom2=GOLD, beard=(10, 8, 16), mous=True, tilak="three", fangs=True, aura=(255, 140, 60), halo=(255, 170, 70), build=1.1),
}
OUTFIT_ALIASES = {"ram": "rama", "laxman": "lakshmana", "lakshman": "lakshmana", "hanumaan": "hanuman", "raavan": "ravana", "rakshasa": "demon", "asura": "demon",
                  "mahadev": "shiva", "shankar": "shiva", "gauri": "parvati", "ganesh": "ganesha", "ganapati": "ganesha", "narayan": "vishnu", "rishi": "sage",
                  "muni": "sage", "guru": "sage", "priest": "brahmin", "soldier": "warrior", "man": "villager", "farmer": "villager", "boy": "child", "girl": "child",
                  "prince": "king", "princess": "queen", "god": "vishnu", "goddess": "lakshmi", "kaal bhairav": "bhairava", "kala bhairava": "bhairava", "arjun": "arjuna",
                  "bheem": "bhima", "dasharatha": "king", "dashrath": "king", "kaikeyi": "queen", "kausalya": "queen", "sugriva": "hanuman", "vali": "hanuman", "vanara": "hanuman"}
def outfit(o):
    """outfit dict for a name (tolerant: aliases, case; unknown -> villager + warning)"""
    if not isinstance(o, str): return o if isinstance(o, dict) else OUTFITS["villager"]
    k = o.strip().lower()
    k = OUTFIT_ALIASES.get(k, k)
    if k not in OUTFITS:
        warn(f"unknown outfit {o!r} (drawn as villager); known: {', '.join(sorted(OUTFITS))}")
        k = "villager"
    return OUTFITS[k]
DEF = dict(lean=0, bob=0, head=0, armR=(8, 6), armL=(8, 6), legs=(0, 0), expr="neutral", blink=False, mouth=0.0, hold=None, holdL=None, armor=None, look=0.0, aura=1.0, gaze=0.0)
POSES = {
    "stand": {}, "namaste": dict(armR=(-18, 232), armL=(-18, 232)), "give": dict(armR=(42, 52), armL=(42, 52)), "point": dict(armR=(96, 4)),
    "raise": dict(armR=(150, 20), armL=(150, 20)), "hips": dict(armR=(40, -80), armL=(40, -80)), "strike": dict(armR=(120, 50)), "think": dict(armR=(40, 120)),
    "plead": dict(armR=(55, 40), armL=(55, 40)), "bless": dict(armR=(75, 70)),
    "walk": dict(legs=(14, -14), armR=(-14, 8), armL=(14, 8)), "run": dict(legs=(32, -32), armR=(-30, 40), armL=(30, 40), lean=8),
    "bow": dict(lean=18, head=12, armR=(-10, 60), armL=(-10, 60)), "kneel": dict(legs=(0, 85), bob=70, armR=(-18, 232), armL=(-18, 232)),
    "aim": dict(armL=(92, -8), armR=(85, -140)), "shout": dict(armR=(150, 20), expr="shock", mouth=0.8), "cry": dict(expr="sad", armR=(60, 120), head=-6),
    "sit": dict(legs=(80, -80), bob=95, armR=(30, 60), armL=(30, 60)), "meditate": dict(legs=(80, -80), bob=95, armR=(30, 90), armL=(30, 90), expr="closed"),
    "hold": dict(armR=(60, 0)), "wave": dict(armR=(140, -30)), "fight": dict(armR=(120, 50), armL=(40, -80), lean=6, expr="stern"), "fly": dict(armR=(170, 0), armL=(30, 10), lean=-12, legs=(-20, 20)),
}
POSE_ALIASES = {"idle": "stand", "standing": "stand", "pray": "namaste", "praying": "namaste", "greet": "namaste", "offer": "give", "pointing": "point", "arms_up": "raise",
                "cheer": "raise", "victory": "raise", "angry": "hips", "proud": "hips", "attack": "strike", "thinking": "think", "beg": "plead", "blessing": "bless",
                "walking": "walk", "running": "run", "kneeling": "kneel", "sitting": "sit", "archer": "aim", "shoot": "aim", "weep": "cry", "sad": "cry", "flying": "fly", "leap": "fly", "jump": "fly"}
def pose_name(name):
    if not isinstance(name, str): return "stand"
    k = name.strip().lower(); k = POSE_ALIASES.get(k, k)
    if k not in POSES:
        warn(f"unknown pose {name!r} (used stand); known: {', '.join(sorted(POSES))}")
        k = "stand"
    return k
def pose(name, **over): d = dict(POSES[pose_name(name)]); d.update(over); return d

def idle(f, seed=0, amp=1.0):
    """always-alive micro motion: breathing, head sway, arm sway"""
    t = f * 0.11 + seed * 2.3
    return dict(bob=math.sin(t) * 2.5 * amp, head=math.sin(t * 0.7 + 1) * 2.2 * amp, lean=math.sin(t * 0.5) * 1.2 * amp, blink=((f + seed * 37) % 93) in (0, 1, 2))

def merge(base, over):
    d = dict(DEF); d.update(base or {}); d.update(over or {}); return d

def draw_char(c, x, y, s=1.0, o="karna", p=None, flip=False, par=1.0):
    """flat geometric cutout: no outlines, square hair block, straight tapering limbs, heavy-lidded almond eyes, bead strands"""
    o = outfit(o)
    p = merge(p, None); sx = -1 if flip else 1
    try: p['armR'] = tuple(p['armR'])[:2]; p['armL'] = tuple(p['armL'])[:2]; p['legs'] = tuple(p['legs'])[:2]
    except Exception: p['armR'], p['armL'], p['legs'] = DEF['armR'], DEF['armL'], DEF['legs']
    if len(p['armR']) < 2: p['armR'] = DEF['armR']
    if len(p['armL']) < 2: p['armL'] = DEF['armL']
    if len(p['legs']) < 2: p['legs'] = DEF['legs']
    sk = o['skin']; skd = shade(sk, 0.84); hair = o['hair']
    belt = o.get('belt') or BELT; bead = o.get('bead') or BEAD
    lean = math.radians(p['lean']); hipc = (0, -170)
    def Wd(px, py): return (x + sx * px * s, y + py * s)
    def U(px, py):
        dx, dy = px - hipc[0], py - hipc[1]
        return Wd(hipc[0] + dx * math.cos(lean) - dy * math.sin(lean), hipc[1] + dx * math.sin(lean) + dy * math.cos(lean) + p['bob'])
    def poly(pts, fill, fn=U): c.poly([fn(*q) for q in pts], fill, None, 0, par)
    def ell(cx, cy, rx, ry, fill, fn=U):
        pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [i * math.pi / 14 for i in range(28)]]; poly(pts, fill, fn)
    def dot(cx, cy, r, fill, fn=U): ell(cx, cy, r, r, fill, fn)
    def rect(x0, y0, x1, y1, fill, fn=U): poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, fn)
    def bar(p1, p2, r1, r2, fill):
        """straight tapering limb with flat ends, p1/p2 already in world coords"""
        (x1, y1), (x2, y2) = p1, p2; ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2; nx, ny = math.cos(ang), math.sin(ang)
        c.poly([(x1 + nx * r1 * s, y1 + ny * r1 * s), (x2 + nx * r2 * s, y2 + ny * r2 * s), (x2 - nx * r2 * s, y2 - ny * r2 * s), (x1 - nx * r1 * s, y1 - ny * r1 * s)], fill, None, 0, par)
    def across(p1, p2, t, r, col, n=3, dr=4.0):
        """row of n beads across a limb at fraction t"""
        (x1, y1), (x2, y2) = p1, p2; ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2; nx, ny = math.cos(ang), math.sin(ang)
        cx, cy = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
        c.dots([(cx + nx * (k - (n - 1) / 2) * dr * 2.1 * s, cy + ny * (k - (n - 1) / 2) * dr * 2.1 * s) for k in range(n)], dr * s, col, par)
    def band(p1, p2, t, r, col, w=2.5, gap=6):
        """two thin lines across a limb (bracelet)"""
        (x1, y1), (x2, y2) = p1, p2; ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2; nx, ny = math.cos(ang), math.sin(ang)
        ux, uy = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
        for k in (-0.5, 0.5):
            cx, cy = x1 + (x2 - x1) * t + ux * k * gap * s, y1 + (y2 - y1) * t + uy * k * gap * s
            c.line([(cx + nx * r * s, cy + ny * r * s), (cx - nx * r * s, cy - ny * r * s)], col, w * s, par)
    def strand(cx, cy, rx, ry, a0, a1, n, r, col, fn=U):
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * k / max(1, n - 1)); dot(cx + rx * math.cos(a), cy + ry * math.sin(a), r, col, fn)

    c.shadow(*Wd(0, 4), 110 * s, 16 * s, 0.28, par=par)
    if o['aura'] and p['aura'] > 0: c.glow(*U(0, -250), 360 * s, o['aura'], 0.55 * p['aura'], par)
    if o['halo']:
        hx, hy = U(0, -366); c.glow(hx, hy, 190 * s, o['halo'], 0.75, par); c.ell(hx, hy, 118 * s, 118 * s, o['halo'], None, 0, par)
    if o.get('monkey'):                                                                           # tail behind the body
        tw = math.sin(f_tail(p)) * 20
        c.line([Wd(-30, -60), Wd(-120, -120 + tw), Wd(-150, -260 + tw * 2), Wd(-100, -330)], hair, 22 * s, par)
        c.ell(*Wd(-100, -336), 16 * s, 16 * s, hair, None, 0, par)
    if o.get('heads', 1) > 1:                                                                     # extra heads (Ravana) peeking out behind
        n = int(o['heads']) - 1
        for i in range(n):
            sd = -1 if i % 2 == 0 else 1; k = i // 2 + 1
            hx, hy = U(sd * 78 * k, -372 + 18 * k)
            c.poly([(hx - 50 * s, hy - 70 * s), (hx + 50 * s, hy - 70 * s), (hx + 50 * s, hy + 30 * s), (hx - 50 * s, hy + 30 * s)], hair, None, 0, par)
            c.poly([(hx - 40 * s, hy - 54 * s), (hx + 40 * s, hy - 54 * s), (hx + 40 * s, hy + 26 * s), (hx + 14 * s, hy + 48 * s), (hx - 14 * s, hy + 48 * s), (hx - 40 * s, hy + 26 * s)], sk, None, 0, par)
            c.poly([(hx - 44 * s, hy - 70 * s), (hx - 32 * s, hy - 100 * s), (hx - 14 * s, hy - 80 * s), (hx, hy - 112 * s), (hx + 14 * s, hy - 80 * s), (hx + 32 * s, hy - 100 * s), (hx + 44 * s, hy - 70 * s)], o['crownc'], None, 0, par)
            for e in (-1, 1):
                ex_, ey_ = hx + e * 17 * s, hy - 6 * s
                c.poly([(ex_ - 14 * s, ey_), (ex_ - 6 * s, ey_ - 7 * s), (ex_ + 6 * s, ey_ - 7 * s), (ex_ + 14 * s, ey_), (ex_ + 6 * s, ey_ + 5 * s), (ex_ - 6 * s, ey_ + 5 * s)], o['eye'], None, 0, par)
                c.ell(ex_, ey_ - 1 * s, 5 * s, 5 * s, PUPIL, None, 0, par)
                c.line([(ex_ - 16 * s, ey_ - 12 * s), (ex_ + 16 * s, ey_ - 15 * s)], INK, 4 * s, par)
            c.line([(hx - 9 * s, hy + 24 * s), (hx + 9 * s, hy + 24 * s)], MOUTH, 4 * s, par)
    # back hair: square block framing the face; long side panels for women, matted locks and elders
    cr = o['crown']
    long_hair = o.get('female') or cr == "jata" or o.get('old')
    hb = -250 if long_hair else -296; ht = -470 if cr == "jata" else -438
    poly([(-70, ht), (70, ht), (70, hb), (-70, hb)], hair, U)

    # ---- legs + lower garment
    for side, ang in ((-1, p['legs'][0]), (1, p['legs'][1])):
        a = math.radians(ang); hip = Wd(side * 28, -170); foot = (hip[0] + sx * math.sin(a) * 160 * s, hip[1] + math.cos(a) * 160 * s)
        bar(hip, foot, 22, 17, sk); fx, fy = foot
        c.poly([(fx - 17 * s, fy - 5 * s), (fx + sx * 30 * s, fy - 5 * s), (fx + sx * 34 * s, fy + 7 * s), (fx - 19 * s, fy + 7 * s)], skd, None, 0, par)
        c.line([(fx - 17 * s, fy - 24 * s), (fx + 17 * s, fy - 24 * s)], GOLD, 4 * s, par)
    hem = -28; w0, w1 = 66, 94
    poly([(-w0, -176), (w0, -176), (w1, hem), (-w1, hem)], o['bottom'], Wd)
    poly([(22, -176), (w0, -176), (w1, hem), (36, hem)], shade(o['bottom'], 0.86), Wd)                 # shadow side
    poly([(-16, -176), (14, -176), (26, hem), (-22, hem)], shade(o['bottom'], 0.93), Wd)                # fold
    poly([(-w1, hem), (w1, hem), (w1 - 3, hem + 22), (-w1 + 3, hem + 22)], o['bottom2'], Wd)
    for i in range(-3, 4): c.dots([Wd(i * 24, hem + 11)], 3.2 * s, CREAM, par)

    # ---- torso: squared shoulders tapering to the waist
    poly([(-88, -304), (88, -304), (62, -172), (-62, -172)], o['top'] or sk, U)
    poly([(30, -304), (88, -304), (62, -172), (22, -172)], shade(o['top'] or sk, 0.88), U)                                                  # shadow side
    if o['top']: poly([(-88, -304), (-40, -304), (0, -262), (40, -304), (88, -304), (88, -292), (0, -238), (-88, -292)], o['top2'], U)    # neckline trim
    if o['sash']: poly([(30, -306), (90, -300), (-36, -172), (-72, -172)], o['sash'], U)                                                # wide diagonal sash
    armor_on = o['armor'] if p['armor'] is None else bool(p['armor'])
    if armor_on:
        poly([(-82, -304), (82, -304), (64, -226), (40, -176), (-40, -176), (-64, -226)], GOLD, U)
        for r_ in range(3):
            for i in range(-2, 3): dot(i * 26 + (13 if r_ % 2 else 0), -276 + r_ * 34, 8, (255, 232, 140))
        ell(0, -236, 20, 20, (255, 244, 190)); ell(0, -236, 11, 11, CRIMSON)
        for sd in (-1, 1): ell(sd * 82, -298, 24, 20, GOLD)
    rect(-64, -188, 64, -160, belt, U)                                                                                                    # belt
    # bead necklaces: two strands
    strand(0, -304, 36, 34, 20, 160, 9, 4.2, bead)
    strand(0, -304, 50, 64, 25, 155, 13, 3.6, bead)

    # ---- arms: straight bars with flat ends
    def arm(side, up, bend, holdv):
        sh = U(side * 74, -292); a1 = math.radians(up); a2 = math.radians(up + bend)
        d1 = (side * math.sin(a1), math.cos(a1)); d2 = (side * math.sin(a2), math.cos(a2))
        def Dv(v): return (sx * (v[0] * math.cos(lean) - v[1] * math.sin(lean)), v[0] * math.sin(lean) + v[1] * math.cos(lean))
        e = (sh[0] + Dv(d1)[0] * 78 * s, sh[1] + Dv(d1)[1] * 78 * s); h = (e[0] + Dv(d2)[0] * 76 * s, e[1] + Dv(d2)[1] * 76 * s)
        if o['top']: c.ell(*sh, 21 * s, 21 * s, o['top'], None, 0, par)
        bar(sh, e, 22, 18, sk); bar(e, h, 18, 13, sk)
        across(sh, e, 0.6, 18, bead, 3, 3.6)                                                                                              # bead armband
        band(e, h, 0.72, 14, (250, 248, 240), 2.2, 7)                                                                                     # bracelet lines
        c.ell(*h, 13 * s, 13 * s, sk, None, 0, par)
        if holdv: prop(holdv, h, Dv(d2), s, c, par, sx)
    arm(-1, *p['armL'], p['holdL']); arm(1, *p['armR'], p['hold'])

    # ---- head
    hc = (0, -366); hr = p['head']
    def Hd(px, py):
        dx, dy = px - hc[0], py - hc[1]
        bx, by = U(hc[0], hc[1])
        r = math.radians(hr); rx = dx * math.cos(r) - dy * math.sin(r); ry = dx * math.sin(r) + dy * math.cos(r)
        return (bx + sx * rx * s, by + ry * s)
    rect(-20, -320, 20, -292, skd, U)                                                                                                     # neck
    if o.get('monkey'):
        for sd in (-1, 1): ell(sd * 54, -366, 18, 20, sk, Hd)
    # face: square top under the hair, straight cheeks, rounded chin
    poly([(-56, -418), (56, -418), (56, -332), (44, -306), (20, -296), (-20, -296), (-44, -306), (-56, -332)], sk, Hd)
    if o.get('monkey'): ell(0, -334, 34, 24, shade(sk, 1.15), Hd)
    if o.get('female'):
        for sd in (-1, 1): dot(sd * 54, -340, 6, o['jewel'], Hd); dot(sd * 54, -328, 4, bead, Hd)
    if o['kundal']:
        for sd in (-1, 1):
            kx, ky = Hd(sd * 56, -332); c.ell(kx, ky, 14 * s, 14 * s, GOLD, None, 0, par); c.ell(kx, ky + 5 * s, 6 * s, 6 * s, CRIMSON, None, 0, par)
    # headgear
    if cr == "band":
        rect(-58, -430, 58, -416, GOLD, Hd); dot(0, -423, 6, CRIMSON, Hd)
    elif cr == "mukut":
        poly([(-58, -438), (-48, -476), (-28, -452), (-13, -500), (0, -464), (13, -500), (28, -452), (48, -476), (58, -438)], o['crownc'], Hd)
        rect(-58, -438, 58, -418, shade(o['crownc'], 0.9), Hd)
        for q in (-30, 0, 30): dot(q, -428, 6, CRIMSON if q else (60, 200, 190), Hd)
    elif cr == "jata":
        poly([(-26, -470), (26, -470), (26, -520), (14, -534), (-14, -534), (-26, -520)], hair, Hd)                                     # top knot
        for q in range(-6, 7): dot(q * 10.4, -464, 4, bead, Hd)                                                                          # rudraksha band
        if o.get('moon'):                                                                                                                # crescent on the left of the knot
            mx, my_ = -46, -496; R = 24
            outer = [(mx + R * math.cos(math.radians(a)), my_ + R * math.sin(math.radians(a))) for a in range(60, 301, 15)]
            inner = [(mx + 12 + R * math.cos(math.radians(a)), my_ + R * math.sin(math.radians(a))) for a in range(300, 59, -15)]
            poly(outer + inner, (250, 248, 240), Hd)
    elif cr == "turban":
        ell(0, -428, 66, 36, o['crownc'], Hd); rect(-62, -428, 62, -416, shade(o['crownc'], 0.8), Hd)
        for q in (-30, 0, 30): c.line([Hd(q - 10, -456), Hd(q + 14, -420)], shade(o['crownc'], 0.7), 4 * s, par)
    else:
        for q in range(-5, 6): dot(q * 10.4, -424, 3.2, bead, Hd) if o.get('female') else None
    # eyes: long heavy-lidded almonds with a thick brow stroke
    ex = 25; ey = -364
    eo = {"closed": 0.0, "shock": 1.3, "sad": 0.8, "stern": 0.7, "smile": 0.85}.get(p['expr'], 1.0)
    if p['blink']: eo = 0.0
    for sd in (-1, 1):
        cx = sd * ex
        tilt = {"stern": 7, "sad": -7, "shock": -3, "smile": -2}.get(p['expr'], 0)
        if eo < 0.12:
            c.line([Hd(cx - 19, ey), Hd(cx, ey + 4), Hd(cx + 19, ey)], INK, 4.5 * s, par)
        else:
            up = [(cx + 20 * math.cos(t), ey - 11 * eo * math.sin(t)) for t in [i * math.pi / 10 for i in range(11)]]
            lo = [(cx + 20 * math.cos(t), ey + 6 * eo * math.sin(t)) for t in [math.pi - i * math.pi / 10 for i in range(11)]]
            poly(up + lo, o['eye'], Hd)
            gx = cx + p['gaze'] * 5; ell(gx, ey - 1, 7, 7 * min(1, eo + 0.2), PUPIL, Hd)
            lid = [Hd(cx + 20 * math.cos(t), ey - 11 * eo * math.sin(t)) for t in [i * math.pi / 10 for i in range(11)]]
            c.line(lid + [Hd(cx + sd * 31, ey - 7)], INK, 4 * s, par)                                                                      # upper lid + wing
        c.line([Hd(cx - sd * 18, ey - 23 + tilt), Hd(cx + sd * 25, ey - 30 - tilt)], INK, 6 * s, par)                                     # brow
    poly([(-4, -360), (4, -360), (10, -338), (-10, -338)], skd, Hd)                                                                        # nose
    my = -322; m = max(p['mouth'], 0.0)
    if p['expr'] == "smile": c.arc(*Hd(0, my - 5), 16 * s, 8 * s, 20, 160, MOUTH, 5 * s, par)
    elif p['expr'] == "sad": c.arc(*Hd(0, my + 8), 14 * s, 6 * s, 200, 340, MOUTH, 5 * s, par)
    elif m > 0.05 or p['expr'] == "shock": ell(0, my, 9 + 5 * m, 3 + 8 * max(m, 0.4 if p['expr'] == 'shock' else 0), MOUTH, Hd)
    else: c.line([Hd(-11, my), Hd(11, my)], MOUTH, 5 * s, par)
    if o['mous']: poly([(-26, my - 12), (-2, my - 18), (-2, my - 12), (-22, my - 6)], hair, Hd); poly([(26, my - 12), (2, my - 18), (2, my - 12), (22, my - 6)], hair, Hd)
    if o.get('fangs'):
        for sd in (-1, 1): poly([(sd * 9, my - 2), (sd * 15, my - 2), (sd * 12, my + 12)], (255, 255, 240), Hd)
    if o['beard']: poly([(-44, -334), (44, -334), (40, -300), (0, -258), (-40, -300)], o['beard'], Hd)
    t = o['tilak']
    if t == "u": c.line([Hd(-6, -400), Hd(0, -386), Hd(6, -400)], CRIMSON, 4.5 * s, par); dot(0, -398, 4, CRIMSON, Hd)
    elif t == "three":
        for dy in (-402, -394, -386): c.line([Hd(-18, dy), Hd(18, dy)], (250, 248, 240), 3 * s, par)
        ell(0, -394, 3, 8, CRIMSON, Hd)
    elif t == "dot": dot(0, -392, 6, CRIMSON, Hd)

def f_tail(p): return p['bob'] * 1.3

PROPS = ("dagger", "staff", "bowl", "lotus", "bow", "mace", "trident", "sword", "torch", "chakra", "flute", "conch", "lamp", "book", "flag", "spear", "shield", "axe", "scroll", "pot")
def prop(kind, h, d, s, c, par, sx):
    ux, uy = d
    nx, ny = -uy, ux
    if not isinstance(kind, str): return
    kind = kind.strip().lower()
    if kind == "dagger":
        tip = (h[0] + ux * 120 * s, h[1] + uy * 120 * s)
        c.poly([(h[0] + nx * 9 * s, h[1] + ny * 9 * s), (tip[0], tip[1]), (h[0] - nx * 9 * s, h[1] - ny * 9 * s)], (236, 240, 250), INK, 4 * s, par)
        c.cap((h[0] - ux * 10 * s, h[1] - uy * 10 * s), (h[0] + ux * 6 * s, h[1] + uy * 6 * s), 11 * s, 11 * s, GOLD, INK, 3 * s, par)
    elif kind == "sword":
        tip = (h[0] + ux * 230 * s, h[1] + uy * 230 * s)
        c.poly([(h[0] + nx * 11 * s, h[1] + ny * 11 * s), (h[0] + ux * 190 * s + nx * 9 * s, h[1] + uy * 190 * s + ny * 9 * s), tip, (h[0] + ux * 190 * s - nx * 9 * s, h[1] + uy * 190 * s - ny * 9 * s), (h[0] - nx * 11 * s, h[1] - ny * 11 * s)], (236, 240, 250), INK, 4 * s, par)
        c.line([(h[0] + nx * 26 * s, h[1] + ny * 26 * s), (h[0] - nx * 26 * s, h[1] - ny * 26 * s)], GOLD, 9 * s, par)
        c.cap((h[0] - ux * 40 * s, h[1] - uy * 40 * s), (h[0], h[1]), 9 * s, 9 * s, (120, 60, 40), INK, 3 * s, par)
    elif kind == "staff":
        c.line([(h[0] - 0, h[1] + 160 * s), (h[0], h[1] - 190 * s)], (120, 78, 50), 11 * s, par); c.ell(h[0], h[1] - 196 * s, 12 * s, 12 * s, GOLD, INK, 3 * s, par)
    elif kind == "spear":
        c.line([(h[0], h[1] + 200 * s), (h[0], h[1] - 260 * s)], (120, 78, 50), 10 * s, par)
        c.poly([(h[0] - 18 * s, h[1] - 250 * s), (h[0], h[1] - 330 * s), (h[0] + 18 * s, h[1] - 250 * s)], (236, 240, 250), INK, 4 * s, par)
    elif kind == "trident":
        c.line([(h[0], h[1] + 200 * s), (h[0], h[1] - 260 * s)], (200, 170, 90), 10 * s, par)
        for k in (-1, 0, 1):
            x0 = h[0] + k * 34 * s; top = h[1] - 330 * s - (0 if k else 20 * s)
            c.line([(h[0], h[1] - 260 * s), (x0, h[1] - 280 * s), (x0, top)], (236, 240, 250), 8 * s, par)
            c.poly([(x0 - 9 * s, top), (x0, top - 26 * s), (x0 + 9 * s, top)], (236, 240, 250), INK, 3 * s, par)
    elif kind == "mace":
        c.line([(h[0] - ux * 20 * s, h[1] - uy * 20 * s), (h[0] + ux * 150 * s, h[1] + uy * 150 * s)], (150, 100, 60), 12 * s, par)
        c.ell(h[0] + ux * 190 * s, h[1] + uy * 190 * s, 46 * s, 46 * s, GOLD, INK, 5 * s, par); c.ell(h[0] + ux * 190 * s, h[1] + uy * 190 * s, 18 * s, 18 * s, CRIMSON, INK, 3 * s, par)
    elif kind == "axe":
        c.line([(h[0] - ux * 20 * s, h[1] - uy * 20 * s), (h[0] + ux * 170 * s, h[1] + uy * 170 * s)], (150, 100, 60), 11 * s, par)
        bx, by = h[0] + ux * 150 * s, h[1] + uy * 150 * s
        c.poly([(bx, by - 10 * s), (bx + nx * 70 * s, by + ny * 70 * s - 50 * s), (bx + nx * 80 * s, by + ny * 80 * s + 30 * s), (bx, by + 30 * s)], (236, 240, 250), INK, 4 * s, par)
    elif kind == "bow":
        bx, by = h[0], h[1]; r = 170 * s
        pts = [(bx + 30 * s * math.cos(t) * sx - 10 * s * sx, by + r * math.sin(t)) for t in [-1.45 + i * 2.9 / 20 for i in range(21)]]
        c.line(pts, (160, 100, 50), 12 * s, par); c.line([pts[0], pts[-1]], (240, 240, 230), 3 * s, par)
        c.ell(bx, by, 12 * s, 12 * s, GOLD, INK, 3 * s, par)
    elif kind == "shield":
        c.ell(h[0], h[1], 70 * s, 80 * s, (200, 80, 60), INK, 6 * s, par); c.ell(h[0], h[1], 30 * s, 30 * s, GOLD, INK, 4 * s, par)
    elif kind == "torch":
        c.line([(h[0], h[1] + 30 * s), (h[0], h[1] - 110 * s)], (120, 78, 50), 12 * s, par)
        c.glow(h[0], h[1] - 150 * s, 90 * s, (255, 180, 60), 0.8, par)
        c.poly([(h[0] - 26 * s, h[1] - 110 * s), (h[0] - 10 * s, h[1] - 170 * s), (h[0], h[1] - 210 * s), (h[0] + 12 * s, h[1] - 160 * s), (h[0] + 26 * s, h[1] - 110 * s)], (255, 150, 50), INK, 3 * s, par)
        c.poly([(h[0] - 12 * s, h[1] - 112 * s), (h[0], h[1] - 165 * s), (h[0] + 12 * s, h[1] - 112 * s)], (255, 230, 120), None, 0, par)
    elif kind == "chakra":
        cx, cy = h[0] + ux * 30 * s, h[1] + uy * 30 * s
        c.glow(cx, cy, 100 * s, (255, 220, 120), 0.7, par)
        c.ell(cx, cy, 56 * s, 56 * s, GOLD, INK, 5 * s, par); c.ell(cx, cy, 36 * s, 36 * s, (255, 240, 200), INK, 3 * s, par)
        for i in range(8):
            a = math.radians(i * 45); c.poly([(cx + 56 * s * math.cos(a - 0.15), cy + 56 * s * math.sin(a - 0.15)), (cx + 74 * s * math.cos(a), cy + 74 * s * math.sin(a)), (cx + 56 * s * math.cos(a + 0.15), cy + 56 * s * math.sin(a + 0.15))], GOLD, INK, 3 * s, par)
    elif kind == "flute":
        c.line([(h[0] - nx * 110 * s, h[1] - ny * 110 * s), (h[0] + nx * 60 * s, h[1] + ny * 60 * s)], (200, 160, 90), 9 * s, par)
        for k in range(4): c.dots([(h[0] - nx * (80 - k * 30) * s, h[1] - ny * (80 - k * 30) * s)], 3 * s, INK, par)
    elif kind == "conch":
        c.ell(h[0], h[1] - 20 * s, 34 * s, 46 * s, (250, 246, 236), INK, 4 * s, par); c.poly([(h[0] - 10 * s, h[1] - 60 * s), (h[0] + 10 * s, h[1] - 60 * s), (h[0], h[1] - 100 * s)], (250, 246, 236), INK, 3 * s, par)
    elif kind == "lamp":
        c.poly([(h[0] - 30 * s, h[1] - 6 * s), (h[0] + 30 * s, h[1] - 6 * s), (h[0] + 18 * s, h[1] + 16 * s), (h[0] - 18 * s, h[1] + 16 * s)], (200, 120, 50), INK, 3 * s, par)
        c.glow(h[0], h[1] - 40 * s, 60 * s, (255, 200, 80), 0.8, par)
        c.poly([(h[0] - 10 * s, h[1] - 8 * s), (h[0], h[1] - 56 * s), (h[0] + 10 * s, h[1] - 8 * s)], (255, 190, 60), INK, 2 * s, par)
    elif kind in ("book", "scroll"):
        c.poly([(h[0] - 44 * s, h[1] - 30 * s), (h[0] + 44 * s, h[1] - 30 * s), (h[0] + 44 * s, h[1] + 26 * s), (h[0] - 44 * s, h[1] + 26 * s)], (250, 240, 210), INK, 4 * s, par)
        for k in range(3): c.line([(h[0] - 30 * s, h[1] - 14 * s + k * 14 * s), (h[0] + 30 * s, h[1] - 14 * s + k * 14 * s)], (150, 100, 60), 2 * s, par)
    elif kind == "flag":
        c.line([(h[0], h[1] + 120 * s), (h[0], h[1] - 300 * s)], (150, 100, 60), 8 * s, par)
        c.poly([(h[0], h[1] - 300 * s), (h[0] + sx * 160 * s, h[1] - 250 * s), (h[0], h[1] - 190 * s)], SAFFRON, INK, 4 * s, par)
    elif kind == "pot":
        c.ell(h[0], h[1] + 20 * s, 36 * s, 40 * s, (200, 110, 60), INK, 4 * s, par); c.ell(h[0], h[1] - 20 * s, 22 * s, 8 * s, (160, 80, 40), INK, 3 * s, par)
    elif kind == "bowl":
        c.poly([(h[0] - 36 * s, h[1] - 4 * s), (h[0] + 36 * s, h[1] - 4 * s), (h[0] + 22 * s, h[1] + 24 * s), (h[0] - 22 * s, h[1] + 24 * s)], GOLD, INK, 4 * s, par)
    elif kind == "lotus":
        from .world import lotus; lotus(c, h[0], h[1] - 6 * s, 40 * s, (255, 150, 190), par)
    else:
        warn(f"unknown prop {kind!r} (not drawn); known: {', '.join(PROPS)}")

def kavach_prop(c, x, y, s=1.0, f=0, glow=1.0, par=1.0, spin=0.0):
    """the detached divine armor + kundal, floating"""
    if glow > 0: c.glow(x, y, 230 * s, (255, 210, 90), 0.85 * glow, par)
    sq = 1 - 0.0 * spin
    c.poly([(x - 90 * s * sq, y - 70 * s), (x + 90 * s * sq, y - 70 * s), (x + 74 * s * sq, y + 10 * s), (x + 46 * s * sq, y + 70 * s), (x - 46 * s * sq, y + 70 * s), (x - 74 * s * sq, y + 10 * s)], GOLD, INK, 6 * s, par)
    for r_ in range(3):
        for i in range(-2, 3): c.dots([(x + (i * 28 + (14 if r_ % 2 else 0)) * s * sq, y + (-40 + r_ * 30) * s)], 8 * s, (255, 238, 160), par)
    c.ell(x, y - 6 * s, 22 * s, 22 * s, (255, 244, 190), INK, 4 * s, par); c.ell(x, y - 6 * s, 12 * s, 12 * s, CRIMSON, None, 0, par)
    for sd in (-1, 1):
        kx = x + sd * 150 * s * sq; ky = y + 30 * s * math.sin(f * 0.15 + sd)
        c.glow(kx, ky, 80 * s, (255, 220, 110), 0.9 * glow, par); c.ell(kx, ky, 24 * s, 24 * s, GOLD, INK, 5 * s, par); c.ell(kx, ky + 10 * s, 9 * s, 9 * s, CRIMSON, None, 0, par)

def act(f, name="stand", seed=0, flip=False, **over):
    """pose preset + always-alive idle motion; keyword overrides win (e.g. lean=12, expr="smile", hold="dagger")"""
    base = merge(idle(f, seed), POSES[pose_name(name)])
    k = pose_name(name)
    if k in ("walk", "run"):                       # animate the legs / arms for locomotion poses
        sw = math.sin(f * (0.45 if k == "run" else 0.28) + seed); amp = 32 if k == "run" else 14
        base.update(legs=(amp * sw, -amp * sw), armR=(-amp * sw * 1.2, 8 if k == "walk" else 40), armL=(amp * sw * 1.2, 8 if k == "walk" else 40), bob=base['bob'] + abs(sw) * 6)
    if k == "fly": base.update(bob=base['bob'] + math.sin(f * 0.2 + seed) * 10)
    base.update(over); return base
