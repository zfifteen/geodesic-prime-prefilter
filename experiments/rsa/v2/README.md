# RSA v2 Strategy Memory For Codex

This file is for future Codex sessions working inside `experiments/rsa/v2`.
Read it as operational memory, not as a public README.

## Center Of Gravity

The active idea is a PGS Factorizer built from the already-working PGS Prime
Generator.

The PGS Prime Generator already implements the concepts needed by the factorizer:

- search intervals;
- wheel-open offsets;
- exact divisor-count interval state;
- GWR-selected integer structure;
- no-later-simpler-composite ceilings;
- search-interval reset;
- explicit unresolved state;
- downstream audit separation.

The factorizer is not a new mathematical engine from nothing. It is a two-sided
application of the PGSPG chamber-state machinery around `isqrt(N)`.

The high-level map is:

```text
public N
-> center at isqrt(N)
-> lower and upper chambers
-> PGSPG-derived chamber state on each side
-> reciprocal chamber-state compatibility
-> small survivor set
-> reciprocal deadline lock
-> downstream audit
```

## Strategy From Prior Progress

The useful prior result was a survivor funnel at toy RSA scale:

```text
2,097,755 candidate integers
-> 37 serious candidates after balance + wheel filtering
-> 2 survivors after PGS chamber + Rule X inference
-> no false rejects
-> true factor ranked first
```

The lesson is not to begin with product testing. The lesson is:

```text
A wrong candidate can be locally valid without being globally closed.
```

PGS chamber logic can make the serious survivor set small. Reciprocal deadline
logic then asks whether both sides preserve the same reset state when each side
is viewed through the public reciprocal map.

## Factorizer Shape

The factorizer should be a survivor funnel:

1. Start from a public candidate band around `isqrt(N)`.
2. Apply public balance and wheel filters.
3. For each serious ordered candidate, derive local PGSPG chamber state.
4. Map the candidate to its public reciprocal cofactor side by `N // x`.
5. Derive local PGSPG chamber state on the reciprocal side.
6. Keep candidates whose lower and upper chamber states are mutually stable.
7. Compare reset signatures, reset-deadline margins, and transported deadline widths.
8. Emit the unique unordered deadline-locked pair, or return unresolved.

The factorizer must never use a hand-authored PGS-state fixture containing
answer-bearing values. PGS state must be derived from public `N` and local
PGSPG machinery.

## Rung Extension Workflow

Rungs are data, not code.

Add public rungs to `ladder_spec.json`:

```json
{
  "case_id": "rsa_v2_50bit_static_001",
  "description": "50-bit ladder rung.",
  "N": "..."
}
```

Add audit endpoints separately to `audit_spec.json` when audit certification is
needed. The runner never reads `audit_spec.json`.

Do not add a branch to `run_experiment.py` for a new bit size. The same global
rule constants and the same solver functions must process every rung.

## Deadline Lock Role

The reciprocal deadline lock is the resolver.

The boundary is:

```text
PGS inference contracts the candidate set.
Deadline lock selects the unique unordered pair.
Audit verifies after selection using the separate audit file.
```

Do not let product closure replace the PGS contraction step. Do not claim PGS
selected a pair if the code simply searched candidates until multiplication
matched `N`.

## Metrics To Preserve

Every serious probe should report the funnel, not only final success:

| Metric | Meaning |
|---|---|
| initial candidate integers | public band size around `isqrt(N)` |
| post-balance candidates | public size/balance contraction |
| post-wheel candidates | wheel-open contraction |
| PGS chamber survivors | value added by PGSPG-derived local state |
| reciprocal-lock survivors | value added by two-sided stability |
| deadline-lock pairs | unique reciprocal reset-deadline locks |
| false rejects | whether true factors were eliminated before closure |
| factor rank | rank of the true factor pair among survivors |
| reset signature / margin / transported width | state fields that explain the lock |

The target pattern is:

```text
many public candidates
-> few serious candidates
-> tiny PGS survivor set
-> unique reciprocal deadline-lock pair
```

## Implementation Direction

Begin with documentation and a clean PGSPG-state adapter.

The first code layer should expose the chamber-state facts from
`src/python/z_band_prime_predictor/simple_pgs_generator.py` without changing the
minimal generator output contract.

Useful state fields include:

- `gap_offset`;
- `carrier_w`;
- `carrier_d`;
- `lock_carrier_offset`;
- `lock_carrier_d`;
- `lower_d_threat_offset`;
- `tail_after_reset_offsets`;
- resolved / unresolved / rejected candidate status.

Keep the production generator narrow. Add factorizer code under
`experiments/rsa/v2`, or add a small read-only adapter if shared code is needed.
Do not add factorization logic to the generator.

## Non-Negotiable Boundary

Inference may use:

- public `N`;
- `isqrt(N)`;
- public candidate-band parameters;
- balance and wheel filters;
- PGSPG-derived chamber state;
- reciprocal mapping by `N // x`;
- reciprocal reset-deadline transport.

Inference must not use:

- hidden factors;
- audit factors;
- hand-authored answer-bearing PGS-state rows;
- `gcd` as a selector;
- divisibility by `N` as the contraction method;
- product closure as the contraction method;
- factorization APIs;
- primality tests as the endpoint source;
- randomness;
- fallback search;
- silent widening or alternate paths.

If the deadline lock does not produce a unique unordered pair, return an
explicit unresolved result.

## First Clean Milestone

Rebuild the survivor funnel cleanly:

```text
public candidate band
-> balance + wheel
-> PGSPG-derived chamber state
-> PGS chamber / Rule X survivors
-> reciprocal chamber lock
-> reciprocal deadline lock
-> audit certification
```

The first milestone is the current 40-bit rung. It locks in machinery shape:
public case rows, global rule constants, mechanically derived PGS state, and
honest metrics.

Only after that surface is clean should the experiment scale upward.
