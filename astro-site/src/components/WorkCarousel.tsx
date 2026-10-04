import { useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';

export type Project = {
  slug: string;
  name: string;
  tag: string;
  text: string;
  alt: string;
};

// Selected work: featured project (image left, story right) with a thumbnail rail.
// Thumbnails, arrows or the arrow keys switch the featured project.
export default function WorkCarousel({ projects, totalCaseStudies }: { projects: Project[]; totalCaseStudies: number }) {
  const [cur, setCur] = useState(0);
  const thumbs = useRef<(HTMLButtonElement | null)[]>([]);
  const n = projects.length;

  const go = (k: number, focus = false) => {
    const next = (k + n) % n;
    setCur(next);
    const t = thumbs.current[next];
    if (t) {
      t.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' });
      if (focus) t.focus();
    }
  };
  const onKey = (ev: KeyboardEvent) => {
    if (ev.key === 'ArrowRight') { ev.preventDefault(); go(cur + 1, true); }
    if (ev.key === 'ArrowLeft') { ev.preventDefault(); go(cur - 1, true); }
  };

  return (
    <section className="wk" id="work" aria-labelledby="wk-title">
      <div className="wk-inner">
        <div className="wk-head reveal">
          <h2 className="wk-title" id="wk-title">Selected work</h2>
          <a className="wk-all" href="/work">All {totalCaseStudies} case studies →</a>
        </div>
        <div className="wk-feature reveal">
          <div className="wk-frame">
            {projects.map((p, i) => (
              <img
                key={p.slug}
                className="wk-media"
                src={`/assets/work/${p.slug}/feature.webp`}
                width={1280}
                height={800}
                alt={p.alt}
                loading={i === 0 ? 'eager' : 'lazy'}
                decoding="async"
                data-on={i === cur ? '' : undefined}
              />
            ))}
          </div>
          <div className="wk-side" aria-live="polite">
            {projects.map((p, i) => (
              <div className="wk-text" id={`wk-slide-${i}`} hidden={i !== cur} key={p.slug}>
                <p className="wk-tag">{p.tag}</p>
                <h3 className="wk-name">{p.name}</h3>
                <p className="wk-para">{p.text}</p>
                <a className="wk-link" href={`/work/${p.slug}`}>Read the case study <span aria-hidden="true">→</span></a>
              </div>
            ))}
          </div>
        </div>
        <div className="wk-rail reveal" onKeyDown={onKey}>
          <button className="wk-arrow" type="button" aria-label="Previous project" onClick={() => go(cur - 1)}>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" /></svg>
          </button>
          <ul className="wk-thumbs">
            {projects.map((p, i) => (
              <li key={p.slug}>
                <button
                  className="wk-thumb"
                  type="button"
                  aria-controls={`wk-slide-${i}`}
                  aria-current={i === cur ? 'true' : 'false'}
                  ref={(el) => { thumbs.current[i] = el; }}
                  onClick={() => go(i)}
                >
                  <img src={`/assets/work/${p.slug}/thumb.webp`} width={800} height={450} alt="" loading="lazy" decoding="async" />
                  <span>{p.name}</span>
                </button>
              </li>
            ))}
          </ul>
          <button className="wk-arrow" type="button" aria-label="Next project" onClick={() => go(cur + 1)}>
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>
      </div>
    </section>
  );
}
