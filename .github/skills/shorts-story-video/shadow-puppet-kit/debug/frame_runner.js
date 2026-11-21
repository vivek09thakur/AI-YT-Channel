  (async () => {
    try { await Promise.all(['400 104px "IM Fell English"', 'italic 400 44px "IM Fell English"', '400 190px "Libre Baskerville"'].map((f) => document.fonts.load(f, 'AaZz09'))); } catch (e) {}
    const t = parseFloat(location.hash.slice(1)) || 0, ctx = document.getElementById('c').getContext('2d');
    const t0 = performance.now(); explainerFrame(ctx, 1280, 720, t); explainerFrame(ctx, 1280, 720, t); document.title = 'ms ' + ((performance.now() - t0) / 2).toFixed(1);
  })();
