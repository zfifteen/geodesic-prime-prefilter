# Unique Floor Dichotomy: falsification package

## Executive summary

**U1–U3 were not falsified through \(p \le 10^7\).** Unique semiprime-floor gaps stay short (max \(g=34\)); long \(m=4\) gaps are multi-tie at rate \(\ge 0.994\); unique high floors stay near-twin scale (max \(g=12\)). Square unique floors still reach \(g=102\) (U4 contrast). Status: **measured on mid-scale regimes only**. Hypothesis survives this pressure; not a theorem; not verified/validated.

Full narrative: [FINDINGS.md](FINDINGS.md) · claims: [HYPOTHESIS.md](HYPOTHESIS.md) · design: [experiment_design.md](experiment_design.md)

### Axis status

| Axis | Status |
| --- | --- |
| U1 unique \(m=4\) short gap | **holds** on \(p\le 10^7\) |
| U2 long \(m=4\) multi \(\ge 0.99\) | **holds** |
| U3 unique \(m\ge 8\) short | **holds** |
| U4 square long unique contrast | **present** |
| Dichotomy as theorem | **not claimed** |
| GWR / NLS / compression | **theorem** (untouched) |
| Program verified / validated | **not claimed** |

---

## Package

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | U1–U4 |
| `experiment_design.md` | Protocol |
| `probe_unique_floor.py` | Deterministic scan |
| `test_probe_unique_floor.py` | 4 unit tests |
| `artifacts/results_pmax_*.json` | Regimes 2e6 / 5e6 / 1e7 |
| `artifacts/counterexamples_pmax_10000000.csv` | Long unique \(m=4\) samples (no hard CE) |
| `FINDINGS.md` | Report |
| `README.md` | This file |

## Headline numbers (\(p_{\max}=10^7\))

| Quantity | Value |
| --- | ---: |
| Unique \(m=4\) max \(g\) | 34 |
| Unique \(m=3\) max \(g\) | 102 |
| Unique \(m\ge 8\) max \(g\) | 12 |
| Multi rate among \(m=4\), \(g\ge 20\) | 0.9941 |
| U1 / U2 / U3 hard hits | 0 / 0 / 0 |

## Repro

```bash
python3 -m pytest experiments/unique-floor-dichotomy-falsification-2026-07/test_probe_unique_floor.py -q

python3 experiments/unique-floor-dichotomy-falsification-2026-07/probe_unique_floor.py \
  --p-max 2000000 \
  --out experiments/unique-floor-dichotomy-falsification-2026-07/artifacts/results_pmax_2000000.json

python3 experiments/unique-floor-dichotomy-falsification-2026-07/probe_unique_floor.py \
  --p-max 5000000 \
  --out experiments/unique-floor-dichotomy-falsification-2026-07/artifacts/results_pmax_5000000.json

python3 experiments/unique-floor-dichotomy-falsification-2026-07/probe_unique_floor.py \
  --p-max 10000000 \
  --out experiments/unique-floor-dichotomy-falsification-2026-07/artifacts/results_pmax_10000000.json \
  --csv-ce experiments/unique-floor-dichotomy-falsification-2026-07/artifacts/counterexamples_pmax_10000000.csv
```

## Exact limits

- Max regime \(p \le 10^7\). Not \(10^{18}\).
- Survival under falsification pressure is not a proof.
