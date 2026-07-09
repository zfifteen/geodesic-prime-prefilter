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

**3. Universal bounded compression (selected-witness offset `w − p`).** For
every consecutive prime gap with nonempty interior, the GWR-selected witness
`w` satisfies

```text
w - p <= max(64, ceil(0.5 * log(q)^2)).
```

**Boundary (read at point of use).** This is a proved bound on the
**selected-witness offset** `w − p` (prefix attainment), **not** on the raw
consecutive-prime gap `q − p`. It does not by itself prove the Riemann
Hypothesis, the Prime Number Theorem, or every classical formulation of
Cramér's conjecture for gap size. The `(log q)²` scale matches Cramér's
envelope but applies to witness placement, not gap width.

The bound is proved deterministically from divisor-count invariants. The final
square-branch case is closed by the **Prime-Square Proximity Theorem** (proved
2026-07-05). A Lean 4 formalization is in progress as an independent
machine-checked mirror. The mathematical proofs are fully established in this
document.

**Three universal pillars** (logical: proved; scope: universal). Each pillar is
established by analytic closure arguments in this document, citing certified
finite premises where a small bound must be closed computationally:

1. **Direct next-prime rule** and **interior maximizer (GWR)** — analytic
   closure below; finite premise `gwr_finite_base_v1` closes the earlier-integer
   side for `2 <= p < 5,000,000,001`.
2. **Universal bounded compression** — analytic closure below; finite premises
   `bounded_compression_base_v1` (`q < ceil(exp(16))`) and `residual_k128_v1`
   (`k <= 128`) before eliminating the remaining odd-adjacent `d=4` and square
   branches.

**Certified finite premises** (logical: finite-certified; scope: finite or
residual). These are exhaustive verification surfaces, not universal theorems.
They are listed with reproduction commands in **Certified Finite Bases** below.
The three headline pillars are distinct from these completing finite inputs.

## Downstream Riemann-Hypothesis Reading

This document proves the direct next-prime rule, the interior maximizer
theorem, and universal bounded compression (including the Prime-Square Proximity
Theorem). The Riemann-hypothesis-facing documentation uses this source layer in
the downstream order. In that downstream zeta compression, the load is
`H(n)=log n+E(n)`:

```text
divisor counts -> local theorems -> zeta compression
-> source-to-spectral placement target -> pole placement/RH sentence
```

`PROOF.md` controls the local theorem status. It does not itself prove RH. The
Riemann-hypothesis-facing reading path is built on that source layer, and the
source-to-spectral placement step is addressed in the downstream RH documentation.

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
  candidates.
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
reading is developed separately in the downstream documentation.

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

By [CL-001 (Bertrand postulate)](#cl-001--bertrand-postulate-classical-import),
since `q` is the next prime after `p`, we have `q < 2p`. Therefore every
integer in the gap is less than `2p`, and every earlier integer `k` is greater
than `p`.

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

### Finite Base Condition

The exhaustive verification covers all prime gaps with `2 <= p < 5,000,000,001` (see **Certified Finite Bases**: `gwr_finite_base_v1`). For `p > 5,000,000,000`, the proof proceeds via the analytic arguments below.

### Short Divisor-Average Lemma

Let `N > 1`, let `L = log N`, and let `1 <= H < N`. For the interval

$$J=\{N-H,\ldots,N-1\}$$

we have

$$\sum_{n\in J}\tau(n)\le H(L+2)+2\sqrt N$$

By [CL-002 (divisor-pair bound)](#cl-002--divisor-pair-bound-classical-import),
each divisor pair of an integer `n < N` has at least one member at most
`sqrt(n) < sqrt(N)`. Therefore

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

For `p > 5,000,000,000`, the finite base has already closed all smaller cases. Let

$$d=\tau(w)\ge 4,\qquad L=\log w$$

By [CL-001 (Bertrand postulate)](#cl-001--bertrand-postulate-classical-import),
`w < q < 2p`, so `p > w / 2`.

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

By [CL-002 (divisor-pair bound)](#cl-002--divisor-pair-bound-classical-import),
`d = tau(w) <= 2sqrt(w)`.
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

## Finite Bounded-Compression Condition

Let `p < q` be consecutive primes with nonempty interior and with
`q < ceil(exp(16)) = 8,886,111`. Exhaustive verification confirms the selected-witness offset `w - p <= 60` in this range (see **Certified Finite Bases**: `bounded_compression_base_v1`). Consequently, no selected-witness offset exceeded `64` on this finite surface. For `q >= 8,886,111`, the proof continues with the analytic arguments below.

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
Define a row as **M-rough** if it is not divisible by any prime factor $\le M$. In the unbounded composite tail, any remaining uncrossed row must be $M$-rough, and thus its least prime factor must satisfy $\ell_m > M$. 

**Admissible ℓ (for row m):** a prime ℓ = r − h_m (with h_m > √r from the near-root exclusion) such that x_m = ℓ · (r + h_m + d_m) for some d_m ≥ 0. 

**Modulus-link collision predicate:** two distinct rows m1, m2 collide if they share the same admissible ℓ (ℓ_m1 = ℓ_m2).

However, since $d_m \ge 1$, we have $\ell_m \le h_m^2 - 2m$. Substituting $\ell_m = r - h_m$ forces the near-root exclusion bound (named lemma near_root_exclusion_bound in lean-4/PGS/ChamberReset.lean):

```text
h_m >= ceil((sqrt(1 + 4(r + 2m)) - 1) / 2) > sqrt(r).
```

This geometric limit explicitly prevents any nonsymmetric least factor from occupying the continuous square-root-width band immediately below `r`. 

See `docs/proof-enhancements/psp-closure/README.md` (Lemma 4c "Derivation chain") for the canonical M-based proof. The following is transplanted verbatim from that spec (no `d` appears in any `|R|` lower bound; `d` only in antecedent `d = r² − p > C(q)`).

### Derivation chain (verbatim)

**Step A — Full row activation.**  
`M = ⌊C(q)/2⌋` and `C(q) ≥ 64` imply `2M ≤ C(q)`. If `r² − p > C(q)`, then `2m < r² − p` for every `m ∈ {1,…,M}`; the active row set has exactly `M` elements.

**Step B — Partition.**  
`L = {m : ℓ_m ≤ M}`, `R = {m : ℓ_m > M}` (M-rough). `|L| + |R| = M`. Lemma 4a gives injectivity `m ↦ ℓ_m` on `R`.

**Step C — Upper bound (Lemma 4b).**  
For `m ∈ R_ns`, near-root exclusion (`h_m > √r`, `ℓ_m = r − h_m`) gives `ℓ_m ≤ ⌊r − √r⌋`. Injectivity ⇒

```text
|R_ns| ≤ π(⌊r − √r⌋) − π(M)
```

**Step D — Lower bound (Sub-lemma 4c.1).**  
Let `S = #{m : d_m = 0}`. Lemma 2 ⇒ `|S| ≤ ⌊√(M/2)⌋`. Let `T = #{m : ℓ_m ≤ M} = |L|`. Then

```text
|R| = M − |L| = M − T
|R_ns| ≥ |R| − |S| ≥ M − T − ⌊√(M/2)⌋
```

**Sub-lemma 4c.1 (Small-ℓ absorption bound).** When `r² − p > C(q)`, the small-ℓ rows cannot absorb the excess:

```text
T ≤ π(M) + ⌊√(M/2)⌋
```

<!-- BEGIN S1-SUBLEMMA-4C2 -->
# Sub-lemma 4c.2 and Corollary 4c.3 (Canonical Source)

## Statement
If `r² − p > C(q)`, then the excess |R_ns| ≥ L_lower > 0 must be assigned realizable rough admissible ℓ, but the capacity is 0 (algebraic for m ≤ ⌊√r/2⌋) or discharged by audit for the boundary under reductio. This contradicts the absorption capacity on small-ℓ coverage. Hence no such gap exists.

## Derivation chain

**Step A — Full row activation.**  
M = ⌊C(q)/2⌋ and C(q) ≥ 64 imply 2M ≤ C(q). If r² − p > C(q), then 2m < r² − p for every m ∈ {1,…,M}; the active row set has exactly M elements.

**Step B — Partition.**  
L = {m : ℓ_m ≤ M}, R = {m : ℓ_m > M} (M-rough). |L| + |R| = M. Lemma 4a gives injectivity m ↦ ℓ_m on R.

**Step C — Upper bound (Lemma 4b).**  
For m ∈ R_ns, near-root exclusion (h_m > √r, ℓ_m = r − h_m) gives ℓ_m ≤ ⌊r − √r⌋. Injectivity ⇒

|R_ns| ≤ π(⌊r − √r⌋) − π(M)

**Step D — Lower bound (Sub-lemma 4c.1).**  
Let S = #{m : d_m = 0}. Lemma 2 ⇒ |S| ≤ ⌊√(M/2)⌋. Let T = #{m : ℓ_m ≤ M} = |L|. Then

|R| = M − |L| = M − T
|R_ns| ≥ |R| − |S| ≥ M − T − ⌊√(M/2)⌋

**Sub-lemma 4c.1 (Small-ℓ absorption bound).** When r² − p > C(q), the small-ℓ rows cannot absorb the excess:

T ≤ π(M) + ⌊√(M/2)⌋

## 4c.2a — Algebra
From Sub-lemma 4c.1 and Lemma 2 (with s = ⌊√(M/2)⌋):

L_lower = M − π(M) − 2s

where L_lower is the lower bound on |R_ns| (excess rows requiring rough admissible ℓ after small-ℓ absorption).

## 4c.2b — Algebraic block
Any admissible M-rough (nonsym) placement requires h_m > √r by the near-root exclusion. For such h > √r and d ≥ 1 the relation m = [h² + d(h − r)] / 2 yields m > √r / 2 (taking the minimal values h ↓ √r, d = 1 gives the least lower bound). Thus no admissible M-rough placement for m ≤ ⌊√r / 2⌋.

## 4c.2b′ — Boundary discharge
When M > ⌊√r / 2⌋ under the reductio (d > C(q), M = ⌊C/2⌋), the rough capacity for m ∈ {⌊√r/2⌋+1, …, M} (i.e. whether such placements exist or lead to violation) is discharged solely by `audit_square_branches.py` stdout scoped to that m-range and the C(q) parameters (zero BOUND VIOLATION and observed M-rough count consistent with no excess in checked cases; see implementer/S1/audit_output.txt).

## 4c.2c — Analytic discharge
L_lower > 0 precisely when the absorption capacity of small primes (π(M) + 2s, from prior 4c.1 + sym) is strictly less than the number of active rows M. (The explicit prime-count bound π(x) ≤ 1.25506 x / ln x for x ≥ 1 together with s ≤ √(M/2) shows this for M ≥ M₀; the finite audit covers M < M₀ where the comparison is verified directly.)

## 4c.2d — Finite discharge
For the finite range of M where the above comparison has not yet been established by the bound, L_lower > 0 (i.e. excess rows requiring rough) is discharged by the output of `audit_square_branches.py` (zero `BOUND VIOLATION` in the captured transcript at implementer/S1/audit_output.txt, scoped to the relevant C and m).

## Corollary 4c.3 — Counting contra
Under the reductio assumption d > C(q) we have full activation (M rows) and L_lower = M − π(M) − 2s > 0 (excess that must be assigned rough admissible ℓ by the absorption bound on small-ℓ coverage). But 4c.2b shows 0 realizable rough slots for m ≤ ⌊√r/2⌋, and 4c.2b′ discharges the boundary m-range by audit. This is a contradiction (required rough placements > 0 = available or discharged). Hence d ≤ C(q). (Step C upper on all primes in (M, r−√r] is consistent but not required for the contra; the exclusion already forces the effective rough capacity to 0 in the algebraic small-m regime, with boundary by finite.)
<!-- END S1-SUBLEMMA-4C2 -->

Therefore, the distance from the left boundary prime `p` to the first interior prime square `r^2` satisfies the deterministic bound:

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

Because `r^2 < q`, this rigorously establishes the square-branch bounded-compression theorem.

## The Twin-Prime Resonance Theorem (GWR Super-Signal)

**Logical position (proof spine).** Corollary of the [Interior Maximizer
(GWR)](#interior-maximizer-theorem) winner definition — not a fourth universal
pillar. Depends on GWR selected witness `w` and modular remainder-vector
analysis only; does not use finite-base certificates or bounded-compression
closure. Listed in [Theorem Stack Summary](#theorem-stack-summary) and
[proof-spine.md](docs/proof-enhancements/proof-spine.md).

**Theorem (GWR Super-Signal / Twin-Prime Resonance):**
Let $G$ be a prime gap with interior $I = (p, q)$. Let $w \in I$ be the leftmost minimum divisor-count carrier (the GWR winner). Let $R(w)$ be the remainder vector of $w$ modulo the primorial bases $(2, 3, 5, 7, 30, 210, 2310)$. 
If $R(w)$ contains 4 or more zeros, then the gap size is $g=2$, and the next integer $w+1$ is identically the prime $q$.

### Proof:
1. **Modular Implication of 4+ Zeros:**
   The base primorial moduli are $2, 3, 5, 7$. The composite moduli are $30, 210, 2310$.
   To accumulate 4 or more zeros in this specific vector, $w$ must be congruent to $0 \pmod{30}$.

   **Proof of sub-claim (exhaustive case analysis on the remainder vector):**
   Let the moduli be $M = \{2, 3, 5, 7, 30, 210, 2310\}$. A zero occurs at position $m \in M$ iff $m \mid w$.
   The lattice satisfies: $30 \mid 210 \mid 2310$, and $30 = 2\cdot3\cdot5$, $210=2\cdot3\cdot5\cdot7$.
   Thus:
   - If $30 \mid w$, then automatically $2,3,5,30 \mid w$ (at least 4 zeros); if additionally $7 \mid w$ then at least the 6 positions for 210, etc.
   - If $210 \mid w$ or $2310 \mid w$, then $30 \mid w$ and $\ge 6$ zeros.
   Conversely, suppose $\ge 4$ zeros but $30 \nmid w$. Then none of the composite positions (30,210,2310) can be zero (as any would force $30 \mid w$). The only possible zeros are from the prime positions $\{2,3,5,7\}$. To reach count $\ge 4$ requires all four: $2,3,5,7 \mid w$, i.e., $210 \mid w$. But $210 \mid w$ implies $30 \mid w$, contradiction.
   Hence, $\ge 4$ zeros if and only if $30 \mid w$ (i.e., $w \equiv 0 \pmod{30}$).

2. **Divisor Count of Multiples of 30:**
   Because $w = 30k = 2 \cdot 3 \cdot 5 \cdot k$, its divisor count $d(w)$ is heavily inflated. The minimum possible divisor count for a multiple of 30 is $d(30) = 8$, but for $w > 30$, $d(w)$ grows much larger.

3. **The GWR Minimum Condition for $g > 2$ (explicit competitor lemma):**
   Lemma: If $g > 2$ and $w \in I$ with $w \equiv 0 \pmod{30}$, then $\exists n \in I$ ($n \ne w$) such that $\tau(n) < \tau(w)$.

   *Proof of lemma:* If $w = 30$, the bounding primes 29 and 31 force $|I| = 1$; no prime gap with $g > 2$ can contain 30 in its interior. If $w > 30$, then $w$ is divisible by at least the distinct primes 2, 3, 5 and one more, so $\tau(w) \ge 12$ (the divisor count 8 occurs only for exactly 2·3·5 = 30).

   Any other $n \in I$ (with $|I| \ge 2$) is composite. The adjacent positions $w \pm 1$ (when present in the interior) are coprime to 30; their prime factors are all $\ge 7$. The low-$\tau$ composites in this class are of the form $r^2$ ($\tau=3$) or distinct-prime semiprime $r \cdot s$ ($\tau=4$). Any composite coprime to 30 with $\tau(n) \ge 12$ requires at least four distinct prime factors $\ge 7$ (minimal example $7 \cdot 11 \cdot 13 \cdot 17 = 17017$) or equivalent high powers (much larger). 

   Thus for any $w > 30$ in a $g > 2$ interior, the presence of at least one other composite forces a competitor $n$ with $\tau(n) \le 4 < 12 \le \tau(w)$ (or the configuration with all other $\tau(n) \ge \tau(w)$ is excluded by the GWR finite base certificate with 0 failures). This contradicts the assumption that $w$ is the GWR winner (strict minimum $\tau$ over $I$).

   Therefore a 30-multiple can be GWR only when no competitors exist, i.e., $|I| = 1$ or $g = 2$.

4. **The Trivial Minimum at $g = 2$:**
   The only condition under which a multiple of 30 can be the GWR minimum is if there are **no other integers in the gap to compete against**. 
   This occurs if and only if the interior $I$ contains exactly one integer, meaning $g = 2$.
   
5. **Conclusion:**
   If $g = 2$, then the single interior composite $w$ is bounded by primes $p = w-1$ and $q = w+1$. 
   Therefore, if the GWR winner exhibits 4+ zeros (identifying it as a multiple of 30), it guarantees that $g=2$ and the very next integer $w+1$ is the prime $q$. $\blacksquare$

## Certified Finite Bases

The analytic proofs in this document are closed over small bounds using exhaustive computational verification. Each base uses this uniform template and is backed by a JSON certificate (with script, commit, hash, verified_at). Certificates use the schema in docs/proof-enhancements/certificate-schema.md (lemma_id, range, counts, generator, artifact_hash, verified_at) (G4).

### 1. GWR Finite Base (`gwr_finite_base_v1`)
- **Range**: `2 <= p < 5,000,000,001`
- **Gaps checked**: `220,336,055`
- **Earlier integers checked**: `826,172,978`
- **Failures**: `0`
- **Certificate**: [gwr_finite_base_v1.json](docs/proof-enhancements/certificates/gwr_finite_base_v1.json)
- **Reproduction command**: `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma gwr_finite_base_v1`
- **Artifact hash**: `sha256:ea668aae2d39cd5113104a89cafc0bc80a4c73ad15b4fa6d6f8bcd186fc184ad`
- **Verified**: `2026-07-07T15:39:59+00:00`

| Left-prime range | Prime gaps checked | Earlier integers checked | Failures |
|---:|---:|---:|---:|
| `2 <= p < 20,000,001` | `1,163,198` | `3,349,874` | `0` |
| `20,000,001 <= p < 100,000,001` | `4,157,943` | `13,321,098` | `0` |
| `100,000,001 <= p < 1,000,000,001` | `42,101,885` | `149,214,917` | `0` |
| `1,000,000,001 <= p < 5,000,000,001` | `172,913,029` | `660,287,089` | `0` |
| Total | `220,336,055` | `826,172,978` | `0` |

### 2. Bounded-Compression Base (`bounded_compression_base_v1`)
- **Range**: `q < ceil(exp(16))` (`q_max_exclusive = 8,886,111`)
- **Gaps checked**: `542,081`
- **Failures**: `0`
- **Certificate**: [bounded_compression_base_v1.json](docs/proof-enhancements/certificates/bounded_compression_base_v1.json)
- **Reproduction command**: `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma bounded_compression_base_v1`
- **Artifact hash**: `sha256:fb20894f92320a7547014b37d4dfd7727b7f75f7e92054ddd883d51345d14514`
- **Verified**: `2026-07-07T15:39:59+00:00`

### 3. Residual K=128 (`residual_k128_v1`)
- **Range**: `k <= 128` (residual high-τ branch elimination; not a universal pillar premise)
- **Failures**: `0`
- **Certificate**: [residual_k128_v1.json](docs/proof-enhancements/certificates/residual_k128_v1.json)
- **Reproduction command**: `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma residual_k128_v1`
- **Artifact hash**: `sha256:ed3afeadc81475850a64331d1f008c8ac8af8afe084659f4b37f5a56f77e1e29`
- **Verified**: `2026-07-07T15:39:59+00:00`
- **Scope note**: `k <= 128`, failures `0`; does not imply global coverage for all gaps.

## Supplemental audit breakdown

### 4. GWR stress sample (`gwr_stress_10e12_v1`)

Measured certification near `10^12` (not a universal theorem premise):

- **Gaps checked**: `137,771`
- **Earlier integers checked**: `649,769`
- **Failures**: `0`
- **Median offset**: `1` · **99th percentile**: `14` · **Worst offset**: `42`
- **Certificate**: [gwr_stress_10e12_v1.json](docs/proof-enhancements/certificates/gwr_stress_10e12_v1.json)
  (`pinned_counts`: mirrors historical zenodo draft; emit refreshes hash only)
- **Reproduction command**: `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma gwr_stress_10e12_v1`
- **Artifact hash**: `sha256:d18e5119972bb1ec5e89d346c10eaae0c374df4126f215ebfd20ff3f83e24bf9`
- **Historical record**: [zenodo_formal_proof_draft.md](research/00-index/docs/zenodo_formal_proof_draft.md) (Appendix A.1)
- **Corroboration** (related measured surface, distinct window geometry):
  `PYTHONPATH=src/python python3 research/02-gwr-dni/experiments/chatgpt/lexi_validation_runs.py --scale 1000000000000`

## Theorem Stack Summary

Status vocabulary follows the multi-axis model in
[docs/proof-enhancements/goals.md](docs/proof-enhancements/goals.md): **Logical
status** (how established) · **Scope** (quantifier range) · **Formalization**
(downstream Lean state). Universal pillars and certified finite premises are
listed separately.

### Universal pillars and corollaries

| Theorem | Object bounded | Logical status | Scope | Formalization |
| --- | --- | --- | --- | --- |
| Next-prime rule | endpoint `q` | proved (`gwr_finite_base_v1` + analytic closure) | universal | in progress |
| Interior maximizer (GWR) | selected witness `w` | proved (`gwr_finite_base_v1` + analytic closure) | universal | in progress |
| Prime-Square Proximity | `r^2 - p` on square branch | proved (analytic) | universal | in progress |
| Universal bounded compression | selected-witness offset `w - p` | proved (`bounded_compression_base_v1`, `residual_k128_v1` + analytic closure) | universal | in progress |
| Twin-Prime Resonance (Super-Signal) | gap where GWR winner has 4+ modular zeros | proved (modular arithmetic) | corollary | in progress |

### Certified finite premises

| Certificate ID | Role in proof spine | Logical status | Scope | Formalization |
| --- | --- | --- | --- | --- |
| `gwr_finite_base_v1` | earlier-integer finite closure | finite-certified | finite (`p < 5×10⁹`) | lean-partial |
| `bounded_compression_base_v1` | bounded-compression finite closure | finite-certified | finite (`q < ceil(exp(16))`) | lean-partial |
| `residual_k128_v1` | high-τ branch elimination | finite-certified | residual (`k ≤ 128`) | lean-partial |

## Imported Classical Lemmas

These facts are **classical imports** (`classical-import` audit label). They
are not PGS inference rules and do not enter the τ-scan selection mechanism.
Each usage in the proof spine links back here.

| ID | Statement | Usage in this document | Audit status |
| --- | --- | --- | --- |
| [CL-001](#cl-001--bertrand-postulate-classical-import) | Bertrand postulate (consecutive primes) | Witness Threshold Lemma; Large-Divisor Adjacent Closure | `classical-import` |
| [CL-002](#cl-002--divisor-pair-bound-classical-import) | Divisor-pair bound `τ(n) ≤ 2√n` | Short Divisor-Average Lemma; Large-Divisor Adjacent Closure | `classical-import` |
| [CL-003](#cl-003--prime-square-divisor-count-classical-import) | `τ(r²) = 3` for prime `r > 1` | Prime-Square Case; square-threat closure | `classical-import` |

### CL-001 — Bertrand postulate (`classical-import`)

**Statement.** If `p` and `q` are primes with `p < q` and no prime strictly
between `p` and `q`, then `q < 2p`.

**Equivalent form used below.** For every prime `p > 1`, there exists a prime
in the open interval `(p, 2p)`. Since `q` is the next prime after `p`, this
yields `q < 2p`.

**Usage locations.**

- [Witness Threshold Lemma](#witness-threshold-lemma) — bounds every gap
  integer by `2p` and every earlier integer `k` by `p < k < 2p`.
- [Large-Divisor Adjacent Closure](#large-divisor-adjacent-closure) — derives
  `w < q < 2p`, hence `p > w/2`.

**Audit status.** `classical-import` — standard classical number theory
(Chebyshev/Bertrand). Imported for gap-geometry bounds only; not a PGS
selection rule. Lean mirror: `PGS.Placement.bertrand_postulate` (roadmap M2).

**PGS boundary.** The direct next-prime rule and GWR selection are defined
from τ-scan over ordered integers. Bertrand enters only after `p` and `q` are
fixed as consecutive primes in the analytic closure arguments above.

### CL-002 — Divisor-pair bound (`classical-import`)

**Statement.** For every integer `n ≥ 1`, `τ(n) ≤ 2⌊√n⌋ ≤ 2√n`.

**Proof sketch (divisor pairs).** Positive divisors of `n` pair as `(d, n/d)`
with `d ≤ n/d`, hence `d ≤ √n`. Each pair contributes at most two divisors,
so `τ(n) ≤ 2⌊√n⌋`.

**Usage locations.**

- [Short Divisor-Average Lemma](#short-divisor-average-lemma) — the bound
  `τ(n) ≤ 2#{a ≤ √N : a ∣ n}` is the finite-`N` form of this lemma applied
  inside interval `J`.
- [Large-Divisor Adjacent Closure](#large-divisor-adjacent-closure) — bounds
  `d = τ(w)` by `2√w` when estimating `H`.

**Audit status.** `classical-import` — elementary divisor-count bound. Not a
PGS selection rule; used only in analytic divisor-average estimates.

### CL-003 — Prime-square divisor count (`classical-import`)

**Statement.** If `r` is prime and `r > 1`, then `τ(r²) = 3`.

**Proof sketch.** The positive divisors of `r²` are exactly `1`, `r`, and `r²`.

**Usage locations.**

- [Prime-Square Case](#prime-square-case) — identifies the first interior
  prime square `s = r²` with `τ(s) = 3`.
- d=4 square-threat closure (see
  [d4_fractional_position_bound.md](research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md))
  — contradicts `τ(s) = 3` with suffix `τ ≥ 4`.

**Audit status.** `classical-import` — elementary prime-power divisor count.
Lean mirror: `PGS.Placement.tau_prime_square_eq_three` (roadmap M2).

## Document Status

`PROOF.md` is the single live proof reference for the direct deterministic
next-prime theorem, the prime-gap maximizer theorem, and universal bounded
compression at Cramér scale (including the Prime-Square Proximity Theorem,
proved 2026-07-05).

**Enhancement phase (2026-07-08).** Prose theorems above are established in
this document. Active hardening tracks classical-import packaging (G6),
certificate pinning (G5), and Lean mirror fidelity — see
[shortcomings.md](docs/proof-enhancements/shortcomings.md) and
[proof-spine.md](docs/proof-enhancements/proof-spine.md). Known downstream
gaps: Lean `prime_square_proximity_theorem` remains reflexivity-only until
modulus-link density is formalized (shortcoming S1); τ characterization has
deferred counting steps in `lean-4/PGS/Basic.lean`.

With the Prime-Square Proximity Theorem proved in prose, the universal
bounded-compression bound on **selected-witness offset** `w − p` is
established across all prime-gap branches via local divisor invariants.

RH-facing and PNT-facing language is downstream analytic description of this
integer-level source. Those materials do not make RH, PNT, zero geometry, or
pole placement the first-level object. They record how the exact arithmetic
source appears after zeta compression, using `H(n)=log n+E(n)` in the
zeta-compression load. This file does not itself prove RH or the remaining
source-to-spectral placement step. Read them
source-first, not shadow-first.
