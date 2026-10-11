#!/usr/bin/env node
/*
 * make-social-icons.js: render the email footer's social icons as PNGs.
 *
 * Draws the official logo shapes as inline SVG (Simple Icons 16.35.0 tracings of the current
 * Facebook and Instagram logos, CC0, copied into this file) and rasterizes them with sharp
 * (libvips + librsvg) to transparent PNGs:
 *
 *   icon-facebook.png   white disc with the "f" knocked out (transparent), the monochrome
 *                       white treatment of the Facebook logo; the footer navy shows through
 *   icon-instagram.png  the white Instagram glyph
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

// Official shapes: Simple Icons 16.35.0 "facebook" and "instagram" (CC0), 24-unit paths.
// Each is scaled to span 58 of the 60 units, i.e. 29px at the 30px display size, which is
// Instagram's minimum. The Facebook path is the disc with the "f" left out, so the "f" is
// truly transparent and the footer navy shows through it. Never recolor these: Meta's rules
// allow white (or black) monochrome, not brand colors.
const FB_PATH = 'M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z';
const IG_PATH = 'M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077';
const official = (d) => svg(`<path transform="translate(1 1) scale(${58 / 24})" d="${d}" fill="${COLOR}"/>`);
const facebook = official(FB_PATH);
const instagram = official(IG_PATH);

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
