# Iteration 2 Audit

Status: `failed_iteration`

Radius: `16384`
Small primes: `[2, 3, 5]`
Residual limit: `32768`
Score mode: `rare_thread_balance`
Top-K: `1000`

| case | classification | hit | rank | source rows | vote targets |
| --- | --- | --- | ---: | ---: | ---: |
| toy_23x31 | covered_but_not_ranked_in_top_k | - | - | 17093 | 32766 |
| toy_43x59 | covered_but_not_ranked_in_top_k | - | - | 18917 | 32766 |
| toy_61x83 | covered_but_not_ranked_in_top_k | - | - | 21443 | 32766 |
| toy_89x113 | covered_but_not_ranked_in_top_k | - | - | 26437 | 32766 |
| continuation_00_131101x144203 | public_window_insufficient_coverage | - | - | 24031 | 24031 |
| continuation_01_1048583x1153441 | public_window_insufficient_coverage | - | - | 24031 | 24031 |
