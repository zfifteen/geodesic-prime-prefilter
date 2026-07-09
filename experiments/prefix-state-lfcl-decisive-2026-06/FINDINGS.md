# Prefix-State L<sub>FCL</sub> Decisive Probe: FINDINGS

**Plain-English version:** (technical only for this run)

**Strongest supported claim (this surface):** Harness **L0** (GWR-offset confound) matched `q_ref` on **0 / 78 493** gaps. Semantic-independence audit **passed**. No substantive law **L1 to L4** achieved early forced closure with a correct endpoint (`any_law_early_support_count = 0`).

**Parent H<sub>CTC</sub> verdict:** **Substantively falsified** on tested closure law **L2** (unique NLSC-admissible composite). **L1, L3, L4** falsified as forward predictors (never fire early). Parent hypothesis remains **unresolved** for a not-yet-specified alternative law.

---

## Executive summary

This experiment tested five pre-registered `Closure(p, State)` laws that use prefix geometry only, no `τ≤2` endpoint selection. The decisive outcome is not ambiguous:

- **L2** fires early on **56 757 / 78 493** gaps and is **wrong every time** it fires (`r ≠ q_ref`). That falsifies H<sub>CTC</sub> for the “unique NLSC-admissible composite” forward path.
- **L1, L3, L4** never declare forced closure before the full gap on R2: each is **falsified as a predictor** on this surface, not a global theorem refutation.
- **L0** fires on every gap (expected) and never matches `q_ref` (expected negative control).

Example counterexample: `p = 47`, `q_ref = 53`. **L2** declares `r = 49` at `B = 2` (composite `49 = 7²`, not the next prime).

---

## Per-law outcomes (R2: `11 ≤ p < 10^6`)

| Law | Early fires | Mismatches | Early match rate | Status |
| --- | ---: | ---: | --- | --- |
| **L0** (harness) | 78 493 | 78 493 | 0% | Harness pass (`l0_match_rate = 0`) |
| **L1** (threat ceiling) | 0 | 0 |: | Falsified as predictor |
| **L2** (unique admissible composite) | 56 757 | 56 757 | 0% | **Substantively falsified** |
| **L3** (threat-gated unique) | 0 | 0 |: | Falsified as predictor |
| **L4** (budget saturation) | 0 | 0 |: | Falsified as predictor |

## D1: uniqueness-before-arrival

| Metric | Value |
| --- | --- |
| Gaps with `max_U_before_gap = 0` | 21 736 |
| Gaps with `max_U_before_gap ≥ 2` | 40 458 |
| `any_law_early_support_count` | **0** |

Chamber geometry under the NLSC-composite admissible definition often leaves **multiple** candidates before the gap ends. No law produced early correct closure.

## State separation

- **Theorem (unchanged):** `q = min{n>p : τ(n)=2}`: `PROOF.md`.
- **Implementation status:** Not under test in this probe.
- **Measured result:** This experiment; artifacts under `output/R2/`.
- **Audit result:** SA static clean; `semantic_tau_le_2_branch_taken_count = 0`.
- **Hypothesis H<sub>CTC</sub>:** **Falsified** for law **L2**; **unresolved** for a replacement forward law not yet specified.
- **Invalidated rule:** **L2** as a forward chamber-closure law.

## Artifacts

```text
experiments/prefix-state-lfcl-decisive-2026-06/
  prefix_state.py
  closure_laws.py
  semantic_audit.py
  prefix_state_closure_probe.py
  summarize_lfcl_probe.py
  test_prefix_closure.py
  output/R2/summary.json
  output/R2/law_reports.json
  output/R2/mismatches.csv
  output/R2/early_fires.csv
  output/R2/gaps.csv
```

## Reproduction

```bash
PYTHONPATH=src/python python3 -m pytest \
  experiments/prefix-state-lfcl-decisive-2026-06/test_prefix_closure.py -q

PYTHONPATH=src/python python3 \
  experiments/prefix-state-lfcl-decisive-2026-06/prefix_state_closure_probe.py \
  --regime R2 \
  --output-dir experiments/prefix-state-lfcl-decisive-2026-06/output/R2

python3 experiments/prefix-state-lfcl-decisive-2026-06/summarize_lfcl_probe.py \
  --summary experiments/prefix-state-lfcl-decisive-2026-06/output/R2/summary.json
```

**Date executed:** 2026-06-19  
**Elapsed:** ≈21 s on R2