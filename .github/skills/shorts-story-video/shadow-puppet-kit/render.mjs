// Render crow_shadow_play.html to MP4 with headless Chrome.
//   NODE_PATH=<dir with puppeteer-core>/node_modules node render.mjs test     -> timing + console check, a few PNGs in debug/
//   NODE_PATH=... node render.mjs render                                     -> ../../07_Export/R16_*.mp4
//   VERTICAL=1 ... (test <t…> | render)                                       -> the 9:16 reel page instead
import { createRequire } from 'module';
import { spawn } from 'child_process';
import { writeFileSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const puppeteer = require('puppeteer-core');
const HERE = path.dirname(fileURLToPath(import.meta.url));
const VID = path.resolve(HERE, '../..');
const V = process.env.VERTICAL === '1';
const PAGE = 'file://' + path.join(HERE, V ? 'crow_shadow_play_9x16.html' : 'crow_shadow_play.html');
const FPS = 30;
const mode = process.argv[2] || 'test';

const browser = await puppeteer.launch({
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  headless: 'new', args: ['--no-first-run', '--autoplay-policy=no-user-gesture-required', '--window-size=1280,800'],
  userDataDir: process.env.CHROME_PROFILE,
});
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 800 });
const errors = [];
page.on('pageerror', (e) => errors.push(e.message));
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
await page.goto(PAGE, { waitUntil: 'load', timeout: 120000 });
await page.waitForFunction('window.READY === true', { timeout: 60000 });
const D = await page.evaluate(() => window.DURATION);

const grab = (t) => page.evaluate((t) => { window.seek(t); return document.getElementById('cv').toDataURL('image/png').split(',')[1]; }, t);

if (mode === 'test' && V) {
  for (const t of process.argv.slice(3).map(Number)) writeFileSync(path.join(HERE, `debug/v_${t}.png`), Buffer.from(await grab(t), 'base64'));
  console.log('errors', JSON.stringify(errors));
} else if (mode === 'test') {
  const ms = await page.evaluate(() => { const r = []; for (const t of [2, 15, 25, 34, 39.8, 41.2, 47, 57]) { const a = performance.now(); window.seek(t); r.push([t, +(performance.now() - a).toFixed(1)]); } return r; });
  console.log('DURATION', D, 'frame ms', JSON.stringify(ms));
  // play for a moment, then pause: the clock and the sound score must run without errors
  await page.click('#play'); await new Promise((r) => setTimeout(r, 1500)); await page.click('#play');
  console.log('after play/pause', await page.evaluate(() => document.getElementById('time').textContent), 'voice:', await page.evaluate(() => document.getElementById('vo-name').textContent));
  for (const t of process.argv.slice(3).map(Number)) writeFileSync(path.join(HERE, `debug/p_${t}.png`), Buffer.from(await grab(t), 'base64'));
  console.log('errors', JSON.stringify(errors));
} else {
  const out = path.join(VID, '07_Export');
  const frames = Math.round(D * FPS);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path.join(out, V ? 'R16_9x16_video_only.mp4' : 'R16_video_only.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let i = 0; i < frames; i++) {
    const buf = Buffer.from(await grab(i / FPS), 'base64');
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${frames}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  }
  ff.stdin.end(); await new Promise((r) => ff.on('close', r));
  // effects score, voiceover mode, rendered offline to a 16-bit stereo WAV
  const b64 = await page.evaluate(async (D) => {
    const { inter, peak, sr } = await SOUND.renderOffline(window.scoreSound, D, 48000, { voiceover: true });
    const i16 = new Int16Array(inter.length); for (let i = 0; i < inter.length; i++) i16[i] = Math.max(-1, Math.min(1, inter[i])) * 32767;
    const bytes = new Uint8Array(i16.buffer); let s = ''; for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    console.log('fx peak', peak, sr); return btoa(s);
  }, D);
  const pcm = Buffer.from(b64, 'base64'), hdr = Buffer.alloc(44);
  hdr.write('RIFF', 0); hdr.writeUInt32LE(36 + pcm.length, 4); hdr.write('WAVEfmt ', 8); hdr.writeUInt32LE(16, 16); hdr.writeUInt16LE(1, 20); hdr.writeUInt16LE(2, 22);
  hdr.writeUInt32LE(48000, 24); hdr.writeUInt32LE(48000 * 4, 28); hdr.writeUInt16LE(4, 32); hdr.writeUInt16LE(16, 34); hdr.write('data', 36); hdr.writeUInt32LE(pcm.length, 40);
  writeFileSync(path.join(VID, '05_Audio/effects.wav'), Buffer.concat([hdr, pcm]));
  console.log('done', frames, 'frames in', ((Date.now() - t0) / 1000).toFixed(0), 's; errors', JSON.stringify(errors));
}
await browser.close();
