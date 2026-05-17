# Zero-To-Zero Landed State

## Result

The simple invariant beneath the current PEDK gap compatibility signal is:

```text
public_selected_defect = 0
and
endpoint_transport_defect = 0
```

This is the rule surface:

```text
public_selected_defect(W) = 0
and prior_absent(W, E)
and supported(E)
and endpoint_transport_defect(E) = 0
    -> exclude E
```

## Public Side

The public object is the prime gap containing `N`.

Inside that public gap, GWR selects a minimum-divisor position. The public
defect is:

```text
public_selected_defect(W) =
    public_n_offset_from_left - public_gwr_winner_offset
```

So:

```text
public_selected_defect(W) = 0
```

means:

```text
N sits at the selected public position.
```

## Endpoint Side

The endpoint object is directed. For each factor endpoint, take the first open
position immediately to its right.

Let:

```text
a = first right-open offset after p
b = first right-open offset after q
```

The endpoint transport defect is:

```text
endpoint_transport_defect(E) = max(a, b) - 4
```

The zero endpoint condition is:

```text
max(a, b) = 4
```

In residue form:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

## Transport

The endpoint movements transport through multiplication:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

This is why the right-following endpoint gaps are the active directed object.
They are the first outward transport steps available to the factor endpoints.

## Evidence

The executable rule kernel emits:

```text
excluded_endpoint_cell_count = 45337
exact_falsification_count = 0
falsification_rate_ppm = 0
```

The public-side by endpoint-defect contrast matrix shows that the clean cell is
the combined zero:

```text
at_winner, endpoint defect -1 -> 3 / 14232 falsified
at_winner, endpoint defect  0 -> 0 / 45337 falsified
at_winner, endpoint defect +1 -> 27 / 5663 falsified

after_winner, endpoint defect -1 -> 25 / 1824 falsified
after_winner, endpoint defect  0 -> 25 / 1810 falsified
after_winner, endpoint defect +1 -> 80 / 5562 falsified
```

The endpoint zero does not stay clean away from the public selected position.
The public selected position is therefore part of the filter.

## Boundary

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = exact_zero_falsification_endpoint_space_exclusion_rule
```

This is not live factor recovery.

This is not a claim that every true factor pair under `public_at_winner` has
endpoint transport defect zero.

It is an endpoint-space exclusion rule over supported prior-absent cells.

## Next Proof Obligation

The remaining theorem step is:

```text
why does public_selected_defect = 0 stabilize supported prior absence
exactly at endpoint_transport_defect = 0?
```

That is the proof problem now. The broad representation search is done.
