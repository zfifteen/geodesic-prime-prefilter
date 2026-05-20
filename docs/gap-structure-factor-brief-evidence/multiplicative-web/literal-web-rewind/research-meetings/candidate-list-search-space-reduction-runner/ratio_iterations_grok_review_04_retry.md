# Ratio Iteration 04 Grok Review Retry

Choose exactly one next setting. No code execution.

Iteration 03 setting:

```text
thread_count_ratio = 1/2
depth_ratio = 4/12
retention_divisor = 512
```

Iteration 03 result:

```text
hit_rate = 0/10
median_emitted_count = 72.0
median_candidate_reduction_bits = 9.0
```

Key public facts:

```text
53-bit case: active_thread_count=14, min_depth=5, max_candidates=131072,
emitted=105886, pre_cap=105886, cap_active=false, status=missed.
47-bit case: active_thread_count=13, min_depth=5, emitted=16384,
pre_cap=35524, cap_active=true, status=missed.
```

Interpretation: retention and one-step depth relaxation did not work. The largest case was cap-inactive and still missed. The next likely single-variable test is increasing the thread alphabet again.

Return exactly:

```text
approved_next_setting:
thread_count_ratio = ?
depth_ratio = ?
retention_divisor = ?
reason = ?
```

Use public observables only. No private ranks, no containment diagnostics.
