# Phase-Lock Public Left Residue Lemma

## Statement

Under the current public `o6` residue-bridge conditions:

```text
{p mod 30, q mod 30} = {13, 19}
```

and the factor phase-lock condition:

```text
p mod 36 = q mod 36
```

the product satisfies:

```text
N = pq = 37 mod 60
```

Since the public selected offset in the trigger is `6`, the left endpoint of
the public gap satisfies:

```text
public left endpoint = 31 mod 60
```

## Proof

The residue bridge gives:

```text
p = 13 or 19 mod 30
q = 19 or 13 mod 30
```

Both `13` and `19` are congruent to `1 mod 6`, so:

```text
p = 1 mod 6
q = 1 mod 6
N = 1 mod 6
```

The product of the forced mod-30 residues is:

```text
13 * 19 = 247 = 7 mod 30
```

So:

```text
N = 7 mod 30
N = 1 mod 6
```

Modulo `60`, the residues congruent to `7 mod 30` are:

```text
7, 37
```

Only one of these is congruent to `1 mod 6`:

```text
37 = 1 mod 6
```

Therefore:

```text
N = 37 mod 60
```

In the public `o6` trigger, the selected offset is:

```text
N - public left endpoint = 6
```

So:

```text
public left endpoint = 37 - 6 = 31 mod 60
```

## Role

This lemma connects the factor-side phase lock back to the public selected
position. The current proof target is no longer only a factor-neighborhood
statement. It has a public residue anchor:

```text
public left endpoint = 31 mod 60
```

The remaining measured obstruction is:

```text
same phase mod 36
and
public left endpoint 31 mod 60
and
balanced endpoint boundary
    -> four-slot lower-twin chain
```

## Status

```text
theorem_status = proved_modular_lemma
proof_role = public_factor_phase_bridge
```
