# Active Research Target

**Updated:** 2026-07-13  
**Program:** square-branch residual pressure, chamber-reset lemma construction,
audit corroboration, Lean formalization of proved surfaces

## Central Obligation: OPEN / UNRESOLVED

Prime-square proximity on the selected-square branch remains the exact remaining
bounded-compression obligation. Controlling reference: `PROOF.md`
§Square-Branch Reduction.

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))   [UNRESOLVED universal target]
```

Until that proximity theorem is proved, the all-scale bounded dynamic cutoff
theorem remains unresolved on the square branch (`PROOF.md`).

Hourly bands below `10^18` are **audit corroboration** only. They do not close
proximity and do not authorize program-level validated language for an
implementation.

## Active Frontiers (do not re-litigate closed theorems)

- Theorem pressure on `D(r)` via Chamber-Reset Endpoint Resolution Lemma
  constructive residuals (S1–S8) without residue-only covers or SDA ports
- Falsification band `5e8–6e8` (next open regime beyond certified `4e8–5e8`)
- Lean 4: formalize proved surfaces only (direct next-prime, Interior Maximizer,
  finite base, residual K=128); do not treat proximity as closed
- External review of proved PGS surfaces; square-branch audit sweeps as
  corroboration (hourly queue)
- RSA endpoint resolver maturation (separate program track)

## Proved (do not re-litigate)

- Direct deterministic next-prime rule (`PROOF.md`)
- Interior Maximizer Theorem / GWR (`PROOF.md`)
- Finite bounded-compression base (`PROOF.md`)
- Residual K=128 first-d4 branch-elimination (`PROOF.md`)

## Unresolved (theorem pressure)

- Prime-square proximity / Target S1*
  `D(r) <= max(64, ceil(0.5 * log(r^2)^2))` for every selected-square gap
- All-scale bounded dynamic cutoff on the square branch (waits on proximity)

## Invalidated (do not revive)

- Fixed cutoff map `{2:44, 4:60, 6:60}`
- d=4 τ≥5 Short-Divisor-Average transfer to the square branch
  (`experiments/square-branch-sda-invalidation-2026-06/FINDINGS.md`)
- Fixed near-540 band `D(r) ∈ [528, 552]` as a law on utilization maxima
  (falsified at `r = 424,171,123`, `D = 738`)

## Last Measured Surface (audit corroboration only)

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

Constructive residual package (lemma, not theorem): Claims S1–S8 in
`research/04-bounded-compression/docs/chamber_reset_endpoint_resolution_lemma/`.
Measured residual holds RC3–RC26 on util maxima through `4e8–5e8` + o_q panel
are audit only.

## Hourly Queue

Rotating queue lives in `research/00-index/continuity/hourly_queue.json`.
The dispatcher executes **exactly one** item per activation. Items target
audit corroboration on **new** regimes and residual structure, not proof of the
square branch and not replay of certified bands.

Contract: `research/00-index/continuity/HOURLY_RELAY_CONTRACT.md`

Default frontier job: falsification `5·10^8 .. 6·10^8`. Replaying the frozen
`3·10^8 .. 4·10^8` or certified `4·10^8 .. 5·10^8` baselines is `NO_DELTA`,
not `ADVANCE`.

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
