// After the Astro build: copy the still-static pages and assets from the repo root into astro-site/dist.
// Astro output wins; nothing already in dist is overwritten.
import { cpSync, readdirSync, statSync } from 'node:fs';
const OUT = 'astro-site/dist', EXT = /\.(html|png|jpe?g|webp|svg|txt|xml|pdf|ico)$/i;
for (const name of readdirSync('.')) {
  const isFile = statSync(name).isFile();
  if (isFile ? EXT.test(name) && !/^Screenshot/.test(name) : name === 'work' || name === 'assets')
    cpSync(name, `${OUT}/${name}`, { recursive: true, force: false, errorOnExist: false });
}
