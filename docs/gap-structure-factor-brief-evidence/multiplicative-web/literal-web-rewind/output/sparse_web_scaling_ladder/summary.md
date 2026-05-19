# Sparse Web Scaling Ladder

Frozen method: dense presence-only public threads `2,3,5`; first public thread only; no exponent extraction.

Radius schedule: `max(16384, 1 << max(0, ((N.bit_length()+1)//2 - 5)))`, doubled up to 6 times, capped at `268435456`.

| rung | bits | p | q | radius | radius/min(p,q) | classification | recovered | rank | trials | seconds |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| toy_23x31 | 10 | 23 | 31 | 16384 | 712.348 | one_factor_success | 23 | 1 | 31336 | 0.001315 |
| toy_43x59 | 12 | 43 | 59 | 16384 | 381.023 | one_factor_success | 43 | 1 | 34680 | 0.000566 |
| toy_61x83 | 13 | 61 | 83 | 16384 | 268.590 | one_factor_success | 83 | 1 | 39311 | 0.000423 |
| toy_89x113 | 14 | 89 | 113 | 16384 | 184.090 | one_factor_success | 113 | 1 | 48467 | 0.000342 |
| rung_04_101x137 | 14 | 101 | 137 | 16384 | 162.218 | signal_failure | 101 | 17 | 55397 | 0.000439 |

## Stop

Stopped at rung_04_101x137: covering radius reached but exact factor was not in the top 5.
