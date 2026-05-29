# Zero-Excess DNI Phase 4 Compatibility Verdict

This document closes the compatibility review required after adding
`exact_zero_excess(n)`.

Phase 4 does not approve script migration, schema migration, vector
regeneration, or public API renaming. It checks that Phase 3 stayed additive
and that legacy Z-Band behavior remains intact.

```text
phase: Phase 4
scope: compatibility review for additive invariant helper
verdict: pass
date: 2026-05-22
```

## Boundary

The Phase 3 code change added one public helper:

```text
exact_zero_excess(n)
```

The existing public names remain:

```text
FIXED_POINT_V
FIXED_POINT_TOLERANCE
exact_divisor_count
exact_z_normalize
```

No legacy Z-Band field, vector, prefilter API, generator output contract, or
benchmark schema changed.

## Compatibility Checks

```text
python3 -m pytest tests/python/prefilter
result: 11 passed

git diff --name-only -- spec/vectors src/python/z_band_prime_prefilter tests/python/prefilter
result: no changed files

git diff --cached --check
result: pass for the Phase 3 commit surface before commit
```

The broader code-adjacent suites were also run during Phase 3:

```text
python3 -m pytest research/02-gwr-dni/tests
result: 96 passed

python3 -m pytest research/11-gap-ridge/tests
result: 38 passed

# RH bridge tests archived externally — see research/12-rh-bridge/README.md and external archive/test_bridge.py
result: 6 passed
```

## Deferred Work

The following work remains outside this compatibility verdict:

- migrating live GWR/DNI scripts from raw-Z argmax wording to zero-excess
  argmin wording;
- adding aliases for fields such as `peak`, `best_n_z`, or
  `log_score_margin`;
- changing committed vector schemas;
- regenerating plots, PDFs, benchmark reports, or public visual artifacts.

Those changes require a separate script and schema migration gate.

## Verdict

Phase 4 passes.

The Zero-Excess DNI helper is now available as an exact additive coordinate.
The old Z-Band API remains stable, and the zeta bridge continues to use
`H(n)=log n+E(n)` as the load.
