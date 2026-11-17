export const FPS = 30;
export const C = {
  cream: '#E6DDCB', beige: '#DDCFB7', ink: '#2B1D14', red: '#C8451E', card: '#F6EFE8',
  night: '#1C1917', navy: '#22284A', maroon: '#3B1B22', teal: '#2C483B', outline: '#2A1A12',
  paper: '#F6EBD9', tan: '#B9A07C',
};
export const T = (s: number) => Math.round(s * FPS);
export const bn = (n: number | string) => String(n).replace(/\d/g, (d) => '০১২৩৪৫৬৭৮৯'[Number(d)]);
export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;
export const SPRING = { damping: 14, stiffness: 150, mass: 0.8 };
