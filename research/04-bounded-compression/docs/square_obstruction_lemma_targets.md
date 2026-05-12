# Square Obstruction Lemma Targets

Proof status: proof target

## Branch State

The bounded-compression conjecture is:

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

The exact unbounded GWR/DNI mechanism is the reference transition. The bounded
runner tests whether the selected witness offset stays below `C(q)`.

Measured through `q <= 10,000,000`:

```text
tested gaps: 664,575
first failure: none
square-witness rows: 444
max cutoff utilization: 0.6153846153846154
sharp witness: 259,081 = 509^2
```

The square branch has low frequency and high extremal pressure.

## Lemma Targets

### 1. Square-Witness Rarity

Target claim:

```text
The GWR/DNI selected witness is a prime square only on a sparse obstruction
subfamily of prime gaps.
```

Measured role:

```text
444 square-witness rows among 664,575 tested gaps through q <= 10,000,000.
```

The theorem task is to express the structural condition that lets a prime
square undercut the competing `d=4` carriers.

### 2. Square-Offset Envelope

Target claim:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

Measured role:

```text
The sharp measured row is q = 259,033, r = 509, r^2 - q = 48,
C(q) = 78, utilization = 0.6153846153846154.
```

The theorem task is to bound the prime-square offset below the dynamic cutoff
envelope, not merely below the raw largest observed witness offset.

### 3. d=4 Fallback

Invalidated literal target:

```text
If no square undercutter appears before the first d=4 carrier, then the first
d=4 carrier is the selected witness.
```

Status:

```text
False at q = 113. The first d=4 carrier is 115, but the exact selected
witness is the later square 121 = 11^2.
```

Viable target:

```text
If no interior prime square appears in the gap, then the first d=4 carrier is
the selected witness.
```

Measured role:

```text
The dominant d=4 surface supports the rule: no interior prime square, then
first interior d=4 wins.
```

The theorem task is to close the non-square branch after the square obstruction
family is isolated.

## Status

These are lemma targets, not proved results. They define the theorem pressure
behind the bounded-compression conjecture without adding new executable
machinery.
