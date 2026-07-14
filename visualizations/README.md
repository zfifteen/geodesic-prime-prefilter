# visualizations/

Home for PGS visual surfaces. Prefer calm, claim-disciplined demos over spectacle.

## Primary (use this)

| Path | Role |
| --- | --- |
| [`index.html`](index.html) | Professional router to the right surface |
| [`library/`](library/README.md) | Catalog-first plot demos (scripts, fixtures, status metadata) |
| [`gallery/`](gallery/index.html) | Built HTML gallery for library entries (`file://` friendly) |
| [`scripts/`](scripts/) | `run_all_demos.py`, `build_gallery.py`, `lint_catalog.py` |

```bash
visualizations/library/.venv/bin/python visualizations/scripts/lint_catalog.py
visualizations/library/.venv/bin/python visualizations/scripts/run_all_demos.py
visualizations/library/.venv/bin/python visualizations/scripts/build_gallery.py
open visualizations/gallery/index.html
```

Always use the library venv Python for lint, demos, and gallery build.

## Other surfaces

| Path | Role |
| --- | --- |
| [`../website/`](../website/index.html) | Public educational course + editorial plates |
| `interactive/`, `conceptual/` | Explorers and metaphor stills (no catalog status chips) |
| `core-diagrams/`, `research/` | Historical or ad-hoc material; not the public claim gallery |
| Chapter `research/*/output/` | Probe evidence artifacts (not the public gallery by default) |
| `../media/` | Narrated media assets (not under `visualizations/video/`) |

## Boundary rule

- **Library gallery**: data-backed or schematic demos with claim discipline.
- **Website plates**: museum pedagogy (STYLE_BIBLE).
- **Historical dumps**: art/exploration only; never substitute for status-labeled entries.
- Do not dump random PNGs into `library/out/` without an `entry.json`.

## Asset truth

- Demo output: `library/out/<id>/plot.png` (+ `meta.json`).
- Gallery copies: `gallery/assets/<id>/plot.png` (build product of `build_gallery.py`).
- Do not hand-edit gallery assets; regenerate from demos.
