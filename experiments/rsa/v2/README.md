# RSA v2 Strategy Memory For Codex

This file is operational memory for future Codex sessions working inside
`experiments/rsa/v2`. It is written for Codex, not as a package README.

For a fresh session, start with:

```text
SESSION_BOOTSTRAP.md
```

## Current State

The live v2 runner is a reciprocal PGSPG certificate-pair probe.

It does not claim to solve the ladder. It derives one public lower PGSPG reset
certificate, transports that reset endpoint through `floor(N / x)`, derives the
opposite-side certificate from the transported coordinate, and returns
unresolved unless the two certificates close under the reciprocal map.

This replaced two invalid solver shapes:

- a fixed additive chamber around `isqrt(N)`;
- a budgeted walk through many lower endpoints.

The square root is now an orientation coordinate only. It does not define a
candidate chamber, and it does not limit the possible factor distance.

## Live Front Door

The live front door is:

```text
public N
-> isqrt(N) as orientation
-> previous public endpoint before isqrt(N)
-> PGSPG reset certificate on the lower side
-> y = floor(N / lower.reset_endpoint)
-> previous public endpoint before y
-> PGSPG reset certificate on the upper side
-> reciprocal certificate-closure check
-> resolved only if the public certificates mutually close
```

The runner never reads audit factors.

## PGSPG Concepts Carried Forward

The factorizer uses the PGS Prime Generator as the local state engine:

- public endpoint anchors;
- wheel-open offsets;
- exact divisor-count interval state;
- GWR carrier state;
- chamber reset;
- tail and threat reset-deadline fields;
- explicit unresolved states.

The factorizer does not place factorization logic inside the generator. It calls
the generator's chamber-reset certificate as a read-only local state adapter.

## Current Output

For each public `N`, the runner writes:

- `inference_rows.jsonl`;
- `survivor_rows.jsonl`;
- `summary.json`.

The current 40-bit and 50-bit rungs both return:

```text
unresolved_by_certificate_pair_not_closed
```

That is the correct state. The previous 40-bit resolution depended on a
close-factor assumption and is no longer part of the live experiment.

## Invalid Rules

Do not restore these as live selection rules:

- fixed `isqrt(N) +/- radius` candidate generation;
- endpoint-walk budgets as solver coverage;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive lock rounds that revisit the same reset endpoint;
- ranking by closeness to `isqrt(N)` as evidence of correctness;
- product closure as the PGS contraction rule.

## Arithmetic Boundary

The current interval-measurement backend is small-regime only.

Coordinates are carried as `gmpy2.mpz`, but divisor-count interval measurement
still calls the repository's current exact interval helper. The official runner
guards this backend boundary with:

```text
SMALL_REGIME_MAX_BITS = 50
```

Cases above that limit return:

```text
gmp_interval_backend_required
```

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

The current runner will explicitly return unresolved for larger rungs until a
GMP interval backend exists.

## Next Live Work

The next mathematical task is to derive a stronger transported certificate
invariant from the PGSPG fields already emitted in `survivor_rows.jsonl`.

Until that invariant is written down and reviewed, the correct output is
unresolved.

Before substantial implementation, use the continuity and shape contract:

```text
docs/research/codex_continuity/continuity_and_shape_contract.md
```

The canonical repository bootstrap is:

```text
docs/research/codex_continuity/START_HERE.md
```

For this experiment, Grok should be used as research pressure before major rule
changes, with code, outputs, failed assumptions, and current hypotheses included
in the prompt.

Record substantial Grok collaborations in:

```text
experiments/rsa/v2/grok_sessions/
```
