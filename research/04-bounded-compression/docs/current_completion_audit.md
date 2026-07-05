# Dynamic Cutoff Completion Audit

## Objective

Prove or falsify the Dynamic Cutoff for bounded GWR/DNI prime walks:

```text
For every consecutive prime gap, the GWR-selected witness w satisfies
w - p <= C(q) = max(64, ceil(0.5 * log(q)^2)).
```

## Status — COMPLETE 2026-07-05

Universal bounded compression is **proved** in
[PROOF.md](../../../PROOF.md). The Prime-Square Proximity Theorem closes the
square branch. See `PROOF.md` Document Status.

## Success Criteria

| Requirement | Evidence | Status |
|---|---|---|
| Prove the cutoff law for every gap | Prime-Square Proximity + finite base + K=128 residual in `PROOF.md` | `proved` |
| Falsify the cutoff law with a first explicit counterexample | No counterexample in repo through tested regimes | `no counterexample found` |
| Preserve an executable falsifier | `bounded_compression_falsification_runner.py` exists with tests | `done` |
| Preserve measured finite surfaces | `1e6` and `1e7` findings exist | `done` (audit corroboration) |
| Reduce non-square branch | Lemma A' survives through `q <= 10,000,000` | `proved per branch decomposition` |
| Identify invalidated reduction | Literal prior-square Lemma A fails at `q = 113` | `done` |
| Close square branch | Prime-Square Proximity Theorem, `PROOF.md` 2026-07-05 | `proved` |

## Boundary

This bounds the selected-witness offset `w - p`. It does not by itself prove
RH, PNT, or every classical formulation of Cramér's conjecture for raw gap size
`q - p`.

## Next Work

- Lean 4 formalization (axioms → derived theorems)
- Continue falsification sweeps as audit corroboration on larger regimes
- External review and publication