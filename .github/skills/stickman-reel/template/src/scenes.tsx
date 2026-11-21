import React from 'react';
import { Stage } from './chrome';
import { C } from './theme';
import { SP, useT, sp, ramp, shake, Flat, Spot, Sky, Space, Stage3, Ground, GROUND, mouthOpen } from './kit';
import { Stick, Crowd } from './figures';
import { pop, Big, Label, Counter, QMark, Exclaim, Check, Heart, Star, Arrow, Draw, Sun, Planet, Earth, Clock, Bars, Sign, Confetti, LikeIcon, FollowIcon, CommentIcon, Stamp } from './props';

// Every scene: <Stage dur={dur}> + a background + at least one <Stick> that moves. t0 = absolute start second.

// 0.0-5.32 hook question: host runs in and wonders, "DID YOU KNOW?", planets pop in one by one
const S0: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const x = 40 + 120 * ramp(f, 0, 18);
  return (
    <Stage dur={dur}>
      <Space f={f} />
      <Ground color={C.navy} />
      <Big x={270} y={170} text="DID YOU KNOW?" k={pop(f, lf(0.8))} size={52} color={C.yellow} />
      <Planet x={430} y={300} r={40} color={C.teal} ring spin={0.3} stripes k={pop(f, lf(1.6))} />
      <Planet x={320} y={400} r={28} color={C.red} spin={0.4} face k={pop(f, lf(2.0))} />
      <Earth x={440} y={500} r={32} k={pop(f, lf(2.4))} />
      <QMark x={300} y={260} k={pop(f, lf(3.2))} size={110} color={C.pink} />
      <Star x={120} y={240} s={1.1} seed={1} /><Star x={500} y={170} s={0.8} seed={2} color={C.pink} />
      <Stick x={x} y={GROUND} s={1.05} pose={f < 18 ? 'run' : 'think'} face={f < 18 ? 'happy' : 'think'} shirt={C.blue} talk={mouthOpen('host', t)} />
    </Stage>
  );
};

// 5.32-7.32 answer: VENUS stamp, confetti, host cheers
const S1: React.FC<SP> = ({ t0, dur }) => {
  const { f, t } = useT(t0);
  return (
    <Stage dur={dur}>
      <Spot color={C.pink} />
      <Ground color={C.purple} />
      <Confetti k={pop(f, 2)} n={40} seed={3} cy={380} />
      <Stick x={270 + shake(f, 0, 6)} y={GROUND} s={1.1} pose="cheer" face="laugh" shirt={C.blue} talk={mouthOpen('host', t)} />
      <Planet x={270} y={220} r={60} color={C.orange} stripes spin={-0.8} k={pop(f, 0)} />
      <Stamp x={270} y={250} text="VENUS!" k={pop(f, 3)} color={C.red} rot={-8} />
      <Check x={450} y={170} k={pop(f, 8)} s={1.3} />
    </Stage>
  );
};

// 7.32-11.97 sun rises in the west: sun arcs right->left, host explains
const S2: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const p = ramp(f, 8, dur - 8);
  const sx = 470 - 400 * p, sy = 420 - Math.sin(p * Math.PI) * 260;
  return (
    <Stage dur={dur}>
      <Sky f={f} sky={C.navy} ground={C.orange} clouds={false} />
      <Sun x={sx} y={sy} s={0.9} />
      <g transform="translate(470,540)"><Sign text="WEST" color={C.yellow} w={100} /></g>
      <g transform="translate(70,540)"><Sign text="EAST" color={C.teal} w={100} /></g>
      <Arrow from={[420, 170]} to={[120, 170]} k={pop(f, lf(8.2))} color={C.white} curve={-60} />
      <Stick x={270} y={GROUND} s={1} pose="explain" face="happy" shirt={C.blue} talk={mouthOpen('host', t)} />
    </Stage>
  );
};

// 11.97-16.55 one day = 243 Earth days: counter + fast clock, host dozes then wakes
const S3: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  return (
    <Stage dur={dur}>
      <Flat color={C.sky} />
      <Ground color={C.green} />
      <Clock x={120} y={240} r={60} k={pop(f, 2)} speed={14} />
      <Counter x={330} y={260} to={243} k={ramp(f, lf(13.4), lf(15.6))} size={92} color={C.red} />
      <Label x={330} y={330} text="Earth days = 1 Venus day" k={pop(f, lf(13.2))} size={22} />
      <Stick x={270} y={GROUND} s={1} pose={t < 14.6 ? 'sit' : 'shrug'} face={t < 14.6 ? 'sleepy' : 'surprised'} shirt={C.blue} talk={mouthOpen('host', t)} />
      <Planet x={450} y={470} r={40} color={C.orange} stripes spin={-0.3} />
    </Stage>
  );
};

// 16.55-19.48 day longer than year: bars compare
const S4: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  return (
    <Stage dur={dur}>
      <Flat color={C.cream} />
      <Ground color={C.brown} />
      <Bars x={300} y={560} values={[243, 225]} labels={['1 DAY', '1 YEAR']} k={pop(f, 4)} w={80} h={260} colors={[C.red, C.blue]} gap={50} />
      <Exclaim x={210} y={200} k={pop(f, lf(17.2))} size={100} />
      <Stick x={110} y={GROUND} s={0.95} pose="pointup" face="surprised" shirt={C.blue} talk={mouthOpen('host', t)} />
    </Stage>
  );
};

// 19.48-24.33 collision: a rock slams in, planet flips upside down
const S5: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const hit = lf(21.0);
  const rockX = f < hit ? 560 - (560 - 300) * ramp(f, lf(19.8), hit) : 300;
  const flip = 180 * sp(f - hit);
  return (
    <Stage dur={dur}>
      <Space f={f} color={C.night} />
      <g transform={`translate(270,330) rotate(${flip})`}><Planet x={0} y={0} r={80} color={C.orange} stripes face spin={f < hit ? 0.5 : -0.5} /></g>
      {f < hit + 12 && <g transform={`translate(${rockX},${240 - 120 * ramp(f, lf(19.8), hit)})`}><circle r={30} fill={C.grey} stroke={C.outline} strokeWidth={5} /><circle cx={-8} cy={-6} r={6} fill="#00000022" /></g>}
      {f >= hit && <Star x={330} y={300} s={2.2 * (1 - ramp(f, hit, hit + 14))} color={C.yellow} twinkle={false} />}
      <Ground color={C.purple} />
      <Stick x={110 + shake(f, hit, 10)} y={GROUND} s={0.9} pose={f < hit ? 'explain' : 'facepalm'} face={f < hit ? 'neutral' : 'surprised'} shirt={C.blue} talk={mouthOpen('host', t)} />
    </Stage>
  );
};

// 24.33-29.26 hotter than Mercury: sun, Venus with heat waves, small Mercury, HOTTER! stamp, host wipes brow
const S6: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  const heat = ramp(f, lf(25.0), lf(26.0));
  return (
    <Stage dur={dur}>
      <Spot color={C.orange} spot="#ffffff55" y={300} />
      <Ground color={C.brown} />
      <Sun x={90} y={180} s={0.8} />
      <Planet x={270} y={340} r={55} color={C.orange} stripes spin={-0.4} k={pop(f, 2)} />
      <Label x={270} y={425} text="VENUS" k={pop(f, 4)} size={22} />
      <g opacity={heat}>
        <Draw d="M225 262 q11 -16 22 0 t22 0 t22 0 t22 0" k={heat} len={120} color={C.red} width={5} />
        <Draw d="M235 240 q11 -16 22 0 t22 0 t22 0" k={heat} len={90} color={C.red} width={5} />
      </g>
      <Planet x={440} y={370} r={30} color={C.grey} k={pop(f, lf(27.0))} />
      <Label x={440} y={430} text="MERCURY" k={pop(f, lf(27.0))} size={20} />
      <Stamp x={270} y={350} text="HOTTER!" k={pop(f, lf(27.3))} color={C.red} rot={-10} />
      <Stick x={110} y={GROUND} s={0.9} pose={t < 26.2 ? 'explain' : 'facepalm'} face={t < 26.2 ? 'neutral' : 'surprised'} shirt={C.blue} talk={mouthOpen('host', t)} />
    </Stage>
  );
};

// 29.26-35.95 CTA: like / comment / follow icons, host dances, crowd cheers; holds to the end
const S7: React.FC<SP> = ({ t0, dur }) => {
  const { f, t, lf } = useT(t0);
  return (
    <Stage dur={dur}>
      <Stage3 color={C.purple} />
      <Confetti k={ramp(f, lf(32.0), lf(32.8))} n={30} seed={7} cy={300} />
      <LikeIcon x={110} y={190} k={pop(f, lf(29.5))} s={1.3} />
      <CommentIcon x={270} y={190} k={pop(f, lf(30.2))} s={1.3} />
      <FollowIcon x={430} y={190} k={pop(f, lf(30.9))} s={1.3} />
      <Big x={270} y={275} text="FOLLOW FOR MORE" k={pop(f, lf(31.4))} size={38} color={C.yellow} />
      <Crowd x={270} y={GROUND} n={3} s={0.55} gap={120} pose="cheer" face="laugh" shirts={[C.red, C.green, C.pink]} />
      <Stick x={270} y={GROUND} s={0.9} pose="dance" face="laugh" shirt={C.blue} talk={mouthOpen('host', t)} />
      <Heart x={460} y={400} k={pop(f, lf(32.2))} s={1.1} />
    </Stage>
  );
};

export const SCENES: { s: number; e: number; C: React.FC<SP> }[] = [
  { s: 0.0, e: 5.32, C: S0 },
  { s: 5.32, e: 7.32, C: S1 },
  { s: 7.32, e: 11.97, C: S2 },
  { s: 11.97, e: 16.55, C: S3 },
  { s: 16.55, e: 19.48, C: S4 },
  { s: 19.48, e: 24.33, C: S5 },
  { s: 24.33, e: 29.26, C: S6 },
  { s: 29.26, e: 35.95, C: S7 },
];
