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

Dark-section text uses `--cream` at opacity steps (`.75` primary body, `.42`-`.58` secondary, `.22`-`.32` labels/meta) rather than a separate token set. Light-section body text uses `--deep-forest` at `rgba(44,62,53,.65)`.

## Typography

- Display/headings: `Merriweather` (serif), weight 400, `letter-spacing: -.025em`, `text-transform: none`
- Body/UI: `Lato` (sans), weight 300 body copy / 700 labels & buttons
- Eyebrows and labels: 9-10px, `font-weight: 700`, `letter-spacing: .13em`-`.22em`, uppercase
- Both loaded via Google Fonts CDN, `display=swap`

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

- No `Donor Journey Mapper` component exists in the codebase (removed with the nonprofits page). The "5 inputs → 1 paragraph" interactive-tool pattern has no direct precedent to copy; closest analog is the homepage's single-input `.cs-input-zone` → `.cs-response-zone` reveal, one level simpler.
- Tracker component's connecting-line math (`left/right: calc(12.5%)`) is hardcoded for 4 phases. Needs generalizing to `50/N %` for variable phase counts before reuse on 3-phase trackers.
