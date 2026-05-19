# Grok-Led Public Window Rerun — Minutes

## Context And Agenda

The meeting was convened after Codex invalidated its own 255-bit sparse-web scale-up claim. The error was repeated hidden-factor leakage: benchmark factors `p` and `q` entered experiment setup through `radius = min(p, q)` and direct factor-offset hole construction before public nomination.

The agenda was to put Grok in control of the corrected experiment decisions, repair the setup, rerun under a strict public/private separation, and classify the result plainly.

## Participants And Command Notes

- Grok: lead decision-maker for corrected setup and classification.
- Codex: facilitator, recorder, and verification auditor.

The first Grok CLI call failed with `max_turns exceeded`; this is recorded in `transcript/round-00-grok-error-01.md`. The retry succeeded with the same semantic prompt and a higher turn cap.

## Negotiated Deliverable

The deliverable was a corrected public-window experiment:

1. Public runner receives only `N` and public constants.
2. Private audit uses `p/q` only after public outputs are frozen.
3. The simple first-thread policy is rerun without hidden-factor leakage.
4. The result is classified as accepted measured result, invalidated result, boundary measurement, or unresolved implementation failure.

## Grok Decision

Grok ratified the separated-runner contract and selected the first policy:

- policy: `first_thread_proximity_v1`
- public threads: `(2, 3, 5)`
- fixed public radius: `R = 262144`
- top-k emitted: `20`
- ranking: proximity on deduplicated first-thread offsets

## Verification Notes

Codex inspected the produced public runner and found one source-hygiene issue in the example `main()`: a continuation public `N` was written as a product expression. Codex replaced it with the literal public `N` value so the public runner source no longer contains that factorization expression.

Validation performed:

- `python3 -m py_compile` on both runners and the meeting helper.
- AST scan of `public_window_runner.py` for forbidden runtime names: no hits.
- Frozen public JSON audit: all records include `"public_only": true` and contain no secret factor keys.
- Private audit rerun completed successfully after the hygiene patch.

## Measured Result

The corrected public experiment produced:

- `0 / 6` factor offsets in the public top-20.
- `5 / 6` cases where the factor offset was inside `R` but ranked below top-20.
- `1 / 6` case where the public window did not reach the factor offset.

The prior 255-bit scale-up claim is invalidated as public factor-recovery evidence.

## Classification

Accepted boundary measurement.

The tested public policy is soundly separated from hidden factors, but it does not recover a factor. It demonstrates a boundary of the simple sparse-window proximity approach.

## Canonical Artifacts

- `grok-decision-contract-and-classification.html`
- `public_window_runner.py`
- `private_audit.py`
- `output/audit_first_thread_proximity_v1/summary.md`
- `output/audit_first_thread_proximity_v1/audit_summary.json`
- `transcript/round-01-grok-decision.md`

## Unresolved Next Step

Any future factor-inference claim must use a non-answer-aware public generator. If the generator is window-based, the window must be chosen from `N` alone and the output must be frozen before audit. Large-factor recovery cannot rely on directly enumerating a feasible window around `N` large enough to contain cryptographic-scale factor offsets.

## Adaptive Support V2 Addendum

After the user asked to proceed with the corrected adaptive-window experiment, Codex attempted to ask Grok for the v2 policy. The first adaptive request stalled without output and was terminated; the second short request failed with a Grok CLI `max_turns exceeded` error. The operational failure is recorded in `transcript/round-02-grok-adaptive-request-error.md`.

Codex then implemented the smallest v2 experiment under the last valid Grok contract:

- public runner: `public_adaptive_support_runner.py`
- private audit: `private_adaptive_support_audit.py`
- public radii: `256, 1024, 4096, 16384, 65536, 262144, 1048576, 2097152`
- public threads: `2, 3, 5`
- ranking: support count first, then proximity
- top-k per radius: `100`

Result:

- `4 / 6` cases placed one factor offset in the public top-100.
- All four toy cases succeeded at `R = 256`.
- Both continuation cases were covered by the final radius but did not enter the public top-100.
- The best final full ranks for the continuation cases were `9614` and `69906`.

Classification:

```text
boundary measurement
```

The v2 result shows that adaptive public windows fix coverage on the tested continuation cases, and support-count ranking improves the toy results. It also shows that the larger covered cases fail because the selector is still too weak: the factor offsets are present but buried deep in the public ordering.

## Adaptive Alphabet V3 Addendum

The user then identified the next missing control: the thread alphabet must adapt together with the window.

Codex implemented:

- `public_alphabet_policy.py`
- `public_adaptive_alphabet_runner.py`
- `private_adaptive_alphabet_audit.py`
- `adaptive_alphabet_v3_result.html`

Public policy:

- each rung increases both public radius and public thread prefix;
- thread prefixes grow from `2,3,5` through `2,3,5,7,11,13,17,19,23,29`;
- ranking uses support count, signature rarity, signature weight, then proximity;
- top-k per rung is `1000`.

Measured result:

- `4 / 6` cases placed one factor offset in the public top-1000;
- all four toy cases succeeded at the first rung, `R = 256`, thread count `3`;
- both continuation cases were covered but did not enter top-1000;
- best final full ranks were `10079` and `669144`.

Grok performed a code review. It found:

- no hidden-factor leakage in the public runner;
- `p/q` remain post-freeze in the private audit;
- the ranking policy is a valid measurement of one heuristic;
- the dominant code flaw was duplicated ranking logic between public and audit code;
- the dominant methodology limitation is that this remains a classical additive-window signature heuristic, not a PGS-native selection rule.

Codex implemented Grok's requested code fix by extracting the pure public ranking machinery into `public_alphabet_policy.py` and having both the public runner and audit import it.

Classification:

```text
boundary measurement
```

Adaptive alphabet growth is now implemented cleanly, but the tested rank function still fails beyond toy scale. More threads alone are insufficient when the rank function rewards signatures that are not factor-specific.

## Triangulated Distance V1 Goal Addendum

The user then set a new explicit goal:

```text
Design and run a better multiplicative-web runner that preserves the original thread-triangulation mechanism, iterating up to 10 versions until either one public version recovers p or q under post-freeze audit or all 10 iterations fail.
```

Codex implemented:

- `public_triangulation_policy.py`
- `private_triangulation_iteration_audit.py`
- `triangulated_distance_v1_result.html`

Public mechanism:

- rank absolute distances, not isolated signed offsets;
- for each distance `d`, observe public small-thread hits on `N - d` and `N + d`;
- score the distance by two-sided triangulation modes;
- freeze the public top-1000 before private audit.

Stop conditions:

1. stop if one iteration recovers `p` or `q` in the public top-1000 for every benchmark case;
2. otherwise stop after 10 failed iterations.

Measured result:

```text
failed_after_10_iterations
```

Iteration summary:

| iteration | mode | R | threads | successes | covered failures | coverage failures |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | balanced_triplets | 256 | 3 | 4 | 0 | 2 |
| 2 | shared_threads | 1024 | 3 | 4 | 0 | 2 |
| 3 | balanced_triplets | 4096 | 4 | 4 | 0 | 2 |
| 4 | union_triplets | 16384 | 4 | 4 | 0 | 2 |
| 5 | asymmetry_pressure | 65536 | 5 | 3 | 1 | 2 |
| 6 | balanced_triplets | 262144 | 6 | 4 | 1 | 1 |
| 7 | shared_threads | 524288 | 7 | 3 | 2 | 1 |
| 8 | union_triplets | 1048576 | 8 | 0 | 5 | 1 |
| 9 | asymmetry_pressure | 1572864 | 9 | 2 | 4 | 0 |
| 10 | balanced_triplets | 2097152 | 10 | 3 | 3 | 0 |

Classification:

```text
boundary measurement
```

The runner now preserves the triangulation unit more faithfully than V3, but all ten tested public versions failed to recover one factor across the full benchmark surface. Once coverage is reached, the remaining failure is selector specificity: ordinary two-sided small-thread coincidences still outrank factor distances.
