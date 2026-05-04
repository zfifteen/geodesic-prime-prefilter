# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## Primes Are Not Random

Primes are not random. Prime gaps are not chaotic or meaningless.

The truth is the exact opposite.

Start with one prime. The next prime can be found exactly by reading the
structure in the numbers that follow it.

This probably contradicts everything you were taught about prime numbers. That
contradiction is where this repository begins.

## The Gap Speaks First

Take the primes `23` and `29`.

Between them are five composite numbers:

```text
23 | 24 25 26 27 28 | 29
```

Those five numbers are not filler. Each one has a divisor count: the number of
positive integers that divide it evenly. For `25`, those divisors are:

```text
1, 5, 25
```

So the divisor count of `25` is `3`.

Now count the whole interior:

- `24` has divisor count `8`
- `25` has divisor count `3`
- `26` has divisor count `4`
- `27` has divisor count `4`
- `28` has divisor count `6`

The lowest count is `3`, and it appears at `25`.

That is the first visible structure. Inside the gap, one composite reaches the
lowest divisor-count load before the others.

## The Tie Is The Next Clue

The next example shows why order matters.

Between `89` and `97`, the interior integers are
`90, 91, 92, 93, 94, 95, 96`.

- `90` has divisor count `12`
- `91` has divisor count `4`
- `92` has divisor count `6`
- `93` has divisor count `4`
- `94` has divisor count `4`
- `95` has divisor count `4`
- `96` has divisor count `12`

The lowest count is `4`, but several numbers share it. Reading from left to
right, the first one is `91`.

That leftmost minimum is the local landmark of the gap. The fuller name is the
[Leftmost Minimum-Divisor Rule](LEFTMOST_MINIMUM_DIVISOR_RULE.md).

The chosen number is not the next prime. It is an interior composite. It marks
the first place where the gap reaches its lowest divisor-count load.

## The Endpoint Has The Sharpest Signal

Now turn from the interior to the right endpoint.

A prime has exactly two positive divisors: `1` and itself. So the endpoint of a
prime gap has a divisor-count signal that no composite in the interior has.

Start with one prime and read forward. Every number before the next prime is
composite. Each of those numbers has more than two divisors. Then the next
prime appears, and the divisor count drops to `2`.

So the endpoint is not found by chance. It is the first later integer whose
divisor count is exactly `2`.

```text
starting from p, the next q is the first later integer with divisor count 2
```

The gap closes there because no earlier integer had the prime signal.

## The Interior Choice And The Endpoint Fit Together

Once the right endpoint is found, the gap has a beginning, an end, and a finite
interior.

The endpoint is the first later integer with divisor count `2`. The interior is
everything before that endpoint. Inside that interior, the selected integer is
the first composite with the lowest divisor count present in the gap.

The selected integer wins two ways at once. It has the smallest divisor count
inside the gap, and it appears as far left as possible among integers with that
count.

Later integers cannot beat it from the left. Earlier integers did not have the
minimum divisor count yet.

That is the interior story in ordinary language.

The score used by the project tells the same story in normalized form. The
[Divisor Normalization Identity](DIVISOR_NORMALIZATION_IDENTITY.md) puts primes
on the fixed-point locus `Z = 1.0` and puts composites below that locus. Inside
a prime gap, that score selects the same local landmark: the leftmost integer
with minimum divisor count.

That is the reversal. A prime gap is not just the distance from one prime to
the next. It has an internal arithmetic landmark, and the endpoint has an exact
divisor-count signal.

## From Structure To Generator

The generator branch turns the structure into an operational artifact.

Given one prime, the [PGS Prime Generator](PRIME_GAP_GENERATOR.md) outputs the
successor prime as a deliberately small record:

```json
{"p": 89, "q": 97}
```

The output stream contains only `p` and `q`. Diagnostics and audit records stay
outside that stream.

The production generator is PGS-only. It does not use trial division. It does
not use Miller-Rabin. It does not use probabilistic primality tests, sieve
generation, fallback prime search, or `nextprime` inside generation. Classical
verification remains downstream audit after generation, not the mechanism for
choosing `q`.

## The Same Lens Opens Other Branches

Once the gap interior is treated as structured, other questions open naturally.

The [Prime Gap Generative Model](PRIME_GAP_GENERATIVE_MODEL.md) studies the
reduced state surface of prime-gap types. The
[recursive prime walk](RECURSIVE_PRIME_WALK.md) studies what happens when the
same divisor-count structure is walked forward gap after gap. The
[legacy prefilter](LEGACY_PREFILTER.md) records a separate downstream
engineering path built from the same normalization program.

The common thread is the same one the small examples already showed: look
inside the prime gap, count what is there, and the interval stops looking like
randomness.

## Reading Further

The formal proof, generator, and model branches all begin from the same local
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
