# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual package, chamber-reset lemma, audit corroboration

## Central Obligation: OPEN / UNRESOLVED

The square-branch prime-square proximity theorem remains the exact open
obligation in [PROOF.md](../../../PROOF.md) §Square-Branch Reduction.
`PROOF.md` controls theorem status. Direct next-prime and Interior Maximizer
remain proved under their stated hypotheses.

```text
Target S1* (UNRESOLVED):
  r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))
```

Do not promote finite utilization, residual claim holds, or chamber-reset
subsections to a proof of Target S1*.

## Active Frontiers (do not re-litigate closed local theorems)

- Constructive Chamber-Reset Endpoint Resolution Lemma subsections on the
  selected-square branch (document:
  `research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/`)
  through **S9** / residual package **RC3-RC29**
- Square-branch audit sweeps as corroboration on larger regimes (hourly queue)
- Lean 4 formalization of proved local theorems (separate track)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (PROOF.md controls)

- Prime-square proximity / Target S1* (`PROOF.md` §Square-Branch Reduction)
- All-scale bounded dynamic cutoff on the square branch until S1* closes

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)
- Fixed-band near-540 as a law for `D(r)` (RC2 falsified at `D=738`)

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

Residual package through RC29 holds on util maxima through `4e8-5e8` plus
`o_q` panel (audit only). Constructive lemma claims S1-S9 do not close S1*.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Default frontier job: falsification beyond certified bands (e.g. `5·10^8 .. 6·10^8`).
Replaying the frozen `3·10^8 .. 4·10^8` baseline is `NO_DELTA`, not `ADVANCE`.

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
