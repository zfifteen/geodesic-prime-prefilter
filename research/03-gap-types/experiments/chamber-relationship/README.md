# Chamber Relationship Probe

This experiment tests whether the PGS chamber enclosing a semiprime modulus
`n = p q` carries detectable locator information about the predecessor chambers
of `p` or `q`.

The factor labels are audit labels only. The measured input object is the
modulus chamber:

```text
C_n = (n^-, n^+)
```

with its selected floor, selected divisor count, normalized modulus position,
and normalized selected-floor position.

## Experiments

1. Phase echo test: compare true factor-chamber selected phases against a
   deterministic shifted-label control.
2. Locator test: compare a scale-only chamber-index predictor against a
   scale-plus-modulus-chamber-feature predictor on an odd-row holdout set.
3. Side split: rerun the locator after splitting rows by whether `n` lies at or
   after the selected floor of `C_n`.

The tested chamber relationship is unsupported on a surface when true and
shifted phase-echo medians are equal and chamber features do not reduce resolved
holdout chamber-index error beyond the scale-only baseline.

## Results

Two deterministic surfaces were measured.

| Surface | Rows | Phase echo gain for `p` | Phase echo gain for `q` | Locator median gain for `p` | Locator median gain for `q` |
|---|---:|---:|---:|---:|---:|
| `small_surface` | `7,344` | `0.0` | `0.0` | `+0.1697` | `-0.2680` |
| `medium_surface` | `27,158` | `0.0` | `0.0` | `-0.0746` | `+0.1809` |

The phase-echo detector found no separation from shifted controls on either
surface.

The chamber-feature locator did not produce stable improvement over the
scale-only baseline. The small surface slightly improved median error for `p`
and worsened `q`; the medium surface reversed that sign. Mean error worsened in
both targets on both surfaces.

The strongest positive observation is separate from locator recovery:

| Surface | `n` at selected floor | `n` after selected floor | selected `tau=4` |
|---|---:|---:|---:|
| `small_surface` | `1,852 / 7,344` | `5,481 / 7,344` | `7,325 / 7,344` |
| `medium_surface` | `6,669 / 27,158` | `20,470 / 27,158` | `27,131 / 27,158` |

On these surfaces, the modulus chamber overwhelmingly has a `tau=4` selected
floor, and `n` is usually at or after that floor. That is a real measured
modulus-chamber geometry fact. It did not localize the predecessor chambers of
`p` or `q` under the detectors tested here.

## Status

Measured result: the tested phase-echo and coarse chamber-feature locator
detectors do not detect the conjectured chamber-to-factor-chamber locator
signal on the measured surfaces.

Unresolved state: this does not rule out a different chamber relation. It rules
out this specific detector family on these two deterministic surfaces.
