# Ratio Iteration 03 Grok Review Request

## Task

Review Iteration 02 results and choose exactly one next ratio setting to run.

This is sequential iteration. Do not propose a preset ladder or multiple variants.

## Iteration 02 Setting

```text
thread_count_ratio = 1/2
depth_ratio = 5/12
retention_divisor = 512
```

## Iteration 02 Output

Summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/ratio_iterations/iteration_02_thread_1_2_depth_5_12_retention_512/summary.json`

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
| toy_989 | 10 | 3 | 2 | 1 | 1 | 7 | true | missed |
| toy_9379 | 14 | 4 | 2 | 1 | 1 | 17 | true | missed |
| toy_25807 | 15 | 5 | 3 | 1 | 1 | 34 | true | missed |
| toy_1242079 | 21 | 6 | 3 | 2 | 2 | 112 | true | missed |
| toy_200250077 | 28 | 8 | 4 | 16 | 16 | 506 | true | missed |
| toy_4295229443 | 33 | 9 | 4 | 128 | 128 | 1599 | true | missed |
| toy_18902665303 | 35 | 10 | 5 | 256 | 256 | 2735 | true | missed |
| toy_1209476905903 | 41 | 11 | 5 | 2048 | 2048 | 6696 | true | missed |
| toy_77468500194643 | 47 | 13 | 6 | 16384 | 16384 | 33795 | true | missed |
| toy_4951764003343009 | 53 | 14 | 6 | 131072 | 103680 | 103680 | false | missed |

## Codex Interpretation From Public Observables

Relaxing retention alone did not recover any case. The largest case was cap-inactive and emitted the full depth-qualified set, yet still missed. That means at least one failure mode is not just capping: the current depth threshold and/or active thread alphabet did not place the true distance in the public qualified set.

Since we already increased thread_count_ratio once and relaxed retention once, the next clean single change appears to be lowering the depth ratio.

## Question

Choose exactly one next public ratio setting for Iteration 03.

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
