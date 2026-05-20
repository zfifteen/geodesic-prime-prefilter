# Ratio Iteration 02 Grok Review Request

## Task

Review Iteration 01 results and choose exactly one next ratio setting to run.

This is sequential iteration. Do not propose a preset ladder or multiple variants.

## Iteration 01 Setting

```text
thread_count_ratio = 1/2
depth_ratio = 5/12
retention_divisor = 1024
```

## Iteration 01 Output

Summary:

`/Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/candidate-list-search-space-reduction-runner/output/ratio_iterations/iteration_01_thread_1_2_depth_5_12_retention_1024/summary.json`

Observed:

```text
case_count = 10
recovered_count = 0
missed_count = 10
hit_rate = 0/10
median_emitted_count = 36.0
median_candidate_reduction_bits = 10.0
```

Per-case public surface:

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | status |
|---|---:|---:|---:|---:|---:|---:|---|---|
| toy_989 | 10 | 3 | 2 | 1 | 1 | 7 | true | missed |
| toy_9379 | 14 | 4 | 2 | 1 | 1 | 17 | true | missed |
| toy_25807 | 15 | 5 | 3 | 1 | 1 | 34 | true | missed |
| toy_1242079 | 21 | 6 | 3 | 1 | 1 | 112 | true | missed |
| toy_200250077 | 28 | 8 | 4 | 8 | 8 | 506 | true | missed |
| toy_4295229443 | 33 | 9 | 4 | 64 | 64 | 1599 | true | missed |
| toy_18902665303 | 35 | 10 | 5 | 128 | 128 | 2735 | true | missed |
| toy_1209476905903 | 41 | 11 | 5 | 1024 | 1024 | 6696 | true | missed |
| toy_77468500194643 | 47 | 13 | 6 | 8192 | 8192 | 33795 | true | missed |
| toy_4951764003343009 | 53 | 14 | 6 | 65536 | 65536 | 103680 | true | missed |

## Codex Interpretation From Public Observables

Increasing the thread alphabet alone did not restore recovery. The retention rule remained the binding constraint on every case, and the first four cases emitted only one public candidate each. That points to `retention_divisor = 1024` being too aggressive for this corpus under the ratio-only no-floor/no-ceiling rule.

## Question

Choose exactly one next public ratio setting for Iteration 02.

Allowed action: change one ratio constant, or explicitly justify changing two if you believe one change cannot test the hypothesis cleanly.

Return:

```text
approved_next_setting:
thread_count_ratio = ?
depth_ratio = ?
retention_divisor = ?
reason = ?
```

Do not run code. Do not use hidden factors beyond the canonical status summary above. Do not compute private ranks or containment.
