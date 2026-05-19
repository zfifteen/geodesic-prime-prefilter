# Triangulated Distance V1 Iteration Audit

Public method: rank absolute distances by two-sided small-thread triangulation.
Top-K per public result: 1000

Stop conditions:

1. Stop when an iteration places `p` or `q` in the public top-K for every benchmark case.
2. Stop after 10 failed iterations.

| iteration | mode | R | threads | successes | covered failures | coverage failures | status |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | balanced_triplets | 256 | 3 | 4 | 0 | 2 | failed_iteration |
| 2 | shared_threads | 1024 | 3 | 4 | 0 | 2 | failed_iteration |
| 3 | balanced_triplets | 4096 | 4 | 4 | 0 | 2 | failed_iteration |
| 4 | union_triplets | 16384 | 4 | 4 | 0 | 2 | failed_iteration |
| 5 | asymmetry_pressure | 65536 | 5 | 3 | 1 | 2 | failed_iteration |
| 6 | balanced_triplets | 262144 | 6 | 4 | 1 | 1 | failed_iteration |
| 7 | shared_threads | 524288 | 7 | 3 | 2 | 1 | failed_iteration |
| 8 | union_triplets | 1048576 | 8 | 0 | 5 | 1 | failed_iteration |
| 9 | asymmetry_pressure | 1572864 | 9 | 2 | 4 | 0 | failed_iteration |
| 10 | balanced_triplets | 2097152 | 10 | 3 | 3 | 0 | failed_iteration |

## Stop

`failed_after_10_iterations` at iteration `10`.

## Final Iteration Case Results

| case | classification | hit | rank | R | threads |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | one_factor_in_public_top_k | p=23 | 29 | 2097152 | 10 |
| toy_43x59 | one_factor_in_public_top_k | p=43 | 134 | 2097152 | 10 |
| toy_61x83 | covered_but_not_ranked_in_top_k | - | - | 2097152 | 10 |
| toy_89x113 | one_factor_in_public_top_k | p=89 | 506 | 2097152 | 10 |
| continuation_00_131101x144203 | covered_but_not_ranked_in_top_k | - | - | 2097152 | 10 |
| continuation_01_1048583x1153441 | covered_but_not_ranked_in_top_k | - | - | 2097152 | 10 |
