# Zero-Excess Return-Time Tail Strategy

Date: 2026-05-24

Status: candidate proof approaches for the Zero-Excess Return-Time Tail
Theorem.

The Zero-Excess Return-Time Tail Theorem asks for a dyadic large-gap bound:

$$
N_X(H)=\#\{q:X<q\le2X,\ q-p(q)\ge H\}
\le
C\frac{X(\log X)^B}{H^2}.
$$

This theorem would imply the reciprocal gap-energy bound, the reciprocal
endpoint occupancy theorem, and the endpoint drift counterterm for the
Chamber-Centered Von Mangoldt Finite-Part Principle.

Two PGS-native approaches are visible.

## Approach 1: Divisor-Field Recurrence

A large gap is a long interval with no zero-excess return:

$$
E(n)>0
\qquad
(p<n<q).
$$

The divisor-field recurrence approach would prove that such long positive
excess excursions have a square-summable tail.

The desired theorem shape is:

> **Divisor-Field Return Recurrence.**
> In each dyadic block `[X,2X]`, the divisor-count field cannot sustain
> positive excess for length at least `H` in more than
> $$
> C X(\log X)^B/H^2
> $$
> chambers.

This would be a direct PGS-native return-time law. It would not depend on
classical prime-density heuristics. It would use the integer-side fact that
zero excess is exactly `tau(n)=2` under the `n>1` guard.

### Possible Mechanism

The mechanism would need to convert divisor-count pressure inside long
positive-excess chambers into a frequency bound:

```text
long positive-excess chamber
-> many composite divisor channels must persist
-> persistence has a global occupancy cost
-> long chambers are rare enough for an H^-2 tail.
```

The local GWR theorem contributes the selected minimum-excess point inside
each chamber, but the recurrence theorem must count how often chambers of each
length can occur.

### Main Obstacle

Current divisor-field theorems are local. They identify the selected interior
minimum and the next zero-excess return once the endpoint chain is given.
They do not yet give a global occupancy cost for sustaining `tau(n)>2` over a
long interval.

The missing object is a divisor-field persistence estimate:

$$
\#\{\text{positive-excess runs of length at least }H\text{ in }[X,2X]\}
\ll
X(\log X)^B/H^2.
$$

Without that persistence estimate, divisor-field recurrence does not prove the
tail theorem.

## Approach 2: Quantitative Chamber Grammar Tail

The grammar and motif work shows measured compression in chamber states. A
theorem-facing version would upgrade that measured grammar into a quantitative
tail law for chamber widths.

The desired theorem shape is:

> **Quantitative Chamber Grammar Tail Law.**
> There is a finite or finite-memory PGS chamber grammar with a weight
> function `width(state)` such that the number of generated or admissible
> chambers in `[X,2X]` with width at least `H` is
> $$
> O(X(\log X)^B/H^2).
> $$

### Possible Mechanism

The existing measured grammar suggests a small persistent state core and a
short-memory transition law. A proof would need to add quantitative width
control:

```text
finite chamber state
-> transition law
-> width/return-time weight
-> tail bound for long positive-excess excursions.
```

If the grammar carried a Lyapunov-style weight that penalized long excursions,
then the reciprocal gap-energy theorem could follow from a finite-state energy
estimate.

### Main Obstacle

The current grammar artifacts are measured surfaces and operational pattern
evidence. They are not all-scale admissibility theorems. They also do not yet
encode an exact width-energy invariant.

To become proof machinery, the grammar track would need:

- a proved all-scale state alphabet or admissibility rule;
- a deterministic transition theorem, not only observed transition
  concentration;
- a width-energy function tied to chamber length;
- a proof that long-width paths have `H^-2` frequency or stronger.

No such theorem is currently recorded.

## Strategy Result

Both approaches require a fundamentally new global theorem.

The divisor-field route needs a positive-excess persistence estimate. The
grammar route needs a proved quantitative width-tail law.

The local GWR theorem remains useful after a chamber exists, but the
Zero-Excess Return-Time Tail Theorem is about how often long chambers occur in
the endpoint chain. That is the missing global structure.
