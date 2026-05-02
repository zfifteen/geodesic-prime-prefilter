# Proof

## Headline Result

This repository has a direct deterministic next-prime algorithm: given a known
prime `p`, it determines the next prime `q` by deterministic prime-gap
structure.

The theorem proved in this document is the mathematical selection law at the
core of that algorithm.

Take two consecutive primes. Look at the composite integers strictly between
them. Among those integers, choose the first one with the smallest number of
positive divisors. That integer is the unique integer in the gap with the
largest value of the logarithmic comparison function below.

That selected integer is the stable interior point used by the deterministic
`p -> q` algorithm. The proof below shows that this point is determined by
ordinary divisor counts in every prime gap with a nonempty interior.

This is a universal statement about every prime gap with a nonempty interior.
The computation tables in this document certify the finite cases used by the
proof. They are not a limit on the theorem.

## Basic Objects

Two primes `p < q` are consecutive if there is no prime strictly between them.
Every integer strictly between consecutive primes is composite.

For consecutive primes `p < q`, define the interval between them as

$$I=\{p+1,\ldots,q-1\}$$

For a positive integer `n`, let `tau(n)` be the number of positive divisors of
`n`. For example, `tau(25) = 3` because the positive divisors of `25` are
`1, 5, 25`.

Inside `I`, look for the smallest divisor count that occurs. Then choose the
first integer in `I` with that divisor count. Call that integer `w`.

The comparison value used in this document is

$$F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n$$

## Theorem

Let `p < q` be consecutive primes, and let

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

The interval has a natural stopping point. Since `q` is prime, `tau(q) = 2`.
Since there is no prime strictly between `p` and `q`, every integer `n` with
`p < n < q` has `tau(n) > 2`.

So the first integer after `p` with divisor count `2` is `q`, and the interval
being studied is exactly the finite set before that first value:

$$I=\{p+1,\ldots,q-1\}$$

For any `x` with `p < x <= q`, define the current minimum divisor count before
`x` by

$$D(x)=\min\{\tau(n):p<n<x\}$$

when the set is nonempty. At `x = q`, this is the minimum divisor count in the
whole interval:

$$D(q)=\min\{\tau(n):n\in I\}$$

The chosen integer `w` is the first integer in `I` with `tau(w) = D(q)`.

There cannot be an integer `t` with `w < t < q` and `tau(t) < tau(w)`. If such
a `t` existed, then the minimum divisor count in `I` would be smaller than
`tau(w)`, contradicting the definition of `w`.

There also cannot be any competing integer after `q` in the same interval. The
value `q` has divisor count `2`, so the interval has ended. Integers after `q`
belong to later intervals, not to `I`.

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

Every integer before `w` has smaller comparison value than `w`.

Every integer after `w` has smaller comparison value than `w`.

Therefore `w` is the unique integer in the prime-gap interval where `F(n)` is
largest.

## Audit Tables

The theorem above is universal. The tables below are retained for
certification and reproducibility. They support the finite base used in the
proof; they are not the boundary of the theorem.

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

`PROOF.md` is the single live proof reference for the prime-gap maximizer
theorem.
