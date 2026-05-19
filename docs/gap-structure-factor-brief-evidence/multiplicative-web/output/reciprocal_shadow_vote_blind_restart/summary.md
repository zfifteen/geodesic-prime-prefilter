# Reciprocal Shadow Vote Blind Restart

## Contract

This restart uses `p` and `q` only for case construction and final audit.
The candidate stream begins at public `floor(sqrt(N))`, scans downward
in fixed public segments, scores every prime candidate it sees, and
stops only after a scored candidate has been checked against the audit
factors.

No hidden factor is used as a candidate bound, filter, or scoring input.

## Results

| bits | N | hit factor | hit candidate | scored until hit | segments | coherence | rows | threads | direct audit rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20 | 526451 | 701 | 701 | 3 | 1 | 1.000000 | 548 | 1673 | 0 |
| 24 | 8406197 | 2803 | 2803 | 11 | 1 | 1.000000 | 572 | 1813 | 0 |
| 28 | 134230823 | 11213 | 11213 | 37 | 1 | 1.000000 | 561 | 1897 | 0 |
| 32 | 2147679749 | 44939 | 44939 | 124 | 1 | 1.000000 | 565 | 1969 | 0 |
| 36 | 34359791299 | 179801 | 179801 | 458 | 1 | 1.000000 | 569 | 2027 | 0 |
| 40 | 549758053997 | 719203 | 719203 | 1658 | 1 | 1.000000 | 571 | 2109 | 0 |
| 44 | 8796138413641 | 2876833 | 2876833 | 5949 | 1 | 1.000000 | 580 | 2173 | 0 |
| 48 | 140737552370539 | 11507371 | 11507371 | 21900 | 1 | 1.000000 | 578 | 2245 | 0 |
| 52 | 2251800397873129 | 46029491 | 46029491 | 80539 | 2 | 1.000000 | 580 | 2299 | 0 |

## Measured Surface

```text
rungs = 9
one_factor_success = 9 / 9
max_bits = 52
fixed_radius = 300
candidate_lower_bound = public scan to 2
hidden_factor_candidate_bound = none
```

## Boundary

This is a blind restart of the measured ladder. It still uses
candidate enumeration and exact neighboring-composite factorization,
so it is not a scalable resolver.
