  const VW = 1080, VH = 1920, K0 = VH / 720;
  const CAP_FONT = `italic 400 60px ${FF}`;
  const SUBTITLE = typeof REEL_SUBTITLE !== 'undefined' ? REEL_SUBTITLE : 'A short story';
  const FOCUS = typeof REEL_FOCUS !== 'undefined' ? REEL_FOCUS : {};
  const SC_NAME = {}; Object.keys(SC).forEach((k) => { SC_NAME[SC[k]] = k; });

  function focusOf(j, t) {
    const t0 = SCENES[j][0], key = SC_NAME[t0] !== undefined ? SC_NAME[t0] : (j === 0 ? 'open' : null);
    let v = key !== null ? FOCUS[key] : null;
    if (typeof v === 'function') v = v(t);
    if (!v) return [640, 400, 1];
    return [v[0], v[1] === undefined ? 400 : v[1], Math.max(1, v[2] || 1)];
  }
  function focusAt(t) {
    let i = SCENES.length - 1; while (i > 0 && t < SCENES[i][0]) i--;
    let f = focusOf(i, t);
    if (i > 0 && t < SCENES[i][0] + FADE) { const p = focusOf(i - 1, t), u = EIO(cl((t - SCENES[i][0]) / FADE)); f = [lerp(p[0], f[0], u), lerp(p[1], f[1], u), lerp(p[2], f[2], u)]; }
    return f;
  }
  function scrim(ctx, y0, y1, a) {
    const g = ctx.createLinearGradient(0, y0, 0, y1); g.addColorStop(0, H.rgba(PAL.ink, a)); g.addColorStop(1, H.rgba(PAL.ink, 0));
    ctx.fillStyle = g; ctx.fillRect(0, Math.min(y0, y1), VW, Math.abs(y1 - y0));
  }

  function reelFrame(ctx, t) {
    const [fx, fy, fz] = focusAt(t), k = K0 * fz, SW = Math.ceil(1280 * k), SH = Math.ceil(720 * k);
    const S = lay('stage', SW, SH), sx = S.getContext('2d');
    explainerFrame(sx, 1280, 720, t, { noLines: true });
    const cx = cl(fx * k - VW / 2, 0, SW - VW), cy = cl(fy * k - VH / 2, 0, SH - VH);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.drawImage(S, cx, cy, VW, VH, 0, 0, VW, VH);
    streaks(ctx, VW, VH, t, { seed: 61, n: 50, alpha: 0.08 });
    const L = lineAt(t), a0 = cl(t / 1.2), tt = titleTime();
    const hookEnd = SCENES[1] ? SCENES[1][0] : 10, hk = a0 * (1 - sm(hookEnd - 0.8, hookEnd + 0.2, t));
    scrim(ctx, 0, 720, t >= tt ? 0.55 : 0.22 + 0.3 * hk); scrim(ctx, VH, VH - 520, 0.72);
    ctx.save(); ctx.textAlign = 'center';
    if (t >= tt) {
      const dt = t - tt, landing = dt < 0.9, s = landing ? 1.25 - 0.25 * EO(cl(dt / 0.9)) : 1, y = landing ? 460 : 380;
      const sz = fitFont(ctx, TITLE, 980, landing ? 170 : 150, 12);
      ctx.save(); ctx.globalAlpha = cl(dt / 0.4); ctx.translate(VW / 2, y); ctx.scale(s, s);
      title(ctx, TITLE, 0, 0, sz, PAL.gold, { letter: '12px', glow: H.rgba(PAL.kesari, 0.9), blur: 46, stroke: PAL.deep, strokeW: 12 });
      title(ctx, TITLE, 0, 0, sz, PAL.gold, { letter: '12px' });
      ctx.restore();
      if (L && L.kind === 'tag') { ctx.globalAlpha = cl(L.dt / 0.4); title(ctx, L.text, VW / 2, 500, 46, PAL.cream, { italic: true, stroke: PAL.deep, strokeW: 7 }); }
    } else {
      ctx.globalAlpha = a0;
      title(ctx, TITLE, VW / 2, 230, fitFont(ctx, TITLE, 900, 56, 16), PAL.gold, { letter: '16px', stroke: PAL.deep, strokeW: 6 });
      ctx.globalAlpha = hk;
      if (hk > 0) title(ctx, HOOK[0], VW / 2, 370, fitFont(ctx, HOOK[0], 980, 104), PAL.cream, { stroke: PAL.deep, strokeW: 9 });
      if (hk > 0 && HOOK[1]) title(ctx, HOOK[1], VW / 2, 490, fitFont(ctx, HOOK[1], 980, 112), PAL.cream, { italic: true, stroke: PAL.deep, strokeW: 9 });
      if (hk > 0) title(ctx, SUBTITLE, VW / 2, 560, 36, PAL.sandal, { italic: true });
    }
    ctx.restore();
    if (L && L.kind !== 'title' && L.kind !== 'tag') {
      const a = cl(L.dt / 0.4) * cl(L.left / 0.35), s = 0.92 + 0.08 * EO(cl(L.dt / 0.4));
      ctx.save(); ctx.globalAlpha = a; ctx.translate(VW / 2, VH - 250); ctx.scale(s, s);
      if (L.kind === 'big') { const txt = L.text.replace(/[.!]/g, '').toUpperCase(); title(ctx, txt, 0, 20, fitFont(ctx, txt, 980, 120, 8), PAL.cream, { letter: '8px', glow: H.rgba(PAL.kesari, 0.9), blur: 30, stroke: PAL.deep, strokeW: 10 }); }
      else wrapText(ctx, L.text, 0, 0, 960, 72, CAP_FONT, PAL.cream, { stroke: PAL.deep, strokeW: 10 });
      ctx.restore();
    }
    ctx.save(); ctx.font = `400 30px ${FF}`; ctx.fillStyle = H.rgba(PAL.cream, 0.55); ctx.textAlign = 'center'; ctx.fillText('Subscribe for more stories', VW / 2, VH - 60); ctx.restore();
    const bk = Math.max(1 - cl(t / 1.2), cl((t - (DURATION - 1.2)) / 1.2));
    if (bk > 0) { ctx.fillStyle = H.rgba(PAL.ink, bk); ctx.fillRect(0, 0, VW, VH); }
  }