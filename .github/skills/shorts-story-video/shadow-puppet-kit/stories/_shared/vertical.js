  // ---------- shared 9:16 reel (any story) ----------
  // Uses TITLE, HOOK (two short lines) and optional REEL_SUBTITLE from story.js, plus the narration layer.
  // The 16:9 stage sits full width in the middle; the bars continue its sky colours (sampled each frame).
  const VW = 1080, VH = 1920, STAGE_H = 608, STAGE_Y = (VH - STAGE_H) / 2 + 40;
  const CAP_FONT = `italic 400 60px ${FF}`;
  const SUBTITLE = typeof REEL_SUBTITLE !== 'undefined' ? REEL_SUBTITLE : 'A short story';

  function reelFrame(ctx, t) {
    const S = lay('stage', 1280, 720), sx = S.getContext('2d', { willReadFrequently: true });
    explainerFrame(sx, 1280, 720, t, { noLines: true });
    const top = sx.getImageData(640, 2, 1, 1).data, bot = sx.getImageData(640, 717, 1, 1).data;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    const g = ctx.createLinearGradient(0, 0, 0, VH);
    g.addColorStop(0, mixc([top[0], top[1], top[2]], PAL.ink, 0.35)); g.addColorStop(STAGE_Y / VH, H.rgba([top[0], top[1], top[2]]));
    g.addColorStop((STAGE_Y + STAGE_H) / VH, H.rgba([bot[0], bot[1], bot[2]])); g.addColorStop(1, mixc([bot[0], bot[1], bot[2]], PAL.ink, 0.45));
    ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
    streaks(ctx, VW, VH, t, { seed: 61, n: 70, alpha: 0.12 });
    ctx.drawImage(S, 0, STAGE_Y, VW, STAGE_H);
    ctx.fillStyle = H.rgba(PAL.gold, 0.7); ctx.fillRect(0, STAGE_Y - 4, VW, 4); ctx.fillRect(0, STAGE_Y + STAGE_H, VW, 4);
    const L = lineAt(t), a0 = cl(t / 1.2), tt = titleTime();
    ctx.save(); ctx.textAlign = 'center';
    if (t >= tt) {
      const dt = t - tt, landing = dt < 0.9, s = landing ? 1.25 - 0.25 * EO(cl(dt / 0.9)) : 1, y = landing ? 520 : 400;
      const sz = fitFont(ctx, TITLE, 980, landing ? 170 : 150, 12);
      ctx.save(); ctx.globalAlpha = cl(dt / 0.4); ctx.translate(VW / 2, y); ctx.scale(s, s);
      title(ctx, TITLE, 0, 0, sz, PAL.gold, { letter: '12px', glow: H.rgba(PAL.kesari, 0.9), blur: 46, stroke: PAL.deep, strokeW: 12 });
      title(ctx, TITLE, 0, 0, sz, PAL.gold, { letter: '12px' });
      ctx.restore();
      if (L && L.kind === 'tag') { ctx.globalAlpha = cl(L.dt / 0.4); title(ctx, L.text, VW / 2, 500, 46, PAL.cream, { italic: true, stroke: PAL.deep, strokeW: 7 }); }
    } else {
      ctx.globalAlpha = a0;
      title(ctx, TITLE, VW / 2, 250, fitFont(ctx, TITLE, 900, 56, 16), PAL.gold, { letter: '16px', stroke: PAL.deep, strokeW: 6 });
      title(ctx, HOOK[0], VW / 2, 390, fitFont(ctx, HOOK[0], 980, 104), PAL.cream, { stroke: PAL.deep, strokeW: 9 });
      if (HOOK[1]) title(ctx, HOOK[1], VW / 2, 510, fitFont(ctx, HOOK[1], 980, 112), PAL.cream, { italic: true, stroke: PAL.deep, strokeW: 9 });
      title(ctx, SUBTITLE, VW / 2, 580, 36, PAL.sandal, { italic: true });
    }
    ctx.restore();
    if (L && L.kind !== 'title' && L.kind !== 'tag') {
      const a = cl(L.dt / 0.4) * cl(L.left / 0.35), s = 0.92 + 0.08 * EO(cl(L.dt / 0.4));
      ctx.save(); ctx.globalAlpha = a; ctx.translate(VW / 2, STAGE_Y + STAGE_H + 250); ctx.scale(s, s);
      if (L.kind === 'big') { const txt = L.text.replace(/[.!]/g, '').toUpperCase(); title(ctx, txt, 0, 20, fitFont(ctx, txt, 980, 120, 8), PAL.cream, { letter: '8px', glow: H.rgba(PAL.kesari, 0.9), blur: 30, stroke: PAL.deep, strokeW: 10 }); }
      else wrapText(ctx, L.text, 0, 0, 960, 72, CAP_FONT, PAL.cream, { stroke: PAL.deep, strokeW: 10 });
      ctx.restore();
    }
    ctx.save(); ctx.font = `400 30px ${FF}`; ctx.fillStyle = H.rgba(PAL.cream, 0.5); ctx.textAlign = 'center'; ctx.fillText('Subscribe for more stories', VW / 2, VH - 90); ctx.restore();
    const bk = Math.max(1 - cl(t / 1.2), cl((t - (DURATION - 1.2)) / 1.2));
    if (bk > 0) { ctx.fillStyle = H.rgba(PAL.ink, bk); ctx.fillRect(0, 0, VW, VH); }
  }
