# Dynamic Cutoff Proof Skeleton

## Theorem Target

Dynamic Cutoff Conjecture:

```text
For every right prime q, the exact unbounded GWR/DNI selected witness occurs
before C(q) = max(64, ceil(0.5 * log(q)^2)).
```

## Reduction

It is enough to control the earliest obstruction before the first `d=4`
carrier.

The proof route separates the next gap into two branches:

```text
square obstruction appears before the first d=4 carrier
no square obstruction appears before the first d=4 carrier
```

The square branch carries the extremal pressure. The non-square branch should
close by the first-`d=4` arrival rule.

## Lemma A: d=4 Fallback

Target:

```text
If no square undercutter appears before the first d=4 carrier, then the first
d=4 carrier is the GWR/DNI selected witness.
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
```

## Open Gap

There is no proof yet that square witnesses remain below `C(q)` for all right
primes `q`.

The proof task is to turn the measured square-branch envelope into a theorem,
then use the `d=4` fallback to close the remaining branch.

## Status

This is a proof skeleton, not a proof. It records the current route from the
bounded-compression conjecture to the lemma targets needed for a proof.
