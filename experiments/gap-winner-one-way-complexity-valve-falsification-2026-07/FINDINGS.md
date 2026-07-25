# Findings: Gap Winner one-way complexity valve falsification

## Executive summary

**The share’s residual-mean elevation claim is falsified on every executed regime.** On left primes `p ≤ 2·10^6`, among 114,417 eligible both-sided gaps, **69,455** (about **60.7%**) have residual mean `tau` **≤** pre-valve mean `tau`. Zero No-Later-Simpler undercuts appear on this surface. The secondary claim that residual/pre-valve ratio increases with `tau(w)` is **also falsified** on `p_max ≥ 10^6` (Spearman `rho ≈ −0.019`). Proved GWR / NLS / compression theorems are untouched; the valve framing’s mean-elevation prediction is demoted.

Status language: **measured on regime only**. Not verified / validated. Highest left-prime regime: `2·10^6` (no `10^18` surface).

---

## Hypothesis (under test)

From https://grok.com/share/bGVnYWN5_774d61ad-5f04-40b6-9ea3-0c906426684f:

> After Gap Winner `w`, mean divisor count on residual `(w, q)` is **strictly greater** than mean on pre-valve `(p, w)`, and the ratio increases with `tau(w)`.

Formal claims: [HYPOTHESIS.md](HYPOTHESIS.md).

## Experiment design

[experiment_design.md](experiment_design.md) · probe: [probe_valve.py](probe_valve.py)

For each consecutive gap with nonempty interior and both pre-valve and residual nonempty:

```text
w = leftmost argmin tau on (p, q)
mean_pre = mean tau on [p+1, w)
mean_res = mean tau on [w+1, q)
ratio = mean_res / mean_pre
```

**F1:** any `ratio ≤ 1` falsifies H1.  
**F2:** Spearman `(tau_w, ratio) ≤ 0` with `n ≥ 1000` eligible falsifies H2.  
**F3:** any later `tau(n) < tau(w)` is an NLS surface failure.

## Execution

```text
python3 -m pytest experiments/gap-winner-one-way-complexity-valve-falsification-2026-07/test_probe_valve.py -q
# 7 passed

python3 .../probe_valve.py --p-max 100000  --out .../artifacts/results_pmax_100000.json
python3 .../probe_valve.py --p-max 1000000 --out .../artifacts/results_pmax_1000000.json
python3 .../probe_valve.py --p-max 2000000 --out .../artifacts/results_pmax_2000000.json \
  --csv-ce .../artifacts/counterexamples_pmax_2000000.csv
```

Environment: local macOS, Python 3, stdlib-only probe, deterministic scan (no seed).

## Results

| Regime `p_max` | Nonempty gaps | Eligible | `ratio ≤ 1` | frac `≤ 1` | mean ratio | Spearman | H1 | H2 | H3 (NLS) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| `1e5` | 8,366 | 6,862 | 4,407 | 0.642 | 0.984 | +0.0097 | **falsified** | did not (rho>0) | did not |
| `1e6` | 70,327 | 59,636 | 36,624 | 0.614 | 1.032 | **−0.0168** | **falsified** | **falsified** | did not |
| `2e6` | 134,060 | 114,417 | 69,455 | 0.607 | 1.049 | **−0.0188** | **falsified** | **falsified** | did not |

Additional notes:

- **One-sided ineligible** (empty pre or residual): 19,643 at `p_max=2e6`. H1/H2 undefined there by design.
- **NLS undercuts:** `0` on all three regimes.
- **Compression window:** all eligible valves lay inside `C(q)` on these regimes (`out_of_window = 0`).
- **Mean ratio can sit slightly above 1** while **most gaps still reverse**: elevation, when present, is large enough to pull the average, but the share claimed a **universal** residual elevation, not an average effect. Universal H1 is falsified.
- High-sample adjacent bucket decreases at `2e6`: mean ratio at `tau_w=6` ≈ 1.258 falls to `tau_w=8` ≈ 0.943 (n=3643 and 8410).

### Sample F1 counter-examples (first rows, all regimes share early CEs)

| p | q | w | tau_w | mean_pre | mean_res | ratio |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 19 | 23 | 21 | 4 | 6.0 | 4.0 | 0.667 |
| 23 | 29 | 25 | 3 | 8.0 | 4.667 | 0.583 |
| 31 | 37 | 33 | 4 | 6.0 | 5.667 | 0.944 |
| 47 | 53 | 49 | 3 | 10.0 | 5.333 | 0.533 |
| 53 | 59 | 55 | 4 | 8.0 | 5.333 | 0.667 |

Artifacts: `artifacts/results_pmax_*.json`, `artifacts/counterexamples_pmax_2000000.csv`.

## Interpretation

| Claim | Outcome |
| --- | --- |
| H1 residual mean strictly higher after valve | **Falsified** (majority of eligible gaps reverse) |
| H2 ratio increases with `tau(w)` | **Falsified** on `p_max ≥ 1e6` (negative Spearman) |
| H3 NLS surface consistency | **Did not falsify** (`0` undercuts) |
| GWR / NLS / compression as theorems | **Untouched** |
| Valve as useful search-truncation metaphor | **Not supported** by residual-mean elevation; truncation still may follow from NLS alone (no later strict min), without mean elevation |

**Program update:** demote residual-mean elevation from candidate quantitative control parameter to **invalidated prediction** on measured mid-scale regimes. Keep the bare ordering facts (leftmost min + no later undercut). Any certificate truncation story should rest on NLS / compression theorems, not on residual mean `tau` being higher.

Shape note: mean residual elevation is **not** a consequence of NLS. NLS only forbids later **strictly smaller** mins; residual integers can (and often do) carry lower **average** complexity than the pre-valve stretch when the valve sits left and pre-valve holds a single high-`tau` composite.

## Exact limits

- Highest regime: left prime `p ≤ 2·10^6`.
- No decade ladder, no `10^18` surface.
- Forbidden words for this package: verified, validated, program-level measured-pass.
- Twin gaps and one-sided valve positions are out of H1/H2 scope by design.

## Provenance

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Formal claims |
| `experiment_design.md` | Protocol |
| `probe_valve.py` | Deterministic probe |
| `test_probe_valve.py` | 7 local unit tests |
| `artifacts/` | JSON + CE CSV |
| `FINDINGS.md` | This report |
| `README.md` | Package entry |

Branch: `experiment/gap-winner-one-way-complexity-valve-falsification-2026-07`

## Next minimal step

Optional sharpening only: re-run with **minimum interval length** filters (e.g. `n_pre ≥ 3` and `n_res ≥ 3`) to test whether short one-integer sides drive reversals. Even if long sides behave better, H1 as stated (all both-sided gaps) remains falsified by the present surface.
