# RSA v2 40-Bit V1 Algorithm

This document defines the first clean factorizer algorithm before implementation.

The first run is a 40-bit calibration case, but the algorithm is written as the
smallest RSA-scale path. No step may rely on a low-bit shortcut that would need
to be replaced for RSA-260.

## Input

The ladder starts from `ladder_spec.json`. Each public case row contains:

- `case_id`;
- `N`;
- optional `description`.

The fixture builder derives `bits` from `N` and writes `ladder_cases.jsonl`.
The inference runner reads `ladder_cases.jsonl`, not the audit spec.

The inference runner does not read audit factors.

The first case is:

```text
case_id = rsa_v2_40bit_static_001
N = 1099507433251
bits = 40
description = 40-bit calibration rung for reciprocal PGS deadline-lock machinery.
```

The chamber radius, balance band, PGSPG endpoint radius, Rule X candidate
bound, recursive depth, and deadline-width tolerance are global rule constants
in the solver. They are not per-rung inputs. Adding a rung means adding another
public `N` row to `ladder_spec.json` and a physically separate audit row to
`audit_spec.json`.

## Stage 1: Public Center

Compute `isqrt(N)`.

This is the public center of the semiprime chamber. It is not a factor and does
not reveal either endpoint. It gives the fixed point around which the lower and
upper factor chambers face each other.

## Stage 2: Candidate Band

Build the full ordered public candidate band:

```text
[isqrt(N) - radius, isqrt(N) + radius]
```

Each candidate `x` is paired with the public reciprocal floor coordinate
`N // x`. The ordered surface preserves both orientations of a candidate pair.

## Stage 3: Public Filters

Apply cheap public filters before any chamber measurement:

1. Keep candidates inside the global balance band.
2. Keep candidates in wheel-open residue classes.
3. Compute `y = N // x`.
4. Keep pairs whose reciprocal floor `y` stays inside the upper balance band.
5. Keep pairs whose upper coordinate is also wheel-open.
6. Keep pairs whose reciprocal floor remains inside the full public chamber.

These filters reduce the chamber without testing whether `x` divides `N`.

## Stage 4: PGSPG Chamber State

For each serious candidate pair `(x, y)`, derive local PGSPG chamber state on
both sides.

The lower side asks:

```text
previous PGS endpoint before x -> chamber reset -> does it return to x?
```

The upper side asks:

```text
previous PGS endpoint before y -> chamber reset -> does it return to y?
```

The state is derived by code from local public intervals. It is not supplied as
a fixture.

## Stage 5: Reciprocal Recursive Lock

Apply recursive reciprocal PGS stability for a fixed number of rounds.

Default depth:

```text
recursive_depth = 4
```

For each round:

1. Lock the lower side by previous endpoint plus chamber reset.
2. Lock the upper side by previous endpoint plus chamber reset.
3. Transport the lower and upper endpoints through the public reciprocal map.
4. Continue only if both sides remain stable.

A pair that fails local stability or reciprocal stability is eliminated.

## Stage 6: Reciprocal Deadline Lock

After local endpoint/reset survival, compare the reset-deadline state of both
sides under the reciprocal map.

The deadline lock requires:

```text
lower reset signature == upper reset signature
lower reset-deadline margin == upper reset-deadline margin
transported reciprocal deadline widths agree within floor-rounding tolerance
```

This is the resolving PGS rule. Product closure is not used to admit a deadline
lock.

## Stage 7: Audit Certification

Inference emits the unique unordered deadline-locked pair when exactly one such
pair exists.

Audit is a separate downstream script. Audit checks the separate factor file
against `N` and then checks whether inference emitted the same pair.

## Output

If exactly one unordered deadline-locked pair remains, emit a resolved row.

If no deadline-locked pair remains, or more than one unordered pair remains, emit
an explicit unresolved row.

The runner also emits survivor rows and a summary so the funnel can be reviewed
without relying on prose.

## Failure Mode

Every failure to resolve is an experiment result.

Do not add fallback paths, alternate algorithms, random retries, hidden widening,
or a direct factor search to force success.
