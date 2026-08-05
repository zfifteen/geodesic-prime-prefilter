# Baseline metrics (pre-cleanup)

**Date:** 2026-08-04  
**Branch at audit:** `issue-45-f18-004-rough-witness` (and shared object pack)  
**Remote:** `https://github.com/zfifteen/prime-gap-structure.git`  
**Plan:** [index.html](./index.html)

## Size layers

| Metric | Value |
| --- | --- |
| Working tree (`du -sh .`) | ~10 GB |
| Working tree file count | ~185,097 (excluding `.git`) |
| `.git` directory | ~530 MB |
| `git count-objects` size-pack | 468.70 MiB |
| Loose + pack object picture | count 1992; in-pack 41362 |
| GitHub `repos.size` | 343529 KB (~335 MB) |
| HEAD tracked files | 8,212 |
| HEAD tracked bytes | ~1000.7 MB |
| All-history blob payload | ~2002 MB (~14930 blobs) |

## HEAD by top-level (tracked)

| Path | Size | Files |
| --- | --- | --- |
| `docs/` | ~584.6 MB | 665 |
| `research/` | ~304.8 MB | 6,905 |
| `visualizations/` | ~49.1 MB | 113 |
| `experiments/` | ~40.4 MB | 190 |
| `website/` | ~19.8 MB | 145 |
| other (src, lean sources, scripts, …) | &lt; 2 MB | rest |

## Highest-leverage tracked fat

| Path | Size | Files | Notes |
| --- | --- | --- | --- |
| `docs/gap-structure-factor-brief-evidence/` | ~583.5 MB | 514 | mostly multiplicative-web dumps |
| `research/02-gwr-dni/` | ~213.3 MB | 5,212 | mostly `output/` |
| `.../scan_checkpoints_5e9` | ~146.6 MB | 4,000 | segment JSON flood |
| `.../scan_checkpoints_1e9` | ~32.8 MB | 900 | same pattern |
| `.../scan_checkpoints_1e8` | ~2.9 MB | 80 | same pattern |
| All tracked paths matching `/output/` | ~851.7 MB | 5,798 | ignore policy not applied to index |
| Files &gt; 1 MB | ~693.2 MB | 100 | size concentrated in few files |
| Top 50 files by size | ~614.0 MB | 50 | |

## HEAD by extension (tracked)

| Ext | Size | Count |
| --- | --- | --- |
| `.json` | ~714.9 MB | 5,580 |
| `.gz` | ~91.2 MB | 8 |
| `.png` | ~78.1 MB | 286 |
| `.csv` | ~65.7 MB | 209 |
| `.html` | ~15.8 MB | 113 |
| `.svg` | ~12.4 MB | 54 |
| `.py` | ~7.9 MB | 842 |
| `.md` | ~5.9 MB | 990 |

## Scenario estimates (HEAD tip only, not history)

| Scenario | Approx size | Approx files |
| --- | --- | --- |
| Drop factor-brief evidence | ~417 MB | ~7,698 |
| + drop all `**/output/**` | ~148 MB | ~2,155 |
| + drop large binaries/data | ~43 MB | ~2,087 |
| Code + prose core | ~14 MB | ~1,903 |

## Local-only (gitignored or untracked noise)

| Path | Size | Files |
| --- | --- | --- |
| `lean-4/.lake/` | ~7.1 GB | ~119,929 |
| `research/06-cryptology-rsa` disk (mostly vendor) | ~611 MB | ~51,908 |
| `media/` | ~504 MB | ~242 |

## Existing ignore rules (partial)

Already present in root `.gitignore` (new files only; does not untrack):

- `media/`
- `**/output/*`
- `*.jsonl`
- `lean-4/.lake/`
- selected BC vendor paths

## Clone success target

After Phases 3 to 4 (slim tip) and Phase 6 (history rewrite or clean remote):

- `du -sh .git` on fresh clone **&lt; 100 MB** (prefer **&lt; 80 MB**)
- Tracked tip roughly **15 to 45 MB**
- Tracked files roughly **1.5k-3k**
