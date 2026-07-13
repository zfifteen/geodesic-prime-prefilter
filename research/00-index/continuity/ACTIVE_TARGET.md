# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual audit + Lean/external review track

## Central Obligation: OPEN (per PROOF.md)

`PROOF.md` §Square-Branch Reduction: the prime-square proximity theorem remains
the exact remaining bounded-compression obligation. It is **not** proved there.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [UNRESOLVED / Target S1*]
```

Direct next-prime and Interior Maximizer remain proved. Hourly work is residual
audit and regime corroboration only — not a proof of proximity.

## Active Frontiers (do not re-litigate closed theorems)

- Prove prime-square proximity (Target S1*) under the square-branch reduction
- Lean 4: chamber-reset / proximity formalization pressure
  (`lean-4/PGS/ChamberReset.lean`)
- Square-branch audit sweeps on **new** regimes (hourly queue; next band `5e8-6e8`)
- Residual chamber package through **RC38** (audit only; not theorem)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (do not promote)

- Prime-square proximity / Target S1* (`PROOF.md` §Square-Branch Reduction)
- Universal all-scale bounded dynamic cutoff on the square branch (depends on S1*)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- Fixed near-540 band law on util maxima (RC2 falsified; D=738 escape)
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)

## Residual package (audit only; through RC38)

Latest falsifiable residual surface on util maxima through `4e8-5e8` + o_q panel:

| IDs | Theme | Status |
| --- | --- | --- |
| RC33-RC35 | IQR/median, trail/mean, body last-quartile | holds (prior) |
| RC36-RC38 | open/mean, max/median, IQR/mean | holds (2026-07-13) |
| RC2 | fixed band [528, 552] as law | falsified (retained) |

Falsification command:

```text
python3 experiments/square-branch-hourly-2026-07-13-rc36/offset_540_residual_rc36_probe.py
```

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
Replaying `4e8-5e8` without a new residual claim is also `NO_DELTA`.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Honest next falsification band: `5·10^8 .. 6·10^8`. Replaying frozen
`3e8-4e8` or certified-signature `4e8-5e8` is `NO_DELTA`, not `ADVANCE`.

Execution root: isolated worktree `~/pgs-hourly/prime-gap-structure`  
Human IdeaProjects dirt does not skip the hour.

Every activation posts to Rocket.Chat `#Prime-Gap-Structure` as `grok`
(wrapper EXIT only — analytic jobs must not double-post).

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
