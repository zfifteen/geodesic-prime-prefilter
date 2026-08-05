# Repo size reduction — STATUS

**Status:** phases 0 to 7 executed (2026-08-05).

## Outcome

| Metric | Before | After (slim surface) |
| --- | --- | --- |
| Fresh clone `.git` | ~469 MB pack / ~335 MB GitHub | **~18 MB** |
| HEAD tracked tip | ~1001 MB / 8212 files | **~34 MB / ~2165 files** (branch); slim export **~25 MB / 2029 files** |
| `scan_checkpoints_*` tracked | ~4980 files | **0** |
| Tracked `/output/` dumps | ~5798 | **0** |

## Published slim remote (Strategy B)

- GitHub: https://github.com/zfifteen/prime-gap-structure-slim
- Local bare (machine): see `SLIM_REMOTE.md`
- Fat origin `zfifteen/prime-gap-structure` retained as archive history (not force-rewritten)

## Sibling bulk store

`../prime-gap-structure-artifacts` with `MANIFEST.md` (hashes for moved dumps).

## Stay-thin controls

- Root `.gitignore` strengthened (outputs, checkpoints, dumps, vendor, plates, generated viz)
- `scripts/check_repo_thinness.py` + `tests/python/test_repo_thinness.py`
- CI: `.github/workflows/repo-thinness.yml`

## Branch

Work landed on `chore/repo-size-slim-tip` in the main working clone.

## History rewrite (2026-08-05)

Git history cleaned with `git filter-repo`:

- Removed historical `**/output/**`, `**/scan_checkpoints_*/**`, `pgs-math-explainer`, `media`, `*.jsonl` / `*.jsonl.gz` paths
- Stripped remaining blobs larger than 512 KiB
- Force-pushed all branches and tags

| Metric | Before (approx) | After (fresh full clone) |
| --- | --- | --- |
| `size-pack` | ~337–469 MiB | **~31 MiB** |
| Full clone `.git` | hundreds of MB | **~32 MB** |
| Tip tree | ~34 MB / ~2177 files | unchanged scale |

Pre-rewrite mirror backup (do not delete until confident):

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure-history-backup-20260805.git
```

Bulk research dumps remain in `../prime-gap-structure-artifacts` and local `pgs-local-bulk` for Lake.
