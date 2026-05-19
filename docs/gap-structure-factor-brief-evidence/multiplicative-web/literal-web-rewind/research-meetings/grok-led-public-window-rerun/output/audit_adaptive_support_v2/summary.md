# Adaptive Support V2 Audit Summary

Public policy: adaptive public radii, threads `(2, 3, 5)`, rank by support count then proximity.
Public radii: (256, 1024, 4096, 16384, 65536, 262144, 1048576, 2097152)
Top-K per radius: 100

Public runner receives only `N`. Private audit uses `p/q` only after public output is frozen.

| case | bits | final coverage | classification | first hit R | first hit | rank | support | best final full rank |
| --- | ---: | --- | --- | ---: | --- | ---: | ---: | ---: |
| toy_23x31 | 10 | yes | one_factor_in_public_top_k | 256 | -p | 2 | 3 | 2 |
| toy_43x59 | 12 | yes | one_factor_in_public_top_k | 256 | p | 3 | 3 | 3 |
| toy_61x83 | 13 | yes | one_factor_in_public_top_k | 256 | -q | 6 | 3 | 6 |
| toy_89x113 | 14 | yes | one_factor_in_public_top_k | 256 | q | 8 | 3 | 8 |
| continuation_00_131101x144203 | 35 | yes | covered_but_not_ranked_in_top_k | - | - | - | - | 9614 |
| continuation_01_1048583x1153441 | 41 | yes | covered_but_not_ranked_in_top_k | - | - | - | - | 69906 |

## Counts

- one_factor_in_public_top_k: 4 / 6
- covered_but_not_ranked_in_top_k: 2 / 6
- public_window_insufficient_coverage: 0 / 6
