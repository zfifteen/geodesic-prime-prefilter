# PGS-GEOFAC Survivor-Chamber Conjecture

## Purpose

This note records the current RSA survivor-chamber experiment as implemented
under `experiments/rsa`.

The current target is not RSA-260 itself. The current target is a deterministic
RSA-like semiprime ladder from 60 through 180 bits. The experiment asks whether
PGS endpoint structure and Rule X can remove most post-wheel candidates without
testing divisibility by `N`.

The final arithmetic certificate remains separate. The inference script does
not store hidden factors and does not call `gcd(N, d)`.

## Current Algorithm

The current inference pipeline is:

```text
RSA-like semiprime N
-> deterministic candidate band around sqrt(N)
-> balance-band rejection
-> wheel admissibility on candidate and implied cofactor floor
-> batched PGS endpoint-state field
-> Rule X reciprocal endpoint compatibility
-> ranked survivor list
```

The downstream audit pipeline is:

```text
ranked survivor list
-> reveal hidden factors
-> measure false rejection
-> measure true-factor survivor rank
-> measure gcd checks before discovery
```

The side recursive-lock probe is:

```text
ranked survivor list
-> reciprocal chamber lock on d and q_floor
-> repeated endpoint reset signatures
-> product-error measurement
```

## Implemented Inference Rules

### Balance And Wheel

For each candidate `d`, the script computes `q_floor = N // d`.

The candidate is rejected if either side falls outside the configured balance
band or fails the fixed wheel admissibility test for primes `2, 3, 5, 7`.

### Batched PGS Endpoint Field

The endpoint stage no longer rebuilds a divisor-count chamber for each
candidate. It first gathers every candidate-side and cofactor-side integer that
survives balance and wheel rejection. It then builds a batched endpoint field
over the local PGS endpoint windows required by those integers.

With `PGS_ENDPOINT_TOLERANCE = 0`, a candidate side is compatible only when the
side itself is a PGS endpoint.

The probe now builds one exact divisor-count field over the union of endpoint
windows induced by the candidate surface. Every rung uses the same GMP-backed
arbitrary-precision divisor-field path. The emitted field
`endpoint_equivalence_failures` must remain `0`.

### Rule X Compatibility

For each side that survives endpoint compatibility, the script finds the
previous PGS endpoint anchor and applies the Rule X next-endpoint relation.

For every row, `rule_x_mode` is:

```text
batched_exact_gmp_chamber_reset
```

There is no separate high-value Rule X path. The probe builds previous-anchor
and chamber-reset divisor fields from the whole PGS survivor surface, then reads
Rule X answers from those fields. If Rule X does not resolve, the candidate is
counted under `rule_x_unresolved`; unresolved states are not counted as Rule X
passes.

## Current RSA-Like Ladder

The active ladder contains only RSA-like semiprimes:

```text
rsa_like_60bit_skew_14
rsa_like_80bit_skew_16
rsa_like_100bit_skew_18
rsa_like_125bit_skew_18
rsa_like_150bit_skew_20
rsa_like_180bit_skew_22
```

The balanced and older moderate-skew cases were removed from the forward test
surface so that the experiment measures RSA-like geometry only.

## Current Results

The latest inference and audit run reports:

| Case | Bits | Generated | Post-Wheel | PGS Rejects | Rule X Rejects | Rule X Unresolved | Resolved Survivors | Total Survivors | PGS Reduction | False Rejects | Factor Rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `rsa_like_60bit_skew_14` | 60 | 33,287 | 36 | 30 | 4 | 0 | 2 | 2 | 94.4444% | 0 | 1 |
| `rsa_like_80bit_skew_16` | 80 | 131,613 | 76 | 62 | 12 | 0 | 2 | 2 | 97.3684% | 0 | 1 |
| `rsa_like_100bit_skew_18` | 100 | 524,935 | 78 | 60 | 12 | 0 | 6 | 6 | 92.3077% | 0 | 1 |
| `rsa_like_125bit_skew_18` | 126 | 524,845 | 76 | 52 | 22 | 0 | 2 | 2 | 97.3684% | 0 | 1 |
| `rsa_like_150bit_skew_20` | 150 | 2,097,755 | 37 | 22 | 13 | 0 | 2 | 2 | 94.5946% | 0 | 1 |
| `rsa_like_180bit_skew_22` | 180 | 8,389,175 | 36 | 16 | 18 | 0 | 2 | 2 | 94.4444% | 0 | 1 |

The strongest supported result is:

```text
On the current RSA-like 60-180 bit ladder, PGS endpoint inference plus Rule X
removes 92.3077% to 97.3684% of post-wheel candidates, with zero false
rejections and true-factor survivor rank 1 in every tested case.
```

For the 150-bit row:

```text
generated candidates:     2,097,755
post-wheel candidates:    37
PGS chamber rejects:      22
Rule X rejects:           13
Rule X unresolved:        0
resolved survivors:       2
total survivors:          2
PGS reduction:            94.5946%
false rejects:            0
factor rank:              1
```

For the 180-bit row:

```text
generated candidates:     8,389,175
post-wheel candidates:    36
PGS chamber rejects:      16
Rule X rejects:           18
Rule X unresolved:        0
resolved survivors:       2
total survivors:          2
PGS reduction:            94.4444%
false rejects:            0
factor rank:              1
```

The 180-bit row now preserves the same shape as the lower rungs: two survivors,
zero false rejections, true-factor rank 1, and no unresolved Rule X states.

## Backend Accounting

The latest summary includes explicit mode and equivalence fields:

| Case | Endpoint Mode | Rule X Mode | Endpoint Values | Endpoint Equivalence Failures |
|---|---|---|---:|---:|
| `rsa_like_60bit_skew_14` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 36 | 0 |
| `rsa_like_80bit_skew_16` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 76 | 0 |
| `rsa_like_100bit_skew_18` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 78 | 0 |
| `rsa_like_125bit_skew_18` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 76 | 0 |
| `rsa_like_150bit_skew_20` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 38 | 0 |
| `rsa_like_180bit_skew_22` | `batched_exact_gmp_divisor_field` | `batched_exact_gmp_chamber_reset` | 36 | 0 |

This closes the earlier implementation issue where a bounded high-value bridge
made lower and higher rows non-comparable.

## Reciprocal Chamber Lock

Product-closed reciprocal chamber lock is not part of the main inference
ladder. It is a kitchen side probe only.

The reason is direct: product closure tests whether a survivor pair actually
multiplies back to `N`. That is a concrete arithmetic certificate of the
factor pair, not the same class of operation as PGS endpoint inference or Rule
X rejection. It belongs outside the clean inference/elimination test surface.

The side probe lives under `kitchen`:

```text
experiments/rsa/kitchen/reciprocal_chamber_lock_probe.py
```

Future side probes should also live under:

```text
experiments/rsa/kitchen
```

Kitchen output from reciprocal chamber lock must not be reported as main ladder
inference performance. It can be used to develop the next algorithmic target,
but the clean ladder result stops at the ranked survivor list.

## Current Conjecture

For RSA-like semiprimes, post-wheel survivors do not behave as independent
candidate integers. They behave as paired local chambers constrained by both
PGS endpoint structure and the global product relation.

The current conjecture is:

```text
PGS endpoint compatibility plus Rule X can reduce the post-wheel survivor set
to a tiny reciprocal chamber without testing divisibility by N.
```

In short:

```text
local endpoint stability is necessary
product closure is a separate certification-side pressure test
```

## Next Algorithmic Target

The next side-probe target is to derive a recursive PGS reduction rule that
reduces the survivor chamber further without using product closure as a
selection condition:

```text
PGS survivors
-> recursive endpoint-state inference
-> survivor-chamber contraction
-> one orientation pair or an explicit unresolved state
```

The decision rule is:

```text
A survivor remains alive only if the next inferred PGS state remains compatible
on both sides of the reciprocal chamber.
```

The immediate success criterion for the next ladder expansion is:

```text
recursive PGS-only reduction lowers survivor counts without increasing false
rejections and without using hidden factors, gcd checks, divisibility checks,
or product-closure checks as inference rules.
```

## Falsification Conditions

The current conjecture weakens if any of the following occur:

- a hidden factor is rejected by balance, wheel, PGS endpoint inference, or
  Rule X;
- endpoint equivalence failures become nonzero;
- unresolved Rule X states grow faster than the resolved survivor chamber can
  control;
- survivor counts grow faster than post-wheel PGS reduction can control as bit
  length and skew increase.

The conjecture fails for the current implementation if the audit reports any
false rejection on the RSA-like ladder.

## Artifact Map

| File | Role |
|---|---|
| `experiments/rsa/run_inference_elimination_probe.py` | Main inference-only survivor funnel. |
| `experiments/rsa/audit_inference_elimination_probe.py` | Separate downstream audit using hidden factors. |
| `experiments/rsa/kitchen/reciprocal_chamber_lock_probe.py` | Kitchen side probe for recursive reciprocal chamber lock. |
| `experiments/rsa/inference_elimination_probe.csv` | Latest inference summary. |
| `experiments/rsa/inference_elimination_survivors.jsonl` | Latest ranked survivor rows. |
| `experiments/rsa/inference_elimination_audit.csv` | Latest downstream audit results. |
| `experiments/rsa/kitchen/reciprocal_chamber_lock_details.csv` | Latest kitchen lock detail rows. |
| `experiments/rsa/kitchen/reciprocal_chamber_lock_summary.csv` | Latest kitchen lock summary rows. |
