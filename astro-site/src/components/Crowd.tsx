import { useEffect, useRef } from 'react';

// Figures walk across in forest green; one stands still in terracotta (the "somebody").
// Open Peeps illustrations. Pauses offscreen; a still frame under reduced motion.
const COLS = 15, ROWS = 7, CW = 240, CH = 324;
const SKIP = [11, 17, 72, 92, 100]; // sheet cells we never use (props we don't want on a business site)

type Walker = { cell: number; dir: 1 | -1; speed: number; y: number; x: number; phase: number; back: boolean };

const rand = (a: number, b: number) => a + Math.random() * (b - a);

export default function Crowd() {
  const wrap = useRef<HTMLDivElement>(null);
  const cv = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const el = wrap.current, canvas = cv.current;
    const ctx = canvas?.getContext('2d');
    if (!el || !canvas || !ctx) return;

    const pool: number[] = [];
    for (let i = 0; i < COLS * ROWS; i++) if (!SKIP.includes(i)) pool.push(i);
    const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const sheet = new Image(), one = new Image();
    let ready = 0, W = 0, H = 0, dpr = 1, scale = 1, walkers: Walker[] = [], raf = 0, visible = false, last = 0;

    // Two rows on one ground line: the canvas bottom is the footer edge and every figure's lower
    // edge sits below it (clipped), so nobody floats. The back row stands slightly higher.
    // Each row is a conveyor: evenly spaced figures, one direction, one speed, so the crowd never clumps or leaves gaps.
    const pick = () => pool[(Math.random() * pool.length) | 0];
    const draw = (t: number) => {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      const pw = CW * scale, ph = CH * scale;
      for (const w of walkers) {
        const sx = (w.cell % COLS) * CW, sy = ((w.cell / COLS) | 0) * CH;
        const bob = still ? 0 : Math.abs(Math.sin(t / 260 + w.phase)) * 5 * scale;
        ctx.save();
        ctx.translate(w.x + (w.dir < 0 ? pw : 0), w.y - bob);
        ctx.scale(w.dir, 1);
        ctx.drawImage(sheet, sx, sy, CW, CH, 0, 0, pw, ph);
        ctx.restore();
      }
      const w1 = 210 * scale;
      ctx.drawImage(one, W / 2 - w1 / 2, H - ph + 66 * scale, w1, ph);
    };

    const size = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = el.clientWidth; H = el.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      scale = H / 360;
      const pw = CW * scale, perRow = Math.max(5, Math.ceil(W / (pw * 0.42)));
      const span = W + pw + 20, gap = span / perRow;
      walkers = [];
      for (let row = 0; row < 2; row++) {
        for (let i = 0; i < perRow; i++) {
          const back = row === 0;
          walkers.push({
            cell: pick(), back, dir: back ? 1 : -1, speed: (back ? 38 : 44) * scale * 3,
            y: H - CH * scale + (back ? 36 : 62) * scale,
            x: -pw - 10 + i * gap + (back ? 0 : gap / 2) + rand(-gap * 0.08, gap * 0.08),
            phase: rand(0, 6.28),
          });
        }
      }
      draw(0);
    };

    const tick = (t: number) => {
      raf = 0;
      if (!visible) return;
      const dt = Math.min((t - (last || t)) / 1000, 0.05);
      last = t;
      for (const w of walkers) {
        w.x += w.dir * w.speed * dt;
        const span = W + CW * scale + 20;
        if (w.x > W + 10) { w.x -= span; w.cell = pick(); }
        else if (w.x < -CW * scale - 10) { w.x += span; w.cell = pick(); }
      }
      draw(t);
      raf = requestAnimationFrame(tick);
    };
    const start = () => { if (!raf && visible && ready === 2 && !still) { last = 0; raf = requestAnimationFrame(tick); } };
    const loaded = () => { if (++ready === 2) { size(); start(); } };
    const onResize = () => { if (ready === 2) size(); };

    const io = new IntersectionObserver((es) => { visible = es[0].isIntersecting; start(); }, { rootMargin: '200px' });
    io.observe(el);
    window.addEventListener('resize', onResize, { passive: true });
    sheet.onload = loaded; one.onload = loaded;
    sheet.src = '/assets/home/crowd.webp';
    one.src = '/assets/home/crowd-one.webp';

    return () => {
      if (raf) cancelAnimationFrame(raf);
      io.disconnect();
      window.removeEventListener('resize', onResize);
    };
  }, []);

  return (
    <div className="crowd" aria-hidden="true" ref={wrap}>
      <canvas ref={cv} />
    </div>
  );
}
