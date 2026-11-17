// Render several still frames with one bundle and one browser (much faster than `remotion still` per frame).
// usage: node tools/stills.mjs <outDir> <frame> [frame...]   env: BROWSER=<chrome executable> (optional)
import path from 'path';
import fs from 'fs';
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition, openBrowser } from '@remotion/renderer';

const [outDir, ...frameArgs] = process.argv.slice(2);
if (!outDir || frameArgs.length === 0) {
  console.error('usage: node tools/stills.mjs <outDir> <frame> [frame...]');
  process.exit(2);
}
const frames = frameArgs.map((f) => Math.max(0, Math.round(Number(f))));
fs.mkdirSync(outDir, { recursive: true });
const browserExecutable = process.env.BROWSER || null;

const serveUrl = await bundle({ entryPoint: path.resolve('src/index.ts'), publicDir: path.resolve('public') });
const browser = await openBrowser('chrome', { browserExecutable, chromiumOptions: { gl: 'swangle' } });
try {
  const composition = await selectComposition({ serveUrl, id: 'StoryVideo', puppeteerInstance: browser, browserExecutable });
  const total = composition.durationInFrames;
  for (const f of frames) {
    const frame = Math.min(total - 1, f);
    const output = path.join(outDir, `f_${String(frame).padStart(5, '0')}.png`);
    await renderStill({ composition, serveUrl, output, frame, imageFormat: 'png', puppeteerInstance: browser, browserExecutable, timeoutInMilliseconds: 60000 });
    console.log(`still ${frame}/${total} -> ${output}`);
  }
  console.log(`done ${frames.length} stills; composition ${composition.width}x${composition.height} ${total} frames @${composition.fps}`);
} finally {
  await browser.close({ silent: true });
}
