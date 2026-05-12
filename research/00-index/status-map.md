# PGS Research Corpus Status Map

This file tracks the repository reorganization state. It records migration
status only. It does not upgrade measured results to proof results.

## Phase 1 Skeleton

Status: complete.

Created chapter homes:

- `research/01-generator/`
- `research/02-gwr-dni/`
- `research/03-gap-types/`
- `research/04-bounded-compression/`
- `research/05-state-budget/`
- `research/06-cryptology-rsa/`
- `research/07-oeis/`
- `research/08-collatz/`
- `research/09-exponents/`
- `research/10-twin-primes/`

## Phase 2 Contained Families

Status: complete.

Moved and validated:

- `research/08-collatz/`
- `research/09-exponents/`
- `research/10-twin-primes/`

## Phase 3 GWR And Generator Surfaces

Status: complete.

Production implementation code remained in place. The chapter homes now route
generator evidence and GWR/DNI evidence without moving `src/`, `tests/`, or
`benchmarks/`.

## Phase 4 Bounded Compression And State Budget

Status: complete.

The chapter homes now preserve the dynamic-cutoff unresolved state, the fixed
cutoff invalidation, the square-branch blocker, and the measured `d4_count`
state-budget carrier without upgrading measured evidence to proof.

## Phase 5 Cryptology And RSA

Status: complete.

The chapter home now routes RSA v2/v3, semiprime, modulus-link, reciprocal
closure, and structural-certificate surfaces while preserving unresolved
survivor/blocker status.

## Phase 6 OEIS

Status: complete.

The OEIS chapter now has a candidate workflow and packet template. No candidate
sequence has been selected in this branch.

## Migration Status

| Chapter | Status | Validation | Next Action |
| --- | --- | --- | --- |
| `01-generator` | mapped | `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py` passed, 36 tests | Production code remains in place. |
| `02-gwr-dni` | mapped | `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py` passed, 36 tests | GWR/DNI evidence routed. |
| `03-gap-types` | mapped | `python3 -m pytest research/03-gap-types/tests/test_gwr_dni_gap_type_catalog.py research/03-gap-types/tests/test_gwr_dni_gap_type_sequence_probe.py research/03-gap-types/tests/test_gwr_dni_gap_type_engine_synthesis.py` passed, 9 tests | Gap-type model remains measured. |
| `04-bounded-compression` | mapped | Bounded/state focused command passed, 20 tests | Square branch remains unresolved. |
| `05-state-budget` | mapped | Bounded/state focused command passed, 20 tests | `d4_count` remains measured. |
| `06-cryptology-rsa` | mapped | Focused RSA command passed, 102 tests | RSA v2 unresolved states preserved. |
| `07-oeis` | workflow initialized | template audit passed by file presence | First candidate packet remains open. |
| `08-collatz` | migrated | `python3 -m pytest research/08-collatz/tests` passed, 55 tests | Contained-family migration complete. |
| `09-exponents` | migrated | `python3 -m pytest research/09-exponents/tests` passed, 68 tests | Contained-family migration complete. |
| `10-twin-primes` | migrated | `python3 -m pytest research/10-twin-primes/tests` passed, 48 tests | Contained-family migration complete. |

## Validation Log

```text
2026-05-11:
  python3 -m pytest research/09-exponents/tests
  68 passed in 94.24s

2026-05-12:
  python3 -m pytest research/08-collatz/tests
  55 passed in 0.42s

  python3 -m pytest research/10-twin-primes/tests
  48 passed in 1.02s

  python3 -m pytest research/09-exponents/tests/test_pgs_exponent_tail_probe.py
  8 passed in 0.21s

  python3 -m pytest research/09-exponents/tests
  68 passed in 93.65s

  python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py
  36 passed in 1.02s

  python3 -m pytest research/03-gap-types/tests/test_gwr_dni_gap_type_catalog.py research/03-gap-types/tests/test_gwr_dni_gap_type_sequence_probe.py research/03-gap-types/tests/test_gwr_dni_gap_type_engine_synthesis.py
  9 passed in 3.75s

  python3 -m pytest tests/python/predictor/test_bounded_compression_falsification_runner.py tests/python/predictor/test_d4_fallback_falsification_runner.py tests/python/predictor/test_d4_no_square_fallback_falsification_runner.py tests/python/predictor/test_square_branch_dynamic_cutoff_search.py tests/python/predictor/test_state_budget_divisor_carrier_sweep.py tests/python/predictor/test_state_budget_pairwise_ruler_test.py
  20 passed in 5.73s

  python3 -m pytest tests/python/test_rsa_v2_scripts.py tests/python/test_rsa_v2_transported_story_law.py tests/python/test_rsa_v2_certificate_commitment_story.py tests/python/predictor/test_pgs_semiprime_backward_law_search.py tests/python/predictor/test_pgs_semiprime_backward_transition_law_search.py tests/python/predictor/test_toy_modulus_backward_chamber_lock.py
  102 passed in 248.72s
```
