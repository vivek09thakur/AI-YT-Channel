"""story.py - "Karna donates the kavach" in folk2d. Every shot is a pure function of the frame number, timed to work/phrases.json.
Replace SHOT_DEFS, the shot functions, CUES and MUSIC for a new story; keep the helpers."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline(os.path.join(HERE, "work", "phrases.json"))
SUBS = os.environ.get("FOLK_SUBS", "1") != "0"
GY = 1560                                            # ground line (design px)

SHOT_DEFS = [                                         # (name, first phrase of the shot - any distinctive substring of its text)
    ("hook", "क्या आप जानते"), ("armor", "कर्ण के जन्म से"), ("war", "लेकिन महाभारत"), ("brahmin", "वो एक बूढ़े"), ("ask", "ब्राह्मण ने कर्ण से कहा"),
    ("realize", "कर्ण समझ गया"), ("smile", "लेकिन कर्ण ने फिर भी"), ("donate", "इसके बाद कर्ण ने अपनी कटार"), ("bow", "ये देखकर"),
    ("compare", "सोचिए"), ("payoff", "कवच चला गया"), ("cta", "ऐसी ही महाभारत")]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"brahmin", "bow", "payoff"}           # place / time jumps get a 6-frame white flash

def shot_at(f):
    for n, a, b in SHOTS:
        if a <= f < b: return n, a, b
    return SHOTS[-1]

def cam(c, lf, n, z=(1.0, 1.0), x=(W / 2, W / 2), y=(H / 2, H / 2), roll=0.0, kicks=()):
    p = smooth(lf / max(1, n)); creep = lf * 0.0006
    kx = ky = 0.0
    for f0, amp in kicks:
        d = lf - f0
        if 0 <= d < 9: kx += amp * math.sin(d * 2.4) * (1 - d / 9); ky += amp * 0.6 * math.cos(d * 3.1) * (1 - d / 9)
    c.set_cam(lerp(x[0], x[1], p) + kx, lerp(y[0], y[1], p) + ky, lerp(z[0], z[1], p) + creep, roll)

def pop(f, f0, dur=9): return back(prog(f, f0, f0 + dur))           # scale-pop 0 -> 1 with overshoot
def title(c, s, f, f0, y=720, size=118, col=GOLD):
    if f >= f0: c.text(s, W / 2, y, size, col, INK, 9, scale=max(0.01, pop(f, f0)))
def river(c, y, f, par=1.0):
    c.poly([(-600, y), (W + 600, y), (W + 600, y + 520), (-600, y + 520)], (60, 130, 200), INK, 6, par)
    for i in range(10):
        x = (i * 160 + f * 3) % (W + 400) - 200; c.arc(x, y + 60 + (i % 3) * 70, 60, 14, 200, 340, (200, 230, 255), 6, par)

def sub(c, f):
    if SUBS:
        s, t = T.sub(f)
        if s: c.subtitle(s, t)

# ---------------- shots ----------------
def s_hook(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.18), y=(H / 2, 1130)); sky(c, "night"); stars(c, f, 80); moon(c, 220, 520, 80)
    mountain(c, 760, 1380, 900, 560, (54, 44, 120), True, 0.35); hills(c, 1450, 120, (74, 44, 130), 3, 0.5); ground(c, GY, (110, 62, 70))
    rays_burst(c, W / 2, 1190, f, 100, 1500, 20, (255, 214, 120, 46), 0.9)
    mandala(c, W / 2, 1200, 400, f, GOLD, 18, 0.9, 0.35)
    draw_char(c, W / 2, GY, 1.62, "karna", act(f, "stand", 1, expr="smile" if lf > 40 else "neutral"))
    title(c, "सूर्यपुत्र कर्ण", f, T.start("सूर्यपुत्र कर्ण"), 640)

def s_armor(c, f, lf, n):
    cam(c, lf, n, (1.15, 1.5), x=(W / 2, W / 2), y=(1150, 1060)); sky(c, "dusk"); sun(c, 880, 640, 120, f, True, 0.2)
    hills(c, 1420, 130, (96, 50, 120), 4, 0.5); ground(c, GY, (130, 70, 70))
    t_k = T.start("कवच और कुंडल"); t_a = T.start("जब तक ये") if True else 0
    n_lit = int(clamp((f - t_k) / 90, 0, 1) * 18)
    bead_ring(c, W / 2, 1180, 430, 18, max(1, n_lit), 0.9)
    draw_char(c, W / 2, GY, 1.62, "karna", act(f, "stand", 1, expr="smile"))
    c.glow(W / 2, 1120, 300, (255, 220, 110), 0.5 * (0.7 + 0.3 * math.sin(f * 0.2)), 0.9)
    title(c, "कवच", f, t_k, 470, 120); title(c, "कुंडल", f, t_k + 24, 610, 120)
    title(c, "अजेय", f, T.start("जब तक ये"), 540, 140, (255, 120, 70)) if f >= T.start("जब तक ये") else None

def s_war(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.12), y=(H / 2, 1060)); sky(c, "heaven"); stars(c, f, 40, ymax=700)
    for i, (x, y, s) in enumerate([(200, 520, 1.2), (880, 760, 0.9), (460, 1180, 1.0)]): cloud(c, (x + f * (0.4 + i * 0.15)) % (W + 400) - 200, y, s, 0.5)
    ground(c, GY, (170, 130, 200), (255, 220, 120)); throne(c, W / 2, GY, 1.0, 0.8)
    t_b = T.start("इसलिए इंद्र"); lean = 0 if f < t_b else 6
    draw_char(c, W / 2, GY, 1.5, "indra", act(f, "think", 2, lean=lean, expr="stern"))
    t_t = T.start("देवराज इंद्र जानते"); k = pop(f, t_t, 12)
    if f >= t_t and k > 0: swirl(c, 700, 760, f, 1.4, 0.8); c.ell(780, 560, 190 * k, 120 * k, (255, 244, 214), INK, 6, 0.8); c.text("अर्जुन", 780, 560, 80 * k, CRIMSON, INK, 5, par=0.8) if k > 0.4 else None

def s_brahmin(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.1), x=(W / 2, 600)); sky(c, "dawn"); sun(c, 800, 700, 130, f, True, 0.3)
    hills(c, 1380, 120, (190, 90, 120), 5, 0.4); tree(c, 120, GY, 1.1, 0.9); river(c, GY, f); ground(c, GY + 40, (170, 110, 80))
    draw_char(c, 700, GY + 30, 1.5, "karna", act(f, "give", 1, expr="smile", hold="bowl"), flip=True)
    t0 = T.start("वो एक बूढ़े"); p = ease_out(prog(f, t0, t0 + 110)); x = lerp(-200, 330, p); walking = p < 0.99
    ph = f * 0.35; legs = (math.sin(ph) * 16, -math.sin(ph) * 16) if walking else (0, 0)
    draw_char(c, x, GY + 30, 1.4, "brahmin", act(f, "stand", 3, lean=8 if walking else 3, legs=legs, hold="staff", expr="neutral"))
    title(c, "अर्घ्य", f, T.start("उस समय कर्ण"), 600, 110, (255, 214, 110))

def s_ask(c, f, lf, n):
    cam(c, lf, n, (1.15, 1.32), x=(W / 2, W / 2), y=(1180, 1130)); sky(c, "dawn"); sun(c, 820, 640, 120, f, True, 0.3); hills(c, 1400, 120, (190, 90, 120), 5, 0.4); ground(c, GY, (170, 110, 80))
    draw_char(c, 720, GY, 1.5, "karna", act(f, "stand", 1, expr="smile"), flip=True)
    t_q = T.start("मुझे तुमसे एक दान"); talking = t_q <= f < T.end("मुझे तुम्हारा कवच")
    draw_char(c, 350, GY, 1.4, "brahmin", act(f, "plead", 3, mouth=0.5 * abs(math.sin(f * 0.6)) if talking else 0, hold="staff", expr="neutral"))
    k = pop(f, T.start("मुझे तुम्हारा कवच"), 10)
    if k > 0: c.ell(360, 650, 250 * k, 110 * k, (255, 244, 214), INK, 6, 1.0); c.text("कवच + कुंडल", 360, 650, 64 * k, CRIMSON, INK, 4)

def s_realize(c, f, lf, n):
    t_i = T.start("ये स्वयं देवराज"); t_w = T.start("कर्ण को ये भी पता"); t_s = T.start("सूर्यदेव ने तो")
    cam(c, lf, n, (1.2, 1.4), x=(W / 2, W / 2), y=(1130, 1080), roll=1.2 * math.sin(lf * 0.03)); sky(c, "dream" if f >= t_s else "dawn"); ground(c, GY, (150, 96, 90))
    if f >= t_s: sun(c, 840, 560, 120, f, True, 0.25)
    brah = "indra" if f >= t_i else "brahmin"
    draw_char(c, 790, GY, 1.35, brah, act(f, "stand", 3, expr="neutral"))
    ring_wave(c, 790, 1100, f, t_i, 420, (255, 230, 150)); sparks(c, 790, 1100, f, t_i, 18, 4)
    ex = "shock" if t_i <= f < t_w else ("sad" if f >= t_w else "stern")
    draw_char(c, 300, GY, 1.5, "karna", act(f, "stand", 1, expr=ex, gaze=1.0, lean=-4), flip=False)
    if f >= t_s:
        k = pop(f, t_s, 12); c.ell(780, 420, 190 * k, 190 * k, (255, 214, 120), INK, 6, 0.3); draw_char(c, 780, 560, 0.55 * k, "surya", act(f, "bless", 5, expr="stern"), par=0.3) if k > 0.3 else None

def s_smile(c, f, lf, n):
    cam(c, lf, n, (1.3, 1.6), y=(1160, 1100)); sky(c, "day"); sun(c, 540, 700, 150, f, True, 0.25); hills(c, 1420, 120, (80, 160, 120), 6, 0.5); ground(c, GY, (150, 100, 70))
    rays_burst(c, W / 2, 1100, f, 100, 1500, 18, (255, 240, 170, 60), 0.8, 0.8)
    draw_char(c, W / 2, GY, 1.62, "karna", act(f, "namaste", 1, expr="smile"))
    t_q = T.start("मेरे द्वार से"); k = pop(f, t_q, 10)
    if k > 0: c.text("कोई खाली हाथ", W / 2, 520, 108 * k, GOLD, INK, 8, par=0.0); c.text("नहीं लौटा", W / 2, 650, 108 * k, GOLD, INK, 8, par=0.0)

def s_donate(c, f, lf, n):
    t_d = T.start("इसके बाद कर्ण ने अपनी कटार"); t_b = T.start("उसके शरीर से खून"); t_g = T.start("उसने अपना कवच"); t_e = T.end("उसने अपना कवच")
    cam(c, lf, n, (1.1, 1.5), x=(W / 2, 620), y=(1100, 1100), kicks=[(t_b - lf - 0 if False else 0, 0)]); sky(c, "fire" if f < t_g else "dusk"); ground(c, GY, (120, 70, 66))
    armor_on = f < t_b + 10
    strike = ease_io(prog(f, t_d + 20, t_b)); dag = "dagger"
    arm = (lerp(150, 70, strike), lerp(30, 90, strike))
    draw_char(c, 420, GY, 1.62, "karna", act(f, "stand", 1, armor=armor_on, armR=arm, hold=dag if f < t_g else None, expr="smile" if f < t_b else "neutral"))
    draw_char(c, 840, GY, 1.4, "brahmin", act(f, "stand", 3, expr="neutral", hold="staff"), flip=True)
    if f >= t_b:                                          # blood = a single drop + soft red glow, no gore
        c.glow(420, 1190, 160, (220, 50, 70), 0.5 * max(0, 1 - (f - t_b) / 80), 1.0)
        for i in range(2): drop(c, 440 + i * 30, 1250 + ((f - t_b) * 2.2 + i * 30) % 160, 12)
        sparks(c, 420, 1160, f, t_b, 22, 7, (255, 190, 90), 220)
    if f >= t_b:
        q = ease_io(prog(f, t_g, t_e)); kx = lerp(430, 800, q); ky = lerp(1130, 1080, q) - 80 * math.sin(q * math.pi)
        kavach_prop(c, kx, ky, 1.0, f, 1.0)
    if f >= t_g: sparks(c, 800, 1090, f, t_e - 6, 24, 9, (255, 230, 150), 260); ring_wave(c, 800, 1090, f, t_e - 6, 380)

def s_bow(c, f, lf, n):
    cam(c, lf, n, (1.1, 1.3), x=(W / 2, W / 2), y=(1130, 1100)); sky(c, "heaven"); stars(c, f, 40, ymax=700); cloud(c, 200, 600, 1.1, 0.5); cloud(c, 880, 800, 1.0, 0.5); ground(c, GY, (170, 130, 200), (255, 220, 120))
    rays_burst(c, 760, 1100, f, 100, 1500, 18, (255, 240, 190, 54), 0.8, 0.5)
    b = ease_io(prog(f, T.start("उसकी दानवीरता") if False else T.start("जिस कर्ण को") + 20, T.start("उनका सिर") + 10 if False else T.end("उनका सिर झुक गया")))
    draw_char(c, 770, GY, 1.5, "indra", act(f, "give", 2, lean=18 * b, head=10 * b, expr="sad" if b > 0.5 else "neutral"))
    kavach_prop(c, 770 + 20 * b, GY - 200 + 10 * b, 0.5, f, 0.8)
    draw_char(c, 290, GY, 1.62, "karna", act(f, "stand", 1, armor=False, expr="smile"))
    c.glow(290, 1100, 330, (255, 214, 110), 0.5, 1.0)

def s_compare(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.04)); t_c = T.start("इसके लिए छल")
    c.gradient([(0, (40, 30, 110)), (0.49, (150, 70, 150)), (0.5, (255, 200, 110)), (1, (255, 160, 70))])
    border(c, 960, f, GOLD); c.rrect(0, 940, W, 980, 0, GOLD, INK, 5, 0.0); border(c, 960, f, CRIMSON, 0.0)
    cloud(c, 200, 420, 0.9, 0.0); cloud(c, 880, 560, 0.8, 0.0)
    draw_char(c, 540, 905, 1.1, "indra", act(f, "hips", 2, expr="stern", lean=-3), par=0.0)
    c.text("छल", 180, 520, 120, (255, 200, 120), INK, 8, scale=pop(f, T.start("सोचिए"), 10))
    draw_char(c, 540, 1830, 1.1, "karna", act(f, "namaste", 1, expr="smile", armor=False), par=0.0)
    if f >= t_c: c.text("वचन", 180, 1330, 120, GOLD, INK, 8, scale=pop(f, t_c + 20, 10))
    mandala(c, 540, 1560, 330, f, GOLD, 14, 0.0, 0.4)

def s_payoff(c, f, lf, n):
    cam(c, lf, n, (1.45, 1.0), y=(1050, H / 2)); sky(c, "dusk"); sun(c, W / 2, 900, 260, f, True, 0.2); hills(c, 1450, 130, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    for i, r in enumerate((420, 560, 700)): mandala(c, W / 2, 1180, r, f * (1 if i % 2 else -1), GOLD, 14 + i * 4, 0.9, 0.3)
    draw_char(c, W / 2, GY, 1.62, "karna", act(f, "stand", 1, armor=False, expr="smile"))
    t_a = T.word("अमर हो गया", 0) if True else 0
    title(c, "अमर", f, T.start("लेकिन कर्ण अपने त्याग") , 620, 190, GOLD)

def s_cta(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.05)); sky(c, "night"); stars(c, f, 90, ymax=1300); moon(c, 860, 360, 70)
    lotus(c, W / 2, 1450, 150, (255, 150, 190), 0.0); mandala(c, W / 2, 1100, 330, f, GOLD, 16, 0.0, 0.3)
    k = pop(f, _starts[-1] + 6, 12); c.text("Maya Effects", W / 2, 760, 118 * k, GOLD, INK, 8) if k > 0 else None
    px = lerp(-200, W + 200, ease_in(prog(f, _starts[-1] + 20, _starts[-1] + 70))); paper_plane(c, px, 520 - 120 * prog(f, _starts[-1] + 20, _starts[-1] + 70), 1.0, -18)
    follow_button(c, W / 2, 1100, prog(f, _starts[-1] + 60, T.total - 10))

FN = dict(hook=s_hook, armor=s_armor, war=s_war, brahmin=s_brahmin, ask=s_ask, realize=s_realize, smile=s_smile, donate=s_donate, bow=s_bow, compare=s_compare, payoff=s_payoff, cta=s_cta)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

# ---------------- sound ----------------
def _cues():
    C = [(0, "swell", 0.8), (T.start("सूर्यपुत्र कर्ण"), "chime", 0.8), (T.start("कर्ण के जन्म से"), "sparkle", 0.7), (T.start("जब तक ये"), "thunk", 0.8),
         (T.start("लेकिन महाभारत"), "dhol", 0.9), (T.start("इसलिए इंद्र"), "dhol", 0.8), (T.start("वो एक बूढ़े"), "whoosh", 0.6), (T.start("उस समय कर्ण"), "bell", 0.6),
         (T.start("मुझे तुम्हारा कवच"), "pop", 0.8), (T.start("ये स्वयं देवराज"), "sparkle", 0.9), (T.start("कर्ण को ये भी पता"), "heart", 0.9), (T.start("सूर्यदेव ने तो"), "swell", 0.7),
         (T.start("मेरे द्वार से"), "chime", 0.7), (T.start("इसके बाद कर्ण ने अपनी कटार"), "riser", 0.7), (T.start("उसके शरीर से खून"), "slice", 0.9), (T.start("उसके शरीर से खून") + 6, "drip", 0.6),
         (T.end("उसने अपना कवच") - 8, "chime", 1.0), (T.start("ये देखकर"), "whoosh", 0.7), (T.start("ये देखकर") + 6, "bell", 0.8), (T.start("सोचिए"), "click", 0.8),
         (T.start("कवच चला गया"), "riser", 0.8), (T.start("लेकिन कर्ण अपने त्याग"), "chime", 1.0), (_starts[-1] + 20, "whoosh", 0.7), (_starts[-1] + 66, "pop", 0.9)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("इसके बाद कर्ण ने अपनी कटार"), back=T.start("कवच चला गया"), sa=146.83)
