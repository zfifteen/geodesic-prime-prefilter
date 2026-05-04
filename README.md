# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## The First Thing To See

Prime numbers do not arrive one unit apart. After one prime appears, the next
prime appears some number of steps later.

Between those two primes sit ordinary composite integers. Each of those
composites has a divisor count: the number of positive integers that divide it
evenly. Prime Gap Structure begins with that visible fact. The gap is not
treated as empty distance. It is treated as an interval whose interior has
arithmetic structure.

## What Is A Prime Gap?

A prime gap is the interval between two consecutive primes. If `p` and `q` are
consecutive primes, then every integer strictly between them is composite.

The gap from `23` to `29` contains five interior integers:

```text
23 | 24 25 26 27 28 | 29
```

Prime Gap Structure begins by asking what arithmetic structure is visible
inside that interior.

## Counting The Interior

The divisor count of an integer is written `tau(n)` in the proof. For example,
`25` has three positive divisors:

```text
1, 5, 25
```

So `tau(25) = 3`.

A prime has exactly two positive divisors: `1` and itself. So `tau(n) = 2` is
not just a useful signal. It is exactly the condition that `n` is prime.

The gap interior goes the other way. If `p` and `q` are consecutive primes,
then every integer between them is composite, so every interior integer has
divisor count greater than `2`.

## A First Gap: 23 To 29

Take the consecutive primes `23` and `29`. The integers between them are
`24, 25, 26, 27, 28`. Their divisor counts are:

- `tau(24) = 8`
- `tau(25) = 3`
- `tau(26) = 4`
- `tau(27) = 4`
- `tau(28) = 6`

So `25` wins this gap because it has the smallest divisor count present.

## A Second Gap: 89 To 97

Now take `89` and `97`. The interior integers are
`90, 91, 92, 93, 94, 95, 96`. Their divisor counts are:

- `tau(90) = 12`
- `tau(91) = 4`
- `tau(92) = 6`
- `tau(93) = 4`
- `tau(94) = 4`
- `tau(95) = 4`
- `tau(96) = 12`

Here the smallest divisor count present is `4`, and the leftmost integer with
that divisor count is `91`, so `91` wins.

These examples show the local arithmetic choice that anchors the repository.
The chosen number is not the next prime. It is an interior composite that marks
the lowest divisor-count load inside the gap.

## The Local Choice

The local rule is the
[Leftmost Minimum-Divisor Rule](LEFTMOST_MINIMUM_DIVISOR_RULE.md):

1. inside a prime gap, find the smallest divisor count present among the
   interior composites;
2. if more than one interior composite has that divisor count, take the
   leftmost one.

That chosen interior integer is the selected integer of the gap.

## From A Local Choice To The Next Prime

The proof uses the same divisor-count language, but it first asks an even more
direct question.

Given a known prime `p`, look at the integers after `p` in order:

```text
p + 1, p + 2, p + 3, ...
```

Compute the exact divisor count of each one. Stop at the first integer with
`tau(n) = 2`.

That stopping point is the next prime `q`. This is the direct deterministic
next-prime theorem proved in [PROOF.md](PROOF.md):

```text
q is the first integer greater than p with tau(q) = 2.
```

This statement is not a finite audit result. It is a theorem. The audit tables
in `PROOF.md` preserve certification and provenance; they are not the boundary
of the theorem.

## Why The Stopping Point Is q

The reason is concrete. A number greater than `1` is prime exactly when its
only positive divisors are `1` and itself. That is exactly what `tau(n) = 2`
means.

The integers are checked in increasing order. The algorithm cannot stop before
the next prime, because every integer between `p` and the next prime is
composite. It does stop at the next prime, because the next prime has divisor
count `2`.

So the first divisor-count-two value after `p` is not merely a candidate. It is
the next prime.

## Why The Selected Integer Wins The Gap

Once the stopping point `q` is known, the interval between `p` and `q` is the
prime gap interior. Every integer in that interval is composite.

Inside that finite interval, the selected integer is the first integer with the
smallest divisor count. Every later integer has divisor count at least as large
as the selected integer. Every earlier integer appears before the first
minimum, so its divisor count is larger.

The proof then compares the interior integers with a logarithmic score. The
score comes from the
[Divisor Normalization Identity](DIVISOR_NORMALIZATION_IDENTITY.md), which
places every prime on the fixed-point locus `Z = 1.0` and places composites
below that locus.

For the README-level picture, the effect is enough: among the composites inside
the gap, the selected integer is the unique score winner. In ordinary
divisor-count language, it is the leftmost interior integer with minimum
divisor count. In the proof language, it is the unique maximizer of the
comparison function.

## Where The Generator Enters

The theorem gives the clean mathematical foundation: exact divisor counts
determine the next prime from a known prime `p`, and the selected integer is
the leftmost minimum-divisor integer inside the resulting gap.

The [PGS Prime Generator](PRIME_GAP_GENERATOR.md) is the operational generator
branch built from prime-gap-structure chamber state. Its output stream is
deliberately small:

```json
{"p": 89, "q": 97}
```

The generator output contains only `p` and `q`. Diagnostics and audit records
stay outside the outputted stream. The production generator does not use trial
division, Miller-Rabin, probabilistic primality tests, sieve generation,
fallback prime search, or `nextprime` inside generation. Classical verification
is downstream audit after generation, not a mechanism for choosing `q`.

## Reading Further

The proof, generator, and model branches all begin from the same local
structure inside prime gaps.

- [PROOF.md](PROOF.md) is the single live proof reference for the direct
  deterministic next-prime theorem and the prime-gap maximizer theorem.
- [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md) expands
  the selected-integer rule in accessible prose.
- [DIVISOR_NORMALIZATION_IDENTITY.md](DIVISOR_NORMALIZATION_IDENTITY.md)
  explains the fixed-point score behind the comparison function.
- [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md) explains the PGS-only
  generator and its minimal `{"p": ..., "q": ...}` output contract.
- [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md) explains the
  reduced prime-gap type model and its stable `14`-state core.
- [RECURSIVE_PRIME_WALK.md](RECURSIVE_PRIME_WALK.md) covers the exact recursive
  walk, no-later-simpler-composite closure, and bounded compression work.
- [LEGACY_PREFILTER.md](LEGACY_PREFILTER.md) records the legacy Z-band
  prefilter and RSA benchmark surface.
- [RESULTS.md](RESULTS.md) is the compact index of headline results and
  measured surfaces.

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
