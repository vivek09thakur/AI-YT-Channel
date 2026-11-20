// Bakes the film-grain tiles assets/grain-1.png..3.png (300x300, black + alpha at the Overlay's 0.1 opacity) once,
// using headless Chrome so they match the old per-frame feTurbulence filter. Only needed if GRAIN_SVG changes.
// Afterwards run `node prepare.mjs` (copies them to public/grain/).
// usage: node tools/bake-grain.mjs   env: BROWSER=<chrome executable> (optional)
import path from 'path';
import fs from 'fs';
import { bundle } from '@remotion/bundler';
import { renderStill, selectComposition, openBrowser } from '@remotion/renderer';

const browserExecutable = process.env.BROWSER || null;
fs.mkdirSync('assets', { recursive: true });
const serveUrl = await bundle({ entryPoint: path.resolve('tools/grain-entry.tsx') });
const browser = await openBrowser('chrome', { browserExecutable, chromiumOptions: { gl: 'swangle' } });
try {
  const composition = await selectComposition({ serveUrl, id: 'GrainTile', puppeteerInstance: browser, browserExecutable });
  for (let frame = 0; frame < 3; frame++) {
    const output = path.resolve('assets', `grain-${frame + 1}.png`);
    await renderStill({ composition, serveUrl, output, frame, imageFormat: 'png', puppeteerInstance: browser, browserExecutable });
    console.log('baked', output);
  }
} finally {
  await browser.close({ silent: true });
}
