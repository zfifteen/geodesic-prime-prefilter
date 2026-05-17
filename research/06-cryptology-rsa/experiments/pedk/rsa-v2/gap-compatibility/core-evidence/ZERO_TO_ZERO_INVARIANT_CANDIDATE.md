# Zero-To-Zero Invariant Candidate

## Candidate Law

The simple invariant beneath the current PEDK gap compatibility signal is:

```text
zero public defect
plus
zero endpoint transport defect
```

In rule form:

```text
public_selected_defect(W) = 0
and prior_absent(W, E)
and supported(E)
and endpoint_transport_defect(E) = 0
    -> exclude E
```

This is the compact PGS-native exclusion rule currently supported by the
evidence.

## Public Defect

The public object is the prime gap containing `N`.

Inside that gap, GWR selects a minimum-divisor position. The public defect is:

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
N sits exactly at the GWR-selected position inside its public containing gap.
```

## Endpoint Transport Defect

Each factor endpoint has a first open offset immediately to its right.

Let:

```text
a = first right-open offset after p
b = first right-open offset after q
```

The possible endpoint offsets are:

```text
2, 4, 6
```

They are fixed by endpoint residue modulo `30`:

```text
offset 2: {11, 17, 29}
offset 4: {7, 13, 19}
offset 6: {1, 23}
```

The endpoint transport defect is:

```text
endpoint_transport_defect(E) =
    (max(a, b) - 4) / 2
```

Equivalently:

```text
endpoint_transport_defect(E) =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

Thus:

```text
endpoint_transport_defect(E) = 0
```

means:

```text
max(a, b) = 4
```

or, in endpoint residue form:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

## Transport Mechanism

Rightward endpoint movement transports through multiplication:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The right-following endpoint offsets are therefore not decorative labels. They
are the first outward transport steps available to the two factor endpoints.

The public selected position is not a residue class of `N`. The clean endpoint
families multiply to all reduced residues modulo `30`, so `N mod 30` alone
cannot select the law.

The selected position supplies a public zero:

```text
public_selected_defect = 0
```

The compact endpoint predicate supplies a transport zero:

```text
endpoint_transport_defect = 0
```

The measured law is the alignment of those two zeros.

## Measured Signature

Across six strict-forward windows, the zero-to-zero cell is clean:

```text
public_selected_defect = 0
endpoint_transport_defect = 0
    -> 0 / 45337 exact endpoint-pair falsifications
```

Moving the endpoint defect away from zero leaks:

```text
public_selected_defect = 0
endpoint_transport_defect = -1
    -> 3 / 14232 exact endpoint-pair falsifications

public_selected_defect = 0
endpoint_transport_defect = +1
    -> 27 / 5663 exact endpoint-pair falsifications
```

Moving the public side away from zero also leaks:

```text
after_winner
endpoint_transport_defect = 0
    -> 25 / 1810 exact endpoint-pair falsifications
```

The current measured matrix has only one zero-falsification supported cell:

```text
public_selected_defect = 0
endpoint_transport_defect = 0
```

## Theorem Target

The theorem should prove that supported prior absence is stable exactly at the
zero-to-zero alignment:

```text
public_selected_defect(W) = 0
and prior_absent(W, E)
and supported(E)
and endpoint_transport_defect(E) = 0
    -> exclude E
```

Equivalently:

```text
N at the selected public position
and endpoint transport reaches but does not cross the middle right-open offset
    -> stable endpoint-cell exclusion
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = six_window_zero_falsification_zero_to_zero_cell
candidate_invariant = public_selected_defect_zero_plus_endpoint_transport_defect_zero
```

The missing proof is no longer a broad grammar search. It is the zero-to-zero
bridge:

```text
why does zero public selected defect stabilize supported absence only at zero
endpoint transport defect?
```
