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
-> public product closure / audit
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

PGS chamber logic can make the serious survivor set small. Reciprocal chamber
logic then asks whether both sides remain stable when each side is viewed as the
other side's implied cofactor. Product closure is the public certification step
after PGS has done the contraction.

## Factorizer Shape

The factorizer should be a survivor funnel:

1. Start from a public candidate band around `isqrt(N)`.
2. Apply public balance and wheel filters.
3. For each serious lower-side candidate, derive local PGSPG chamber state.
4. Map the candidate to its public reciprocal cofactor side by `N // x`.
5. Derive local PGSPG chamber state on the reciprocal side.
6. Keep candidates whose lower and upper chamber states are mutually stable.
7. Rank or reduce the survivor pairs.
8. Use public product closure only after the PGS survivor set exists.

The factorizer must never use a hand-authored PGS-state fixture containing
answer-bearing values. PGS state must be derived from public `N` and local
PGSPG machinery.

## Product Closure Role

Product closure is not hidden information. For a public RSA challenge, the
published modulus `N` is the object to be factored, and `p * q = N` is the final
certificate.

The boundary is:

```text
PGS inference contracts the candidate set.
Product closure certifies or ranks the tiny survivor set.
Audit verifies after selection.
```

Do not let product closure replace the PGS contraction step. Do not claim PGS
selected a pair if the code simply searched candidates until `p * q = N`.

## Metrics To Preserve

Every serious probe should report the funnel, not only final success:

| Metric | Meaning |
|---|---|
| initial candidate integers | public band size around `isqrt(N)` |
| post-balance candidates | public size/balance contraction |
| post-wheel candidates | wheel-open contraction |
| PGS chamber survivors | value added by PGSPG-derived local state |
| reciprocal-lock survivors | value added by two-sided stability |
| product-closed pairs | final public closure count |
| false rejects | whether true factors were eliminated before closure |
| factor rank | rank of the true factor pair among survivors |
| false survivor product error | separation between locally stable wrong pairs and true closure |

The target pattern is:

```text
many public candidates
-> few serious candidates
-> tiny PGS survivor set
-> unique product-closed pair
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
- public product closure after PGS survivor contraction.

Inference must not use:

- hidden factors;
- audit factors;
- hand-authored answer-bearing PGS-state rows;
- `gcd` as a selector;
- divisibility by `N` as the contraction method;
- factorization APIs;
- primality tests as the endpoint source;
- randomness;
- fallback search;
- silent widening or alternate paths.

If the PGS contraction does not produce a usable survivor surface, return an
explicit unresolved result.

## First Clean Milestone

Rebuild the 150-bit survivor funnel cleanly:

```text
public candidate band
-> balance + wheel
-> PGSPG-derived chamber state
-> PGS chamber / Rule X survivors
-> reciprocal chamber lock
-> product-closed survivor ranking
```

The first milestone is not RSA-260. It is a clean reproduction of the prior
toy-scale shape with mechanically derived PGS state and honest metrics.

Only after that surface is clean should the experiment scale upward.
