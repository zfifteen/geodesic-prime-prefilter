# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-23T04:53:08.539918+00:00
**Mode**: `real`
**Artifact type**: `ladder_summary`
**Scale claim**: `False`
**Reference factor space**: 198 words
**Samples per level**: 5

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
| 64 | 5/5 | 35.76% | 29.20% | 0.0% | 59.6% | 0 | 0 | 0 | 0 |
| 72 | 5/5 | 44.24% | 23.10% | 0.0% | 59.6% | 0 | 0 | 0 | 0 |

## Mode Contract

Real mode derives motifs from deterministic public semiprimes.
The corpus is constructed using gmpy2.next_prime **only for fixture generation**.
p and q are discarded before any call to derive_public_motif or prune_factor_space.
Implementation-blocked derivations are reported as derivation_blocked, not unresolved.
Backend errors are reported as backend_error and do not contribute to averages.
No synthetic motif is substituted.

## Top Motifs per Level

**64 bits**
- `o4_d4_a4_d4_odd@early + o4_d4_even prev`: 1
- `o4_d4_a18_d4_odd@early + o6_d4_odd prev`: 1
- `o2_d4_a6_d4_odd@early + o4_higher_divisor_even prev`: 1
- `o2_d4_a12_d4_odd@late + o6_higher_divisor_even prev`: 1
- `o2_d4_a8_d4_odd@mid + o4_d4_odd prev`: 1

**72 bits**
- `o2_d4_a17_d4_even@mid + o6_d4_even prev`: 1
- `o2_d4_a4_d4_odd@mid + o6_d4_odd prev`: 1
- `o6_d4_a24_d4_odd@mid + o4_d4_odd prev`: 1
- `o4_d4_a10_d4_odd@mid + o2_higher_divisor_even prev`: 1
- `o4_d4_a4_d4_odd@mid + o4_d4_even prev`: 1


## Summary (Real Derivation)

- Total cases: 10
- Measured cases: 10
- Resolved cases: 10
- Unresolved cases: 0
- Derivation-blocked cases: 0
- Backend-error cases: 0
- Actual bit-length mismatches: 0
- Average reduction (measured cases): 40.00%
- Average reduction (all cases): 40.00%
- Average reduction (resolved cases): 40.00%
- Min / Max reduction: 0.00% / 59.60%
- Motifs with coverage gaps: 3

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a12_d4_odd@late + o6_higher_divisor_even prev` | 1 | 59.60% | 0 |
| `o2_d4_a17_d4_even@mid + o6_d4_even prev` | 1 | 59.60% | 0 |
| `o2_d4_a4_d4_odd@mid + o6_d4_odd prev` | 1 | 0.00% | 1 |
| `o2_d4_a6_d4_odd@early + o4_higher_divisor_even prev` | 1 | 0.00% | 1 |
| `o2_d4_a8_d4_odd@mid + o4_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a10_d4_odd@mid + o2_higher_divisor_even prev` | 1 | 59.60% | 0 |
| `o4_d4_a18_d4_odd@early + o6_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a4_d4_odd@early + o4_d4_even prev` | 1 | 0.00% | 1 |
| `o4_d4_a4_d4_odd@mid + o4_d4_even prev` | 1 | 42.42% | 0 |
| `o6_d4_a24_d4_odd@mid + o4_d4_odd prev` | 1 | 59.60% | 0 |

## Top Rules

- PG-061: 6
- PG-062: 6
- PG-063: 6
- PG-064: 6
- PG-065: 6

## Per-Case Results (Real Derivation)

### 64 bits

| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |
|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_64_0 | 64 | 64 | 10392492460848205459 | `o4_d4_a4_d4_odd@early + o4_d4_even prev` | derive_public_motif(N_only) | yes | attempted | - | 0 | 198 | 0.00% | resolved | yes | - |
| semiprime_64_1 | 64 | 64 | 10408702856885301037 | `o4_d4_a18_d4_odd@early + o6_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_64_2 | 64 | 64 | 10424924961869999753 | `o2_d4_a6_d4_odd@early + o4_higher_divisor_even prev` | derive_public_motif(N_only) | yes | attempted | - | 0 | 198 | 0.00% | resolved | yes | - |
| semiprime_64_3 | 64 | 64 | 10441158407682135877 | `o2_d4_a12_d4_odd@late + o6_higher_divisor_even prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_64_4 | 64 | 64 | 10457403672765138077 | `o2_d4_a8_d4_odd@mid + o4_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |

### 72 bits

| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |
|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_72_0 | 72 | 72 | 2656590243754032754661 | `o2_d4_a17_d4_even@mid + o6_d4_even prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_1 | 72 | 72 | 2656849349671085360381 | `o2_d4_a4_d4_odd@mid + o6_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | - | 0 | 198 | 0.00% | resolved | yes | - |
| semiprime_72_2 | 72 | 72 | 2657108468385612408137 | `o6_d4_a24_d4_odd@mid + o4_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_3 | 72 | 72 | 2657367598763752167127 | `o4_d4_a10_d4_odd@mid + o2_higher_divisor_even prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_4 | 72 | 72 | 2657626740805691265263 | `o4_d4_a4_d4_odd@mid + o4_d4_even prev` | derive_public_motif(N_only) | yes | attempted | PG-003,PG-005,PG-007,PG-049,PG-050,PG-053,PG-054,PG-055 | 84 | 114 | 42.42% | resolved | no | - |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
