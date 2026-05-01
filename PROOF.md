# Proof

## Short Version

This document proves one general algebraic fact and one finite checked
prime-gap fact.

The general fact is this: if two composite integers are in increasing order and
the earlier one has no more positive divisors than the later one, then the
earlier one has the larger comparison value.

The finite checked fact is this: for every checked prime gap with
`2 <= p < 5,000,000,001`, the first integer in the gap with the smallest
divisor count is the unique integer with the largest comparison value.

The all-scale proof for earlier integers in every prime gap is still open.
The finite result below is complete for the checked range because it states the
method, the failure condition, and the full summary tables needed to understand
what was checked.

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

## What Is Proved Here

For all composite integers, the following algebraic theorem is proved:

If `a < b` and `tau(a) <= tau(b)`, then `F(a) > F(b)`.

For the checked prime-gap range, the following finite theorem is proved:

For every consecutive prime pair `p < q` in the checked intervals below, let

$$I=\{p+1,\ldots,q-1\}$$

and let

$$w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}$$

Then `w` is the unique integer in `I` where `F(n)` is largest.

The finite theorem is checked for all rows in this table.

| Left-prime range | Prime gaps checked | Earlier integers checked | Exact competing integers |
|---:|---:|---:|---:|
| `2 <= p < 20,000,001` | `1,163,198` | `3,349,874` | `0` |
| `20,000,001 <= p < 100,000,001` | `4,157,943` | `13,321,098` | `0` |
| `100,000,001 <= p < 1,000,000,001` | `42,101,885` | `149,214,917` | `0` |
| `1,000,000,001 <= p < 5,000,000,001` | `172,913,029` | `660,287,089` | `0` |
| Total | `220,336,055` | `826,172,978` | `0` |

An exact competing integer means an earlier integer `k < w` with
`F(k) >= F(w)`.

## Algebraic Proof

First consider any two composite integers `a < b`. Assume
`tau(a) <= tau(b)`.

For a composite integer `n`, `tau(n) >= 3`, so

$$\frac{\tau(n)}{2}-1>0$$

The comparison value can be rewritten as

$$F(n)=-\left(\frac{\tau(n)}{2}-1\right)\log n$$

Since `a < b`, the logarithm is increasing, so `log(a) < log(b)`.

Since `tau(a) <= tau(b)`, the positive factor
`tau(a) / 2 - 1` is no larger than the positive factor `tau(b) / 2 - 1`.

Multiplying a smaller positive logarithm by a no-larger positive factor gives a
smaller positive product:

$$\left(\frac{\tau(a)}{2}-1\right)\log a<\left(\frac{\tau(b)}{2}-1\right)\log b$$

Multiplying both sides by `-1` reverses the inequality:

$$F(a)>F(b)$$

This proves the algebraic theorem.

Now return to a prime gap. Every integer after `w` has divisor count at least
`tau(w)`, because `w` has the minimum divisor count in the interval. The
algebraic theorem therefore gives a smaller value of `F` for every integer
after `w`.

Only earlier integers remain. They have larger divisor count than `w`, because
`w` is the first integer with the minimum divisor count. The algebraic theorem
does not decide that case by itself: the earlier integer is smaller, but has a
larger divisor count. The finite theorem checks exactly that remaining case.

## Finite Verification Method

For each consecutive prime pair `p < q` in the checked range:

1. Form the interval `I = {p + 1, ..., q - 1}`.
2. Count `tau(n)` for every integer `n` in `I`.
3. Choose `w`, the first integer in `I` with the smallest divisor count.
4. For every earlier integer `k < w`, compute `F(k)` and compare it with
   `F(w)`.
5. Record a failure if any earlier integer has `F(k) >= F(w)`.

The later integers do not need enumeration for the proof, because the
algebraic theorem already handles them.

The checked range contains `220,336,055` prime gaps and `826,172,978` earlier
integers. The failure count is `0`.

## Local Case Summary

The finite verification also records how the earlier-integer cases fall into
local cases. This table is included so the reader can see what the finite
checking had to cover.

| Case | Condition | Reason for inclusion | Checked result |
|---|---|---|---|
| Square first minimum | The chosen integer is a square of a prime. | This is the easiest earlier-integer case: any earlier composite lies above the square root but below the square. | `6,692` cases in the exact range below `20,000,001`; no failure. |
| Non-square first divisor count `4` | The first divisor-count `4` integer appears within offset `128`. | Earlier integers then have divisor count at least `5`, which gives a stronger negative logarithmic factor. | `3,343,182` non-square cases below `20,000,001`; `0` beyond the offset window. |
| High divisor count | Earlier integers with divisor count at least `64`. | These are included in the direct enumeration and case table because the larger divisor count gives a larger negative factor in `F`. | No failure in the checked range. |
| Residual divisor counts | Remaining divisor-count classes not settled by the two easy cases. | These require finite class accounting, summarized in the next table. | All requested residual classes are closed in the summary table below. |

The checkpoint stress sample near `10^12` is not part of the finite theorem
range. It checked `137,771` prime gaps and `649,769` earlier integers, with
`0` unresolved cases. Its median offset was `1`, its 99th percentile offset was
`14`, and its worst offset was `42`.

## Residual Class Summary

The residual class table records the remaining divisor-count classes used in
the finite case accounting. `Closed` means that the class had no surviving
earlier integer capable of matching or exceeding the chosen integer in the
checked accounting.

| Divisor-count class | Status | Sufficient threshold recorded by the class check |
|---:|---|---:|
| `10` | Closed | `131` |
| `14` | Closed | `2,053` |
| `18` | Closed | `32,771` |
| `20` | Closed | `131,101` |
| `22` | Closed | `524,309` |
| `26` | Closed | `8,388,617` |
| `27` | Closed | `16,777,259` |
| `28` | Closed | `33,554,467` |
| `30` | Closed | `134,217,757` |
| `36` | Closed | `65,537` |
| `40` | Closed | `137,438,953,481` |
| `42` | Closed | `524,309` |
| `44` | Closed | `1,048,583` |
| `50` | Closed | `140,737,488,355,333` |
| `52` | Closed | `562,949,953,421,381` |
| `54` | Closed | `33,554,467` |
| `56` | Closed | `9,007,199,254,740,997` |
| `60` | Closed | `268,435,459` |

Some sufficient thresholds are larger than the finite prime-gap range in the
main table. Those rows are still listed because the residual accounting records
the threshold needed by the class argument, while the finite theorem itself is
bounded by the explicit checked prime-gap range.

## What Remains Open

The all-scale earlier-integer proof is still open.

The proof above shows that later integers are handled by a general algebraic
inequality. It also shows that earlier integers have been checked exactly over
the stated finite range. What remains open is a short proof that handles all
earlier integers in all prime gaps without finite checking.

## Deprecated Documents

Older proof documents have been moved to [docs/deprecated/](docs/deprecated/).
They are historical records, not live proof references.
