# Super-Signal false-positive residual class R0

**Status split (mandatory):**

| Layer | Status |
| --- | --- |
| Super-Signal `z(w) >= 4 => g = 2` | **invalidated** (unchanged) |
| Modular lemma `z >= 4 <=> 30 \| w` on `M_v1` | **proved** (`PROOF.md`) |
| FP set through `p < 5e7` | **measured** (catalog) |
| Algebraic form on those FPs | **measured** (catalog rows) |
| "Every FP at any scale is in R0" | **hypothesis** only |
| Verified / validated | **not claimed** (no `10^18` surface) |

**Anti-revival:** This does not repair Super-Signal. Class R0 describes
observed failures. It is not the theorem `z >= 4 => (g = 2 or R0)`.

## Observable object

A Super-Signal false positive (FP) is a non-twin consecutive prime gap
(`g = q - p > 2`) whose GWR selected witness `w` is divisible by 30.

## Residual class R0 (descriptive)

```text
R0 = { class-A, tau(w) = 16, g = 8, seven-open }
```

Independence note: on the measured form `w = 2*3*5*r` with `r` prime,
`tau(w) = 16` is forced. The freer residual pressure is mainly class-A,
`g = 8`, and seven-open, plus the absence of other forms.

## Algebraic form (measured on the five catalog rows)

```text
w = 2 * 3 * 5 * r   (r prime)
p = 30 * r - 1
q = 30 * r + 7
```

Status: **measured** on the FP list below. Not a generative theorem.

## Measured fact (through `p < 50_000_000`)

Exactly five Super-Signal FPs. All five lie in R0. Zero FPs outside R0.
Evaluation label: `all_fps_in_R0` (not vacuous).

| p | q | g | w | r | tau(w) | w%7 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 17666309 | 17666317 | 8 | 17666310 | 588877 | 16 | 4 |
| 22284029 | 22284037 | 8 | 22284030 | 742801 | 16 | 6 |
| 39110069 | 39110077 | 8 | 39110070 | 1303669 | 16 | 6 |
| 45515369 | 45515377 | 8 | 45515370 | 1517179 | 16 | 5 |
| 49117829 | 49117837 | 8 | 49117830 | 1637261 | 16 | 6 |

The first two are the pinned `PROOF.md` CEs. The last three appeared after
extending the scan past 25e6 and still match R0 and the algebraic form.

## Hypothesis (universal)

Every Super-Signal FP at any scale lies in R0.

**Disconfirmation:** any FP with `off != 1`, or `tau(w) != 16`, or `g != 8`,
or `7 | w`.

## Related residual tracks

| Object | Relation |
| --- | --- |
| H-210 | separate hypothesis; bare FPs here are seven-open, so they do not stress H-210 antecedents |
| H-tau16 | dual: no bare FP here has `tau(w) > 16` |

## Reproduce (regenerates `measure.json`)

```text
python3 research/16-predictions/probes/super-signal-fp-signature-2026-07/probe_fp_signature.py --p-max 50000000
```

## Exact limits

- Highest measured package magnitude: `5e7`.
- Sample size is five FPs. Universality of R0 is unresolved.
- No verified/validated language. No `PROOF.md` edit. No Super-Signal restore.


## Extension surfaces (measured, labeled)

### Targeted class-A search through `p < 1e8`

Method: candidates `p = 30r - 1` with `r` prime and `p+2` composite, then GWR.
Limitation: misses non-class-A FPs if any exist above the full-sieve regime.

| `p_max` | candidates | Super-Signal FPs | outside R0 |
| ---: | ---: | ---: | ---: |
| 5e7 | 21518 | 5 | 0 |
| 1e8 | 39495 | 20 | 0 |

Artifact: `targeted_extension.json`

### Full-sieve completeness band `[5e7, 6e7)`

Full GWR on all nontwin gaps. Result: 2 FPs, both class-A and in R0, 0 non-class-A.
Matches the two targeted hits in that band. Artifact: `band_5e7_6e7_full.json`

Status: **measured on named surfaces only**. Universal R0 remains **hypothesis**.
