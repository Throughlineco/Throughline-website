# Design

## Visual Theme

Editorial brand-strategy studio site. Warm cream section backgrounds alternate with a deep forest dark section for the "live case study" proof moments — the one place the site goes dark and dense, reserved for demonstrated work rather than pitch copy. Committed color strategy: terracotta is the single active-state, CTA, and "this is happening now" signal used sparingly against cream/forest neutrals.

## Color Palette

```css
--cream:       #F5F0E8;  /* primary section background */
--cream-d:     #EDE8DC;  /* secondary/alternating background */
--deep-forest: #2C3E35;  /* ink on cream; dark section background */
--sage-green:  #3D6B4F;  /* secondary accent, tracker line, nav progress */
--muted-sage:  #8BA888;  /* tertiary/muted accent, upcoming-state outline */
--terracotta:  #C2714F;  /* single active accent: CTAs, active phase, live-dot, cursor */
```

Dark-section text uses `--cream` at opacity steps: `.75` primary body copy, `.42`-`.58` secondary/supporting text (stat captions, contact details), `.22`-`.32` eyebrows/section labels specifically (tight-tracked uppercase tags — not every small dark-section string, just that specific role).

Light-section body text uses `--deep-forest` at two documented steps: `.68` for subheads/intros (shorter supporting text directly under a headline) and `.78` for reading body copy (longer paragraphs). One page (`index.html` `.founder-body`, `about.html` `.story-body`) deliberately runs darker at `.82` for long personal-narrative copy — a legitimate third tier, not drift. `index.html`'s hero body text over the photographic hero image is a deliberate exception at `.92` plus a text-shadow, since flat opacity steps calibrated for solid-color sections aren't legible over a busy photo background.

## Typography

- Display/headings: `Merriweather` (serif), weight 400 (including italic emphasis lines), `letter-spacing: -.025em`, `text-transform: none`. Weight 700 Merriweather is not part of the system — if you see it, it's drift, not a variant.
- Body/UI: `Lato` (sans), weight 300 body copy / 700 labels & buttons. This pairing is deliberate brand identity (documented here on purpose), not a generic-font reflex — don't swap it out based on a mechanical "overused font" scanner flag alone.
- Eyebrows and labels: 10px, `font-weight: 700`, `letter-spacing: .22em` uppercase — one canonical value, not a range. (A few instances drifted to `.18em`/`.2em` over time; treat any new one that isn't `.22em` as a bug.)
- Real reading copy (paragraphs, descriptions, case-study intros) has a 14px floor. Labels/eyebrows/meta text are the only things allowed below that.
- Both loaded via Google Fonts CDN with the full weight/style set every page needs: `Lato:ital,wght@0,300;0,400;0,700;0,900;1,300;1,400` + `Merriweather:ital,wght@0,400;1,300;1,400`, `display=swap`. Keep every page's `<link>` identical to this even if a given page doesn't currently use every weight — a page-specific subset silently breaks the moment that page's copy needs a weight it didn't preload.
- `discovery.html`'s `.color-hex` label uses `font-family: monospace` to display literal hex codes — an intentional, narrow exception for a technical/code-like value, not a second brand typeface.

## Layout & Spacing

- Section horizontal padding: 80px desktop, 24px mobile (720px breakpoint)
- Cards/panels: rounded 14px, never nested
- Tracker phase grid: `repeat(N, 1fr)` where N = phase count (currently hardcoded to 4; generalize for 3-phase trackers)
- Two-column hero: text column + image column, image gets gradient overlay + tint layer

## Components

**Nav**: fixed, cream/blur background, uppercase 9.5px tracked links, terracotta `.active` state, hamburger + full-screen mobile overlay on the deep-forest background, staggered link entrance.

**Tracker (live case study)**: config-driven — a JS object array of `{ label, title, state, statusText, body }` phases rendered into `.tracker-phase` nodes. States: `complete` (terracotta filled circle + checkmark), `in-progress` (terracotta ring, pulsing animation, filled dot), `next` (sage ring, hollow), `upcoming` (faint cream ring, hollow). A connecting line fills via `IntersectionObserver` to the in-progress phase's position. `.tracker-meta` shows last-updated/next-update dates. Lives inside a dark-forest section (`.s-casestudy`) with soft radial-gradient glows.

**Buttons**: `.btn-terra` — pill radius, terracotta fill, cream text, uppercase 12px bold tracked, hover = opacity .85 + translateY(-2px).

**Cookie banner**: fixed bottom, deep-forest background, Consent Mode v2 wired to GA4 + LinkedIn Insight, accept/decline pill buttons.

**Scroll reveal**: `.reveal` class + staggered `transition-delay` inline styles, IntersectionObserver-driven (pattern used everywhere; check existing JS for the observer before adding a new one).

**Custom cursor**: 10px terracotta dot following the pointer on fine-pointer devices, default cursor hidden.

## Motion

- Transform/opacity only, no layout-property animation
- Scroll-triggered reveals with per-element stagger delays
- Pulsing glow on "live"/"in-progress" indicators (`pulse-live`, `pulse-phase` keyframes) — signals "this is active right now"
- No reduced-motion media query currently present in the codebase; new components should add one even though the existing pattern doesn't (don't propagate the gap)

## Known Gaps

- No `Donor Journey Mapper` component exists in the codebase (removed with the nonprofits page). The Perception Gap Detector on `for-established-brands.html` (5 inputs → 1 templated paragraph + a 3-circle SVG diagram) is the current closest pattern for this kind of tool; copy its structure rather than the old homepage single-input tool if building another.
- Tracker component (`renderTracker(prefix, config)`) is already generalized for variable phase counts (3 or 4), used across 5 independent instances on two pages. Grid columns and connecting-line position are set per-instance via JS (`50/N %`), not hardcoded.
