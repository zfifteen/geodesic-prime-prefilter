# Experiment design: one-way complexity valve falsification

## Purpose

Attempt to falsify the share prediction that the Gap Winner (leftmost min-`tau` composite) acts as a one-way complexity valve by elevating residual mean divisor count above the pre-valve mean, with ratio scaling in `tau(w)`.

## Method (minimal)

1. Build exact `tau[n]` on `0..limit` by linear divisor accumulation (field prep).
2. Extract primes as `{n : tau[n] = 2}`.
3. For each consecutive pair `(p, q)` with `p` in `[p_min, p_max]` and `q - p >= 2`:
   - locate `w` = leftmost interior argmin of `tau`;
   - if pre-valve or residual is empty, count as **one-sided / ineligible** for H1/H2;
   - else compute `mean_pre`, `mean_res`, `ratio`;
   - scan residual for strict min undercuts (H3);
   - record `offset = w - p` vs `C(q)` (H4).
4. Aggregate:
   - F1 count of `ratio <= 1`;
   - Spearman `(tau_w, ratio)`;
   - bucket mean ratios by `tau_w`;
   - F3 undercut count;
   - H4 out-of-window fraction.
5. Emit JSON summary + optional CSV of counter-example rows.

## Eligibility for H1/H2

A gap is **eligible** only when both intervals are nonempty:

```text
w >= p + 2   and   w <= q - 2
```

Otherwise pre-valve or residual has no integers and the mean comparison is undefined.

## Pass / fail criteria

| ID | Criterion | Hypothesis impact |
| --- | --- | --- |
| F1 | `n_ratio_le_1 > 0` among eligible gaps | **falsifies H1** on that regime |
| F2 | Spearman `rho(tau_w, ratio) <= 0` with `n_eligible >= 1000` | **falsifies H2** on that regime |
| F2b | Adjacent tau buckets each with `n >= 50` and mean ratio strictly decreasing | **weakens H2** (report; not sole hard fail if Spearman still > 0) |
| F3 | `n_nls_undercuts > 0` | **implementation / surface failure** (unexpected vs NLS) |
| F4 | `offset > C(q)` fraction | scope note for decision rule only |

## Reproducibility pins

| Pin | Value |
| --- | --- |
| Language | Python 3.11+ (stdlib only for probe) |
| Arithmetic | exact integer `tau`; means as float from integer sums |
| `p_min` default | 11 |
| `p_max` regimes | 100_000; 1_000_000; 2_000_000 (extend if needed) |
| Seed | none (deterministic scan) |
| Classical gates | none in inference path |

## Commands

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

## Status language

All outcomes are **measured on regime R** only. Do not use verified / validated / program-level measured-pass language. Theorems in `PROOF.md` are untouched.
