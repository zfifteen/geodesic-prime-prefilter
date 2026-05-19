# Reciprocal Shadow Vote 64-Bit New Rungs

## Contract

This run tests only the new rungs above the existing 48-bit ladder.
The reciprocal-shadow score and fixed observation radius are unchanged.
The radius is `300` and the lower audit factor is built at
`97 / 100` of the target square-root scale.

Each rung streams prime lower-endpoint candidates downward from
`floor(sqrt(N))` and stops at the first audit hit on either hidden
factor. One factor is the success condition.

## Results

| bits | N | p | q | hit factor | hit candidate | streamed until hit | coherence | heldout rows | direct rows removed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 52 | 2251800397873129 | 46029491 | 48920819 | 46029491 | 46029491 | 80539 | 1.000000 | 580 | 0 |
| 56 | 36028801434106567 | 184118047 | 195683161 | 184118047 | 184118047 | 299144 | 1.000000 | 583 | 0 |
| 60 | 576460775398492357 | 736472593 | 782732149 | 736472593 | 736472593 | 1114417 | 1.000000 | 586 | 0 |
| 64 | 9223372071187795567 | 2945890471 | 3130928377 | 2945890471 | 2945890471 | 4174647 | 1.000000 | 581 | 0 |

## Measured Surface

```text
new_rungs = 4
one_factor_success = 4 / 4
max_bits = 64
fixed_radius = 300
```

## Boundary

This is a measured new-rung extension of the indirect-web hypothesis.
It is not a universal theorem and not a live factor resolver.
