# Findings: Hypothesis U (Unique Super-Signal)

## Executive Summary

**Hypothesis U is falsified.**

A single counterexample was found and dual-audited:

```text
p = 156,942,923
q = 156,942,931
g = 8
GWR w = 156,942,930
τ(w) = 16
ties = 1   (unique interior minimum)
z(w) = 4   (30 | w; not 210 | w)
```

Antecedent of U holds (`z ≥ 4` and unique `τ`-min). Consequent fails (`g ≠ 2`).  
Therefore unique minimum + four remainder zeros does **not** force a twin gap.

Secondary survivors in the same run (still **hypothesis / measured**, not theorems):

- **H-210** (`210 | w` as GWR ⇒ `g = 2`): **0** false positives in tested regimes.
- **H-τ16** (`z ≥ 4` and `τ(w) > 16` ⇒ `g = 2`): **0** false positives in tested regimes.

---

## Hypothesis (formal)

See `HYPOTHESIS.md`.

**Hypothesis U.** If the GWR witness `w` satisfies `z(w) ≥ 4` on `M_v1` and the interior `τ`-minimum is unique (`ties = 1`), then `g = 2` and `q = w + 1`.

**Status before experiment:** hypothesis  
**Status after experiment:** **invalidated**

---

## Experiment design

See `experiment_design.md`.

| Phase | Method | Regime |
| --- | --- | --- |
| A | Full-gap sieve of primes + `τ` | left prime `p ∈ [11, 5×10^7)` |
| B | Full-gap sympy interiors | `p ∈ [5×10^7, 1.2×10^8)` |
| C | Targeted: every `30k` as candidate unique-min GWR in non-twin gaps | `w ∈ [1.2×10^8, 2×10^8)` |

**Decision rule:** ≥1 U-CE ⇒ `falsified` (definitive). 0 CEs ⇒ `not_falsified_in_tested_regime` only (not a proof).

---

## Execution

```bash
python3 experiments/hypothesis-u-unique-supersignal-falsification-2026-07/run_hypothesis_u.py \
  --p-max-a 50000000 --p-max-b 120000000 --p-max-c 200000000
python3 -m pytest experiments/hypothesis-u-unique-supersignal-falsification-2026-07/test_hypothesis_u_core.py -q
```

- Runtime: ~63 minutes wall clock  
- Artifact: `results.json`  
- Core unit tests: **3 passed**

---

## Results

| Metric | Value |
| --- | ---: |
| Gaps scanned (A+B) | 6,841,644 |
| Phase C multiples of 30 checked | 2,666,667 |
| Phase C non-twin containers | 2,568,064 |
| Bare Super-Signal FPs (`z≥4`, `g>2`) | 23 (A+B; expected) |
| **Hypothesis U CEs** | **1** |
| H-210 FPs | 0 |
| H-τ>16 FPs | 0 |
| Unique-min + `z≥4` twin hits (A+B) | 172,130 / 172,130 |

### Counterexample (verified)

Interior of `(156942923, 156942931)`:

| n | τ(n) | note |
| ---: | ---: | --- |
| 156942924 | 24 | |
| 156942925 | 24 | |
| 156942926 | 32 | |
| 156942927 | 20 | |
| 156942928 | 20 | |
| 156942929 | 24 | |
| **156942930** | **16** | unique min; `2·3·5·5231431` |

```text
R(w) on M_v1 = (0, 0, 0, 4, 0, 60, 1530)
z(w) = 4
ties = 1
g = 8
```

Independent sympy primality + factorization + shipped `classify_gap` all agree: **`hypothesis_u_ce = True`**.

### Shape note vs earlier bare Super-Signal CEs

Earlier bare CEs (`p ≈ 1.77×10^7` … `4.9×10^7`) had **ties ≥ 3** and `w = p+1`.  
This U-CE still has `g = 8`, `τ = 16`, `z = 4`, but:

- **unique** minimum (`ties = 1`)
- witness is **rightmost** interior (`w = q − 1`), not leftmost class-A form

So unique-min was a real side condition, not enough for a universal twin lock.

---

## Interpretation

| Claim | Status after this experiment |
| --- | --- |
| Bare Super-Signal `z≥4 ⇒ g=2` | still **invalidated** |
| **Hypothesis U** (unique min + `z≥4 ⇒ g=2`) | **invalidated** |
| H-210 (`210\|w` as GWR ⇒ `g=2`) | **hypothesis**, measured-clean in this run |
| H-τ16 (`z≥4` and `τ(w)>16 ⇒ g=2`) | **hypothesis**, measured-clean in this run |
| Modular `z≥4 ⇔ 30\|w` | **proved** (untouched) |
| GWR maximizer pillar | **not demoted** |

**Program update:** Super-Signal cannot be repaired by “unique minimum” alone. Any remaining twin-lock candidate must at least dodge this CE: e.g. require `210 | w` (six zeros) and/or `τ(w) > 16`, then re-run a CE hunt with the same discipline.

Finite empty scans of H-210 / H-τ16 are **not** proofs.

---

## Provenance

| Path | Role |
| --- | --- |
| `HYPOTHESIS.md` | formal statement |
| `experiment_design.md` | protocol |
| `run_hypothesis_u.py` | runner (Phases A–C) |
| `test_hypothesis_u_core.py` | shipped decision-core tests |
| `results.json` | machine-readable outcome |
| `FINDINGS.md` | this report |

Reproduce:

```bash
python3 experiments/hypothesis-u-unique-supersignal-falsification-2026-07/run_hypothesis_u.py \
  --p-max-a 50000000 --p-max-b 120000000 --p-max-c 200000000
```

---

## Next minimal step

Pressure **H-210** and **H-τ16** with the same CE-first discipline (targeted 210-multiples and `τ>16` resonant GWR beyond `2×10^8`). Do not promote either to theorem on empty finite scans.
