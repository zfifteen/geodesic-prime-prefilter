# Simple Right-Residue Invariant

## Claim

The current clean exclusion surface collapses to one simple invariant:

```text
under the public at-winner condition,
the maximum right-following factor endpoint residue is o4
```

This single condition exactly collects the two previously clean classes:

```text
Rres=o2|o4
Rres=o4|o4
```

It excludes the low-only case:

```text
Rres=o2|o2
```

and every case that touches the high residue:

```text
Rres=o2|o6
Rres=o4|o6
Rres=o6|o6
```

## Measured Result

Across the four strict-forward windows already used by the boundary-law
profile:

```text
21001..23000
23001..25000
25001..27000
27001..30000
```

the split is:

| right-following maximum residue | testable exact cells | exact falsifications | rate per million |
| --- | ---: | ---: | ---: |
| `o4` | `30618` | `0` | `0` |
| `o2` | `9372` | `2` | `213` |
| `o6` | `4146` | `21` | `5065` |

Window by window, `right_residue_max=o4` stays clean:

| strict-forward window | testable exact cells | exact falsifications |
| --- | ---: | ---: |
| `21001..23000` | `8903` | `0` |
| `23001..25000` | `6915` | `0` |
| `25001..27000` | `6448` | `0` |
| `27001..30000` | `8352` | `0` |

The complement is not clean:

| strict-forward window | testable exact cells | exact falsifications |
| --- | ---: | ---: |
| `21001..23000` | `3862` | `4` |
| `23001..25000` | `2468` | `3` |
| `25001..27000` | `3136` | `4` |
| `27001..30000` | `4052` | `12` |

## Interpretation

The simple measured object is not the pair label itself. It is the upper
boundary reached by the two right-following endpoint residues.

Using the residue rank:

```text
o2 = 1
o4 = 2
o6 = 3
```

the clean condition is:

```text
max(right endpoint residue ranks) = 2
```

The right-following side must reach the middle residue and must not reach the
high residue. Too low and too high both leave the clean surface.

This is the first genuinely simple invariant candidate in this branch:

```text
public selected position of N
    aligns with
middle right-following endpoint residue maximum
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = zero_falsification_candidate_invariant
tested_exact_cells = 30618
exact_falsifications = 0
```

## Reproduction

Run:

```text
python3 simple_invariant_probe.py
```

Primary outputs:

```text
output/simple_invariant_probe/summary.json
output/simple_invariant_probe/invariant_profile_rows.jsonl
output/simple_invariant_probe/window_rows.jsonl
```
