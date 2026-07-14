# Generator decade ladder scoreboard

## Observable object

Two published implementation surfaces for the Minimal PGS Generator:

1. Full-exact walk style surface on `11..1000000`.
2. Decade ladder with 256 consecutive input primes per decade from `10^8` through `10^18`.

## Mechanism

Each left-panel bar is the **nominal production form** of the decade ladder (256 primes per decade anchor). Heights are not a fresh per-decade re-audit of raw ladder files. The right panel shows published aggregate totals mirrored from `docs/RESULTS.md` via the library fixture.

## Project terms

- **Emitted stream**: only `{"p": ..., "q": ...}`.
- **Decade ladder**: production reference form of the mandatory `10^18` evidence surface for generator claims.

## Status and limits

- Status: **measured** implementation evidence drawn from a fixture that mirrors `docs/RESULTS.md` aggregates.
- A measured surface aggregate is not a theorem bound and does not prove RH, PNT, or RSA-scale claims.
- This figure uses weak measured language only. It does not use program-level claim words.
- The `has_10e18_surface` flag marks that the published generator surface includes magnitude `10^18`. This demo does not re-execute the ladder.
- For forensic re-audit, open the committed ladder artifacts under the generator chapter, not only this scoreboard.
