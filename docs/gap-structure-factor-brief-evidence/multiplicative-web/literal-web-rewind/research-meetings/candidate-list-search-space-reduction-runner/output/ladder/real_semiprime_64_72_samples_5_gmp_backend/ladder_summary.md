# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-23T02:56:20.462577+00:00
**Mode**: `real`
**Reference factor space**: 198 words
**Samples per level**: 5

## Results by Bit Length

| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |
|------|---------------|---------|-----|-----|------------|
| 64 | 47.27% | 20.88% | 15.2% | 71.2% | 0 |
| 72 | 47.78% | 21.48% | 15.2% | 73.7% | 0 |

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
- `o2_d4_a2_d4_odd@mid + o6_higher_divisor_even prev`: 1
- `o4_d4_a16_d4_odd@mid + o6_higher_divisor_odd prev`: 1

**72 bits**
- `o4_d4_a19_d4_even@mid + o2_d4_odd prev`: 1
- `o2_d4_a2_d4_odd@mid + o2_d4_odd prev`: 1
- `o2_d4_a2_d4_odd@late + o4_d4_odd prev`: 1
- `o2_d4_a10_d4_odd@mid + o2_d4_odd prev`: 1
- `o6_d4_a6_d4_odd@mid + o2_d4_odd prev`: 1


## Summary (Real Derivation)

- Total cases: 10
- Resolved cases: 10
- Unresolved cases: 0
- Average reduction (all cases): 47.53%
- Average reduction (resolved cases): 47.53%
- Min / Max reduction: 15.15% / 73.74%
- Motifs with coverage gaps: 2

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a10_d4_odd@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | 1 | 15.15% | 1 |
| `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | 1 | 73.74% | 0 |
| `o2_d4_a2_d4_odd@mid + o6_higher_divisor_even prev` | 1 | 71.21% | 0 |
| `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a16_d4_odd@mid + o6_higher_divisor_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | 1 | 15.15% | 1 |
| `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | 2 | 30.81% | 0 |

## Top Rules

- PG-061: 4
- PG-062: 4
- PG-063: 4
- PG-064: 4
- PG-065: 4

## Per-Case Results (Real Derivation)

### 64 bits

| case_id | N | motif | source | factors_discarded | rules | pruned | remaining | % | status | gap | error |
|---------|---|-------|--------|-------------------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_64_0 | 4611826790276202551 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_64_1 | 4612108295318995049 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | derive_public_motif(N_only) | yes | PG-086 | 30 | 168 | 15.15% | resolved | yes | - |
| semiprime_64_2 | 4612389821840163257 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057,PG-085 | 61 | 137 | 30.81% | resolved | no | - |
| semiprime_64_3 | 4612671249567121423 | `o2_d4_a2_d4_odd@mid + o6_higher_divisor_even prev` | derive_public_motif(N_only) | yes | PG-001,PG-002,PG-008,PG-010,PG-018,PG-022,PG-026,PG-030,PG-034,PG-038,PG-039,PG-040,PG-041,PG-042,PG-043,PG-044,PG-045,PG-056,PG-058,PG-059,PG-060,PG-081 | 141 | 57 | 71.21% | resolved | no | - |
| semiprime_64_4 | 4612952844814057687 | `o4_d4_a16_d4_odd@mid + o6_higher_divisor_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |

### 72 bits

| case_id | N | motif | source | factors_discarded | rules | pruned | remaining | % | status | gap | error |
|---------|---|-------|--------|-------------------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_72_0 | 1180600630115703194183 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_1 | 1180618643689577382163 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-001,PG-002,PG-008,PG-010,PG-014,PG-018,PG-022,PG-026,PG-030,PG-034,PG-038,PG-039,PG-040,PG-041,PG-042,PG-043,PG-044,PG-045,PG-056,PG-058,PG-059,PG-060,PG-081 | 146 | 52 | 73.74% | resolved | no | - |
| semiprime_72_2 | 1180636659050177364127 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | derive_public_motif(N_only) | yes | PG-087 | 30 | 168 | 15.15% | resolved | yes | - |
| semiprime_72_3 | 1180654673998473593203 | `o2_d4_a10_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |
| semiprime_72_4 | 1180672688809299411287 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | derive_public_motif(N_only) | yes | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057,PG-085 | 61 | 137 | 30.81% | resolved | no | - |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
