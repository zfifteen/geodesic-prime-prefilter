# Adaptive Alphabet V3 Audit Summary

Public policy: adaptive public radius, adaptive public thread alphabet, rank by support count, signature rarity, signature weight, then proximity.
Top-K per rung: 1000

Public runner receives only `N`. Private audit uses `p/q` only after public output is frozen.

| case | bits | classification | first hit R | threads | hit | rank | support | signature count | best final full rank |
| --- | ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| toy_23x31 | 10 | one_factor_in_public_top_k | 256 | 3 | -p | 2 | 3 | 17 | 52060 |
| toy_43x59 | 12 | one_factor_in_public_top_k | 256 | 3 | p | 3 | 3 | 17 | 286613 |
| toy_61x83 | 13 | one_factor_in_public_top_k | 256 | 3 | -q | 6 | 3 | 17 | 286960 |
| toy_89x113 | 14 | one_factor_in_public_top_k | 256 | 3 | q | 8 | 3 | 17 | 223648 |
| continuation_00_131101x144203 | 35 | covered_but_not_ranked_in_top_k | - | - | - | - | - | - | 10079 |
| continuation_01_1048583x1153441 | 41 | covered_but_not_ranked_in_top_k | - | - | - | - | - | - | 669144 |

## Counts

- one_factor_in_public_top_k: 4 / 6
- covered_but_not_ranked_in_top_k: 2 / 6
- public_window_insufficient_coverage: 0 / 6
