# Proof

## Headline Theorem

Given a known prime `p`, there is a direct deterministic next-prime algorithm:
compute exact divisor counts for the integers greater than `p`, in increasing
order, and stop at the first integer with exactly two positive divisors. That
integer is the next prime `q`.

For a positive integer `n`, let `tau(n)` be the number of positive divisors of
`n`. The theorem defines `q` from `p` alone:

$$q=\min\{n>p:\tau(n)=2\}$$

This document first proves that this deterministic rule returns the next prime.
It then proves the selected-integer theorem inside the interval produced by
that rule: among the integers strictly between `p` and `q`, the first integer
with the smallest divisor count is the unique maximizer of the logarithmic
comparison function below.

Both statements are universal under their stated hypotheses. The computation
tables in this document certify finite cases used by the proof; they are not
limits on the theorem.

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
comparison, and the finite classification tables in this document.

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

### Threshold Lemma

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

This finite base closes every row whose threshold is below `5,000,000,000`,
because the threshold lemma closes all larger `p`.

### Witness Threshold Lemma

Let `M(d)` be the least positive integer with exactly `d` positive divisors.
If `M(d) >= 2T(d,e)`, then any chosen integer with divisor count `d` satisfies
`w >= M(d)`. Since `w < 2p`, it follows that `p > M(d) / 2`, hence
`p > T(d,e)`. The threshold lemma then closes that pair.

The witness rows used below are:

| Winner divisor count `d` | Earlier divisor count `e` | `M(d)` | `T(d,e)` | Result |
|---:|---:|---:|---:|---|
| `41` | `42` | `1,099,511,627,776` | `549,755,813,888` | `M(d) = 2T(d,e)` |
| `43` | `44` | `4,398,046,511,104` | `2,199,023,255,552` | `M(d) = 2T(d,e)` |
| `53` | `54` | `4,503,599,627,370,496` | `2,251,799,813,685,248` | `M(d) = 2T(d,e)` |
| `59` | `60` | `288,230,376,151,711,744` | `144,115,188,075,855,872` | `M(d) = 2T(d,e)` |

### Odd Adjacent Branch Lemma

The only adjacent odd winner branches that remain above the finite base and
are not closed by the witness threshold lemma are listed below.

For each row, the enumeration condition was: list every integer with divisor
count `d` whose previous prime `p` lies in the stated interval, then compute
the actual containing prime gap and check whether that integer is the chosen
integer and whether an earlier integer with divisor count `e` occurs before
it.

| Winner divisor count `d` | Earlier divisor count `e` | Certified `p` interval | Candidate count | Result |
|---:|---:|---|---:|---|
| `35` | `36` | `5,000,000,000 < p <= 8,589,934,592` | `5` | `0` chosen-integer gaps and `0` earlier pairs |
| `39` | `40` | `5,000,000,000 < p <= 137,438,953,472` | `655` | `0` chosen-integer gaps and `0` earlier pairs |
| `49` | `50` | `5,000,000,000 < p <= 140,737,488,355,328` | `58` | `1` chosen-integer gap and `0` earlier pairs |
| `51` | `52` | `5,000,000,000 < p <= 562,949,953,421,312` | `9,413` | `3` chosen-integer gaps and `0` earlier pairs |
| `55` | `56` | `5,000,000,000 < p <= 9,007,199,254,740,992` | `439` | `0` chosen-integer gaps and `0` earlier pairs |

Thus none of these branches contains an earlier integer with `F(k) >= F(w)`.

### Classification Lemma

After the prime-square case and the threshold monotonicity reductions, the
retained divisor-count pairs are exactly the rows below. Each row is closed by
the stated mechanism. Any unlisted larger `e` for the same `d` has a smaller
threshold, and any unlisted smaller `d` for the same `e` has a smaller
threshold.

The table is not a catalog of every divisor count that can occur as `tau(w)`.
Large divisor counts can occur as the minimum divisor count in a gap. A divisor
count `d` needs a row here only when the adjacent earlier-integer comparison
`(d, d + 1)` remains a case requiring proof after the preceding reductions. If
the chosen integer is the first interior integer, or if no earlier integer with
the adjacent divisor count occurs before it in the checked cases, then there is
no earlier integer of that class to compare with `w`.

Thus the rows below are the retained adjacent comparison pairs, not the retained
winner divisor counts.

| Winner divisor count `d` | Earlier divisor count `e` | `T(d,e)` | Closure |
|---:|---:|---:|---|
| `4` | `5` | `4` | Threshold lemma; smaller prime case has no earlier integer |
| `9` | `10` | `128` | Finite Base Lemma |
| `13` | `14` | `2,048` | Finite Base Lemma |
| `17` | `18` | `32,768` | Finite Base Lemma |
| `19` | `20` | `131,072` | Finite Base Lemma |
| `21` | `22` | `524,288` | Finite Base Lemma |
| `25` | `26` | `8,388,608` | Finite Base Lemma |
| `26` | `27` | `16,777,216` | Finite Base Lemma |
| `27` | `28` | `33,554,432` | Finite Base Lemma |
| `29` | `30` | `134,217,728` | Finite Base Lemma |
| `33` | `34` | `2,147,483,648` | Finite Base Lemma |
| `35` | `36` | `8,589,934,592` | Odd Adjacent Branch Lemma |
| `39` | `40` | `137,438,953,472` | Odd Adjacent Branch Lemma |
| `41` | `42` | `549,755,813,888` | Witness Threshold Lemma |
| `43` | `44` | `2,199,023,255,552` | Witness Threshold Lemma |
| `49` | `50` | `140,737,488,355,328` | Odd Adjacent Branch Lemma |
| `51` | `52` | `562,949,953,421,312` | Odd Adjacent Branch Lemma |
| `53` | `54` | `2,251,799,813,685,248` | Witness Threshold Lemma |
| `55` | `56` | `9,007,199,254,740,992` | Odd Adjacent Branch Lemma |
| `59` | `60` | `144,115,188,075,855,872` | Witness Threshold Lemma |

Every retained pair is closed. By the two monotonicity facts in the threshold
lemma, no omitted larger earlier divisor count or smaller winner divisor count
can be harder than the listed closed row.

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

## Square-Branch Reduction

This reduction records the remaining bounded-compression obligation. It is not
a proof of the square branch.

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

Since `w` is the leftmost interior minimum, this `r^2` is the first prime
square in the gap interior. The square-branch bounded-compression target is
exactly

```text
r^2 - p <= C(q),
```

where

```text
C(q) = max(64, ceil(0.5 * log(q)^2)).
```

Because `r^2 < q`, the stronger sufficient theorem is

```text
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

The Interior Maximizer Theorem does not imply this distance bound. In the
square branch, it identifies the first interior prime square as the selected
witness after the gap interior is fixed. It does not bound the distance from
the left endpoint `p` to that first interior prime square.

Thus the square branch is closed exactly by the following independent theorem:

```text
For every consecutive prime gap whose first interior prime square is r^2,
r^2 - p <= max(64, ceil(0.5 * log(r^2)^2)).
```

Until that prime-square proximity theorem is proved, the all-scale bounded
dynamic cutoff theorem remains unresolved on the square branch.

## Audit Tables

The direct next-prime theorem and the Interior Maximizer Theorem are universal.
The finite bounded-compression base is a finite computational lemma. The
residual K=128 lemma is a finite residual branch-elimination theorem. The
square-branch reduction identifies the exact remaining theorem obligation. The
tables below are retained for certification and reproducibility. They support
the finite base used in the maximizer proof; they are not the boundary of either
universal theorem.

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

## Document Status

`PROOF.md` is the single live proof reference for the direct deterministic
next-prime theorem, the prime-gap maximizer theorem, and the finite
bounded-compression base. It also records the residual K=128 first-d4
branch-elimination lemma and the square-branch reduction obligation.
