# Prefix Attainment Theorem Target

Proof status: proof target

## Status

The bounded dynamic cutoff theorem is unresolved.

The proved baseline remains:

- the direct divisor-count next-prime theorem in `PROOF.md`;
- the Interior Maximizer Theorem in `PROOF.md`.
- the finite bounded-compression base in `PROOF.md`: for every consecutive
  prime pair `p < q` with `q < ceil(exp(16)) = 8,886,111`, the selected witness
  satisfies `w - p <= 60`.
- the residual K=128 first-d4 branch-elimination lemma in `PROOF.md`, which
  closes the retained odd adjacent `tau=35`, `tau=39`, and `tau=55` residual
  branches under exact finite hypotheses.

The current bounded compression rule

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

is measured evidence, not theorem status.

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

## Next Proof Action

The next theorem-bearing action is to extract the referenced first-d4 window
lemma and decide whether it is a theorem or only an artifact-level support
claim. The supported residual theorem has now been extracted. The broader
global theorem remains open:

```text
For all consecutive prime gaps beyond the committed finite base, if the gap
has a tau(n) = 4 interior integer, then the first such integer appears within
128 of the left endpoint.
```

The finite base side is now proved in `PROOF.md`, with maximum selected-witness
offset `60` across `542,081` nonempty prime-gap interiors below
`ceil(exp(16))`.

If the `K = 128` theorem is recovered, the dynamic cutoff theorem reduces to
one exact all-scale remaining obligation:

```text
square branch: prove every selected prime-square witness satisfies
r^2 - p <= C(q).
```

That square branch is not closed by the current artifacts. It requires a
separate theorem bounding the distance from a selected interior prime square to
the preceding prime by the dynamic logarithmic-square cutoff.

The exact missing theorem is:

```text
For every prime r, let p be the greatest prime below r^2. If r^2 lies in the
prime gap after p and is the selected divisor-count minimum, then
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

The current square-branch search through prime roots `<= 100,000,000` is
evidence for this theorem, not a proof of it.

The reduction is recorded separately in
[`square_branch_reduction.md`](./square_branch_reduction.md). The exact proof
acceptance boundary is recorded in
[`square_branch_blocker_acceptance.md`](./square_branch_blocker_acceptance.md).

The proof must supply deterministic arrival of a semiprime or prime cube, or
an exact finite-base reduction. Heuristic density, Cramer-style gap
assumptions, random arrival language, and finite audit surfaces do not close
this lemma.
