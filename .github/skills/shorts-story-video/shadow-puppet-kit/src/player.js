  // ---------- player ----------
  // With a voiceover loaded the audio element is the clock; without one the page keeps its own.
  const cv = document.getElementById('cv'), ctx = cv.getContext('2d');
  const $ = (id) => document.getElementById(id);
  const fmt = (s) => { const m = Math.floor(s / 60), r = s - m * 60; return `${m}:${r.toFixed(1).padStart(4, '0')}`; };
  let playing = false, clockT = 0, clockAt = 0, stopSound = null, audio = null, lastDrawn = -1;

  function draw(t) {
    t = cl(t, 0, DURATION);
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    explainerFrame(ctx, 1280, 720, t);
    lastDrawn = t;
    $('scrub').value = t; $('time').textContent = `${fmt(t)} / ${fmt(DURATION)}`;
  }
  // audio clock while the voice runs; our own clock before it loads and after it ends
  function now() {
    if (playing && audio && !audio.paused && !audio.ended) return audio.currentTime;
    return playing ? clockT + (performance.now() - clockAt) / 1000 : clockT;
  }
  function soundOff() { if (stopSound) { stopSound(); stopSound = null; } }
  function soundOn(t) { soundOff(); window.SOUND_FROM = t; if ($('sound').checked) stopSound = SOUND.live(scoreSound, t, { voiceover: true }); window.SOUND_FROM = 0; }
  function startAt(t) {
    clockT = t; clockAt = performance.now();
    if (audio) { audio.currentTime = Math.min(t, audio.duration || t); if (t < (audio.duration || 0)) audio.play().catch(() => {}); }
    soundOn(t);
  }
  function play() { if (playing) return; playing = true; $('play').textContent = 'Pause'; if (clockT >= DURATION - 0.01) clockT = 0; startAt(clockT); }
  function pause() { if (!playing) return; clockT = now(); playing = false; $('play').textContent = 'Play'; if (audio) audio.pause(); soundOff(); }
  function seek(t) {
    clockT = cl(t, 0, DURATION); clockAt = performance.now();
    if (audio) audio.currentTime = Math.min(clockT, audio.duration || clockT);
    if (playing) { soundOff(); startAt(clockT); }
    draw(clockT);
  }
  function tick() {
    if (playing) {
      let t = now();
      if (t >= DURATION) {
        if ($('loop').checked) { soundOff(); startAt(0); t = 0; }
        else { t = DURATION; pause(); clockT = DURATION; }
      }
      draw(t);
    }
    requestAnimationFrame(tick);
  }

  function loadVoice(src, name) {
    if (audio) { audio.pause(); URL.revokeObjectURL(audio.src); }
    audio = new Audio(src); audio.preload = 'auto';
    // the voice ends before DURATION: carry on from its end on our own clock
    audio.addEventListener('ended', () => { if (playing) { clockT = audio.duration; clockAt = performance.now(); } });
    $('vo-name').textContent = name;
    if (playing) { const t = clockT = now(); clockAt = performance.now(); audio.addEventListener('loadedmetadata', () => { if (playing) { audio.currentTime = Math.min(t, audio.duration); audio.play().catch(() => {}); } }, { once: true }); }
  }
  $('vo').addEventListener('change', (e) => { const f = e.target.files[0]; if (f) loadVoice(URL.createObjectURL(f), f.name); });
  const stageEl = $('stage');
  ['dragenter', 'dragover'].forEach((ev) => stageEl.addEventListener(ev, (e) => { e.preventDefault(); stageEl.classList.add('drop'); }));
  ['dragleave', 'drop'].forEach((ev) => stageEl.addEventListener(ev, () => stageEl.classList.remove('drop')));
  stageEl.addEventListener('drop', (e) => { e.preventDefault(); const f = [...e.dataTransfer.files].find((x) => x.type.startsWith('audio/')); if (f) loadVoice(URL.createObjectURL(f), f.name); });

  $('play').addEventListener('click', () => (playing ? pause() : play()));
  cv.addEventListener('click', () => (playing ? pause() : play()));
  $('scrub').max = DURATION;
  $('scrub').addEventListener('input', (e) => seek(parseFloat(e.target.value)));
  $('sound').addEventListener('change', () => { if (!$('sound').checked) soundOff(); else if (playing) soundOn(now()); });
  document.addEventListener('keydown', (e) => { if (e.code === 'Space' && e.target.tagName !== 'INPUT') { e.preventDefault(); playing ? pause() : play(); } });

  // for frame-by-frame rendering
  window.seek = (t) => { pause(); clockT = cl(t, 0, DURATION); draw(clockT); };
  window.DURATION = DURATION;
  window.scoreSound = scoreSound;
  window.BEATS = BEATS;

  (async () => {
    const specs = ['400 104px "IM Fell English"', 'italic 400 44px "IM Fell English"', 'italic 400 36px "IM Fell English"', '400 190px "Libre Baskerville"', '400 150px "Libre Baskerville"'];
    try { await Promise.all(specs.map((f) => document.fonts.load(f, 'AaZz09 →+'))); await document.fonts.ready; } catch (e) { /* draw anyway */ }
    if (window.VOICE_DATA_URL) loadVoice(window.VOICE_DATA_URL, 'voice: Seed-VC Rasa male (built in)');
    draw(0.9);
    clockT = 0;
    window.READY = true;
    requestAnimationFrame(tick);
  })();
