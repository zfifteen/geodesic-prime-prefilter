# Prime Gap Structure

![Prime Gap Structure hero](docs/assets/prime-gap-structure-hero.jpg)

This repository now carries three major prime-gap results:

- a proved direct deterministic next-prime theorem and local arithmetic
  selection law inside prime gaps, with the live proof reference in
  [PROOF.md](PROOF.md);
- a frozen hierarchical finite-state model for reduced prime-gap types.
- a PGS Prime Generator that infers the successor prime from deterministic
  prime-gap-structure chamber state, without trial division, Miller-Rabin,
  sieve generation, fallback prime search, or `nextprime` inside generation.

Take the consecutive primes `23` and `29`. The integers between them are
`24, 25, 26, 27, 28`. Their divisor counts are:

- `d(24) = 8`
- `d(25) = 3`
- `d(26) = 4`
- `d(27) = 4`
- `d(28) = 6`

So `25` wins this gap because it has the smallest divisor count present.

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
