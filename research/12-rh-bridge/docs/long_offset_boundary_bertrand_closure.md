# Long-Offset Boundary Bertrand Closure

Date: 2026-05-24

Status: candidate-treatment comparison and boundary closure for the
fourth-moment uncovered-set range.

The first-moment endpoint-density note proves the required positive mean in
the interior range `N <= X/2`. The apparent remaining case is `N > X/2`, where
the shifted intervals `M-(2s+1)` can leave the dyadic prime range. There are
three natural treatments of this boundary.

## Candidate Treatments

### 1. Restrict The Fourth-Moment Range

Run the fourth-moment uncovered-set argument only for

$$
N\le X/2+O(1).
$$

Then every offset

$$
h=2s+1,\qquad s<N,
$$

satisfies `h <= X+O(1)`, so the first-moment endpoint-density input applies
to the shifted intervals

$$
[X-h,2X-h].
$$

The trade-off is that the complementary range `N > X/2` must be shown empty
or bounded by a separate endpoint-gap input. This path keeps the Selberg
upper-bound tuple estimates unchanged and preserves the parity normalization:
`M` remains even, `h` remains odd, and `M-h` remains odd.

### 2. Re-Dyadize In The Shifted Prime Variable

Instead of keeping `M` as the only dyadic variable, set

$$
u=M-(2s+1)
$$

and dyadically decompose `u`. This keeps prime endpoint density available even
when `h` is large.

The trade-off is added bookkeeping. The Selberg tuple forms no longer live in
one fixed center block with one offset interval; the proof must track how
many pairs `(M,s)` land in each shifted `u`-block. Parity remains manageable,
but the fourth-moment assembly becomes a two-parameter dyadic sum rather than
a single-block estimate.

### 3. Invoke A Global Prime-Gap Upper-Tail Input

A global endpoint-gap theorem could directly bound centers whose previous
endpoint lies more than `X` behind them.

The trade-off is proof-source cost. This imports a stronger global arithmetic
input than the local shifted-sieve moment argument needs. It may also obscure
which part of the RH bridge is being supplied by PGS divisor-channel structure
and which part is being imported from classical prime-gap theory.

The first treatment is the cleanest if the complementary range is empty by a
half-reset theorem.

## Age And Odd-Offset Length

For an even center `M`, let

$$
a(M)=M-p(M)
$$

be the backward distance to the previous zero-excess endpoint.

A complete odd-offset cover of length

$$
H=2N+O(1)
$$

behind `M` requires

$$
a(M)\ge H.
$$

Thus the long-offset case `N > X/2` corresponds to age exceeding `X` up to
constant endpoint conventions.

## Bertrand Half-Reset

Bertrand's postulate gives a prime in

$$
(M/2,M)
$$

for every `M>2`. Therefore the previous endpoint satisfies

$$
p(M)>M/2,
$$

and hence

$$
a(M)=M-p(M)<M/2.
$$

For centers in the dyadic block

$$
X\le M\le2X,
$$

this gives

$$
a(M)<X.
$$

Consequently, no center in `[X,2X]` can support a complete backward cover of
odd-offset length `H >= X`.

Since `H=2N+O(1)`, the extinction event is empty once

$$
N>X/2+O(1).
$$

## Resolution Of Treatment 1

The fourth-moment uncovered-set argument only needs to treat

$$
N\le X/2+O(1).
$$

In exactly this range, every offset

$$
h=2s+1,\qquad s<N,
$$

satisfies

$$
h\le X+O(1),
$$

so the shifted interval

$$
[X-h,2X-h]
$$

has enough positive prime range for the first-moment endpoint-density lower
bound.

Thus the interior first-moment lemma and the Bertrand half-reset fit together:

```text
N <= X/2  -> endpoint-density mean applies;
N > X/2   -> complete-cover event is empty.
```

## Source Status

Bertrand's postulate is an external endpoint-existence theorem unless it is
restated and proved inside the PGS source framework. For a PGS-internal bridge,
the needed statement is:

> **Endpoint Half-Reset Lemma.**
> For every `M>2`, the previous zero-excess endpoint satisfies
> $$
> p(M)>M/2.
> $$

This lemma is weaker than the full endpoint-density input and only closes the
long-offset boundary.

## Result

The long-offset dyadic boundary is closed. The fourth-moment uncovered-set
argument only needs the interior range `N <= X/2`, where the shifted
first-moment endpoint-density estimate applies. No separate very-long-offset
tail theorem is needed for this boundary.
