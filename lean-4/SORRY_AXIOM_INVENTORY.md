# Lean 4 sorry / axiom inventory

**As of:** 2026-07-23 (M5 program DoD exit on branch `lean/m5-dod-exit`)  
**Command:** `rg -n 'sorry|^\s*axiom ' lean-4/PGS/*.lean`  
**DoD:** `DEFINITION_OF_DONE.md` · Peer accept: `peer/M5_DOD_ACCEPT.md`

## Summary

| Kind | Count | Status |
| --- | --- | --- |
| `sorry` on core path | **0** | D2.1 **pass** |
| `axiom` on core path | **1** | `tau_prime_square_eq_three` — **audit premise** (D3.2a) |
| Empty-shell PSP | **0** | D4.4b **pass** |
| Finite-base packages | **3** named + `FiniteBaseBundle` | D4.6 **pass** |

## Axiom allowlist (D2.3 / D3)

| Location | Name | Label | PROOF.md |
| --- | --- | --- | --- |
| `PGS/Placement.lean` | `tau_prime_square_eq_three` | **audit premise** (CL-003 classical import) | Prime-square divisor count; not a UBC/PSP smuggle |

No other `axiom` on `lean-4/PGS/*.lean`.

## Finite-base hypothesis packages (D4.6)

Canonical module: `PGS/FiniteBases.lean`.

| Certificate id | Lean name | Range / meaning | Certificate path | Artifact hash |
| --- | --- | --- | --- | --- |
| `gwr_finite_base_v1` | `GwrFiniteBaseV1` | `p < 5_000_000_001` ⇒ `EarlierSideClosed` | `docs/proof-enhancements/certificates/gwr_finite_base_v1.json` | `sha256:222398f59d1ab1e6f6a7b17c691ebc44a96038a713f5218ea407f1bb5a5cff57` |
| `bounded_compression_base_v1` | `BoundedCompressionBaseV1` | `q < 8_886_111` ⇒ `w−p ≤ 60` | `docs/proof-enhancements/certificates/bounded_compression_base_v1.json` | `sha256:fb20894f92320a7547014b37d4dfd7727b7f75f7e92054ddd883d51345d14514` |
| `residual_k128_v1` | `ResidualK128Premise` / `ResidualK128Holds` | K=128 residual elimination token | `docs/proof-enhancements/certificates/residual_k128_v1.json` | `sha256:ed3afeadc81475850a64331d1f008c8ac8af8afe084659f4b37f5a56f77e1e29` |

Unified: `FiniteBaseBundle p q w`. Lean does **not** re-prove exhaustions.

## Module status

| Module | Milestone | Notes |
| --- | --- | --- |
| `Basic.lean` | M1 | tau characterization proved |
| `ChamberReset.lean` | M2 | replay discharged; near-root proved; empty PSP removed |
| `NextPrime.lean` | M2 | weak L_FCL export |
| `GWR.lean` | M3 | Ordered Comparison + maximizer packaging |
| `BoundedCompression.lean` | M4 | non-vacuous UBC + PSP assembly |
| `FiniteBases.lean` | M5 | certificate-aligned hypothesis bundles |
| `Placement.lean` | support | Bertrand theorem; one audit axiom |

## Named analytic packages (not axioms)

| Name | Role |
| --- | --- |
| `EarlierSideClosed` | GWR earlier-integer side (M3) |
| `SquareBranchCapacityContra` | PSP Corollary 4c.3 packaging (M4) |
| `AnalyticUBCClosure` | UBC complementary regime (M4) |

## Scratch / non-core

`lean-4/scratch/` may contain exploratory `sorry`; non-blocking (D2.2).

## Update rule

After each milestone: re-run ripgrep, refresh this table, bump “As of”, note SHA.

*M5 CLOSED (2026-07-23). Program DoD D1–D7 recorded in `peer/M5_DOD_ACCEPT.md`.*
