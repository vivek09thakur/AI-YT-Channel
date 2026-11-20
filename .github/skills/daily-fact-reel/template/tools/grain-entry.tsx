// Entry for tools/bake-grain.mjs: one 300x300 transparent tile per frame, drawn with the exact
// feTurbulence filter the Overlay used to rasterise every frame (seed = frame + 1), already at the
// Overlay's 0.1 opacity so the tile can be stacked with the vignette in one layer (black => multiply == normal).
import React from 'react';
import { Composition, registerRoot, useCurrentFrame } from 'remotion';

export const GRAIN_SVG = (seed: number) =>
  `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' seed='${seed}'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.9 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")`;

const Tile: React.FC = () => {
  const f = useCurrentFrame();
  return <div style={{ width: 300, height: 300, opacity: 0.1, backgroundImage: GRAIN_SVG(f + 1) }} />;
};
registerRoot(() => <Composition id="GrainTile" component={Tile} durationInFrames={3} fps={1} width={300} height={300} />);
