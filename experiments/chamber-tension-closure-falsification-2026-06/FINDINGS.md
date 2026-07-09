# Chamber-Tension Closure Experiment: FINDINGS

**Plain-English version:** [FINDINGS_plain_english.html](FINDINGS_plain_english.html)

**Strongest supported claim (this surface):** On consecutive gaps with `11 ≤ p < 10^6`, production Rule X and its F2-RX isomorph both return the proved next prime on **78 493 / 78 493** gaps (R2, `B = gap`). The GWR-offset negative control fails on every gap. Prefix forcing at `B = gap - 1` never resolves. Tier C composite-exclusion on `11..10 000`, `B = 64` reproduces **`unique_resolved_survivor_count = 0 / 1225`**. Parent H<sub>CTC</sub> substantive closure remains **unresolved**.

**Parent H<sub>CTC</sub> verdict:** **Unresolved** on tested surfaces. Not falsified.

---

## Tier outcomes

| Tier | Regime | Result | Status |
| --- | --- | --- | --- |
| **Harness F0** | R2 | `f0_match_rate = 0 / 78 493` | Pass |
| **A. Rule X ≡ min{τ=2}** | R2 | `f1_match_rate = 1.0`, `audit_tau2_f1_fail = 0` | Supported |
| **B. F2-RX notational isomorph** | R2 | `f2rx_match_rate = 1.0`, ≡ F1 | Expected pass (notational only) |
| **C, adjacent exclusion closure** | C1-EXCL | `unique_resolved_survivor_count = 0`, `no_unique_boundary_count = 1225`, `true_boundary_rejected_count = 0` | Unresolved (pre-registered) |
| **Prefix forcing** | R2 sample | `prefix_none_at_gap_minus_1_rate = 1.0` on 78 493 gaps; `decision_offset_eq_gap_rate = 1.0` on 158 sampled gaps | No early closure |

## R1 production-bound surface (`B = 128`)

| Metric | Value |
| --- | --- |
| `gaps_total` | 78 493 |
| `f1_match_rate` | 1.0 |
| `f2rx_match_rate` | 1.0 |
| `f0_match_rate` | 0.0 |
| `bound_miss_count` | 0 |
| `elapsed_seconds` | ≈190 |

No gap with `p < 10^6` exceeded bound `128` on this surface.

## Tier C baseline reproduction

| Metric | Value |
| --- | --- |
| `row_count` | 1225 |
| `unique_resolved_survivor_count` | **0** |
| `no_unique_boundary_count` | 1225 |
| `true_boundary_rejected_count` | 0 |
| `unique_survivor_match_rate` | ≈0.812 (secondary; survivors with unresolved alternatives) |
| Elimination-slice forbidden gate | **0 violations** on `classify_candidate` + `eliminate_candidates` |

## State separation

- **Theorem (unchanged):** `q = min{n>p : τ(n)=2}` and GWR interior maximizer: `PROOF.md`.
- **Implementation status:** Rule X production selector matches reference on R1/R2 tested regimes.
- **Measured result:** This experiment; artifacts under `output/`.
- **Audit result:** `τ(q)=2` post-hoc on all F1/F2-RX outputs.
- **Hypothesis H<sub>CTC</sub> substantive claim:** Unresolved: no forward law independent of Rule X equivalence demonstrated; exclusion path has zero resolved-unique survivors on default rules.
- **Not falsified:** True boundary never rejected in tier C; no forward selector mismatch on R2.

## Artifacts

```text
experiments/chamber-tension-closure-falsification-2026-06/
  forward_chamber_closure_probe.py
  f2rx_selector.py
  audit_utils.py
  summarize_probe.py
  test_forward_closure.py
  output/R2/summary.json
  output/R1/summary.json
  output/C1-EXCL/composite_exclusion_boundary_probe_summary.json
  output/merged_report.json
```

## Reproduction

```bash
PYTHONPATH=src/python python3 -m pytest \
  experiments/chamber-tension-closure-falsification-2026-06/test_forward_closure.py -q

PYTHONPATH=src/python python3 \
  experiments/chamber-tension-closure-falsification-2026-06/forward_chamber_closure_probe.py \
  --regime R2 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/R2

PYTHONPATH=src/python python3 \
  experiments/chamber-tension-closure-falsification-2026-06/forward_chamber_closure_probe.py \
  --regime R1 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/R1

python3 research/01-generator/scripts/prime_inference_generator/composite_exclusion_boundary_probe.py \
  --start-anchor 11 --max-anchor 10000 --candidate-bound 64 \
  --output-dir experiments/chamber-tension-closure-falsification-2026-06/output/C1-EXCL

python3 experiments/chamber-tension-closure-falsification-2026-06/summarize_probe.py \
  --gap-summary experiments/chamber-tension-closure-falsification-2026-06/output/R2/summary.json \
  --excl-summary experiments/chamber-tension-closure-falsification-2026-06/output/C1-EXCL/composite_exclusion_boundary_probe_summary.json
```

**Date executed:** 2026-06-19