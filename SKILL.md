---
name: yoto-icon-maker
description: Use when creating custom track or chapter icons for Yoto Player or Yoto Mini. Explore a silhouette, rebuild it on a true 16x16 grid, preview it on black, and validate the upload-ready PNG.
version: 1.0.0
author: Santi Pochat and Janus
license: MIT
metadata:
  hermes:
    tags: [yoto, pixel-art, icons, image-generation]
---

# Yoto Icon Maker

## When to use

Use for custom Yoto track icons, chapter art, and coherent icon batches. Do not use for card cover art or ordinary-resolution illustration.

## Hard constraints

- final file is PNG, exactly 16×16, and RGBA
- background is transparent
- no visible pure-black pixels
- normally four to eight opaque colors
- one-pixel safe margin where practical
- no text, gradients, texture, or tiny decorative detail

## Method

1. Infer the simplest recognizable view; do not ask about style when the display already determines it.
2. If useful, generate one concept image for silhouette reference. Never accept it as the final file.
3. Rebuild deliberately on a 16×16 RGBA canvas. Draw the silhouette first, then one to three semantic details.
4. Preview on black using nearest-neighbor enlargement.
5. Run `yoto-icon verify ICON --preview PREVIEW`.
6. Inspect the preview at display scale. Technical validity is necessary, not sufficient.
7. Deliver both the 16×16 upload file and enlarged preview.

## Batch method

Use one concrete noun or simple scene per track, keep a shared palette, author each sprite independently, number files in track order, and review a contact sheet on black.

## Pitfalls

- naive downsampling erases defining details
- pure-black outlines disappear against the display
- generated checkerboards are not transparency
- a technically valid icon can still be unreadable
- historical military objects should default to object-only, non-violent treatment

## Verification

- [ ] exact 16×16 PNG
- [ ] RGBA with transparent pixels
- [ ] no visible pure black
- [ ] compact palette
- [ ] preview rendered on black
- [ ] immediately recognizable at display scale
