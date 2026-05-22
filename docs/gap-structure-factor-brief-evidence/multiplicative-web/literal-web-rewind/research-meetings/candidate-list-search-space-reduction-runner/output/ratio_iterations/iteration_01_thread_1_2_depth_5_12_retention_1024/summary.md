# Ratio Probe Iteration Summary

- thread_count_ratio: `1/2`
- depth_ratio: `5/12`
- retention_divisor: `1024`
- hit_rate: `0/10`
- median_emitted_count: `36.0`
- median_candidate_reduction_bits: `10.0`

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status | recovered |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| `toy_989` | 10 | 3 | 2 | 1 | 1 | 7 | `True` | 4.0 | `missed` | `None` |
| `toy_9379` | 14 | 4 | 2 | 1 | 1 | 17 | `True` | 6.0 | `missed` | `None` |
| `toy_25807` | 15 | 5 | 3 | 1 | 1 | 34 | `True` | 7.0 | `missed` | `None` |
| `toy_1242079` | 21 | 6 | 3 | 1 | 1 | 112 | `True` | 10.0 | `missed` | `None` |
| `toy_200250077` | 28 | 8 | 4 | 8 | 8 | 506 | `True` | 10.0 | `missed` | `None` |
| `toy_4295229443` | 33 | 9 | 4 | 64 | 64 | 1599 | `True` | 10.0 | `missed` | `None` |
| `toy_18902665303` | 35 | 10 | 5 | 128 | 128 | 2735 | `True` | 10.0 | `missed` | `None` |
| `toy_1209476905903` | 41 | 11 | 5 | 1024 | 1024 | 6696 | `True` | 10.0 | `missed` | `None` |
| `toy_77468500194643` | 47 | 13 | 6 | 8192 | 8192 | 33795 | `True` | 10.0 | `missed` | `None` |
| `toy_4951764003343009` | 53 | 14 | 6 | 65536 | 65536 | 103680 | `True` | 10.0 | `missed` | `None` |
