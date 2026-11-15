  // ---------- 9:16 reel (S3 landscape-in-reel layout) ----------
  // Top bar: hook line. Middle: the 16:9 stage at full width (1080x608), not cropped. Bottom bar: Hinglish captions.
  const VW = 1080, VH = 1920, STAGE_Y = (VH - 608) / 2;
  // caption chunks from the voiceover word times; *word* = emphasis
  const CAPS = [
    [0.01, 'Aapne kabhi kauwe ko'], [0.97, '*pareshan* kiya hai?'], [1.90, 'Woh aapka chehra'], [2.85, '*saalon* yaad rakhega…'],
    [4.20, 'aur apne doston ko'], [5.25, 'bhi bata dega.'], [6.20, 'Ye kahani nahi hai.'], [7.29, 'America ki'],
    [7.72, '*University of Washington*'], [9.20, 'mein scientists ne'], [10.20, 'ise *sach mein* test kiya.'], [11.66, '*2006* mein ek scientist ne'],
    [13.46, 'ek ajeeb sa *mask* pehna,'], [14.58, 'aur campus ke'], [15.12, 'kuch kauwe *pakde.*'], [16.74, 'Unhe chot nahi pahunchayi.'],
    [18.11, 'Bas pakda,'], [18.90, '*tag* kiya'], [19.48, 'aur *chhod* diya.'], [20.42, 'Uske baad jo bhi'],
    [21.47, 'wo *mask* pehen kar'], [22.32, 'campus mein chalta,'], [23.20, 'kauwe uske upar'], [24.33, '*cheekhne* lagte.'],
    [25.11, '*Jhund* bana kar'], [26.00, 'peeche padte.'], [26.89, 'Ek *dusra mask* bhi pehna gaya,'], [28.58, 'aur us par kisi ne'],
    [29.30, 'dhyan *nahi* diya.'], [30.32, 'Ab *twist* suniye.'], [31.49, 'Kuch saal baad'], [32.16, 'wo kauwe bhi cheekh rahe the'],
    [33.56, 'jo kabhi *pakde hi nahi* gaye the.'], [35.09, 'Matlab kauwon ne'], [35.93, 'ek dusre ko *sikha diya*'], [37.59, 'ki *dushman* kaun hai.'],
    [38.47, 'Aur ye nafrat'], [39.64, '*15 saal* se zyada chali.'], [41.14, 'Ek aur *research* mein'], [42.23, 'dekha gaya ki'],
    [42.87, 'jab koi kauwa mar jaata hai,'], [44.17, 'to baaki kauwe'], [45.13, 'uske aas-paas'], [46.04, '*jama* ho jaate hain.'],
    [46.75, 'Scientists ka maanna hai'], [48.34, 'ki aise wo *seekhte* hain'], [49.58, 'ki *khatra kahan* hai,'], [50.52, 'aur *kaun* hai.'],
    [51.28, 'To agli baar kauwa dikhe,'], [52.83, 'to *izzat* se pesh aaiye,'], [54.10, 'kyunki wo aapko'], [54.89, '*dekh raha hai.*'],
    [55.75, 'Aur aapke shehar ka kauwa'], [57.09, 'kitna *smart* hai?'], [58.06, '*Comment* mein bataiye.'],
  ];
  const CAP_END = 59.6;
  const CAP_FONT = 'bold 66px "Helvetica Neue", Helvetica, Arial, sans-serif';
  const AMBER = '#ffb347', CREAM = '#fff4e2';

  // the theatre surround: dark hide with the lace valance edge facing the stage
  function surround(ctx, t) {
    const g = ctx.createLinearGradient(0, 0, 0, VH);
    g.addColorStop(0, '#120703'); g.addColorStop(0.34, '#1e0d05'); g.addColorStop(0.66, '#1e0d05'); g.addColorStop(1, '#0d0502');
    ctx.fillStyle = g; ctx.fillRect(0, 0, VW, VH);
    // a faint lamp spill on the hide just above and below the screen
    const f = 1 + 0.04 * NZ.n2(t * 6.1, 0.3);
    for (const [y, dir] of [[STAGE_Y, -1], [STAGE_Y + 608, 1]]) {
      const sg = ctx.createLinearGradient(0, y, 0, y + dir * 260);
      sg.addColorStop(0, `rgba(240,140,50,${0.16 * f})`); sg.addColorStop(1, 'rgba(240,140,50,0)');
      ctx.fillStyle = sg; ctx.fillRect(0, Math.min(y, y + dir * 260), VW, 260);
    }
  }
  function captionAt(t) {
    for (let i = CAPS.length - 1; i >= 0; i--) if (t >= CAPS[i][0]) return t < (CAPS[i + 1] ? CAPS[i + 1][0] : CAP_END) ? [i, t - CAPS[i][0]] : null;
    return null;
  }
  function drawCaption(ctx, t) {
    const c = captionAt(t);
    if (!c) return;
    const [i, dt] = c, words = CAPS[i][1].split(' ').map((w) => ({ w: w.replace(/\*/g, ''), hot: w.includes('*') }));
    // join words that sit inside one *...* span
    let on = false; words.forEach((x, k) => { const raw = CAPS[i][1].split(' ')[k]; if (raw.startsWith('*')) on = true; x.hot = on; if (raw.endsWith('*') || raw.endsWith('*.') || raw.endsWith('*,')) on = false; });
    ctx.save(); ctx.font = CAP_FONT; ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round';
    const space = ctx.measureText(' ').width, lines = [[]]; let lw = 0;
    words.forEach((x) => { x.width = ctx.measureText(x.w).width; if (lw + x.width > 940 && lines[lines.length - 1].length) { lines.push([]); lw = 0; } lines[lines.length - 1].push(x); lw += x.width + space; });
    const s = 0.86 + 0.14 * H.ease.back(cl(dt / 0.16)), cy = STAGE_Y + 608 + 230;
    ctx.translate(VW / 2, cy); ctx.scale(s, s); ctx.globalAlpha = cl(dt / 0.06);
    lines.forEach((L, li) => {
      const total = L.reduce((a, x) => a + x.width, 0) + space * (L.length - 1);
      let x = -total / 2; const y = (li - (lines.length - 1) / 2) * 84 + 24;
      L.forEach((w) => {
        ctx.lineWidth = 12; ctx.strokeStyle = '#140803'; ctx.strokeText(w.w, x, y);
        ctx.fillStyle = w.hot ? AMBER : CREAM; ctx.fillText(w.w, x, y);
        x += w.width + space;
      });
    });
    ctx.restore();
  }
  function hookBar(ctx, t) {
    const a = cl(t / 0.5);
    ctx.save(); ctx.globalAlpha = a; ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
    ctx.shadowColor = 'rgba(255,150,60,0.55)'; ctx.shadowBlur = 24;
    ctx.fillStyle = '#ffcf7a'; ctx.font = `400 104px ${FF}`; ctx.fillText('Kauwa kabhi', VW / 2, STAGE_Y - 250);
    ctx.font = `italic 400 112px ${FF}`; ctx.fillText('nahi bhoolta', VW / 2, STAGE_Y - 130);
    ctx.shadowBlur = 0; ctx.fillStyle = '#c79a66'; ctx.font = `italic 400 38px ${FF}`; ctx.fillText('University of Washington research', VW / 2, STAGE_Y - 62);
    ctx.restore();
  }
  function reelFrame(ctx, t) {
    const S = lay('stage', 1280, 720), sx = S.getContext('2d');
    explainerFrame(sx, 1280, 720, t);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    surround(ctx, t);
    ctx.drawImage(S, 0, STAGE_Y, VW, 608);
    hookBar(ctx, t);
    drawCaption(ctx, t);
    ctx.save(); ctx.font = 'bold 30px "Helvetica Neue", Helvetica, Arial, sans-serif'; ctx.fillStyle = 'rgba(244,227,196,0.45)'; ctx.textAlign = 'right'; ctx.fillText('AST BTS', VW - 48, VH - 96); ctx.restore();
  }
