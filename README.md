# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## The First Contradiction

Primes are not random. Prime gaps are not chaotic or meaningless.

The truth is the exact opposite.

Start with one prime. Look at the integers that come after it. The next prime can be found exactly by reading those numbers.

This idea probably contradicts what most people believe about primes. The usual story makes primes feel isolated. A prime appears. A stretch of composites follows. Then another prime appears. That stretch in the middle is called a gap, and the name itself encourages us to think nothing important happens there.

But the middle is not meaningless. It is full of information.

Everything between two consecutive primes is factor structure. Those composite numbers carry the arithmetic that makes the ending of the gap visible.

The usual story treats the numbers between primes as an obstacle. Here they are the evidence.

## Look Between 23 and 29

A small concrete example shows what this means.

The primes 23 and 29 are consecutive. Everything between them is composite:

23 | 24 25 26 27 28 | 29

If you only ask how large the gap is, the answer is six. That is true, but it discards most of the picture.

The interior is not just empty space. It is a short ordered list of divisor counts. Here is that list:

number:        24  25  26  27  28
divisor count:  8   3   4   4   6

The smallest value in this list is 3. It appears first at the number 25.

## When The Lowest Count Appears Multiple Times

To see that this is not an accident, look at the gap from 89 to 97:

89 | 90 91 92 93 94 95 96 | 97

The divisor counts inside are:

number:        90  91  92  93  94  95  96
divisor count: 12   4   6   4   4   4  12

The lowest count is now 4, and it appears four different times. Reading from left to right, the first time that lowest count occurs is at 91.

This pattern holds generally: inside any prime gap there is always a first interior number with the lowest divisor count.

## How The Gap Ends

At the right end of the gap something very clear happens.

A prime has exactly two positive divisors: 1 and itself. Every composite number has more than two.

If you start at one prime and read forward through the integers, every composite has a divisor count greater than 2. The next prime is the first number that has a divisor count of exactly 2.

In the 23–29 gap the list continues:

number:        24  25  26  27  28  29
divisor count:  8   3   4   4   6   2

The count stays above 2 until it reaches 29.

## Interior And Endpoint Together

The interior pattern and the endpoint are part of the same story. They are read from the same ordered sequence.

The first interior number with the lowest divisor count marks a special point inside the gap. The first later number with divisor count 2 marks the end of the gap. Both are visible in the divisor count list.

This gives the entire interval a clear structure. The gap is no longer just a distance between two primes. It has an internal shape that points directly to the next prime.

## A Different Way To Generate Primes

Most methods for finding primes work by testing candidate numbers one after another.

This project uses a different approach. It starts from one known prime and reads the factor structure that follows. Using the divisor count pattern inside the gap, it determines exactly where the next prime appears.

The output is therefore very small and direct.

This generator does not choose the next prime through repeated primality testing. The structure itself shows where the gap will close. Testing comes afterward only for confirmation.

## Where This Leads

Once you start seeing prime gaps this way, many natural questions open up. You can follow what that first special composite means. You can study the normalized score that places all primes at 1.0. You can explore how this structure behaves across large ranges of numbers. You can examine the exact process of walking from prime to prime using only this information.

All of these paths grow from one simple shift in perspective: look inside the gap and count what is there.

## Reading Further

- [PROOF.md](PROOF.md) gives the formal statement and proof of the direct next-prime theorem and the prime-gap maximizer theorem.
- [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md) explores the rule that identifies the special composite inside each gap.
- [DIVISOR_NORMALIZATION_IDENTITY.md](DIVISOR_NORMALIZATION_IDENTITY.md) explains the normalization that places primes at Z = 1.0.
- [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md) describes how the generator reads the structure.
- [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md) and [RECURSIVE_PRIME_WALK.md](RECURSIVE_PRIME_WALK.md) examine the broader model and recursive behavior.
- [LEGACY_PREFILTER.md](LEGACY_PREFILTER.md) documents the earlier prefilter approach.
- [RESULTS.md](RESULTS.md) presents the measured results and surfaces.

## Python API

Install the Python package from the repo root:

```bash
python3 -m pip install -e ./src/python
