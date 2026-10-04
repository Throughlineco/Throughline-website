import { useState } from 'react';
import type { MouseEvent } from 'react';

export type Site = {
  href: string;
  slug: string;
  img: string;
  name: string;
  label: string;
  external: boolean;
};

// Websites we have built: expanding panels. Click (or hover on desktop) a panel to open it;
// the open panel's label links to the site. Arrows and the counter work for keyboard and touch.
export default function SitePanels({ sites }: { sites: Site[] }) {
  const [cur, setCur] = useState(0);
  const n = sites.length;
  const canHover = typeof window !== 'undefined' && window.matchMedia('(hover: hover)').matches;
  const go = (k: number) => setCur((k + n) % n);

  return (
    <section className="home-sec sites-sec" id="websites">
      <div className="home-head reveal">
        <h2 className="sites-h">Websites we have built</h2>
        <p className="sites-sub">Live now. Click a panel to see the next site, then click its name to visit it.</p>
      </div>
      <ul className="sp-row reveal">
        {sites.map((s, i) => (
          <li
            key={s.slug}
            className={`sp${i === cur ? ' on' : ''}`}
            onClick={(ev: MouseEvent) => { if (i !== cur) { ev.preventDefault(); go(i); } }}
            onMouseEnter={() => { if (canHover) go(i); }}
          >
            <img src={`/assets/work/${s.slug}/${s.img}.webp`} alt="" loading="lazy" decoding="async" />
            <a
              className="sp-label"
              href={s.href}
              {...(s.external ? { target: '_blank', rel: 'noopener' } : {})}
              onFocus={() => go(i)}
            >
              <strong>{s.name}</strong>
              <span>
                {s.label}
                {s.external && <span className="visually-hidden"> (opens in a new tab)</span>}
              </span>
            </a>
          </li>
        ))}
      </ul>
      <div className="sp-controls reveal">
        <button className="wk-arrow sp-arrow" type="button" aria-label="Previous site" onClick={() => go(cur - 1)}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" /></svg>
        </button>
        <span className="sp-count" aria-live="polite">{cur + 1} / {n}</span>
        <button className="wk-arrow sp-arrow" type="button" aria-label="Next site" onClick={() => go(cur + 1)}>
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" /></svg>
        </button>
      </div>
    </section>
  );
}
