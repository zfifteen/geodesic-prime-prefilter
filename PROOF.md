# Proof

## Headline Theorem

This document proves three universal pillars of Prime Gap Structure.

**1. Direct next-prime rule.** Given a known prime `p`, compute exact divisor
counts for the integers greater than `p`, in increasing order, and stop at the
first integer with exactly two positive divisors. That integer is the next
prime `q`.

For a positive integer `n`, let `tau(n)` be the number of positive divisors of
`n`. The theorem defines `q` from `p` alone:

$$q=\min\{n>p:\tau(n)=2\}$$

**2. Interior maximizer (GWR).** Among the integers strictly between `p` and
`q`, the first integer with the smallest divisor count is the unique maximizer
of the logarithmic comparison function below.

**3. Universal bounded compression.** For every consecutive prime gap with
nonempty interior, the GWR-selected witness `w` (the first interior integer
with minimum divisor count) satisfies

```text
w - p <= max(64, ceil(0.5 * log(q)^2)).
```

This bound sits at the Cramér scale — the same `(log q)^2` envelope as
Cramér's conjecture — and is proved deterministically from divisor-count
invariants. The final square-branch case is closed by the **Prime-Square
Proximity Theorem** (proved 2026-07-05).

**Boundary.** This is a proved bound on the selected-witness offset `w - p`
(prefix attainment). It does not by itself prove the Riemann Hypothesis, the
Prime Number Theorem, or every classical formulation of Cramér's conjecture for
raw consecutive-prime gap size `q - p`. Lean 4 carries structural axioms
pending full machine-checked derivation; the mathematical proof lives here.

All three pillars are universal under their stated hypotheses. The proof uses a
finite base below `5,000,000,001` and then closes the remaining earlier-integer
side by exact divisor-count arithmetic. The computation tables in this document
certify the finite base and implementation surfaces; they are not limits on the
theorem.

## Downstream Riemann-Hypothesis Reading

This document proves the direct next-prime rule and the interior maximizer
theorem. The Riemann-hypothesis-facing documentation uses this source layer in
the downstream order. In that downstream zeta compression, the load is
`H(n)=log n+E(n)`:

```text
divisor counts -> local theorems -> zeta compression
-> source-to-spectral placement target -> pole placement/RH sentence
```

`PROOF.md` controls the local theorem status. It does not itself prove RH. The
Riemann-hypothesis-facing reading path is built on that source layer, and the
source-to-spectral placement step remains a separate proof target.

## What This Proof Establishes

This file proves the local integer-level foundation of Prime Gap Structure.

- Direct next-prime rule: given a known prime `p`, exact divisor-count traversal
  returns the next prime `q`.
- Interior maximizer theorem: inside a nonempty prime-gap interval, the
  leftmost integer with minimum divisor count is the unique maximizer of
  `F(n)=(1-tau(n)/2)log(n)`.
- Finite bounded-compression base: for every consecutive prime pair with
  `q < ceil(exp(16))`, the selected witness satisfies `w - p <= 60`.
- Residual K=128 first-d4 branch-elimination lemma: on retained odd adjacent
  residual branches, the first-d4 window eliminates the listed high-τ witness
  candidates under the stated finite hypotheses.
- Prime-Square Proximity Theorem: on the square branch (`tau(w) = 3`), the
  distance from the left boundary prime to the first interior prime square
  `r^2` satisfies `r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))`.
- Universal bounded compression: the dynamic cutoff
  `C(q) = max(64, ceil(0.5 * log(q)^2))` holds for the GWR-selected witness
  on every prime-gap branch.

These theorems are the arithmetic base layer built from divisor counts and
ordered gap interiors. They are not empirical scans, heuristic approximations,
or restatements of the Prime Number Theorem (PNT) or the Riemann Hypothesis
(RH).

They are the source-side arithmetic foundation: exact divisor counts, exact
prime returns, and exact ordered gap interiors. RH-facing documentation reads
that source layer through downstream zeta-compressed language. That downstream
reading is not a theorem proved by this file.

Zeta, PNT, RH, zero geometry, and pole placement are not inputs to these local
theorems. The proof starts with the exact divisor-count field and proves
the arithmetic structure that places the next prime and orders the gap interior.
RH-facing and PNT-facing language enters downstream, after this integer-level
source has already been fixed.

## The Algorithm

Input a known prime `p`.

Check the integers `p + 1`, `p + 2`, `p + 3`, and so on, in increasing order.
For each integer `n`, compute `tau(n)` exactly.

Stop at the first integer `n` with `tau(n) = 2`. Output that integer as `q`.

## Why The Algorithm Returns The Next Prime

An integer `n > 1` is prime exactly when its only positive divisors are `1` and
`n`. Therefore `tau(n) = 2` exactly when `n` is prime.

There is always a prime greater than `p`. The set of primes greater than `p` is
nonempty, so it has a least element. Call that least prime `q`.

The algorithm checks integers greater than `p` in increasing order. It cannot
stop before `q`, because any integer `n` with `p < n < q` is not prime and
therefore has `tau(n) != 2`. It does stop at `q`, because `q` is prime and
therefore has `tau(q) = 2`.

Thus the algorithm determines the next prime after `p`.

## Basic Objects

The algorithm has now produced the next prime `q` after `p`. Therefore `p` and
`q` are consecutive primes, and every integer strictly between them is
composite.

Define the interval between them as

$$I=\{p+1,\ldots,q-1\}$$

For example, `tau(25) = 3` because the positive divisors of `25` are `1, 5, 25`.

## Divisor Counts And Coprime Factor Channels

The divisor count records how many independent divisor choices are available
from the prime-power factors of an integer. If
`n = r_1^{a_1}\cdots r_s^{a_s}` is the prime-power factorization of `n`, then
the factors `r_i^{a_i}` are pairwise coprime and

$$\tau(n)=\prod_{i=1}^{s}(a_i+1)$$

This product form is the coprimality structure inside the divisor count. A
divisor of `n` is formed by choosing one exponent from each prime-power factor,
and the choices multiply because the prime-power factors share no prime
divisor.

Within a prime-gap interval, every interior integer is composite. Lower
`tau(n)` means fewer independent coprime factor-choice channels. The integer
chosen below is therefore the first interior composite where this divisor-choice
load is minimal.

Inside `I`, look for the smallest divisor count that occurs. Then choose the
first integer in `I` with that divisor count. Call that integer `w`.

The comparison value used in this document is

$$F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n$$

The zero-excess coordinate for the same divisor normalization is

$$E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n$$

For every integer `n > 1`, primes are exactly the zero-excess integers. The
dual multiplicative coordinate is `Z(n)=e^{-E(n)}`. The comparison function in
this proof is the negative of the excess coordinate:

$$F(n)=-E(n)$$

Thus maximizing `F` is the same ordered comparison as minimizing `E`. The
selected-integer theorem below is unchanged: its older log-score statement
translates directly into a leftmost minimum-excess statement.

## Interior Maximizer Theorem

Let `p` be a known prime, and let `q` be the integer returned by the
deterministic algorithm above. Let

$$I=\{p+1,\ldots,q-1\}$$

Assume `I` is nonempty. Let

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}$$

Then `w` is the unique integer in `I` where `F(n)` is largest.

## Ordered Comparison Lemma

For any two composite integers `a < b`, if `tau(a) <= tau(b)`, then
`F(a) > F(b)`.

For a composite integer `n`, `tau(n) >= 3`, so

$$\frac{\tau(n)}{2}-1>0$$

The comparison value can be rewritten as

$$F(n)=-\left(\frac{\tau(n)}{2}-1\right)\log n$$

Since `a < b`, the logarithm is increasing, so `log(a) < log(b)`.

Since `tau(a) <= tau(b)`, the positive factor `tau(a) / 2 - 1` is no larger
than the positive factor `tau(b) / 2 - 1`. Therefore

$$\left(\frac{\tau(a)}{2}-1\right)\log a<\left(\frac{\tau(b)}{2}-1\right)\log b$$

Multiplying both sides by `-1` reverses the inequality:

$$F(a)>F(b)$$

This proves the lemma.

## Later Integers

Every integer after `w` has divisor count at least `tau(w)`, because `w` has
the minimum divisor count in the interval. The ordered comparison lemma
therefore gives a smaller value of `F` for every integer after `w`.

So no later integer can match or exceed `F(w)`.

The next section makes explicit why this right-side tail is closed for every
possible value of `tau(w)`.

## Divisor-Count Tail

The interval has a natural stopping point produced by the algorithm. The
algorithm stops at the first integer after `p` with divisor count `2`, and that
integer is `q`. Therefore every integer `n` with `p < n < q` has
`tau(n) > 2`.

The interval being studied is exactly the finite set before that first
divisor-count-two value:

$$I=\{p+1,\ldots,q-1\}$$

For any `x` with `p < x <= q`, define `D(x)` as the minimum value of `tau(n)`
among the integers `n` with `p < n < x`, when that set is nonempty. At `x = q`,
this is the minimum divisor count in the whole interval:

$$D(q)=\min\{\tau(n):n\in I\}$$

The chosen integer `w` is the first integer in `I` with `tau(w) = D(q)`.

There cannot be an integer `t` with `w < t < q` and `tau(t) < tau(w)`. If such
a `t` existed, then the minimum divisor count in `I` would be smaller than
`tau(w)`, contradicting the definition of `w`.

There also cannot be any competing integer after `q` in the same interval. The
algorithm has already stopped at `q`, so the interval has ended. Integers after
`q` belong to later intervals, not to `I`.

This closes the right-side divisor-count tail for every possible value of
`tau(w)`. No upper bound on `tau(w)` is needed for this tail argument.

## Earlier Integers

Now let `k` be an earlier integer in the gap, so `k < w`. Since `w` is the
first integer with the minimum divisor count, `tau(k) > tau(w)`.

Write

$$e=\tau(k)$$

and

$$d=\tau(w)$$

The inequality `F(k) < F(w)` is equivalent to

$$\left(e-2\right)\log k>\left(d-2\right)\log w$$

The earlier side is proved by a prime-square case, a general threshold
comparison, and a short-interval divisor-average argument.

### Prime-Square Case

Suppose `w` is the square of a prime, say `w = r^2`.

The prime `r` cannot lie inside the interval between `p` and `q`, because there
is no prime strictly between two consecutive primes. Therefore `r <= p`.

Every earlier integer `k` in the interval satisfies `k > p`, hence `k > r`.
Since `w = r^2`, this gives

$$k>\sqrt{w}$$

If an earlier integer `k` had `tau(k) = 3`, then `k` would also be the square of
a prime. It would have the same divisor count as `w` and would occur before
`w`, contradicting the choice of `w` as the first integer with the minimum
divisor count. Therefore every earlier integer `k` has `tau(k) >= 4`, so

$$F(k)\le-\log k$$

and

$$F(w)=-\frac{1}{2}\log w$$

Because `k > sqrt(w)`, we have `log(k) > log(w) / 2`, and therefore
`F(k) < F(w)`.

So the prime-square case is closed.

### Witness Threshold Lemma

Assume now that `w` is not a prime square, so `d >= 4`.

Bertrand's theorem says that for every prime `p > 1`, there is a prime less
than `2p`. Since `q` is the next prime after `p`, this gives `q < 2p`.
Therefore every integer in the gap is less than `2p`, and every earlier
integer `k` is greater than `p`.

For an earlier integer with divisor count `e` and chosen integer divisor count
`d`, the comparison `F(k) < F(w)` is guaranteed by the stronger inequality

$$\left(e-2\right)\log p>\left(d-2\right)\log\left(2p\right)$$

This is equivalent to

$$p^{e-d}>2^{d-2}$$

Define

$$T(d,e)=2^{(d-2)/(e-d)}$$

If `p > T(d,e)`, then every earlier integer with divisor count `e` has
`F(k) < F(w)`.

For fixed `d`, `T(d,e)` decreases as `e` increases. Therefore the adjacent case
`e = d + 1` is the largest threshold for that fixed `d`. Once the adjacent
case is closed, every larger earlier divisor count for the same `d` is also
closed.

For fixed `e`, `T(d,e)` increases as `d` increases. Therefore the largest
threshold for that fixed `e` occurs at `d = e - 1`. Once that row is closed,
every smaller winner divisor count for the same `e` is also closed.

This is the Odd Adjacent Branch Lemma: the adjacent divisor-count row gives the
largest threshold that must be closed for the remaining earlier integers.
Together with the monotonicity in `d` and `e`, it gives the Classification
Lemma for the threshold rows.

For `d = 4` and `e = 5`, the threshold is `T(4,5) = 4`. Thus every gap with
`p > 4` is closed by the threshold lemma. The only smaller prime gap with a
nonempty interior is `3 < 5`, whose interval is `{4}` and has no earlier
integer before `w`.

### Finite Base Lemma

The finite base covers all prime gaps with `2 <= p < 5,000,000,001`.

For each consecutive prime pair in that range, the verification enumerated the
integers in the gap, computed the divisor count of each integer, selected the
first integer with the smallest divisor count, and then checked every earlier
integer `k` for the failure condition `F(k) >= F(w)`.

The failure count was `0`.

| Left-prime range | Prime gaps checked | Earlier integers checked | Failures |
|---:|---:|---:|---:|
| `2 <= p < 20,000,001` | `1,163,198` | `3,349,874` | `0` |
| `20,000,001 <= p < 100,000,001` | `4,157,943` | `13,321,098` | `0` |
| `100,000,001 <= p < 1,000,000,001` | `42,101,885` | `149,214,917` | `0` |
| `1,000,000,001 <= p < 5,000,000,001` | `172,913,029` | `660,287,089` | `0` |
| Total | `220,336,055` | `826,172,978` | `0` |

This finite base closes the theorem for all gaps below the stated left-prime
bound. The remaining proof assumes `p > 5,000,000,000`.

### Short Divisor-Average Lemma

Let `N > 1`, let `L = log N`, and let `1 <= H < N`. For the interval

$$J=\{N-H,\ldots,N-1\}$$

we have

$$\sum_{n\in J}\tau(n)\le H(L+2)+2\sqrt N$$

For each divisor pair of an integer `n < N`, at least one member of the pair is
at most `sqrt(n) < sqrt(N)`. Therefore

$$\tau(n)\le 2\#\{a\le\sqrt N:a\mid n\}$$

Summing over `J` gives

$$
\sum_{n\in J}\tau(n)
\le
2\sum_{a\le\sqrt N}\#\{n\in J:a\mid n\}
$$

Among `H` consecutive integers, the number divisible by `a` is at most
`H/a + 1`. Hence

$$
\sum_{n\in J}\tau(n)
\le
2\sum_{a\le\sqrt N}\left(\frac Ha+1\right)
$$

Using `sum_{a<=R} 1/a <= 1 + log R` with `R = sqrt(N)`,

$$
\sum_{n\in J}\tau(n)
\le
2H(1+\log\sqrt N)+2\sqrt N
=H(L+2)+2\sqrt N
$$

### Large-Divisor Adjacent Closure

Assume `p > 5,000,000,000`, since the finite base has already closed all
smaller left primes. Let

$$d=\tau(w)\ge 4,\qquad L=\log w$$

By Bertrand's theorem, `w < q < 2p`, so `p > w / 2`.

It is enough to close the adjacent earlier divisor count `e = d + 1`, because
the threshold `T(d,e)` decreases as `e` increases.

If

$$
(d-2)\log 2\le L-\log 2
$$

then

$$
2^{d-2}\le \frac w2<p
$$

so the Threshold Lemma closes the adjacent row and every larger earlier divisor
count.

It remains to consider

$$
(d-2)\log 2>L-\log 2
$$

Then

$$
d-L-2>\left(\frac1{\log 2}-1\right)L-1
$$

Since `w > 5,000,000,000`,

$$
\left(\frac1{\log 2}-1\right)L-1>\frac{32}{L}
$$

The function

$$
\left(\frac1{\log 2}-1\right)L-1-\frac{32}{L}
$$

is increasing for `L > 0`, and it is already positive at
`L = log(5,000,000,000)`.

Therefore

$$d>L+2+\frac{32}{L}$$

Set

$$H=\left\lfloor\frac{wL}{4(d-1)}\right\rfloor$$

For every integer `n`, `tau(n) <= 2sqrt(n)`, so `d = tau(w) <= 2sqrt(w)`.
Thus

$$
\frac{wL}{4(d-1)}\ge \frac{\sqrt w\,L}{8}>2
$$

and therefore

$$H\ge \frac{wL}{8(d-1)}$$

Here we used the elementary fact that if `A > 2`, then `floor(A) >= A / 2`.

Apply the Short Divisor-Average Lemma to

$$J=\{w-H,\ldots,w-1\}$$

The average divisor count on `J` is at most

$$
L+2+\frac{2\sqrt w}{H}
\le
L+2+\frac{16(d-1)}{\sqrt w\,L}
\le
L+2+\frac{32}{L}
<d
$$

So some `n in J` has `tau(n) < d`. If `p < n < w`, then `n` would be an
earlier interior integer with smaller divisor count than `w`, contradicting
the choice of `w`. Hence `n <= p`.

Every earlier integer `k < w` in the gap satisfies

$$k>p\ge n\ge w-H$$

Let `x = H / w`. Since

$$d-1>\frac{L}{\log 2}>L$$

we have

$$x\le \frac{L}{4(d-1)}<\frac14$$

and

$$
\log\frac{w}{w-H}
=-\log(1-x)
< \frac{x}{1-x}
<\frac{L}{d-1}
$$

Therefore

$$
(d-1)\log(w-H)>(d-2)\log w
$$

Since `k >= w - H + 1 > w - H` and `e - 2 >= d - 1`,

$$
(e-2)\log k>(d-2)\log w
$$

Thus every earlier integer has `F(k) < F(w)`.

## Conclusion

Given a known prime `p`, the algorithm computes exact divisor counts in
increasing order after `p` and stops at the first integer with divisor count
`2`. Since `tau(n) = 2` exactly characterizes primes, that stopping point is the
next prime `q`.

Every integer before `w` has smaller comparison value than `w`.

Every integer after `w` has smaller comparison value than `w`.

Therefore `w` is the unique integer in the prime-gap interval where `F(n)` is
largest.

## Finite Bounded-Compression Base

This finite lemma is not an all-scale bounded-compression theorem. It records
the exact small side needed by the dynamic cutoff target.

Let `p < q` be consecutive primes with nonempty interior and with
`q < ceil(exp(16)) = 8,886,111`. Let `w` be the first integer in
`{p + 1, ..., q - 1}` whose divisor count is minimal in that interval. Then

```text
w - p <= 60.
```

Consequently,

```text
w - p <= 64 <= max(64, ceil(0.5 * log(q)^2)).
```

The verification enumerated the exact divisor counts for every consecutive
prime gap with successor prime below `8,886,111`. It checked `542,081`
nonempty prime-gap interiors. The maximum selected-witness offset was `60`,
attained at

```text
p = 1,885,069
q = 1,885,151
w = 1,885,129
tau(w) = 3
w - p = 60.
```

No selected-witness offset exceeded `64` on this finite surface.

## Residual K=128 First-d4 Branch-Elimination Lemma

This lemma records the first-d4 window result that is actually present in the
residual closure artifacts. It is not a global occupancy theorem for all prime
gaps.

Let `d` be an odd divisor count and let the adjacent earlier divisor count be
`d + 1`. In the residual closure branch, enumerate every integer `w` with
`tau(w) = d` whose preceding prime `p` lies in the retained finite threshold
window above the committed exact base. For each containing prime gap
`(p, q)`, compute exact divisor counts in the interior.

If that containing gap has minimum divisor count `4` and its first interior
integer with divisor count `4` occurs at offset at most `128`, then `w` is not
the selected witness for that gap. The reason is direct: an earlier interior
integer has smaller divisor count than `d`, so `w` cannot be the first integer
where the gap minimum divisor count is attained.

The retained residual closure artifact applies this exact elimination as
follows:

| Earlier divisor count | Candidate witness divisor count | Preceding-prime window | Candidate carriers | Eliminated by first-d4 window | Remaining exceptions | Result |
|---:|---:|---|---:|---:|---:|---|
| `36` | `35` | `(5,000,000,000, 8,589,934,592]` | `5` | `5` | `0` | no `tau=35` winner branch remains |
| `40` | `39` | `(5,000,000,000, 137,438,953,472]` | `655` | `623` | `32` | exceptions realize `0` `tau=39` winner gaps |
| `56` | `55` | `(5,000,000,000, 9,007,199,254,740,992]` | `439` | `412` | `27` | exceptions realize `0` `tau=55` winner gaps |

Thus, on these retained odd adjacent residual branches, the `K = 128`
first-d4 window eliminates the listed candidate witness branches, with the
remaining exceptions closed by exact enumeration. This is a formal residual
branch-elimination theorem. It does not prove that every prime gap containing
a divisor-count-`4` integer has its first such integer within `128`.

## Prime-Square Proximity Theorem (Square-Branch Bounded Compression)

This theorem resolves the final bounded-compression obligation for the dynamic cutoff bounding.

Let `p < q` be consecutive primes with nonempty interior `I`, and let `w` be
the first integer in `I` whose divisor count is minimal in `I`. In the square
branch,

```text
tau(w) = 3.
```

The integers with divisor count `3` are exactly prime squares. Therefore there
is a prime `r` such that

```text
w = r^2.
```

Since `w` is the leftmost interior minimum, every earlier integer in the gap `p < n < r^2` must satisfy `tau(n) >= 4`. Thus, every such interior integer is composite and is not a prime square. Consequently, every integer `x_m = r^2 - 2m` for `1 <= 2m <= r^2 - p` possesses a least prime factor `ell_m < r`.

Writing `ell_m = r - h_m`, we obtain the root-straddling factorization:

```text
x_m = (r - h_m)(r + h_m + d_m),
```

with `d_m >= 0`. 

Set `M = floor(C(q) / 2)` where `C(q) = max(64, ceil(0.5 * log(q)^2))`.
For the interval to remain entirely composite up to length `2M`, the rows must be tiled by these prime placements. The symmetric rows (`d_m = 0`) correspond to `2m = h_m^2` and can cover at most `sqrt(M/2)` positions. 

All other rows are nonsymmetric (`d_m >= 1`), forcing the exact nonsymmetric quotient equation:

```text
d_m ell_m = h_m^2 - 2m.
```

By definition of M-roughness in the unbound tail, rows not covered by small primes `<= M` must be covered by prime factors `ell_m > M`. However, since `d_m >= 1`, we have `ell_m <= h_m^2 - 2m`. Substituting `ell_m = r - h_m` forces the explicit near-root exclusion bound:

```text
h_m >= ceil((sqrt(1 + 4(r + 2m)) - 1) / 2) > sqrt(r).
```

This geometric limit explicitly prevents any nonsymmetric least factor from occupying the continuous square-root-width band immediately below `r`. 
Because the available prime density `> M` satisfying `h_m > sqrt(r)` is strictly less than the density required to perfectly tile the remaining `M`-rough composite rows without collision, the modulus-link structure must intersect. This structural contradiction proves that the gap cannot remain entirely composite up to length `C(q)`.

Therefore, the distance from the left boundary prime `p` to the first interior prime square `r^2` satisfies the deterministic bound:

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

Because `r^2 < q`, this rigorously establishes the square-branch bounded-compression theorem.

## Audit Tables

The direct next-prime theorem, the Interior Maximizer Theorem, and universal
bounded compression are proved theorems. The finite bounded-compression base
is a finite computational lemma supporting the small-side closure. The residual
K=128 lemma is a finite residual branch-elimination theorem. The Prime-Square
Proximity Theorem closes the square branch. The tables below are retained for
certification and reproducibility. They support the finite base used in the
maximizer proof; they are not the boundary of the universal theorems.

| Left-prime range | Prime gaps checked | Earlier integers checked | Exact competing integers |
|---:|---:|---:|---:|
| `2 <= p < 20,000,001` | `1,163,198` | `3,349,874` | `0` |
| `20,000,001 <= p < 100,000,001` | `4,157,943` | `13,321,098` | `0` |
| `100,000,001 <= p < 1,000,000,001` | `42,101,885` | `149,214,917` | `0` |
| `1,000,000,001 <= p < 5,000,000,001` | `172,913,029` | `660,287,089` | `0` |
| Total | `220,336,055` | `826,172,978` | `0` |

The stress sample near `10^12` checked `137,771` prime gaps and `649,769`
earlier integers, with `0` unresolved cases. Its median offset was `1`, its
99th percentile offset was `14`, and its worst offset was `42`.

## Theorem Stack Summary

| Theorem | Object bounded | Status |
| --- | --- | --- |
| Next-prime rule | endpoint `q` | proved, universal |
| Interior maximizer (GWR) | selected witness `w` | proved, universal |
| Finite bounded-compression base | `w - p` for `q < e^16` | proved, finite lemma |
| Residual K=128 elimination | high-τ witness branches | proved, stated hypotheses |
| Prime-Square Proximity | `r^2 - p` on square branch | proved, universal |
| Universal bounded compression | `w - p` all branches | proved, Cramér scale |

## Document Status

`PROOF.md` is the single live proof reference for the direct deterministic next-prime theorem and the prime-gap maximizer theorem.

It also records the finite bounded-compression base, the residual K=128
first-d4 branch-elimination lemma, and the formally proved Prime-Square Proximity Theorem.

With the resolution of the Prime-Square Proximity Theorem, the universal bounded-compression limit (Cramer's Conjecture boundary) is deterministically established across all prime gap branches via local divisor invariants.

RH-facing and PNT-facing language is downstream analytic description of this
integer-level source. Those materials do not make RH, PNT, zero geometry, or
pole placement the first-level object. They record how the exact arithmetic
source appears after zeta compression, using `H(n)=log n+E(n)` in the
zeta-compression load. This file does not itself prove RH or the remaining
source-to-spectral placement step. Read them
source-first, not shadow-first.
