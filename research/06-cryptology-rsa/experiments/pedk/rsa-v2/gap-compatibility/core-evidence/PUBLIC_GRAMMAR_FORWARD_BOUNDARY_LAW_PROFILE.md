# Public Grammar Forward Boundary Law Profile

## Claim

The simple forward-boundary law candidate is now visible.

Under the public at-winner condition, the clean right-following residue classes
are:

```text
Rres=o2|o4
Rres=o4|o4
```

Across four strict-forward windows, those two classes produced:

```text
30618 testable exact endpoint-pair exclusions
0 exact endpoint-pair falsifications
```

The remaining right-following residue classes contain every observed
right-gated exact-pair falsification.

This is measured sidecar evidence. It is not a theorem and it is not live PEDK
factor recovery.

## Right-Residue Split

The right-residue profile across all four windows is:

| right-following residue pair | testable exact cells | exact falsifications | rate per million |
| --- | ---: | ---: | ---: |
| `Rres=o2|o4` | `22509` | `0` | `0` |
| `Rres=o4|o4` | `8109` | `0` | `0` |
| `Rres=o2|o2` | `9372` | `2` | `213` |
| `Rres=o6|o6` | `2490` | `9` | `3614` |
| `Rres=o2|o6` | `712` | `4` | `5617` |
| `Rres=o4|o6` | `944` | `8` | `8474` |

The aggregate right-gated exact-pair surface was:

```text
44136 testable exact cells
23 exact falsifications
521 per million
```

The clean classes account for most of the testable surface:

```text
30618 / 44136 = 69.37 percent
```

## Phase Split

The right-following phase profile also has a simple boundary:

| right-following phases | testable exact cells | exact falsifications | rate per million |
| --- | ---: | ---: | ---: |
| `early|mid` | `11544` | `0` | `0` |
| `early|late` | `1173` | `0` | `0` |
| `early|early` | `1170` | `0` | `0` |
| `late|late` | `484` | `0` | `0` |
| `late|mid` | `10967` | `7` | `638` |
| `mid|mid` | `18798` | `16` | `851` |

All observed right-gated exact-pair falsifications occur when the
right-following phases include `mid|mid` or `late|mid`.

## Interpretation

The earlier directional result said:

```text
right-following boundary residues beat left-following and both-side residues
```

This profile makes the result simpler:

```text
o2|o4 and o4|o4 right-following residue pairs are clean exclusion carriers
under the public at-winner condition.
```

The factor endpoint-pair is still the implementation carrier, but it is not
the simplest measured law object. The simple measured object is:

```text
public at-winner condition
    selects
right-following residue-pair classes
    which exclude
exact directed endpoint-pair cells
```

The left boundary is not a primary signal. In this profile, left-side fields
mainly describe which exact endpoint pairs live inside a right-following class.
They do not create the clean split.

## Current Candidate Rule

The current candidate exclusion rule is:

```text
If N is at the public minimum-divisor position, and a right-following
factor-residue pair Rres=o2|o4 or Rres=o4|o4 is independently supported but
absent for that public word across the prior bands, then every exact directed
endpoint-pair cell carrying that right-following pair is excluded.
```

Measured status:

```text
tested_windows = 4
testable_exact_cells = 30618
exact_falsifications = 0
```

## Boundary

This does not prove the rule. It isolates the rule-shaped object.

The fragile classes are not noise to discard. They are the next resolver
problem:

```text
Rres=o2|o2
Rres=o2|o6
Rres=o4|o6
Rres=o6|o6
```

Those classes need additional structure. The clean classes currently do not.

## Reproduction

Run:

```text
python3 forward_boundary_law_profile.py
```

Primary outputs:

```text
output/forward_boundary_law_profile/summary.json
output/forward_boundary_law_profile/window_rows.jsonl
output/forward_boundary_law_profile/axis_profile_rows.jsonl
output/forward_boundary_law_profile/recurring_pair_rows.jsonl
```
