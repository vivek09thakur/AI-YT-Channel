export const FPS = 30;
// Doodle look: black-outline stick figures on bright flat colour. Props and backgrounds carry the colour.
export const C = {
  white: '#FFFFFF', paper: '#FFF8E7', ink: '#141414', outline: '#141414', card: '#FFFFFF', grey: '#CFd4dc', shadow: '#00000022',
  yellow: '#FFD93D', orange: '#FF8C42', red: '#FF5252', pink: '#FF7BAC', purple: '#9B5DE5', blue: '#4D96FF', sky: '#BDE0FE',
  teal: '#00C2A8', green: '#6BCB77', lime: '#C5E063', brown: '#B5651D', navy: '#1B2340', night: '#141A2E', cream: '#FFF3C4',
};
export const PALETTE = [C.yellow, C.orange, C.red, C.pink, C.purple, C.blue, C.teal, C.green];
export const T = (s: number) => Math.round(s * FPS);
export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
export const SPRING = { damping: 12, stiffness: 160, mass: 0.7 };
export const BOUNCY = { damping: 8, stiffness: 190, mass: 0.6 };
export const SOFT = { damping: 18, stiffness: 90, mass: 1 };
