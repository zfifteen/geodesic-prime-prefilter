# Experiment design: Unique Floor Dichotomy falsification

## Purpose

Attempt to falsify U1–U3 (and report U4 contrast) from the Unique Floor Dichotomy insight.

## Method

1. Exact \(\tau[n]\) by linear accumulation on \(0..\mathrm{hard\_limit}\).
2. Primes as \(\tau(n)=2\).
3. For each consecutive \((p,q)\) with \(p\in[p_{\min},p_{\max}]\):
   - compute \(m\), \(L\), \(w\), \(g\);
   - classify unique vs multi-tie;
   - score U1–U4 aggregates.
4. Emit JSON + optional CE CSV for unique \(m=4\) long rows and U1/U3 violators.

## Regimes

| Label | \(p_{\max}\) |
| --- | ---: |
| A | \(2\cdot 10^6\) |
| B | \(5\cdot 10^6\) |
| C | \(10^7\) |

## Commands

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

## Reproducibility

Python 3 stdlib only; deterministic; field prep by divisor accumulation only.
