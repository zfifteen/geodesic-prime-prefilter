# Zero-Excess DNI Phase 3 Risk Verdict

This document gates the Phase 3 additive code helper work.

Phase 3 adds the exact zero-excess coordinate to the invariant helper package
and pins the zeta-compression bridge load with tests. It does not rename the
legacy Z-Band API, change generator output, rewrite committed vectors, or alter
historical artifacts.

```text
phase: Phase 3
scope: additive code helper and tests
verdict: pass
date: 2026-05-22
```

## Phase 3 Scope

Included:

- add `exact_zero_excess(n)` to
  `src/python/z_band_prime_invariant/core.py`;
- export `exact_zero_excess` from
  `src/python/z_band_prime_invariant/__init__.py`;
- add focused tests for the zero-excess coordinate;
- add an RH bridge test that preserves
  `FIXED_POINT_V * normalization_load[n] == log(n) + exact_zero_excess(n)`;
- preserve `exact_z_normalize`, `FIXED_POINT_V`, `proxy_z`, legacy vectors,
  and public Z-Band names.

Excluded:

- no schema migration;
- no committed vector rewrite;
- no generator-output change;
- no generated artifact rewrite;
- no migration of live GWR or gap-ridge scripts;
- no unrelated Grok experiment files.

## Risk Ledger

| Risk | Failure mode | Phase 3 control | Verdict |
|---|---|---|---|
| Bridge-load drift | A doc or test treats `E(n)` alone as the DNI-to-zeta numerator. | Bridge test pins `log(n)+E(n)` as the scaled normalization load. | cleared |
| Prime-zero overclaim | Code or tests state `E(n)=0` iff prime without the `n > 1` guard. | Tests make `E(1)=0` explicit and separately assert prime/composite behavior for `n > 1`. | cleared |
| Sign reversal | The local score relation loses the `F(n)=-E(n)` duality. | Tests pin the local F score as the negative of zero excess. | cleared |
| Legacy API churn | Existing Z-Band names, vectors, or prefilter behavior change. | Prefilter tests pass and no vector or prefilter diff exists. | cleared |
| Artifact churn | Historical outputs or generated artifacts are rewritten. | Phase 3 touched only invariant code, tests, and zero-excess docs. | cleared |
| Scope contamination | Unrelated Grok experiment files enter the phase commit. | Staging scope excludes the unrelated modified and untracked files. | cleared |

## Checks

```text
python3 -m pytest tests/python/test_zero_excess_invariant.py
result: 5 passed

python3 -m pytest research/12-rh-bridge/tests/test_bridge.py
result: 6 passed

python3 -m pytest tests/python/prefilter
result: 11 passed

python3 -m pytest research/02-gwr-dni/tests
result: 96 passed

python3 -m pytest research/11-gap-ridge/tests
result: 38 passed

git diff --check
result: pass

relative Markdown link check
result: checked 2 markdown files

scoped excess-only bridge drift scan
result: no matches on Phase 3 commit surface
```

Compatibility scan:

```text
git diff --name-only -- spec/vectors src/python/z_band_prime_prefilter tests/python/prefilter
result: no changed files
```

## Verdict

Phase 3 passes.

The new helper is additive. It defines the exact coordinate

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n
$$

without changing the legacy `Z(n)` helper. The bridge test keeps the
DNI-to-zeta numerator on

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

The phase may proceed to commit.
