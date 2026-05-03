# RSA v2 Metrics Contract

The live runner reports the PGS-first reciprocal anchor surface. It does not
claim a resolved factor pair.

## Required Summary Fields

Each run writes `summary.json` with one row per public case.

| Field | Meaning |
|---|---|
| `case_id` | Public case identifier |
| `bits` | Public modulus bit size |
| `N` | Public modulus |
| `balance_band` | Global balance-band constant |
| `center` | `isqrt(N)`, used for orientation only |
| `balance_lower` | Lower public balanced endpoint |
| `balance_upper` | Upper public balanced endpoint |
| `max_lower_endpoints` | Endpoint-walk budget from the square-root side |
| `lower_pgs_endpoints_seen` | Count of lower endpoints measured by the walk |
| `lower_endpoint_walk_budget_exhausted` | Whether the walk stopped by budget before the lower balance edge |
| `lowest_endpoint_seen` | Leftmost endpoint reached by the walk |
| `reciprocal_balance_rows` | Transported rows whose `floor(N / x)` is on the upper balanced side |
| `reciprocal_wheel_rows` | Transported rows open under the fixed 30-wheel |
| `reciprocal_endpoint_rows` | Rows where both sides are endpoints |
| `upper_locked_rows` | Rows where the upper endpoint is a PGSPG reset endpoint |
| `two_sided_pgs_lock_rows` | Rows where both endpoints are PGSPG reset endpoints |
| `ordered_survivors` | Ordered two-sided PGS lock rows |
| `unordered_survivors` | Canonical unordered two-sided PGS lock pairs |
| `resolver_status` | Current resolver state |
| `rule_id` | Surface rule identifier |

## Required Survivor Fields

Each survivor row records a two-sided PGSPG reset lock:

- `case_id`;
- `rank`;
- `x`;
- `y`;
- previous endpoint on each side;
- reset endpoint on each side;
- carrier state on each side;
- tail and threat fields on each side;
- reset-deadline value and margin on each side;
- transported reset-to-deadline widths;
- `resolver_status`.

Survivor rows may contain final candidate values because they are emitted by
public inference. They must not contain audit-only labels or audit status.

## Resolver Status

The live resolver status is:

```text
transported_deadline_invariant_not_derived
```

This means the PGS surface exists but the final selection invariant is not yet
reviewed.

## Ranking

Rank rows deterministically for reproducibility.

The current rank key is distance from `isqrt(N)`, then lower coordinate. This
ordering is not evidence of correctness. It is only a stable display order.

## Acceptance For Current V2

The current v2 surface is acceptable if:

1. inference reads only public case rows;
2. PGS state is derived by code;
3. fixed-radius candidate-band metrics are absent;
4. stationary recursive-lock metrics are absent;
5. raw deadline-margin equality is not used as a resolver;
6. the runner returns unresolved until the transported invariant is derived;
7. audit remains physically separate;
8. all text artifacts use LF line endings.

## Scaling Signal

The current runner is not RSA-260-ready. It has a small-regime exact interval
backend.

The next scaling signal is a GMP interval backend that preserves the same
surface fields without changing selection logic.
