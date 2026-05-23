# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-22T23:44:11.285235+00:00
**Mode**: `real`
**Reference factor space**: 198 words
**Samples per level**: 3

## Results by Bit Length

| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |
|------|---------------|---------|-----|-----|------------|
| 64 | 25.09% | 25.23% | 0.0% | 59.6% | 0 |
| 72 | 44.45% | 31.95% | 0.0% | 73.7% | 0 |
| 80 | 5.22% | 7.38% | 0.0% | 15.7% | 0 |

## Mode Contract

Real mode derives motifs from deterministic public semiprimes.
The corpus is constructed using gmpy2.next_prime **only for fixture generation**.
p and q are discarded before any call to derive_public_motif or prune_factor_space.
Derivation failures are recorded as unresolved rows. No synthetic motif is substituted.

## Top Motifs per Level

**64 bits**
- `o2_d4_a8_d4_odd@mid + o2_d4_odd prev`: 1
- `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev`: 1
- `o6_d4_a6_d4_odd@mid + o2_d4_odd prev`: 1

**72 bits**
- `o4_d4_a19_d4_even@mid + o2_d4_odd prev`: 1
- `o2_d4_a2_d4_odd@mid + o2_d4_odd prev`: 1
- `o2_d4_a2_d4_odd@late + o4_d4_odd prev`: 1

**80 bits**
- `o6_d4_a6_d4_odd@mid + o2_d4_odd prev`: 1
- `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev`: 1
- `o4_d4_a6_d4_odd@mid + o6_d4_odd prev`: 1


## Summary (Real Derivation)

- Total cases: 9
- Resolved cases: 9
- Unresolved cases: 0
- Average reduction (all cases): 24.92%
- Average reduction (resolved cases): 24.92%
- Min / Max reduction: 0.00% / 73.74%
- Motifs with coverage gaps: 5

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | 1 | 0.00% | 1 |
| `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | 1 | 73.74% | 0 |
| `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | 1 | 0.00% | 1 |
| `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | 1 | 0.00% | 1 |
| `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | 1 | 0.00% | 1 |
| `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | 2 | 15.66% | 2 |

## Top Rules

- PG-061: 2
- PG-062: 2
- PG-063: 2
- PG-064: 2
- PG-065: 2

## Per-Case Results (Real Derivation)

### 64 bits

| case_id | N | motif | source | factors_discarded | rules | pruned | remaining | % | status | gap | error |
|---------|---|-------|--------|-------------------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_64_0 | 4611826790276202551 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_64_1 | 4612108295318995049 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | derive_public_motif(N_only) | yes | - | 0 | 198 | 0.00% | resolved | yes | - |
| semiprime_64_2 | 4612389821840163257 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057 | 31 | 167 | 15.66% | resolved | yes | - |

### 72 bits

| case_id | N | motif | source | factors_discarded | rules | pruned | remaining | % | status | gap | error |
|---------|---|-------|--------|-------------------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_72_0 | 1180600630115703194183 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_1 | 1180618643689577382163 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-001,PG-002,PG-008,PG-010,PG-014,PG-018,PG-022,PG-026,PG-030,PG-034,PG-038,PG-039,PG-040,PG-041,PG-042,PG-043,PG-044,PG-045,PG-056,PG-058,PG-059,PG-060,PG-081 | 146 | 52 | 73.74% | resolved | no | - |
| semiprime_72_2 | 1180636659050177364127 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | derive_public_motif(N_only) | yes | - | 0 | 198 | 0.00% | resolved | yes | - |

### 80 bits

| case_id | N | motif | source | factors_discarded | rules | pruned | remaining | % | status | gap | error |
|---------|---|-------|--------|-------------------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_80_0 | 302232031384200830517547 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057 | 31 | 167 | 15.66% | resolved | yes | - |
| semiprime_80_1 | 302233184299108378083419 | `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | derive_public_motif(N_only) | yes | - | 0 | 198 | 0.00% | resolved | yes | - |
| semiprime_80_2 | 302234337229409109409939 | `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | derive_public_motif(N_only) | yes | - | 0 | 198 | 0.00% | resolved | yes | - |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
