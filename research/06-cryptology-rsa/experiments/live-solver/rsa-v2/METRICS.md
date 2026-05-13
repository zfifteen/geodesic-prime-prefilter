# RSA v2 Metrics Contract

The live runner reports one reciprocal PGSPG certificate pair per public case.
It does not claim a resolved factor. It emits public endpoint classes, and
downstream audit reports whether at least one emitted endpoint is a factor.

## Required Summary Fields

Each run writes `summary.json` with one row per public case.

| Field | Meaning |
|---|---|
| `case_id` | Public case identifier |
| `bits` | Public modulus bit size |
| `N` | Public modulus |
| `center` | `isqrt(N)`, used for orientation only |
| `balance_band` | Global balance-band constant |
| `closure_status` | Certificate-pair result state |
| `lower_certificate_present` | Whether the lower PGSPG certificate exists |
| `upper_certificate_present` | Whether the upper PGSPG certificate exists |
| `corrected_lower_certificate_present` | Whether deadline correction derived a lower PGSPG certificate |
| `rule_id` | Certificate-pair rule identifier |

## Required Survivor Fields

Each survivor row records a public certificate pair:

- `case_id`;
- `bits`;
- `N`;
- `closure_status`;
- transported reset endpoints;
- corrected lower and upper deadline endpoints when present;
- transported corrected endpoints when present;
- transported reset-to-deadline widths;
- lower certificate fields;
- upper certificate fields when present;
- corrected-lower certificate fields when present;
- `rule_id`.

Survivor rows may contain public reset endpoints because inference derived
them. They must not contain audit-only labels or audit status.

## Closure Status

Resolved closure states are:

```text
endpoint_class_by_mutual_certificate_closure
endpoint_class_by_reciprocal_deadline_signature_correction
endpoint_class_by_oriented_endpoint_chain_closure
```

The current unresolved statuses are:

```text
unresolved_by_certificate_pair_not_closed
unresolved_by_reset_endpoint_crosses_orientation
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
```

These mean public PGSPG state did not close before the deterministic stop
condition.

## Acceptance For Current V2

The current v2 surface is acceptable if:

1. inference reads only public case rows;
2. PGS state is derived by code;
3. fixed-radius candidate-band metrics are absent;
4. endpoint-budget metrics are absent;
5. stationary recursive-lock metrics are absent;
6. raw deadline-margin equality is not used as a resolver;
7. product closure is not used as a resolver;
8. the runner returns unresolved when certificate closure fails;
9. audit remains physically separate;
10. all text artifacts use LF line endings.

## Scaling Signal

The current runner is not RSA-260-ready. It has a small-regime exact interval
backend.

The next scaling signal is a GMP interval backend that preserves the same
certificate fields without changing selection logic.
