# Toy Endpoint-Chain Closure Blocker

Run time: 2026-05-12 06:16:36 EDT.

## Strongest Supported Finding

The public reciprocal certificate runner resolves a deterministic below-40-bit
toy family, but the mechanism is still a twin-endpoint strict landing artifact,
not a scalable resolver rule.

Six public toy rows below 40 bits resolved by the existing strict rule:

```text
case_id                                      bits  N            lower   upper   U  L  S
rsa_v2_toy_chain_28bit_first_strict_001      28   257987843    16061   16063   0  0  true
rsa_v2_toy_chain_34bit_strict_001            34   10444431203  102197  102199  0  0  true
rsa_v2_toy_chain_35bit_strict_001            35   20592824003  143501  143503  0  0  true
rsa_v2_toy_chain_35bit_strict_002            35   27100402883  164621  164623  0  0  true
rsa_v2_toy_chain_36bit_strict_001            36   50724949283  225221  225223  0  0  true
rsa_v2_toy_chain_37bit_strict_001            37   72243763523  268781  268783  0  0  true
```

Here:

```text
U = transported_upper_endpoint - upper_reset_endpoint
L = transported_lower_endpoint - lower_reset_endpoint
S = lower_reset_signature == upper_reset_signature
```

All six closure rows are twin endpoint pairs with gap `2` and reset signature:

```text
carrier_d=8;lock_carrier_d=8;threat=True;deadline=tail
```

## Baseline Reproduced

Official runner output remains unchanged:

```text
rsa_v2_40bit_static_001 -> unresolved_by_certificate_pair_not_closed
rsa_v2_50bit_static_001 -> unresolved_by_certificate_pair_not_closed
```

Official transported story law reproduced:

```text
row_count = 512
ledger_effective_survivor_count = 202
recursive_row_count = 713
recursive_final_survivor_count = 0
falsification_status = passed
```

Official transported d4 budget reproduced:

```text
row_count = 512
ledger_effective_survivor_count = 202
recursive_row_count = 713
strict_budget_frontier_candidate_count = 50
```

Official transported d4 trace reproduced:

```text
strict_candidate_count = 50
terminal_partition = {recursive_cycle: 44, typed: 6}
still_unresolved_count = 0
non_depth0_recursive_survivor_count = 1
non_depth0_survivor_child_terminal_partition = {stale: 1}
```

## Toy Regime Definition

The toy regime was built as a deterministic PGSPG endpoint-chain sidecar:

```text
start endpoint = 5
repeat: certificate = pgs_certificate(endpoint)
next endpoint = certificate.reset_endpoint
for consecutive public reset endpoints lower, upper:
  define public toy N row from the endpoint-chain pair
  run the existing public runner on only case_id, bits, N
```

No audit factors, hidden factors, factor APIs, primality APIs, `gcd`,
divisibility, randomness, fallback search, fixed chamber radius, or endpoint
budget resolver was used during inference.

The deterministic endpoint-chain scan found one strict closure in the first
5000 endpoint pairs:

```text
row_count = 5000
exact_landing_count = 679
exact_landing_signature_false = 678
exact_landing_signature_true = 1
resolved_count = 1
first_resolved_pair_index = 1863
```

The next 200 endpoint pairs after the sixth closure were a holdout:

```text
start_pair_index = 23538
row_count = 200
resolved_count = 0
twin_pair_count = 19
d_zero_signature_true_count = 0
status_partition = {unresolved_by_certificate_pair_not_closed: 200}
defect_partition = {U=0;L=0;S=False: 19, U=None;L=None;S=False: 181}
```

This separates exact reciprocal landing from reset-signature transport. Exact
landing is common in the endpoint-chain toy surface; signature agreement is the
rare gate.

## Toy Sidecars

Toy transported story law over the six public rows with `measured_rows=64`:

```text
row_count = 384
ledger_effective_survivor_count = 159
recursive_row_count = 544
recursive_final_survivor_count = 0
```

The story-law script reports `falsification_status = failed` only because its
embedded expected counts are the official two-rung counts. The toy recursive
surface itself still has `0` final recursive survivors.

Toy transported d4 budget:

```text
row_count = 384
ledger_effective_survivor_count = 159
recursive_row_count = 544
strict_budget_frontier_candidate_count = 34
```

Toy transported d4 trace:

```text
strict_candidate_count = 34
terminal_partition = {recursive_cycle: 30, typed: 4}
still_unresolved_count = 0
```

## Grok Prompt And Response Summary

Orientation prompt summary:

```text
Confirm the PGS-native RSA v2 frame, the public-only reciprocal certificate
contract, the official unresolved 40-bit and 50-bit state, the reproduced
transported-story and d4 sidecars, and the toy D=(U,L,S) closure surface.
```

Grok acknowledged the frame and asked for the exact certificate construction
and closure predicate before technical judgment.

Technical prompt summary:

```text
Given run_experiment.py closure code, the six toy closure rows, official
40-bit/50-bit blocker rows, invalidated rules, and candidate D=(U,L,S), judge
hidden classical shortcut risk, false-resolution risk, deterministic
falsification tests, and one next action.
```

Grok technical judgment:

```text
The toy strict reciprocal closures are close-pair artifacts restricted to
gap=2 twin endpoints with identical carrier_d=8 signatures. D=(0,0,true) is
not supported as a scalable PGS invariant and must remain sidecar-only.
```

Grok's concrete next action was to run the next 200 consecutive endpoint pairs
without twin filtering and report all D vectors. That holdout was run and found
zero resolutions.

## Novel Insight Candidate

Core candidate:

```text
The toy closure surface splits into two independent gates: reciprocal landing
and reset-signature transport. Exact landing supplies the floor-cell arithmetic
condition, but signature transport decides whether the public chamber state
actually closes.
```

Falsifiable prediction:

```text
If this framing is right, endpoint-chain pairs with U=0 and L=0 but S=false
remain unresolved under the current strict runner, while rows with
U=0, L=0, S=true resolve.
```

Current test result:

```text
pre-first 5000 endpoint pairs:
  U=0,L=0,S=false -> 678 rows
  U=0,L=0,S=true -> 1 row
  resolved rows -> 1

next 200 endpoint-pair holdout:
  U=0,L=0,S=false -> 19 rows
  U=0,L=0,S=true -> 0 rows
  resolved rows -> 0
```

The result supports the split as a sidecar diagnostic. It does not supply a
PGSPG theorem that predicts `S=true`, so it does not promote a resolver rule.

## 40-Bit And 50-Bit Comparison

Official 40-bit row:

```text
closure_status = unresolved_by_certificate_pair_not_closed
U = -9
L = -9
S = false
lower_reset_endpoint = 1048573
upper_reset_endpoint = 1048583
transported_upper_endpoint = 1048574
transported_lower_endpoint = 1048564
```

Official 50-bit row:

```text
closure_status = unresolved_by_certificate_pair_not_closed
upper certificate = missing
S = false
transported_upper_endpoint = 32053634
```

The toy invariant does not resolve either official row.

## Files Changed

Added or regenerated generated toy sidecar outputs:

```text
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/toy_cases.jsonl
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/inference/
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/transported_story_law/
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/transported_d4_budget/
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/transported_d4_budget_trace/
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/pre_first_closure_defect_summary.json
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/endpoint_pair_holdout_rows.jsonl
experiments/rsa/v2/output/toy_endpoint_chain_closure_current/endpoint_pair_holdout_summary.json
```

Restored missing local contract file required by the RSA v2 script tests:

```text
experiments/rsa/v2/AGENTS.md
```

Added this note:

```text
experiments/rsa/v2/automation_notes/2026-05-12-061636-EDT-toy-endpoint-chain-closure-blocker.md
```

No resolver code was changed.

## Tests Run

```text
python3 experiments/rsa/v2/build_ladder_fixtures.py
python3 experiments/rsa/v2/run_experiment.py
python3 experiments/rsa/v2/audit_experiment.py
python3 experiments/rsa/v2/transported_story_law_probe.py --cases experiments/rsa/v2/fixtures/ladder_cases.jsonl --measured-rows 256 --recursive-depth 4 --output-dir experiments/rsa/v2/output/transported_story_law_current
python3 experiments/rsa/v2/transported_d4_budget_probe.py --story-rows experiments/rsa/v2/output/transported_story_law_current/story_law_rows.jsonl --recursive-rows experiments/rsa/v2/output/transported_story_law_current/recursive_rows.jsonl --output-dir experiments/rsa/v2/output/transported_d4_budget_current
python3 experiments/rsa/v2/transported_d4_budget_trace.py --budget-rows experiments/rsa/v2/output/transported_d4_budget_current/budget_rows.jsonl --recursive-budget-rows experiments/rsa/v2/output/transported_d4_budget_current/recursive_budget_rows.jsonl --output-dir experiments/rsa/v2/output/transported_d4_budget_trace_current
pytest -q tests/python/test_rsa_v2_scripts.py tests/python/test_rsa_v2_transported_story_law.py tests/python/test_rsa_v2_transported_d4_budget.py tests/python/test_rsa_v2_transported_d4_budget_trace.py
```

Focused pytest result:

```text
92 passed in 235.78s
```

## Next Blocker

Unresolved: no public PGSPG theorem predicts reset-signature agreement across
reciprocal transport.

Next scaling step:

```text
Build a public signature-transport sidecar over endpoint-chain pairs:
  source reset signature
  induced reset signature
  U
  L
  endpoint gap
  source carrier/deadline fields
  induced carrier/deadline fields

Falsification gate:
  if any proposed public chamber-field predicate predicts S=true but accepts
  a U=0,L=0,S=false row from the 678 pre-first rows or 19 holdout rows, reject
  the predicate.
```

Resolver promotion remains blocked until a public PGSPG law derives signature
transport, not merely observes it on twin endpoint closures.
