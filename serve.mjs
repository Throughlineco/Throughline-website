import { createServer } from 'http';
import { readFile } from 'fs/promises';
import { extname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const PORT = 3000;

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'application/javascript',
  '.mjs': 'application/javascript',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.webp': 'image/webp',
  '.woff2': 'font/woff2',
  '.ico': 'image/x-icon',
};

async function tryRead(path) {
  return readFile(join(__dirname, decodeURIComponent(path)));
}

createServer(async (req, res) => {
  const url = req.url === '/' ? '/index.html' : req.url;
  // mimic Vercel's cleanUrls: /about -> about.html when there's no extension
  const candidates = extname(url) ? [url] : [url, `${url}.html`];
  for (const candidate of candidates) {
    try {
      const data = await tryRead(candidate);
      const ext = extname(candidate);
      res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
      res.end(data);
      return;
    } catch {}
  }
  res.writeHead(404);
  res.end('Not found');
}).listen(PORT, () => console.log(`Server running at http://localhost:${PORT}`));
