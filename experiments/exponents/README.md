# PGS Exponent-Tail Probe

Prime powers are the first place where exponents enter the recursive PGS
obstruction language directly.

The width-2 twin-prime chamber already exposes prime-power tail material:

```text
q | q+1 | q+2
```

When `q+2` is composite, least-factor peeling either exits into fixed-point
material, exits into distinct-semiprime material, or carries forward through
multi-prime material. Sometimes the peel reaches prime-power tail material.
That tail has an exponent pattern.

The toy question is:

```text
Do exposed prime-power exponents cluster by strip depth, residue path, scale,
or chamber state?
```

## Current Hypothesis

```text
Prime-power tails are strip-depth clocks in the recursive PGS obstruction
language.
```

In plain terms: the exponent may remember how long the endpoint obstruction
kept shedding least factors before repeated-prime structure was exposed.

## Input Surface

This experiment reads existing twin-primes obstruction artifacts. It does not
rerun the twin-primes scans.

The current inputs are:

```text
experiments/twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_higher_rows.csv
experiments/twin-primes/output/twin_prime_fourth_strip_pressure_probe/fourth_strip_rows.csv
experiments/twin-primes/output/twin_prime_fifth_strip_pressure_probe/fifth_strip_rows.csv
experiments/twin-primes/output/twin_prime_sixth_strip_pressure_probe/sixth_strip_rows.csv
```

## Outputs

```text
experiments/exponents/output/pgs_exponent_tail_probe/summary.json
experiments/exponents/output/pgs_exponent_tail_probe/exponent_tail_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/dominant_residue_path_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/high_exponent_tail_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/base_path_pressure_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/path_pressure_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/path_shape_pressure_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/carrier_capacity_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/decade_next_layer_pressure_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/decade_carrier_capacity_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/depth_exponent_rows.csv
experiments/exponents/output/pgs_exponent_tail_probe/residue_exponent_rows.csv
experiments/exponents/output/mersenne_boundary_contract_probe/summary.json
experiments/exponents/output/mersenne_boundary_contract_probe/boundary_contract_rows.csv
experiments/exponents/output/mersenne_boundary_contract_probe/boundary_failure_rows.csv
experiments/exponents/output/mersenne_known_endpoint_validation/summary.json
experiments/exponents/output/mersenne_known_endpoint_validation/mersenne_chamber_rows.csv
```

## First Signal To Chase

The initial run found a dominant peeled residue path:

```text
7->7->7
```

Measured on the current surface:

```text
total exponent-tail rows: 15
7->7->7 rows: 7
high-exponent tails: 2
high-exponent tails on 7->7->7: 2
base third-higher denominator rows: 183
7->7->7 denominator rows: 47
7->7->7 tail rate inside denominator: 7 / 47
7->7->7 high-exponent rate inside denominator: 2 / 47
```

This path carries the largest square-tail cell and every exposed tail with
exponent greater than `2` in the current surface.

The denominator pressure makes the signal sharper. The `7->7->7` path is not
just present among tails; it is the largest third-higher denominator cell and
the only observed carrier of exponent patterns greater than `2`.

The path-shape pressure makes it sharper again:

```text
mixed paths: 124 rows, 6 tails, 0 high-exponent tails
repeated_7: 47 rows, 7 tails, 2 high-exponent tails
repeated_11: 8 rows, 0 tails, 0 high-exponent tails
repeated_13: 3 rows, 1 tail, 0 high-exponent tails
repeated_29: 1 row, 0 tails, 0 high-exponent tails
```

The current signal is therefore not just repeated residue. It is the repeated
least-factor residue `7` carrier.

The carrier-capacity comparison explains why `7` is the high-exponent carrier
on this measured surface:

```text
repeated_7: 47 rows, capacity floor(1000000 / 7^3) = 2915, 2 high-exponent tails
repeated_11: 8 rows, capacity floor(1000000 / 11^3) = 751, 0 high-exponent tails
repeated_13: 3 rows, capacity floor(1000000 / 13^3) = 455, 0 high-exponent tails
repeated_29: 1 row, capacity floor(1000000 / 29^3) = 41, 0 high-exponent tails
```

The two high-exponent tails are `13^3 = 2197` and `7^4 = 2401`. Both fit
inside the `7^3` post-peel window. The larger repeated carriers leave smaller
windows and have much lower denominator occupancy on this surface, so they do
not expose the same high-exponent tail material here.

## Scale Increase

The same carrier-pressure analyzer now reads the decade-ladder next-layer
surface from `10^7` through `10^18`.

Measured on the `852` sampled next-layer rows:

```text
mixed paths: 729
repeated_7: 95
repeated_11: 16
repeated_13: 5
repeated_17: 4
repeated_19: 2
repeated_23: 1
```

At the `10^18` rung:

```text
repeated_7: 12 / 154 next-layer rows, capacity floor(10^18 / 7^3) = 2915451895043731
repeated_11: 3 / 154 next-layer rows, capacity floor(10^18 / 11^3) = 751314800901577
repeated_17: 1 / 154 next-layer rows, capacity floor(10^18 / 17^3) = 203541624262161
```

The scale increase preserves the same ordering: repeated `7` remains the
dominant repeated least-factor carrier, and it keeps the largest post-triple
capacity at every tested decade.

## Live PGS Boundary Recovery

The live Mersenne-side research path recovers a boundary from the exponent wall
itself. For each prime exponent `p <= 127`, the probe starts at:

```text
exponent wall: 2^p
```

It scans left with exact divisor-count state and stops at the first integer
with divisor count `2`. That recovered integer is the PGS left boundary
`L_p`. The load-bearing measurement is:

```text
boundary distance = 2^p - L_p
```

The boundary survives exactly when the distance is `1`, meaning the recovered
PGS boundary is `2^p - 1`.

Measured result through `p <= 127`:

```text
prime exponents tested: 31
boundary survival count: 12
boundary leak count: 19
candidate-prime audit count: 12
candidate-composite audit count: 19
audit false positives: 0
audit false negatives: 0
```

The live boundary recovery does not use `prevprime`, `nextprime`, `isprime`,
known Mersenne exponent lists, or endpoint lookup logic to choose the boundary.
Exact factorization and candidate divisor signatures are sidecar audit fields
after the PGS boundary has already been recovered.

On this surface, every candidate-prime audit row has boundary distance `1`, and
every candidate-composite audit row has boundary distance greater than `1`.

The offset-2 selected-cell pattern is not the full separator:

```text
survivor second-cell selected count: 9 / 12
leak second-cell selected count: 0 / 19
```

The quotient-prime pattern is also not the full separator:

```text
candidate-prime audit rows with (2^p + 1) / 3 prime: 10 / 12
candidate-composite audit rows with (2^p + 1) / 3 prime: 5 / 19
```

The exact separator in this measured exponent range is therefore boundary
survival, not the later second-cell or quotient-prime condition.

## Post-Run Known-Endpoint Validation

The known-endpoint validation is separate from the live PGS path. It begins
from known Mersenne prime endpoints and uses classical endpoint lookup to
inspect the chamber immediately to the right. It validates and explains the
local chamber shape after the endpoint is already known; it does not recover
the boundary.

For a known Mersenne prime `q = 2^p - 1`, the first interior integer is forced:

```text
q | 2^p | 2^p + 1
```

The first interior cell carries the exponent directly because
`tau(2^p) = p + 1`. The measured relation is that this pure power is a
divisor-load wall, not the selected chamber integer.

Measured for known Mersenne prime endpoints inside the `10^18` scale ceiling:

```text
Mersenne prime endpoints: 8
nontrivial endpoints with p > 2: 7
nontrivial right-power selected count: 0
nontrivial second-cell selected count: 7
nontrivial minimizer offset distribution: offset 2, count 7
```

The concrete validation pattern is:

```text
2^p      has tau p + 1
2^p + 1  is divisible by 3 for odd p
(2^p + 1) / 3 is prime in all nontrivial measured rows
```

On these known endpoints, `2^p + 1` has divisor count `3` or `4` and is always
the leftmost minimum-divisor interior integer. The exponent is visible as load
at offset `1`, while the chamber selection moves one step right to offset `2`.

## Run

```text
python3 experiments/exponents/scripts/pgs_exponent_tail_probe.py \
  --output-dir experiments/exponents/output/pgs_exponent_tail_probe

python3 experiments/exponents/scripts/mersenne_boundary_contract_probe.py \
  --output-dir experiments/exponents/output/mersenne_boundary_contract_probe

python3 experiments/exponents/validation/mersenne_known_endpoint_validation.py \
  --output-dir experiments/exponents/output/mersenne_known_endpoint_validation
```

## Interpret

If the same exponent patterns concentrate at specific strip depths and residue
paths, the exponent-tail surface is structured.

If exponent patterns spread broadly across depths and residue paths, this toy
width-2 surface is a weak place to look for exponent structure.
