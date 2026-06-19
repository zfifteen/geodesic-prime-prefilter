# Weak L_FCL Sufficient-Bound Probe — FINDINGS

**Strongest supported claim (this surface):** On consecutive gaps with `11 ≤ p < 10^6` at sufficient bound `B = gap`, Rule X emits a **unique resolved reset** at `q_ref` on **78 493 / 78 493** gaps. Audit-demoted zero-excess signature (structural resolved + lemma bridge, no `τ(q)` lookup) matches lane V on **78 493 / 78 493** gaps.

**H<sub>CTC</sub>-weak verdict:** **Supported on R2 measured surface.** Equivalence **theorem** (L5 in proof target) remains **unresolved**.

---

## Results

| Estimand | Value |
| --- | --- |
| `cert_match_rate` | **1.0** (78 493 / 78 493) |
| `unique_resolved_rate` | **1.0** |
| `replay_match_rate` | **1.0** |
| `demoted_audit_pass_rate` | **1.0** |
| `lane_v_tau2_pass_rate` | **1.0** |
| `semantic_composite_only_rate` | **1.0** |
| `failure_count` | **0** |
| `weak_lfcl_supported_on_surface` | **true** |

## State separation

- **Theorem (unchanged):** `q = min{n>p : τ(n)=2}` — `PROOF.md`.
- **Measured result:** Unique resolved survivor at `B = gap` on full R2 surface.
- **Audit-demoted lemma (measured):** Structural selection record + `n > 1` bridge aligns with `τ(q)=2` on all tested gaps.
- **Hypothesis H<sub>CTC</sub>-weak:** Supported on this surface; not yet promoted to theorem (proof of forced equivalence open).
- **H<sub>CTC</sub>-strong:** Still invalidated (prior prefix-state probe).

## What this does not prove

- Early closure at `B < gap`
- Mechanism independence from divisor-count field during traversal
- Universal theorem without proof attempt on L5

## Next step

Proof work on L5 in `lean-4/PGS/NextPrime.lean` per `weak_lfcl_proof_target.html`. Phase 2 exclusion at `B = gap` only if equivalence proof stalls.

## Reproduction

```bash
PYTHONPATH=src/python python3 -m pytest \
  experiments/weak-lfcl-sufficient-bound-2026-06/test_weak_lfcl.py -q

PYTHONPATH=src/python python3 \
  experiments/weak-lfcl-sufficient-bound-2026-06/weak_lfcl_probe.py \
  --output-dir experiments/weak-lfcl-sufficient-bound-2026-06/output/R2
```

**Date executed:** 2026-06-19 · **Elapsed:** ≈33 s