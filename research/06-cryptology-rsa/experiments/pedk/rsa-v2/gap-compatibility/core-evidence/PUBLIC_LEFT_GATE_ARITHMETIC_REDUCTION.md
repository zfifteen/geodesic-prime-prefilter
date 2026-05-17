# Public Left-Gate Arithmetic Reduction

## Finding

The public left-neighbor gate has a direct residue form.

The previous public first-open offset is `o4` exactly when the left endpoint of
the previous public gap lies in the wheel-residue set:

```text
{7, 13, 19} mod 30
```

So the active public gate is:

```text
public previous-left endpoint in {7, 13, 19} mod 30
and
public containing exact type = o6_d4_a6_d4_odd
```

This is the same gate as:

```text
previous public first-open offset o4
and
containing public exact type o6_d4_a6_d4_odd
```

but it is now written as ordinary residue arithmetic.

## Measured Contrast

Inside the same observed mod-180 factor lanes:

```text
prior rows = 42
prior rows with target containing type = 5
prior rows with previous public left endpoint in {7, 13, 19} = 10
prior rows with both = 0
```

For the observed replacement rows:

```text
observed rows = 2
observed rows with both = 2
```

The observed previous public left residues are:

```text
7, 19
```

The prior rows with the target containing type use only:

```text
1, 17, 23
```

So the prior support reaches each side of the gate separately, but not the
residue conjunction.

## Reduced Bridge

The remaining bridge sharpens from:

```text
public left-neighbor gate
and
same factor phase mod 36
and
balanced endpoint right boundary
    -> lower-twin conjunction
```

to:

```text
public previous-left endpoint in {7, 13, 19} mod 30
and
public containing exact type o6_d4_a6_d4_odd
and
same factor phase mod 36
and
balanced endpoint right boundary
    -> lower-twin conjunction
```

The remaining question is now arithmetic:

```text
Why does the target public containing type admit prior support only at
previous-left residues {1, 17, 23}, while the balanced reentry rows land at
previous-left residues {7, 19} and simultaneously lift through the lower
twin?
```

## Status

```text
theorem_status = hypothesis_not_proved
measured_status = reduced_to_public_left_gate_residue_arithmetic
remaining_bridge = public_previous_left_residue_gate_to_lower_twin
```

## Reproduction

```text
python3 public_left_gate_arithmetic_probe.py
```

Output:

```text
observed rows in residue gate = 2
prior same-lane rows in residue gate = 0
prior same-lane target containing type rows = 5
prior same-lane previous-o4 residue rows = 10
```
