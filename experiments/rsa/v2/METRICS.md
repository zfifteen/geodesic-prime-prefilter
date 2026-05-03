# RSA v2 Metrics Contract

The factorizer must report the survivor funnel. A final resolved pair without
stage counts is not enough.

## Required Summary Fields

Each run should produce `summary.json` with these fields:

| Field | Meaning |
|---|---|
| `case_id` | Public case identifier |
| `bits` | Declared modulus bit size |
| `radius` | Global full-chamber radius used by the solver |
| `balance_band` | Global balance-band constant used by the solver |
| `initial_candidate_integers` | Count in `[isqrt(N) - radius, isqrt(N) + radius]` |
| `post_balance_candidates` | Count after balance filtering |
| `post_wheel_candidates` | Count after lower and upper wheel filtering |
| `reciprocal_window_candidates` | Count whose `N // x` lands in the full public chamber |
| `recursive_lock_survivors` | Count after reciprocal recursive lock |
| `ordered_survivors` | Count of ordered survivor pairs |
| `unordered_survivors` | Count of canonical unordered survivor pairs |
| `deadline_lock_ordered_rows` | Count of ordered rows satisfying reciprocal deadline lock |
| `deadline_lock_pairs` | Count of unordered reciprocal deadline-lock pairs |
| `rule_id` | Resolver rule identifier |

## Required Survivor Fields

Each survivor row should include:

- `case_id`;
- `rank`;
- `x`;
- `y`;
- PGS chamber status for `x`;
- PGS chamber status for `y`;
- recursive lock round count;
- reset signatures;
- reset-deadline margins;
- transported reciprocal deadline widths;
- deadline-lock status and reason.

The survivor rows may contain final candidate values. They must not contain
audit-only factors unless those values were emitted by inference.

## Ranking

Rank survivors deterministically.

The first rank key is symmetric distance from `isqrt(N)`. The second rank key is
the lower coordinate. This preserves the prior survivor-funnel convention and
makes repeated runs reproducible.

## Acceptance For 40-Bit V1

The 40-bit v1 milestone succeeds if:

1. inference reads only the public case file;
2. PGS state is derived by code;
3. the run reports the full funnel;
4. the recursive lock produces a reviewable survivor surface;
5. the reciprocal deadline lock reduces the 40-bit ordered surface to two rows;
6. audit confirms the emitted pair;
7. all artifacts use LF line endings.

If any condition fails, the milestone is not complete.

## Scaling Signal

The 40-bit result is not RSA-260 evidence by itself.

It is a machinery lock-in result. The important scaling signal is whether the
same code path can report:

```text
many public candidates
-> few serious candidates
-> tiny PGS survivor set
-> unique reciprocal deadline-lock pair
```

without changing arithmetic libraries or adding branch-specific logic.
