# Gap Winner as one-way complexity valve: falsification package

## Executive summary

**H1 (residual mean `tau` strictly elevated after the Gap Winner) is falsified.** On left primes through `2·10^6`, about **60.7%** of eligible both-sided gaps have residual mean `≤` pre-valve mean (`69,455 / 114,417`). H2 (ratio increases with `tau(w)`) is falsified on `p_max ≥ 10^6` (negative Spearman). NLS undercuts: **0**. Theorems in `PROOF.md` are not demoted. Status: **measured on mid-scale regimes only** (not verified / validated; no `10^18` surface).

Full narrative: [FINDINGS.md](FINDINGS.md) · claims: [HYPOTHESIS.md](HYPOTHESIS.md) · design: [experiment_design.md](experiment_design.md)

### Axis status (after pressure)

| Axis | Status |
| --- | --- |
| H1 residual mean elevation (universal on both-sided gaps) | **falsified** (`p ≤ 2e6`) |
| H2 ratio scales up with `tau(w)` | **falsified** (`p_max ≥ 1e6`) |
| H3 NLS surface consistency | **did not falsify** (0 undercuts) |
| GWR maximizer / NLS / compression | **theorem** (untouched) |
| Program verified / validated | **not claimed** |

Source insight share: https://grok.com/share/bGVnYWN5_774d61ad-5f04-40b6-9ea3-0c906426684f

---

## Package contents

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Formal claims and falsifiers |
| `experiment_design.md` | Protocol |
| `probe_valve.py` | Deterministic residual-mean probe |
| `test_probe_valve.py` | Local unit checks (7 tests) |
| `artifacts/results_pmax_*.json` | Measured outputs |
| `artifacts/counterexamples_pmax_2000000.csv` | Sample F1 rows |
| `FINDINGS.md` | Executive findings |
| `README.md` | This file |

## Repro

```bash
python3 -m pytest experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/test_probe_valve.py -q

python3 experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/probe_valve.py \
  --p-max 100000 \
  --out experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/artifacts/results_pmax_100000.json

python3 experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/probe_valve.py \
  --p-max 1000000 \
  --out experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/artifacts/results_pmax_1000000.json

python3 experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/probe_valve.py \
  --p-max 2000000 \
  --out experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/artifacts/results_pmax_2000000.json \
  --csv-ce experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/artifacts/counterexamples_pmax_2000000.csv
```

## Headline numbers (`p_max = 2e6`)

| Quantity | Value |
| --- | ---: |
| Nonempty-interior gaps | 134,060 |
| Eligible (both sides nonempty) | 114,417 |
| `ratio ≤ 1` (F1 hits) | 69,455 |
| Fraction F1 | 0.607 |
| Mean ratio (eligible) | 1.049 |
| Spearman `(tau_w, ratio)` | −0.0188 |
| NLS undercuts | 0 |

## Exact limits

- Highest left-prime regime: `2e6`. Not `10^18`.
- Do not use verified / validated / program-level measured-pass language for this package.
- Residual-mean elevation is **falsified** as a universal gap law on these regimes; average ratio slightly above 1 does not rescue H1.
- Theorems in `PROOF.md` remain theorem under their stated hypotheses.
