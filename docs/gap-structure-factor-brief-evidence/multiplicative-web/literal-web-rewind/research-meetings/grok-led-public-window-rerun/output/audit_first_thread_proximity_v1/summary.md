# Grok-Led Public Window Rerun — Private Audit Summary

Policy: first_thread_proximity_v1
Public threads: (2, 3, 5)
Public radius R (fixed, computed from policy only): 262144
Top-K reported by public runner: 20

Public runner received only N. p/q used exclusively for post-freeze scoring.

| case | bits | p | covered_by_R | classification | best_rank | topK_hit |
| --- | ---: | ---: | --- | --- | ---: | --- |
| toy_23x31 | 10 | 23 | yes | factor_offset_inside_R_but_ranked_below_top_k | 34 | no |
| toy_43x59 | 12 | 43 | yes | factor_offset_inside_R_but_ranked_below_top_k | 63 | no |
| toy_61x83 | 13 | 61 | yes | factor_offset_inside_R_but_ranked_below_top_k | 89 | no |
| toy_89x113 | 14 | 89 | yes | factor_offset_inside_R_but_ranked_below_top_k | 131 | no |
| continuation_00_131101x144203 | 35 | 131101 | yes | factor_offset_inside_R_but_ranked_below_top_k | 192281 | no |
| continuation_01_1048583x1153441 | 41 | 1048583 | no | public_window_insufficient_coverage | - | no |

## Classification (Grok decision)

All prior 'one_factor_success' claims from the invalidated scaling scripts
(sparse_web_first_coverage_scale.py, sparse_web_scaling_ladder.py, ratio audit)
are INVALIDATED. They used radius = min(p, q) and constructed the candidate
hole set directly from the secret p/q offsets before scoring.

Under the corrected public contract the first simple policy
(sparse 2-3-5 first-thread proximity ranking inside a fixed public R) produces:

- one_factor_in_public_top_k: 0 / 6
- factor_inside_R_but_too_low_rank: 5 / 6
- public_window_insufficient_coverage (R too small for factor offset): 1 / 6

Plain result: the cheap public nomination by proximity of 2-3-5 hits
does not place the hidden-factor offsets (p or q) inside the reported top-20
for any tested case where coverage was even possible. The large-offset p/q
are always buried far down the list (rank hundreds to tens of thousands).

Therefore the 255-bit 'scale-up' result is not evidence of public factor recovery.
It is a boundary measurement of a public window policy that cannot reach the
necessary offsets without knowledge of p/q.
