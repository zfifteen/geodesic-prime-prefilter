# Iteration 3 Audit

Status: `failed_iteration`

Radius: `16384`
Small primes: `[2, 3, 5]`
Residual limit: `32768`
Score mode: `rare_per_distance`
Top-K: `1000`

| case | classification | hit | rank | source rows | vote targets |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | one_factor_in_public_top_k | p=23 | 48 | 17093 | 32766 |
| toy_43x59 | one_factor_in_public_top_k | q=59 | 45 | 18917 | 32766 |
| toy_61x83 | one_factor_in_public_top_k | p=61 | 71 | 21443 | 32766 |
| toy_89x113 | one_factor_in_public_top_k | p=89 | 151 | 26437 | 32766 |
| continuation_00_131101x144203 | public_window_insufficient_coverage | - | - | 24031 | 24031 |
| continuation_01_1048583x1153441 | public_window_insufficient_coverage | - | - | 24031 | 24031 |
