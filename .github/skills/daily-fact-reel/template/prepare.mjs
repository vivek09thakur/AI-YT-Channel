// Copies the Bengali web fonts from node_modules into public/fonts and generates the procedural SFX.
// usage: node prepare.mjs [padSeconds]   (padSeconds = total video length; the ambient pad must cover it)
import fs from 'fs';
import path from 'path';
import { execFileSync } from 'child_process';

const FONTS = [
  ['@fontsource/hind-siliguri', 'hind-siliguri-latin-600-normal.woff2'],
  ['@fontsource/hind-siliguri', 'hind-siliguri-latin-700-normal.woff2'],
  ['@fontsource/noto-serif-bengali', 'noto-serif-bengali-latin-800-normal.woff2'],
  ['@fontsource/hind-siliguri', 'hind-siliguri-bengali-600-normal.woff2'],
  ['@fontsource/hind-siliguri', 'hind-siliguri-bengali-700-normal.woff2'],
  ['@fontsource/noto-serif-bengali', 'noto-serif-bengali-bengali-800-normal.woff2'],
];
fs.mkdirSync('public/fonts', { recursive: true });
for (const [pkg, file] of FONTS) {
  const src = path.join('node_modules', pkg, 'files', file);
  if (!fs.existsSync(src)) throw new Error(`font missing: ${src} (run npm install)`);
  fs.copyFileSync(src, path.join('public/fonts', file));
}
const pad = Number(process.argv[2] || 66);
execFileSync(process.execPath, ['gen-sfx.mjs'], { stdio: 'inherit', env: { ...process.env, PAD_DUR: String(pad) } });
console.log(`fonts: ${FONTS.length} copied to public/fonts; sfx generated (pad ${Math.ceil(pad)} s)`);
