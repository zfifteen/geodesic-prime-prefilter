# Public-To-Endpoint Balance Bridge

## Finding

The compact endpoint predicate is now:

```text
avoid {1, 23}
and touch {7, 13, 19}
```

This is the endpoint-residue form of:

```text
max(a, b) = 4
```

where `a` and `b` are the first right-open offsets after the two factor
endpoints.

The public side supplies the other zero:

```text
public selected defect = 0
```

where:

```text
public selected defect =
    public_n_offset_from_left - public_gwr_winner_offset
```

The current bridge is therefore:

```text
public selected defect = 0
    aligns with stable absence at
endpoint transport defect = 0
```

The endpoint transport defect is:

```text
endpoint transport defect =
    max(a, b) - 4
```

or, in rank form:

```text
endpoint transport defect =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

## What The Bridge Is Not

The public residue of `N` modulo `30` does not determine the endpoint rule.

The compact endpoint families are:

```text
low     = {11, 17, 29}  -> first right-open offset 2
middle  = {7, 13, 19}   -> first right-open offset 4
high    = {1, 23}       -> first right-open offset 6
```

The clean endpoint predicate allows only:

```text
low|middle
middle|middle
```

Their product residues are:

```text
low|middle    -> {11, 17, 23, 29}
middle|middle -> {1, 7, 13, 19}
```

Together those two clean families cover all reduced residues modulo `30`:

```text
{1, 7, 11, 13, 17, 19, 23, 29}
```

So the rule cannot be reduced to:

```text
N mod 30 selects the endpoint family
```

The selector is the position of `N` inside its public containing gap, not the
residue of `N` alone.

## Why The Selected Position Matters

The public at-winner condition says that `N` occupies the selected
minimum-divisor position inside its public prime gap:

```text
public_n_offset_from_left = public_gwr_winner_offset
```

That is the public zero-defect condition.

The factor endpoints have their own directed right-open offsets. Multiplication
transports those endpoint movements into public composite-space:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The endpoint predicate:

```text
avoid {1, 23}
and touch {7, 13, 19}
```

says:

```text
one endpoint reaches the middle right-open offset
neither endpoint reaches the high right-open offset
```

That is the endpoint zero-defect condition.

The measured law is an absence-stability law:

```text
public selected defect = 0
and supported prior absence
and endpoint transport defect = 0
    -> stable endpoint-cell exclusion
```

The two off-balance endpoint states do not stay clean:

```text
shortfall:  max(a, b) = 2
overshoot:  max(a, b) = 6
```

They re-enter the forward surface as exact endpoint-pair falsifications.

## Measured Support

Across six strict-forward windows:

```text
21001..23000
23001..25000
25001..27000
27001..30000
30001..32000
32001..34000
```

the compact endpoint predicate has:

```text
45337 / 45337 survived
0 / 45337 exact endpoint-pair falsifications
```

The complement has:

```text
30 / 19895 exact endpoint-pair falsifications
```

The newest forward band:

```text
32001..34000
```

contributed:

```text
7503 / 7503 survived
0 / 7503 exact endpoint-pair falsifications
```

The directed transport audit confirms that the endpoint residue modulo `30`
determines the first right-open offset without mismatch across the observed
at-winner corpus:

```text
observed_at_winner_row_count = 31679
right_step_endpoint_residue_mismatch_count = 0
```

## Rule Form

Let `W` be a public at-winner composite-gap word. Let `E` be a directed
endpoint-pair cell. Define:

```text
High(E) =
    one endpoint residue is in {1, 23}

Middle(E) =
    one endpoint residue is in {7, 13, 19}
```

Then the compact exclusion rule is:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and not High(E)
and Middle(E)
    -> exclude E
```

Equivalently:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and endpoint_transport_defect(E) = 0
    -> exclude E
```

## Status

```text
theorem_status = hypothesis_not_proved
inference_status = not_live_pedk_inference
measured_status = six_window_zero_falsification_compact_predicate
bridge_status = mechanism_candidate
```

The remaining theorem task is to prove the zero-to-zero bridge:

```text
public selected defect = 0
    -> stable absence at endpoint transport defect = 0
```

for supported prior-absent endpoint cells.
