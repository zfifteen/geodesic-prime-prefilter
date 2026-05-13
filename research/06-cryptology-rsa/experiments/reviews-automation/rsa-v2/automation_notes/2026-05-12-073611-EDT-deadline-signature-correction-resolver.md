# Deadline Signature Correction Resolver

Run time: 2026-05-12 07:36:11 EDT.

## Strongest Supported Finding

RSA v2 now has a public resolver rule beyond strict reset closure.

The new rule is reciprocal deadline signature correction:

```text
public N
-> lower reset certificate
-> upper reset certificate induced by floor(N / lower.reset_endpoint)
-> failed upper reset transports back to z = floor(N / upper.reset_endpoint)
-> c = previous public endpoint before z
-> corrected lower certificate at c
-> d = upper.reset_deadline_value
-> resolve only if:
     c < lower.anchor
     d > upper.reset_endpoint
     floor(N / c) == d
     floor(N / d) == c
     corrected_lower.reset_signature == upper.reset_signature
```

This is one deterministic public correction. It is not a candidate scan,
endpoint budget, product check, divisibility test, audit lookup, hidden-factor
lookup, primality API, or per-rung branch.

## Implementation Status

Implemented in:

```text
research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
```

Rule id changed to:

```text
reciprocal_pgs_certificate_pair_v2
```

New closure status:

```text
endpoint_class_by_reciprocal_deadline_signature_correction
```

The existing strict closure status remains:

```text
endpoint_class_by_mutual_certificate_closure
```

The runner emits corrected public fields in `survivor_rows.jsonl`:

```text
corrected_lower_endpoint
corrected_upper_endpoint
transported_corrected_upper_endpoint
transported_corrected_lower_endpoint
corrected_lower_* certificate fields
```

No resolver code reads audit factors.

## Demonstration Below 40 Bits

The new branch resolves a 17-bit public toy row:

```text
case_id = rsa_v2_toy_deadline_17bit_static_001
N = 73903
initial lower anchor/reset = 269 / 271
initial upper anchor/reset = 271 / 277
z = floor(N / 277) = 266
c = previous public endpoint before z = 263
d = upper.reset_deadline_value = 281
floor(N / 263) = 281
floor(N / 281) = 263
corrected lower signature = carrier_d=4;lock_carrier_d=4;threat=True;deadline=tail
upper signature = carrier_d=4;lock_carrier_d=4;threat=True;deadline=tail
output = 263, 281
```

This toy row is covered by:

```text
tests/python/test_rsa_v2_scripts.py::test_deadline_signature_correction_resolves_public_toy_case
```

## 40-Bit Result

The official 40-bit row now resolves:

```text
case_id = rsa_v2_40bit_static_001
N = 1099507433251
initial lower anchor/reset = 1048571 / 1048573
initial upper anchor/reset = 1048573 / 1048583
upper deadline d = 1048589
z = floor(N / 1048583) = 1048564
c = previous public endpoint before z = 1048559
floor(N / 1048559) = 1048589
floor(N / 1048589) = 1048559
corrected lower signature = carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail
upper signature = carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail
closure_status = endpoint_class_by_reciprocal_deadline_signature_correction
output = 1048559, 1048589
```

Audit result:

```text
audit_integrity_status = integrity_pass
inference_audit_status = inference_audit_pass
```

## 50-Bit Result

The official 50-bit row remains unresolved:

```text
case_id = rsa_v2_50bit_static_001
closure_status = unresolved_by_certificate_pair_not_closed
reason = upper certificate missing under the live public rule
audit_integrity_status = integrity_pass
inference_audit_status = inference_audit_fail
```

This is the correct state. The new rule does not add a fallback path when the
upper certificate is absent.

## Sidecar Status

Transported story and d4 sidecars remain unchanged as sidecar evidence:

```text
transported story = 512 -> 202 -> 713 -> 0
d4 strict frontier candidates = 50
d4 trace terminal partition = {recursive_cycle: 44, typed: 6}
```

`toy_normalized_frontier_closure_sweep_current` now records that the 40-bit
case is closed by official inference while the normalized-frontier sidecar
still has one live row. That sidecar is not resolver logic.

## Falsification Pressure

Endpoint-pair product sweeps were used only as downstream audit pressure:

```text
first 5000 consecutive PGSPG endpoint-pair products:
  resolved_strict = 1
  resolved_deadline_correction = 0
  audit false positives = 0

first 25000 consecutive PGSPG endpoint-pair products:
  resolved_strict = 6
  resolved_deadline_correction = 0
  audit false positives = 0
```

This does not prove the rule. It shows the correction branch is not a loose
classifier over nearby endpoint products.

## Grok Review

Orientation prompt:

```text
Confirm the public-only RSA v2 frame, allowed PGSPG certificate fields, the new
deadline-correction rule, the 17-bit toy resolution, the official 40-bit
resolution, the 50-bit unresolved state, and the unchanged story/d4 sidecars.
```

Grok asked for the exact official 40-bit numeric anchors and signatures.

Technical prompt supplied:

```text
N = 1099507433251
lower anchor/reset/signature = 1048571 / 1048573 /
  carrier_d=96;lock_carrier_d=96;threat=True;deadline=threat
upper anchor/reset/deadline/signature = 1048573 / 1048583 / 1048589 /
  carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail
z = 1048564
c = 1048559
floor(N/c) = 1048589
floor(N/d) = 1048559
corrected lower signature matches upper signature
```

Grok judgment:

```text
Reciprocal deadline signature correction introduces no hidden classical
shortcut under the stated contract. The rule is PGS-valid because the deadline
endpoint is certificate-supplied and mutual floor closure plus signature match
closes the transported pair. False-resolution risk remains unproved beyond the
current exact backend.
```

Grok next action:

```text
Run the exact rule on the next official 60-bit row that supplies both lower and
upper certificates and verify that either it resolves correctly or the four
conditions fail without emitting a candidate.
```

## Files Changed

```text
research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
tests/python/test_rsa_v2_scripts.py
research/06-cryptology-rsa/experiments/rsa/v2/ALGORITHM.md
research/06-cryptology-rsa/experiments/rsa/v2/PGS_CERTIFICATE.md
research/06-cryptology-rsa/experiments/rsa/v2/METRICS.md
research/06-cryptology-rsa/experiments/rsa/v2/README.md
research/06-cryptology-rsa/experiments/rsa/v2/SESSION_BOOTSTRAP.md
research/06-cryptology-rsa/experiments/rsa/v2/AGENTS.md
research/06-cryptology-rsa/experiments/rsa/v2/TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md
research/06-cryptology-rsa/experiments/rsa/v2/output/inference_rows.jsonl
research/06-cryptology-rsa/experiments/rsa/v2/output/survivor_rows.jsonl
research/06-cryptology-rsa/experiments/rsa/v2/output/summary.json
research/06-cryptology-rsa/experiments/rsa/v2/output/audit_results.csv
research/06-cryptology-rsa/experiments/rsa/v2/output/toy_normalized_frontier_closure_sweep_current/
```

## Tests Run

```text
pytest -q tests/python/test_rsa_v2_scripts.py
50 passed in 24.17s

pytest -q tests/python/test_rsa_v2_scripts.py tests/python/test_rsa_v2_transported_story_law.py tests/python/test_rsa_v2_transported_d4_budget.py tests/python/test_rsa_v2_transported_d4_budget_trace.py
93 passed in 231.92s
```

Full output refresh:

```text
python3 research/06-cryptology-rsa/experiments/rsa/v2/build_ladder_fixtures.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/run_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/audit_experiment.py
python3 research/06-cryptology-rsa/experiments/rsa/v2/transported_story_law_probe.py --cases research/06-cryptology-rsa/experiments/rsa/v2/fixtures/ladder_cases.jsonl --measured-rows 256 --recursive-depth 4 --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current
python3 research/06-cryptology-rsa/experiments/rsa/v2/transported_d4_budget_probe.py --story-rows research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current/story_law_rows.jsonl --recursive-rows research/06-cryptology-rsa/experiments/rsa/v2/output/transported_story_law_current/recursive_rows.jsonl --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/transported_d4_budget_current
python3 research/06-cryptology-rsa/experiments/rsa/v2/transported_d4_budget_trace.py --budget-rows research/06-cryptology-rsa/experiments/rsa/v2/output/transported_d4_budget_current/budget_rows.jsonl --recursive-budget-rows research/06-cryptology-rsa/experiments/rsa/v2/output/transported_d4_budget_current/recursive_budget_rows.jsonl --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/transported_d4_budget_trace_current
python3 research/06-cryptology-rsa/experiments/rsa/v2/toy_normalized_frontier_closure_sweep.py --output-dir research/06-cryptology-rsa/experiments/rsa/v2/output/toy_normalized_frontier_closure_sweep_current
```

## Next Scaling Step

Add or generate a 60-bit public rung with separate audit labels, run the same
rule unchanged, and accept only these outcomes:

```text
resolved by strict reset closure;
resolved by reciprocal deadline signature correction and audit passes;
unresolved with no candidate emitted.
```

Any audit-failing emitted candidate falsifies the rule at that scale.
