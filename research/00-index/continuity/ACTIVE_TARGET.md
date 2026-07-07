# Active Research Target

**Updated:** 2026-07-05  
**Program:** post-breakthrough — Lean formalization, external review, audit corroboration

## Central Obligation — CLOSED 2026-07-05

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
| Segment | `3·10^8 .. 4·10^8` |
| Prime roots tested | `5,084,001` |
| First counterexample | `none` |
| Max utilization | `0.7036082474226805` |
| Extremal root `r` | `358,018,553` |
| Offset `D(r)` | `546` |
| Local artifacts | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_3e8_4e8/` |

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items now target
audit corroboration and Lean formalization — not proof of the square branch.

## Repro Gate

```text
python3 -m pytest research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py -q
```

## Ledger

Append every run to `research/04-bounded-compression/docs/square_branch_hourly.md`.

## Read-First Contract (every activation)

1. `docs/AGENTS.md`
2. `PROOF.md` (theorem status only)
3. This file
4. Last ledger block in `square_branch_hourly.md`

## Relay Branch

Hourly artifacts commit to `codex/hourly-square-branch`.