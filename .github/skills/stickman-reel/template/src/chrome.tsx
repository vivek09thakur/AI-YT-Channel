import React, { useEffect, useState } from 'react';
import { AbsoluteFill, Sequence, delayRender, continueRender, getInputProps, interpolate, spring, staticFile, useCurrentFrame } from 'remotion';
import { C, FPS, SPRING, T, clamp } from './theme';
import { CAPS, SCENE_TAGS, Cap } from './data';
import { PAGE_NAME } from './brand';

const FONTS: [string, string, string][] = [
  ['Baloo', '600', 'baloo-2-latin-600-normal.woff2'],
  ['Baloo', '700', 'baloo-2-latin-700-normal.woff2'],
  ['Baloo', '800', 'baloo-2-latin-800-normal.woff2'],
  ['Hand', '400', 'patrick-hand-latin-400-normal.woff2'],
];
export const useFonts = () => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => {
    Promise.all(FONTS.map(([f, w, u]) => new FontFace(f, `url(${staticFile('fonts/' + u)})`, { weight: w }).load().then((ff) => document.fonts.add(ff))))
      .then(() => continueRender(h))
      .catch(() => continueRender(h));
  }, [h]);
};

// 540x960 design space scaled to 1080x1920 with a slow push-in and a short fade-in on every cut.
// The check script renders stills with inputProps {still:true}; then the push is off so frame differences measure real motion.
export const Stage: React.FC<{ dur: number; push?: number; children: React.ReactNode; bg?: string }> = ({ dur, push = 0.04, children, bg }) => {
  const f = useCurrentFrame();
  const still = Boolean((getInputProps() as { still?: boolean }).still);
  const sc = still ? 1 : 1 + push * (f / Math.max(1, dur));
  const op = still ? 1 : interpolate(f, [0, 4], [0.6, 1], clamp);
  return (
    <AbsoluteFill style={{ background: bg ?? C.paper, opacity: op }}>
      <div style={{ position: 'absolute', inset: 0, transform: `scale(${sc})`, transformOrigin: '50% 55%' }}>
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
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 172, display: 'flex', justifyContent: 'center', opacity: Math.min(1, sp) * out, transform: `translateY(${(1 - sp) * 14}px) scale(${0.92 + 0.08 * sp})` }}>
      <div style={{ padding: '10px 22px 12px', borderRadius: 18, background: C.card, border: `4px solid ${C.ink}`, boxShadow: `6px 6px 0 ${C.ink}`, fontFamily: 'Baloo', fontWeight: 700, fontSize: 28, lineHeight: 1.3, color: C.ink, textAlign: 'center', whiteSpace: 'nowrap' }}>
        {cap.who && <div style={{ fontSize: 15, fontWeight: 600, color: '#777', marginBottom: 2 }}>{cap.who}</div>}
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
            <div style={{ position: 'absolute', left: '50%', top: 24, transform: 'translateX(-50%)', padding: '4px 22px 6px', borderRadius: 24, background: C.white, border: `3px solid ${C.ink}`, fontFamily: 'Baloo', fontWeight: 800, fontSize: 17, color: C.ink, whiteSpace: 'nowrap' }}>{PAGE_NAME}</div>
          )}
          {tag && (
            <div style={{ position: 'absolute', left: '50%', top: 66, transform: `translateX(-50%) rotate(-2deg) scale(${0.85 + 0.15 * Math.min(1, tsp)})`, opacity: Math.min(1, tsp), padding: '5px 22px 7px', borderRadius: 14, background: C.yellow, border: `4px solid ${C.ink}`, boxShadow: `4px 4px 0 ${C.ink}`, fontFamily: 'Baloo', fontWeight: 800, fontSize: 26, lineHeight: 1.25, color: C.ink, whiteSpace: 'nowrap' }}>
              {tag.tag}
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
    </AbsoluteFill>
  );
};
