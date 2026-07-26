# Findings: Unique Floor Dichotomy falsification pressure

## Executive summary

**The Unique Floor Dichotomy was not falsified on any executed regime through left primes \(p \le 10^7\).** U1 (unique \(m=4\) short gap), U2 (long \(m=4\) multi-tie rate \(\ge 0.99\)), and U3 (unique \(m\ge 8\) short gap) all **hold** on \(p_{\max}\in\{2\cdot 10^6, 5\cdot 10^6, 10^7\}\). U4 contrast holds: unique square floors reach \(g=102\). Unique \(m=4\) max gap creeps only to **34** (still under U1 ceilings 40 / \(\max(48,\lfloor 0.5 C\rfloor)\)). Status: **measured on mid-scale regimes only**. Not theorem. Not verified/validated. No \(10^{18}\) surface.

---

## Hypothesis

If the min-\(\tau\) level set is a singleton, long gaps occur only on the prime-square branch (\(m=3\)). Unique semiprime floors and higher unique floors force short gaps; long non-square corridors are multi-tie.

Formal claims: [HYPOTHESIS.md](HYPOTHESIS.md).

## Results

| \(p_{\max}\) | Unique \(m=4\) max \(g\) | Unique \(m=3\) max \(g\) | Unique \(m\ge 8\) max \(g\) | Multi rate \(m=4\), \(g\ge 20\) | U1 | U2 | U3 | U4 |
| ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| \(2\cdot 10^6\) | 30 | 82 | 10 | 0.9981 | **holds** | **holds** | **holds** | contrast_ok |
| \(5\cdot 10^6\) | 34 | 102 | 12 | 0.9960 | **holds** | **holds** | **holds** | contrast_ok |
| \(10^7\) | 34 | 102 | 12 | 0.9941 | **holds** | **holds** | **holds** | contrast_ok |

Hard hits: `u1_hits = 0`, `u3_hits = 0` on all three regimes. Left compression theorem breaks: 0.

### Extremal unique \(m=4\) row (through \(10^7\))

```text
p = 3587359
q = 3587393
g = 34
m = 4
w = 3587383
alpha = 24
L_size = 1
```

### Extremal unique \(m=3\) row (contrast)

```text
p = 4044077
q = 4044179
g = 102
m = 3
```
(from max-row fields in `results_pmax_5000000.json` / `10000000.json`)

## Interpretation

| Claim | Outcome |
| --- | --- |
| U1 unique \(m=4\) short gap | **Did not falsify** (max \(g=34\) under ceilings) |
| U2 long \(m=4\) multi \(\ge 0.99\) | **Did not falsify** (rate \(\ge 0.994\)) |
| U3 unique high floor short | **Did not falsify** (max \(g=12\)) |
| U4 square long unique | **Contrast present** |
| Dichotomy as theorem | **not claimed** |
| Dichotomy as mid-scale measured regularity | **supported on tested regimes** |

Slow creep of unique \(m=4\) max \(g\) (30 \(\to\) 34 from \(2e6\) to \(5e6\), flat through \(1e7\)) is compatible with a soft growth law. A future kill would need unique \(m=4\) gaps that clear the registered ceilings or multi-rate collapse below 0.99 on long \(m=4\) corridors.

**Program update:** Unique Floor Dichotomy remains a live **hypothesis** with failed falsification on mid-scale surfaces. It is eligible for further pressure (higher \(p_{\max}\), decade sampling), not for theorem language.

## Exact limits

- Highest left-prime regime: \(10^7\).
- No decade ladder, no \(10^{18}\) surface.
- Forbidden: verified / validated / program-level measured-pass language.

## Provenance

| Path | Role |
| --- | --- |
| `probe_unique_floor.py` | Deterministic probe |
| `test_probe_unique_floor.py` | 4 unit tests |
| `artifacts/` | JSON + sample CSV |
| `FINDINGS.md` | This report |

Branch: `experiment/unique-floor-dichotomy-falsification-2026-07`

## Repro

```bash
python3 -m pytest experiments/unique-floor-dichotomy-falsification-2026-07/test_probe_unique_floor.py -q
python3 experiments/unique-floor-dichotomy-falsification-2026-07/probe_unique_floor.py \
  --p-max 10000000 \
  --out experiments/unique-floor-dichotomy-falsification-2026-07/artifacts/results_pmax_10000000.json
```
