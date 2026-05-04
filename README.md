# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## What This Repository Studies

Prime numbers do not arrive one unit apart. After one prime appears, the next
prime appears some number of steps later. The integers between those two primes
are composite, and their divisor counts are not random-looking noise in this
repository. They are the first visible structure.

Prime Gap Structure studies that structure. Given a known prime `p`, the
project studies the arithmetic shape of the interval after `p`, the local rule
that selects an interior integer, and the deterministic generator that infers
the next prime `q`.

## What Is A Prime Gap?

A prime gap is the interval between two consecutive primes. If `p` and `q` are
consecutive primes, then every integer strictly between them is composite.

The gap from `23` to `29` contains five interior integers:

```text
23 | 24 25 26 27 28 | 29
```

Prime Gap Structure begins by asking what arithmetic structure is visible
inside that interior.

## A First Gap: 23 To 29

Take the consecutive primes `23` and `29`. The integers between them are
`24, 25, 26, 27, 28`. Their divisor counts are:

- `d(24) = 8`
- `d(25) = 3`
- `d(26) = 4`
- `d(27) = 4`
- `d(28) = 6`

So `25` wins this gap because it has the smallest divisor count present.

## A Second Gap: 89 To 97

Now take `89` and `97`. The interior integers are
`90, 91, 92, 93, 94, 95, 96`. Their divisor counts are:

- `d(90) = 12`
- `d(91) = 4`
- `d(92) = 6`
- `d(93) = 4`
- `d(94) = 4`
- `d(95) = 4`
- `d(96) = 12`

Here the smallest divisor count present is `4`, and the leftmost integer with
that divisor count is `91`, so `91` wins.

These examples show the local arithmetic choice that anchors the repository.

## The Local Choice

The local rule is the **Leftmost Minimum-Divisor Rule**:

1. inside a prime gap, find the smallest divisor count present among the
   interior composites;
2. if more than one interior composite has that divisor count, take the
   leftmost one.

That chosen interior integer is the selected integer of the gap.

## From This Local Choice To The Project

The repository studies how this local arithmetic structure determines,
organizes, and generates prime gaps.

The proof branch states the direct deterministic next-prime theorem and the
leftmost minimum-divisor theorem. The generator branch uses deterministic
prime-gap-structure chamber state to output the successor prime. The model
branch studies the reduced state surface of prime-gap types.

## The Three Main Results

- **Direct deterministic next-prime theorem and Leftmost Minimum-Divisor Rule:**
  exact divisor counts determine the next prime from a known prime `p`, and the
  selected integer inside each prime gap is the leftmost interior integer with
  minimum divisor count. The live proof reference is [PROOF.md](PROOF.md), with
  a readable overview in
  [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md).
- **PGS Prime Generator:** the generator outputs one two-key
  `{"p": ..., "q": ...}` record per given prime `p`, with diagnostics outside
  the outputted stream. See
  [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md).
- **Prime Gap Generative Model:** the reduced prime-gap type surface closes to
  a frozen hierarchical finite-state model with a stable `14`-state core. See
  [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md).

## Start Reading Here

- For the core proof, read [PROOF.md](PROOF.md).
- For the leftmost minimum-divisor rule, read
  [LEFTMOST_MINIMUM_DIVISOR_RULE.md](LEFTMOST_MINIMUM_DIVISOR_RULE.md).
- For the PGS Prime Generator, read
  [PRIME_GAP_GENERATOR.md](PRIME_GAP_GENERATOR.md).
- For the prime-gap generative model, read
  [PRIME_GAP_GENERATIVE_MODEL.md](PRIME_GAP_GENERATIVE_MODEL.md).
- For the divisor-normalization score, read
  [DIVISOR_NORMALIZATION_IDENTITY.md](DIVISOR_NORMALIZATION_IDENTITY.md).
- For the recursive prime walk and bounded compression, read
  [RECURSIVE_PRIME_WALK.md](RECURSIVE_PRIME_WALK.md).
- For the legacy prefilter and RSA benchmark surface, read
  [LEGACY_PREFILTER.md](LEGACY_PREFILTER.md).
- For the compact result index, read [RESULTS.md](RESULTS.md).

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
