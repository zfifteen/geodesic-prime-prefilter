# Divisor Normalization Identity

The README shows that simply counting divisors inside a prime gap already changes how you see the numbers. The gap stops looking like empty space the moment you list those counts from left to right and notice the lowest one emerge at a particular spot.

Raw divisor counts are easy to compute by hand and they reveal real structure. Yet they still have a limitation. They are just plain positive integers — two for any prime, three or more for every composite — but they do not place primes and composites onto one clean, shared scale where you can compare everything directly against the prime class.

The Divisor Normalization Identity solves exactly that problem. It creates a mathematical scale on which every prime sits at precisely the same fixed value while every composite falls below that value in a consistent and meaningful way.

## The Prime Baseline

Begin with the familiar fact that defines a prime. A prime number has exactly two positive divisors: 1 and itself. That divisor count of two becomes the natural baseline for the entire construction.

The goal of the normalization is straightforward: build a function that keeps every prime, no matter how large or small, anchored at exactly the same special value:

$$Z=1.0$$

Once the primes are locked at this fixed point, the scale can push all composites below it without ever disturbing the prime baseline itself. This prime-centered view turns out to be surprisingly powerful when you look inside actual gaps.

## Building The Load

To reach this scale we first combine two pieces of information about any integer n: how many divisors it has, and how large the number itself is. This combination is called the load:

$$\kappa(n)=\frac{d(n)\ln(n)}{e^{2}}$$

Here d(n) is the divisor count of n. The natural logarithm of n accounts for the size of the number. The e² in the denominator is part of the careful tuning that will cancel later.

This load then passes through a transformation that produces the normalized score Z(n):

$$Z(n)=\frac{n}{\exp(v\cdot\kappa(n))}$$

The parameter v controls the strength of the transformation. The key choice in this project is a very specific value of v that creates an exact cancellation and reveals a much simpler identity underneath.

## The Beautiful Cancellation

For the mathematics of prime-gap structure the distinguished value chosen is:

$$v=\frac{e^{2}}{2}$$

When you substitute this particular v into the expression, something elegant happens. Walk through the algebra step by step and watch the pieces simplify.

Start with the full expression after inserting the load:

$$Z(n)=\frac{n}{\exp\left(v\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

Now insert v = e² / 2:

$$Z(n)=\frac{n}{\exp\left(\frac{e^{2}}{2}\cdot\frac{d(n)\ln(n)}{e^{2}}\right)}$$

The e² terms cancel cleanly:

$$Z(n)=\frac{n}{\exp\left(\frac{d(n)}{2}\ln(n)\right)}$$

The exponential of (d(n)/2) times ln(n) is exactly the same as raising n to the power of d(n)/2. This simplifies to:

$$Z(n)=\frac{n}{n^{d(n)/2}}$$

Which reduces directly to the Divisor Normalization Identity:

$$Z(n)=n^{1-d(n)/2}$$

That is the clean, exact form at the heart of the project.

## What The Identity Actually Does

Now apply this simplified identity to different kinds of numbers and watch what happens.

If n is a prime p, then d(p) = 2. Substituting that in gives:

$$Z(p)=p^{1-2/2}=p^{1-1}=p^{0}=1$$

Every prime lands exactly at Z = 1.0, as intended.

Now consider a composite number. A semiprime (the product of two distinct primes) has four divisors, so d(n) = 4. The identity gives:

$$Z(n)=n^{1-4/2}=n^{1-2}=n^{-1}=\frac{1}{n}$$

For any composite number with d(n) > 2 the exponent 1 − d(n)/2 becomes negative. This means Z(n) is a fraction strictly less than 1. The larger the divisor count, the farther below 1 the normalized value falls.

## Why This Matters Inside Prime Gaps

Inside any prime gap every interior number is composite, so every Z value inside that gap is strictly below 1.0. The normalization therefore gives a clear, consistent way to compare those composites against the fixed prime baseline without ever moving the primes themselves.

This is why the selected composite inside a gap can be described in two perfectly matching ways. In ordinary divisor-count language it is the leftmost interior number with the lowest divisor count. In normalized score language it is the interior composite that stands out most clearly according to Z(n) = n^(1 − d(n)/2). Both descriptions identify exactly the same number.

The divisor-count tables make the pattern visible at a glance. The Divisor Normalization Identity places that same pattern onto a clean, fixed, prime-centered mathematical scale. Together they turn the interior of every gap from something that once looked meaningless into structured evidence.
