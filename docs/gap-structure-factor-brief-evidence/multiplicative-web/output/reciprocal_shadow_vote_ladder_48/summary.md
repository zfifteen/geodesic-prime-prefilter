# Reciprocal Shadow Vote 48-Bit Ladder

## Contract

The ladder keeps the reciprocal-shadow score and the fixed observation
radius `300`. Only `N = p q` changes across rungs.
The lower audit factor is constructed at `97 / 100` of the target square-root scale.

Each rung streams prime lower-endpoint candidates downward from
`floor(sqrt(N))` and stops at the first audit hit on either hidden
factor. One factor is the success condition.

## Results

| bits | N | p | q | hit factor | hit candidate | scored until hit | candidates below sqrt | coherence | heldout rows | direct rows removed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 16 | 33043 | 173 | 191 | 173 | 173 | 3 | 42 | 1.000000 | 537 | 4 |
| 20 | 526451 | 701 | 751 | 701 | 701 | 3 | 128 | 1.000000 | 548 | 0 |
| 24 | 8406197 | 2803 | 2999 | 2803 | 2803 | 11 | 419 | 1.000000 | 572 | 0 |
| 28 | 134230823 | 11213 | 11971 | 11213 | 11213 | 37 | 1393 | 1.000000 | 561 | 0 |
| 32 | 2147679749 | 44939 | 47791 | 44939 | 44939 | 124 | 4792 | 1.000000 | 565 | 0 |
| 36 | 34359791299 | 179801 | 191099 | 179801 | 179801 | 458 | 16777 | 1.000000 | 569 | 0 |
| 40 | 549758053997 | 719203 | 764399 | 719203 | 719203 | 1658 | 59631 | 1.000000 | 571 | 0 |
| 44 | 8796138413641 | 2876833 | 3057577 | 2876833 | 2876833 | 5949 | 214516 | 1.000000 | 580 | 0 |
| 48 | 140737552370539 | 11507371 | 12230209 | 11507371 | 11507371 | 21900 | 779638 | 1.000000 | 578 | 0 |

## Measured Surface

```text
rungs = 9
one_factor_success = 9 / 9
max_bits = 48
fixed_radius = 300
```

## Boundary

This is a measured ladder for the indirect-web hypothesis. It is not
a universal theorem and not a live factor resolver.
