# Ratio Iteration 04 Grok Review Request

## Task

Review Iteration 03 results and choose exactly one next ratio setting to run.

This is sequential iteration. Do not propose a preset ladder or multiple variants.

## Iteration 03 Setting

```text
thread_count_ratio = 1/2
depth_ratio = 4/12
retention_divisor = 512
```

## Iteration 03 Output

Summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/ratio_iterations/iteration_03_thread_1_2_depth_4_12_retention_512/summary.json`

Observed:

```text
case_count = 10
recovered_count = 0
missed_count = 10
hit_rate = 0/10
median_emitted_count = 72.0
median_candidate_reduction_bits = 9.0
```

Per-case public surface:

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| toy_989 | 10 | 3 | 1 | 1 | 1 | 7 | true | missed |
| toy_9379 | 14 | 4 | 2 | 1 | 1 | 17 | true | missed |
| toy_25807 | 15 | 5 | 2 | 1 | 1 | 38 | true | missed |
| toy_1242079 | 21 | 6 | 2 | 2 | 2 | 114 | true | missed |
| toy_200250077 | 28 | 8 | 3 | 16 | 16 | 525 | true | missed |
| toy_4295229443 | 33 | 9 | 3 | 128 | 128 | 1620 | true | missed |
| toy_18902665303 | 35 | 10 | 4 | 256 | 256 | 2891 | true | missed |
| toy_1209476905903 | 41 | 11 | 4 | 2048 | 2048 | 6891 | true | missed |
| toy_77468500194643 | 47 | 13 | 5 | 16384 | 16384 | 35524 | true | missed |
| toy_4951764003343009 | 53 | 14 | 5 | 131072 | 105886 | 105886 | false | missed |

## Codex Interpretation From Public Observables

The isolated depth relaxation did not recover any case. The 53-bit case was cap-inactive again and emitted every depth-qualified candidate at min_depth 5, yet still missed. That points away from retention and away from a one-step depth threshold problem. The next clean test appears to be increasing thread_count_ratio again while keeping the relaxed depth and current retention fixed.

## Question

Choose exactly one next public ratio setting for Iteration 04.

Allowed action: change one ratio constant, or explicitly justify changing two if one change cannot test the hypothesis cleanly.

Return:

```text
approved_next_setting:
thread_count_ratio = ?
depth_ratio = ?
retention_divisor = ?
reason = ?
```

Do not run code. Do not use hidden factors beyond the canonical status summary above. Do not compute private ranks or containment.
