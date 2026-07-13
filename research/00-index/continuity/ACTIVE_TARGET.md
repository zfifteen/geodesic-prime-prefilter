# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual audit + chamber-reset lemma pressure;
prime-square proximity remains open

## Central Obligation: OPEN / UNRESOLVED

The square-branch prime-square proximity theorem is **not proved**.
`PROOF.md` §Square-Branch Reduction records the exact remaining obligation:

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [UNRESOLVED]
```

Until that proximity theorem is proved, all-scale bounded dynamic cutoff on the
square branch remains unresolved. Direct next-prime and Interior Maximizer
remain proved and are not re-litigated here.

## Active Frontiers (do not re-litigate closed theorems)

- Theorem pressure on `D(r)` via Chamber-Reset Endpoint Resolution Lemma
  constructive subsections S1-S10 (Target S1* still open)
- Square-branch audit sweeps / residual structure on new regimes (hourly queue)
- Lean 4 formalization track (separate; does not close proximity by fiat)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (do not downgrade or promote)

- Prime-square proximity / Target S1* (`PROOF.md` §Square-Branch Reduction)
- All-scale bounded dynamic cutoff on the square branch (depends on proximity)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)
- Fixed-band near-540 as a law on utilization maxima (RC2 falsified at `D=738`)

## Residual package (audit only; not theorems)

Through RC35 / Claims S10-A-S10-C:

- RC27-RC29: successive max/mean, gap CV, Dual isolation in mean-gap units
- RC30-RC32: successive median/mean, sub-mean majority, Tau4 body early-mass
- RC33-RC35: successive IQR/median robust scale, trail/mean closing isolation,
  Tau4 body last-quartile mass
- Constructive residual states: `GapRegularity` / `ResetResidual^G`,
  `GapShape` / `ResetResidual^S`

Do not promote residual envelopes to theorem status.

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

Prior certified baseline (replay = NO_DELTA): `3·10^8 .. 4·10^8` in `hourly_baseline_signature.json`.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not a claim that
proximity is proved and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Default frontier job: falsification beyond the latest certified surface
(currently next open regime `5·10^8 .. 6·10^8`). Replaying a frozen certified
baseline is `NO_DELTA`, not `ADVANCE`.

Execution root: isolated worktree `~/pgs-hourly/prime-gap-structure`  
Human IdeaProjects dirt does not skip the hour.

Every activation posts to Rocket.Chat `#Prime-Gap-Structure` as `grok`
(parent wrapper only; analytic jobs do not notify).

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
