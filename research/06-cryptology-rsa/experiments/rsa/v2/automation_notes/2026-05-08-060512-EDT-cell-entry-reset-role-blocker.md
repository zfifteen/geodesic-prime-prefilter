# RSA v2 Automation Note: Cell-Entry Reset-Role Blocker

Run time: 2026-05-08 06:05:12 EDT.

## Baseline Reproduced

Commands run:

```text
python3 research/06-cryptology-rsa/experiments/rsa/v2/build_ladder_fixtures.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/audit_experiment.py
pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
```

Baseline result:

```text
rsa_v2_40bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_40bit_static_001 integrity_pass inference_audit_fail
rsa_v2_50bit_static_001 integrity_pass inference_audit_fail
44 passed in 24.26s
```

The 40-bit and 50-bit rungs remain honestly unresolved.

## Grok Prompt And Response Summary

Orientation prompt:

```text
Confirm the RSA v2 frame: public N only; reciprocal PGSPG reset certificates;
no hidden factors, audit factors, divisibility, gcd, product closure,
factor APIs, primality APIs, fixed-radius chambers, endpoint budgets,
per-rung special cases, randomness, or fallback paths.
```

Grok acknowledged the frame and requested the exact proposed invariant before
technical review.

Technical prompt:

```text
For a PGSPG certificate C, define r(C)=reset_endpoint and
d(C)=reset_deadline_value. Define the public transported reset-to-deadline
cell I_N(C)=[floor(N / d(C)), floor(N / r(C))].

Ask whether a reciprocal pair can be promoted only if r(C_u) lies in I_N(C_l)
and r(C_l) lies in I_N(C_u), with both endpoints produced as live PGSPG reset
endpoints from the single public derivation path.
```

Grok first classified the cell-membership check as a valid public PGS blocker
and suggested adding it as an eligibility guard.

Follow-up prompt:

```text
The public 512-row transported-debt sidecar shows broad reset-endpoint
cell-membership would exclude many ledger-effective survivor rows:
40-bit effective outside/missing = 95 / 109;
50-bit effective outside/missing = 93 / 93.

Should this be recorded only as an official-orientation blocker, not as a
general frontier guard or resolver predicate?
```

Grok agreed: record the distinction as a blocker note and do not implement
cell membership as a frontier guard or resolver predicate.

## Novel Insight Candidate

The transported coordinate and the induced PGSPG reset role are different
public objects.

`T_N(r(C)) = floor(N / r(C))` is the entry coordinate of the transported
reset-to-deadline cell. The subsequent operation
`previous_endpoint(T_N(r(C))) -> pgs_certificate(anchor)` may produce a reset
endpoint outside that transported cell. That jump is PGSPG-local state on the
target side, not proof that the target reset endpoint inherits the source
cell-entry role.

Falsifiable rule:

```text
If transported reset-role inheritance is valid, then induced reset endpoints
should remain inside the source transported reset-to-deadline cell on the
public transported surface.
```

Disconfirmation:

```text
A public transported row where T_N(r(C)) lies in I_N(C), but the induced
PGSPG reset endpoint lies outside I_N(C), shows that cell entry and reset role
cannot be identified without an additional PGSPG theorem.
```

The current artifacts contain that disconfirmation.

## Invariant Tested

For each source certificate:

```text
I_N(C) = [floor(N / d(C)), floor(N / r(C))]
```

Tested condition:

```text
induced_reset_endpoint in I_N(C)
```

Official orientation rows:

```text
40-bit lower cell = [1048573, 1048574]
40-bit upper reset = 1048583
contained = false

40-bit upper cell = [1048559, 1048564]
40-bit lower reset = 1048573
contained = false

40-bit transported_upper_endpoint = 1048574
lower cell-entry contained = true

50-bit upper certificate = missing
50-bit transported_upper_endpoint = 32053634
lower cell-entry contained = true
```

Public transported-debt sidecar:

```text
40-bit rows = 256
40-bit induced reset contained = 21
40-bit outside or missing = 235
40-bit ledger-effective rows = 109
40-bit ledger-effective contained = 14
40-bit ledger-effective outside or missing = 95

50-bit rows = 256
50-bit induced reset contained = 0
50-bit outside or missing = 256
50-bit ledger-effective rows = 93
50-bit ledger-effective contained = 0
50-bit ledger-effective outside or missing = 93
```

## Result

The candidate is a valid blocker for the official orientation row, not a valid
resolver rule.

The tested data separates three facts:

```text
1. The transported cell-entry coordinate is public and lies in I_N(C).
2. The induced target PGSPG reset endpoint can lie outside I_N(C).
3. Broad reset-endpoint cell containment would reject many measured
   ledger-effective transported-story rows.
```

Therefore the current 40-bit row must remain unresolved. Promoting the induced
upper reset endpoint as though it were the lower transported cell entry would
identify two different public roles without a PGSPG theorem.

## Files Changed

```text
research/06-cryptology-rsa/experiments/rsa/v2/AGENTS.md
research/06-cryptology-rsa/experiments/rsa/v2/automation_notes/2026-05-08-060512-EDT-cell-entry-reset-role-blocker.md
```

`AGENTS.md` was restored from the main checkout because this worktree was
missing the local contract file required by the run request and by
`research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py`.

No resolver code was changed.

## Tests Run

```text
python3 research/06-cryptology-rsa/experiments/rsa/v2/build_ladder_fixtures.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/audit_experiment.py
pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
```

## Next Blocker

Derive a PGSPG theorem that transports commitment roles, not just coordinates.

The next rule must explain when a target-side PGSPG reset endpoint inherits a
source transported cell role after `previous_endpoint(T_N(r(C)))`. Without
that theorem, `T_N(r(C))` remains a cell-entry coordinate and the induced reset
endpoint remains target-local PGSPG state.
