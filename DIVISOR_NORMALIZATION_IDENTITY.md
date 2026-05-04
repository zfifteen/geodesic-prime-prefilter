# Divisor Normalization Identity

The README begins with divisor counts because they are easy to see. Count the divisors inside a prime gap, read the counts from left to right, and the gap stops looking like a meaningless jump.

But divisor counts by themselves are still raw counts. They tell you how many divisors an integer has, but they do not yet put primes and composites on one shared scale.

The Divisor Normalization Identity gives the project that scale.

## The Prime Baseline

A prime has exactly two positive divisors: `1` and itself. That makes divisor count `2` the prime baseline.

The normalization is built so that every prime lands at the same value:

$$Z=1.0$$

That is the fixed point for primes. Composites have more than two divisors, and under the same normalization they fall below that prime value.

The purpose is not to guess whether a number is prime from a vague score. The purpose is to compare numbers in a way that keeps the prime class fixed and pushes composites below it.

## The Load

The construction starts with the divisor normalization load:

$$\kappa(n)=\frac{d(n)\ln(n)}{e^{2}}$$

Here `d(n)` is the divisor count of `n`. The load combines two pieces of information: how many divisors the number has, and how large the number is.

That load then passes through the Z-transform:

$$Z(n)=\frac{n}{\exp(v\cdot\kappa(n))}$$

The parameter `v` sets the scale of the transformation.

## The Cancellation

For this prime-gap structure program, the distinguished value is:

$$v=\frac{e^{2}}{2}$$

That value matters because it cancels the `e^2` in the load and leaves an exact arithmetic identity.

Substitute the load into the transform:

$$Z(n)=\frac{n}{\exp\left(v\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

Now set `v = e^2 / 2`:

$$Z(n)=\frac{n}{\exp\left(\frac{e^{2}}{2}\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

The `e^2` terms cancel:

$$Z(n)=\frac{n}{\exp\left(\frac{d(n)}{2}\ln(n)\right)}$$

The exponential term becomes a power of `n`:

$$Z(n)=\frac{n}{n^{d(n)/2}}$$

So the identity is:

$$Z(n)=n^{1-d(n)/2}$$

That is the Divisor Normalization Identity.

## What It Does

Now apply the identity to the prime baseline.

If `p` is prime, then `d(p) = 2`. Substitute that into the exponent:

$$Z(p)=p^{1-2/2}=p^{0}=1$$

Every prime lands at `Z = 1.0`.

A semiprime with two distinct prime factors has divisor count `4`, so:

$$Z(n)=n^{1-4/2}=n^{-1}=\frac{1}{n}$$

Composites in general have divisor count greater than `2`, so their exponent is negative and their `Z` value falls below `1`.

## Why It Matters For Prime Gaps

Inside a prime gap, every interior number is composite. The normalization lets the project compare those composites against the prime baseline without moving the prime baseline itself.

That is why the selected composite can be described in two matching ways.

In ordinary divisor-count language, it is the leftmost interior number with the lowest divisor count.

In normalized score language, it is the interior composite chosen by the score derived from `Z(n) = n^(1 - d(n)/2)`.

The two descriptions point to the same object. The divisor-count table makes the structure visible. The Divisor Normalization Identity puts that same structure on a fixed prime-centered scale.
