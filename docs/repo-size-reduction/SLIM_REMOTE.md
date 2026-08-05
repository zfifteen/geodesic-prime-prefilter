# Slim published surface (Phase 6 Strategy B)

The fat historical remote `zfifteen/prime-gap-structure` remains as archive history.

## Clone target for tools (Gemini, etc.)

**Published slim remote:**

```text
https://github.com/zfifteen/prime-gap-structure-slim
```

Clone:

```bash
git clone https://github.com/zfifteen/prime-gap-structure-slim.git
```

Measured fresh clone (2026-08-05):

| Metric | Value |
| --- | --- |
| `.git` | **11 MB** |
| `size-pack` | **10.89 MiB** |
| Working tree | **41 MB** |
| HEAD tip | **25.3 MB / 2034 files** |
| `scan_checkpoints_*` | 0 |
| `/output/` dumps | 0 |

Bulk dumps: `../prime-gap-structure-artifacts` (see `MANIFEST.md`).

Stay-thin gate in this tree: `python3 scripts/check_repo_thinness.py`.
