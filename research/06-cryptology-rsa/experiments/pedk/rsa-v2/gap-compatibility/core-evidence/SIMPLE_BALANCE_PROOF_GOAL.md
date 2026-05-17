# Simple Balance Proof Goal

## Goal

Prove the simple reason that the selected public position stabilizes
endpoint-space absence exactly at the balanced right endpoint condition.

The proof should not introduce another compatibility catalog. The current
object has already collapsed to two concrete facts:

```text
N is the first minimum-divisor composite in its public prime gap
and
the two factor endpoints reach the middle right-open boundary without crossing it
```

That is the goal now.

## Public Side

In this corpus, `N = pq` with distinct prime factors. Therefore:

```text
tau(N) = 4
```

If `N` is the selected public position inside its containing prime gap, then the
gap winner has divisor count `4`. The measured corpus verifies:

```text
public at selected position, selected divisor count 4: 65137 rows
public at selected position, selected divisor count not 4: 0 rows
```

So the public condition can be read without extra terminology:

```text
N is the first integer in its public prime gap where the divisor count reaches 4
```

Equivalently:

```text
no earlier integer in the same public prime gap has divisor count 3 or 4
```

This is the first simplification. The public side is a first-minimum statement.

## Endpoint Side

Each factor endpoint has a first open position to its right. Let:

```text
a = first right-open offset after p
b = first right-open offset after q
```

For the current wheel states:

```text
a, b are in {2, 4, 6}
```

The clean endpoint condition is:

```text
max(a, b) = 4
```

That means:

```text
at least one endpoint reaches the middle right-open offset
and neither endpoint reaches the high right-open offset
```

In residue form:

```text
both endpoint residues avoid {1, 23}
and at least one endpoint residue is in {7, 13, 19}
```

This is the second simplification. The endpoint side is a middle-boundary
statement.

## Transport

Right movement at the factor endpoints transports through multiplication:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

The first available right movements around `p` and `q` therefore become the
first directed outward product movements from `N`.

The balanced endpoint condition is the exact middle case of the three possible
right-boundary states:

```text
shortfall: max(a, b) = 2
balance:   max(a, b) = 4
overshoot: max(a, b) = 6
```

## Current Measured Law

Over supported prior-absent endpoint cells, the measured surface is:

```text
selected public position and max(a, b) = 4
    -> 45337 exclusions, 0 exact falsifications
```

The neighboring endpoint states leak:

```text
selected public position and max(a, b) = 2
    -> 14232 testable cells, 3 exact falsifications

selected public position and max(a, b) = 6
    -> 5663 testable cells, 27 exact falsifications
```

The balanced endpoint condition also leaks away from the selected public
position:

```text
after selected public position and max(a, b) = 4
    -> 1810 testable cells, 25 exact falsifications
```

So neither side is sufficient alone. The stable surface is the joint event:

```text
first divisor-count-4 position in the public gap
and
middle right-open endpoint boundary
```

## Proof Shape

The proof should reduce to four small lemmas.

### Lemma 1: First-Minimum Public Lemma

For a semiprime `N = pq` with `p != q`, if `N` is the selected public position
inside its containing prime gap, then `N` is the first interior integer in that
gap with divisor count `4`.

This follows from `tau(N) = 4` and the definition of the selected gap position
as the first integer attaining the minimum divisor count.

### Lemma 2: Right-Boundary Trichotomy

The first right-open endpoint offsets fall into exactly three ordered states:

```text
2 < 4 < 6
```

The balanced state is the middle state:

```text
max(a, b) = 4
```

### Lemma 3: Directed Product Transport

The first right-open endpoint movements transport into product space by:

```text
aq
bp
aq + bp + ab
```

Thus the endpoint boundary is not decoration around the factors. It is the
first directed product boundary available from `N`.

### Lemma 4: First-Minimum Balance Lemma

For supported endpoint cells that are absent before the forward band, a true
balanced endpoint realization under the selected public position would have to
preserve both:

```text
N is the first divisor-count-4 point in the public gap
and
the endpoint product boundary reaches the middle state without overshoot
```

The theorem must show that those two requirements are incompatible for a
previously absent balanced endpoint cell. That gives the desired contradiction:

```text
selected public position
and supported prior absence
and max(a, b) = 4
    -> endpoint cell remains absent
```

This is the remaining proof step.

## Current Status

```text
theorem_status = hypothesis_not_proved
measured_status = 45337 exclusions, 0 exact falsifications
proof_reduction_status = reduced_to_first_minimum_balance_lemma
```

The next move is to prove Lemma 4 directly or find the smaller invariant inside
it.
