# Ratio Iteration Summary

## Status

No agreed working ratio setting was found inside the current pure-ratio, no-floor/no-ceiling, fixed-scoring thread-triangulation runner family.

This is a measured implementation result, not a proof about the broader multiplicative-web idea.

## Iteration Rule

Each setting was chosen sequentially from the previous failure and reviewed with Grok before execution. This was not a preset variant ladder.

The public probe received only:

- `N`;
- public ratio settings;
- output path.

Private audit pairs were supplied only after each public freeze log and public manifest were written.

## Tested Settings

| run | thread_count_ratio | depth_ratio | retention_divisor | hit_rate | median_emitted_count | median_reduction_bits |
|---|---:|---:|---:|---:|---:|---:|
| v02 | 3/8 | 5/12 | 1024 | 0/10 | 36.0 | 10.0 |
| iteration 01 | 1/2 | 5/12 | 1024 | 0/10 | 36.0 | 10.0 |
| iteration 02 | 1/2 | 5/12 | 512 | 0/10 | 72.0 | 9.0 |
| iteration 03 | 1/2 | 4/12 | 512 | 0/10 | 72.0 | 9.0 |
| iteration 04 | 5/8 | 4/12 | 512 | 0/10 | 72.0 | 9.0 |
| iteration 05 | 5/8 | 4/12 | 128 | 0/10 | 288.0 | 7.0 |

## Grok Stop Decision

Grok returned:

```text
stop_iteration:

reason = After six settings in the public ratio runner family (v02 through iter05), hit_rate remains 0/10 on the fixed 10-case corpus. The 53-bit case now emits its complete qualified set (284797 distances, min_depth=6, 18 threads, cap_active=false, pre_cap=284797) yet still misses, placing the target outside the distances generable under the current thread_count + depth_ratio controls. The 47-bit (pre_cap=71163, emitted=65536, cap=true) and 33-bit (pre_cap=3364, emitted=512, cap=true) cases remain cap-bound under retention=128, but the largest case demonstrates that the generator itself (first-N odd-prime CRT at depth >= min_depth) does not produce the target for at least one corpus member. Small cases continue to emit 1/1/1/8 because ratio-only retention on small original_space_size structurally cannot allocate more slots without exiting the runner family. No single ratio adjustment (thread, depth, or retention) within the pure-ratio, no-floor, no-ceiling, fixed-scoring family can expand coverage for the observed misses while preserving the runner. Record that no agreed working ratio setting has been found.
```

## Measured Lesson

The ratio conversion was implemented cleanly and audited, but ratio tuning did not restore recovery.

The current public candidate generator is too narrow in mechanism, not merely mis-scaled by one constant. The strongest evidence is the 53-bit case in iteration 05:

```text
active_thread_count = 18
min_depth = 6
pre_cap_qualified_count = 284797
emitted_count = 284797
cap_active = false
status = missed
```

That case emitted the full public qualified set under the tested mechanism and still missed. The failure is therefore not only a retention-cap problem.

## Next Research Boundary

Do not keep tuning these three ratios as if a working setting has been found.

The next runner must change the public candidate-generation mechanism or scoring mechanism, while preserving:

- public generation before audit;
- no hidden factors in inference;
- no private ranks;
- no containment diagnostics as recovery;
- deterministic construction;
- explicit freeze records.

The current ratio runner remains useful as a negative control and as evidence that hard constants were removed without solving recovery.
