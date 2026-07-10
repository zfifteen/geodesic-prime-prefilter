# PGS Website Illustration Style Bible

Locked decisions for the saturated AI plate pack.

## Palette

- Background void: near black `#070708` to `#0e0e10`
- Champagne gold: `#c9a962`, `#e0c47a`, `#e8d5a3`
- Dim gold ink: `#8a7340`
- Soft graphite structure: `#2a2a30`, `#3a3a42`
- No bright neon cyan/magenta; no pure white floods

## Mood

- Dark luxury editorial noir
- Museum catalog / private research exhibition
- Structural-literal objects with luxury finish
- Quiet, expensive, precise

## What plates depict

- Rulers and chambers between primes
- Divisor-count bar fields
- Selected-witness landmarks
- Endpoint walls and chains
- Floor transport / reciprocal loops
- Residual fields and certificate seals
- Status chips as abstract material states (not UI screenshots)
- Generator pair as twin gold monoliths / twin marks

## Hard bans

- No people, faces, hands, silhouettes of humans
- No corporate stock, laptops, handshakes, server rooms as generic tech
- No flags, currency, brand logos
- No readable text, letters, or numbers inside the image
- No cartoon mascots

## Text policy

- Minimal in-image text: prefer none
- All teaching captions live in HTML: full 1-2 sentence captions
- Figure IDs: chapter-based (e.g. Fig. 02.04)

## Aspect ratios

- 16:9 heroes and process strips
- 1:1 concept tiles
- 3:2 process frames
- Occasional 9:16 side panels

## Consistency method

1. Generate master plates first (`plates/masters/`)
2. Use masters as `image_edit` style references for AI hero plates
3. Fill saturated density with style-locked procedural PNG plates (`assets/scripts/generate_plates.py`) using the same palette and bans
4. Same lighting language: soft gold rim, deep void, fine construction lines
5. Rebuild page HTML with `assets/scripts/build_pages.py`

## Overlay motion (site layer)

- Static AI plates underneath
- SVG/CSS overlays: traveling endpoint dots, hairline sweeps, pulse on selected witness, residual shimmer
- Never animate the raster itself unless a future session adds video

## Density

- Saturated pack: about 10-15 plates per page
- Editorial rhythm: full-bleed, figure+prose, tile grids, process strips
