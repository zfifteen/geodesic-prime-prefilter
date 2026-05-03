# RSA v2 Strategy Memory For Codex

This file is operational memory for future Codex sessions working inside
`experiments/rsa/v2`. It is not a traditional package README.

## Current State

The official v2 runner is now a PGS-first anchor-surface probe.

It does not claim to solve the ladder. It derives public two-sided PGSPG
endpoint/reset state and returns unresolved until the transported deadline
invariant is derived.

This is intentional. The previous radius-first solver was withdrawn as the live
algorithm because it applied a close-factor gate before PGS state was measured.

## Governing Correction

The wrong front door was:

```text
isqrt(N) +/- fixed radius
-> wheel / reciprocal filters
-> PGSPG state
-> raw deadline-margin equality
```

That path solved the 40-bit rung only because the factors were already close to
`isqrt(N)`. It excluded the 50-bit factors before PGS logic could inspect them.

The live front door is:

```text
public N
-> isqrt(N) as orientation only
-> walk lower public endpoints from the square-root side
-> map each endpoint by y = floor(N / x)
-> require the reciprocal side to be a public endpoint
-> derive PGSPG reset state on both sides
-> report two-sided reset locks
-> return unresolved until the transported deadline invariant is known
```

The square root orients the lower and upper sides. It is not a fixed additive
candidate chamber.

## PGSPG Concepts Carried Forward

The factorizer uses the PGS Prime Generator as the local state engine:

- public endpoints;
- wheel-open offsets;
- exact divisor-count interval state;
- GWR carrier state;
- search-interval reset;
- tail and threat reset-deadline fields;
- explicit unresolved state.

The factorizer does not place factorization logic inside the generator. It calls
the generator's chamber-reset certificate as a read-only local state adapter.

## What The Current Runner Emits

For each public `N`, the runner reports:

- lower PGS endpoints seen from the square-root side;
- reciprocal floor rows inside the public balanced interval;
- reciprocal wheel-open rows;
- reciprocal endpoint rows;
- two-sided PGSPG reset-lock rows;
- transported reset-to-deadline widths;
- explicit unresolved inference rows.

The unresolved reason is:

```text
transported_deadline_invariant_not_derived
```

when two-sided PGS locks exist but no reviewed resolver is available.

## Known Invalid Rules

Do not restore these as live selection rules:

- fixed `isqrt(N) +/- radius` candidate generation;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive lock rounds that revisit the same reset endpoint;
- ranking by closeness to `isqrt(N)` as evidence of correctness;
- product closure as the PGS contraction rule.

The 50-bit true factor pair has valid PGSPG reset locks on both sides but raw
deadline margins `2` and `12`. Raw margin equality is therefore false as a
resolver.

## Arithmetic Boundary

The current interval-measurement backend is small-regime only.

Coordinates are carried as `gmpy2.mpz`, but divisor-count interval measurement
still calls the repository's NumPy-backed exact interval helper. The official
runner guards this boundary with:

```text
SMALL_REGIME_MAX_BITS = 50
```

Cases above that limit must return unresolved with:

```text
gmp_interval_backend_required
```

until a genuine GMP interval backend exists.

Do not describe the current runner as RSA-260-ready or GMP-only at the interval
backend level.

## Rung Extension Workflow

Rungs are data, not code.

Add public rungs to `ladder_spec.json`. Add audit endpoints separately to
`audit_spec.json` only when audit certification is available. The runner never
reads audit data.

Starting at RSA-100, use the public RSA Challenge moduli recorded in:

```text
RSA_PUBLIC_MODULI_THROUGH_260.md
```

The current runner will explicitly return unresolved for those larger rungs
until the GMP interval backend exists.

## Next Live Work

The next mathematical task is to derive the transported deadline invariant.

Raw local margins are not invariant under the public reciprocal map. The
resolver must compare reset/deadline state after transport, using public `N`,
PGSPG state, and floor-map geometry only.

Until that invariant is written down and reviewed, the correct output is
unresolved.
