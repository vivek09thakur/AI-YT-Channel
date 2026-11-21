"""story.py - "Ramayan: 2 minute trailer" in folk2d. Every shot is a pure function of the frame number, timed to phrases.json.
Structure to copy for a new story: SHOT_DEFS -> shot functions -> FN -> render_frame -> CUES / MUSIC."""
import math
from folk2d import *
from folk2d.timeline import Timeline

T = Timeline()                                        # reads the phrases file named by FOLK_PHRASES
GY = 1560                                             # ground line (design px)

SHOT_DEFS = [                                         # (name, distinctive substring of the FIRST phrase of the shot)
    ("cosmos", "Before the beginning of time"), ("gods", "There existed a world"), ("dharma", "and where the eternal battle"),
    ("ayodhya", "In the magnificent kingdom"), ("rama", "Rama."), ("exile", "But destiny does not always"),
    ("companions", "Alongside him walked Sita"), ("darkness", "Deep within the forests"), ("pride", "His pride would challenge"),
    ("promise", "But he had underestimated"), ("journey", "From the forests of Panchavati"), ("army", "An army would rise"),
    ("climax", "When darkness threatens"), ("arrow", "One warrior will rise"), ("title", "RAMAYAN."),
]
_starts = [0] + [T.start(s) for _, s in SHOT_DEFS[1:]]
SHOTS = [(n, _starts[i], _starts[i + 1] if i + 1 < len(_starts) else T.total) for i, (n, _) in enumerate(SHOT_DEFS)]
FLASH_SHOTS = {"dharma", "ayodhya", "darkness", "journey", "climax", "title"}     # place / time jumps get a short white flash

def shot_at(f):
    for n, a, b in SHOTS:
        if a <= f < b: return n, a, b
    return SHOTS[-1]

def cam(c, lf, n, z=(1.0, 1.0), x=(W / 2, W / 2), y=(1130, 1130), roll=0.0, kicks=()):
    """slow camera move over the shot (z zoom, x/y look-at in design px) + optional impact kicks [(local_frame, amp)]"""
    p = smooth(lf / max(1, n)); creep = lf * 0.0004
    kx = ky = 0.0
    for f0, amp in kicks:
        d = lf - f0
        if 0 <= d < 9: kx += amp * math.sin(d * 2.4) * (1 - d / 9); ky += amp * 0.6 * math.cos(d * 3.1) * (1 - d / 9)
    c.set_cam(lerp(x[0], x[1], p) + kx, lerp(y[0], y[1], p) + ky, lerp(z[0], z[1], p) + creep, roll)

def pop(f, f0, dur=9): return back(prog(f, f0, f0 + dur))           # scale-pop 0 -> 1 with overshoot
def title(c, s, f, f0, y=700, size=118, col=GOLD, hold=None):
    """big word that pops in at frame f0 (and fades after `hold` frames if given)"""
    if f < f0: return
    a = 1.0 if hold is None else clamp(1 - (f - f0 - hold) / 12)
    if a > 0: c.text(s, W / 2, y, size, col, INK, 9, scale=max(0.01, pop(f, f0)), alpha=a)
def talk(f, a, b): return 0.5 * abs(math.sin(f * 0.6)) if a <= f < b else 0.0   # mouth movement while a phrase is spoken
def crown(c, x, y, s=1.0, par=1.0):
    c.poly([(x - 54 * s, y), (x - 48 * s, y - 38 * s), (x - 28 * s, y - 20 * s), (x - 14 * s, y - 70 * s), (x, y - 36 * s), (x + 14 * s, y - 70 * s), (x + 28 * s, y - 20 * s), (x + 48 * s, y - 38 * s), (x + 54 * s, y)], GOLD, INK, 5, par)
    for q in (-30, 0, 30): c.dots([(x + q * s, y - 14 * s)], 6 * s, CRIMSON if q else (60, 200, 190), par)

def sub(c, f):
    s, t = T.sub(f)
    if s: c.subtitle(s, t)

# ---------------- shots ----------------
def s_cosmos(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.15), y=(1060, 1130)); sky(c, "night"); stars(c, f, 90); moon(c, 220, 480, 80)
    rays_burst(c, W / 2, 1150, f, 100, None, 20, (255, 214, 120, 40), 0.9, 0.3)
    mountain(c, 300, 1500, 900, 520, (54, 44, 120), True, 0.35); mountain(c, 900, 1520, 800, 440, (64, 50, 130), True, 0.4); hills(c, 1480, 110, (74, 44, 130), 3, 0.5); ground(c, GY, (90, 52, 80))
    mandala(c, W / 2, 1150, 420, f, GOLD, 18, 0.9, 0.3)
    t_war = T.start("Before the greatest war")
    if f < t_war:
        draw_char(c, W / 2, GY, 1.5, "vishnu", act(f, "bless", 1, hold="chakra", expr="smile"))
    else:
        k = pop(f, t_war, 12)
        crowd(c, GY - 10, f, 11, -300, W + 300, 0.85, 4, ((150, 40, 60), (60, 60, 120), (170, 110, 40)))
        draw_char(c, 330, GY, 1.3 * k, "warrior", act(f, "fight", 2, hold="sword", expr="stern")) if k > 0.05 else None
        draw_char(c, 760, GY, 1.3 * k, "demon", act(f, "strike", 3, hold="mace", expr="stern"), flip=True) if k > 0.05 else None
        sparks(c, 540, 1250, f, t_war + 20, 18, 5, (255, 220, 120), 200)

def s_gods(c, f, lf, n):
    cam(c, lf, n, (1.05, 1.15), x=(W / 2, 600)); sky(c, "dawn"); sun(c, 820, 560, 110, f, True, 0.25)
    hills(c, 1420, 120, (190, 90, 120), 5, 0.4); temple(c, 860, GY, 0.9, 0.75); tree(c, 120, GY, 1.1, 0.9); ground(c, GY, (170, 110, 80))
    t_k = T.start("where destiny shaped kingdoms")
    draw_char(c, 330, GY, 1.4, "shiva", act(f, "bless", 1, hold="trident", expr="smile"))
    draw_char(c, 660, GY, 1.15, "villager", act(f, "namaste", 2, expr="smile"), flip=True)
    draw_char(c, 800, GY, 0.8, "child", act(f, "namaste", 3, expr="smile"), flip=True)
    if f >= t_k:
        k = pop(f, t_k, 12); palace(c, 540, 1180, 0.55 * k, 0.45) if k > 0.05 else None
        title(c, "KINGDOMS", f, t_k + 6, 560, 110)

def s_dharma(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.0), y=(H / 2, H / 2))
    c.gradient([(0, (40, 30, 110)), (0.49, (150, 70, 150)), (0.5, (60, 14, 40)), (1, (120, 30, 40))])
    border(c, 960, f, GOLD); border(c, 960, f, CRIMSON, 0.0, True)
    rays_burst(c, 540, 560, f, 80, None, 16, (255, 240, 170, 50), 0.0, 0.5)
    draw_char(c, 540, 900, 1.15, "rama", act(f, "stand", 1, hold="bow", expr="smile"), par=0.0)
    draw_char(c, 540, 1830, 1.15, "ravana", act(f, "hips", 2, hold="sword", expr="stern"), par=0.0)
    t_a = T.start("and Adharma was about")
    c.text("DHARMA", 540, 440, 120, GOLD, INK, 8, scale=pop(f, _starts[2] + 10, 10))
    if f >= t_a: c.text("ADHARMA", 540, 1250, 120, (255, 90, 90), INK, 8, scale=pop(f, t_a, 10))
    sparks(c, 540, 960, f, t_a, 20, 3, (255, 200, 120), 260)

def s_ayodhya(c, f, lf, n):
    cam(c, lf, n, (1.0, 1.18), y=(1080, 1150)); sky(c, "day"); sun(c, 200, 420, 100, f, True, 0.25)
    for i, (x, y, s) in enumerate([(200, 620, 1.0), (880, 520, 0.8)]): cloud(c, (x + f * (0.3 + i * 0.1)) % (W + 2 * XPAD + 400) - XPAD - 200, y, s, 0.5)
    hills(c, 1440, 100, (80, 160, 120), 6, 0.5); palace(c, 540, 1340, 0.9, 0.6); ground(c, GY, (170, 120, 70))
    flag(c, 120, GY, 1.0, f, 0.9); flag(c, 960, GY, 1.0, f, 0.9)
    t_b = T.start("A prince was born"); t_e = T.start("A prince whose name")
    draw_char(c, 330, GY, 1.4, "king", act(f, "bless" if f >= t_b else "stand", 1, expr="smile"))
    draw_char(c, 740, GY, 1.3, "queen", act(f, "give", 2, expr="smile"), flip=True)
    if f >= t_b:
        k = pop(f, t_b, 14); c.glow(640, 1300, 220 * k, (255, 230, 150), 0.7, 1.0)
        draw_char(c, 640, GY - 150, 0.55 * k, "child", act(f, "raise", 5, expr="smile")) if k > 0.05 else None
        sparks(c, 640, 1300, f, t_b, 20, 6, (255, 230, 150), 220)
    if f >= t_e: rays_burst(c, 640, 1250, f, 60, None, 14, (255, 240, 180, 50), 0.9, 0.6)

def s_rama(c, f, lf, n):
    t_son = T.start("The son of Dasharatha"); t_pro = T.start("The protector of the innocent"); t_emb = T.start("The embodiment of righteousness")
    cam(c, lf, n, (1.15, 1.25), y=(1130, 1110)); sky(c, "dusk"); sun(c, W / 2, 760, 170, f, True, 0.2)
    hills(c, 1440, 120, (96, 50, 120), 4, 0.5); ground(c, GY, (130, 70, 70))
    for i, r in enumerate((430, 560)): mandala(c, W / 2, 1150, r, f * (1 if i % 2 else -1), GOLD, 14 + i * 4, 0.9, 0.3)
    draw_char(c, W / 2 if f < t_son else 420, GY, 1.6, "rama", act(f, "stand" if f < t_pro else "bless", 1, hold="bow", expr="smile"))
    title(c, "RAMA", f, _starts[4], 560, 170, GOLD, hold=40)
    if t_son <= f < t_pro: draw_char(c, 850, GY, 1.3, "king", act(f, "bless", 2, expr="smile"), flip=True)
    if t_pro <= f < t_emb:
        draw_char(c, 820, GY, 0.8, "child", act(f, "namaste", 3, expr="smile"), flip=True); draw_animal(c, "deer", 900, GY, 0.6, f, True)
    if f >= t_emb: rays_burst(c, W / 2, 1150, f, 80, None, 18, (255, 240, 170, 60), 0.9, 0.6); title(c, "DHARMA", f, t_emb, 560, 120)

def s_exile(c, f, lf, n):
    t_c = T.start("A crown was taken away"); t_k = T.start("A kingdom was left behind"); t_x = T.start("And a prince willingly")
    cam(c, lf, n, (1.1, 1.0), x=(W / 2, 480), y=(1130, 1130)); sky(c, "storm" if f < t_x else "dusk"); stars(c, f, 30, ymax=600)
    hills(c, 1430, 120, (60, 50, 90), 7, 0.45); palace(c, 900 if f < t_x else 1500, 1300, 0.6, 0.5, (150, 130, 120), (170, 150, 90)); ground(c, GY, (100, 70, 70))
    walking = f >= t_x
    draw_char(c, 420 if not walking else 420 + (f - t_x) * 0.6, GY, 1.5, "rama", act(f, "walk" if walking else "stand", 1, hold="bow", expr="neutral" if f < t_c else "sad"))
    if f >= t_c:
        q = ease_io(prog(f, t_c, t_k)); crown(c, lerp(420, 900, q), lerp(1070, 600, q) - 120 * math.sin(q * math.pi), 1.3 - 0.5 * q)
        sparks(c, 420, 1070, f, t_c, 16, 8, (255, 220, 120), 200)
    if t_k <= f < t_x: title(c, "LEFT BEHIND", f, t_k, 560, 100, (220, 200, 220))
    if walking: tree(c, 980, GY, 1.2, 1.0, (40, 120, 80)); tree(c, 1250, GY, 1.0, 1.0, (40, 120, 80)); title(c, "14 YEARS", f, t_x + 20, 560, 140, (255, 170, 90))

def s_companions(c, f, lf, n):
    t_s = T.start("The embodiment of strength"); t_l = T.start("And Lakshmana"); t_y = T.start("Whose loyalty knew")
    cam(c, lf, n, (1.0, 1.1), x=(500, 600)); sky(c, "day"); sun(c, 900, 500, 90, f, True, 0.25)
    hills(c, 1420, 110, (80, 160, 120), 6, 0.5)
    for x in (-150, 140, 1000, 1280): tree(c, x, GY, 1.2, 1.0)
    ground(c, GY, (150, 110, 70))
    draw_char(c, 330, GY, 1.4, "rama", act(f, "walk", 1, hold="bow", expr="smile"))
    draw_char(c, 600, GY, 1.3, "sita", act(f, "walk", 2, expr="smile"))
    title(c, "SITA", f, _starts[6] + 6, 520, 130, (255, 190, 210), hold=60)
    if f >= t_s: draw_animal(c, "deer", 820, GY, 0.55, f)
    if f >= t_l:
        k = pop(f, t_l, 12); draw_char(c, 860, GY, 1.3 * k, "lakshmana", act(f, "walk", 3, hold="bow", expr="stern")) if k > 0.05 else None
        title(c, "LAKSHMANA", f, t_l + 6, 520, 110, (190, 230, 170), hold=70)

def s_darkness(c, f, lf, n):
    t_a = T.start("A darkness was awakening"); t_r = T.start("The mighty Ravana"); t_k = T.start("King of Lanka"); t_c = T.start("A conqueror feared")
    cam(c, lf, n, (1.0, 1.25), y=(1130, 1100), kicks=[(t_r - _starts[7], 10)]); sky(c, "storm"); rain(c, f, 90)
    hills(c, 1400, 120, (40, 34, 70), 8, 0.45); cave(c, 540, GY, 1.0, 0.9); ground(c, GY, (60, 44, 60))
    for x in (-100, 1180): tree(c, x, GY, 1.3, 1.0, (30, 70, 60), (60, 40, 40))
    draw_char(c, 200, GY, 1.0 if f < t_c else 1.0, "devotee", act(f, "walk" if f < t_a else "kneel", 5, expr="neutral" if f < t_a else "shock"), flip=True)
    draw_char(c, 900, GY, 1.0, "villager", act(f, "walk" if f < t_a else "kneel", 6, expr="neutral" if f < t_a else "shock"))
    if t_a <= f < t_r:
        for sd in (-1, 1): c.glow(540 + sd * 70, 1360, 40, (255, 60, 60), 0.9 + 0.1 * math.sin(f * 0.3), 1.0); c.ell(540 + sd * 70, 1360, 22, 10, (255, 80, 80), INK, 3)
    if f >= t_r:
        k = pop(f, t_r, 12); lightning(c, 760, 100, 1100, f, t_r, 2); lightning(c, 300, 60, 1000, f, t_k, 3)
        draw_char(c, 540, GY, 1.75 * k, "ravana", act(f, "hips" if f < t_c else "raise", 4, hold="sword" if f < t_c else "mace", expr="stern", mouth=talk(f, t_c, T.end("A conqueror feared")))) if k > 0.05 else None
        title(c, "RAVANA", f, t_r + 4, 560, 150, (255, 110, 110), hold=30)
    if f >= t_k: palace(c, 540, 1280, 0.5, 0.45, (90, 70, 110), (255, 170, 40)); title(c, "LANKA", f, t_k + 4, 700, 120, GOLD, hold=40)
    if f >= t_c:
        crowd(c, GY - 10, f, 9, -200, W + 200, 0.85, 7, ((150, 40, 60), (60, 60, 120), (170, 110, 40)))

def s_pride(c, f, lf, n):
    t_w = T.start("His actions would ignite"); t_f = T.start("the foundations of the universe")
    cam(c, lf, n, (1.2, 1.35), y=(1100, 1080), roll=1.5 * math.sin(lf * 0.05), kicks=[(t_w - _starts[8], 14)]); sky(c, "fire" if f >= t_w else "storm"); stars(c, f, 40, ymax=500)
    hills(c, 1430, 130, (60, 30, 60), 9, 0.45); ground(c, GY, (80, 40, 50))
    for x in (120, 960): fire(c, x, GY, 0.9 if f >= t_w else 0.5, f)
    lightning(c, 540, 60, 980, f, _starts[8] + 10, 4); lightning(c, 820, 80, 900, f, t_w, 5, life=10)
    draw_char(c, 540, GY, 1.7, "ravana", act(f, "raise" if f < t_w else "shout", 4, hold="mace", expr="stern" if f < t_w else "shock"))
    if f >= t_w: ring_wave(c, 540, 1150, f, t_w, 600, (255, 180, 100)); sparks(c, 540, 1150, f, t_w, 26, 9, (255, 200, 110), 320)
    if f >= t_f: title(c, "WAR", f, t_f, 520, 180, (255, 120, 80))

def s_promise(c, f, lf, n):
    t_d = T.start("The power of Dharma"); t_v = T.start("The power of devotion"); t_p = T.start("And the strength of a promise")
    cam(c, lf, n, (1.1, 1.2), y=(1130, 1110)); sky(c, "night"); stars(c, f, 80); moon(c, 860, 420, 70)
    hills(c, 1440, 120, (54, 44, 120), 3, 0.5); ground(c, GY, (90, 60, 80))
    rays_burst(c, 540, 1150, f, 80, None, 18, (255, 240, 180, 40), 0.9, 0.4)
    draw_char(c, 540 if f < t_v else 380, GY, 1.5, "rama", act(f, "meditate" if f < t_d else ("give" if f >= t_p else "stand"), 1, expr="smile" if f >= t_d else "closed", hold=None if f >= t_p else "bow"))
    if f >= t_d: mandala(c, 540, 1150, 440, f, GOLD, 16, 0.9, 0.3); title(c, "DHARMA", f, t_d, 540, 130)
    if f >= t_v:
        k = pop(f, t_v, 12); draw_char(c, 780, GY, 1.3 * k, "hanuman", act(f, "namaste", 2, expr="smile"), flip=True) if k > 0.05 else None
        title(c, "DEVOTION", f, t_v, 540, 120, (255, 190, 120))
    if f >= t_p:
        k = pop(f, t_p, 12); draw_char(c, 160, GY, 1.3 * k, "sita", act(f, "give", 3, expr="smile")) if k > 0.05 else None
        title(c, "A PROMISE", f, t_p, 540, 120, (255, 220, 170)); c.glow(270, 1180, 120, (255, 230, 150), 0.6, 1.0)

def s_journey(c, f, lf, n):
    t_o = T.start("To the shores of the mighty ocean"); t_h = T.start("From Hanuman's legendary leap"); t_l = T.start("To the burning skies of Lanka")
    cam(c, lf, n, (1.0, 1.08), x=(W / 2, W / 2 + 80))
    if f < t_o:
        sky(c, "day"); sun(c, 880, 480, 90, f, True, 0.25); hills(c, 1420, 110, (80, 160, 120), 6, 0.5)
        for x in (-100, 200, 900, 1200): tree(c, x, GY, 1.2, 1.0)
        ground(c, GY, (150, 110, 70)); hut(c, 560, GY, 1.0, 0.95)
        draw_char(c, 330, GY, 1.3, "rama", act(f, "walk", 1, hold="bow")); draw_char(c, 560, GY, 1.2, "sita", act(f, "walk", 2)); draw_char(c, 760, GY, 1.2, "lakshmana", act(f, "walk", 3, hold="bow"))
    elif f < t_l:
        sky(c, "dusk" if f < t_h else "heaven"); sun(c, 760, 560, 140, f, True, 0.2); stars(c, f, 30, ymax=500)
        ocean(c, 1500, f); ground(c, GY + 160, (190, 160, 110))
        draw_char(c, 240, GY + 160, 1.2, "rama", act(f, "point", 1, hold="bow", expr="stern"))
        if f < t_h: draw_char(c, 520, GY + 160, 1.15, "hanuman", act(f, "think", 2, expr="neutral"))
        else:
            q = ease_io(prog(f, t_h, T.end("From Hanuman's legendary leap")))
            hx = lerp(420, 960, q); hy = lerp(GY + 160, 900, q) - 420 * math.sin(q * math.pi)
            draw_char(c, hx, hy, 1.3, "hanuman", act(f, "fly", 2, expr="stern", hold="mace")); c.glow(hx, hy - 200, 200, (255, 200, 100), 0.6, 1.0)
            sparks(c, 420, GY + 60, f, t_h, 16, 2, (255, 230, 150), 200); title(c, "THE LEAP", f, t_h + 6, 520, 120, (255, 200, 120), hold=40)
    else:
        sky(c, "fire"); hills(c, 1430, 120, (60, 30, 60), 9, 0.45); palace(c, 540, 1330, 0.9, 0.6, (90, 70, 110), (255, 170, 40)); ground(c, GY, (80, 40, 50))
        for x in (200, 540, 880): fire(c, x, 1340, 1.0, f)
        draw_char(c, 540, GY, 1.5, "hanuman", act(f, "raise", 2, hold="torch", expr="stern")); title(c, "LANKA BURNS", f, t_l + 6, 520, 120, (255, 150, 80))

def s_army(c, f, lf, n):
    t_b = T.start("A bridge would be built"); t_g = T.start("And the greatest battle")
    cam(c, lf, n, (1.0, 1.15), y=(1130, 1110), kicks=[(t_g - _starts[11], 12)]); sky(c, "dusk" if f < t_g else "fire"); sun(c, 540, 600, 150, f, True, 0.2)
    ocean(c, 1520, f)
    if f < t_g:
        ground(c, GY + 140, (190, 160, 110))
        q = ease_io(prog(f, t_b, T.end("A bridge would be built")))
        if f >= t_b: bridge(c, 200, 1900, 1540, f, q)
        draw_char(c, 200, GY + 140, 1.25, "rama", act(f, "point", 1, hold="bow", expr="stern"))
        draw_char(c, 440, GY + 140, 1.2, "hanuman", act(f, "raise", 2, expr="smile"))
        for i, x in enumerate((640, 800, 950)): draw_animal(c, "monkey", x, GY + 140, 0.5 + 0.1 * (i % 2), f + i * 7)
        title(c, "THE ARMY", f, _starts[11] + 6, 520, 120, (255, 200, 120), hold=50)
        if f >= t_b: title(c, "THE BRIDGE", f, t_b + 6, 520, 120, GOLD, hold=60)
    else:
        ground(c, GY, (80, 40, 50)); fire(c, 540, GY, 0.7, f)
        draw_char(c, 300, GY, 1.35, "rama", act(f, "aim", 1, holdL="bow", expr="stern"))                                                      # scales trimmed so Ravana's crown and raised sword stay under the title band at this zoom
        draw_char(c, 800, GY, 1.4, "ravana", act(f, "strike", 4, hold="sword", expr="stern"), flip=True)
        sparks(c, 540, 1250, f, t_g + 10, 22, 11, (255, 220, 120), 260); ring_wave(c, 540, 1250, f, t_g, 500)
        title(c, "THE BATTLE", f, t_g + 6, 520, 130, (255, 150, 80))

def s_climax(c, f, lf, n):
    t_e = T.start("When evil believes itself"); t_d = T.start("When Dharma stands against")
    cam(c, lf, n, (1.1, 1.3), y=(1130, 1090), roll=1.0 * math.sin(lf * 0.04)); sky(c, "storm"); rain(c, f, 70); stars(c, f, 20, ymax=400)
    hills(c, 1430, 130, (40, 34, 70), 8, 0.45); ground(c, GY, (60, 44, 60))
    lightning(c, 260, 40, 900, f, _starts[12] + 8, 6); lightning(c, 860, 60, 1000, f, t_e + 4, 7)
    if f < t_d:
        draw_char(c, 640, GY, 1.75, "ravana", act(f, "hips" if f >= t_e else "raise", 4, hold="sword", expr="stern"))
        c.glow(640, 1100, 300, (150, 40, 120), 0.5, 1.0)
        if f >= t_e: title(c, "INVINCIBLE", f, t_e + 4, 500, 120, (255, 110, 110), hold=50)
    else:
        draw_char(c, 300, GY, 1.35, "rama", act(f, "aim", 1, holdL="bow", expr="stern"))
        draw_char(c, 820, GY, 1.4, "ravana", act(f, "strike", 4, hold="sword", expr="stern"), flip=True)
        c.text("DHARMA", 300, 520, 100, GOLD, INK, 7, scale=pop(f, t_d, 10)); c.text("ADHARMA", 820, 520, 100, (255, 90, 90), INK, 7, scale=pop(f, T.word("When Dharma stands against", 3), 10))

def s_arrow(c, f, lf, n):
    t_a = T.start("One arrow will change"); t_n = T.start("And one name"); t_w = T.start("Will become eternal")
    cam(c, lf, n, (1.2, 1.4), x=(W / 2, 600), y=(1120, 1080), kicks=[(T.end("One arrow will change") - 10 - _starts[13], 16)])
    sky(c, "dusk" if f < t_n else "night"); stars(c, f, 60, ymax=800); sun(c, 860, 620, 150, f, True, 0.2) if f < t_n else moon(c, 860, 420, 70)
    hills(c, 1440, 120, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    rays_burst(c, 300, 1150, f, 80, None, 18, (255, 240, 170, 50), 0.9, 0.6)
    draw_char(c, 300, GY, 1.6, "rama", act(f, "aim", 1, holdL="bow", expr="stern"))
    if f < t_n: draw_char(c, 900, GY, 1.3, "ravana", act(f, "strike" if f < t_a else "shout", 4, hold="sword", expr="stern" if f < t_a else "shock"), flip=True)
    title(c, "ONE WARRIOR", f, _starts[13] + 4, 520, 110, GOLD, hold=40)
    if t_a <= f < t_n:
        q = ease_in(prog(f, t_a + 8, T.end("One arrow will change") - 10)); arrow(c, lerp(420, 880, q), lerp(1200, 1180, q), -2, 300, 1.2, 1.0, (255, 230, 150))
        if q >= 0.99: sparks(c, 880, 1180, f, T.end("One arrow will change") - 10, 30, 12, (255, 230, 150), 360); ring_wave(c, 880, 1180, f, T.end("One arrow will change") - 10, 700)
    if f >= t_n: mandala(c, 300, 1150, 420, f, GOLD, 16, 0.9, 0.3); title(c, "ONE NAME", f, t_n + 4, 520, 110, (255, 230, 170), hold=None)
    if f >= t_w: ring_wave(c, 300, 1150, f, t_w, 800, (255, 230, 150), 1.0, 40)

def s_title(c, f, lf, n):
    t_p = T.start("The story of a prince"); t_g = T.start("The journey of a god"); t_v = T.start("And the eternal victory")
    cam(c, lf, n, (1.0, 1.08), y=(1100, 1130)); sky(c, "dusk"); sun(c, W / 2, 820, 240, f, True, 0.2); stars(c, f, 50, ymax=600)
    hills(c, 1450, 130, (90, 40, 110), 7, 0.5); ground(c, GY, (110, 60, 70))
    for i, r in enumerate((420, 560, 700)): mandala(c, W / 2, 1180, r, f * (1 if i % 2 else -1), GOLD, 14 + i * 4, 0.9, 0.3)
    k = pop(f, _starts[14], 14)
    if f >= t_p: draw_char(c, W / 2 if f < t_v else 540, GY, 1.6, "rama", act(f, "bless" if f >= t_g else "stand", 1, hold="bow", expr="smile"))
    if f >= t_g: rays_burst(c, W / 2, 1150, f, 80, None, 18, (255, 240, 170, 60), 0.9, 0.6)
    if f >= t_v:
        draw_char(c, 240, GY, 1.3, "sita", act(f, "namaste", 2, expr="smile")); draw_char(c, 820, GY, 1.3, "lakshmana", act(f, "namaste", 3, hold="bow", expr="smile"), flip=True)
        draw_char(c, 1000, GY, 1.1, "hanuman", act(f, "namaste", 4, expr="smile"), flip=True); draw_char(c, 60, GY, 1.1, "hanuman", act(f, "kneel", 5, expr="smile"))
        title(c, "VICTORY OF DHARMA", f, t_v + 8, 640, 80, (255, 240, 200))
    c.text("RAMAYAN", W / 2, 480 if f >= t_p else 900, 190 if f >= t_p else 230, GOLD, INK, 12, scale=max(0.01, k))   # drawn last: on top of the cast
    if f >= T.end("And the eternal victory") + 20: follow_button(c, W / 2, 1750, prog(f, T.end("And the eternal victory") + 20, T.total - 10))

FN = dict(cosmos=s_cosmos, gods=s_gods, dharma=s_dharma, ayodhya=s_ayodhya, rama=s_rama, exile=s_exile, companions=s_companions, darkness=s_darkness,
          pride=s_pride, promise=s_promise, journey=s_journey, army=s_army, climax=s_climax, arrow=s_arrow, title=s_title)

def render_frame(f):
    c = Canvas(); name, a, b = shot_at(f); lf = f - a; n = b - a
    FN[name](c, f, lf, n)
    c.vignette(0.38)
    if name in FLASH_SHOTS: c.flash(0.85 * max(0.0, 1 - lf / 6.0))
    sub(c, f)
    return c.finish()

# ---------------- sound ----------------
def _cues():
    C = [(0, "swell", 0.8), (T.start("Before the greatest war"), "dhol", 0.9), (T.start("Before the greatest war") + 20, "slice", 0.7),
         (T.start("There existed a world"), "chime", 0.7), (T.start("where destiny shaped kingdoms"), "pop", 0.7),
         (T.start("and where the eternal battle"), "whoosh", 0.7), (T.start("and Adharma was about"), "thunk", 0.8),
         (T.start("In the magnificent kingdom"), "bell", 0.8), (T.start("A prince was born"), "sparkle", 0.9), (T.start("Rama."), "chime", 1.0),
         (T.start("The embodiment of righteousness"), "swell", 0.7), (T.start("A crown was taken away"), "heart", 0.9), (T.start("And a prince willingly"), "riser", 0.7),
         (T.start("Alongside him walked Sita"), "chime", 0.7), (T.start("And Lakshmana"), "pop", 0.7),
         (T.start("Deep within the forests"), "rumble", 0.9), (T.start("The mighty Ravana"), "thunk", 1.0), (T.start("The mighty Ravana") + 2, "rumble", 0.8),
         (T.start("King of Lanka"), "dhol", 0.8), (T.start("His pride would challenge"), "riser", 0.8), (T.start("His actions would ignite"), "thunk", 1.0),
         (T.start("the foundations of the universe"), "dhol", 0.9), (T.start("But he had underestimated"), "heart", 0.8), (T.start("The power of Dharma"), "chime", 0.9),
         (T.start("The power of devotion"), "bell", 0.8), (T.start("And the strength of a promise"), "sparkle", 0.8),
         (T.start("From the forests of Panchavati"), "whoosh", 0.7), (T.start("To the shores of the mighty ocean"), "swell", 0.7), (T.start("From Hanuman's legendary leap"), "whoosh", 0.9),
         (T.start("To the burning skies of Lanka"), "rumble", 0.9), (T.start("An army would rise"), "dhol", 0.9), (T.start("A bridge would be built"), "riser", 0.7),
         (T.start("And the greatest battle"), "thunk", 1.0), (T.start("And the greatest battle") + 12, "slice", 0.8),
         (T.start("When darkness threatens"), "rumble", 0.9), (T.start("When evil believes itself"), "thunk", 0.8), (T.start("When Dharma stands against"), "dhol", 0.9),
         (T.start("One warrior will rise"), "riser", 0.9), (T.end("One arrow will change") - 10, "slice", 1.0), (T.end("One arrow will change") - 8, "thunk", 1.0),
         (T.start("And one name"), "heart", 0.9), (T.start("Will become eternal"), "swell", 0.8), (T.start("RAMAYAN."), "chime", 1.0), (T.start("RAMAYAN.") + 2, "dhol", 1.0),
         (T.start("And the eternal victory"), "bell", 0.9), (T.end("And the eternal victory") + 60, "pop", 0.8)]
    return sorted(C)
CUES = _cues()
MUSIC = dict(stop=T.start("Deep within the forests"), back=T.start("But he had underestimated"), sa=146.83, mood="bright", tempo=76)
