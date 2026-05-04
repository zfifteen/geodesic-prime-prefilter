# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## The First Contradiction

Primes are not random. Prime gaps are not chaotic or meaningless.

The truth is the exact opposite.

Start with one prime. The next prime can be found exactly by reading the
numbers that follow it.

That probably contradicts what you were taught about prime numbers. It also
sounds strange at first, because the usual way to talk about primes makes them
feel isolated. A prime appears. Then there is a stretch of composite numbers.
Then another prime appears. The stretch in the middle is called a gap, and the
word makes it easy to imagine that nothing important is happening there.

But the middle is not empty. It is full of integers.

Those integers are not prime, but they are not meaningless. They are composite,
and composite numbers have factor structure. That factor structure is what
this repository reads. The next prime appears where the run of composites ends,
and the composites before it carry the arithmetic that makes that ending
visible.

The usual story treats the numbers between primes as the obstacle. Here they
are the evidence.

## Look Between 23 And 29

It is easier to see the point with a small gap.

The primes `23` and `29` are consecutive. That means everything between them is
composite:

```text
23 | 24 25 26 27 28 | 29
```

If you only ask how large the gap is, the answer is `6`. That is true, but it
throws away almost everything in the picture. The interior is not just a
distance. It is a short ordered list of composite numbers.

Now count divisors.

The number `25` is divisible by `1`, `5`, and `25`, so its divisor count is
`3`. The other interior numbers have their own counts. Read from left to right,
the gap looks like this:

```text
number:        24  25  26  27  28
divisor count:  8   3   4   4   6
```

Now something has changed. The gap is no longer just the distance from `23` to
`29`. It has an internal shape. The smallest divisor count in the interior is
`3`, and it happens at `25`.

That is the first thing to see. The composites between the primes are not
merely non-primes. They form an ordered divisor-count pattern, and one interior
number appears first at the lowest count in the gap.

## When The Lowest Count Repeats

A single example can be too convenient. Maybe `25` stands out only because
that small gap has one obvious winner.

The gap from `89` to `97` removes that comfort. The numbers inside are:

```text
89 | 90 91 92 93 94 95 96 | 97
```

Their divisor counts are:

```text
number:        90  91  92  93  94  95  96
divisor count: 12   4   6   4   4   4  12
```

The lowest count is `4`, but now it appears more than once. It appears at
`91`, `93`, `94`, and `95`.

That means the gap is not only telling us which count is smallest. It is also
telling us where the first occurrence is. Read from left to right, the first
interior number with the lowest count is `91`.

That is the
[Leftmost Minimum-Divisor Rule](LEFTMOST_MINIMUM_DIVISOR_RULE.md) in ordinary
language: inside the gap, find the lowest divisor count, and take the first
number where that count appears.

The chosen number is not the next prime. It is a composite inside the gap. Its
role is different. It marks the first place where the interior reaches its
lowest divisor count.

## Where The Gap Ends

The usual way to find a prime is to test candidates. Try a number. If it is
composite, reject it. Try the next one. Keep going until a number is prime.

That works, but it teaches the wrong instinct for this project. It makes the
next prime feel like an answer that arrives only after enough checks.

There is a simpler way to say what the right endpoint is. A prime has exactly
two positive divisors: `1` and itself. A composite has more than two. So if you
start at a known prime and read forward, every number before the next prime has
more than two divisors. The next prime is the first later number whose divisor
count is exactly `2`.

In the `23` to `29` gap, the counts tell that story directly:

```text
number:        24  25  26  27  28  29
divisor count:  8   3   4   4   6   2
```

The count stays above `2` through the composite interior. At `29`, it becomes
`2`. That is where the gap ends.

So the next prime is not found by chance. Starting from one prime, the next
prime is the first later number with divisor count `2`.

## The Interior And The Endpoint Belong Together

It is tempting to split the story in two. The primes are the real objects, and
the composites between them are just the numbers that are not prime.

This repository does not split them apart. The endpoint and the interior are
read as one interval.

At the right edge, divisor count `2` identifies the next prime. Inside the
gap, the first lowest divisor count identifies the selected composite. Those
two facts live in the same ordered list of numbers.

For `23` to `29`, the selected composite is `25`, and the endpoint is `29`.
For `89` to `97`, the selected composite is `91`, and the endpoint is `97`.

The project also uses a score that says the same thing in normalized form. The
[Divisor Normalization Identity](DIVISOR_NORMALIZATION_IDENTITY.md) places
primes at `Z = 1.0` and places composites below that value. Inside a prime
gap, that score chooses the same selected composite: the leftmost interior
number with the lowest divisor count.

That is the larger reversal. A prime gap is not just a size. It has an ordered
interior, a selected composite inside that interior, and a right endpoint where
the divisor count reaches `2`.

## Why The Prime Generator Is Different

Most prime generators are candidate testers.

They propose a number and ask whether it is prime. If the number is composite,
they reject it and try another. Better generators can make that process much
faster, but the shape is still familiar: propose, test, reject, repeat.

The [PGS Prime Generator](PRIME_GAP_GENERATOR.md) is built around the opposite
reading. It starts with one known prime and reads the arithmetic structure
after it. It is not asking which candidate survives a primality test. It is
asking where the next gap closes.

That is why the output is so small:

```json
{"p": 89, "q": 97}
```

The record says only what matters: start at `89`; the next prime is `97`.

The prime generator uses prime-gap structure to choose the next prime. It does
not choose `q` by trial division, Miller-Rabin, probabilistic primality tests,
sieve generation, fallback prime search, or `nextprime`.

Those checks still matter. They happen after the answer is generated. They
verify the answer; they do not choose it.

## Where The Other Documents Fit

Once you stop treating a prime gap as a meaningless jump, several paths open.

One path follows the selected composite itself. That leads to the
[Leftmost Minimum-Divisor Rule](LEFTMOST_MINIMUM_DIVISOR_RULE.md).

Another path follows the score that puts primes at `Z = 1.0` and compares the
composites below that value. That leads to the
[Divisor Normalization Identity](DIVISOR_NORMALIZATION_IDENTITY.md).

Another path asks how the same kind of structure behaves across many gaps.
That leads to the [Prime Gap Generative Model](PRIME_GAP_GENERATIVE_MODEL.md)
and the [recursive prime walk](RECURSIVE_PRIME_WALK.md).

The [legacy prefilter](LEGACY_PREFILTER.md) records a separate engineering
path built from the same divisor-count normalization.

All of these documents start from the same small observation: look inside the
gap, count what is there, and the interval stops looking like randomness.

## Reading Further

The rest of the repository gives the formal proof, the generator details, the
model results, and the measured surfaces.

- [PROOF.md](PROOF.md) gives the formal proof of the direct next-prime theorem
  and the prime-gap maximizer theorem.
- [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md) expands
  the selected-integer rule in accessible prose.
- [DIVISOR_NORMALIZATION_IDENTITY.md](DIVISOR_NORMALIZATION_IDENTITY.md)
  explains the fixed-point score behind the comparison function.
- [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md) explains how the prime
  generator uses prime-gap structure and why it outputs only
  `{"p": ..., "q": ...}`.
- [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md) explains the
  reduced prime-gap type model and its stable `14`-state core.
- [RECURSIVE_PRIME_WALK.md](RECURSIVE_PRIME_WALK.md) covers the exact recursive
  walk, no-later-simpler-composite closure, and bounded compression work.
- [LEGACY_PREFILTER.md](LEGACY_PREFILTER.md) records the legacy Z-band
  prefilter and RSA benchmark surface.
- [RESULTS.md](RESULTS.md) collects the headline results and measured surfaces.

## Python API

Install the Python package from the repo root:

```bash
python3 -m pip install -e ./src/python
```

## License

This repository is source-available under the
[Business Source License 1.1](LICENSE).

The current grant keeps the code open for research, evaluation, and other
non-production work, and it also permits internal production use for smaller
organizations under the Additional Use Grant in [LICENSE](LICENSE).

Commercial production use outside that grant requires a separate commercial
license. For licensing terms, support, or private commercial use, contact
`dionisio.lopez@icloud.com`.

Each version converts to [Apache License, Version 2.0](LICENSE) four years
after that version is first publicly distributed under the Business Source
License 1.1.

Versions that were first publicly distributed before this change under the MIT
license remain available under those earlier terms.
