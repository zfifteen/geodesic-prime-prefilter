# Iteration 4 Audit

Status: `failed_iteration`

Radius: `262144`
Small primes: `[2, 3, 5]`
Residual limit: `32768`
Score mode: `rare_per_distance`
Top-K: `1000`

| case | classification | hit | rank | source rows | vote targets |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | one_factor_in_public_top_k | p=23 | 40 | 201496 | 485308 |
| toy_43x59 | one_factor_in_public_top_k | q=59 | 34 | 202833 | 485305 |
| toy_61x83 | one_factor_in_public_top_k | p=61 | 53 | 204686 | 485300 |
| toy_89x113 | one_factor_in_public_top_k | p=89 | 89 | 208348 | 485281 |
| continuation_00_131101x144203 | covered_but_not_ranked_in_top_k | - | - | 384479 | 385422 |
| continuation_01_1048583x1153441 | public_window_insufficient_coverage | - | - | 384479 | 384479 |
