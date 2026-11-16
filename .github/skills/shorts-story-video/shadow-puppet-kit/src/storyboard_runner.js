  const PANELS = [
    { beat: 1, t: 5.6, flow: 'Opening. The oil lamp sputters alight on a tight close-up of the crow. On "pareshan" its head card swings round on its pin to face us and the screen shakes once. SAALON slams down as a red-gel stamp, throwing hide crumbs. Three crows slide in on rods, held a little back from the cloth (softer), and all swing their heads round to face us at once.', sound: 'Lamp whump and sputter · wooden head-snap + screen thud on "pareshan" · stamp slam on "saalon" (big) · hide rustle + three rod taps as the crows arrive · bronze note when they all turn.' },
    { beat: 2, t: 10.9, flow: 'Scene change: the lamp is turned down and up (the story jumps from "you" to the research). In the dark, the campus picture is pinned to the screen: a gothic library facade cut against a sky-blue gel, a crow on the gable. The name strip rises on its rod and types itself; REAL RESEARCH stamps across the corner.', sound: 'Lamp turned down/up (low swell) · rod tap as the strip rises · soft typing while the name types · stamp slam on "sach mein test kiya".' },
    { beat: 3, t: 18.95, flow: 'Continuous: the picture is hoisted away on its string. The 2006 tag flips in at top left. The scientist in the caveman mask hops in from the right; a red-gel ring draws round the mask on "mask". Two crows hop in, a cord net drops over them and bounces; on "tag kiya" a gold leg band pops onto each. On "chhod diya" the net lifts and they fly off.', sound: 'Tag flip and tap on "2006" · hopping rod taps · brush stroke while the ring draws · net drop: rustle + thud + bounce · two ticks for the leg bands · wing flaps as they fly.' },
    { beat: 4, t: 25.7, flow: 'Continuous: the scientist walks to centre stage. On "cheekhne lagte" crows swoop in from every side and circle the masked head; four KAA! bursts pop one after another. On "jhund bana kar" three more join and the circle tightens.', sound: 'Wing flaps as they swoop (minor) · caw-like reedy bursts on each KAA! · a hide whoosh as the ring tightens.' },
    { beat: 5, t: 29.5, flow: 'Continuous, re-arranged: on "Ek dusra mask" a torn hide strip drops down the middle. The scientist and his crows slide left; a second person in the plain control mask walks in on the right. Red ❌ badge on the left, green ✅ on the right. The right-hand crows ignore him; one pecks the ground, again on "dhyan nahi diya".', sound: 'Strip drop thud · clashing bronze on ❌ (wrong) · bright double note on ✅ (right) · two small wooden pecks.' },
    { beat: 6, t: 38.1, flow: 'Scene change: lace curtains close and part (the reveal), and the lamp comes back lower. TWIST card drops and is hoisted to the corner. One crow with a gold leg band sits centre. On "kabhi pakde hi nahi gaye" hide vines grow from it to six untagged crows; each one\'s eye gel flares red as its vine arrives. SIKHA DIYA stamps across the middle. On "dushman kaun hai" the caveman mask drops in on its string and every crow swings round to glare at it.', sound: 'Curtain swish both sides · card drop + bronze note on "twist" · brush stroke per vine + a rising bronze note each time a crow lights up · stamp slam on "sikha diya" · low clash as they glare.' },
    { beat: 7, t: 40.7, flow: 'Continuous: the crows fly off, SIKHA DIYA lifts away; the mask stays and drifts back from the cloth (bigger, softer, fainter: time passing). The counter board drops and rolls the years 2006 → 2021, slowing; on "15" it lands on 15+ with SAAL swinging in beside it and "2006 → 2021+" above. A vine underline grows on "zyada". The flame flares on the hit.', sound: 'Board drop tap · wooden ticks per year, slowing (≤12/s) · the low gong on "15" (biggest hit of the reel) · brush stroke for the underline.' },
    { beat: 8, t: 50.95, flow: 'Scene change: a crow flies at the lamp until its shadow fills the screen (new study, new place). A muted, dimmer stage: a 2015 tag. On "mar jaata hai" the still crow is brought from far back to the cloth (soft to sharp): on its back, feet curled up, eyes closed. On "jama ho jaate hain" five crows come down one by one and stand round it, heads low, while the vignette closes in. A red map pin drops on "khatra kahan hai"; a faint person at the edge gets a red ? tag on "aur kaun hai".', sound: 'Wing beats + whoosh into the lamp, soft thud in the dark · near silence: only a few soft taps as crows land · single low bronze note on the pin · questioning two-note bronze on the ?.' },
    { beat: 9, t: 58.6, flow: 'Scene change: the lamp is turned down and up bright again, back on the opening crow (bookend). It tilts its head. Folded hands pop in on "izzat se pesh aaiye", then lift away. On "wo aapko dekh raha hai" we push in on its eye while WOH DEKH RAHA HAI types onto a hanging card and an eye charm swings below. On "aapke shehar ka kauwa" the crow pulls back (softer) and the question bubble rises from below and keeps bobbing to the end.', sound: 'Lamp swell · bronze pop for the hands · typing while the line types · rod tap as the bubble rises · resolving three-note bronze phrase as it lands (takeaway).' },
  ];
  const ASSUMED = [
    'Voiceover: there is no TTS in the project, so the base voice is macOS\'s built-in Hindi voice (Lekha) reading the script in Devanagari at rate 188, converted to the Rasa male voice with Seed-VC and polished with voice_polish.py (medium). Word times come from whisper on the base voice; Seed-VC keeps timing, so they carry over. 59.3 s of speech, DURATION 60.3 s.',
    'The campus picture is a generic gothic library facade (in the spirit of UW\'s Suzzallo Library), not a traced photo of a real building.',
    'The "dangerous" mask is drawn as a caveman mask and the control as a plain neutral face. In the real study the neutral mask was a Dick Cheney mask; a real person\'s face is avoided on purpose.',
    'No number of captured crows is shown (the study trapped 7 in 2006; the script does not say it).',
    '"15+ SAAL" and "2006 → 2021+" follow the script: reports in 2023 said crows were still scolding the mask about 17 years on.',
    'The dead-crow study is tagged 2015 (Swift & Marzluff, Animal Behaviour, 2015). The faint person stands for the human seen with the dead crow, whom crows then scold and avoid.',
    'The leg band is drawn gold; field bands are coloured plastic, so any colour is fair.',
    'The red "dotted arrows" in the script become the medium\'s own arrows: hide vines growing between the crows, with each crow\'s eye gel flaring red as its vine arrives. Torn-paper and paper-dust moments become lamp dips, curtains, a crow flying at the lamp and hide crumbs.',
  ];
  const fmtT = (s) => { const m = Math.floor(s / 60), r = s - m * 60; return `${m}:${r.toFixed(1).padStart(4, '0')}`; };

  async function runStoryboard() {
    const specs = ['400 104px "IM Fell English"', 'italic 400 44px "IM Fell English"', '400 190px "Libre Baskerville"'];
    try { await Promise.all(specs.map((f) => document.fonts.load(f, 'AaZz09 →'))); await document.fonts.ready; } catch (e) {  }
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
            <dt>Voice</dt><dd class="vo">${B.vo}</dd>
            <dt>How it gets here</dt><dd>${P.flow}</dd>
            <dt>Key sounds</dt><dd>${P.sound}</dd>
            <dt>Frame shown</dt><dd>t = ${P.t.toFixed(2)} s</dd>
          </dl>
        </figcaption>`);
      grid.appendChild(fig);
      const ctx = cv.getContext('2d');
      explainerFrame(ctx, 1280, 720, P.t);
      await new Promise((r) => setTimeout(r, 0));
    }
    document.getElementById('assumed').innerHTML = ASSUMED.map((a) => `<li>${a}</li>`).join('');
    window.STORYBOARD_DONE = true;
  }
  runStoryboard();
