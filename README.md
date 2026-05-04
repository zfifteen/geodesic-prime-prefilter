# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

## The Usual Story Is Incomplete

Most people meet prime numbers through the same warning: primes are irregular,
prime gaps are unpredictable, and after a prime appears there is no obvious
way to know where the next one will be.

That story is useful as a first impression, but it misses the thing this
repository studies. A prime gap is not empty space. Between one prime and the
next prime sit ordinary composite integers, and those composites carry visible
arithmetic structure.

Prime Gap Structure starts there. It looks inside the gap instead of treating
the gap as a blank distance.

## The Gap Has An Interior

Take two consecutive primes, call them `p` and `q`. The prime gap is the
interval between them. Every integer strictly between `p` and `q` is composite,
because if another prime appeared there, then `p` and `q` would not be
consecutive.

For example, the gap from `23` to `29` looks like this:

```text
23 | 24 25 26 27 28 | 29
```

The primes are the endpoints. The composites in the middle are the interior.
PGS begins by asking what the interior is telling us.

## Divisor Counts Are The First Signal

Every integer has a divisor count: the number of positive integers that divide
it evenly. The number `25` has three positive divisors:

```text
1, 5, 25
```

So the divisor count of `25` is `3`.

A prime has exactly two positive divisors: `1` and itself. A composite has more
than two. That means divisor count gives a direct way to read the difference
between the endpoints of a prime gap and the composite interior.

Now look again at the gap from `23` to `29`. The interior integers are
`24, 25, 26, 27, 28`. Their divisor counts are:

- `24` has divisor count `8`
- `25` has divisor count `3`
- `26` has divisor count `4`
- `27` has divisor count `4`
- `28` has divisor count `6`

The smallest divisor count in this gap is `3`, and it occurs at `25`. So `25`
is the interior integer that stands out.

## The Tie Is The Next Clue

The gap from `89` to `97` shows why the left-to-right order matters. Its
interior integers are `90, 91, 92, 93, 94, 95, 96`. Their divisor counts are:

- `90` has divisor count `12`
- `91` has divisor count `4`
- `92` has divisor count `6`
- `93` has divisor count `4`
- `94` has divisor count `4`
- `95` has divisor count `4`
- `96` has divisor count `12`

Here the smallest divisor count is `4`, but several integers have that count.
Reading the gap from left to right, the first one is `91`.

So the local choice is not merely "find a low divisor count." It is more exact:
find the smallest divisor count in the gap, and if several integers share it,
take the first one. That is the
[Leftmost Minimum-Divisor Rule](LEFTMOST_MINIMUM_DIVISOR_RULE.md).

The chosen number is called the selected integer of the gap. It is not the next
prime. It is the interior composite where the gap first reaches its lowest
divisor-count load.

## The Endpoint Has Its Own Signal

Now turn from the interior back to the right endpoint.

A prime is exactly a number with two positive divisors. So if you start just
after a known prime `p` and inspect the integers in order, the first integer
with divisor count `2` is the next prime `q`.

That is the direct deterministic next-prime statement at the center of the
repository:

```text
starting from p, the next q is the first later integer with divisor count 2
```

This does not say the gap is guessed. It says the endpoint has a precise
divisor-count signature. Before `q`, every integer is composite. At `q`, the
divisor count drops to `2`, and the gap closes.

## The Interior Choice And The Endpoint Fit Together

Once `q` closes the gap, the interior is a finite list of composites. In that
finite list, one composite appears first at the lowest divisor count present in
the gap. That is the selected integer.

The selected integer wins two ways at once. It has the smallest divisor count
inside the gap, and it appears as far left as possible among integers with that
count. Later integers cannot be earlier than it. Earlier integers did not have
the minimum divisor count yet.

The score used by the project makes the same choice in normalized form. The
[Divisor Normalization Identity](DIVISOR_NORMALIZATION_IDENTITY.md) puts primes
on the fixed-point locus `Z = 1.0` and places composites below that locus.
Inside a prime gap, that score selects the same interior integer: the leftmost
integer with minimum divisor count.

This is the first real reversal of the usual intuition. The gap is not just the
distance from `p` to `q`. It has an internal arithmetic landmark.

## From Structure To Generator

The generator branch asks what can be done with that structure operationally.
Given a prime `p`, the [PGS Prime Generator](PRIME_GAP_GENERATOR.md) outputs
the successor prime as a deliberately small record:

```json
{"p": 89, "q": 97}
```

The output stream contains only `p` and `q`. Diagnostics and audit records stay
outside that stream.

The production generator is PGS-only. It does not use trial division,
Miller-Rabin, probabilistic primality tests, sieve generation, fallback prime
search, or `nextprime` inside generation. Classical verification remains
downstream audit after generation, not the mechanism for choosing `q`.

## The Same Lens Opens Other Branches

Once the gap interior is treated as structured, other questions become visible.
The [Prime Gap Generative Model](PRIME_GAP_GENERATIVE_MODEL.md) studies the
reduced state surface of prime-gap types. The
[recursive prime walk](RECURSIVE_PRIME_WALK.md) studies what happens when the
same divisor-count structure is walked forward gap after gap. The
[legacy prefilter](LEGACY_PREFILTER.md) records a separate downstream
engineering path built from the same normalization program.

The common thread is the same one the small examples already showed: look
inside the prime gap, count what is there, and the interval stops looking like
empty distance.

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
