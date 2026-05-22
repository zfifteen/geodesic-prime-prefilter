# Divisor Normalization Identity

The README shows that simply counting divisors inside a prime gap already changes how you see the numbers. The gap stops looking like empty space the moment you list those counts from left to right and notice the lowest one emerge at a particular spot.

Raw divisor counts are easy to compute by hand and they reveal real structure. Yet they still have a limitation. They are just plain positive integers: two for any prime greater than `1`, three or more for every composite. They do not place primes and composites onto one clean, shared scale where you can compare everything directly against the prime class.

The Divisor Normalization Identity solves exactly that problem. Its preferred coordinate is the excess

$$E(n)=\left(\frac{d(n)}{2}-1\right)\ln n$$

For every integer `n > 1`, primes are exactly the zero-excess integers:

$$E(n)=0$$

Composites have positive excess. The historical normalized score remains the dual coordinate

$$Z(n)=e^{-E(n)}$$

so every prime greater than `1` sits at `Z = 1.0` and every composite falls below that value. Zero-excess is an exact coordinate reformulation of the same identity, not a new theorem.

## The Prime Baseline

Begin with the familiar fact that defines a prime. A prime number greater than `1` has exactly two positive divisors: `1` and itself. That divisor count of two becomes the natural baseline for the entire construction.

The goal of the normalization is straightforward: build a function that keeps every prime greater than `1`, no matter how large or small, anchored at exactly the same special value in the excess coordinate:

$$E=0$$

Once primes greater than `1` are locked at zero excess, the scale places every composite above zero without ever disturbing the prime baseline itself. The dual `Z` coordinate expresses the same fact multiplicatively: primes greater than `1` have `Z = 1.0`, and composites have `0 < Z < 1`. This prime-centered view turns out to be surprisingly powerful when you look inside actual gaps.

## Building The Load

To reach this scale we first combine two pieces of information about any integer `n`: how many divisors it has, and how large the number itself is. This combination is called the load:

$$\kappa(n)=\frac{d(n)\ln(n)}{e^{2}}$$

Here `d(n)` is the divisor count of `n`. The natural logarithm of `n` accounts for the size of the number. The `e^2` in the denominator is part of the careful tuning that will cancel later.

This load then passes through a transformation that produces the normalized score `Z(n)`:

$$Z(n)=\frac{n}{\exp(v\cdot\kappa(n))}$$

The parameter `v` controls the strength of the transformation. The key choice in this project is a very specific value of `v` that creates an exact cancellation and reveals a much simpler identity underneath.

## The Beautiful Cancellation

For the mathematics of prime-gap structure the distinguished value chosen is:

$$v=\frac{e^{2}}{2}$$

When you substitute this particular v into the expression, something elegant happens. Walk through the algebra step by step and watch the pieces simplify.

Start with the full expression after inserting the load:

$$Z(n)=\frac{n}{\exp\left(v\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

Now insert `v = e^2 / 2`:

$$Z(n)=\frac{n}{\exp\left(\frac{e^{2}}{2}\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

The `e^2` terms cancel cleanly:

$$Z(n)=\frac{n}{\exp\left(\frac{d(n)}{2}\ln(n)\right)}$$

The exponential of `(d(n)/2) ln(n)` is exactly the same as raising `n` to the power of `d(n)/2`. This simplifies to:

$$Z(n)=\frac{n}{n^{d(n)/2}}$$

Which reduces directly to the Divisor Normalization Identity:

$$Z(n)=n^{1-d(n)/2}$$

That is the clean, exact multiplicative form at the heart of the project. Taking the negative logarithm gives the preferred zero-excess coordinate:

$$E(n)=-\ln Z(n)=\left(\frac{d(n)}{2}-1\right)\ln n$$

Thus the same identity has two coordinates:

$$Z(n)=e^{-E(n)}$$

## What The Identity Actually Does

Now apply this simplified identity to different kinds of numbers and watch what happens.

If `n > 1` is a prime `p`, then `d(p) = 2`. Substituting that into the excess coordinate gives:

$$E(p)=\left(\frac{2}{2}-1\right)\ln p=0$$

In the dual coordinate:

$$Z(p)=p^{1-2/2}=p^{1-1}=p^{0}=1$$

Every prime greater than `1` lands exactly at `E = 0` and exactly at `Z = 1.0`, as intended.

Now consider a composite number. A semiprime (the product of two distinct primes) has four divisors, so `d(n) = 4`. The excess coordinate gives:

$$E(n)=\left(\frac{4}{2}-1\right)\ln n=\ln n$$

The dual coordinate gives:

$$Z(n)=n^{1-4/2}=n^{1-2}=n^{-1}=\frac{1}{n}$$

For any composite number with `d(n) > 2`, the excess `E(n)` is positive and the exponent `1 - d(n)/2` is negative. This means `Z(n)` is a fraction strictly less than `1`. The larger the divisor count, the larger the excess and the farther below `1` the dual normalized value falls.

## Why This Matters Inside Prime Gaps

Inside any prime gap every interior number is composite, so every excess value inside that gap is strictly above `0` and every `Z` value is strictly below `1.0`. The normalization therefore gives a clear, consistent way to compare those composites against the fixed prime baseline without ever moving the primes themselves.

This is why the selected composite inside a gap can be described in two perfectly matching ways. In ordinary divisor-count language it is the leftmost interior number with the lowest divisor count. In zero-excess language it is the leftmost interior number where the excess is minimal. In the dual score language it is the interior composite that stands out according to `Z(n) = n^(1 - d(n)/2)`. These descriptions identify exactly the same number because

$$\arg\max Z(n)=\arg\min E(n)$$

The divisor-count tables make the pattern visible at a glance. The Divisor Normalization Identity places that same pattern onto a clean, fixed, prime-centered mathematical scale. The preferred reading is now zero excess at primes greater than `1`, positive excess at composites, and `Z(n)=e^{-E(n)}` as the exact dual coordinate.
