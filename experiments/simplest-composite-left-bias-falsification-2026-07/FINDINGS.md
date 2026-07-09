# Simplest-Composite Left-Bias: Falsification Report

**Date:** 2026-07-07  
**Regime:** Full gap scan through `p < 2·10^6` (148,931 interiors)

## Executive Summary

**The hypothesis is not falsified.** Across 148,931 prime-gap interiors, high-complexity simplest composites (`τ(w) ≥ 12`) form a tight left-edge cloud (median offset 1, p90 offset 1, max offset 5), while the dominant low-complexity branch (`τ(w) = 4`) spreads much farther (median offset 3, p90 offset 6, max offset 24). Prefix cleanliness holds on every row: no easier composite precedes the leftmost minimum. All five pre-registered falsification checks pass.

---

## Hypothesis (verbatim source: user insight, 2026-07-07)

> High complexity minima in the stretch between consecutive primes are forced to sit much closer to the earlier prime than simpler minima.
>
> In real lists of prime pairs the distances from each earlier prime to its stretch's simplest composite should form two visibly different clouds: one cloud for low-complexity simplest composites that spreads out farther as numbers grow, and a second much tighter cloud near the left edge for high-complexity simplest composites.

**Formal test object:** For consecutive primes `p < q`, let `w` be the leftmost interior argmin of `τ(n)` (GWR witness = simplest composite). Measure `offset = w − p` and `τ(w)`.

---

## PGS Frame

| Object | Role |
| --- | --- |
| Gap interior `I = {p+1,…,q−1}` | Composite stretch |
| Divisor-count field `τ(n)` | Complexity measure |
| GWR witness `w` | Leftmost interior argmin `τ(n)` |
| Prefix offset `w − p` | Distance from earlier prime |
| Dynamic cutoff `C(q) = max(64, ⌈0.5·log(q)²⌉)` | Growing envelope (same for all complexities) |

---

## Falsification Matrix

| ID | Criterion | Result | Status |
| --- | --- | --- | --- |
| **F1** | `median(offset \| τ≥12) < median(offset \| τ=4)` | 1.0 vs 3.0 | **Not falsified** |
| **F2** | p90(offset) non-increasing across τ buckets 4→6-7→8-11→12-23→≥24 | 6→5→3→2→1 | **Not falsified** |
| **F3** | No `n ∈ (p,w)` with `τ(n) < τ(w)` | 0 violations / 148,931 | **Not falsified** |
| **F4** | No `τ≥12` gap with `offset ≥ 6` (τ=4 p90) | 0 counterexamples | **Not falsified** |
| **F5** | In each `log₁₀(p)` bin, `τ≥16` median offset `< τ=4` p90 | All bins pass | **Not falsified** |

**Overall verdict:** hypothesis **not falsified**; all supporting checks pass.

---

## Measured Evidence

### Offset clouds by complexity bucket

| Bucket | Count | Median | p90 | Max | Mean |
| ---: | ---: | ---: | ---: | ---: | ---: |
| `τ = 4` | 110,947 | 3 | 6 | 24 | 3.75 |
| `τ = 6 to 7` | 5,432 | 3 | 5 | 20 | 3.11 |
| `τ = 8 to 11` | 15,607 | 2 | 3 | 8 | 2.03 |
| `τ = 12 to 23` | 6,320 | 1 | 2 | 5 | 1.36 |
| `τ ≥ 24` | 10,402 | 1 | 1 | 3 | 1.00 |

The two predicted clouds are structurally visible: low-τ spreads to offset 24; high-τ (`≥12`) almost never exceeds offset 5 and is overwhelmingly at offset 1.

### Scale behavior (`log₁₀(p)` bins)

| Bin | `τ=4` p90 | `τ=4` max | `τ≥16` median | `τ≥16` max |
| --- | ---: | ---: | ---: | ---: |
| `10² to 10³` | 4 | 6 | 1 | 1 |
| `10³ to 10⁴` | 5 | 10 | 1 | 1 |
| `10⁴ to 10⁵` | 6 | 16 | 1 | 3 |
| `10⁵ to 10⁶` | 6 | 22 | 1 | 5 |
| `10⁶ to 10⁷` | 6 | 24 | 1 | 3 |

Low-complexity max offset grows with scale (3 → 24). High-complexity median stays pinned at 1 across every bin with sufficient data.

### Mechanistic check (prefix cleanliness)

Every gap satisfies: if `w` is the leftmost `τ`-minimizer, no integer in `(p, w)` has strictly smaller `τ`. This is a tautology of the leftmost-argmin definition, but it is exactly the structural reason high-τ minima cannot sit deep in a stretch without an easier composite appearing first.

---

## Interpretation

### Supported claims

1. **Left-side bias grows with complexity.** Offset distributions tighten monotonically as `τ(w)` rises; the high-τ cloud is visibly distinct from the `τ=4` cloud.
2. **Envelope decoupling.** The same growing cutoff `C(q)` bounds all branches, yet high-τ witnesses almost never use even the modest offsets that `τ=4` routinely reaches.
3. **Prefix-forcing mechanism.** Zero prefix violations confirm that deep placement of a high-τ minimum is impossible without an easier composite in the prefix: matching the insight's "declare early or be displaced" logic.

### Sharpening note (square branch)

`τ=3` prime-square gaps (223 rows) are excluded from the high/low comparison. They are *low* divisor-count but can offset far (mean 9.85, max 60). That is a separate square-capture phenomenon (see `experiments/prime-square-capture-falsification-2026-07/`). The user's insight targets **high-complexity** minima specifically; square-branch behavior does not contradict it.

### Open regime

Tested only through `2·10^6`. The insight itself notes possible weakening at extreme scales if long stretches without easy-to-factor numbers become common. That regime is **unresolved** here.

---

## Reproducibility

```bash
cd /Users/velocityworks/IdeaProjects/prime-gap-structure
python3 experiments/simplest-composite-left-bias-falsification-2026-07/simplest_composite_left_bias_probe.py
```

**Pins:** Python 3.13, deterministic divisor sieve, `prime_limit = 2_000_000`, 201-sample cross-check against `gwr_next_gap_profile` (0 mismatches).

**Artifacts:**
- `simplest_composite_left_bias_probe.py`: probe script
- `gap_simplest_composite_rows.csv`, per-gap rows
- `falsification_summary.json`, machine-readable verdict
- `offset_clouds.svg`, scatter visualization (`log₁₀(p)` vs offset, colored by τ bucket)

---

## Next Minimal Step

Extend the same probe to a sparse high-`p` sample (e.g. primes near `10^12` from record-gap tables) to test whether any `τ≥12` simplest composite reaches offset ≥ 6 at scales where `τ=4` gaps are wider, the first regime where the insight's extreme-scale caveat could bite.