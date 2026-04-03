# GWR Proof Scripts

This folder is for executable scripts that pursue a universal proof of the
`Gap Winner Rule` (`GWR`).

The current scripts in this folder are not part of the validation registry.
They target the exact missing universal step identified in the findings notes:

- the ordered-dominance theorem already proves that the `GWR` candidate beats
  every later interior composite,
- the remaining proof task is to eliminate every earlier higher-divisor
  spoiler.

## Current Entry Point

- [`earlier_spoiler_scan.py`](./earlier_spoiler_scan.py):
  exact interval scan that
  - identifies the `GWR` candidate in each tested prime gap,
  - checks every earlier interior composite against that candidate using exact
    integer-power score comparison,
  - and records which earlier candidates are already eliminated by the current
    spoiler-bound reduction.
- [`finite_remainder_attempt.py`](./finite_remainder_attempt.py):
  deterministic `Route B3` constructor that
  - attempts to derive the explicit finite remainder bound required by the
    proof note from the current spoiler reduction,
  - and emits the exact obstruction family showing that the current reduction
    alone does not close the infinite tail.
- [`large_prime_reducer.py`](./large_prime_reducer.py):
  deterministic proof-pursuit reducer that
  - exhaustively scans every prime gap below a fixed explicit large-prime
    threshold,
  - then tests a fixed-factor large-prime class table against the exact
    earlier-spoiler inequality,
  - and emits the remaining large-prime divisor classes, if any.
