import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { T } from './theme';
import { TOTAL, SFX } from './data';
import { Overlay, useFonts } from './chrome';
import { SCENES } from './scenes';


export const Video: React.FC = () => {
  useFonts();
  return (
    <AbsoluteFill style={{ background: '#DDCFB7' }}>
      {SCENES.map(({ s, e, C: Comp }, i) => (
        <Sequence key={i} from={T(s)} durationInFrames={T(e) - T(s)}>
          <Comp t0={s} dur={T(e) - T(s)} />
        </Sequence>
      ))}
      <Overlay />
      <Audio src={staticFile('voice.mp3')} volume={1} />
      <Audio src={staticFile('sfx/pad.wav')} volume={0.1} />
      {SCENES.slice(1).map(({ s }, i) => (
        <Sequence key={`k${i}`} from={T(s)}>
          <Audio src={staticFile('sfx/tick.wav')} volume={0.16} />
        </Sequence>
      ))}
      {SFX.map(([n, s, v], i) => (
        <Sequence key={`x${i}`} from={T(s)}>
          <Audio src={staticFile(`sfx/${n}.wav`)} volume={v} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
