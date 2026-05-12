# Square-Tail Carrier Economy Audit

## Status

Measured carrier-economy audit. This is not a proof of the square-tail
theorem.

## Finding

The current record separates into repeat-capable carriers and singleton
carriers.

For

```text
r = 424,171,123
```

the full counterexample word length is

```text
M = floor(C / 2) = 395.
```

A least factor `ell <= M` can cover multiple positions in the moving window.
A least factor `ell > M` can cover only one position in the moving window,
because two covered positions differ by a positive integer less than `ell`.

The obstruction prefix has:

| Quantity | Value |
|---|---:|
| Prefix length | `368` |
| Distinct least factors | `99` |
| Repeat-capable factors `ell <= M` | `43` |
| Singleton factors `ell > M` | `56` |
| Prefix rows using singleton factors | `56` |
| Positions covered by repeat-capable prefix factors | `329 / 395` |
| Positions covered by all prefix factors | `385 / 395` |
| Positions left after repeat-capable factors | `66` |
| Positions left after all prefix factors | `10` |

## Audit Artifact

```text
research/04-bounded-compression/output/square_tail_carrier_economy_424171123.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_carrier_economy.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_carrier_economy.py \
  --root 424171123 \
  --output research/04-bounded-compression/output/square_tail_carrier_economy_424171123.json
```

## Proof Consequence

The moving-cover route should not treat all factors as equal. Repeat-capable
factors propagate across the window. Singleton factors fill one position and
do not propagate.

A complete square-tail counterexample must therefore supply a full carrier
economy:

```text
repeat-capable cover + singleton fills = every position 1..M.
```

The current record almost realizes that economy but stops at prime-valued
defects. The theorem target is to prove that a selected-square branch cannot
complete the singleton-fill burden without leaving at least one prime-valued
defect before the cutoff.
