# PGS Plot Library

Catalog-first home for **reproducible demonstration plots** of Prime Gap Structure
objects, invariants, and published evidence scoreboards.

## Layout

```text
visualizations/library/
  catalog.json           # ordered entry ids
  entries/<id>/          # demo.py + entry.json + caption.md
  fixtures/              # tiny teaching data
  out/<id>/plot.png      # generated demo output (rebuild product)
  _common/               # style, status lint, render, data helpers
  requirements.txt
  .venv/                 # local matplotlib env (optional, gitignored)

visualizations/gallery/  # built HTML site (file://)
visualizations/scripts/
  run_all_demos.py
  build_gallery.py
  lint_catalog.py
```

## What belongs here

| Kind | Location |
| --- | --- |
| Data-backed demos + status captions | this library |
| Public educational noir plates | `website/` |
| Chapter experiment artifacts | `research/<nn>-*/output/` |
| One-off visual experiments | keep out of catalog until durable |

## Quick start

```bash
# once
python3 -m venv visualizations/library/.venv
visualizations/library/.venv/bin/pip install -r visualizations/library/requirements.txt

# every change
visualizations/library/.venv/bin/python visualizations/scripts/lint_catalog.py
visualizations/library/.venv/bin/python visualizations/scripts/run_all_demos.py
visualizations/library/.venv/bin/python visualizations/scripts/build_gallery.py
open visualizations/gallery/index.html
```

## Authoring a new entry

1. Create `entries/<id>/` with `demo.py`, `entry.json`, `caption.md`.
2. Add `<id>` to `catalog.json`.
3. Caption order: observable object → mechanism → project term → status → limits.
4. Set `status`, `regime`, `claim_language` (`weak` default). Never use
   verified/validated language without `claim_language=program` and
   `has_10e18_surface=true` plus a real executed surface.
5. Run lint + demos + build.

### entry.json fields

- `id`, `title`, `tier` (0 public spine, 1 research, …)
- `status`: theorem | measured | audit | hypothesis | unresolved | invalidated | mixed | editorial | legacy
- `status_detail`, `regime`
- `claim_language`: weak | program
- `has_10e18_surface`: boolean
- `tags`, `chapter_refs`, `script`, `outputs`, `kind`

## Contract notes

- Toy `divisor_count` helpers in `_common/data.py` are teaching tools only.
  They are not PGS generator inference.
- Toy illustrations of proved objects should use status `mixed` (or `editorial`),
  not an unqualified `theorem` chip. Theorems remain in `PROOF.md`.
- Measured scoreboards must name the exact regime and whether data is a fixture
  mirror versus a live re-audit.
- Caption bodies are linted for forbidden claim words (`validated`, `verified`,
  `measured pass`, …) unless `claim_language=program` and `has_10e18_surface=true`.
- Legacy wraps copy committed chapter PNGs; regenerate chapter scripts if those sources change.
- `library/out/` is demo output; `gallery/assets/` is a build copy. Do not hand-edit gallery PNGs.

## Scaffold status

Library scaffold is in place: lint, demos, build, eight tier-0 entries
(five demos + three GWR legacy wraps). This is a teaching and documentation
spine, not full research-instrument coverage of cryptology residuals or
high-scale forensic surfaces.
