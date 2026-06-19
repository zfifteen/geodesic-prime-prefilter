# Active Hourly Research Target

**Updated:** 2026-06-19  
**Program:** square-branch proximity closure for bounded dynamic cutoff

## Central Obligation (unresolved)

For every selected-square branch gap whose first interior prime square is `r^2`,

```text
D(r) = r^2 - P(r^2) <= max(64, ceil(0.5 * log(r^2)^2)).
```

Equivalently: the bounded dynamic cutoff theorem closes on the square branch when
this prime-square proximity statement is proved (`PROOF.md`, square-branch
reduction).

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Square-branch band bound `D(r) < (r-s)(r+s)` from GWR characterization

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)

## Last Measured Surface

| Field | Value |
| --- | --- |
| Segment | `2·10^8 .. 3·10^8` |
| Prime roots tested | `5,173,388` |
| First counterexample | `none` |
| Max utilization | `0.7209612817089452` |
| Extremal root `r` | `251,066,071` |
| Offset `D(r)` | `540` |
| Artifacts | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_2e8_3e8/` |

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation.

## Repro Gate

```text
python3 -m pytest research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py -q
```

## Ledger

Append every run to `research/04-bounded-compression/docs/square_branch_hourly.md`.

## Read-First Contract (every activation)

1. `AGENTS.md`
2. `PROOF.md` (theorem status only)
3. This file
4. Last ledger block in `square_branch_hourly.md`
5. `research/04-bounded-compression/docs/square_branch_blocker_acceptance.md`

## Relay Branch

Hourly artifacts commit to `codex/hourly-square-branch`.