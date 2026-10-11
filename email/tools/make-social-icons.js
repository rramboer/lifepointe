#!/usr/bin/env node
/*
 * make-social-icons.js: render the email footer's social icons as PNGs.
 *
 * Draws simple geometric glyphs as inline SVG (no brand files are downloaded) and
 * rasterizes them with sharp (libvips + librsvg) to transparent PNGs:
 *
 *   icon-facebook.png   white disc with the "f" knocked out (transparent), the monochrome
 *                       white treatment of the Facebook logo; the footer navy shows through
 *   icon-instagram.png  white glyph: rounded-square outline, lens ring, flash dot
 *   icon-website.png    white globe outline (a generic icon, not a brand mark)
 *
 * The outputs are committed in email/images/, so nothing has to run before sending an
 * email. This script is only needed to change or re-render the icons.
 *
 * Usage (from the repo root; sharp lives outside the repo, nothing npm is added here):
 *
 *   mkdir -p /tmp/icon-tools && (cd /tmp/icon-tools && npm install --ignore-scripts --no-save sharp@0.35.5)
 *   NODE_TOOLS=/tmp/icon-tools node email/tools/make-social-icons.js [options]
 *
 *   --out DIR      output directory (default: email/images, next to this folder)
 *   --size N       output edge in px (default 60 = 2x for 30x30 display)
 *   --color HEX    glyph color as #RRGGBB (default #FFFFFF). Meta does not allow recoloring
 *                  the Facebook logo to your own brand colors; keep it white.
 *   --svg          also write each icon's SVG source next to its PNG
 *   --preview DIR  write preview-on-navy.png / preview-on-white.png contact sheets to DIR
 *                  (keep DIR outside email/images)
 *
 * Exits non-zero if any output fails verification (size, alpha channel, transparent
 * corners, enough glyph pixels, and for Facebook a transparent "f").
 */
'use strict';
const fs = require('fs');
const path = require('path');

function loadSharp() {
  try { return require('sharp'); } catch (e) { /* fall through */ }
  const dir = process.env.NODE_TOOLS;
  if (dir) return require(path.join(dir, 'node_modules', 'sharp'));
  throw new Error('sharp not found. Run `npm install --ignore-scripts --no-save sharp@0.35.5` in a folder outside the repo and set NODE_TOOLS to that folder.');
}

// ---------------------------------------------------------------- args
const args = process.argv.slice(2);
function arg(name, dflt) {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : dflt;
}
const OUT = path.resolve(arg('--out', path.join(__dirname, '..', 'images')));
const SIZE = parseInt(arg('--size', '60'), 10);
const COLOR = arg('--color', '#FFFFFF');
const WRITE_SVG = args.includes('--svg');
const PREVIEW = args.includes('--preview') ? arg('--preview', null) : null;
if (!/^#[0-9A-Fa-f]{6}$/.test(COLOR)) throw new Error('--color must be #RRGGBB');
if (!(SIZE >= 16 && SIZE <= 1024)) throw new Error('--size must be 16..1024');
if (args.includes('--preview') && !PREVIEW) throw new Error('--preview needs a directory');

// ---------------------------------------------------------------- glyphs
// All geometry is authored on a 60x60 grid; the SVG width/height set the raster size.
const svg = (inner) =>
  `<svg xmlns="http://www.w3.org/2000/svg" width="${SIZE}" height="${SIZE}" viewBox="0 0 60 60">${inner}</svg>`;

// Facebook: full disc, "f" cut out with a mask so it is truly transparent (the background
// colour shows through), and the stem runs out through the bottom of the disc like the
// current Facebook logo.
const F_PATH = [
  'M25.5 61', 'V36.5', 'H19.5', 'V29', 'H25.5', 'V24.5',
  'C25.5 17.6 29.3 13.5 36 13.5', 'H40.5', 'V20.6', 'H37',
  'C34.6 20.6 33.5 21.7 33.5 24', 'V29', 'H40.5', 'L39.4 36.5', 'H33.5', 'V61', 'Z',
].join(' ');
const facebook = svg(
  `<defs><mask id="m" maskUnits="userSpaceOnUse" x="0" y="0" width="60" height="60">` +
  `<rect width="60" height="60" fill="#fff"/><path d="${F_PATH}" fill="#000"/></mask></defs>` +
  `<circle cx="30" cy="30" r="29" fill="${COLOR}" mask="url(#m)"/>`
);

// Instagram: stroke weight ~9% of the glyph, ring ~ 0.4 of the glyph, dot top-right.
// The glyph spans 58 of 60 units, i.e. 29px at 30px display (Instagram's minimum size).
const instagram = svg(
  `<g fill="none" stroke="${COLOR}" stroke-width="5.2">` +
  `<rect x="3.6" y="3.6" width="52.8" height="52.8" rx="15"/>` +
  `<circle cx="30" cy="30" r="11.6"/></g>` +
  `<circle cx="44.6" cy="15.4" r="3.6" fill="${COLOR}"/>`
);

// Website: globe with an outer ring, meridian ellipse, equator and two latitude chords,
// clipped to the ring so the chords meet it cleanly.
const website = svg(
  `<defs><clipPath id="c"><circle cx="30" cy="30" r="26"/></clipPath></defs>` +
  `<g fill="none" stroke="${COLOR}" stroke-width="4.2">` +
  `<circle cx="30" cy="30" r="26"/>` +
  `<g clip-path="url(#c)"><ellipse cx="30" cy="30" rx="11" ry="26"/>` +
  `<path d="M2 30H58M2 18.5H58M2 41.5H58"/></g></g>`
);

const ICONS = { facebook, instagram, website };
const fileFor = (dir, name) => path.join(dir, `icon-${name}.png`);

// ---------------------------------------------------------------- render + verify
async function main() {
  const sharp = loadSharp();
  fs.mkdirSync(OUT, { recursive: true });
  let ok = true;
  const written = [];

  for (const [name, markup] of Object.entries(ICONS)) {
    const file = fileFor(OUT, name);
    if (WRITE_SVG) fs.writeFileSync(path.join(OUT, `icon-${name}.svg`), markup);
    await sharp(Buffer.from(markup), { density: 72 })
      .png({ compressionLevel: 9, adaptiveFiltering: true })
      .toFile(file);

    // Verify: dimensions, alpha channel, transparent corner, some opaque glyph pixels.
    const meta = await sharp(file).metadata();
    const { data, info } = await sharp(file).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    const px = (x, y) => data[(y * info.width + x) * info.channels + 3];
    let opaque = 0;
    for (let i = 3; i < data.length; i += info.channels) if (data[i] > 200) opaque++;
    const coverage = opaque / (info.width * info.height);
    const checks = {
      size: meta.width === SIZE && meta.height === SIZE,
      alpha: meta.hasAlpha === true && meta.channels === 4,
      cornerTransparent: px(0, 0) === 0 && px(SIZE - 1, 0) === 0,
      hasGlyph: coverage > 0.15,
    };
    if (name === 'facebook') {
      // the "f" must be a hole: sample inside the stem, below the crossbar
      const s = SIZE / 60;
      checks.fIsTransparent = px(Math.round(29.5 * s), Math.round(48 * s)) === 0;
    }
    const pass = Object.values(checks).every(Boolean);
    ok = ok && pass;
    const bytes = fs.statSync(file).size;
    written.push({ name, file, width: meta.width, height: meta.height, channels: meta.channels,
      bytes, coverage: +coverage.toFixed(3), checks, pass });
  }

  if (PREVIEW) {
    // Contact sheets: each icon at full size and at display size (SIZE/2), on navy and white.
    const dir = path.resolve(PREVIEW);
    fs.mkdirSync(dir, { recursive: true });
    for (const [label, bg] of [['navy', '#00205B'], ['white', '#FFFFFF']]) {
      const half = Math.round(SIZE / 2), pad = 16;
      const names = Object.keys(ICONS);
      const W = pad + names.length * (SIZE + pad) + names.length * (half + pad);
      const H = SIZE + pad * 2;
      const comps = [];
      let x = pad;
      for (const n of names) {
        comps.push({ input: fileFor(OUT, n), left: x, top: pad }); x += SIZE + pad;
      }
      for (const n of names) {
        const small = await sharp(fileFor(OUT, n)).resize(half, half).png().toBuffer();
        comps.push({ input: small, left: x, top: pad + Math.round((SIZE - half) / 2) }); x += half + pad;
      }
      await sharp({ create: { width: W, height: H, channels: 4, background: bg } })
        .composite(comps).png().toFile(path.join(dir, `preview-on-${label}.png`));
    }
  }

  console.log(JSON.stringify({ out: OUT, size: SIZE, color: COLOR, icons: written }, null, 2));
  if (!ok) { console.error('VERIFICATION FAILED'); process.exit(1); }
}

main().catch((e) => { console.error(e); process.exit(2); });
