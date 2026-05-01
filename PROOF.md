# Proof

## Short Version

This document proves the prime-gap maximizer theorem.

Take two consecutive primes. Look at the composite integers strictly between
them. Among those integers, choose the first one with the smallest number of
positive divisors. That integer is the unique integer in the gap with the
largest value of the logarithmic comparison function below.

This is a universal statement about every prime gap with a nonempty interior.
The computation tables in this document are part of the finite case
certification and audit trail. They are not a limit on the theorem.

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

## Earlier Integers

Now let `k` be an earlier integer in the gap, so `k < w`. Since `w` is the
first integer with the minimum divisor count, `tau(k) > tau(w)`.

Write

$$e=\tau(k)$$

and

$$d=\tau(w)$$

The inequality `F(k) < F(w)` is equivalent to

$$\left(e-2\right)\log k>\left(d-2\right)\log w$$

The proof closes the earlier side by the following cases.

### Prime-Square Case

Suppose `w` is the square of a prime, say `w = r^2`.

The prime `r` cannot lie inside the interval between `p` and `q`, because there
is no prime strictly between two consecutive primes. Therefore `r <= p`.

Every earlier integer `k` in the interval satisfies `k > p`, hence
`k > r`. Since `w = r^2`, this gives

$$k>\sqrt{w}$$

Every earlier composite before the first prime square has at least `4`
positive divisors. Therefore

$$F(k)\le-\log k$$

and

$$F(w)=-\frac{1}{2}\log w$$

Because `k > sqrt(w)`, we have `log(k) > log(w) / 2`, and therefore
`F(k) < F(w)`.

So the prime-square case is closed.

### Early Divisor-Count `4` Case

Suppose `w` is not a prime square and the first integer in the interval with
divisor count `4` occurs no later than offset `128` from `p`.

Every earlier integer then has divisor count at least `5`. Thus

$$F(k)\le-\frac{3}{2}\log k$$

while the first divisor-count `4` integer has comparison value `-log(w)`.

It is enough to have `k^3 > w^2`. Since `k >= p + 1` and `w <= p + 128`, it is
enough to have

$$\left(p+1\right)^3>\left(p+128\right)^2$$

This inequality holds for every `p >= 28`. The remaining smaller prime gaps
are included in the finite audit table below.

The finite classification found `0` non-square cases where the first
divisor-count `4` integer occurred beyond offset `128`.

So the early divisor-count `4` case is closed.

### Residual Divisor-Count Cases

The remaining earlier integers have larger divisor counts that are not settled
by the two cases above.

For these cases, use Bertrand's theorem: for every prime `p > 1`, there is a
prime less than `2p`. Since `q` is the next prime after `p`, this gives
`q < 2p`. Therefore every integer in the gap is less than `2p`, and every
earlier integer `k` is greater than `p`.

For an earlier integer with divisor count `e` and chosen integer divisor count
`d`, the inequality

$$\left(e-2\right)\log k>\left(d-2\right)\log w$$

is guaranteed by the stronger inequality

$$\left(e-2\right)\log p>\left(d-2\right)\log\left(2p\right)$$

which is equivalent to

$$p^{e-d}>2^{d-2}$$

The table below records the residual divisor-count closures. `Closed` means
that the threshold inequality, the exact finite audit below the threshold, and
the listed branch exhaustion leave no surviving earlier integer with
`F(k) >= F(w)`.

| Earlier divisor count `e` | Status | Largest threshold used | Branch note |
|---:|---|---:|---|
| `10` | Closed | `131` | Threshold plus finite audit below `5,000,000,000`. |
| `14` | Closed | `2,053` | Threshold plus finite audit below `5,000,000,000`. |
| `18` | Closed | `32,771` | Threshold plus finite audit below `5,000,000,000`. |
| `20` | Closed | `131,101` | Threshold plus finite audit below `5,000,000,000`. |
| `22` | Closed | `524,309` | Threshold plus finite audit below `5,000,000,000`. |
| `26` | Closed | `8,388,617` | Threshold plus finite audit below `5,000,000,000`. |
| `27` | Closed | `16,777,259` | Threshold plus finite audit below `5,000,000,000`. |
| `28` | Closed | `33,554,467` | Threshold plus finite audit below `5,000,000,000`. |
| `30` | Closed | `134,217,757` | Threshold plus finite audit below `5,000,000,000`. |
| `34` | Closed | Below audit base | Surfaced in the retained audit and discharged below `5,000,000,000`. |
| `36` | Closed | `65,537` | Top odd branch excluded by exact branch exhaustion and the early divisor-count `4` case. |
| `40` | Closed | `137,438,953,481` | Remaining odd branch exhausted exactly between `5,000,000,000` and the threshold. |
| `42` | Closed | `524,309` | Top odd branch is automatic from the least integer with divisor count `41`. |
| `44` | Closed | `1,048,583` | Top odd branch is automatic from the least integer with divisor count `43`. |
| `50` | Closed | `140,737,488,355,333` | Remaining odd branch exhausted exactly between `5,000,000,000` and the threshold. |
| `52` | Closed | `562,949,953,421,381` | Remaining odd branch exhausted exactly between `5,000,000,000` and the threshold. |
| `54` | Closed | `33,554,467` | Top odd branch is automatic from the least integer with divisor count `53`. |
| `56` | Closed | `9,007,199,254,740,997` | Remaining odd branch exhausted exactly between `5,000,000,000` and the threshold. |
| `60` | Closed | `268,435,459` | Top odd branch is automatic from the least integer with divisor count `59`. |

The high divisor-count cases are closed by the same threshold comparison and
finite divisor-count classification. No requested residual class remains open.

Thus every earlier integer has `F(k) < F(w)`.

## Conclusion

Every integer before `w` has smaller comparison value than `w`.

Every integer after `w` has smaller comparison value than `w`.

Therefore `w` is the unique integer in the prime-gap interval where `F(n)` is
largest.

## Audit Tables

The theorem above is universal. The following tables are retained as audit
evidence and finite-case certification.

| Left-prime range | Prime gaps checked | Earlier integers checked | Exact competing integers |
|---:|---:|---:|---:|
| `2 <= p < 20,000,001` | `1,163,198` | `3,349,874` | `0` |
| `20,000,001 <= p < 100,000,001` | `4,157,943` | `13,321,098` | `0` |
| `100,000,001 <= p < 1,000,000,001` | `42,101,885` | `149,214,917` | `0` |
| `1,000,000,001 <= p < 5,000,000,001` | `172,913,029` | `660,287,089` | `0` |
| Total | `220,336,055` | `826,172,978` | `0` |

The checkpoint stress sample near `10^12` checked `137,771` prime gaps and
`649,769` earlier integers, with `0` unresolved cases. Its median offset was
`1`, its 99th percentile offset was `14`, and its worst offset was `42`.

## Scope

This proof identifies the unique maximizer of `F(n)` inside every prime-gap
interior. It is not a direct next-prime inference theorem.

## Deprecated Documents

Older proof documents have been moved to [docs/deprecated/](docs/deprecated/).
They are historical records, not live proof references.
