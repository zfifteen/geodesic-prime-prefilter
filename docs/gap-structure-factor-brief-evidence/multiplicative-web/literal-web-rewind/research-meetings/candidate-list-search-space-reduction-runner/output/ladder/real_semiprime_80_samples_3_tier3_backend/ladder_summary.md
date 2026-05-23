# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-23T04:53:08.574985+00:00
**Mode**: `real`
**Artifact type**: `ladder_summary`
**Scale claim**: `False`
**Reference factor space**: 198 words
**Samples per level**: 3

## Backend

- name: `gmp_tier3_public_coordinate_backend`
- kind: `pgs_live_tier3`
- classification: `classical_assisted_public_coordinate`
- scale_capable: `True`
- pgs_native: `False`
- classical_assisted: `True`

## Results by Bit Length

| Bits | Measured | Avg Reduction | Std Dev | Min | Max | Unresolved | Derivation Blocked | Backend Error | Bit Mismatch |
|------|----------|---------------|---------|-----|-----|------------|--------------------|---------------|--------------|
| 80 | 3/3 | 57.58% | 2.86% | 53.5% | 59.6% | 0 | 0 | 0 | 0 |

## Mode Contract

Real mode derives motifs from deterministic public semiprimes.
The corpus is constructed using gmpy2.next_prime **only for fixture generation**.
p and q are discarded before any call to derive_public_motif or prune_factor_space.
Implementation-blocked derivations are reported as derivation_blocked, not unresolved.
Backend errors are reported as backend_error and do not contribute to averages.
No synthetic motif is substituted.

## Top Motifs per Level

**80 bits**
- `o4_d4_a10_d4_odd@mid + o6_d4_odd prev`: 1
- `o2_d4_a2_d4_odd@early + o2_d4_odd prev`: 1
- `o4_d4_a16_d4_odd@very_late + o2_d4_odd prev`: 1


## Summary (Real Derivation)

- Total cases: 3
- Measured cases: 3
- Resolved cases: 3
- Unresolved cases: 0
- Derivation-blocked cases: 0
- Backend-error cases: 0
- Actual bit-length mismatches: 0
- Average reduction (measured cases): 57.58%
- Average reduction (all cases): 57.58%
- Average reduction (resolved cases): 57.58%
- Min / Max reduction: 53.54% / 59.60%
- Motifs with coverage gaps: 0

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a2_d4_odd@early + o2_d4_odd prev` | 1 | 53.54% | 0 |
| `o4_d4_a10_d4_odd@mid + o6_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a16_d4_odd@very_late + o2_d4_odd prev` | 1 | 59.60% | 0 |

## Top Rules

- PG-061: 2
- PG-062: 2
- PG-063: 2
- PG-064: 2
- PG-065: 2

## Per-Case Results (Real Derivation)

### 80 bits

| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |
|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_80_0 | 80 | 80 | 680024919005709216054023 | `o4_d4_a10_d4_odd@mid + o6_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_80_1 | 80 | 80 | 680029064456764659917383 | `o2_d4_a2_d4_odd@early + o2_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-004,PG-006,PG-011,PG-020,PG-024,PG-028,PG-032,PG-036,PG-046,PG-047,PG-048,PG-051,PG-052 | 106 | 92 | 53.54% | resolved | no | - |
| semiprime_80_2 | 80 | 80 | 680033209983702930677281 | `o4_d4_a16_d4_odd@very_late + o2_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
