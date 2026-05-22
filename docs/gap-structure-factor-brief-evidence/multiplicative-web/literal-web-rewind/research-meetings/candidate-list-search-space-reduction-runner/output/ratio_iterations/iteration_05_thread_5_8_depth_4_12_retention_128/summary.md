# Ratio Probe Iteration Summary

- thread_count_ratio: `5/8`
- depth_ratio: `4/12`
- retention_divisor: `128`
- hit_rate: `0/10`
- median_emitted_count: `288.0`
- median_candidate_reduction_bits: `7.0`

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status | recovered |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| `toy_989` | 10 | 4 | 2 | 1 | 1 | 8 | `True` | 4.0 | `missed` | `None` |
| `toy_9379` | 14 | 5 | 2 | 1 | 1 | 20 | `True` | 6.0 | `missed` | `None` |
| `toy_25807` | 15 | 6 | 2 | 1 | 1 | 45 | `True` | 7.0 | `missed` | `None` |
| `toy_1242079` | 21 | 8 | 3 | 8 | 8 | 180 | `True` | 7.0 | `missed` | `None` |
| `toy_200250077` | 28 | 10 | 4 | 64 | 64 | 781 | `True` | 7.0 | `missed` | `None` |
| `toy_4295229443` | 33 | 12 | 4 | 512 | 512 | 3364 | `True` | 7.0 | `missed` | `None` |
| `toy_18902665303` | 35 | 12 | 4 | 1024 | 1024 | 4730 | `True` | 7.0 | `missed` | `None` |
| `toy_1209476905903` | 41 | 14 | 5 | 8192 | 8192 | 15356 | `True` | 7.0 | `missed` | `None` |
| `toy_77468500194643` | 47 | 16 | 6 | 65536 | 65536 | 71163 | `True` | 7.0 | `missed` | `None` |
| `toy_4951764003343009` | 53 | 18 | 6 | 524288 | 284797 | 284797 | `False` | 7.880425576267019 | `missed` | `None` |
