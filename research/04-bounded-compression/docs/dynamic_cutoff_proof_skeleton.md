# Dynamic Cutoff Proof Skeleton

Proof status: proof target

## Theorem Target

Dynamic Cutoff Conjecture:

```text
For every right prime q, the exact unbounded GWR/DNI selected witness occurs
before C(q) = max(64, ceil(0.5 * log(q)^2)).
```

## Concrete Goal

Prove or falsify the Dynamic Cutoff Conjecture for bounded GWR/DNI prime walks.

The bounded-compression branch succeeds if it proves the cutoff law, or fails
usefully by producing the first explicit counterexample and its obstruction
type.

Mission statement:

```text
Show that exact next-prime recovery by GWR/DNI does not require scanning the
whole gap interior. It only requires a dynamic logarithmic-square window,
unless a square obstruction breaks the law.
```

## Reduction

It is enough to control the earliest obstruction before the first `d=4`
carrier.

The proof route separates the next gap into two branches:

```text
an interior square obstruction appears in the gap
no interior square obstruction appears in the gap
```

The square branch carries the extremal pressure. The non-square branch should
close by the first-`d=4` arrival rule.

## Lemma A: d=4 Fallback

Invalidated literal target:

```text
If no square undercutter appears before the first d=4 carrier, then the first
d=4 carrier is the GWR/DNI selected witness.
```

Status:

```text
False. The first failure is q = 113: first d=4 carrier 115, exact witness
121 = 11^2.
```

Viable target:

```text
If no interior prime square appears in the gap, then the first d=4 carrier is
the GWR/DNI selected witness.
```

Measured status:

```text
Survived through q <= 10,000,000:
  no-square d=4 fallback cases: 499,896
  first failure: none
```

Role:

```text
This closes the dominant non-square branch.
```

## Lemma B: Square-Offset Envelope

Target:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

Role:

```text
This bounds the rare branch that owns the sharp normalized obstruction.
```

## Lemma C: Square-Witness Rarity And Separation

Target:

```text
Prime-square witnesses occur only on a sparse obstruction subfamily, and their
offsets remain separated from the dynamic cutoff envelope.
```

Role:

```text
This supplies the structural condition behind Lemma B rather than treating
square witnesses as typical gaps.
```

## Known Evidence

```text
1e6 surface:
  gaps tested: 78,494
  first failure: none
  max witness offset: 48
  max cutoff utilization: 0.6153846153846154
  extremal witness: 259,081 = 509^2

1e7 surface:
  gaps tested: 664,575
  first failure: none
  max witness offset: 60
  max cutoff utilization: 0.6153846153846154
  extremal witness: 259,081 = 509^2

square catalog through 1e7:
  square-witness rows: 444
  top utilization row: 259,081 = 509^2

d=4 no-square fallback through 1e7:
  no-square d=4 fallback cases: 499,896
  first failure: none

square-offset envelope through prime roots <= 1e8:
  odd prime squares tested: 5,761,454
  first counterexample: none
  max utilization: 0.8120300751879699

square-offset envelope through prime roots <= 5e8:
  first counterexample: none
  standing record: 0.9341772151898734 at 424,171,123^2
```

## Open Gap

There is no proof yet that square witnesses remain below `C(q)` for all right
primes `q`.

The proof task is to turn the measured square-branch envelope into a theorem,
then use the `d=4` fallback to close the remaining branch.

## Status

This is a proof skeleton, not a proof. It records the current route from the
bounded-compression conjecture to the lemma targets needed for a proof.
