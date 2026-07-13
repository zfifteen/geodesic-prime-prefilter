# Active Research Target

**Updated:** 2026-07-10  
**Program:** post-breakthrough: Lean formalization, external review, audit corroboration

## Central Obligation: CLOSED 2026-07-05

The square-branch prime-square proximity theorem is **proved** in
[PROOF.md](../../../PROOF.md) §Prime-Square Proximity Theorem. Universal bounded
compression at Cramér scale is established across all prime-gap branches per
`PROOF.md` Document Status.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [PROVED]
w - p <= max(64, ceil(0.5 * log(q)^2))       [PROVED, all branches]
```

## Active Frontiers (do not re-litigate closed theorems)

- Lean 4: promote `near_root_exclusion_bound` and `prime_square_proximity_theorem`
  from axioms to derived theorems (`lean-4/PGS/ChamberReset.lean`)
- External review and publication of the Prime-Square Proximity proof
- Square-branch audit sweeps as corroboration on larger regimes (hourly queue)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)
- **Prime-Square Proximity Theorem** (`PROOF.md`, 2026-07-05)
- **Universal bounded compression** (`PROOF.md`, 2026-07-05)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
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

Prior certified baseline (replay = NO_DELTA): `3·10^8 .. 4·10^8` in `hourly_baseline_signature.json`.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Default frontier job: falsification `4·10^8 .. 5·10^8`. Replaying the frozen
`3·10^8 .. 4·10^8` baseline is `NO_DELTA`, not `ADVANCE`.

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