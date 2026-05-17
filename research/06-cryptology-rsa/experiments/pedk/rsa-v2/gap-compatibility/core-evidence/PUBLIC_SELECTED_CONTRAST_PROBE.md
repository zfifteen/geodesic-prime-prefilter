# Public Selected Contrast Probe

## Finding

The compact endpoint predicate is clean only under the public selected-position
condition.

The predicate is:

```text
avoid {1, 23}
and touch {7, 13, 19}
```

Equivalently:

```text
max(a, b) = 4
endpoint transport defect = 0
```

When the public side is `at_winner`, the predicate remains clean:

```text
0 / 45337 exact endpoint-pair falsifications
```

When the public side is `after_winner`, the same predicate leaks:

```text
25 / 1810 exact endpoint-pair falsifications
```

This is the strongest current evidence that the public selected position is an
active filter. The endpoint predicate is not clean by itself. It becomes clean
when paired with:

```text
public selected defect = 0
```

## Contrast Table

The same prior-absence and right-boundary-absence construction was run by
public side across the six strict-forward windows.

| public side | compact endpoint predicate | testable cells | exact falsifications | rate ppm |
| --- | --- | ---: | ---: | ---: |
| `at_winner` | `true` | `45337` | `0` | `0` |
| `at_winner` | `false` | `19895` | `30` | `1507` |
| `after_winner` | `true` | `1810` | `25` | `13812` |
| `after_winner` | `false` | `7386` | `105` | `14216` |
| `before_winner` | `true` | `0` | `0` | n/a |
| `before_winner` | `false` | `0` | `0` | n/a |

The same result in public-side by endpoint-defect form:

| public side | endpoint transport defect | testable cells | exact falsifications | rate ppm |
| --- | ---: | ---: | ---: | ---: |
| `at_winner` | `-1` | `14232` | `3` | `210` |
| `at_winner` | `0` | `45337` | `0` | `0` |
| `at_winner` | `+1` | `5663` | `27` | `4767` |
| `after_winner` | `-1` | `1824` | `25` | `13706` |
| `after_winner` | `0` | `1810` | `25` | `13812` |
| `after_winner` | `+1` | `5562` | `80` | `14383` |
| `before_winner` | `-1` | `0` | `0` | n/a |
| `before_winner` | `0` | `0` | `0` | n/a |
| `before_winner` | `+1` | `0` | `0` | n/a |

The `before_winner` side has no supported contrast surface in this measured
range. The corpus contains very few `before_winner` rows, so the useful
contrast is currently `at_winner` against `after_winner`.

## Mechanism Reading

The public at-winner condition is:

```text
public_n_offset_from_left = public_gwr_winner_offset
```

or:

```text
public selected defect = 0
```

The compact endpoint predicate is:

```text
endpoint transport defect = 0
```

The contrast probe shows that endpoint zero-defect does not stay clean when
the public side moves away from the selected position:

```text
after_winner
and endpoint transport defect = 0
    -> falsifies
```

The measured clean law is therefore the zero-to-zero alignment:

```text
public selected defect = 0
and endpoint transport defect = 0
    -> stable supported prior absence
```

In this contrast surface, that zero-to-zero cell is the only measured cell
with zero exact endpoint-pair falsifications.

## Rule Boundary

The rule is still an endpoint-space exclusion rule:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and not High(E)
and Middle(E)
    -> exclude E
```

where:

```text
High(E)   = one endpoint residue is in {1, 23}
Middle(E) = one endpoint residue is in {7, 13, 19}
```

This contrast does not prove the theorem. It sharpens the theorem target by
showing that the public selected-position condition is necessary in the
measured exclusion surface.

## Reproduction

Run:

```text
python3 public_selected_contrast_probe.py
```

Primary outputs:

```text
output/public_selected_contrast_probe/summary.json
output/public_selected_contrast_probe/side_rows.jsonl
output/public_selected_contrast_probe/endpoint_defect_rows.jsonl
output/public_selected_contrast_probe/window_rows.jsonl
output/public_selected_contrast_probe/candidate_rows.jsonl
```
