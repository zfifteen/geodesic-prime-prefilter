# Findings: GWR remainder-zero residual classes

**Status:** measured residual map only. Super-Signal universal rule remains **invalidated**.

## What was measured

For each consecutive prime gap with left prime `p` in a stated range:

- GWR witness `w` = leftmost interior min-`tau`
- `z(w)` on `M_v1 = (2, 3, 5, 7, 30, 210, 2310)`
- gap size `g = q - p`
- tie count for min-`tau`
- residual class `A` / `B` / `C` / `D`

## Residual classes

| Class | Definition |
| --- | --- |
| A | `z >= 4` and `g == 2` |
| B | `z >= 4` and `g > 2` and ties `> 1` |
| C | `z >= 4` and `g > 2` and unique min-`tau` |
| D | `z < 4` |

## Results

### Regime 1 (original Super-Signal claim surface): `p in [11, 2e6]`

| Class | Count |
| --- | ---: |
| A (z4 twin) | 4919 |
| B (z4 non-twin ties) | 0 |
| C (z4 non-twin unique) | 0 |
| D (z < 4) | 144010 |
| gaps | 148929 |
| bare Super-Signal FPs (B+C) | **0** |

On this surface Super-Signal looks perfect. That is why a 2e6 scan could not kill it.

### Regime 2: `p in [11, 2e7]`

| Class | Count |
| --- | ---: |
| A | 35540 |
| B | **1** |
| C | 0 |
| D | 1235062 |
| gaps | 1270603 |
| bare Super-Signal FPs (B+C) | **1** |

The single class-B row is the public counterexample:

```text
p=17666309  q=17666317  g=8
w=17666310  tau(w)=16  ties=5  z=4  first_min_index=1  div30=true
```

## Interpretation (strict)

- Super-Signal as a universal rule is **false**. Class B is nonempty by `2e7`.
- The original 2e6 surface was too small: residual class B first appears only after that window.
- Class C is empty through `2e7` in this probe. That is **measured absence**, not a theorem (Hypothesis U was separately falsified at larger scale in `hypothesis-u-unique-supersignal-falsification-2026-07`).
- No classical "primes near primorials" inference is promoted.

## Repro

```bash
python3 -m pytest experiments/gwr-remainder-zero-residual-classes-2026-07/test_residual_class_probe.py -q
python3 experiments/gwr-remainder-zero-residual-classes-2026-07/residual_class_probe.py --p-max 2000000
python3 experiments/gwr-remainder-zero-residual-classes-2026-07/residual_class_probe.py --p-max 20000000 \
  --out experiments/gwr-remainder-zero-residual-classes-2026-07/results_2e7.json
```

Artifacts: `results_2e6.json`, `results_2e7.json`.
