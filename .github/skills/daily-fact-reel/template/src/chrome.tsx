import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Sequence, delayRender, continueRender, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, clamp } from './theme';
import { CAPS, SCENE_TAGS, Cap } from './data';
import { PAGE_NAME } from './brand';

const FONTS: [string, string, string][] = [
  ['Hind', '600', 'hind-siliguri-latin-600-normal.woff2'],
  ['Hind', '700', 'hind-siliguri-latin-700-normal.woff2'],
  ['NSB', '800', 'noto-serif-bengali-latin-800-normal.woff2'],
  ['Hind', '600', 'hind-siliguri-bengali-600-normal.woff2'],
  ['Hind', '700', 'hind-siliguri-bengali-700-normal.woff2'],
  ['NSB', '800', 'noto-serif-bengali-bengali-800-normal.woff2'],
];
const RANGE: Record<string, string> = { latin: 'U+0000-00FF, U+0100-024F, U+2000-206F, U+20A0-20CF, U+2190-21FF, U+2600-27BF', bengali: 'U+0980-09FF, U+0964-0965, U+200C-200D, U+25CC' };
export const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(FONTS.map(([f, w, u]) => new FontFace(f, `url(${staticFile('fonts/' + u)})`, { weight: w, unicodeRange: RANGE[u.includes('-latin-') ? 'latin' : 'bengali'] }).load().then((ff) => document.fonts.add(ff))))
      .then(() => continueRender(h))
      .catch(() => continueRender(h));
  }, [h]);
};

// 540x960 design space scaled to 1080x1920, with slow push-in, fade-in, grain + vignette
export const Stage: React.FC<{ dur: number; push?: number; children: React.ReactNode; bg?: string }> = ({ dur, push = 0.05, children, bg }) => {
  const f = useCurrentFrame();
  const sc = 1 + push * (f / dur);
  const op = interpolate(f, [0, 4], [0.55, 1], clamp);
  return (
    <AbsoluteFill style={{ background: bg ?? C.beige, opacity: op }}>
      <div style={{ position: 'absolute', inset: 0, transform: `scale(${sc})`, transformOrigin: '50% 58%' }}>
        <div style={{ width: 540, height: 960, transform: 'scale(2)', transformOrigin: '0 0', position: 'relative', overflow: 'hidden' }}>
          <svg width={540} height={960} viewBox="0 0 540 960" style={{ position: 'absolute', left: 0, top: 0 }}>{children}</svg>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const parse = (t: string) =>
  t.split('\n').map((line, i) => (
    <div key={i}>
      {line.split(/(\{[^}]+\})/).map((p, j) =>
        p.startsWith('{') ? <b key={j} style={{ color: C.red }}>{p.slice(1, -1)}</b> : <span key={j}>{p}</span>
      )}
    </div>
  ));

const Caption: React.FC<{ cap: Cap; len: number }> = ({ cap, len }) => {
  const f = useCurrentFrame();
  const sp = spring({ frame: f, fps: FPS, config: SPRING });
  const out = interpolate(f, [len - 5, len], [1, 0], clamp);
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 168, display: 'flex', justifyContent: 'center', opacity: Math.min(1, sp) * out, transform: `translateY(${(1 - sp) * 14}px) scale(${0.92 + 0.08 * sp})` }}>
      <div style={{ padding: '12px 24px', borderRadius: 20, background: C.card, boxShadow: '0 4px 14px #0003', fontFamily: 'Hind', fontWeight: 700, fontSize: 28, lineHeight: 1.38, color: C.ink, textAlign: 'center', whiteSpace: 'nowrap' }}>
        {cap.who && <div style={{ fontSize: 14, fontWeight: 600, color: '#8a7a68', marginBottom: 2 }}>● {cap.who}</div>}
        {parse(cap.t)}
      </div>
    </div>
  );
};

export const Overlay: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const tag = SCENE_TAGS.find((x) => t >= x.s + 0.15 && t < x.e);
  const ts = tag ? tag.s : 0;
  const tsp = spring({ frame: f - T(ts + 0.2), fps: FPS, config: SPRING });
  return (
    <AbsoluteFill>
      <div style={{ position: 'absolute', inset: 0 }}>
        <div style={{ width: 540, height: 960, transform: 'scale(2)', transformOrigin: '0 0', position: 'relative' }}>
          {String(PAGE_NAME).trim() !== '' && (
            <div style={{ position: 'absolute', left: '50%', top: 26, transform: 'translateX(-50%)', padding: '6px 26px', borderRadius: 24, background: '#f1e8d8d9', fontFamily: 'NSB', fontWeight: 800, fontSize: 17, color: C.ink, whiteSpace: 'nowrap' }}>— {PAGE_NAME} —</div>
          )}
          {tag && (
            <div style={{ position: 'absolute', left: '50%', top: 68, transform: `translateX(-50%) scale(${0.85 + 0.15 * Math.min(1, tsp)})`, opacity: Math.min(1, tsp), padding: '7px 24px 8px', borderRadius: 30, background: '#F6EFE8', border: `3px solid ${C.red}`, boxShadow: '0 4px 12px #0003', fontFamily: 'Hind', fontWeight: 700, fontSize: 27, lineHeight: 1.25, color: C.ink, whiteSpace: 'nowrap' }}>
              <i style={{ display: 'inline-block', width: 13, height: 13, borderRadius: '50%', background: C.red, marginRight: 11, verticalAlign: 'middle' }} />{tag.tag}
            </div>
          )}
          {CAPS.map((c, i) => {
            const len = T(c.e + 0.18) - T(c.s);
            return (
              <Sequence key={i} from={T(c.s)} durationInFrames={len}>
                <Caption cap={c} len={len} />
              </Sequence>
            );
          })}
        </div>
      </div>
      <FilmLook f={f} />
    </AbsoluteFill>
  );
};

// Vignette + film grain in ONE static compositor layer per grain phase. The three 300x300 tiles in public/grain/
// are the old per-frame feTurbulence filter baked once at its 0.1 opacity (tools/bake-grain.mjs); they are black
// with alpha, so the old "multiply" blend equals normal blending and the blend mode is dropped. All three layers stay
// mounted (raster cached via will-change) and only their opacity toggles with the original (f % 3) + 1 schedule.
const VIGNETTE = 'radial-gradient(ellipse at center, transparent 55%, rgba(30,15,5,0.22) 100%)';
const GRAIN_TILES = [1, 2, 3].map((i) => staticFile(`grain/grain-${i}.png`));

const useGrainPreload = () => {
  const [h] = useState(() => delayRender('grain'));
  useEffect(() => {
    Promise.all(GRAIN_TILES.map((src) => new Promise<void>((res) => { const im = new Image(); im.onload = () => res(); im.onerror = () => res(); im.src = src; })))
      .then(() => continueRender(h));
  }, [h]);
};

const FilmLook: React.FC<{ f: number }> = ({ f }) => {
  useGrainPreload();
  const cur = f % 3;
  return (
    <>
      {GRAIN_TILES.map((src, i) => (
        <AbsoluteFill key={i} style={{ opacity: i === cur ? 1 : 0, pointerEvents: 'none', backgroundImage: `url("${src}"), ${VIGNETTE}`, backgroundRepeat: 'repeat, no-repeat', backgroundSize: '300px 300px, 100% 100%', willChange: 'transform' }} />
      ))}
    </>
  );
};
