# PGA Grammar Pruner Real-Probe Replay

- mode: `real_replay`
- source_probe: `output/ladder/real_semiprime_64_80_samples_3/ladder_summary.json`
- reference_space: `198`
- total_cases: `9`
- resolved_cases: `9`
- unresolved_cases: `0`
- average_reduction_over_all_cases: `35.02%`
- average_reduction_over_resolved_cases_only: `35.02%`
- min_reduction: `15.15%`
- max_reduction: `73.74%`

## Results By Bit Length

| bits | avg | min | max | unresolved |
|------|-----|-----|-----|------------|
| 64 | 35.19% | 15.15% | 59.60% | 0 |
| 72 | 49.50% | 15.15% | 73.74% | 0 |
| 80 | 20.37% | 15.15% | 30.81% | 0 |

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | 1 | 15.15% | 1 |
| `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | 1 | 73.74% | 0 |
| `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | 1 | 15.15% | 1 |
| `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | 1 | 59.60% | 0 |
| `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | 1 | 15.15% | 1 |
| `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | 1 | 15.15% | 1 |
| `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | 2 | 30.81% | 0 |

## Per-Case Replay

### 64 bits

| case_id | motif | rules | pruned | remaining | reduction | gap |
|---------|-------|-------|--------|-----------|-----------|-----|
| semiprime_64_0 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | no |
| semiprime_64_1 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | PG-086 | 30 | 168 | 15.15% | yes |
| semiprime_64_2 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057,PG-085 | 61 | 137 | 30.81% | no |

### 72 bits

| case_id | motif | rules | pruned | remaining | reduction | gap |
|---------|-------|-------|--------|-----------|-----------|-----|
| semiprime_72_0 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | no |
| semiprime_72_1 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | PG-001,PG-002,PG-008,PG-010,PG-014,PG-018,PG-022,PG-026,PG-030,PG-034,PG-038,PG-039,PG-040,PG-041,PG-042,PG-043,PG-044,PG-045,PG-056,PG-058,PG-059,PG-060,PG-081 | 146 | 52 | 73.74% | no |
| semiprime_72_2 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | PG-087 | 30 | 168 | 15.15% | yes |

### 80 bits

| case_id | motif | rules | pruned | remaining | reduction | gap |
|---------|-------|-------|--------|-----------|-----------|-----|
| semiprime_80_0 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | PG-009,PG-012,PG-021,PG-025,PG-029,PG-033,PG-037,PG-057,PG-085 | 61 | 137 | 30.81% | no |
| semiprime_80_1 | `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | PG-088 | 30 | 168 | 15.15% | yes |
| semiprime_80_2 | `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | PG-089 | 30 | 168 | 15.15% | yes |

Replay uses already-derived public motifs only. It does not rerun motif derivation.
