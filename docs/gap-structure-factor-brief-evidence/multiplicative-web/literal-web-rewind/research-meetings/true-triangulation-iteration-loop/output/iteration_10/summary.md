# Iteration 10 Audit

Status: `failed_iteration`

Radius: `2097152`
Small primes: `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]`
Residual limit: `1`
Score mode: `anchor_confirmed`
Top-K: `16384`

| case | classification | hit | rank | source rows | vote targets |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | one_factor_in_public_top_k | p=23 | 7 | 1766511 | 3531833 |
| toy_43x59 | one_factor_in_public_top_k | p=43 | 14 | 1768049 | 3531829 |
| toy_61x83 | one_factor_in_public_top_k | p=61 | 48 | 1770174 | 3531832 |
| toy_89x113 | one_factor_in_public_top_k | p=89 | 28 | 1774383 | 3531831 |
| continuation_00_131101x144203 | one_factor_in_public_top_k | q=144203 | 2897 | 3531828 | 3531828 |
| continuation_01_1048583x1153441 | covered_but_not_ranked_in_top_k | - | - | 3531821 | 3531821 |
