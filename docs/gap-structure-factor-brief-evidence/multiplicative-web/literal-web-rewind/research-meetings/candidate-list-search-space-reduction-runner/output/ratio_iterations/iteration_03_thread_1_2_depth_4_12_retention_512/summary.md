# Ratio Probe Iteration Summary

- thread_count_ratio: `1/2`
- depth_ratio: `4/12`
- retention_divisor: `512`
- hit_rate: `0/10`
- median_emitted_count: `72.0`
- median_candidate_reduction_bits: `9.0`

| case | N bits | active threads | min depth | max candidates | emitted | pre-cap | cap active | reduction bits | status | recovered |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|---|
| `toy_989` | 10 | 3 | 1 | 1 | 1 | 7 | `True` | 4.0 | `missed` | `None` |
| `toy_9379` | 14 | 4 | 2 | 1 | 1 | 17 | `True` | 6.0 | `missed` | `None` |
| `toy_25807` | 15 | 5 | 2 | 1 | 1 | 38 | `True` | 7.0 | `missed` | `None` |
| `toy_1242079` | 21 | 6 | 2 | 2 | 2 | 114 | `True` | 9.0 | `missed` | `None` |
| `toy_200250077` | 28 | 8 | 3 | 16 | 16 | 525 | `True` | 9.0 | `missed` | `None` |
| `toy_4295229443` | 33 | 9 | 3 | 128 | 128 | 1620 | `True` | 9.0 | `missed` | `None` |
| `toy_18902665303` | 35 | 10 | 4 | 256 | 256 | 2891 | `True` | 9.0 | `missed` | `None` |
| `toy_1209476905903` | 41 | 11 | 4 | 2048 | 2048 | 6891 | `True` | 9.0 | `missed` | `None` |
| `toy_77468500194643` | 47 | 13 | 5 | 16384 | 16384 | 35524 | `True` | 9.0 | `missed` | `None` |
| `toy_4951764003343009` | 53 | 14 | 5 | 131072 | 105886 | 105886 | `False` | 9.30784767339783 | `missed` | `None` |
