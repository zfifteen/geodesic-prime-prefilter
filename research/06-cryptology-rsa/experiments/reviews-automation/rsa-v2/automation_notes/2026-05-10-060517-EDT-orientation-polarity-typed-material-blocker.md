# 2026-05-10 06:05:17 EDT: Orientation Polarity And Typed-Material Blocker

## Baseline Reproduced

Commands run:

```bash
python3 research/06-cryptology-rsa/experiments/rsa/v2/build_ladder_fixtures.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/audit_experiment.py
pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
```

Official inference remains unresolved:

```text
rsa_v2_40bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 unresolved unresolved_by_certificate_pair_not_closed
```

Audit output:

```text
rsa_v2_40bit_static_001 integrity_pass inference_audit_fail
rsa_v2_50bit_static_001 integrity_pass inference_audit_fail
```

Focused test suite:

```text
44 passed in 23.42s
```

Regenerated transported-story sidecar:

```bash
python3 research/06-cryptology-rsa/experiments/rsa/v2/transported_story_law_probe.py \
  --cases research/06-cryptology-rsa/experiments/rsa/v2/fixtures/ladder_cases.jsonl \
  --measured-rows 256 \
  --recursive-depth 4 \
  --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current
```

Sidecar summary:

```text
row_count = 512
ledger_eliminated_count = 110
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
falsification_status = passed
```

## Grok Prompt And Response Summary

Orientation round prompt:

```text
PGS RSA v2 uses public N only, PGSPG reset certificates, reciprocal floor
transport T_N(x)=floor(N/x), and strict mutual certificate closure. It forbids
hidden factors, audit factors, divisibility, gcd, product closure, factor APIs,
primality APIs, fixed-radius chambers, endpoint budgets, per-rung special
cases, randomness, and fallback paths. Current 40-bit and 50-bit rungs remain
unresolved. A transported-story sidecar collapses recursively but is measured
evidence only, not resolver code. Acknowledge the frame before technical review.
```

Grok acknowledged the frame and asked for no additional context.

Technical prompt supplied:

```text
Code excerpt from certificate_pair:
  center = isqrt(N)
  lower = pgs_certificate(previous_endpoint(center))
  transported_upper = floor(N / lower.reset_endpoint)
  if transported_upper < center or transported_upper > upper_balance:
      return unresolved with no upper certificate
  upper = pgs_certificate(previous_endpoint(transported_upper))
  closed iff transported_upper == upper.reset_endpoint,
            transported_lower == lower.reset_endpoint,
            lower.reset_signature == upper.reset_signature

40-bit official row:
  center=1048573
  lower_reset=1048573
  transported_upper=1048574
  upper_reset=1048583
  transported_lower=1048564
  unresolved_by_certificate_pair_not_closed

40-bit story row:
  source_anchor=1048571
  induced_anchor=1048573
  induced_carrier=1048574
  induced_carrier_in_prefix_zone=true
  induced_carrier_in_suffix_zone=true
  ledger_eliminated=true
  ledger_effective_survivor=false

50-bit official row:
  center=32053641
  lower_reset=32053649
  transported_upper=32053634
  upper_anchor=null
  unresolved_by_certificate_pair_not_closed

50-bit story row:
  source_anchor=32053639
  induced_anchor=32053631
  ledger_eliminated=false
  frontier_new_transport_state=true
  ledger_effective_survivor=true

Review whether this should remain a blocker note rather than resolver code.
Look for hidden classical shortcuts, false-resolution risk, and falsification
tests.
```

Grok's technical response:

```text
The proposed framing should remain a blocker note rather than resolver code.
The 40-bit case triggers typed-material exclusion. The 50-bit case fails
opposite-side polarity before an upper certificate is generated. No hidden
classical shortcut is present in the supplied frame. The risk is relaxing
typed-material exclusion or treating sidecar counts as a theorem.
```

Grok suggested adding assertions or header prose, but this run does not make
resolver or source-code changes because the tested condition remains a blocker,
not a valid public closure rule.

## Novel Insight Candidate

Prior measured work treated frontier freshness, recurrence, typed material, and
same-side induced rows as related bookkeeping around one transported story
surface. The sharper candidate is a two-axis validity gate:

```text
P = opposite-side orientation polarity:
    floor(N / source_reset_endpoint) lies strictly across isqrt(N)

M = transported material contact:
    induced state is prefix, suffix, or threat material under the public
    transported-story predicates
```

Candidate decision rule:

```text
Public certificate closure requires P=true and M=false before recursive
frontier evidence is allowed to matter. P=true alone does not resolve. M=false
alone does not resolve. A sidecar survivor with P=false is same-side material
for the official front door and cannot create an upper certificate.
```

Falsification condition:

```text
A public mutual certificate closure with P=false, or with M=true, falsifies the
gate. A valid PGSPG theorem proving that same-side induced certificates can
serve as opposite-side certificates would also falsify the polarity blocker.
```

This is a blocker-framing invariant, not a resolver.

## Invariant Tested

Tested on the regenerated 512 public transported-story rows:

```text
material_with_opposite = 110
material_without_opposite = 0
effective_with_opposite = 201
effective_without_opposite = 1
effective_material_overlap = 0
eliminated_without_material = 0
stale_with_opposite_nonmaterial = 200
```

Per-rung partition:

```text
40-bit:
  P=true,  M=false, effective=false: 94
  P=true,  M=false, effective=true:  109
  P=true,  M=true,  effective=false: 53

50-bit:
  P=false, M=false, effective=true:  1
  P=true,  M=false, effective=false: 106
  P=true,  M=false, effective=true:  92
  P=true,  M=true,  effective=false: 57
```

Official source rows:

```text
40-bit:
  source_anchor=1048571
  source_transport_reset_image=1048574
  P=true
  M=true
  ledger_eliminated=true
  ledger_effective_survivor=false
  induced_carrier_in_prefix_zone=true
  induced_carrier_in_suffix_zone=true

50-bit:
  source_anchor=32053639
  source_transport_reset_image=32053634
  P=false
  M=false
  ledger_eliminated=false
  ledger_effective_survivor=true
  induced_carrier_in_prefix_zone=false
  induced_carrier_in_suffix_zone=true
```

## Result

The current artifacts support a blocker, not a resolver.

The 40-bit official transport crosses the square-root orientation, but the
induced carrier is transported material in both prefix and suffix zones. That
state is eliminated by the public sidecar predicates and must not be promoted
without a new PGSPG theorem.

The 50-bit official transport does not cross the square-root orientation:

```text
floor(N / lower_reset_endpoint) = 32053634 < center = 32053641
```

Therefore the official runner correctly reports no upper certificate. The
sidecar's same-side induced row is useful evidence, but it is not the
opposite-side certificate required by the live algorithm.

## Files Changed

Code changes:

```text
none
```

Research and generated artifacts changed:

```text
research/06-cryptology-rsa/experiments/rsa/v2/AGENTS.md
research/06-cryptology-rsa/experiments/rsa/v2/automation_notes/2026-05-10-060517-EDT-orientation-polarity-typed-material-blocker.md
research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current/summary.json
research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current/story_law_rows.jsonl
research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current/recursive_rows.jsonl
```

`research/06-cryptology-rsa/experiments/rsa/v2/AGENTS.md` was restored because it was missing in this
worktree and the RSA v2 test suite asserts that the local contract exists.

## Tests Run

```bash
python3 research/06-cryptology-rsa/experiments/rsa/v2/build_ladder_fixtures.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/audit_experiment.py
pytest -q research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/transported_story_law_probe.py --cases research/06-cryptology-rsa/experiments/rsa/v2/fixtures/ladder_cases.jsonl --measured-rows 256 --recursive-depth 4 --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current
```

## Next Blocker

A valid resolver still needs a public PGSPG theorem that explains why a
certificate state satisfying both gates, `P=true` and `M=false`, uniquely closes
under reciprocal transport. The sidecar shows many such effective survivors, so
the gate is necessary blocker structure, not sufficient closure.
