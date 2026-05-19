# Iteration 8 Audit

Status: `failed_iteration`

Radius: `262144`
Small primes: `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`
Residual limit: `1`
Score mode: `rare_per_distance`
Top-K: `16384`

| case | classification | hit | rank | source rows | vote targets |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | one_factor_in_public_top_k | p=23 | 4 | 221335 | 441478 |
| toy_43x59 | one_factor_in_public_top_k | p=43 | 18 | 222874 | 441480 |
| toy_61x83 | one_factor_in_public_top_k | p=61 | 132 | 225001 | 441481 |
| toy_89x113 | one_factor_in_public_top_k | p=89 | 40 | 229203 | 441478 |
| continuation_00_131101x144203 | covered_but_not_ranked_in_top_k | - | - | 441481 | 441481 |
| continuation_01_1048583x1153441 | public_window_insufficient_coverage | - | - | 441488 | 441488 |
