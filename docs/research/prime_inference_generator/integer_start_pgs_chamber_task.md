# Integer-Start PGS Chamber Task

## Claim

The high-scale C PGS generator can use the parsed scale value directly:

```text
scale S -> integer start n -> PGS chamber -> q
```

For `pgs_cli 10^1233`, the start value is the integer `10^1233`. The output
record for this high-scale generator should use `n`, not `p`, because the start
integer is not required to be prime:

```json
{"n":"1000...000","q":"..."}
```

## Mini Theorem

Let `n >= 5` be any integer and let `q = nextprime(n)`. If the PGS chamber uses
exact divisor-count state on every integer in `(n, n + B]`, and `B >= q - n`,
then the current chamber-reset selector resolves `q` from start `n`.

## Proof Sketch

Every integer `m` with `n < m < q` is composite, so exact divisor counting gives
`d(m) > 2`.

The endpoint `q` is prime, so exact divisor counting gives `d(q) = 2`. Since
`q > 5`, `q mod 30` is in the wheel-open residue set `{1, 7, 11, 13, 17, 19,
23, 29}`.

The chamber sees no earlier integer with divisor count `2`, so the first
wheel-open candidate with `d = 2` is `q`. Under the current chamber-reset
status rule, that candidate is the first resolved survivor. Therefore the
selector emits `q`.

The argument fails only when the bound does not reach `q`, or when the chamber
state is not exact.

## Probe

Run:

```bash
python benchmarks/python/predictor/integer_start_pgs_chamber_probe.py
```

The probe uses `sympy.nextprime` only as an audit label. It does not feed the
audit value into the selector.

The probe covers:

- decade starts `10^1` through `10^18`;
- 256 consecutive integer starts beginning at `10000`;
- exact bound equal to the audit gap for each row.

Initial result:

```text
starts: 274
resolved: 274
audit_passed: 274
audit_failed: 0
max_true_gap_for_audit_only: 61
```

This supports the mini theorem on the tested surface.

## C Generator Implication

Replace the abandoned scale-to-anchor path with:

```text
pgs_parse_scale(n, argv[1])
pgs_resolve_from_integer(q, certificate, n, candidate_bound)
pgs_emit_integer_record(stdout, n, q)
```

The required output contract becomes:

```json
{"n":"...","q":"..."}
```

The remaining hard part for `10^1233` is exact high-scale chamber state, not
anchor construction.
