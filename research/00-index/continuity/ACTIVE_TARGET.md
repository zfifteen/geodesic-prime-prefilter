# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual audit; Lean formalization; external review

## Central Obligation: OPEN / UNRESOLVED

Prime-square proximity remains an **unresolved** square-branch reduction in
[PROOF.md](../../../PROOF.md) §Square-Branch Reduction. The Interior Maximizer
Theorem and the direct next-prime rule are proved. They do **not** close the
distance bound from the left endpoint prime `p` to the first interior prime
square `r^2`.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [UNRESOLVED obligation]
w - p <= max(64, ceil(0.5 * log(q)^2))       [UNRESOLVED on square branch]
```

Do not write CLOSED, PROVED, or universal bounded compression for the square
branch until `PROOF.md` itself records that proof.

## Active Frontiers (do not re-litigate closed local theorems)

- Square-branch residual chamber structure (offset-540 audit chain; RC package)
- Falsification sweeps on new regimes beyond certified bands (next: `5e8-6e8`)
- Lean 4: promote chamber-reset material carefully without inventing proximity
- External review of proved local theorems; RSA endpoint track separate

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (do not promote residual audit to theorem)

- Prime-square proximity / square-branch distance bound (`PROOF.md` §Square-Branch Reduction)
- Residual chamber claims RC3-RC32 (audit only on measured surfaces)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- Fixed near-540 band law for `D(r)` on segment util maxima (RC2 falsified)
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)

## Last Measured Surface (audit corroboration)

| Field | Value |
| --- | --- |
| Segment | `4·10^8 .. 5·10^8` |
| Prime roots tested | `5,019,541` |
| First counterexample | `none` |
| Max utilization | `0.9341772151898734` |
| Extremal root `r` | `424,171,123` |
| Offset `D(r)` | `738` |
| Local artifacts | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/` |
| Residual package | through RC32 (`experiments/square-branch-hourly-2026-07-13-rc30/`) |

Prior certified baseline (replay = NO_DELTA): `3·10^8 .. 4·10^8` in `hourly_baseline_signature.json`.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Default frontier job: falsification beyond certified regimes. Replaying the
frozen `3·10^8 .. 4·10^8` baseline is `NO_DELTA`, not `ADVANCE`.

Execution root: isolated worktree `~/pgs-hourly/prime-gap-structure`  
Human IdeaProjects dirt does not skip the hour.

Every activation posts to Rocket.Chat `#Prime-Gap-Structure` as `grok`.

## Repro Gate

```text
python3 -m pytest research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py -q
```

## Ledger

Append every run to `research/04-bounded-compression/docs/square_branch_hourly.md`
with Research status and Ops status.

## Read-First Contract (every activation)

1. `Agents.md` (repo root)
2. `PROOF.md` (theorem status only)
3. This file
4. `HOURLY_RELAY_CONTRACT.md`
5. Last ledger block in `square_branch_hourly.md`

## Relay Branch

Hourly artifacts commit to `codex/hourly-square-branch`.
