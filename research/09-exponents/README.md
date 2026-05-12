# PGS Exponent-Tail Probe

## Migration Note

This chapter moved from `experiments/exponents/` to
`research/09-exponents/` during the repository reorganization. The local test
suite passed after relocation with:

```text
python3 -m pytest research/09-exponents/tests
```

## Object

Mersenne and exponent-wall PGS experiments, including exponent-tail pressure,
toy wall mechanics, Mersenne boundary contracts, and PGS Mersenne-prime
generator probes.

## Invariant Or Rule

The chapter studies PGS structure around exponent walls and preserves the
research distinction between PGS-side generation/probes and downstream
validation.

## Proof Status

No chapter-local proof upgrade is made by this migration. Root theorem status
continues to live in `PROOF.md`.

## Measured Evidence

Measured outputs live under `research/09-exponents/output/`.

## Audit Status

The moved test suite passed after relocation:

```text
python3 -m pytest research/09-exponents/tests
68 passed in 94.24s
```

## Invalidated Rules

No invalidated-rule status changed during migration.

## Unresolved State

No unresolved-state status changed during migration.

## Reproduce

Use the reproduce commands in the command section below. The relocation changed
paths from `experiments/exponents/` to `research/09-exponents/`.

## Provenance

Original home: `experiments/exponents/`.

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
research/10-twin-primes/output/twin_prime_endpoint_fixed_point_decomposition_probe/third_strip_higher_rows.csv
research/10-twin-primes/output/twin_prime_fourth_strip_pressure_probe/fourth_strip_rows.csv
research/10-twin-primes/output/twin_prime_fifth_strip_pressure_probe/fifth_strip_rows.csv
research/10-twin-primes/output/twin_prime_sixth_strip_pressure_probe/sixth_strip_rows.csv
```

## Outputs

```text
research/09-exponents/output/pgs_exponent_tail_probe/summary.json
research/09-exponents/output/pgs_exponent_tail_probe/exponent_tail_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/dominant_residue_path_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/high_exponent_tail_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/base_path_pressure_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/path_pressure_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/path_shape_pressure_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/carrier_capacity_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/decade_next_layer_pressure_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/decade_carrier_capacity_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/depth_exponent_rows.csv
research/09-exponents/output/pgs_exponent_tail_probe/residue_exponent_rows.csv
research/09-exponents/output/toy_exponent_wall_mechanics_probe/summary.json
research/09-exponents/output/toy_exponent_wall_mechanics_probe/pgs_summary.json
research/09-exponents/output/toy_exponent_wall_mechanics_probe/pgs_power_of_two_rows.csv
research/09-exponents/output/toy_exponent_wall_mechanics_probe/validation_summary.json
research/09-exponents/output/toy_exponent_wall_mechanics_probe/validation_rows.csv
research/09-exponents/output/toy_exponent_wall_mechanics_probe/mersenne_location_inferred_rows.csv
research/09-exponents/output/toy_exponent_wall_mechanics_probe/mersenne_location_not_inferred_rows.csv
research/09-exponents/output/mersenne_boundary_contract_probe/summary.json
research/09-exponents/output/mersenne_boundary_contract_probe/boundary_contract_rows.csv
research/09-exponents/output/mersenne_boundary_contract_probe/boundary_failure_rows.csv
research/09-exponents/output/mersenne_known_endpoint_validation/summary.json
research/09-exponents/output/mersenne_known_endpoint_validation/mersenne_chamber_rows.csv
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

## Toy Powers Of Two

The reset experiment has three parts:

```text
PGS mechanism: recovers the nearest prime less than 2^e
validator: checks the PGS rows with classical primality and factorization
controller: runs the PGS mechanism first, then the validator
```

The PGS mechanism starts from powers of two:

```text
W = 2^e
```

For each power of two, the live PGS mechanism checks admissible candidates less
than `2^e` with exact divisor-count state and stops at the first integer with
divisor count `2`. That recovered integer is the nearest prime less than
`2^e`. The first measurement is:

```text
distance = 2^e - left prime
```

PGS infers a Mersenne-prime location exactly when the distance is `1`.

The current rule is `pgs_left_prime_wheel_open_v1`. It does not scan every
integer. It builds bounded candidates for the nearest prime less than `2^e`
from `2`, `3`, `5`, and wheel-open residues, rejects candidates with divisor
count greater than `2`, and fails explicitly if the configured bound does not
resolve.

Measured on the toy surface `e = 2..31`:

```text
candidate bound: 128
powers of two tested: 30
PGS inferred Mersenne locations: 8
PGS did not infer Mersenne locations: 22
classical Mersenne primes: 8
classical composite Mersenne numbers: 22
classical false positives: 0
classical false negatives: 0
```

The dominant distance from `2^e` to the nearest prime less than `2^e` is `3`:

```text
distance 3: 10 rows
distance 1: 8 rows
distance 5: 3 rows
distance 9: 2 rows
distance 15: 2 rows
distance 39: 2 rows
```

Most rows resolve after very few candidate checks:

```text
1 candidate evaluated: 16 rows
2 candidates evaluated: 5 rows
3 candidates evaluated: 2 rows
4 candidates evaluated: 2 rows
```

This toy pass is mechanism-first. The PGS mechanism does not use `prevprime`,
`nextprime`, `isprime`, known Mersenne exponent lists, factorization, or
endpoint lookup logic. Classical primality and factorization are confined to
the validator after the PGS rows have already been emitted.

## Exponent Decade Ladder

The scale ladder grows by exponent:

```text
e <= 31
e <= 100
e <= 1000
```

Each row starts with the exponent itself. The first live measurement is
`tau(e)`. If `tau(e) != 2`, the exponent is recorded as excluded and the
mechanism does not inspect `2^e - 1`.

If `tau(e) == 2`, the mechanism builds bounded wheel-open candidates less than
`2^e` and stops at the first candidate with divisor count `2`. The measured
distance is:

```text
distance = 2^e - left prime
```

PGS infers a Mersenne-prime location exactly when the distance is `1`.

If a candidate does not clear within the configured per-candidate work limit,
the row is recorded as unresolved. The mechanism does not switch to another
method.

The ladder has the same three-part harness as the toy pass:

```text
PGS mechanism: exponent gate, then bounded left-prime recovery
validator: classical endpoint validation after PGS rows exist
controller: runs PGS first, then validation
```

The ladder outputs are:

```text
research/09-exponents/output/exponent_decade_ladder_probe/pgs_ladder_rows.csv
research/09-exponents/output/exponent_decade_ladder_probe/pgs_rung_summary_rows.csv
research/09-exponents/output/exponent_decade_ladder_probe/pgs_cumulative_summary_rows.csv
research/09-exponents/output/exponent_decade_ladder_probe/pgs_summary.json
research/09-exponents/output/exponent_decade_ladder_probe/validation_rows.csv
research/09-exponents/output/exponent_decade_ladder_probe/validation_summary.json
research/09-exponents/output/exponent_decade_ladder_probe/summary.json
research/09-exponents/output/exponent_decade_ladder_probe/mersenne_location_inferred_rows.csv
research/09-exponents/output/exponent_decade_ladder_probe/pgs_unresolved_rows.csv
```

Measured with `candidate_bound = 4096` and a `1.0` second per-candidate work
limit:

```text
rungs: 31, 100, 1000
row model: non-cumulative exponent windows
unique exponents tested: 999
excluded by tau(e) != 2: 831
left-prime resolved rows: 34
left-prime unresolved rows: 134
PGS inferred Mersenne locations: 14
classical Mersenne-prime validations: 14
classical false positives: 0
classical false negatives: 0
```

New exponent window per rung:

```text
2 <= e <= 31:      8 inferred, 0 unresolved
32 <= e <= 100:    2 inferred, 0 unresolved
101 <= e <= 1000:  4 inferred, 134 unresolved
```

Cumulative view:

```text
e <= 31:    8 inferred, 0 unresolved
e <= 100:  10 inferred, 0 unresolved
e <= 1000: 14 inferred, 134 unresolved
```

## PGSMPG v0.1

The Prime Gap Structure Mersenne Prime Generator starts from an accepted
Mersenne exponent and emits the next exponent inferred by PGS.

The contract is only:

```text
accepted Mersenne exponent p -> next Mersenne exponent q
```

The output stream is physically minimal:

```json
{"p": 31, "q": 61}
```

For each candidate exponent `e > p`, the live generator first measures
`tau(e)`. If `tau(e) != 2`, the candidate exponent is excluded before the
generator inspects `2^e - 1`.

If `tau(e) == 2`, the generator mirrors the PGSPG chamber-reset rule around the
wall:

```text
W = 2^e
candidate boundary = W - offset
```

The v0.1 live rule scans leftward through wheel-open boundary candidates and
emits the first exponent whose recovered boundary is at distance `1`.

That full boundary scan is an implementation detail of v0.1, not the permanent
PGSMPG contract. The successor generator does not need the exact nearest-left
prime for every rejected exponent. A rejected candidate exponent only needs
enough PGS state to continue scanning.

Default v0.1 run:

```text
start exponent: 2
chain length requested: 10
max exponent: 127
candidate bound: 4096
emitted transition records: 9
Mersenne exponents recovered: 10
classical validation agreements: 9
unresolved records: 0
```

The recovered exponent chain is:

```text
2, 3, 5, 7, 13, 17, 19, 31, 61, 89
```

The emitted transition records are:

```text
2 -> 3
3 -> 5
5 -> 7
7 -> 13
13 -> 17
17 -> 19
19 -> 31
31 -> 61
61 -> 89
```

The live generator does not use endpoint lookup, factorization, known Mersenne
exponent lists, `prevprime`, `nextprime`, or `isprime`. The validator checks the
emitted records after the PGS rows exist.

## PGSMPG Baseline Cost Stats

The baseline stats harness measures the existing PGSMPG path unchanged.

The measured value ceiling is:

```text
2^p - 1 <= 10^50
```

That gives the exponent ceiling:

```text
p <= 166
```

The recovered Mersenne exponents under this ceiling are:

```text
2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127
```

The harness also records the terminal unresolved scan from `127` through `166`,
so the measurement means: find every PGSMPG Mersenne exponent under `10^50`,
then stop at the ceiling.

Baseline with the current SymPy-backed `tau`:

```text
candidate bound: 4096
resolved transitions: 11
terminal unresolved scans: 1
tau calls: 695
exponent tau calls: 164
boundary tau calls: 531
tau elapsed seconds: 69.73206145729637
maximum tau call seconds: 9.69560304202605
maximum boundary input bit length: 163
```

The terminal scan after `p = 127` dominates the boundary work:

```text
terminal scan attempted exponents: 128..166
terminal scan tau calls: 194
terminal scan boundary tau calls: 155
```

The generator and stats artifacts now store compact integer diagnostics:
exponents, offsets, divisor counts, bit lengths, and timing. They do not write
full `2^p`, `2^p - 1`, left-boundary, or per-candidate integers into sidecar
records. The live scan also evaluates only admissible left offsets. Offsets
that cannot be prime candidates do not receive a divisor-count call.

This keeps the rule scale-independent and prevents artifact size or impossible
candidate offsets from becoming the limiting factor before arithmetic itself
does.

## Direct Tau Replacement Result

A direct thresholded `tau(n, 2)` replacement was tested and rejected as the next
implementation path. This test was run before the admissible-offset cleanup, so
its call count belongs to the earlier full-prefix scan, not the current
optimized v0.1 baseline.

Measured on the same `10^18` surface:

```text
same recovered exponent chain: 2, 3, 5, 7, 13, 17, 19, 31
same tau call count: 475
SymPy-backed tau elapsed seconds: 0.1290664139087312
direct thresholded tau elapsed seconds: 59.748020194878336
direct thresholded maximum tau call seconds: 51.217119958018884
```

The direct thresholded function reduced no candidate surface. It only changed
how each candidate was certified. Prime boundary candidates still required a
full absence-of-divisor check, and that dominated the run.

The result is an invalidated implementation path:

```text
Do not replace the current generator with a direct divisor scan for tau(n, 2).
```

## Residue-Return Side Probe

A disposable side probe tested residue-return gating against the actual PGSMPG
successor contract.

Measured on the `10^18` surface:

```text
current PGSMPG exponents: 2, 3, 5, 7, 13, 17, 19, 31
residue-return gated exponents: 2, 3, 5, 7, 13, 17, 19, 31
current boundary tau calls: 418
residue-return gated boundary tau calls: 10
boundary tau call reduction: 408
```

The side probe preserved the successor output while avoiding exact boundary
recovery for non-surviving candidate exponents. That matches the PGSMPG
contract better than the v0.1 full-boundary scan.

The next implementation target is therefore:

```text
accepted p
scan e > p
exclude e when tau(e) != 2
test offset-1 survival for prime exponents
use residue-return pressure to reject or defer non-survivors
emit the first surviving e
```

Do not compute exact nearest-left-prime distances for non-survivors in PGSMPG
v0.2.

## Mersenne Order-Filter Validation

For a composite Mersenne number `2^p - 1`, any prime factor must satisfy:

```text
factor = 1 mod 2p
factor = 1 or 7 mod 8
```

The validation probe checks this condition on prime exponents `p <= 127`.
The measured surface is:

```text
prime exponents tested: 31
Mersenne-prime rows: 12
composite Mersenne rows: 19
order-filter failures: 0
```

The same probe now measures fixed-point residue return before the least factor
appears. For an order-filter candidate `m`, it computes the distance from
`2^p mod m` to `1`. Only candidates that set a new record-low distance are
kept. A zero distance is the least-factor obstruction.

Measured with a raw-rank scan limit of `10000`:

```text
composite rows scanned: 15
composite rows skipped above rank limit: 4
record-low residue events: 35
zero-distance hits found: 15
maximum compression ratio: 254.33333333333334
median record-low event count: 2
```

Example:

```text
p = 59
raw order-filter candidates before least factor: 763
record-low fixed-point return events: 3
zero-distance event rank: 763
least factor: 179951
```

The result changes the immediate implementation target from raw divisor-count
search to fixed-point residue-return search.

## Unresolved-Row Pressure

The first pressure campaign reuses the same PGS rule on the `134` unresolved
rows from the `e <= 1000` ladder. It does not rerun the full ladder.

Passes:

```text
3.0 second candidate limit: 134 -> 129 unresolved, 5 resolved, 0 inferred
10.0 second candidate limit: 129 -> 125 unresolved, 4 resolved, 0 inferred
```

The remaining surface is not primarily a search-depth problem. The diagnostic
on the `125` still-unresolved rows found:

```text
offset 1 work-limit rows: 95 / 125
offset 1 share: 0.76
minimum exponent: 167
maximum exponent: 997
```

That triggers the pressure stop rule. The next task is not a uniform larger
time limit. The next task is to improve exact divisor-count handling for the
first left candidate `2^e - 1` while preserving the PGS-only live path.

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
python3 research/09-exponents/scripts/pgs_exponent_tail_probe.py \
  --output-dir research/09-exponents/output/pgs_exponent_tail_probe

python3 research/09-exponents/scripts/toy_exponent_wall_mechanics_probe.py \
  --output-dir research/09-exponents/output/toy_exponent_wall_mechanics_probe

python3 research/09-exponents/scripts/mersenne_boundary_contract_probe.py \
  --output-dir research/09-exponents/output/mersenne_boundary_contract_probe

python3 research/09-exponents/validation/mersenne_known_endpoint_validation.py \
  --output-dir research/09-exponents/output/mersenne_known_endpoint_validation

python3 research/09-exponents/validation/pgs_mersenne_order_filter_validation.py \
  --output-dir research/09-exponents/output/pgs_mersenne_order_filter_validation

python3 research/09-exponents/validation/pgs_mersenne_prime_generator_baseline_stats.py \
  --output-dir research/09-exponents/output/pgs_mersenne_prime_generator_baseline_stats
```

## Interpret

If the same exponent patterns concentrate at specific strip depths and residue
paths, the exponent-tail surface is structured.

If exponent patterns spread broadly across depths and residue paths, this toy
width-2 surface is a weak place to look for exponent structure.
