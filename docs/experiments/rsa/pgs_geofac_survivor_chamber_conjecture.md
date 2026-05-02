# PGS-GEOFAC Survivor-Chamber Conjecture

## Purpose

This note records a working conjecture for applying the repository's PGS
inference laws, together with GEOFAC, Z5D, and phi-harmonic filtering ideas, to
RSA challenge semiprime factor search.

The goal is not to replace the final arithmetic certificate. The goal is to
replace as many candidate divisibility checks as possible with deterministic
inference before exact `gcd(N, d)` certification.

## Conjecture

For RSA-style semiprimes `N = p*q`, factor search can be compressed by treating
candidate factors not as isolated divisibility guesses, but as members of local
prime-pair chambers.

A candidate should survive only if it passes deterministic geometric
feasibility filters and its implied factor region remains compatible with PGS
endpoint inference on both sides.

In operational form:

```text
candidate generation
-> geometric invalid-candidate rejection
-> wheel and residue admissibility
-> PGS chamber endpoint inference
-> GEOFAC/Z5D survivor ranking
-> exact gcd certification on the final ranked survivors
```

The conjecture is that this pipeline can replace most concrete divisibility
checks with deduction. The final `gcd(N, d)` remains the certificate, but it is
applied only after the candidate has survived geometric feasibility, residue
admissibility, and PGS chamber closure.

## Two Component Insights

### Survivor Rank Conservation

Filters are valuable only if they preserve the hidden factor. Rankers are
valuable only after unsafe or impossible candidates have been removed.

The target metric is not standalone filter rejection or standalone rank
quality. The target metric is the rank of the true factor among survivors.

### Prime-Pair Chamber Collapse

A candidate divisor implies a paired cofactor region. Instead of testing each
candidate directly, infer whether both sides can close as lawful PGS prime
endpoints.

Nonfactor regions should collapse before divisibility because their local
chamber forces endpoint structure incompatible with `N = p*q`.

## Core Claim

There exists a deterministic survivor funnel for RSA challenge semiprimes in
which most GEOFAC, Z5D, phi-harmonic, and wheel-admissible candidates can be
rejected without trial division by showing that their implied prime-pair chamber
cannot close under PGS endpoint rules.

## Proposed Replay Metric

For known RSA challenge numbers, hide the factors during candidate generation,
filtering, and ranking. Reveal the factors only for downstream measurement.

Measure:

```text
N
known p, q hidden from pipeline
generated candidates
rejected by balance band
rejected by wheel
rejected by PGS chamber collapse
ranked survivors
true factor survivor rank
gcd checks before discovery
compression ratio
```

The replay target is:

```text
true_factor_survival = 100%
median survivor rank after PGS chamber collapse <= 10^6
worst survivor rank after PGS chamber collapse <= 10^8
gcd checks reduced by at least 10^3 relative to naive survivor scan
```

## Falsification Conditions

If any known RSA factor is rejected by a deterministic filter or PGS chamber
rule, that rule is invalid for RSA-260 and must be weakened or removed.

If the true factors survive but their survivor ranks remain too high, then the
conjecture's safety part holds but the feasibility part fails.

If PGS chamber collapse removes few candidates after wheel and geometric
filtering, then the conjecture does not provide meaningful additional
compression beyond known filters.

## Development Target

The next artifact should be a deterministic replay harness over known RSA
challenge numbers from RSA-100 through RSA-250.

The harness should preserve the generator discipline used elsewhere in this
repository:

- no randomness when deterministic construction is possible;
- no fallback factorization path;
- no hidden use of the known factors during generation, filtering, or ranking;
- exact `gcd(N, d)` only as the final arithmetic certificate;
- downstream audit only after the candidate pipeline has emitted its ranked
  survivor list.

The conjecture matures if replay shows that PGS chamber collapse removes large
blocks of candidates while preserving hidden factors across RSA-100 through
RSA-250.
