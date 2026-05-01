# Exact Divisor-Count Tail Note

## Purpose

This note records the mathematical tail argument recovered from the exact
next-prime generator work.

The point is narrow: once an exact divisor-count scan reaches the first later
integer with divisor count `2`, the current interval is over. Integers after
that value belong to the next interval. They are not an unbounded tail of cases
inside the interval just closed.

## Setting

Let `p` be a prime, and let `q` be the least integer greater than `p` with
exactly two positive divisors.

Then `q` is the next prime after `p`.

Every integer `n` with `p < n < q` is composite, so `tau(n) > 2`. The value
`q` itself has `tau(q) = 2`.

Thus the interval between `p` and `q` is exactly the finite set

$$I=\{p+1,\ldots,q-1\}$$

The first value with divisor count `2` terminates the interval.

## Prefix Minimum

For each `x` with `p < x <= q`, define the current composite prefix minimum by
looking only at composite integers before `x`:

$$D(x)=\min\{\tau(n):p<n<x\}$$

when the set is nonempty.

At `x = q`, this gives the minimum divisor count inside the whole interval:

$$D(q)=\min\{\tau(n):n\in I\}$$

Let `w` be the first integer in `I` where this minimum occurs. Then
`tau(w) = D(q)`.

## Tail Closure

There cannot be an integer `t` with `w < t < q` and `tau(t) < tau(w)`.

If such a `t` existed, then `t` would be in `I`, so the minimum divisor count
inside `I` would be at most `tau(t)`, which is strictly smaller than `tau(w)`.
That contradicts the definition of `w`.

There also cannot be a competing integer after `q` inside the same interval.
The value `q` has divisor count `2`, so it is the next prime and the interval
has already ended.

Therefore the right-side tail has two separate closures:

- before `q`, no lower divisor count can occur after `w`;
- after `q`, integers are outside the interval and cannot compete.

This argument does not depend on an upper bound for the possible value of
`tau(w)`. It holds for every divisor count because it uses exact termination at
the first later value with divisor count `2`.

## Relation To The Live Proof

The live root proof uses this argument to make clear that there is no unbounded
right-side divisor-count tail inside a prime gap.

The remaining earlier-side comparison is a different question: if `k < w`, then
`tau(k) > tau(w)`, and the proof must compare the positional advantage of `k`
against its larger divisor count.
