# Sparse Web First Slice

Policy: `trial_2_stop_1`.

Extractor: dense offsets, trial division only by `2`, record multiplicity, stop.

Scoring gate: at least `3` distinct public thread values before one-factor scoring.

| case | public r count | classification | one-factor | two-factor | best hidden rank | top18 direct hits | touched | trials | zero-yield | seconds |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| toy_23x31 | 1 | insufficient_thread_diversity | false | false | 1 | 14 | 360 | 716 | 180 | 0.000534 |
| toy_43x59 | 1 | insufficient_thread_diversity | false | false | 1 | 10 | 520 | 1038 | 260 | 0.000439 |
| toy_61x83 | 1 | insufficient_thread_diversity | false | false | 1 | 10 | 720 | 1440 | 360 | 0.000564 |
| toy_89x113 | 1 | insufficient_thread_diversity | false | false | 1 | 10 | 1040 | 2079 | 520 | 0.000966 |

## Measured Result

`trial_2_stop_1` reaches only one public thread value, `r = 2`, on every toy case.
Under the v1.0 contract, each run is classified `insufficient_thread_diversity` before hidden-thread scoring.
This is an informative lower bound: parity alone creates a comb, not a multiplicative web with public-thread intersections.
