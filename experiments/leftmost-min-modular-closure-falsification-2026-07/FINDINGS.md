# Findings: Leftmost-min modular closure insight falsification

## Executive Summary

**The Core insight from the Grok share is falsified on its stated comparative edge, and its absolute forcing reading remains invalidated.**

On the decisive regime `left prime p in [11, 2.5e7]` (1,565,923 consecutive gaps):

| Selector | Mismatches (`z>=4` and `g>2`) |
| --- | ---: |
| GWR (leftmost min-`tau`) | **2** |
| alt-A rightmost min-`tau` | **0** |
| alt-A unique min only | **0** |
| alt-B first interior `p+1` | **152,620** |

The share's own disconfirmation clause is met:

1. GWR carries `z >= 4` with `g > 2` on the two pinned Super-Signal counterexamples (already in `PROOF.md`).
2. Alternative (a) produces **strictly fewer** mismatches than leftmost-min (`0 < 2`).

So leftmost position is **not** necessary for low mismatch count under the modular zero threshold. On this surface the rightmost min-`tau` probe is strictly cleaner than GWR. First-interior (b) is much worse, so tau-minimization still matters; leftmost bias does not.

**Status labels after experiment:**

| Claim | Status |
| --- | --- |
| H-absolute: GWR `z>=4 => g=2` universal | **invalidated** (reconfirmed; already in `PROOF.md`) |
| H-comparative: leftmost is necessary; alts produce more / at least one mismatch | **falsified** |
| Modular zero lemma `z>=4 <=> 30\|w` | **proved** in `PROOF.md` (untouched) |
| GWR interior maximizer theorem | **proved** in `PROOF.md` (untouched) |

No `verified` / `validated` language is used. Surfaces stop at `2.5e7`.

---

## Hypothesis

Source share: `https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553`

**Core theme (hypothesis, not theorem):**  
"The Leftmost Minimal-Divisor Probe Converts Partial Modular Data into Gap-Closure Rules."

**Falsifiable prediction (from Part 2 of the share):**

- Official leftmost min-divisor witness with `z >= 4` aligns with twin gaps at the known residual rate.
- Redefining the witness as (a) global min-`tau` without leftmost position, or (b) first interior, produces **at least one** mismatch (`z>=4` yet `g>2`) in any multi-thousand-gap range.
- Disconfirmation includes either a GWR mismatch, or an alternative with **strictly fewer** mismatches than leftmost-min.

Full formalization: `HYPOTHESIS.md`.

---

## Experiment design

**Purpose:** Attempt to falsify the share's comparative claim that leftmost min-`tau` is the selector that makes modular zero counts force gap closure.

**PGS frame:**

```text
ordered prime gap (p,q)
  -> divisor-count field tau on interior
  -> selector witness w
  -> z(w) on M_v1 = (2,3,5,7,30,210,2310)
  -> mismatch if z(w)>=4 and g>2
  -> resolved comparative counts / falsified / not_falsified_in_regime
```

**Selectors:**

| Name | Rule |
| --- | --- |
| `gwr` | leftmost interior n with minimal `tau` |
| `alt_a_rightmost_min` | rightmost interior n with minimal `tau` (position bias flipped) |
| `alt_a_unique_only` | the single global min-`tau` n only when ties==1; else unresolved |
| `alt_b_first` | first interior `p+1` (no min-`tau`) |

**Mismatch definition (exact):** `z(w) >= 4` and `g = q - p > 2`.

**Pass criterion for falsification of H-comparative:**

- any alternative has strictly fewer mismatches than GWR, **or**
- on a regime with several thousand gaps, alt-A or alt-B has zero mismatches while the share predicted at least one.

**Classical boundary:** Eratosthenes and linear `tau` accumulation prepare the field only. No classical gate chooses the PGS decision.

---

## Execution

```bash
python3 -m pytest experiments/leftmost-min-modular-closure-falsification-2026-07/test_probe_selectors.py -q

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 100000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_100000.json

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 2000000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_2000000.json

python3 experiments/leftmost-min-modular-closure-falsification-2026-07/probe_selectors.py \
  --p-max 25000000 \
  --out experiments/leftmost-min-modular-closure-falsification-2026-07/artifacts/results_pmax_25000000.json
```

Environment: Python 3.13, local worktree, deterministic (no RNG).

Unit tests: **5 passed**.

---

## Results

### Regime S (smoke): `p in [11, 1e5]`, 9588 gaps

| Selector | z4 | hit_twin | mismatch | twin_rate among z4 |
| --- | ---: | ---: | ---: | ---: |
| gwr | 407 | 407 | 0 | 1.0 |
| alt_a_rightmost_min | 407 | 407 | 0 | 1.0 |
| alt_a_unique_only | 407 | 407 | 0 | 1.0 |
| alt_b_first | 1198 | 407 | 791 | 0.339733 |

H-comparative on this regime: **falsified_zero_mismatch_arm** (alt-A has zero mismatches on >9000 gaps).

### Regime M: `p in [11, 2e6]`, 148929 gaps

| Selector | z4 | hit_twin | mismatch | twin_rate among z4 |
| --- | ---: | ---: | ---: | ---: |
| gwr | 4919 | 4919 | 0 | 1.0 |
| alt_a_rightmost_min | 4919 | 4919 | 0 | 1.0 |
| alt_a_unique_only | 4919 | 4919 | 0 | 1.0 |
| alt_b_first | 18627 | 4919 | 13708 | 0.264079 |

Same comparative kill of the "alt-A must mismatch" arm. Matches historical Super-Signal residual surface (GWR FPs appear only after 2e6).

### Regime D (decisive): `p in [11, 2.5e7]`, 1565923 gaps

| Selector | z4 | hit_twin | mismatch | twin_rate among z4 |
| --- | ---: | ---: | ---: | ---: |
| gwr | 43170 | 43168 | **2** | 0.999954 |
| alt_a_rightmost_min | 43168 | 43168 | **0** | 1.0 |
| alt_a_unique_only | 43168 | 43168 | **0** | 1.0 |
| alt_b_first | 195788 | 43168 | **152620** | 0.220483 |

GWR mismatches are exactly the pinned certificates:

```text
p=17666309  q=17666317  g=8  w_GWR=17666310  tau=16  z=4
p=22284029  q=22284037  g=8  w_GWR=22284030  tau=16  z=4
```

On both gaps, min-`tau` is tied across several interiors. Rightmost min picks a different point with `z=1` (no mismatch). Unique-only declines to fire (ties > 1). First interior coincides with GWR on these rows and also mismatches.

Gaps where rightmost min differs from GWR: **987,444** of 1,565,923.

---

## Interpretation

1. **Absolute forcing** of `z(GWR) >= 4 => g = 2` is false universally. Already recorded in `PROOF.md`. Reconfirmed here with mismatch count 2 at `2.5e7`.

2. **Comparative necessity of leftmost** is false on the share's own criterion. Removing leftmost bias (rightmost min) **eliminates** the two GWR false positives on this surface rather than adding more.

3. **Tau minimization still matters.** First-interior produces a huge mismatch load. The share is right that a non-minimal probe loses sufficiency. It is wrong that **leftmost** among minima is what creates the incompatibility.

4. **Mechanism note (hypothesis-level, not theorem):** Super-Signal false positives sit on min-`tau` **ties** where the leftmost min is highly divisible by the primorial bases and a later min-`tau` point is not. Leftmost bias is what *creates* those particular mismatches, opposite to the share's causal story.

5. **What survives:** GWR as a proved maximizer theorem; modular zero lemma; measured fact that min-`tau` witnesses with high `z` are often twins on finite regimes. None of that restores the insight's "leftmost is necessary for forcing" claim.

---

## Provenance

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | Formal claims and falsifiers |
| `probe_selectors.py` | Deterministic probe |
| `test_probe_selectors.py` | Local unit checks |
| `artifacts/results_pmax_*.json` | Raw measured outputs |
| `FINDINGS.md` | This report |

Reproduce with the commands under Execution.

---

## Limitations

- Upper left prime `2.5e7` only. Not a `10^18` surface. No program-level verified language.
- alt-A unique-only has many unresolved gaps (ties). Its zero mismatch count means "no unique-min z4 non-twin on this surface," not a universal rule (Hypothesis U is separately invalidated at higher scale).
- Rightmost min having zero mismatches here is **measured on regime D**, not a theorem that rightmost is perfect.
- Twin-gap interiors are length 1; all selectors agree there.

---

## Next minimal step (optional)

If the residual question is "which min-`tau` position among ties minimizes modular false positives," run a position-index histogram of min-`tau` set members that carry `z>=4` and `g>2`. That is a new hypothesis, not a rescue of the share insight.
