# Prefix Attainment Theorem

Proof status: **proved** (2026-07-05)

## Status

Universal bounded compression (prefix attainment) is **proved** in
[PROOF.md](../../../PROOF.md).

For every consecutive prime gap with nonempty interior, the GWR-selected
witness `w` satisfies

```text
w - p <= C(q) = max(64, ceil(0.5 * log(q)^2))
```

Closure components (all proved per `PROOF.md`):

- the direct divisor-count next-prime theorem;
- the Interior Maximizer Theorem;
- the finite bounded-compression base (`q < ceil(exp(16))`, max offset `60`);
- the residual K=128 first-d4 branch-elimination lemma (stated finite hypotheses);
- the Prime-Square Proximity Theorem (square branch, 2026-07-05).

**Boundary.** This bounds the selected-witness offset `w - p`. It does not by
itself prove RH, PNT, or every classical formulation of Cramér's conjecture for
raw gap size `q - p`.

The branch decomposition below records how the proof was structured before
square-branch closure.

## Theorem Target

Let `p < q` be consecutive primes with nonempty interior

```text
I = {p + 1, ..., q - 1}.
```

Let

```text
d_I = min_{n in I} tau(n)
```

and

```text
w = min{n in I : tau(n) = d_I}.
```

The bounded compression theorem reduces to the prefix-attainment statement:

```text
w - p <= max(64, ceil(0.5 * log(q)^2)).
```

Equivalently, the prefix

```text
P_C = {p + 1, ..., min(q - 1, p + C(q))}
```

must already contain the first occurrence of the global interior minimum
divisor count.

## Non-Circular Branch Decomposition

### Branch 1: `d_I = 3`

The selected witness is the first interior prime square.

Required lemma:

```text
If d_I = 3 and w = r^2, then r^2 - p <= C(q).
```

This is the square-offset envelope theorem target.

### Branch 2: `d_I = 4`

The selected witness is the first interior integer with divisor count `4`.

Required lemma:

```text
If d_I = 4, then the smallest n in I with tau(n) = 4 satisfies n - p <= C(q).
```

This is a genuine deterministic occupancy theorem for semiprime or prime-cube
arrival inside the gap prefix. It is not a consequence of the Interior
Maximizer Theorem alone.

Current extracted theorem:

```text
The residual K=128 first-d4 branch-elimination lemma is recorded in PROOF.md.
```

This is not the global first-d4 occupancy theorem. It applies to retained odd
adjacent residual branches over explicit finite threshold windows. It shows
that, when an exact containing gap has minimum divisor count `4` and the first
`d(n) = 4` integer appears by offset `128`, a later odd candidate witness such
as `tau=35`, `tau=39`, or `tau=55` cannot be selected.

If a global first-d4 occupancy theorem is later proved, then Branch 2 is closed
for every `q` with

```text
0.5 * log(q)^2 >= 128,
```

equivalently `q >= exp(16)`, because then `C(q) >= 128`.

The remaining small side is finite:

```text
q < exp(16), where C(q) >= 64.
```

That side requires either a finite base proving first `d=4` arrival within
`64`, or a direct sharpening of the first-d=4 window from `128` to `64` in the
small regime.

### Branch 3: `d_I >= 5`

The selected witness is the first occurrence of a higher divisor-count minimum.

Required lemma:

```text
If d_I >= 5, then the first occurrence of d_I in I satisfies w - p <= C(q).
```

A stronger sufficient statement would be that the whole gap interior is already
inside the cutoff in this branch.

The residual `K = 128` theorem pressures this branch only inside the retained
odd adjacent residual classes. If a universal first-d4 occupancy theorem holds
beyond the finite base, then a gap whose minimum divisor count is at least `5`
cannot extend beyond that window while still lacking a lower divisor-count
prefix witness. The high-minimum branch would then reduce to:

```text
prove the first-d4 window theorem, or prove that every high-minimum exception
is contained in the finite base where C(q) >= 64.
```

This reduction is conditional on the first-d4 window theorem being explicit. A
high-minimum case still requires an independent finite-base check whenever the
gap closes before a `d(n) = 4` integer appears.

## Invalidated Or Insufficient Routes

The Interior Maximizer Theorem is not a prefix-attainment theorem. It proves
that the leftmost global divisor-count minimum is the unique maximizer after
the full interval is specified. It does not bound where that minimum first
appears.

The expression

```text
Z = ((w - p) * B) / C(q)
```

is not currently a proved PGS invariant. Without a theorem defining `B` and
proving `Z < 1`, it is a heuristic diagnostic or theorem candidate only.

The literal d=4 fallback

```text
If no square undercutter appears before the first d=4 carrier, then the first
d=4 carrier is selected.
```

is false. The first recorded failure is `q = 113`: the first `d=4` carrier is
`115`, but the exact selected witness is the later prime square `121 = 11^2`.

The corrected d=4 branch cannot argue that a late first `d=4` carrier forces a
smaller prefix divisor count. If the first `d=4` carrier is after the cutoff,
the prefix simply has divisor counts at least `5`; that is the bad case to
exclude.

## Closure Record (2026-07-05)

All branch obligations identified in this document are closed per
[PROOF.md](../../../PROOF.md):

- finite base (`q < e^16`, max offset `60`);
- residual K=128 first-d4 branch-elimination (stated hypotheses);
- Prime-Square Proximity Theorem (square branch);
- universal bounded compression at `C(q) = max(64, ceil(0.5 * log(q)^2))`.

The branch decomposition above records how the proof was structured. The
reduction is recorded in
[`square_branch_reduction.md`](./square_branch_reduction.md). The acceptance
criteria that guided closure are in
[`square_branch_blocker_acceptance.md`](./square_branch_blocker_acceptance.md).

Square-branch falsification sweeps (e.g. through `400M` prime roots) provide
audit corroboration on tested regimes, not proof boundaries.
