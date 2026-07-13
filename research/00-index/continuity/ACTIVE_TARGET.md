# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual audit, Lean formalization, external review

## Central Obligation: OPEN / UNRESOLVED

Prime-square proximity on the square branch remains an **unresolved** theorem
obligation under [PROOF.md](../../../PROOF.md) §Square-Branch Reduction.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [UNRESOLVED obligation]
```

Until that proximity theorem is proved, the all-scale bounded dynamic cutoff
theorem remains unresolved on the square branch. Hourly bands below `10^18` are
**audit corroboration only**, not program-level verification.

Do not restate proximity as proved. Direct next-prime and Interior Maximizer
remain proved under their stated hypotheses.

## Active Frontiers (do not re-litigate closed local theorems)

- Prove the prime-square proximity obligation (`PROOF.md` §Square-Branch Reduction)
- Lean 4: chamber-reset / proximity formalization when the English obligation closes
- Square-branch residual audit sweeps on new regimes (hourly queue)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (do not promote residuals)

- Prime-square proximity / square-branch dynamic-cutoff closure (`PROOF.md` §Square-Branch Reduction)
- Residual chamber claims RC18–RC29 (audit holds on measured panels only)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- Fixed near-540 band as a law for `D(r)` on util maxima (RC2; `D=738` at `r=424171123`)
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
| Newest residual table | RC27–RC29 (`experiments/square-branch-hourly-2026-07-13-rc27/`) |

Prior certified baseline (replay = NO_DELTA): `3·10^8 .. 4·10^8` in `hourly_baseline_signature.json`.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Honest next falsification band: `5·10^8 .. 6·10^8`. Replaying the frozen
`3·10^8 .. 4·10^8` or certified `4·10^8 .. 5·10^8` surface is `NO_DELTA`, not
`ADVANCE`. Re-check RC18–RC29 on any new util maximum.

Execution root: isolated worktree `~/pgs-hourly/prime-gap-structure`  
Human IdeaProjects dirt does not skip the hour.

Every activation posts to Rocket.Chat `#Prime-Gap-Structure` as `grok`
(wrapper EXIT trap only).

## Repro Gate

```text
python3 -m pytest research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py -q
```

RC27–RC29 falsification:

```text
python3 experiments/square-branch-hourly-2026-07-13-rc27/offset_540_residual_rc27_probe.py
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
