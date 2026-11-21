import fs from 'fs';
fs.mkdirSync('public/sfx',{recursive:true});
const SR=44100;
function wav(name,samples){const n=samples.length;const b=Buffer.alloc(44+n*2);
 b.write('RIFF',0);b.writeUInt32LE(36+n*2,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);
 b.writeUInt32LE(SR,24);b.writeUInt32LE(SR*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n*2,40);
 for(let i=0;i<n;i++){b.writeInt16LE(Math.max(-1,Math.min(1,samples[i]))*32767|0,44+i*2);} fs.writeFileSync('public/sfx/'+name+'.wav',b);}
let seed=7;const rnd=()=>{seed=(seed*16807)%2147483647;return seed/2147483647*2-1;};
// tick: short soft blip
{const n=SR*0.07|0;const s=new Float32Array(n);for(let i=0;i<n;i++){const t=i/SR;s[i]=Math.sin(2*Math.PI*1400*t)*Math.exp(-t*60)*0.5;}wav('tick',s);}
// pop: pitch drop
{const n=SR*0.18|0;const s=new Float32Array(n);let ph=0;for(let i=0;i<n;i++){const t=i/SR;const f=520*Math.exp(-t*14)+120;ph+=2*Math.PI*f/SR;s[i]=Math.sin(ph)*Math.exp(-t*22)*0.7;}wav('pop',s);}
// stamp: thud + click
{const n=SR*0.5|0;const s=new Float32Array(n);let ph=0;for(let i=0;i<n;i++){const t=i/SR;const f=95*Math.exp(-t*6)+45;ph+=2*Math.PI*f/SR;s[i]=Math.sin(ph)*Math.exp(-t*9)*0.9+rnd()*Math.exp(-t*90)*0.5;}wav('stamp',s);}
// printer: rapid noise bursts
{const n=SR*1.3|0;const s=new Float32Array(n);for(let i=0;i<n;i++){const t=i/SR;const g=(Math.floor(t*38)%2===0)?1:0.25;const env=Math.min(1,t*20)*Math.min(1,(1.3-t)*12);s[i]=rnd()*0.35*g*env+Math.sin(2*Math.PI*(900+60*Math.sin(t*38*6.28))*t)*0.06*env;}wav('printer',s);}
// whoosh: filtered noise swell
{const n=SR*0.35|0;const s=new Float32Array(n);let lp=0;for(let i=0;i<n;i++){const t=i/SR;const a=0.05+0.4*Math.sin(Math.PI*t/0.35);lp+=a*(rnd()-lp);s[i]=lp*Math.sin(Math.PI*t/0.35)*1.2;}wav('whoosh',s);}
// ding: bright two-partial bell (correct answer)
{const n=SR*0.9|0;const s=new Float32Array(n);for(let i=0;i<n;i++){const t=i/SR;s[i]=(Math.sin(2*Math.PI*1318*t)*0.6+Math.sin(2*Math.PI*2637*t)*0.25)*Math.exp(-t*5)*0.7;}wav('ding',s);}
// boing: pitch wobble (jump / bounce / wrong guess)
{const n=SR*0.45|0;const s=new Float32Array(n);let ph=0;for(let i=0;i<n;i++){const t=i/SR;const f=160+90*Math.sin(2*Math.PI*9*t)*Math.exp(-t*4);ph+=2*Math.PI*f/SR;s[i]=Math.sin(ph)*Math.exp(-t*6)*0.7;}wav('boing',s);}
// drum: low tom hit (countdown second)
{const n=SR*0.35|0;const s=new Float32Array(n);let ph=0;for(let i=0;i<n;i++){const t=i/SR;const f=140*Math.exp(-t*10)+60;ph+=2*Math.PI*f/SR;s[i]=Math.sin(ph)*Math.exp(-t*8)*0.9+rnd()*Math.exp(-t*60)*0.3;}wav('drum',s);}
// tada: quick ascending arpeggio (reveal / celebration)
{const n=SR*1.1|0;const s=new Float32Array(n);const notes=[523.25,659.25,783.99,1046.5];for(let i=0;i<n;i++){const t=i/SR;let v=0;notes.forEach((f,k)=>{const on=t>k*0.09;const tt=t-k*0.09;if(on)v+=Math.sin(2*Math.PI*f*tt)*Math.exp(-tt*(k===3?3:9))*0.35;});s[i]=v;}wav('tada',s);}// pad: warm ambient; length = PAD_DUR seconds (env or argv), default 66 s. Must cover the whole video.
{const dur=Math.max(10,Math.ceil(Number(process.env.PAD_DUR||process.argv[2]||66)));const n=SR*dur|0;const s=new Float32Array(n);const notes=[110,164.81,220,277.18];for(let i=0;i<n;i++){const t=i/SR;let v=0;notes.forEach((f,k)=>{v+=Math.sin(2*Math.PI*f*t+Math.sin(t*0.3+k))*0.12+Math.sin(2*Math.PI*f*1.003*t)*0.08;});const lfo=0.75+0.25*Math.sin(2*Math.PI*t/9);const fade=Math.min(1,t/3)*Math.min(1,(dur-t)/3);s[i]=v*lfo*fade*0.5;}wav('pad',s);}

