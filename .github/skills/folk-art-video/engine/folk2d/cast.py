"""folk2d.cast - frontal folk-art puppet characters (cutout rig). One call = one pose at one frame.
Local units: feet at (0,0), head top ~ -425 at scale 1. Angles in degrees, 0 = hanging straight down, positive = swing outward/up."""
import math, os
from .draw import *

GOLD = (222, 168, 52); CRIMSON = (166, 30, 50); SAFFRON = (228, 124, 38); CREAM = (242, 226, 192)                                        # antique gold, kumkum red, deep saffron, parchment (Pattachitra pigments)
BEAD = (26, 20, 26); BELT = (46, 138, 142); PUPIL = (18, 12, 22); IRIS = (92, 54, 30); MOUTH = (74, 30, 64)      # bead strands, waist belt, eyes, lips
WARNINGS = []                      # unknown outfit / pose / prop names end up here (checked by the pipeline)
def warn(msg):
    if msg not in WARNINGS: WARNINGS.append(msg)
def O(**k):
    base = dict(skin=(226, 170, 122), hair=(40, 26, 30), top=None, top2=GOLD, bottom=(250, 244, 230), bottom2=SAFFRON, sash=None, crown="none",
                crownc=GOLD, beard=None, mous=False, tilak="none", jewel=GOLD, kundal=False, armor=False, halo=None, aura=None, build=1.0, eye=(255, 252, 240),
                female=False, heads=1, monkey=False, fangs=False, old=False, belt=None, bead=None, moon=False, dhoti=None, longhair=False, veil=None, guards=False, talwar=False)
    base.update(k); return base

OUTFITS = {
    "karna":   O(dhoti="short", skin=(214, 158, 110), hair=(30, 20, 26), crown="band", armor=True, kundal=True, aura=(255, 190, 70), bottom=(255, 120, 50), bottom2=GOLD, mous=True, tilak="u", sash=(190, 40, 60), build=1.08),
    "indra":   O(dhoti="short", skin=(196, 150, 230), hair=(40, 26, 50), crown="mukut", crownc=GOLD, top=(190, 36, 80), top2=GOLD, bottom=(60, 90, 200), bottom2=GOLD, kundal=True, aura=(150, 160, 255), tilak="three", sash=(255, 220, 120), build=1.05),
    "brahmin": O(skin=(210, 156, 112), hair=(236, 232, 226), crown="jata", beard=(236, 232, 226), mous=True, top=None, bottom=(244, 238, 222), bottom2=(190, 120, 60), tilak="three", sash=(230, 220, 200), build=0.94),
    "surya":   O(skin=(255, 170, 70), hair=(120, 50, 20), crown="mukut", crownc=(255, 120, 40), top=(255, 120, 40), bottom=(255, 90, 40), bottom2=GOLD, halo=(255, 214, 90), aura=(255, 170, 60), kundal=True, tilak="dot", build=1.05),
    "krishna": O(dhoti="short", skin=(92, 150, 232), hair=(30, 24, 60), crown="mukut", crownc=GOLD, top=None, bottom=(255, 214, 70), bottom2=CRIMSON, tilak="u", kundal=True, sash=(255, 150, 60), halo=(255, 230, 140)),
    "villager": O(skin=(190, 140, 100), hair=(40, 30, 30), crown="turban", crownc=(230, 80, 60), top=(250, 244, 230), bottom=(250, 244, 230), bottom2=(120, 130, 220), mous=True),
    # ---- Ramayana / Shaiva / Shakta roster
    "rama":     O(skin=(70, 162, 134), hair=(18, 14, 20), crown="none", top=None, bottom=(238, 118, 58), bottom2=(126, 74, 44), tilak="none", kundal=False, jewel=BEAD, sash=(238, 118, 58), aura=(255, 236, 170), build=1.04),
    "sita":     O(skin=(212, 140, 70), hair=(18, 14, 20), crown="none", top=(246, 242, 226), top2=GOLD, bead=(236, 222, 190), bottom=(240, 238, 212), bottom2=(126, 176, 118), tilak="dot", sash=None, veil=(247, 243, 215, 92), female=True, build=0.96),
    "lakshmana": O(skin=(132, 82, 48), hair=(18, 14, 20), crown="none", top=None, bottom=(236, 134, 60), bottom2=(168, 86, 40), tilak="none", jewel=BEAD, sash=(236, 134, 60), guards=True, talwar=True),
    "hanuman":  O(dhoti="short", skin=(240, 150, 80), hair=(170, 80, 40), crown="mukut", crownc=GOLD, top=None, bottom=(220, 40, 50), bottom2=GOLD, tilak="dot", monkey=True, aura=(255, 190, 90), build=1.1),
    "ravana":   O(skin=(90, 70, 120), hair=(20, 14, 30), crown="mukut", crownc=(255, 170, 40), top=(40, 24, 60), top2=GOLD, bottom=(120, 20, 50), bottom2=GOLD, mous=True, beard=(20, 14, 30), tilak="three", kundal=True, heads=3, fangs=True, aura=(150, 40, 120), build=1.2),
    "demon":    O(skin=(70, 110, 90), hair=(20, 30, 30), crown="none", top=(50, 30, 40), top2=CRIMSON, bottom=(90, 40, 60), bottom2=(200, 120, 40), mous=True, fangs=True, build=1.15),
    "shiva":    O(longhair=True, skin=(172, 98, 162), hair=(74, 32, 96), crown="jata", top=None, sash=(214, 184, 88), bottom=(214, 184, 88), bottom2=(86, 198, 206), tilak="three", halo=(255, 230, 160), aura=(190, 170, 230), kundal=False, moon=True, build=1.06),
    "parvati":  O(skin=(236, 190, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(200, 60, 100), top2=GOLD, bottom=(60, 150, 110), bottom2=GOLD, tilak="dot", sash=(255, 220, 110), female=True, halo=(255, 230, 160), build=0.96),
    "durga":    O(skin=(236, 184, 140), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(220, 30, 60), top2=GOLD, bottom=(255, 150, 50), bottom2=GOLD, tilak="dot", sash=(255, 220, 110), female=True, halo=(255, 220, 120), aura=(255, 150, 60), build=1.0),
    "ganesha":  O(dhoti="short", skin=(240, 160, 110), hair=(120, 60, 40), crown="mukut", crownc=GOLD, top=None, bottom=(255, 200, 70), bottom2=CRIMSON, tilak="u", halo=(255, 230, 140), build=1.0),
    "vishnu":   O(dhoti="short", skin=(80, 120, 220), hair=(30, 22, 50), crown="mukut", crownc=GOLD, top=None, bottom=(255, 200, 70), bottom2=CRIMSON, tilak="u", kundal=True, halo=(255, 230, 140), aura=(170, 190, 255), build=1.06),
    "lakshmi":  O(skin=(240, 196, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(220, 60, 90), top2=GOLD, bottom=(255, 120, 80), bottom2=GOLD, tilak="dot", female=True, halo=(255, 230, 140), build=0.96),
    "sage":     O(skin=(200, 150, 110), hair=(230, 226, 220), crown="jata", beard=(230, 226, 220), mous=True, top=None, bottom=(255, 150, 60), bottom2=(190, 90, 40), tilak="three", old=True, build=0.94),
    "king":     O(skin=(214, 160, 114), hair=(40, 26, 30), crown="mukut", crownc=GOLD, top=(150, 40, 90), top2=GOLD, bottom=(250, 240, 220), bottom2=GOLD, mous=True, tilak="u", kundal=True, sash=(255, 210, 90), build=1.06),
    "queen":    O(skin=(236, 190, 150), hair=(30, 20, 26), crown="mukut", crownc=GOLD, top=(60, 120, 180), top2=GOLD, bottom=(200, 50, 90), bottom2=GOLD, tilak="dot", female=True, sash=(255, 220, 110), build=0.96),
    "warrior":  O(dhoti="short", skin=(200, 150, 108), hair=(40, 26, 30), crown="band", armor=True, top=(90, 60, 50), bottom=(160, 60, 50), bottom2=GOLD, mous=True, tilak="u", build=1.08),
    "woman":    O(skin=(220, 170, 128), hair=(30, 20, 26), crown="none", top=(60, 150, 110), top2=GOLD, bottom=(220, 80, 60), bottom2=GOLD, tilak="dot", female=True, build=0.95),
    "child":    O(skin=(226, 176, 130), hair=(40, 26, 30), crown="none", top=(250, 230, 120), bottom=(120, 140, 220), bottom2=GOLD, tilak="dot", build=0.7),
    "girl":     O(skin=(226, 176, 130), hair=(30, 20, 26), crown="none", top=(250, 230, 120), top2=GOLD, bottom=(200, 60, 100), bottom2=GOLD, tilak="dot", female=True, build=0.7),
    "devotee":  O(skin=(200, 150, 108), hair=(40, 26, 30), crown="none", top=(250, 244, 230), bottom=(250, 244, 230), bottom2=(200, 120, 60), tilak="three", mous=True),
    "arjuna":   O(dhoti="short", skin=(214, 164, 118), hair=(30, 22, 40), crown="mukut", crownc=GOLD, top=None, bottom=(60, 90, 200), bottom2=GOLD, tilak="u", kundal=True, sash=(255, 190, 70), build=1.05),
    "bhima":    O(dhoti="short", skin=(200, 140, 100), hair=(30, 22, 30), crown="band", top=None, bottom=(200, 60, 50), bottom2=GOLD, mous=True, tilak="u", build=1.25),
    "duryodhana": O(skin=(190, 140, 110), hair=(30, 20, 26), crown="mukut", crownc=(220, 160, 60), top=(60, 30, 70), top2=GOLD, bottom=(120, 30, 60), bottom2=GOLD, mous=True, tilak="u", kundal=True, build=1.1),
    "kali":     O(longhair=True, skin=(40, 40, 90), hair=(10, 8, 16), crown="mukut", crownc=GOLD, top=(20, 16, 40), top2=CRIMSON, bottom=(180, 30, 50), bottom2=GOLD, tilak="dot", female=True, fangs=True, aura=(200, 40, 80), halo=(255, 200, 100), build=1.05),
    "bhairava": O(longhair=True, skin=(60, 60, 110), hair=(10, 8, 16), crown="jata", top=None, bottom=(40, 20, 50), bottom2=GOLD, beard=(10, 8, 16), mous=True, tilak="three", fangs=True, aura=(255, 140, 60), halo=(255, 170, 70), build=1.1),
}
OUTFIT_ALIASES = {"ram": "rama", "laxman": "lakshmana", "lakshman": "lakshmana", "hanumaan": "hanuman", "raavan": "ravana", "rakshasa": "demon", "asura": "demon",
                  "mahadev": "shiva", "shankar": "shiva", "gauri": "parvati", "ganesh": "ganesha", "ganapati": "ganesha", "narayan": "vishnu", "rishi": "sage",
                  "muni": "sage", "guru": "sage", "priest": "brahmin", "soldier": "warrior", "man": "villager", "farmer": "villager", "boy": "child", "daughter": "girl", "young girl": "girl",
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
DEF = dict(lean=0, bob=0, head=0, armR=(8, 6), armL=(8, 6), legs=(0, 0), expr="neutral", blink=False, mouth=0.0, hold=None, holdL=None, armor=None, look=0.0, aura=1.0, gaze=0.0, view=None, seat=None, anjali=False)
# seated poses: `seat` picks the folded-leg geometry and `bob` lowers the torso onto it (seat = throne/stool, lotus = cross-legged on the ground, kneel = one knee down)
SEAT_BOB = {"seat": 122, "lotus": 196, "kneel": 118}
NAMASTE_ARM = (-35, 150)
ANJALI_FRONT = (25, 208)                                                                                                                   # frontal rig: palms meet at the heart instead of the forearms crossing
POSES = {
    "stand": {}, "namaste": dict(armR=NAMASTE_ARM, armL=NAMASTE_ARM, anjali=True), "give": dict(armR=(42, 52), armL=(42, 52)), "point": dict(armR=(96, 4)),
    "raise": dict(armR=(112, 30), armL=(112, 30)), "hips": dict(armR=(40, -80), armL=(40, -80)), "strike": dict(armR=(125, 35)), "think": dict(armR=(40, 120)),
    "plead": dict(armR=(55, 40), armL=(55, 40)), "bless": dict(armR=(75, 70)), "cross": dict(armR=(30, -112), armL=(4, 72), legs=(-12, 14), expr="stern"),
    "walk": dict(legs=(14, -14), armR=(-14, 8), armL=(14, 8)), "run": dict(legs=(32, -32), armR=(-30, 40), armL=(30, 40), lean=8),
    "bow": dict(lean=18, head=12, armR=(-10, 60), armL=(-10, 60)), "kneel": dict(seat="kneel", bob=SEAT_BOB["kneel"], armR=NAMASTE_ARM, armL=NAMASTE_ARM, anjali=True),
    "aim": dict(armL=(80, -8), armR=(80, -150)), "shout": dict(armR=(108, 30), expr="shock", mouth=0.8), "cry": dict(expr="sad", armR=(60, 120), head=-6),
    "sit": dict(seat="seat", bob=SEAT_BOB["seat"], armR=(-10, 87), armL=(-10, 87)), "meditate": dict(seat="lotus", bob=SEAT_BOB["lotus"], armR=(-10, 87), armL=(-10, 87), expr="closed"),
    "hold": dict(armR=(60, 0)), "wave": dict(armR=(140, -30)), "fight": dict(armR=(70, 45), armL=(40, -80), lean=6, expr="stern"), "fly": dict(armR=(170, 0), armL=(30, 10), lean=-12, legs=(-20, 20)),
    "cradle": dict(armR=(20, -110), armL=(20, -110)),                                                                                      # frontal: elbows out, both forearms level across the belly (hold="newborn" lays a swaddled baby on them)
}
POSE_ALIASES = {"idle": "stand", "standing": "stand", "pray": "namaste", "praying": "namaste", "greet": "namaste", "offer": "give", "pointing": "point", "arms_up": "raise",
                "cheer": "raise", "victory": "raise", "angry": "hips", "proud": "hips", "attack": "strike", "thinking": "think", "beg": "plead", "blessing": "bless",
                "walking": "walk", "running": "run", "kneeling": "kneel", "sitting": "sit", "throne": "sit", "seated": "sit", "lotus": "meditate", "dhyana": "meditate", "yoga": "meditate", "tapas": "meditate", "penance": "meditate",
                "archer": "aim", "shoot": "aim", "weep": "cry", "sad": "cry", "flying": "fly", "leap": "fly", "jump": "fly", "carry": "cradle", "cradling": "cradle"}
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

VIEW = os.environ.get("FOLK_VIEW", "auto").strip().lower()       # auto: men in profile, women frontal. front / side force one view.

# skeleton (local units, s=1): feet 0, knee -112, hip -224, waist -238, shoulders -336, chin -362, head top -432, top-knot -452
HIP, SH, CHIN, HTOP, HC = -224, -336, -362, -432, -398
HS = 0.74                                                            # head scale about the chin (frontal men)
SIDE_LIFT = -11                                                     # profile head lift (design units); -24 floated the head too high
SIDE_ROT = -25                                                      # profile head tilt (deg, skyward); poses add p['head'] on top
HSF = 1.0                                                           # women: a little larger, rounder head

def smooth(pts, it=3):
    """closed-curve corner cutting; a vertex written as (x, y, 'k') is kept sharp"""
    P = [(q[0], q[1], len(q) > 2) for q in pts]
    for _ in range(it):
        out = []; n = len(P)
        for i, (x, y, k) in enumerate(P):
            if k: out.append((x, y, True)); continue
            px, py, _ = P[i - 1]; nx, ny, _ = P[(i + 1) % n]
            out.append((x + (px - x) * 0.25, y + (py - y) * 0.25, False)); out.append((x + (nx - x) * 0.25, y + (ny - y) * 0.25, False))
        P = out
    return [(x, y) for x, y, _ in P]

def _vsub(a, b): return (a[0] - b[0], a[1] - b[1])
def _vnorm(v):
    L = math.hypot(*v) or 1.0; return (v[0] / L, v[1] / L)
def _perp(d): return (-d[1], d[0])
def _mad(p, d, k): return (p[0] + d[0] * k, p[1] + d[1] * k)
def _miter(p0, p1, p2, r, sign):
    """corner point of the offset outline at joint p1 (sharp elbow / knee)"""
    d1 = _vnorm(_vsub(p1, p0)); d2 = _vnorm(_vsub(p2, p1)); n1 = _perp(d1); n2 = _perp(d2)
    a = _mad(p1, n1, r * sign); b = _mad(p1, n2, r * sign)
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-6: return a
    t = ((b[0] - a[0]) * d2[1] - (b[1] - a[1]) * d2[0]) / den
    m = _mad(a, d1, t)
    if math.hypot(m[0] - p1[0], m[1] - p1[1]) > 2.4 * r: m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    return m

def _prep(c, x, y, s, o, p, flip, par):
    """shared setup for both rigs -> dict of helpers. Everything is straight-edged (no round caps)."""
    o = outfit(o)
    child = o['build'] < 0.85
    if child: s *= o['build']                                                                                                               # child / girl: smaller body with a bigger head, so "from childhood" is not the adult sprite
    p = merge(p, None); sx = -1 if flip else 1
    try: p['armR'] = tuple(p['armR'])[:2]; p['armL'] = tuple(p['armL'])[:2]; p['legs'] = tuple(p['legs'])[:2]
    except Exception: p['armR'], p['armL'], p['legs'] = DEF['armR'], DEF['armL'], DEF['legs']
    if len(p['armR']) < 2: p['armR'] = DEF['armR']
    if len(p['armL']) < 2: p['armL'] = DEF['armL']
    if len(p['legs']) < 2: p['legs'] = DEF['legs']
    lean = math.radians(p['lean']); hipc = (0, HIP)
    def Wd(px, py): return (x + sx * px * s, y + py * s)
    def U(px, py):
        dx, dy = px - hipc[0], py - hipc[1]
        return Wd(hipc[0] + dx * math.cos(lean) - dy * math.sin(lean), hipc[1] + dx * math.sin(lean) + dy * math.cos(lean) + p['bob'])
    def poly(pts, fill, fn=U): c.poly([fn(*q) for q in pts], fill, None, 0, par)
    def polyw(pts, fill): c.poly(pts, fill, None, 0, par)
    def ell(cx, cy, rx, ry, fill, fn=U):
        pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [i * math.pi / 16 for i in range(32)]]; poly(pts, fill, fn)
    def dot(cx, cy, r, fill, fn=U): ell(cx, cy, r, r, fill, fn)
    def cdot(clip, cx, cy, r, fill, fn=U): c.clip_ell([fn(*q) for q in clip], *fn(cx, cy), r * s, r * s, fill, par)                       # dot clipped inside a polygon
    def hexa(cx, cy, r, fill, fn=U): poly([(cx + r * math.cos(a), cy + r * math.sin(a)) for a in [i * math.pi / 3 + math.pi / 6 for i in range(6)]], fill, fn)
    def limb(p0, p1, p2, r0, r1, r2, fill):
        """two-segment limb as ONE polygon with sharp mitred joint"""
        d1 = _vnorm(_vsub(p1, p0)); d2 = _vnorm(_vsub(p2, p1)); n1 = _perp(d1); n2 = _perp(d2)
        polyw([_mad(p0, n1, r0 * s), _miter(p0, p1, p2, r1 * s, 1), _mad(p2, n2, r2 * s), _mad(p2, n2, -r2 * s), _miter(p0, p1, p2, r1 * s, -1), _mad(p0, n1, -r0 * s)], fill)
    def band(p1, p2, t, r, col, w=5):
        d = _vnorm(_vsub(p2, p1)); n = _perp(d); cpt = (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
        a = _mad(cpt, d, -w * s / 2); b = _mad(cpt, d, w * s / 2)
        polyw([_mad(a, n, r * s), _mad(b, n, r * s), _mad(b, n, -r * s), _mad(a, n, -r * s)], col)
    def beads(p1, p2, t, r, col, n=4):
        d = _vnorm(_vsub(p2, p1)); nn = _perp(d); cpt = (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
        for i in range(n):
            k = (i - (n - 1) / 2) / ((n - 1) / 2) * 0.8
            q = _mad(cpt, nn, r * s * k); c.ell(q[0], q[1], 2.3 * s, 2.3 * s, col, None, 0, par)
    def hand(h, d, side, fill, fist=False, k=1.0):
        """small angular palm + four finger blades + thumb along world direction d (unit); k scales the hand"""
        s = g_s * k
        n = _perp(d); pe = _mad(h, d, 8 * s)
        polyw([_mad(h, n, 6.5 * s), _mad(pe, n, 5.5 * s), _mad(pe, n, -5.5 * s), _mad(h, n, -6.5 * s)], fill)
        fl = 4 if fist else 13
        for k, L in zip((-1.5, -0.5, 0.5, 1.5), (0.8, 1.0, 1.0, 0.86)):
            b = _mad(pe, n, k * 2.8 * s); t = _mad(b, d, fl * L * s)
            polyw([_mad(b, n, 1.4 * s), _mad(t, n, 0.8 * s), _mad(t, n, -0.8 * s), _mad(b, n, -1.4 * s)], fill)
        if not fist:
            for k in (-1, 0, 1): b = _mad(pe, n, k * 2.8 * s); c.line([b, _mad(b, d, fl * 0.7 * s)], shade(fill, 0.72), 0.7 * s, par)     # finger separations
        tb = _mad(_mad(h, n, side * 6.5 * s), d, 1 * s); tt = _mad(_mad(tb, n, side * 4 * s), d, 6.5 * s)
        polyw([_mad(tb, d, -1.5 * s), tt, _mad(tb, d, 4 * s)], fill)
    def rlimb(p0, p1, p2, r0, r1, r2, fill):
        """two capsule segments with a round joint (smooth organic limb)"""
        c.cap(p0, p1, r0 * s, r1 * s, fill, None, 0, par); c.cap(p1, p2, r1 * s, r2 * s, fill, None, 0, par)
    def rband(p1, p2, t, r, col, w=6):
        """ring around a capsule limb at parameter t"""
        d = _vnorm(_vsub(p2, p1)); cpt = (p1[0] + (p2[0] - p1[0]) * t, p1[1] + (p2[1] - p1[1]) * t)
        c.cap(_mad(cpt, d, -w * s / 2), _mad(cpt, d, w * s / 2), r * s, r * s, col, None, 0, par)
    def rfoot(ank, fwd, fill):
        """rounded foot pointing in world direction fwd (+-1)"""
        c.cap((ank[0] - fwd * 4 * s, ank[1] + 4 * s), (ank[0] + fwd * 22 * s, ank[1] + 5 * s), 6 * s, 4.5 * s, fill, None, 0, par)
    g_s = s
    def foot(ank, fwd, fill):
        """flat wedge foot pointing in world direction fwd (+-1)"""
        polyw([(ank[0] - fwd * 8 * s, ank[1] + 1 * s), (ank[0] + fwd * 28 * s, ank[1] + 7 * s), (ank[0] + fwd * 4 * s, ank[1] + 9 * s), (ank[0] - fwd * 10 * s, ank[1] + 8 * s)], fill)
    sw = math.sin(p['bob'] * 0.9) * 5 - 10
    return dict(o=o, p=p, s=s, sx=sx, lean=lean, Wd=Wd, U=U, poly=poly, polyw=polyw, ell=ell, dot=dot, hexa=hexa, limb=limb, band=band, beads=beads, hand=hand, foot=foot, sw=sw, rlimb=rlimb, rband=rband, rfoot=rfoot, cdot=cdot,
                sk=o['skin'], skd=shade(o['skin'], 0.84), hair=o['hair'], bead=o.get('bead') or BEAD, jew=o['jewel'], cr=o['crown'], fem=bool(o.get('female')), hk=1.22 if child else 1.0)

def draw_char(c, x, y, s=1.0, o="karna", p=None, flip=False, par=1.0):
    """flat-colour angular 'graphic-novel' rig: ~7-head figure, straight edges, smooth solid limbs, broad chest, big almond eye.
    Men are drawn in profile (facing +x, `flip` turns them), women frontal; pose key view="front"/"side" overrides.
    Local units: feet at (0,0), head top ~ -432, top-knot ~ -452 (at s=1)."""
    g = _prep(c, x, y, s, o, p, flip, par)
    v = (g['p'].get('view') or VIEW)
    if v == "auto": v = "front" if g['fem'] else "side"
    (_draw_front if v == "front" else _draw_side)(c, g, par)

PLANTED = ("trident", "staff", "spear", "bow", "bow_tall")                                                                                # tall props a seated figure rests on the ground and grips instead of waving about
GRIP = "__grip__"                                                                                                                          # hand closes round a pole that is drawn separately (planted prop)
PLANT_Y = -200                                                                                                                             # local y of a planted pole's anchor: foot on the ground, top ~ -550 (below the title band)
FAR_SH = (-42, -366)                                                                                                                       # profile rig: far shoulder at the top back corner of the chest; its deltoid cap peeks over the back shoulder and the upper arm emerges from the back edge
NEAR_SH = (56, -370)                                                                                                                       # near shoulder pivot = the chest's top FRONT corner (deltoid cap sits half over the edge); the near arm hangs down the chest front
RAISE_SHIFT = 0.0                                                                                                                          # extra forward roll of a raised near shoulder (units per degree past 110); not needed now the pivot is already at the front corner
FAR_REST_BACK = 14                                                                                                                         # degrees a resting far arm hangs behind its own pose angle, so the hand shows behind the dhoti (never hidden: both arms always read)
FAR_LAP = (-6, 55)                                                                                                                         # seated two-hand poses: the far arm drops behind the back and its forearm rests on the lap under the near elbow
ANJALI_FAR = (28, 10)                                                                                                                      # pressed palms: the far arm is a darker twin pivoted this far behind/below the near shoulder, drawn over the chest
POLE_HELD = ("trident", "staff", "spear", "flag", "bow")                                                                                        # upright poles a standing figure holds a little forward, so the shaft does not run through the face
ARM_EDGE = 0                                                                                                                               # contour width (units) around an arm drawn over the torso; 0 = none (owner prefers flat colour, arms now hang from the chest corners)
def planted_prop(p):
    """prop kind to draw standing behind a cross-legged figure (so a meditating Shiva's trishul never floats off to his knee)"""
    h = p.get('hold')
    if p.get('seat') == 'lotus' and isinstance(h, str) and h.strip().lower() in PLANTED: return h.strip().lower()
    return None

def _legs_seated(c, g, par, side_view, seat):
    """folded legs + draped dhoti for sit / meditate / kneel. Everything is placed in final local units (feet of a standing figure at y=0),
    so the hips really sit `bob` lower and the feet still touch the ground."""
    o, p, s, sx, Wd, poly, limb, band, foot, sk, jew = (g[k] for k in ("o", "p", "s", "sx", "Wd", "poly", "limb", "band", "foot", "sk", "jew"))
    rlimb, rfoot = g['rlimb'], g['rfoot']
    fem = g['fem']; bob = p['bob']; hy = (-236 if side_view else HIP - 2) + bob
    b, b2 = o['bottom'], o['bottom2']
    def leg(i, hip, knee, ankle, fwd=None):
        side = -1 if i == 0 else 1
        hip, knee, ankle = Wd(*hip), Wd(*knee), Wd(*ankle)
        if side_view:
            fill = sk if i == 1 else shade(sk, 0.9)
            rlimb(hip, knee, ankle, 20, 12.5, 7, fill)
            if fwd is not None: rfoot(ankle, fwd * sx, fill)
        elif fem:
            rlimb(hip, knee, ankle, 12, 8.5, 6, sk)
            if fwd is not None: rfoot(ankle, fwd * sx, sk)
        else:
            limb(hip, knee, ankle, 18, 13, 9, sk)
            if fwd is not None: foot(ankle, fwd * sx, shade(sk, 0.92))
        if fwd is not None: band(knee, ankle, 0.9, 10 if side_view else 7.5, jew, 3.5)
    def drape(pts, panel=None):
        poly(smooth(pts), b, Wd)
        if panel: poly(smooth(panel), b2, Wd)
    if side_view:
        if seat == "seat":
            leg(0, (-14, hy), (104, hy - 2), (104, -12), 1); leg(1, (14, hy), (122, hy + 2), (124, -12), 1)
            drape([(-50, hy - 6, 'k'), (50, hy - 6, 'k'), (126, hy - 4), (134, hy + 18), (118, hy + 54), (90, hy + 56), (60, hy + 44), (-40, hy + 50), (-52, hy + 24)], [(-6, hy - 6, 'k'), (10, hy - 6, 'k'), (40, hy + 48), (16, hy + 46)])
        elif seat == "lotus":
            leg(0, (-14, hy), (96, hy + 4), (6, hy + 10)); leg(1, (14, hy), (112, hy + 6), (26, hy + 12))
            drape([(-50, hy - 6, 'k'), (50, hy - 6, 'k'), (124, hy), (132, hy + 24), (100, hy + 34, 'k'), (-30, hy + 34, 'k'), (-50, hy + 20)], [(-6, hy - 6, 'k'), (10, hy - 6, 'k'), (30, hy + 30), (6, hy + 30)])
            rfoot(Wd(64, hy - 10), sx, sk)                                                                                                   # foot resting on top of the near thigh
        else:
            leg(0, (-14, hy), (-30, -8), (-130, -6), -1); leg(1, (14, hy), (130, hy + 2), (132, -12), 1)
            drape([(-50, hy - 6, 'k'), (50, hy - 6, 'k'), (128, hy - 4), (136, hy + 20), (120, hy + 52), (92, hy + 58), (60, hy + 52), (10, hy + 88), (-24, hy + 94), (-46, hy + 58)], [(-6, hy - 6, 'k'), (10, hy - 6, 'k'), (40, hy + 50), (16, hy + 52)])
        return
    if seat == "seat":
        for i, side in ((0, -1), (1, 1)): leg(i, (side * 13, hy), (side * 34, hy + 22), (side * 36, -12), side)
        drape([(-28, hy - 14, 'k'), (28, hy - 14, 'k'), (62, hy + 8), (66, hy + 38), (52, hy + 68, 'k'), (-52, hy + 68, 'k'), (-66, hy + 38), (-62, hy + 8)], [(-10, hy - 14, 'k'), (8, hy - 14, 'k'), (14, hy + 66), (-12, hy + 66)])
    elif seat == "lotus":
        for i, side in ((0, -1), (1, 1)): leg(i, (side * 13, hy), (side * 108, hy + 8), (-side * 16, hy + 14))
        drape([(-28, hy - 28, 'k'), (28, hy - 28, 'k'), (116, hy), (126, hy + 24, 'k'), (-126, hy + 24, 'k'), (-116, hy)], [(-10, hy - 28, 'k'), (8, hy - 28, 'k'), (16, hy + 22), (-14, hy + 22)])
        for side in (-1, 1): rfoot(Wd(-side * 34, hy - 6), -sx * side, sk)                                                                  # feet resting on the opposite thighs
    else:
        for i, side in ((0, -1), (1, 1)): leg(i, (side * 13, hy), (side * 16, hy + 50), (side * 18, -14))
        drape([(-30, hy - 6, 'k'), (30, hy - 6, 'k'), (56, hy + 18), (60, hy + 78, 'k'), (-60, hy + 78, 'k'), (-56, hy + 18)], [(-10, hy - 6, 'k'), (8, hy - 6, 'k'), (14, hy + 76), (-12, hy + 76)])

def _legs_dhoti(c, g, par, side_view):
    o, p, s, sx, Wd, poly, limb, band, foot, sk, skd, jew, sw = (g[k] for k in ("o", "p", "s", "sx", "Wd", "poly", "limb", "band", "foot", "sk", "skd", "jew", "sw"))
    fem = g['fem']
    if p.get('seat') in SEAT_BOB: return _legs_seated(c, g, par, side_view, p['seat'])
    lg = p['legs']
    if side_view and lg[0] == 0 and lg[1] == 0: lg = (-9, 11)                                                                            # default profile stance: back leg back, front leg forward
    for i, ang in ((0, lg[0]), (1, lg[1])):
        side = -1 if i == 0 else 1
        a = math.radians(ang)
        if side_view:
            # smooth capsule legs; swing (ang) rotates the whole leg about the hip toward +x
            fill = sk if i == 1 else shade(sk, 0.9)
            hip = Wd(side * 14, -236)
            vx, vy = sx * side * 12 * s, 118 * s
            knee = (hip[0] + vx * math.cos(a) + vy * math.sin(a) * sx, hip[1] + vy * math.cos(a) - vx * math.sin(a) * sx)
            a2 = a * 0.55; ux_, uy_ = -sx * side * 2 * s, 106 * s
            ank = (knee[0] + ux_ * math.cos(a2) + uy_ * math.sin(a2) * sx, knee[1] + uy_ * math.cos(a2) - ux_ * math.sin(a2) * sx)
            g['rlimb'](hip, knee, ank, 20, 12.5, 7, fill)
            g['rfoot'](ank, sx, fill)
            band(knee, ank, 0.9, 10, jew, 3.5)
            continue
        fill = sk
        hip = Wd(side * (13 if fem else 14), HIP - 2)
        fx = side
        knee = (hip[0] + sx * fx * math.sin(a) * 112 * s, hip[1] + math.cos(a) * 112 * s)
        a2 = a * 0.55; ank = (knee[0] + sx * fx * math.sin(a2) * 106 * s, knee[1] + math.cos(a2) * 106 * s)
        if fem:
            g['rlimb'](hip, knee, ank, 12, 8.5, 6, fill); g['rfoot'](ank, sx * side, fill); band(knee, ank, 0.9, 7.5, jew, 3.5); continue
        limb(hip, knee, ank, 18, 13, 9, fill)
        foot(ank, sx * side, shade(fill, 0.92))
        band(knee, ank, 0.9, 7.5, jew, 3.5)
    short = o.get('dhoti') == 'short'; hem = -104 if short else -66
    b, b2 = o['bottom'], o['bottom2']
    if side_view:
        w = 58 if short else 76
        poly(smooth([(-50, -242, 'k'), (50, -242, 'k'), (56, -200), (w, hem, 'k'), (-w, hem, 'k'), (-56, -200)]), b, Wd)                     # soft A-line wrap
        for q in (-38, -26, -14, -4, 10, 20, 32): c.line([Wd(q, -236), Wd(q * 1.5 - 2, (hem - 236) / 2), Wd(q * 2.2, hem + 2)], shade(b, 0.9), 1.8 * s, par)   # pleat lines
        poly(smooth([(-6, -242, 'k'), (10, -242, 'k'), (22, hem, 'k'), (-14, hem, 'k')]), b2, Wd)                                              # centre panel
    elif fem:
        w1 = 60
        poly(smooth([(-28, -254, 'k'), (28, -254, 'k'), (72, -198), (76, -148), (w1, hem, 'k'), (-w1, hem, 'k'), (-76, -148), (-72, -198)]), b, Wd)                     # wide hip curve
        poly(smooth([(-10, -252, 'k'), (8, -252, 'k'), (16, hem, 'k'), (-12, hem, 'k')]), b2, Wd)                                               # green pleats
        for q in (-22, 24): c.line([Wd(q, -246), Wd(q * 1.7, (hem - 246) / 2), Wd(q * 2.4, hem + 2)], shade(b, 0.88), 2 * s, par)         # fold lines
    else:
        w1 = 52 if short else 66
        poly([(-30, -240), (30, -240), (w1, hem), (-w1, hem)], b, Wd)
        poly([(9, -240), (30, -240), (w1, hem), (18, hem)], shade(b, 0.86), Wd)
        poly([(-5, -240), (5, -240), (10, hem), (-10, hem)], b2, Wd)
        poly([(-5, -240), (-2.5, -240), (-7, hem), (-10, hem)], shade(b2, 0.76), Wd)

def _arm_dir(a, lean, sx):
    def Dv(v): return (sx * (v[0] * math.cos(lean) - v[1] * math.sin(lean)), v[0] * math.sin(lean) + v[1] * math.cos(lean))
    return Dv((math.sin(a), math.cos(a)))

def _halo_aura(c, g, par, hx, hy=HC):
    o, p, s, U = g['o'], g['p'], g['s'], g['U']
    if o['aura'] and p['aura'] > 0: c.glow(*U(0, -300), 340 * s, o['aura'], 0.5 * p['aura'], par)
    if o['halo']:
        x_, y_ = U(hx, hy); c.glow(x_, y_, 170 * s, o['halo'], 0.4, par); c.arc(x_, y_, 74 * s, 74 * s, 0, 360, shade(o['halo'], 0.92), 4 * s, par)

def _necklaces(c, g, par, cx, hw, y0):
    """tight bead choker + long bead loop across the chest"""
    s, U, bead, jew = g['s'], g['U'], g['bead'], g['jew']
    for j, (rx, ry, n, col) in enumerate(((hw, 16, 9, bead), (hw * 0.92, 58, 13, bead), (hw * 0.6, 34, 7, jew))):
        if j == 2 and not g['o'].get('kundal') and not g['fem']: continue
        for k in range(n):
            a = math.radians(14 + 152 * k / (n - 1))
            q = U(cx + rx * math.cos(a), y0 + ry * math.sin(a)); c.ell(q[0], q[1], 3 * s, 3 * s, col, None, 0, par)
    if g['fem']:
        for k in range(11):
            a = math.radians(14 + 152 * k / 10); q = U(cx + hw * 0.78 * math.cos(a), y0 + 40 * math.sin(a)); c.ell(q[0], q[1], 2.4 * s, 2.4 * s, bead, None, 0, par)
    if g['fem'] or g['o'].get('kundal'): hexa_ = g['hexa']; hexa_(cx, y0 + 58, 5, jew)

# ============================================================ frontal rig ============================================================
def _draw_front(c, g, par):
    o, p, s, sx, lean, Wd, U, poly, polyw, ell, dot, hexa, limb, band, beads, hand, sw = (g[k] for k in ("o", "p", "s", "sx", "lean", "Wd", "U", "poly", "polyw", "ell", "dot", "hexa", "limb", "band", "beads", "hand", "sw"))
    sk, skd, hair, bead, jew, cr, fem = (g[k] for k in ("sk", "skd", "hair", "bead", "jew", "cr", "fem"))
    top = o['top']
    c.shadow(*Wd(0, 4), 80 * s, 12 * s, 0.3, par=par)
    _halo_aura(c, g, par, 0)
    if o.get('veil'):
        poly(smooth([(0, -456), (-32, -448), (-46, -410), (-54, -350), (-54, -300), (-50, -262, 'k'), (50, -262, 'k'), (54, -300), (54, -350), (46, -410), (32, -448)]), o['veil'])   # dupatta behind
    elif fem or o.get('longhair'):
        poly(smooth([(-24, -420), (24, -420), (44, -368), (50 + sw * 0.5, -330), (46 + sw, -292, 'k'), (-46 + sw, -292, 'k'), (-50 + sw * 0.5, -330), (-44, -368)]), hair)   # hair ends at the shoulder blades (waist-long strips beside the torso read as extra arms)
    if o.get('monkey'):
        tw = math.sin(f_tail(p)) * 18
        polyw([Wd(-16, -100), Wd(-24, -90), Wd(-100, -150 + tw), Wd(-128, -300 + tw * 2), Wd(-84, -366), Wd(-78, -354), Wd(-114, -300 + tw * 2), Wd(-90, -160 + tw)], hair)
    if o.get('heads', 1) > 1:
        for i in range(int(o['heads']) - 1):
            sd = -1 if i % 2 == 0 else 1; k = i // 2 + 1
            hx, hy = sd * 40 * k, HC - 6 + 8 * k
            poly([(hx - 20, hy - 22), (hx - 20, hy + 4), (hx - 8, hy + 24), (hx, hy + 28), (hx + 8, hy + 24), (hx + 20, hy + 4), (hx + 20, hy - 22), (hx, hy - 30)], sk)
            poly([(hx - 22, hy - 20), (hx - 16, hy - 48), (hx - 6, hy - 32), (hx, hy - 56), (hx + 6, hy - 32), (hx + 16, hy - 48), (hx + 22, hy - 20)], o['crownc'])
            for e in (-1, 1):
                poly([(hx + e * 3, hy - 4), (hx + e * 8, hy - 9), (hx + e * 15, hy - 4), (hx + e * 8, hy)], o['eye']); dot(hx + e * 9, hy - 4, 2.6, PUPIL)
            poly([(hx - 5, hy + 12), (hx + 5, hy + 12), (hx + 3, hy + 15), (hx - 3, hy + 15)], MOUTH)
    plant = planted_prop(p); floor_y = Wd(0, 0)[1]
    if plant:
        shx0 = 42 if fem else 48; a1 = math.radians(p['armR'][0]); a2 = math.radians(sum(p['armR']))
        hx = U(shx0, -330)[0] + _arm_dir(a1, lean, sx)[0] * 78 * s + _arm_dir(a2, lean, sx)[0] * 72 * s
        prop(plant, (hx, Wd(0, PLANT_Y)[1]), (0.0, -1.0), s, c, par, sx, floor=floor_y)                                                     # pole rises from the ground through the resting near hand
    _legs_dhoti(c, g, par, False)
    if fem:
        chest = smooth([(-48, -322), (-40, -340), (0, -346), (40, -340), (48, -322), (40, -298), (20, -272), (26, -248, 'k'), (-26, -248, 'k'), (-20, -272), (-40, -298)]); shx = 42
        c.line([U(-26, -328), U(0, -322), U(26, -328)], shade(sk, 0.74), 1.3 * s, par)                                                      # collarbone
        poly(smooth([(-8.6, -376.6, 'k'), (8.6, -376.6, 'k'), (10.5, -334), (-10.5, -334)]), shade(sk, 0.94))                                             # neck
    else:
        chest = [(-54, -324), (-56, -334), (-44, -342), (44, -342), (56, -334), (54, -324), (46, -290), (24, -246), (-24, -246), (-46, -290)]; shx = 48
    poly(chest, sk)
    if fem:
        if top:
            poly(smooth([(-48, -326), (-40, -342), (-18, -344, 'k'), (0, -328, 'k'), (18, -344, 'k'), (40, -342), (48, -326), (42, -300), (32, -286, 'k'), (0, -290), (-32, -286, 'k'), (-42, -300)]), top)   # blouse, sweetheart neck
            for sd in (-1, 1): poly(smooth([(sd * 4, -318), (sd * 34, -324), (sd * 38, -300), (sd * 20, -290), (sd * 4, -296)]), shade(top, 0.9))                                             # bust
            c.line([U(-32, -287), U(0, -291), U(32, -287)], o['top2'], 2.2 * s, par); c.line([U(-18, -344), U(0, -328), U(18, -344)], o['top2'], 2.2 * s, par)                              # gold trim
        else:
            for sd in (-1, 1): poly(smooth([(sd * 4, -318), (sd * 30, -324), (sd * 34, -300), (sd * 18, -290), (sd * 4, -296)]), shade(sk, 0.9))
    elif top:
        poly([(-54, -326), (54, -326), (46, -290), (24, -246), (-24, -246), (-46, -290)], top); poly([(0, -326), (54, -326), (46, -290), (24, -246), (0, -246)], shade(top, 0.86))
        poly([(-54, -330), (-20, -330), (0, -302), (20, -330), (54, -330), (54, -322), (0, -288), (-54, -322)], o['top2'])
    else:
        poly([(0, -342), (44, -342), (46, -290), (24, -246), (0, -246)], shade(sk, 0.9))
        poly([(-36, -306), (-5, -306), (-5, -292), (-32, -292)], shade(sk, 0.86)); poly([(5, -306), (36, -306), (32, -292), (5, -292)], shade(sk, 0.86))
        if o['sash']: poly([(-50, -326), (-30, -338), (30, -250), (12, -246)], o['sash']); poly([(-50, -326), (-42, -331), (20, -248), (12, -246)], shade(o['sash'], 0.8))
    armor_on = o['armor'] if p['armor'] is None else bool(p['armor'])
    if armor_on:
        poly([(-54, -334), (54, -334), (46, -290), (24, -250), (-24, -250), (-46, -290)], GOLD)
        poly([(14, -334), (54, -334), (46, -290), (24, -250), (8, -250)], shade(GOLD, 0.88))
        for r_ in range(3):
            for i in range(-1, 2): hexa(i * 22 + (11 if r_ % 2 else 0), -316 + r_ * 24, 5, (255, 232, 140))
        hexa(0, -282, 12, (255, 244, 190)); hexa(0, -282, 6, CRIMSON)
    ww = 27 if fem else 26
    if fem: poly(smooth([(-ww - 2, -252, 'k'), (ww + 2, -252, 'k'), (ww + 1, -240, 'k'), (-ww - 1, -240, 'k')]), jew)                           # waist chain
    else: poly([(-ww - 2, -250), (ww + 2, -250), (ww + 1, -238), (-ww - 1, -238)], jew); poly([(-ww - 2, -243), (ww + 2, -243), (ww + 1, -240), (-ww - 1, -240)], shade(jew, 0.7))
    _necklaces(c, g, par, 0, 24 if not fem else 20, -336)
    def arm(side, up, bend, holdv):
        sh = U(side * shx, -330); a1 = math.radians(up); a2 = math.radians(up + bend)
        d1 = _arm_dir(a1, lean, sx * side); d2 = _arm_dir(a2, lean, sx * side)
        e = (sh[0] + d1[0] * 78 * s, sh[1] + d1[1] * 78 * s); h = (e[0] + d2[0] * 72 * s, e[1] + d2[1] * 72 * s)
        grip = holdv == GRIP
        if grip: holdv = None
        if fem:
            c.ell(*sh, 12 * s, 12 * s, sk, None, 0, par); g['rlimb'](sh, e, h, 10.5, 8, 6, sk)
            hand(h, d2, sx * side, sk, fist=bool(holdv) or grip)
            band(sh, e, 0.5, 9.5, jew, 7)
            for t_ in (0.72, 0.8, 0.88): band(e, h, t_, 7.2, jew, 3.2); band(e, h, t_ + 0.035, 7.2, shade(jew, 0.72), 1.2)
            if holdv: prop(holdv, h, d2, s, c, par, sx, floor=floor_y)
            return
        r = (15, 10.5, 6.5)
        limb(sh, e, h, r[0], r[1], r[2], sk)
        hand(h, d2, sx * side, sk, fist=bool(holdv) or grip)
        beads(sh, e, 0.48, r[1] + 1, bead, 4)
        if o.get('guards'): g['rband'](e, h, 0.62, r[2] + 1.6, INK, 44)
        else: band(e, h, 0.88, r[2] + 1, jew, 4)
        if holdv == 'sword' and o.get('talwar'): holdv = 'talwar'
        if holdv: prop(holdv, h, d2, s, c, par, sx, floor=floor_y)
    # anjali: elbows out at the ribs, forearms angled up so the palms meet at the heart (the profile rig reads the same numbers as "hands forward")
    armR, armL = (ANJALI_FRONT if p.get('anjali') and tuple(p['armR']) == NAMASTE_ARM else p['armR']), (ANJALI_FRONT if p.get('anjali') and tuple(p['armL']) == NAMASTE_ARM else p['armL'])
    arm(-1, *armL, p['holdL']); arm(1, *armR, GRIP if plant else p['hold'])
    _head_front(c, g, par)

def _Hd_fn(g, hs=HS, lift=0, rot=0):
    U, sx, s, hr = g['U'], g['sx'], g['s'], g['p']['head']; hc = (0, HC); hs = hs * g.get('hk', 1.0)
    def Hd(px, py):
        px, py = px * hs, CHIN + (py - CHIN) * hs + lift
        dx, dy = px - hc[0], py - hc[1]
        bx, by = U(*hc)
        r = math.radians(hr + rot); rx = dx * math.cos(r) - dy * math.sin(r); ry = dx * math.sin(r) + dy * math.cos(r)
        return (bx + sx * rx * s, by + ry * s)
    return Hd

def _head_front(c, g, par):
    o, p, s, sx, U, poly, ell, dot, hexa, sk, skd, hair, bead, jew, cr, fem = (g[k] for k in ("o", "p", "s", "sx", "U", "poly", "ell", "dot", "hexa", "sk", "skd", "hair", "bead", "jew", "cr", "fem"))
    Hd = _Hd_fn(g, HSF if fem else HS)
    if not fem: poly([(-9, -372), (9, -372), (10, -332), (-10, -332)], skd, U)                                                               # long thin neck
    if fem: face = smooth([(-41.9, -407.6), (-34.6, -436.7), (0, -442.1), (34.6, -436.7), (41.9, -407.6), (29.1, -383), (0, -363, 'k'), (-29.1, -383)])   # broad heart face tapering to a small V chin
    else:   face = [(-27, -420), (-29, -398), (-23, -374), (-10, -363), (0, -359), (10, -363), (23, -374), (29, -398), (27, -420), (15, -430), (0, -433), (-15, -430)]
    if fem: poly(smooth([(-43.7, -409.4), (-36.4, -440.3), (0, -445.8), (36.4, -440.3), (43.7, -409.4), (37.3, -382.1), (21.8, -367.5), (41.9, -343.9, 'k'), (7, -343.9, 'k'), (7, -366, 'k'), (-7, -366, 'k'), (-7, -343.9, 'k'), (-41.9, -343.9, 'k'), (-21.8, -367.5), (-37.3, -382.1)]), hair, Hd)        # hair curving in around the jaw then sweeping out behind the shoulders
    poly(face, sk, Hd)
    for sd in (-1, 1): poly([(sd * (25 if not fem else 34), -406 if not fem else -410), (sd * (31 if not fem else 41), -403 if not fem else -407), (sd * (31 if not fem else 40), -388 if not fem else -393), (sd * (25 if not fem else 33), -390 if not fem else -395)], sk, Hd)                                    # ears
    if o.get('monkey'): poly([(-16, -386), (16, -386), (12, -370), (-12, -370)], shade(sk, 1.12), Hd); dot(0, -382, 2.8, PUPIL, Hd)
    if o['kundal']:
        for sd in (-1, 1): hexa(sd * 30, -382, 6.5, GOLD, Hd); dot(sd * 30, -382, 3, CRIMSON, Hd)
    if fem:
        hl = [(0, -442.1, 'k'), (-23, -438.5), (-41.5, -418), (-41.9, -407.6, 'k'), (-31.5, -424), (-12.7, -431.5)]
        if o.get('veil'):
            for sd in (-1, 1): poly(smooth([(sd * x, y) + tuple(k) for (x, y, *k) in hl]), hair, Hd)                                              # thin black hair band along a high arched hairline
        else: poly(smooth([(-44, -398), (-46, -426), (-28, -450), (0, -454), (28, -450), (46, -426), (44, -398), (41.9, -407.6, 'k'), (31.5, -424), (12.7, -431.5), (0, -442.1, 'k'), (-12.7, -431.5), (-31.5, -424), (-41.9, -407.6, 'k')]), hair, Hd)   # low rounded hairline, small centre parting
        if o.get('veil'):
            outer = [(-58, -346, 'k'), (-54, -392), (-46, -430), (-28, -459), (0, -466), (28, -459), (46, -430), (54, -392), (58, -346, 'k')]
            inner = [(52, -346, 'k'), (49, -394), (46, -402), (44, -408), (42, -419), (24, -440), (0, -444, 'k'), (-24, -440), (-42, -419), (-44, -408), (-46, -402), (-49, -394), (-52, -346, 'k')]
            poly(smooth(outer + inner), o['veil'], Hd)                                                                                         # translucent dupatta dome over the hair, open at the face
            c.line([Hd(0, -460), Hd(0, -444)], GOLD, 2 * s, par); poly(smooth([(0, -446, 'k'), (5.5, -437), (0, -430), (-5.5, -437)]), GOLD, Hd)   # big gold teardrop maang tikka at the brow bridge
        for sd in (-1, 1): dot(sd * 37, -396, 2.6, GOLD, Hd); c.line([Hd(sd * 37, -396), Hd(sd * 37, -386)], GOLD, 1.4 * s, par); poly(smooth([(sd * 37, -388, 'k'), (sd * 43, -376, 'k'), (sd * 31, -376, 'k')]), GOLD, Hd); dot(sd * 37, -373, 2.4, bead, Hd)
    elif cr != "turban":
        poly([(-28, -406), (-29, -422), (-18, -432), (0, -436), (18, -432), (29, -422), (28, -406), (22, -416), (10, -423), (0, -418), (-10, -423), (-22, -416)], hair, Hd)
        for sd in (-1, 1): poly([(sd * 28, -410), (sd * 33, -402), (sd * 27, -386)], hair, Hd)                                                # side blades
        if not fem and cr in ("none", "band"):
            ell(0, -448, 14, 12, hair, Hd); poly([(-9, -438), (9, -438), (8, -433), (-8, -433)], GOLD, Hd)                                      # round top-knot + gold ring
    _crown(c, g, par, Hd, 0, 0, False)
    ex, ey = (19.1, -403) if fem else (11.5, -404)
    eo = {"closed": 0.0, "shock": 1.3, "sad": 0.8, "stern": 0.7, "smile": 0.85}.get(p['expr'], 1.0)
    if p['blink']: eo = 0.0
    for sd in (-1, 1):
        cx = sd * ex; tilt = {"stern": 4, "sad": -4, "shock": -2, "smile": -1}.get(p['expr'], 0)
        _eye(c, g, par, Hd, cx, ey, sd, eo, 15.5 if fem else 12.5)
        if fem: poly(smooth([(cx - sd * 13, ey - 5.5 + tilt, 'k'), (cx, ey - 18), (cx + sd * 15, ey - 10, 'k'), (cx, ey - 15.5)]), INK, Hd)   # thin high-arched brow floating above the lash
        else: poly(smooth([(cx - sd * 10, ey - 11 + tilt, 'k'), (cx + sd * 3, ey - 18.5), (cx + sd * 16, ey - 14, 'k'), (cx + sd * 3, ey - 15.5)]), INK, Hd)   # arched brow
    if fem: poly(smooth([(-0.9, -395.7), (1.8, -383.9, 'k'), (-2.7, -383, 'k')]), shade(sk, 0.82), Hd)                                        # slim nose sliver
    else: poly([(0, -410), (2.5, -408), (4.5, -386), (0, -383), (-4.5, -386)], shade(sk, 0.86), Hd)                                           # nose wedge
    if fem and max(p['mouth'], 0.0) <= 0.05 and p['expr'] != 'shock':
        k = {"sad": -3, "stern": -2}.get(p['expr'], 0)
        poly(smooth([(-12, -375.7 - k, 'k'), (0, -369.3 - k * 0.3), (12, -375.7 - k, 'k'), (0, -373 + k * 0.5)]), MOUTH, Hd)                       # wide crescent smile
    else: _mouth(c, g, par, Hd, 0, -373 if not fem else -374, 1)
    if o['beard']: poly([(-24, -380), (-21, -368), (0, -365), (21, -368), (24, -380), (22, -362), (0, -340), (-22, -362)], o['beard'], Hd)
    if not (fem and o.get('veil')): _tilak(c, g, par, Hd, 0, -420)

def _eye(c, g, par, Hd, cx, ey, sd, eo, w):
    """big almond eye with a large black pupil; sd = direction of the outer corner (lash wedge sweeps that way)"""
    o, p, s, poly, dot, fem = (g[k] for k in ("o", "p", "s", "poly", "dot", "fem"))
    if eo < 0.12:
        poly([(cx - w, ey - 1), (cx, ey + 1.5), (cx + w, ey - 1), (cx + sd * (w + 4), ey - 4.5), (cx + w, ey + 1), (cx, ey + 3.5), (cx - w, ey + 1)], INK, Hd); return
    h = (7.5 if not fem else 12) * eo
    to = 5 if fem else 1                                                                                                                  # outer-corner lift (cat-eye for women)
    if fem:
        sclera = smooth([(cx - sd * 12.7, ey + 2, 'k'), (cx, ey - 11 * eo), (cx + sd * 13.7, ey - 3.65, 'k'), (cx, ey + 12 * eo)])          # big upward-sweeping leaf eye
        poly(sclera, o['eye'], Hd)
        g['cdot'](sclera, cx + p['gaze'] * 3, ey, min(8.0, 5 + 3 * eo), PUPIL, Hd)                                                     # iris touches both lids, white only at the corners
        poly(smooth([(cx - sd * 13.6, ey + 1, 'k'), (cx, ey - 12.75), (cx + sd * 15, ey - 4.6, 'k'), (cx, ey - 9)]), INK, Hd)            # dark upper lash line
        return
    poly([(cx - w, ey), (cx - w * 0.45, ey - h), (cx + w * 0.4, ey - h * 0.95), (cx + w, ey - to), (cx + w * 0.4, ey + h * 0.62), (cx - w * 0.45, ey + h * 0.55)], o['eye'], Hd)
    gx = cx + p['gaze'] * 3 + sd * 2
    dot(gx, ey - 0.3, min(4.6, 3 + 2.2 * eo), PUPIL, Hd)
    poly([(cx - w, ey), (cx - w * 0.45, ey - h), (cx + w * 0.4, ey - h * 0.95), (cx + w, ey - to), (cx + sd * (w + 4.5), ey - 4 - to), (cx + w * 0.4, ey - h * 0.95 - 2.6), (cx - w * 0.45, ey - h - 2), (cx - w - 0.8, ey - 1.5)], INK, Hd)
    if fem: poly([(cx + sd * w, ey + 0.8), (cx + sd * (w + 5), ey - 3), (cx + sd * (w + 5), ey - 1.5), (cx + sd * w, ey + 2.4)], INK, Hd)

def _mouth(c, g, par, Hd, mx, my, fwd):
    o, p, s, poly, hair, fem = (g[k] for k in ("o", "p", "s", "poly", "hair", "fem"))
    m = max(p['mouth'], 0.0); lipl = (216, 104, 122) if fem else shade(MOUTH, 1.4)
    w = 6.5 if fwd == 1 else 3.5
    if m > 0.05 or p['expr'] == "shock":
        hh = 2 + 4 * max(m, 0.4 if p['expr'] == 'shock' else 0)
        poly([(mx - w, my - 1.5), (mx, my - 2.5), (mx + w, my - 1.5), (mx + w * 0.6, my + hh), (mx - w * 0.6, my + hh)], PUPIL, Hd)
        poly([(mx - w, my - 1.5), (mx - 2, my - 3), (mx + 2, my - 3), (mx + w, my - 1.5), (mx, my - 0.3)], MOUTH, Hd)
    else:
        k = {"smile": 2, "sad": -2}.get(p['expr'], 0)
        poly([(mx - w, my - 1 - k), (mx - 2, my - 3), (mx + 2, my - 3), (mx + w, my - 1 - k), (mx, my + 0.3)], MOUTH, Hd)
        poly([(mx - w, my - 1 - k), (mx, my + 0.3), (mx + w, my - 1 - k), (mx + 2, my + 3 + k * 0.5), (mx - 2, my + 3 + k * 0.5)], lipl, Hd)
    if o['mous']:
        if fwd == 1: poly([(-14, my - 4), (-1, my - 7), (-1, my - 4), (-11, my - 1)], hair, Hd); poly([(14, my - 4), (1, my - 7), (1, my - 4), (11, my - 1)], hair, Hd)
        else: poly([(mx + 4, my - 5), (mx - 12, my - 8), (mx - 10, my - 4), (mx + 3, my - 1.5)], hair, Hd)
    if o.get('fangs'):
        for sd in ((-1, 1) if fwd == 1 else (1,)): poly([(mx + sd * 3, my - 1), (mx + sd * 6, my - 1), (mx + sd * 4.5, my + 6)], (255, 255, 240), Hd)

def _tilak(c, g, par, Hd, tx, ty):
    o, s, poly, dot = (g[k] for k in ("o", "s", "poly", "dot")); t = o['tilak']
    if t == "u": poly([(tx - 3.5, ty - 6), (tx - 1.5, ty - 6), (tx, ty + 0.5), (tx + 1.5, ty - 6), (tx + 3.5, ty - 6), (tx, ty + 3.5)], CRIMSON, Hd)
    elif t == "three":
        for dy in (-5, -1.5, 2): poly([(tx - 7, ty + dy), (tx + 7, ty + dy), (tx + 7, ty + dy + 1.5), (tx - 7, ty + dy + 1.5)], (250, 248, 240), Hd)
        poly([(tx - 1.5, ty - 6), (tx + 1.5, ty - 6), (tx + 1.5, ty + 3), (tx - 1.5, ty + 3)], CRIMSON, Hd)
    elif t == "dot": dot(tx, ty, 3, CRIMSON, Hd)

def _crown(c, g, par, Hd, cx, dy, side):
    """headgear at the hairline (cx, -420+dy). side=True draws the profile version (facing +x)."""
    o, s, poly, ell, dot, hexa, hair, bead, cr = (g[k] for k in ("o", "s", "poly", "ell", "dot", "hexa", "hair", "bead", "cr"))
    y0 = -420 + dy
    if cr == "mukut":
        if side: poly([(cx - 16, y0 - 6), (cx + 22, y0 - 4), (cx + 25, y0 - 38), (cx + 13, y0 - 27), (cx + 4, y0 - 52), (cx - 4, y0 - 27), (cx - 16, y0 - 36)], o['crownc'], Hd)
        else: poly([(cx - 27, y0 - 7), (cx - 23, y0 - 42), (cx - 12, y0 - 30), (cx, y0 - 60), (cx + 12, y0 - 30), (cx + 23, y0 - 42), (cx + 27, y0 - 7)], o['crownc'], Hd)
        poly([(cx - 29, y0 - 10), (cx + 29, y0 - 10), (cx + 28, y0 - 1), (cx - 28, y0 - 1)], shade(o['crownc'], 0.9), Hd)
        for q in ((-15, 0, 15) if not side else (-10, 7, 22)): hexa(cx + q, y0 - 5.5, 3, CRIMSON if q else (60, 200, 190), Hd)
    elif cr == "band":
        poly([(cx - 29, y0 - 10), (cx + 29, y0 - 10), (cx + 28, y0 - 2), (cx - 28, y0 - 2)], GOLD, Hd); hexa(cx + (0 if not side else 16), y0 - 6, 3.4, CRIMSON, Hd)
    elif cr == "jata":
        if side: poly([(cx - 18, y0 - 9), (cx + 8, y0 - 9), (cx + 6, y0 - 36), (cx - 2, y0 - 47), (cx - 12, y0 - 38), (cx - 18, y0 - 22)], hair, Hd)
        else: poly([(cx - 14, y0 - 12), (cx + 14, y0 - 12), (cx + 12, y0 - 48), (cx + 8, y0 - 58), (cx - 8, y0 - 58), (cx - 12, y0 - 48)], hair, Hd)
        for q in range(-3, 4): dot(cx + q * 8, y0 - 10, 2.4, bead, Hd)
        if o.get('moon'):
            mx, my_ = cx - 24, y0 - 40; R = 11
            outer = [(mx + R * math.cos(math.radians(a)), my_ + R * math.sin(math.radians(a))) for a in range(60, 301, 15)]
            inner = [(mx + 6 + R * math.cos(math.radians(a)), my_ + R * math.sin(math.radians(a))) for a in range(300, 59, -15)]
            poly(outer + inner, (250, 248, 240), Hd)
    elif cr == "turban":
        if side:
            poly([(cx - 52, y0 - 4), (cx - 48, y0 - 26), (cx - 22, y0 - 38), (cx + 14, y0 - 36), (cx + 30, y0 - 20), (cx + 32, y0 - 4)], o['crownc'], Hd)
            poly([(cx - 52, y0 - 4), (cx + 32, y0 - 4), (cx + 30, y0 + 3), (cx - 50, y0 + 3)], shade(o['crownc'], 0.8), Hd)
        else:
            poly([(cx - 34, y0 - 6), (cx - 30, y0 - 26), (cx - 10, y0 - 35), (cx + 15, y0 - 33), (cx + 32, y0 - 22), (cx + 34, y0 - 6)], o['crownc'], Hd)
            poly([(cx - 32, y0 - 6), (cx + 32, y0 - 6), (cx + 30, y0 + 1), (cx - 30, y0 + 1)], shade(o['crownc'], 0.8), Hd)
        for q in (-15, 0, 15): poly([(cx + q - 6, y0 - 26), (cx + q - 4, y0 - 27), (cx + q + 9, y0 - 6), (cx + q + 7, y0 - 5)], shade(o['crownc'], 0.7), Hd)
    elif g['fem'] and not o.get('veil'):
        for q in range(-3, 4): dot(cx + q * 7, y0 - 8, 2, bead, Hd)

# ============================================================ profile rig ============================================================
def _draw_side(c, g, par):
    """facing +x (flip turns around). Far arm/leg drawn first in a darker tone, near ones on top."""
    o, p, s, sx, lean, Wd, U, poly, polyw, ell, dot, hexa, limb, band, beads, hand, sw = (g[k] for k in ("o", "p", "s", "sx", "lean", "Wd", "U", "poly", "polyw", "ell", "dot", "hexa", "limb", "band", "beads", "hand", "sw"))
    sk, skd, hair, bead, jew, cr, fem = (g[k] for k in ("sk", "skd", "hair", "bead", "jew", "cr", "fem"))
    top = o['top']; skf = shade(sk, 0.9)
    def far_active(up, bend): return (up > 25 or abs(bend) > 30) and not p.get('anjali')                                                   # far arm is "in use" (not a resting hang / walk swing / pressed palms)
    plant = planted_prop(p)
    hk = p['hold'].strip().lower() if isinstance(p['hold'], str) else None
    if hk in POLE_HELD and not plant and not far_active(*p['armR']): p = dict(p, armR=(26, -26))                                          # standing with an upright pole: hold it at arm's length ahead so the shaft and prongs clear the face
    c.shadow(*Wd(4, 4), 70 * s, 12 * s, 0.3, par=par)
    _halo_aura(c, g, par, -4, -448)
    rlimb, rband = g['rlimb'], g['rband']
    if fem or o.get('longhair'):
        poly(smooth([(-30, -440), (-10, -450), (-26, -380), (-34, -330), (-40 + sw, -260), (-20 + sw * 1.6, -230, 'k'), (-10 + sw, -270), (-16, -330), (-22, -380)]), hair)
    if o.get('monkey'):
        tw = math.sin(f_tail(p)) * 18
        pts = [Wd(-22, -96), Wd(-104, -150 + tw), Wd(-132, -300 + tw * 2), Wd(-88, -366)]
        for q0, q1 in zip(pts, pts[1:]): c.cap(q0, q1, 7 * s, 7 * s, hair, None, 0, par)
    if o.get('heads', 1) > 1:
        for i in range(int(o['heads']) - 1):
            k = i + 1; hx, hy = -28 * k, HC - 28 + 5 * k
            poly(smooth([(hx - 16, hy - 24), (hx - 18, hy + 4), (hx - 6, hy + 24), (hx + 4, hy + 26), (hx + 16, hy + 4), (hx + 16, hy - 24), (hx, hy - 32)]), shade(sk, 0.86))
            poly([(hx - 16, hy - 22), (hx - 10, hy - 46), (hx - 3, hy - 32), (hx + 4, hy - 54), (hx + 10, hy - 32), (hx + 16, hy - 22)], shade(o['crownc'], 0.9))
            ell(hx + 7, hy - 5, 6, 3.5, o['eye']); dot(hx + 8, hy - 5, 2.4, PUPIL)
    def far_angles(up, bend):
        """far-arm pose derived from its own angles + the near arm's, so in every pose the far arm reads shoulder -> elbow -> hand: at rest it
        hangs behind the back; in a two-hand pose it is offset from the near arm (never stacked behind it); akimbo puts the elbow out behind."""
        nu, nb = p['armR']
        stacks = abs(up - nu) < 30 and abs(bend - nb) < 30                                                                                # both arms strike the same pose -> the far hand would land exactly behind the near one
        if bend < -50 and up > 0: return -up * 0.75, -bend * 0.94                                                                          # hand on hip: far elbow juts out behind the back, hand on the back of the hip
        if stacks:
            if p.get('seat'): return FAR_LAP                                                                                                # seated: far forearm rests on the lap, elbow showing behind the back
            if up >= 110: return 195, -40                                                                                                  # both raised: far arm rises behind the back edge (a sliver of upper arm shows behind the hair), hand above the head
            if up > 15: return up + 20, max(bend - 20, 0)                                                                                   # both forward: far arm reaches out above the near one from the chest front edge
            return up - 12, bend                                                                                                            # both hanging bent (bow): far a little behind
        if not far_active(up, bend):
            t = max(0.0, min((up - nu) / 24.0, 1.0))                                                                                        # counter-swing (walk): as the far arm swings ahead of the near one it blends from hanging behind the back to reaching
            return up - FAR_REST_BACK + t * (FAR_REST_BACK + 22), bend + t * 22                                                             # forward past the belly, so the two hands never sit side by side on one hip
        if 0 <= up < 20 and bend > 30: return up + 12, bend                                                                                 # reaching across the body (folded arms): hand clears the torso front
        return up, bend
    def arm_pts(up, bend, side):
        # near arm hangs from the middle of the torso and is drawn over it; a raised near arm rolls its shoulder forward so it clears the face.
        # far arm hangs from the top back corner of the chest and is drawn under the body (see far_angles). Anjali (pressed palms) instead puts
        # the far arm just behind the near one, in front of the chest, drawn over the torso.
        shx, shy = NEAR_SH
        if side > 0: shx += max(0.0, min(up - 110.0, 60.0)) * RAISE_SHIFT
        elif p.get('anjali'): shx, shy = NEAR_SH[0] - ANJALI_FAR[0], NEAR_SH[1] + ANJALI_FAR[1]
        else: (shx, shy), (up, bend) = FAR_SH, far_angles(up, bend)
        shp = U(shx, shy)
        bend_in = bend > 150; fwd = -1 if bend_in else 1
        a1 = math.radians(up); a2 = math.radians(up + bend)
        d1 = _arm_dir(a1, lean, sx * fwd); d2 = _arm_dir(a2, lean, sx * fwd)
        e = (shp[0] + d1[0] * 102 * s, shp[1] + d1[1] * 102 * s); h = (e[0] + d2[0] * 88 * s, e[1] + d2[1] * 88 * s)
        return shp, e, h, d2
    def arm(up, bend, holdv, side):
        """side -1 = left/far arm, +1 = right/near arm. Round shoulder, capsule upper arm / forearm, round elbow; lifted arms swing forward (+x).
        The far arm hangs from a shoulder behind the torso centre and is drawn under the body: its upper arm emerges from the back edge of the chest,
        so it always reads as a second, attached arm (hanging behind at rest, reaching out from behind the chest when in use)."""
        shp, e, h, d2 = arm_pts(up, bend, side)
        grip = holdv == GRIP
        if grip: holdv = None
        fill = sk if side > 0 else skf
        cap_col = fill; cap_r = 17                                                                                                           # shoulder = the rounded end of the upper-arm capsule (no larger disc, which read as a ring on the shoulder)
        if top: cap_col, cap_r = (top if side > 0 else shade(top, 0.84)), 17                                                                 # dressed torso: tunic-coloured shoulder that blends into the chest
        over_body = ARM_EDGE > 0 and (side > 0 or p.get('anjali'))
        if over_body:
            # the arm lies over the torso, often skin on skin: a contour in a deeper tone of the skin (folk-painting outline) separates it
            edge = shade(sk, 0.58); ew = ARM_EDGE
            c.ell(*shp, (cap_r + ew) * s, (cap_r + ew) * s, edge, None, 0, par)
            rlimb(shp, e, h, 17 + ew, 11 + ew, 5.5 + ew, edge)
        c.ell(*shp, cap_r * s, cap_r * s, cap_col, None, 0, par)                                                                                  # round deltoid cap
        rlimb(shp, e, h, 17, 11, 5.5, fill)
        hand(h, d2, sx, fill, fist=bool(holdv) or grip, k=1.4)
        ink = INK if side > 0 else shade(INK, 1.3)
        band(shp, e, 0.56, 15, ink, 9)                                                                                                        # black arm band
        if o.get('guards'): rband(e, h, 0.62, 8, ink, 54)                                                                                     # long black forearm guard
        else: band(e, h, 0.86, 9, ink, 7)                                                                                                     # wrist band
        if holdv == 'sword' and o.get('talwar'): holdv = 'talwar'
        if holdv: prop(holdv, h, d2, s, c, par, sx, floor=floor_y)
    anj = bool(p.get('anjali')); floor_y = Wd(0, 0)[1]
    if plant:
        hx_, hy_ = arm_pts(*p['armR'], 1)[2]
        prop(plant, (hx_, hy_ if plant == "bow" else Wd(0, PLANT_Y)[1]), (0.0, -1.0), s, c, par, sx, floor=floor_y)                       # pole rises from the ground through the resting near hand (a planted bow puts its grip band in that hand)
    _legs_dhoti(c, g, par, True)
    if not anj: arm(*p['armL'], p['holdL'], -1)                                                                                              # far arm: over the legs, under the torso -> hangs visibly behind the back, or reaches out from behind the chest
    Hd_ = _Hd_fn(g, 1.0, SIDE_LIFT, SIDE_ROT)
    polyw([Hd_(-27.5, -394), Hd_(-12, -392), Hd_(4, -390), U(13.2, -324), U(-33, -324)], shade(sk, 0.93))                       # vertical neck rising to the jaw underside                                                # slender neck, leaning into the tilted head
    # torso: rounded shoulders (half-width 62, ~1.5x the waist) flowing into a tapered waist
    chest = smooth([(-62, -346), (-60, -366), (-50, -380), (-34, -386), (0, -380), (34, -386), (50, -380), (60, -366), (62, -346), (54, -312), (44, -266), (40, -238, 'k'), (-40, -238, 'k'), (-44, -266), (-54, -312)])
    poly(chest, sk)
    back_rim = smooth([(-62, -346), (-60, -366), (-50, -380), (-44, -383), (-54, -312), (-42, -238, 'k'), (-40, -238, 'k'), (-44, -266), (-54, -312)])   # thin rim shadow on the back edge (a wide strip read as a third arm)
    if top:
        poly(chest, top)
        poly(back_rim, shade(top, 0.86))
    else:
        poly(back_rim, shade(sk, 0.9))
        poly(smooth([(6, -348), (42, -358), (52, -330), (40, -300), (10, -304)]), shade(sk, 0.92))                                            # near pectoral
        if o['sash']:
            wrap = o['sash']
            poly(smooth([(-60, -354, 'k'), (-54, -378, 'k'), (-22, -386, 'k'), (44, -270, 'k'), (44, -238, 'k'), (12, -238, 'k')]), wrap)      # sash from the far shoulder to the near hip
            c.line([U(-34, -384), U(46, -266)], shade(wrap, 0.82), 2.5 * s, par); c.line([U(-58, -362), U(28, -240)], shade(wrap, 0.86), 2.5 * s, par)
    armor_on = o['armor'] if p['armor'] is None else bool(p['armor'])
    if armor_on:
        poly(smooth([(-52, -362), (-30, -376), (0, -374), (30, -376), (52, -362), (48, -312), (36, -242, 'k'), (-36, -242, 'k'), (-48, -312)]), GOLD)
        for r_ in range(4):
            for i in range(-2, 3): dot(i * 16 + (8 if r_ % 2 else 0), -340 + r_ * 20, 4.4, (255, 232, 140))
        dot(0, -290, 9, (255, 244, 190)); dot(0, -290, 4.5, CRIMSON)
    b2_ = o['bottom2']; poly(smooth([(-46, -244, 'k'), (46, -244, 'k'), (48, -222, 'k'), (-48, -222, 'k')]), b2_)
    c.line([U(-48, -234), U(48, -236)], shade(b2_, 0.8), 2 * s, par)                                                                           # belt fold
    c.line([U(-24, -364), U(-2, -358), U(24, -362)], shade(sk, 0.74), 1.4 * s, par)                                                          # collarbone
    _necklaces(c, g, par, 0, 30, -368)
    _head_side(c, g, par)
    if anj: arm(*p['armL'], p['holdL'], -1)                                                                                                  # pressed palms: far arm over the chest, a darker twin just behind the near arm, so both arms read
    arm(*p['armR'], GRIP if plant else p['hold'], 1)

def _head_side(c, g, par):
    """graphic-novel profile head, tilted ~25 deg skyward: one straight diagonal from hairline through brow and nose bridge to a sharp
    upturned nose tip; white wedge mouth cut into the profile edge; chin jutting over a straight jaw underside, neck meeting it under the ear; large
    wedge eye whose upper rim is the thick brow, big half-disc pupil tucked in the front corner; black hair cap with an angular
    sideburn hook and a teardrop bun angled off the back of the skull."""
    o, p, s, sx, U, poly, ell, dot, hexa, sk, skd, hair, bead, jew, cr, fem = (g[k] for k in ("o", "p", "s", "sx", "U", "poly", "ell", "dot", "hexa", "sk", "skd", "hair", "bead", "jew", "cr", "fem"))
    cdot = g["cdot"]
    Hd = _Hd_fn(g, 1.0, SIDE_LIFT, SIDE_ROT)
    cream = o['eye']
    face = smooth([(-26.4, -385.8), (-35.2, -418.8), (-19.8, -456.2), (8.8, -457.3), (28.6, -434.2), (40.7, -412.2, 'k'), (31.9, -403.4), (34.1, -394.6), (36.3, -385.8, 'k'), (19.8, -381.4), (-2.2, -384.7)])   # full round cranium, sharp nose, chin jutting forward over a straight jaw underside
    poly(face, sk, Hd)
    if o.get('monkey'): poly(smooth([(16, -418), (46, -406, 'k'), (40, -390, 'k'), (14, -394)]), shade(sk, 1.12), Hd); dot(39, -400, 2.2, PUPIL, Hd)
    ell(-9, -406, 4.2, 5.2, shade(sk, 0.9), Hd)                                                                                              # ear cutout inside the C-hook
    poly(smooth([(-26.4, -385.8, 'k'), (-36.3, -418.8), (-23.1, -456.2), (5.5, -459.5), (19.8, -449.6, 'k'), (0, -444.1), (-9.9, -427.6), (-16.5, -412.2), (-6.6, -403.4), (-1.1, -411.1, 'k'), (-3.3, -396.8), (-18.7, -394.6)]), hair, Hd)   # hair cap covering the whole back of the skull down to the nape, sideburn hook round the ear
    # earring: a small ring at the lobe with a drop hanging below the jaw (a disc level with the eye read as a second eye)
    if o['kundal']: dot(-9, -398, 2.6, GOLD, Hd); poly([(-9, -395), (-13, -387), (-9, -380), (-5, -387)], GOLD, Hd); dot(-9, -387, 1.7, CRIMSON, Hd)
    elif fem: dot(-9, -398, 2.4, jew, Hd); poly([(-9, -395), (-12.5, -388), (-9, -382), (-5.5, -388)], jew, Hd); dot(-9, -388, 1.5, bead, Hd)
    else: dot(-9, -398, 2.2, GOLD, Hd)
    if not fem and cr in ("none", "band"):
        poly(smooth([(-23, -454), (-38.4, -458.4), (-39.5, -476), (-23, -476), (-17.5, -460.6)]), hair, Hd)                                  # bun high on the upper crown
        poly([(-21, -452.5), (-27, -463.5), (-23, -465.5), (-18, -455.5)], GOLD, Hd)                                                                   # gold tie
    _crown(c, g, par, Hd, -10, -30, True)
    eo = {"closed": 0.0, "shock": 1.3, "sad": 0.8, "stern": 0.9, "smile": 0.85}.get(p['expr'], 1.0)
    if p['blink']: eo = 0.0
    cy = -419
    def E(x, y, *k): return (x, cy + (y - cy) * max(eo, 0.1)) + k
    tilt = {"stern": 3, "sad": -3, "shock": -2, "smile": 0}.get(p['expr'], 0)
    if eo < 0.12:
        poly([(3.3, -425), (19.8, -429), (34.1, -417), (19.8, -426)], INK, Hd)
    else:
        gx = p['gaze'] * 2
        sclera = smooth([E(3.3, -425.4, 'k'), E(19.8, -434.2), E(34.1, -416.6, 'k'), E(20.9, -404.5), E(5.5, -410)])
        poly(sclera, cream, Hd)                                                                                                             # sharp wedge eye, flat lower lid rising to the nose
        cdot(sclera, 23.1 + gx, -418.8, min(10.4, 6.3 + 4.1 * eo), PUPIL, Hd)                                                                          # oversized pupil tucked into the front/upper corner                                                                                 # pupil tucked front/up (brow clips it to a half-disc)
    poly(smooth([(2.2, -431, 'k'), (19.8, -441), (32.5, -423 + tilt, 'k'), (19.8, -437.5)]), INK, Hd)             # arched brow = upper rim of the eye
    _mouth_side(c, g, par, Hd, cream)
    if o['beard']: poly(smooth([(-16, -388), (8, -384), (32, -387, 'k'), (24, -370), (8, -352, 'k'), (-8, -356), (-22, -376)]), o['beard'], Hd)
    if cr not in ("mukut", "turban"): _tilak(c, g, par, Hd, 10.5, -445)

def _mouth_side(c, g, par, Hd, cream):
    """white triangular wedge cut into the profile edge (stylised smile); dark open wedge when speaking"""
    o, p, poly, hair = g['o'], g['p'], g['poly'], g['hair']
    m = max(p['mouth'], 0.0)
    if m > 0.05 or p['expr'] == "shock":
        hh = 3 + 5 * max(m, 0.4 if p['expr'] == 'shock' else 0)
        poly([(33, -401.2), (26.3, -396.8), (33.5, -396.8 + hh)], PUPIL, Hd); poly([(32, -400), (27.5, -397.3), (31.5, -396)], cream, Hd)
    else:
        k = {"sad": -1, "stern": -1}.get(p['expr'], 0)
        sk = g['sk']
        poly([(33, -401.2), (26.3, -396.8 + k), (33, -392.4)], shade(sk, 0.8), Hd)                                                         # lip-toned notch (a cream wedge under the moustache read as a second eye)
        poly([(33, -401.2), (26.3, -396.8 + k), (26.8, -395.4 + k), (33, -399.8)], MOUTH, Hd)                                                     # upper lip line
    if o['mous']: poly([(33, -400), (16, -403), (16, -399), (32, -397)], hair, Hd)
    if o.get('fangs'): poly([(27.5, -396), (30.5, -396), (29, -389)], (255, 255, 240), Hd)

def f_tail(p): return p['bob'] * 1.3

PROPS = ("dagger", "staff", "bowl", "lotus", "bow", "bow_low", "bow_tall", "arrow", "mace", "trident", "sword", "talwar", "torch", "chakra", "flute", "conch", "lamp", "book", "flag", "spear", "shield", "axe", "scroll", "pot", "newborn")
def prop(kind, h, d, s, c, par, sx, floor=None):
    """draw a hand prop at hand h along unit direction d. `floor` (world y of the figure's feet) keeps upright poles from spearing
    through the ground: a pole's lower end is clamped to it and a tall bow is slid up so its lower tip rests on it."""
    ux, uy = d
    if not isinstance(kind, str): return
    kind = kind.strip().lower()
    lift = (floor - h[1]) / s if floor is not None else 0.0                                                                                 # how high the hand is above the feet (local units)
    if kind in ("sword", "talwar") and lift > 440 and uy < -0.75: ux, uy = (0.999 if ux >= 0 else -0.999), -0.04                                         # blade in a hand raised over the head is levelled forward (overhead guard): stays under a title band and over the opponent's head
    elif kind in ("sword", "talwar", "mace", "axe", "torch") and uy < -0.75:                                                                           # a weapon thrust straight up spears the title band: tilt it forward to ~45 deg (wrist cocked), keeping its facing
        ux, uy = (0.707 if ux >= 0 else -0.707), -0.707
    nx, ny = -uy, ux
    def pole_bottom(L):
        yb = h[1] + L * s
        return min(yb, floor) if floor is not None else yb
    if kind == "dagger":
        tip = (h[0] + ux * 120 * s, h[1] + uy * 120 * s)
        c.poly([(h[0] + nx * 9 * s, h[1] + ny * 9 * s), (tip[0], tip[1]), (h[0] - nx * 9 * s, h[1] - ny * 9 * s)], (236, 240, 250), INK, 4 * s, par)
        c.cap((h[0] - ux * 10 * s, h[1] - uy * 10 * s), (h[0] + ux * 6 * s, h[1] + uy * 6 * s), 11 * s, 11 * s, GOLD, INK, 3 * s, par)
    elif kind == "sword":
        tip = (h[0] + ux * 230 * s, h[1] + uy * 230 * s)
        c.poly([(h[0] + nx * 11 * s, h[1] + ny * 11 * s), (h[0] + ux * 190 * s + nx * 9 * s, h[1] + uy * 190 * s + ny * 9 * s), tip, (h[0] + ux * 190 * s - nx * 9 * s, h[1] + uy * 190 * s - ny * 9 * s), (h[0] - nx * 11 * s, h[1] - ny * 11 * s)], (236, 240, 250), INK, 4 * s, par)
        c.line([(h[0] + nx * 26 * s, h[1] + ny * 26 * s), (h[0] - nx * 26 * s, h[1] - ny * 26 * s)], GOLD, 9 * s, par)
        c.cap((h[0] - ux * 40 * s, h[1] - uy * 40 * s), (h[0], h[1]), 9 * s, 9 * s, (120, 60, 40), INK, 3 * s, par)
    elif kind == "talwar":
        # long scimitar curving back over the hand, blade widening toward the tip
        L, K = 250 * s, 70 * s
        def sp(t): return (h[0] + ux * L * t - nx * K * t * t, h[1] + uy * L * t - ny * K * t * t)
        def wd(t): return (10 + 9 * t) * s if t < 0.86 else (19 * s) * (1 - t) / 0.14
        ts = [i / 12 for i in range(13)]
        edge_a = [(sp(t)[0] + nx * wd(t), sp(t)[1] + ny * wd(t)) for t in ts]
        edge_b = [(sp(t)[0] - nx * wd(t) * 0.55, sp(t)[1] - ny * wd(t) * 0.55) for t in reversed(ts)]
        c.poly(edge_a + edge_b, (236, 240, 250), INK, 4 * s, par)
        c.line([(h[0] + nx * 24 * s, h[1] + ny * 24 * s), (h[0] - nx * 24 * s, h[1] - ny * 24 * s)], GOLD, 9 * s, par)
        c.cap((h[0] - ux * 40 * s, h[1] - uy * 40 * s), (h[0], h[1]), 9 * s, 9 * s, (120, 60, 40), INK, 3 * s, par)
        c.ell(h[0] - ux * 44 * s, h[1] - uy * 44 * s, 11 * s, 11 * s, GOLD, INK, 3 * s, par)
    elif kind == "staff":
        c.line([(h[0] - 0, pole_bottom(160)), (h[0], h[1] - 190 * s)], (120, 78, 50), 11 * s, par); c.ell(h[0], h[1] - 196 * s, 12 * s, 12 * s, GOLD, INK, 3 * s, par)
    elif kind == "spear":
        c.line([(h[0], pole_bottom(200)), (h[0], h[1] - 260 * s)], (120, 78, 50), 10 * s, par)
        c.poly([(h[0] - 18 * s, h[1] - 250 * s), (h[0], h[1] - 330 * s), (h[0] + 18 * s, h[1] - 250 * s)], (236, 240, 250), INK, 4 * s, par)
    elif kind == "trident":
        # trishul about one figure tall: pole from the ground to brow height, prongs above (shorter than the old 556 so it clears title bands);
        # held standing (hand at hip height) the head is trimmed so the prongs stay under the title band, and raised high (bless) it sits just above the fist
        pt = 230 if lift < 150 else (175 if lift < 300 else 110)
        c.line([(h[0], pole_bottom(200)), (h[0], h[1] - pt * s)], (200, 170, 90), 10 * s, par)
        for k in (-1, 0, 1):
            x0 = h[0] + k * 34 * s; top = h[1] - (pt + 70) * s - (0 if k else 20 * s)
            c.line([(h[0], h[1] - pt * s), (x0, h[1] - (pt + 20) * s), (x0, top)], (236, 240, 250), 8 * s, par)
            c.poly([(x0 - 9 * s, top), (x0, top - 26 * s), (x0 + 9 * s, top)], (236, 240, 250), INK, 3 * s, par)
    elif kind == "newborn":
        # swaddled baby cradled across the forearms: a soft cloth bundle lying along the forearm, a small round head at the far end, no limbs
        cloth, skin = (250, 238, 210), (214, 160, 112)
        cx, cy = h[0] - ux * 6 * s, h[1] - 14 * s
        a, b = (cx - ux * 44 * s, cy - uy * 44 * s), (cx + ux * 44 * s, cy + uy * 44 * s)
        c.cap(a, b, 24 * s, 24 * s, cloth, INK, 3 * s, par)
        c.line([(cx - ux * 30 * s + nx * 6 * s, cy - uy * 30 * s + ny * 6 * s), (cx + ux * 20 * s + nx * 14 * s, cy + uy * 20 * s + ny * 14 * s)], shade(cloth, 0.86), 4 * s, par)   # fold
        hx, hy = b[0] + ux * 14 * s, b[1] + uy * 14 * s - 4 * s
        c.ell(hx, hy, 17 * s, 17 * s, skin, INK, 3 * s, par)
        c.poly([(hx - 10 * s, hy - 12 * s), (hx, hy - 20 * s), (hx + 10 * s, hy - 12 * s), (hx + 4 * s, hy - 9 * s), (hx - 4 * s, hy - 9 * s)], (24, 18, 22), None, 0, par)   # tuft of hair
        for e in (-1, 1): c.arc(hx + e * 6 * s, hy, 4 * s, 3 * s, 0, 180, (24, 18, 22), 1.8 * s, par)                                      # sleeping eyes
        c.ell(hx + 8 * s, hy + 4 * s, 3 * s, 2 * s, (232, 140, 130), None, 0, par)                                                           # cheek
    elif kind == "mace":
        c.line([(h[0] - ux * 20 * s, h[1] - uy * 20 * s), (h[0] + ux * 150 * s, h[1] + uy * 150 * s)], (150, 100, 60), 12 * s, par)
        c.ell(h[0] + ux * 190 * s, h[1] + uy * 190 * s, 46 * s, 46 * s, GOLD, INK, 5 * s, par); c.ell(h[0] + ux * 190 * s, h[1] + uy * 190 * s, 18 * s, 18 * s, CRIMSON, INK, 3 * s, par)
    elif kind == "axe":
        c.line([(h[0] - ux * 20 * s, h[1] - uy * 20 * s), (h[0] + ux * 170 * s, h[1] + uy * 170 * s)], (150, 100, 60), 11 * s, par)
        bx, by = h[0] + ux * 150 * s, h[1] + uy * 150 * s
        c.poly([(bx, by - 10 * s), (bx + nx * 70 * s, by + ny * 70 * s - 50 * s), (bx + nx * 80 * s, by + ny * 80 * s + 30 * s), (bx, by + 30 * s)], (236, 240, 250), INK, 4 * s, par)
    elif kind in ("bow", "bow_low"):
        bx, by = h[0], h[1]; r = (135 if kind == "bow" else 150) * s; k = 22 * s * sx; gt = 0.0
        if kind == "bow" and uy < 0 and floor is not None:                                                                                    # planted (seated figure): lower tip rests on the ground, the grip slides up to the resting hand
            r = 165 * s; gt = by - (floor - r); by = floor - r
            u_ = min(abs(gt) / r, 1.0); kk_ = k * (1.0 if u_ < 0.12 else (1.0 - (u_ - 0.12) / 0.43 * 0.1 if u_ < 0.55 else 0.9 - (u_ - 0.55) / 0.45 * 0.8))
            bx -= kk_                                                                                                                      # ...and the limb (not the string) passes through that hand
        # "bow": upright, canted ~20 deg forward and a little shorter so its upper tip stays beside the chest / under a title band (aiming / carrying);
        # "bow_low": axis follows the forearm, so a forward forearm holds it horizontally at the hip
        ax, ay = (ux, uy) if kind == "bow_low" else ((0.0, 1.0) if abs(ux) < 0.3 else (-0.342 * sx, 0.94))                                   # carried in a hanging hand: straight up-and-down so it stays out of a companion's space
        if ay < 0: ax, ay = -ax, -ay
        px_, py_ = ay * sx, -ax * sx
        def P(t, kk): return (bx + ax * t + px_ * kk, by + ay * t + py_ * kk)
        pts = [P(-r, k * 0.1), P(-r * 0.55, k * 0.9), P(-r * 0.12, k), P(r * 0.12, k), P(r * 0.55, k * 0.9), P(r, k * 0.1)]
        c.line(pts, INK, 5 * s, par); c.line([pts[0], pts[-1]], (236, 232, 220), 1.8 * s, par)
        c.poly([P(gt - 9 * s, k - 4 * s), P(gt - 9 * s, k + 4 * s), P(gt + 9 * s, k + 4 * s), P(gt + 9 * s, k - 4 * s)], shade(INK, 1.8), None, 0, par)
    elif kind == "bow_tall":
        # Patel-style tall pale bow, held upright: tips reach from the knee to well above the head (slid up if the lower tip would pierce the ground)
        bx, by = h[0], h[1]; k = 48 * s * sx
        if floor is not None: by = min(by, floor - 236 * s)
        ax, ay = 0.08 * sx, 1.0; n_ = math.hypot(ax, ay); ax, ay = ax / n_, ay / n_                                               # near-vertical stave
        def P(t, kk): return (bx + ax * t + ay * kk, by + ay * t - ax * kk)
        pts = [P(-230 * s, k * 0.05), P(-150 * s, k * 0.72), P(-50 * s, k), P(50 * s, k), P(150 * s, k * 0.72), P(230 * s, k * 0.05)]
        c.line(pts, (240, 228, 190), 9 * s, par); c.line([pts[0], pts[-1]], (250, 246, 232), 1.8 * s, par)
        for t_ in (-230, 230): q = P(t_ * s, k * 0.05); c.ell(q[0], q[1], 7 * s, 7 * s, GOLD, None, 0, par)
        c.poly([P(-12 * s, k - 6 * s), P(-12 * s, k + 6 * s), P(12 * s, k + 6 * s), P(12 * s, k - 6 * s)], GOLD, None, 0, par)
    elif kind == "arrow":
        tip = (h[0] + ux * 150 * s, h[1] + uy * 150 * s); tail = (h[0] - ux * 60 * s, h[1] - uy * 60 * s)
        c.glow(tip[0], tip[1], 70 * s, (255, 236, 170), 0.7, par)
        c.line([tail, tip], (240, 228, 190), 5 * s, par)
        c.poly([(tip[0] + nx * 9 * s, tip[1] + ny * 9 * s), (tip[0] + ux * 34 * s, tip[1] + uy * 34 * s), (tip[0] - nx * 9 * s, tip[1] - ny * 9 * s)], GOLD, None, 0, par)
        for sg in (1, -1): c.poly([tail, (tail[0] + ux * 30 * s + nx * sg * 12 * s, tail[1] + uy * 30 * s + ny * sg * 12 * s), (tail[0] + ux * 38 * s, tail[1] + uy * 38 * s)], (250, 246, 232), None, 0, par)
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
        c.line([(h[0], pole_bottom(120)), (h[0], h[1] - 300 * s)], (150, 100, 60), 8 * s, par)
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
        asw = amp * sw * (1.2 if k == "run" else 0.86)                                                                                     # walk: arms swing only ~12 deg with a slight elbow bend (no stiff rods flung behind the back)
        nr = -asw if (asw < 0 or k == "run") else -asw * 0.45                                                                                 # walk: the near arm (front shoulder) barely swings back, so its elbow never folds into the chest
        base.update(legs=(amp * sw, -amp * sw), armR=(nr, (22 if asw < 0 else 14) if k == "walk" else 40), armL=(asw, 22 if k == "walk" else 40), bob=base['bob'] + abs(sw) * 6)
    if k == "fly": base.update(bob=base['bob'] + math.sin(f * 0.2 + seed) * 10)
    base.update(over); return base

