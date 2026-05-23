# Divisor Classifier Calibration

This is a diagnostic calibration report. It is not a reduction evidence surface.

- artifact_type: `diagnostic_divisor_classifier_calibration`
- baseline_source: `original committed/pre-exact-bit fixture artifacts`
- total_cases: `28`
- lowest_full_surface_success_tier: `tier_3`
- classifier_computation_note: Non-exact tiers compute only the class they report. Public-coordinate factorization is used inside the diagnostic to classify d4 and coarse higher buckets; exact tau values are not emitted for non-exact tiers.

## Baseline Inputs

- `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json`: observed `10`, expected `10`
- `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json`: observed `9`, expected `9`
- `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json`: observed `9`, expected `9`

## Tier Definitions

- `tier_0`: parity and gap position only; no divisor-family detection
- `tier_1`: prime_square vs non-prime_square; withholds d4 vs higher_divisor
- `tier_2`: prime_square, d4, higher_divisor; no exact tau(n) when tau(n) > 4
- `tier_3`: prime_square, d4, and coarse higher buckets; no exact tau(n) inside buckets
- `tier_exact`: exact divisor count control

## Reproduction By Tier

| tier | reproduced | mismatched | total | rate |
|------|------------|------------|-------|------|
| `tier_0` | 0 | 28 | 28 | 0.00% |
| `tier_1` | 0 | 28 | 28 | 0.00% |
| `tier_2` | 25 | 3 | 28 | 89.29% |
| `tier_3` | 28 | 0 | 28 | 100.00% |
| `tier_exact` | 28 | 0 | 28 | 100.00% |

## Per-Case Minimum Tier

| source | case_id | bits | baseline motif | minimum successful tier | first non-exact failure |
|--------|---------|------|----------------|-------------------------|-------------------------|
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_64_0` | 64 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_64_1` | 64 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_64_2` | 64 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_64_3` | 64 | `o2_d4_a2_d4_odd@mid + o6_higher_divisor_even prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_64_4` | 64 | `o4_d4_a16_d4_odd@mid + o6_higher_divisor_odd prev` | `tier_3` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_72_0` | 72 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_72_1` | 72 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_72_2` | 72 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_72_3` | 72 | `o2_d4_a10_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json` | `semiprime_72_4` | 72 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_64_0` | 64 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_64_1` | 64 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_64_2` | 64 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_72_0` | 72 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_72_1` | 72 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_72_2` | 72 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_80_0` | 80 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_80_1` | 80 | `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | `tier_3` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json` | `semiprime_80_2` | 80 | `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_64_0` | 64 | `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_64_1` | 64 | `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_64_2` | 64 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_72_0` | 72 | `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_72_1` | 72 | `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_72_2` | 72 | `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_80_0` | 80 | `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_80_1` | 80 | `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | `tier_3` | `tier_0:winner_offset` |
| `output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json` | `semiprime_80_2` | 80 | `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | `tier_2` | `tier_0:winner_offset` |

## Motif Reproduction Summary

| motif | tier_0 | tier_1 | tier_2 | tier_3 | tier_exact |
|-------|--------|--------|--------|--------|------------|
| `o2_d4_a10_d4_odd@mid + o2_d4_odd prev` | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| `o2_d4_a2_d4_odd@late + o4_d4_odd prev` | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| `o2_d4_a2_d4_odd@mid + o2_d4_odd prev` | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| `o2_d4_a2_d4_odd@mid + o6_higher_divisor_even prev` | 0/1 | 0/1 | 1/1 | 1/1 | 1/1 |
| `o2_d4_a6_d4_odd@mid + o4_higher_divisor_odd prev` | 0/2 | 0/2 | 0/2 | 2/2 | 2/2 |
| `o2_d4_a8_d4_odd@mid + o2_d4_odd prev` | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| `o4_d4_a16_d4_odd@mid + o6_higher_divisor_odd prev` | 0/1 | 0/1 | 0/1 | 1/1 | 1/1 |
| `o4_d4_a19_d4_even@mid + o2_d4_odd prev` | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| `o4_d4_a4_d4_odd@early + o4_higher_divisor_even prev` | 0/3 | 0/3 | 3/3 | 3/3 | 3/3 |
| `o4_d4_a6_d4_odd@mid + o6_d4_odd prev` | 0/2 | 0/2 | 2/2 | 2/2 | 2/2 |
| `o6_d4_a6_d4_odd@mid + o2_d4_odd prev` | 0/6 | 0/6 | 6/6 | 6/6 | 6/6 |

This calibration uses public coordinates from already-measured baseline rows. It does not modify production motif derivation or publish a new reduction surface.
