# Ratio Iteration 01 Grok Review Request

## Task

Review the exploratory ratio probe and approve or reject the next single ratio setting before execution.

This is not a batch sweep. The next setting is chosen from the previous v02 failure and Grok's own recommendation.

## Source Files

Public probe:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/thread_triangulation_ratio_probe.py`

SHA-256:

`8dc166e92045bf0871c5d1069380dd933833c82241185473f0a79960a6e8a594`

Private freeze-then-audit harness:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/run_ratio_probe_iteration.py`

SHA-256:

`76e0727171fe8d2baee752649d7fafaa5020dfd0b468d9f35b8b9a35643ddee2`

## Mechanical Checks

`python3 -m py_compile` passed for both files.

Forbidden-token scan for:

```text
factorint
isprime
nextprime
sqrt
random
gcd
known_factor
factor_distance
exact_factor_rank
target_distance
private_distance
N % candidate
product closure
```

returned no matches.

## Previous v02 Result

The previous certified v02 setting was:

```text
thread_count_ratio = 3/8
depth_ratio = 5/12
retention_divisor = 1024
```

It produced:

```text
recovered_count = 0
missed_count = 10
hit_rate = 0/10
median_emitted_count = 36.0
median_candidate_reduction_bits = 10.0
```

Your prior recommendation was to change only:

```text
thread_count_ratio: 3/8 -> 1/2
```

and keep:

```text
depth_ratio = 5/12
retention_divisor = 1024
```

## Proposed Iteration 01 Setting

```text
thread_count_ratio = 1/2
depth_ratio = 5/12
retention_divisor = 1024
```

## Boundaries

- Public probe receives public `N`, public ratios, and output path only.
- Private audit pairs are available only in the harness after the public freeze log is written.
- The harness must not re-rank, re-score, or filter public candidates after audit.
- No private rank, containment, near-miss, or per-distance hidden-factor diagnostic is allowed.

## Requested Output

Return exactly one approval classification:

- `approved_for_iteration_01`
- `not_approved`
- `approved_with_required_corrections`

Then state the reason. If approved, say whether this is the correct next single iteration under the observed v02 failure. Do not run the experiment.
