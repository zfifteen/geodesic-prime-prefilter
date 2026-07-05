# Bounded Compression

## Object

Dynamic cutoff, bounded compression, square-branch closure, and falsification
audit surfaces for bounded GWR/DNI prime walks.

Primary homes:

- `research/04-bounded-compression/docs/`
- `research/02-gwr-dni/output/gwr_proof/`
- `research/04-bounded-compression/output/square_branch_gap_audit_summary.json`
- `research/04-bounded-compression/scripts/bounded_compression_falsification_runner.py`
- `research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py`
- `research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py`

## Invariant Or Rule

The proved dynamic cutoff is:

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

It is the universal bounded witness-distance theorem for GWR/DNI selected
witnesses. Authority: [PROOF.md](../../PROOF.md) (2026-07-05).

## Proof Status

`PROOF.md` records and proves:

- the finite bounded-compression base;
- the residual `K = 128` first-d4 branch-elimination lemma;
- the **Prime-Square Proximity Theorem** (square branch, proved 2026-07-05);
- **universal bounded compression** across all prime-gap branches at Cramér scale.

**Boundary.** This bounds the selected-witness offset `w - p`. It does not by
itself prove RH, PNT, or every classical formulation of Cramér's conjecture for
raw gap size `q - p`. Lean 4 carries structural axioms pending full
machine-checked derivation.

## Measured Evidence

Measured documentation lives in `research/04-bounded-compression/docs/` and
`research/02-gwr-dni/output/gwr_proof/`.

Falsification sweeps provide **audit corroboration** of the proved bound. No
universal counterexample exists in the repository through tested regimes.

## Audit Status

Focused validation passed after the chapter map was finalized:

```text
python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py research/05-state-budget/tests/test_state_budget_pairwise_ruler_test.py
20 passed in 5.73s
```

## Invalidated Rules

The old fixed cutoff theorem `{2:44, 4:60, 6:60}` is false. It fails at
`q = 24,098,209`, where the square branch gives `E(q) = 72 > 60`.

The literal prior-square Lemma A is invalidated at `q = 113`, where the exact
witness is later square `121 = 11^2`.

## Next Work

- Lean 4: promote `near_root_exclusion_bound` and `prime_square_proximity_theorem`
  from axioms to derived theorems
- Continue square-branch audit sweeps as corroboration on larger regimes
- External review and publication of the Prime-Square Proximity proof

## Reproduce

Run the focused bounded-compression validation:

```text
python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped bounded-compression
chapter in Phase 4 of the repository reorganization. Universal bounded
compression proved 2026-07-05 (Prime-Square Proximity Theorem).