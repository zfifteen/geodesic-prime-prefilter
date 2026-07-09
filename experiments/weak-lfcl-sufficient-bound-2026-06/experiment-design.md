# Experiment Design: Weak L_FCL at Sufficient Bound + Audit-Demoted τ=2

**Date:** 2026-06-19  
**Hypothesis:** H<sub>CTC</sub>-weak: `research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/`  
**Objective:** On R2 (`11 ≤ p < 10^6`, `B = gap`), verify unique resolved reset, Rule X match, and audit-demoted τ=2 lemma.

## Estimands

| ID | Check |
| --- | --- |
| W1 | `pgs_chamber_reset_state_certificate(p, gap).q == q_ref` |
| W2 | Certificate replay: exactly one resolved survivor |
| W3 | Demoted audit predicate passes without τ(q) table lookup |
| V | Lane V: `τ(q_ref) == 2` |

## Falsification

Any failure in W1/W2/W3 vs V on any gap.

## Commands

```bash
PYTHONPATH=src/python python3 -m pytest experiments/weak-lfcl-sufficient-bound-2026-06/test_weak_lfcl.py -q
PYTHONPATH=src/python python3 experiments/weak-lfcl-sufficient-bound-2026-06/weak_lfcl_probe.py \
  --output-dir experiments/weak-lfcl-sufficient-bound-2026-06/output/R2
```