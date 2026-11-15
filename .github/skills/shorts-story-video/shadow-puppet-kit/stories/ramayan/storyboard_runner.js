  // ---------- storyboard: one key frame per beat ----------
  const PANELS = [
    { beat: 1, t: 6.5, flow: 'Night sky, stars, a sun waiting under the hills. Spears and banners rise from behind the near ridge on "the greatest war".', sound: 'Low gongs on each line, a slow rising hiss as the spears come up.' },
    { beat: 2, t: 15.5, flow: 'The sun rises and the sky turns amber. A haloed god and a mortal walk the ridge together. On "Adharma" the right side darkens and a dark crowned figure rises.', sound: 'Riser into the cut, temple bells, a sawtooth growl and a low gong for Adharma.' },
    { beat: 3, t: 22.5, flow: 'The pavilion temple of the reference, elephants in procession dress either side, king and queen inside. On "a prince was born" rays and a lotus of light open in the pavilion.', sound: 'Four ascending bells and a sparkle for the birth.' },
    { beat: 4, t: 29.0, flow: 'Rama stands with his bow before a huge sun with rotating rays. RAMA appears as a big title. The innocent kneel on either side; lotuses pop along the ground.', sound: 'Big gong + bell on RAMA, a bell per epithet.' },
    { beat: 5, t: 46.0, flow: 'Warm to dusk. On "a crown was taken away" the crown lifts off his head and fades. The palace slides out left; on "exile" the forest slides in from the right and he starts walking.', sound: 'Rising sine as the crown lifts, a rumble as the palace slides, footsteps.' },
    { beat: 6, t: 52.0, flow: 'Side-scrolling forest with three parallax layers over a river. Lakshmana, Sita, Rama walk. Sita glows gold on her line, Lakshmana glows red on his.', sound: 'Footsteps in threes, water, bells on the names.' },
    { beat: 7, t: 70.5, flow: 'Night forest, red eyes blink in the dark. Ravana rises from behind the ridge: a dark figure with a fan of crowned heads and extra arms. Golden Lanka appears across the water. Two lightning strikes; on the second the frame shakes and fire climbs the edges.', sound: 'Thunder, a growl under the rise, double gong on RAVANA, crackling fire.' },
    { beat: 8, t: 83.5, flow: 'Close-up: Rama draws the bow across the frame. Hanuman kneels on the right on "devotion". On "a promise" a gold ring opens top right with Sita in it.', sound: 'The bowstring draw as a rising band of noise, three ascending bells.' },
    { beat: 9, t: 91.5, flow: 'Four quick cuts: the Panchavati hut in the forest; the three on the shore; Hanuman arcing across the sky over the sea; Lanka burning in gold and red with smoke rising.', sound: 'A whoosh per cut, a long riser and a rush for the leap, thunder and fire for Lanka.' },
    { beat: 10, t: 101.5, flow: 'The vanara army rises from the left ridge and marches out along the stone bridge as it grows across the water toward Lanka. On "the greatest battle" arrows arc across the sky.', sound: 'Marching steps, stones landing one by one, swishes for the arrows.' },
    { beat: 11, t: 111.9, flow: 'Split sky: amber left, night right. Rama aims, Ravana looms with mace and flames. On "one warrior" Rama glows and rays spread; on "one arrow" the arrow streaks across, a white flash, Ravana and the darkness dissolve to amber.', sound: 'Gongs per line, a riser, the twang, the impact gong and sparkle.' },
    { beat: 12, t: 119.0, flow: 'The reference composition: sunrise behind the pavilion, striped clouds, pennants, the four inside. RAMAYAN lands as a gold title; three taglines follow.', sound: 'Big gong + three bells + sparkle on the title, bells on the taglines, a soft fade.' },
  ];
  const ASSUMED = [
    'There is no voice track: the narration is shown as on-screen lines, timed to about 2.1 words per second with cinematic pauses, 124.5 s total. Drop a voiceover on the player page to replace the synthesized bed.',
    'Style follows SKILL.md section 2: flat 2D vector, mid-century poster look, one warm palette per video with Hindu-tradition accents (saffron, kumkum, Rama blue, temple gold, lotus pink, tulsi green, indigo for night).',
    'Ravana is drawn with a fan of crowned heads behind the central head and two extra pairs of arms, as a silhouette; no face detail beyond the almond eyes and crown.',
    'Hanuman is the orange monkey-faced figure with a tail and mace; the vanara army reuses the same puppet smaller.',
    'The bridge, the leap and the burning of Lanka are compressed into a few seconds each, as a trailer would.',
  ];
  const fmtT = (s) => { const m = Math.floor(s / 60), r = s - m * 60; return `${m}:${r.toFixed(1).padStart(4, '0')}`; };

  async function runStoryboard() {
    const specs = ['400 104px "IM Fell English"', 'italic 400 44px "IM Fell English"'];
    try { await Promise.all(specs.map((f) => document.fonts.load(f, 'AaZz09'))); await document.fonts.ready; } catch (e) { /* draw anyway */ }
    const grid = document.getElementById('grid');
    for (const P of PANELS) {
      const B = BEATS.find((b) => b.n === P.beat);
      const fig = document.createElement('figure'); fig.className = 'panel';
      const cv = document.createElement('canvas'); cv.width = 1280; cv.height = 720;
      fig.appendChild(cv);
      fig.insertAdjacentHTML('beforeend', `
        <figcaption>
          <div class="head"><span class="num">Beat ${B.n}</span><span class="name">${B.name}</span><span class="time">${fmtT(B.t0)} – ${fmtT(B.t1)}</span></div>
          <dl>
            <dt>On screen</dt><dd class="screen">${B.screen}</dd>
            <dt>Narration</dt><dd class="vo">${B.vo}</dd>
            <dt>How it gets here</dt><dd>${P.flow}</dd>
            <dt>Key sounds</dt><dd>${P.sound}</dd>
            <dt>Frame shown</dt><dd>t = ${P.t.toFixed(2)} s</dd>
          </dl>
        </figcaption>`);
      grid.appendChild(fig);
      explainerFrame(cv.getContext('2d'), 1280, 720, P.t);
      await new Promise((r) => setTimeout(r, 0));
    }
    document.getElementById('assumed').innerHTML = ASSUMED.map((a) => `<li>${a}</li>`).join('');
    window.STORYBOARD_DONE = true;
  }
  runStoryboard();
