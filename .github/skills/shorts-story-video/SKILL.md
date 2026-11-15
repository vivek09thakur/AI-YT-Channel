---
name: shorts-story-video
description: Create a YouTube Shorts storytelling video script and stylized flat 2D vector animation prompts (warm amber, mid-century Indian mythology art) from a given source. Use when asked to make a short, story video, narration script, or animated video (Indian mythology / epic style) from a topic, article, or text.
---

# Shorts Storytelling Video

## 1. Script

- Analyze the given source first; keep facts faithful to it.
- Open with a familiar, conversational hook that pulls the viewer in, for example: "Hello guys, have you ever wondered how this started?", "Do you know why...", "Have you ever noticed...".
- Tell the story in a clear sequence of short scenes, in a tone familiar to the viewer.
- End with a call to action asking viewers to subscribe and support, for example: "If you want to know more about <topic>, subscribe to us. We will keep posting new videos."

## 2. Animation style

Create the entire video as **stylized flat 2D vector animation** in a mid-century modern, graphic-poster look inspired by Indian mythological art (think Sanjay Patel / Ramayana-style illustration): bold geometric shapes, warm saffron-amber glow, layered silhouettes.

- Palette: dominant warm gradient of amber, saffron, burnt orange and deep brown, plus colors rooted in Hindu tradition as accents. Keep one palette per video.
  - Saffron / kesari (sacred fire, renunciation, dharma) and turmeric yellow (auspicious, Vishnu's pitambara).
  - Kumkum / vermilion red (shakti, marriage, devotion) and marigold orange (offerings, festivals).
  - Krishna / Rama blue (Vishnu avatars, infinity) and peacock teal (Krishna's peacock feather).
  - Temple gold and brass (Lakshmi, wealth, divinity) and sandalwood cream (purity, peace).
  - Lotus pink (Lakshmi, Saraswati), tulsi / leaf green (nature, Hanuman's land) and deep maroon (royalty, Durga).
  - Ash white (Shiva's vibhuti) with Shiva-blue/indigo for night and celestial scenes; black only for demons and Kali-style fierce figures.
- Characters: simplified geometric figures with angular limbs, large almond eyes in profile or three-quarter view, pointed noses, minimal faces, stylized Indian costume, crown, jewelry and bow shapes. Skin tones can be flat blue, red, cream or brown by character.
- Shading: flat color fills with soft gradients only; no realistic textures, no 3D rendering, no photoreal lighting.
- Environments: temples with domes, tiered roofs and pillars, pennant flags, rolling hills, built from layered flat shapes; the sky is filled with scalloped clouds drawn with thin horizontal stripe lines.
- Lighting: a glowing sunset or sunrise haze that tints the whole frame; depth comes from overlapping layers, not from shadows.
- Motion: limited-animation feel, with parallax layer drifts, drifting clouds, slow pans and zooms, cut-out style character movement, and graphic scene transitions (wipes, shape reveals).
- Camera: poster-like compositions, wide establishing shots, symmetrical framing, slow push-ins on key moments.
- Every frame should look like a framed illustration from a stylized Indian epic art book, not a photo or a 3D render.
- Keep faces, costumes, proportions and palette consistent across the whole video.
- Turn narration into action: show characters doing things, not static images.
- Format: vertical 9:16 for YouTube Shorts; keep main characters and action centered and visible.

## 3. Avoid

3D CGI, realistic or semi-realistic rendering, photoreal textures, cluttered detail, off-palette colors, static slides, inconsistent characters, random visual changes.

## 4. Output format

1. Script (hook, story, subscribe call).
2. Character sheet (fixed look per character, reused in every scene prompt).
3. Scene list: narration line + visual prompt applying section 2 + camera + duration.

## 5. Shadow puppet option

For a fully code-drawn video (no AI image generation), use the bundled kit in `shadow-puppet-kit/` and follow its `README.md` (browser player, 16:9 and 9:16 render, synthesized sound). `stories/ramayan/` is a complete example of the flat 2D poster style from section 2 (a 2 minute Ramayan trailer); copy it to `stories/<name>/` and replace the timeline and scenes with the user's script. The original `src/` crow story keeps the black shadow-puppet look.

