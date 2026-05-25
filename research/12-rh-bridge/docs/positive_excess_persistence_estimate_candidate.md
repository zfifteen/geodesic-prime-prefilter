# Positive-Excess Persistence Estimate Candidate

Date: 2026-05-24

Status: candidate missing estimate for the divisor-field recurrence route.

The Zero-Excess Return-Time Tail Theorem requires a square-summable tail for
long positive-excess excursions:

$$
N_X(H)=\#\{q:X<q\le2X,\ q-p(q)\ge H\}
\le
C\frac{X(\log X)^B}{H^2}.
$$

This note formulates the positive-excess persistence estimate that would
produce that tail and records why current local divisor-count/GWR results do
not yet prove it.

## Positive-Excess Runs

In a chamber `(p,q]`,

$$
E(n)>0
\qquad(p<n<q),
$$

and

$$
E(q)=0.
$$

Thus the prime gap length

$$
g(q)=q-p
$$

is the return time from one zero-excess endpoint to the next.

The required estimate is:

> **Positive-Excess Persistence Estimate.**
> In every dyadic block `[X,2X]`, positive-excess runs of length at least `H`
> obey
> $$
> N_X(H)\le C X(\log X)^B/H^2.
> $$

Equivalently,

$$
\sum_{X<q\le2X}g(q)^2
\le
C X(\log X)^B.
$$

## Why First-Moment Occupancy Is Not Enough

The endpoint chambers partition the integer line. Therefore

$$
\sum_{X<q\le2X}g(q)\le X+O(\max g).
$$

This gives only the first-moment tail

$$
N_X(H)\le \frac{X}{H}+O(1).
$$

The divisor-count excess area does not improve this enough. Since every
interior composite has `tau(n) >= 3`,

$$
E(n)=\left(\frac{\tau(n)}2-1\right)\log n
\ge
\frac12\log n.
$$

A chamber of width `H` carries positive-excess area at least comparable to

$$
H\log X.
$$

But the total positive-excess area on `[X,2X]` is itself first-moment sized.
Markov-type counting again gives an `H^-1` tail, not the required `H^-2`
tail.

The gap-energy theorem needs second-moment control, not just total occupancy
or total excess area.

## Candidate Divisor-Field Mechanism

A long positive-excess run means every integer in a long interval has at least
one nontrivial divisor channel:

```text
for each p < n < q, tau(n) > 2.
```

A divisor-field proof would need to show that complete persistence of these
channels over length `H` has a quadratic global cost.

The needed mechanism has the shape:

```text
long run of positive excess
-> interval must be completely covered by divisor channels
-> complete divisor-channel coverings of length H are rare with H^-2 tail
-> positive-excess return times have square-summable tail.
```

This is a global covering theorem for the divisor field.

## Additional Structure Required

The estimate requires one of the following new inputs.

1. **Divisor-channel covering bound.**
   A theorem bounding how often intervals of length `H` can be completely
   covered by proper-divisor residue channels.

2. **Persistence-energy inequality.**
   A global inequality of the form
   $$
   \sum_{X<q\le2X}g(q)^2
   \le
   C X(\log X)^B
   $$
   derived directly from divisor-count structure.

3. **Return-time quasi-orthogonality.**
   A theorem showing that long positive-excess runs cannot cluster often
   enough to violate the dyadic second-moment bound.

4. **Quantitative recurrence invariant.**
   A PGS invariant that assigns a cost to sustaining `E(n)>0` and proves the
   total cost over `[X,2X]` is `O(X(log X)^B)` while each run of length `H`
   costs at least `H^2`.

## Role Of GWR

The GWR theorem identifies the leftmost minimum-excess point inside each
positive-excess chamber. It can contribute local information about where the
least divisor-channel load occurs.

It does not currently attach a quadratic persistence cost to the full chamber
length. A long chamber can have a valid GWR selector without violating any
local theorem recorded in `PROOF.md`.

To use GWR for the persistence estimate, a new theorem would need to connect

$$
\text{selector position and divisor-count minimum}
$$

to

$$
\text{global frequency of long zero-excess return times}.
$$

That connection is not present yet.

## Result

The positive-excess persistence estimate is a new global divisor-field
theorem. It cannot be obtained from first-moment chamber occupancy, excess
area, or the current local GWR theorem.

The missing ingredient is a quadratic persistence cost for long
positive-excess runs.
