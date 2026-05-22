# Ratio Probe Iteration Summary

- thread_count_ratio: `5/8`
- depth_ratio: `4/12`
- retention_divisor: `512`
- hit_rate: `0/10`
- median_emitted_count: `72.0`
- median_candidate_reduction_bits: `9.0`

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status | recovered |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| `toy_989` | 10 | 4 | 2 | 1 | 1 | 8 | `True` | 4.0 | `missed` | `None` |
| `toy_9379` | 14 | 5 | 2 | 1 | 1 | 20 | `True` | 6.0 | `missed` | `None` |
| `toy_25807` | 15 | 6 | 2 | 1 | 1 | 45 | `True` | 7.0 | `missed` | `None` |
| `toy_1242079` | 21 | 8 | 3 | 2 | 2 | 180 | `True` | 9.0 | `missed` | `None` |
| `toy_200250077` | 28 | 10 | 4 | 16 | 16 | 781 | `True` | 9.0 | `missed` | `None` |
| `toy_4295229443` | 33 | 12 | 4 | 128 | 128 | 3364 | `True` | 9.0 | `missed` | `None` |
| `toy_18902665303` | 35 | 12 | 4 | 256 | 256 | 4730 | `True` | 9.0 | `missed` | `None` |
| `toy_1209476905903` | 41 | 14 | 5 | 2048 | 2048 | 15356 | `True` | 9.0 | `missed` | `None` |
| `toy_77468500194643` | 47 | 16 | 6 | 16384 | 16384 | 71163 | `True` | 9.0 | `missed` | `None` |
| `toy_4951764003343009` | 53 | 18 | 6 | 131072 | 131072 | 284797 | `True` | 9.0 | `missed` | `None` |
