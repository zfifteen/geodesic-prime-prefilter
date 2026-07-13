# Active Research Target

**Updated:** 2026-07-13  
**Program:** post-breakthrough: Lean formalization, external review, audit corroboration

> **Separate live research goal (2026-07-13):** 50-bit public residual
> discriminator `D` on modulus-link residual
> `unresolved_by_reciprocal_carrier_misalignment`. Continuity pin:
> [notes/ACTIVE_GOAL_50bit_residual_discriminator.md](notes/ACTIVE_GOAL_50bit_residual_discriminator.md).
> Full report:
> [reports/next-impact-task/index.html](reports/next-impact-task/index.html).
> That goal does **not** replace this file's Lean / square-branch hourly center.

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
- Square-branch audit sweeps as corroboration on larger regimes (4h relay queue)
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

## Square-branch relay (historical name: hourly)

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

| Ops field | Live value |
| --- | --- |
| Cadence | **Every 4 hours** (`StartInterval` = `14400`) |
| Analytic effort | **`/heavy`** (solo; not Quartet) |
| PGS Quartet | **Off** for this path (solo activation; do not spawn four roles) |
| Status class | Operator preference / ops config (not theorem) |
| Contract | `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md` |
| Continuity note | `research/00-index/continuity/notes/hourly-relay-4h-no-quartet-2026-07-13.md` |

Default frontier job: falsification `4·10^8 .. 5·10^8`. Replaying the frozen
`3·10^8 .. 4·10^8` baseline is `NO_DELTA`, not `ADVANCE`.

Execution root: isolated worktree `~/pgs-hourly/prime-gap-structure`  
Human IdeaProjects dirt does not skip the activation.

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
4. `HOURLY_RELAY_CONTRACT.md` (4h schedule; `/heavy`; no Quartet on relay)
5. Last ledger block in `square_branch_hourly.md`

## Relay Branch

Relay artifacts commit to `codex/hourly-square-branch`.
