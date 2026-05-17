# Directed Transport Audit

## Purpose

This note addresses the first proof obligation in the zero-defect theorem
target:

```text
right endpoint movement at p and q
    -> directed outward movement of pq
    -> public containing-gap boundary class
```

The audit is not a factor-recovery method and not the endpoint exclusion rule.
It checks the arithmetic bridge that makes directed endpoint gaps relevant to
the public gap containing `N`.

## Transport Formula

Let:

```text
N = pq
```

Let `a` be the first right-following wheel-open offset after `p`, and let `b`
be the first right-following wheel-open offset after `q`.

The endpoint residue modulo `30` fixes the first right-open offset:

| endpoint residue mod 30 | first right-open offset |
| ---: | ---: |
| `1` | `6` |
| `7` | `4` |
| `11` | `2` |
| `13` | `4` |
| `17` | `2` |
| `19` | `4` |
| `23` | `6` |
| `29` | `2` |

Then the first directed outward movements transport through multiplication as:

```text
(p + a)q - pq = aq
p(q + b) - pq = bp
(p + a)(q + b) - pq = aq + bp + ab
```

These are the three public-side movements induced by the two right-following
factor endpoint gaps.

## Zero-Defect Boundary

The right-boundary defect is:

```text
right_boundary_defect =
    max(rank(p_right_residue), rank(q_right_residue)) - rank(o4)
```

Measured over observed at-winner rows from the current six bands:

| right-boundary defect | observed at-winner rows |
| ---: | ---: |
| `-1` | `4865` |
| `0` | `13029` |
| `+1` | `13785` |

Total:

```text
observed_at_winner_row_count = 31679
distinct_transport_key_count = 55
right_step_endpoint_residue_mismatch_count = 0
transport_balance_counts:
    shortfall_below_4 = 4865
    middle_4_balance = 13029
    overshoot_above_4 = 13785
```

## Boundary

This audit confirms the arithmetic transport object. It also sharpens the
claim boundary.

Observed true factor pairs under the public at-winner condition include all
three defect classes:

```text
defect = -1
defect = 0
defect = +1
```

Therefore the zero-defect law is not:

```text
all true factor pairs under public_at_winner have defect = 0
```

The measured rule is narrower and stronger:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and right_boundary_defect(E) = 0
    -> exclude E
```

The theorem must explain why zero defect stabilizes absence in endpoint space,
while nonzero defects can still occur as observed factor-pair states and can
leak back into the candidate surface.

## Reproduction

Run:

```text
python3 directed_transport_audit.py
```

Primary outputs:

```text
output/directed_transport_audit/summary.json
output/directed_transport_audit/transport_rows.jsonl
output/directed_transport_audit/defect_count_rows.jsonl
```
