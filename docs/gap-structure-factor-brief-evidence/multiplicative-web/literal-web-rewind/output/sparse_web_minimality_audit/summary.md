# Sparse Web Minimality Audit

This audit checks whether the current successful policy is minimal on the four-toy surface.

The diversity gate requires at least three distinct public thread values. Therefore every one-thread and two-thread dense policy is classified before scoring as `insufficient_thread_diversity`.

## Dense Thread-Set Audit

| policy | cases | one-factor successes | classifications | total trials |
| --- | ---: | ---: | --- | ---: |
| dense_first_2 | 4 | 0 | insufficient_thread_diversity:4 | 5273 |
| dense_first_3 | 4 | 0 | insufficient_thread_diversity:4 | 3957 |
| dense_first_5 | 4 | 0 | insufficient_thread_diversity:4 | 3297 |
| dense_first_7 | 4 | 0 | insufficient_thread_diversity:4 | 3083 |
| dense_first_11 | 4 | 0 | insufficient_thread_diversity:4 | 2907 |
| dense_first_2_3 | 4 | 0 | insufficient_thread_diversity:4 | 7253 |
| dense_first_2_5 | 4 | 0 | insufficient_thread_diversity:4 | 6921 |
| dense_first_2_7 | 4 | 0 | insufficient_thread_diversity:4 | 6814 |
| dense_first_2_11 | 4 | 0 | insufficient_thread_diversity:4 | 6728 |
| dense_first_3_5 | 4 | 0 | insufficient_thread_diversity:4 | 6154 |
| dense_first_3_7 | 4 | 0 | insufficient_thread_diversity:4 | 6012 |
| dense_first_3_11 | 4 | 0 | insufficient_thread_diversity:4 | 5895 |
| dense_first_5_7 | 4 | 0 | insufficient_thread_diversity:4 | 5765 |
| dense_first_5_11 | 4 | 0 | insufficient_thread_diversity:4 | 5623 |
| dense_first_7_11 | 4 | 0 | insufficient_thread_diversity:4 | 5574 |
| dense_first_2_3_5 | 4 | 4 | one_factor_success:4 | 8351 |
| dense_first_2_3_7 | 4 | 4 | one_factor_success:4 | 8280 |
| dense_first_2_3_11 | 4 | 4 | one_factor_success:4 | 8222 |
| dense_first_2_5_7 | 4 | 4 | one_factor_success:4 | 8154 |
| dense_first_2_5_11 | 4 | 4 | one_factor_success:4 | 8088 |
| dense_first_2_7_11 | 4 | 4 | one_factor_success:4 | 8061 |
| dense_first_3_5_7 | 4 | 4 | one_factor_success:4 | 7802 |
| dense_first_3_5_11 | 4 | 4 | one_factor_success:4 | 7704 |
| dense_first_3_7_11 | 4 | 4 | one_factor_success:4 | 7674 |
| dense_first_5_7_11 | 4 | 4 | one_factor_success:4 | 7757 |

## Presence-Only Dense Audit

This removes the exponent-peeling work. The web only uses whether a public factor thread exists, so multiplicity is unnecessary for this experiment.

| policy | cases | one-factor successes | classifications | total trials |
| --- | ---: | ---: | --- | ---: |
| presence_first_2 | 4 | 0 | insufficient_thread_diversity:4 | 2640 |
| presence_first_3 | 4 | 0 | insufficient_thread_diversity:4 | 2640 |
| presence_first_5 | 4 | 0 | insufficient_thread_diversity:4 | 2640 |
| presence_first_7 | 4 | 0 | insufficient_thread_diversity:4 | 2640 |
| presence_first_11 | 4 | 0 | insufficient_thread_diversity:4 | 2640 |
| presence_first_2_3 | 4 | 0 | insufficient_thread_diversity:4 | 3960 |
| presence_first_2_5 | 4 | 0 | insufficient_thread_diversity:4 | 3960 |
| presence_first_2_7 | 4 | 0 | insufficient_thread_diversity:4 | 3960 |
| presence_first_2_11 | 4 | 0 | insufficient_thread_diversity:4 | 3960 |
| presence_first_3_5 | 4 | 0 | insufficient_thread_diversity:4 | 4399 |
| presence_first_3_7 | 4 | 0 | insufficient_thread_diversity:4 | 4399 |
| presence_first_3_11 | 4 | 0 | insufficient_thread_diversity:4 | 4399 |
| presence_first_5_7 | 4 | 0 | insufficient_thread_diversity:4 | 4752 |
| presence_first_5_11 | 4 | 0 | insufficient_thread_diversity:4 | 4752 |
| presence_first_7_11 | 4 | 0 | insufficient_thread_diversity:4 | 4903 |
| presence_first_2_3_5 | 4 | 4 | one_factor_success:4 | 4839 |
| presence_first_2_3_7 | 4 | 4 | one_factor_success:4 | 4839 |
| presence_first_2_3_11 | 4 | 4 | one_factor_success:4 | 4839 |
| presence_first_2_5_7 | 4 | 4 | one_factor_success:4 | 5016 |
| presence_first_2_5_11 | 4 | 4 | one_factor_success:4 | 5016 |
| presence_first_2_7_11 | 4 | 4 | one_factor_success:4 | 5091 |
| presence_first_3_5_7 | 4 | 4 | one_factor_success:4 | 5807 |
| presence_first_3_5_11 | 4 | 4 | one_factor_success:4 | 5807 |
| presence_first_3_7_11 | 4 | 4 | one_factor_success:4 | 5907 |
| presence_first_5_7_11 | 4 | 4 | one_factor_success:4 | 6561 |

## Center-Out Discovery Audit

| case | policy | touched | trials | public threads | recovered factor | rank | classification |
| --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| toy_23x31 | center_out_until_3_first_2_3_5 | 4 | 14 | 2, 3, 5 | 23 | 2 | one_factor_success |
| toy_43x59 | center_out_until_3_first_2_3_5 | 16 | 49 | 2, 3, 5 | 43 | 3 | one_factor_success |
| toy_61x83 | center_out_until_3_first_2_3_5 | 4 | 13 | 2, 3, 5 |  | 6 | signal_failure |
| toy_89x113 | center_out_until_3_first_2_3_5 | 4 | 13 | 2, 3, 5 |  | 8 | signal_failure |

## Result

`2,3,5` is minimal by public-thread count under the three-thread diversity gate.
Dense `2,3,5` succeeds on all four toys and is the successful policy with the smallest prime ceiling in this audit.
Presence-only `2,3,5` removes unnecessary multiplicity extraction and ties for the lowest trial count among successful three-thread policies with the same first two tests.
The center-out acquisition that stops as soon as it discovers `2`, `3`, and `5` is not sufficient on this surface: it succeeds on the first two toys and fails on the last two.
