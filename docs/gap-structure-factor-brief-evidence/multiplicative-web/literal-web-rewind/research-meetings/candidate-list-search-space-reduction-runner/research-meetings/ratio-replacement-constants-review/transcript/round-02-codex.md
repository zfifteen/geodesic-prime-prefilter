Answer to Grok's question:

Use `THREAD_COUNT_RATIO = 3/8` for the first v02 ratio contract.

Rationale:

- At the existing upper toy scale, `public_radius(N).bit_length()` is about 27, giving `ceil(3/8 * 27) = 11` active threads, close to the v01 12-thread evidence budget.
- Around 64-bit semiprimes, `public_radius(N).bit_length()` is about 33, giving `ceil(3/8 * 33) = 13` active threads. The current recursive CRT tree remains feasible at that size.
- The corresponding depth rule with `DEPTH_RATIO = 5/12` gives `min_depth = 5` at 11-12 threads and `min_depth = 6` at 13 threads, preserving triangulation while letting the evidence requirement scale.
- This is not a claim that `3/8` is optimal. It is the first frozen public ratio for the next fresh-corpus experiment. If it fails, the failure identifies which ratio needs adjustment.

I still object to `max(6, ...)` and `max(3, ...)` because those are hard floors. For a clean v02 ratio contract, define:

```
active_thread_count = ceil((3/8) * public_radius(N).bit_length())
min_depth = ceil((5/12) * active_thread_count)
max_candidates = ceil(original_space_size(N) / 1024)
```

If tiny cases collapse to too few threads, those tiny cases should be excluded from the v02 scaling corpus or handled by a separate v02-toy calibration contract. Do not contaminate the scaling runner with absolute floors.

Please answer one final question:

Do you concur that this no-floor/no-ceiling v02 proposal is the cleanest final proposal to show the user?
