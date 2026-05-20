# Ratio Iteration 05 Grok Review Request

Choose exactly one next setting. No code execution.

Iteration 04 setting:

```text
thread_count_ratio = 5/8
depth_ratio = 4/12
retention_divisor = 512
```

Iteration 04 result:

```text
hit_rate = 0/10
median_emitted_count = 72.0
median_candidate_reduction_bits = 9.0
```

Key public facts:

```text
All 10 cases missed.
All 10 cases had cap_active=true.
53-bit case: active_thread_count=18, min_depth=6, max_candidates=131072,
emitted=131072, pre_cap=284797, cap_active=true, status=missed.
47-bit case: active_thread_count=16, min_depth=6, emitted=16384,
pre_cap=71163, cap_active=true, status=missed.
Small cases still emit only 1 or 2 candidates because retention_divisor is too large relative to original_space_size.
```

Interpretation: increasing thread ratio created many more qualified candidates and computational pressure, but still no recovery. Retention is again binding everywhere. A much lower retention divisor may be the next single-variable test.

Return exactly:

```text
approved_next_setting:
thread_count_ratio = ?
depth_ratio = ?
retention_divisor = ?
reason = ?
```

Use public observables only. No private ranks, no containment diagnostics.
