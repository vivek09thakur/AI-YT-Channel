  // ---------- shared narration layer (any story) ----------
  // Expects, from lines.js (generated from the voice track):
  //   const DURATION = <seconds>;  const LINES = [[t0, 'text', kind?, t1?], ...]   kind: 'line' | 'big' | 'title' | 'tag'
  // Expects, from story.js:
  //   const TITLE = 'RAMAYAN'; const HOOK = ['line 1', 'line 2']; const FADE = 0.9;
  //   const SCENES = [[0, sceneA], [t, sceneB], ...]   each scene: (ctx, W, Hh, t) => void, drawing a full 1280x720 frame
  // Provides: lineAt, drawLines, stageFrame, explainerFrame and small scene helpers (pop, fade, cam, stars, WARM/DUSK/NIGHT).
  const LINE_HOLD = 4.2;
  function lineAt(t) {
    for (let i = LINES.length - 1; i >= 0; i--) {
      const L = LINES[i];
      if (t >= L[0]) {
        const kind = L[2] || 'line', next = LINES[i + 1] ? LINES[i + 1][0] : DURATION;
        const spoken = L[3] != null ? L[3] + 0.45 : L[0] + LINE_HOLD;
        const end = kind === 'tag' || kind === 'title' ? next : Math.min(next, Math.max(spoken, L[0] + 1.2));
        return t < end ? { i, text: L[1], kind, dt: t - L[0], left: end - t, t0: L[0], t1: L[3] != null ? L[3] : end } : null;
      }
    }
    return null;
  }
  const titleTime = () => { const i = LINES.findIndex((L) => L[2] === 'title'); return i < 0 ? Infinity : LINES[i][0]; };
  function fitFont(c, txt, maxW, base, letter) {
    c.save(); c.font = `400 ${base}px ${FF}`; const w = c.measureText(txt).width + txt.length * (letter || 0); c.restore();
    return Math.min(base, Math.floor(base * maxW / w));
  }

  function drawLines(c, W, Hh, t) {
    const tt = titleTime();
    if (t >= tt) {
      // the title lands once and stays to the end; taglines sit under it
      const dt = t - tt, s = 1.25 - 0.25 * EO(cl(dt / 0.9)), sz = fitFont(c, TITLE, 1150, 150, 14);
      c.save(); c.globalAlpha = cl(dt / 0.4); c.translate(W / 2, 140); c.scale(s, s);
      title(c, TITLE, 0, 0, sz, PAL.gold, { letter: '14px', glow: H.rgba(PAL.kesari, 0.9), blur: 40, stroke: PAL.deep, strokeW: 10 });
      title(c, TITLE, 0, 0, sz, PAL.gold, { letter: '14px' });
      c.restore();
    }
    const L = lineAt(t); if (!L || L.kind === 'title') return;
    const a = cl(L.dt / 0.4) * cl(L.left / 0.35);
    c.save(); c.globalAlpha = a;
    if (L.kind === 'big') {
      const txt = L.text.replace(/[.!]/g, '').toUpperCase(), sz = fitFont(c, txt, 1160, 108, 10);
      const s = 1 + 0.08 * (1 - EO(cl(L.dt / 0.6)));
      c.translate(W / 2, 128); c.scale(s, s);
      title(c, txt, 0, 0, sz, PAL.cream, { letter: '10px', glow: H.rgba(PAL.kesari, 0.9), blur: 30, stroke: PAL.deep, strokeW: 9 });
    } else if (L.kind === 'tag') {
      title(c, L.text, W / 2, 262, 40, PAL.cream, { italic: true, stroke: PAL.deep, strokeW: 7 });
    } else {
      const y = 600 + 10 * (1 - EO(cl(L.dt / 0.5)));
      wrapText(c, L.text, W / 2, y, 1000, 50, `italic 400 42px ${FF}`, PAL.cream, { stroke: PAL.deep, strokeW: 8 });
    }
    c.restore();
  }
  function stageFrame(ctx, W, Hh, t) {
    let i = SCENES.length - 1; while (i > 0 && t < SCENES[i][0]) i--;
    const [t0, fn] = SCENES[i];
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    if (i > 0 && t < t0 + FADE) {
      const A = lay('A', W, Hh), B = lay('B', W, Hh);
      SCENES[i - 1][1](A.getContext('2d'), W, Hh, t); fn(B.getContext('2d'), W, Hh, t);
      ctx.drawImage(A, 0, 0); ctx.save(); ctx.globalAlpha = EIO((t - t0) / FADE); ctx.drawImage(B, 0, 0); ctx.restore();
    } else fn(ctx, W, Hh, t);
    H.vignette(ctx, W, Hh, 0.32, '60,20,5');
    const bk = Math.max(1 - cl(t / 1.2), cl((t - (DURATION - 1.2)) / 1.2));
    if (bk > 0) { ctx.fillStyle = H.rgba(PAL.ink, bk); ctx.fillRect(0, 0, W, Hh); }
  }
  function explainerFrame(ctx, W, Hh, t, o) {
    stageFrame(ctx, W, Hh, t);
    if (!(o && o.noLines)) drawLines(ctx, W, Hh, t);
  }

  // ---- helpers scenes may use
  const pop = (t, t0, d) => H.ease.back(cl((t - t0) / (d || 0.5)));
  const fade = (t, t0, d) => cl((t - t0) / (d || 0.6));
  function cam(c, W, Hh, k, px, py) { c.translate(W / 2 + (px || 0), Hh / 2 + (py || 0)); c.scale(1 + k, 1 + k); c.translate(-W / 2, -Hh / 2); }
  const WARM = [[0, PAL.amber], [0.45, PAL.saffron], [0.8, PAL.burnt], [1, PAL.brown]];
  const DUSK = [[0, PAL.maroon], [0.4, PAL.burnt], [0.75, PAL.saffron], [1, PAL.turmeric]];
  const NIGHT = [[0, PAL.night], [0.5, PAL.indigo], [0.85, PAL.maroon], [1, PAL.burnt]];
  const mixStops = (A, B, u) => A.map((s, i) => [s[0], mixc(s[1], B[i][1], u)]);
  const stars = (c, W, Hh, t, a) => { const r = H.rng(12); c.save(); c.fillStyle = PAL.cream; for (let i = 0; i < 90; i++) { const x = r() * W, y = r() * Hh * 0.6, s = 1 + r() * 1.6, tw = 0.5 + 0.5 * Math.sin(t * (1 + r() * 2) + r() * 9); c.globalAlpha = a * tw; c.beginPath(); c.arc(x, y, s, 0, TAU); c.fill(); } c.restore(); };
