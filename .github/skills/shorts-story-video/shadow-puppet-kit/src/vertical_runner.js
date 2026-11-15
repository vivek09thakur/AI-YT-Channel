  // render-only page for the 9:16 reel: window.seek(t) draws one frame
  const vctx = document.getElementById('cv').getContext('2d');
  window.seek = (t) => reelFrame(vctx, cl(t, 0, DURATION));
  window.DURATION = DURATION;
  window.scoreSound = scoreSound;
  (async () => {
    const specs = ['400 104px "IM Fell English"', 'italic 400 112px "IM Fell English"', 'italic 400 36px "IM Fell English"', '400 190px "Libre Baskerville"', '400 150px "Libre Baskerville"'];
    try { await Promise.all(specs.map((f) => document.fonts.load(f, 'AaZz09 →+'))); await document.fonts.ready; } catch (e) { /* draw anyway */ }
    window.seek(3);
    window.READY = true;
  })();
