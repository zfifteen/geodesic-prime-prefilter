# Bounded Compression

## Object

Dynamic cutoff, bounded compression, square-branch pressure, and falsification
surfaces for bounded GWR/DNI prime walks.

Primary homes:

- `research/04-bounded-compression/docs/`
- `output/gwr_proof/`
- `research/04-bounded-compression/output/square_branch_gap_audit_summary.json`
- `research/04-bounded-compression/scripts/bounded_compression_falsification_runner.py`
- `research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py`
- `research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py`

## Invariant Or Rule

The active empirical cutoff rule is:

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

It is a bounded witness-distance target for GWR/DNI selected witnesses.

## Proof Status

`PROOF.md` records:

- the finite bounded-compression base;
- the residual `K = 128` first-d4 branch-elimination lemma;
- the square-branch reduction;
- the unresolved all-scale square-branch proximity obligation.

The all-scale dynamic cutoff theorem remains unresolved.

## Measured Evidence

Measured documentation lives in `research/04-bounded-compression/docs/` and
`output/gwr_proof/`.

The current completion audit states that no proof artifact closes the universal
cutoff law and no universal counterexample exists in the repository.

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py tests/python/predictor/test_state_budget_divisor_carrier_sweep.py tests/python/predictor/test_state_budget_pairwise_ruler_test.py
20 passed in 5.73s
```

## Invalidated Rules

The old fixed cutoff theorem `{2:44, 4:60, 6:60}` is false. It fails at
`q = 24,098,209`, where the square branch gives `E(q) = 72 > 60`.

The literal prior-square Lemma A is invalidated at `q = 113`, where the exact
witness is later square `121 = 11^2`.

## Unresolved State

The square branch remains unresolved. A completion claim requires either a
proof that the square-offset envelope holds for every right prime, or a first
explicit counterexample.

## Reproduce

Run the focused bounded-compression validation:

```text
python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped bounded-compression
chapter in Phase 4 of the repository reorganization.
