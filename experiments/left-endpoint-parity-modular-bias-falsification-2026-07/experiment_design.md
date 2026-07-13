# Experiment design: left-endpoint parity modular bias falsification

## Target

Attempt to **falsify** the hypothesis that left-endpoint parity creates a
systematic modular bias under min-`tau` gap reading.

Related prior (different claim, already falsified on leftmost *necessity*):  
`experiments/leftmost-min-modular-closure-falsification-2026-07/`

## PGS frame

```text
ordered prime gap (p, q)
  -> divisor-count field tau on interior
  -> min-tau set
  -> leftmost vs rightmost selection
  -> witness parity and endpoint flag (w == p+1)
  -> z(w) on M_v1 = (2, 3, 5, 7, 30, 210, 2310)
  -> mismatch if z(w) >= T and g > 2  (T in {3, 4})
  -> resolved measured rates / falsified / weakened / survives
```

## Minimal decisive probes

### Probe 1: Even vs odd under leftmost (H-parity)

Split all GWR rows by `w % 2`. Report:

- gap counts
- `z >= 4` counts
- mismatch counts and rates
- Explicit flag: `z >= 4` impossible for odd `w` (structural)

Also report the same table for `z >= 3` (non-degenerate).

### Probe 2: Endpoint concentration (H-endpoint)

Among GWR mismatches (`T = 4`): fraction with `w == p + 1`.  
Among GWR `z4` events: fraction with `w == p + 1`.  
Compare mismatch rate when leftmost is `p + 1` vs not.

### Probe 3: Leftmost vs rightmost on a FRESH band (H-rightmost)

Prior decisive window was `p in [11, 2.5e7]`. Fresh band:

| Label | Regime | Role |
| --- | --- | --- |
| Prior-D (reconfirm only) | `p in [11, 2.5e7]` | optional; already measured elsewhere |
| Fresh-F | `p in (2.5e7, 5.0e7]` | independent multi-hundred-thousand-gap band |

Count total mismatches for leftmost vs rightmost min-`tau`.

### Probe 4: Ties vs unique control (H-tie-break)

- **Unique min:** left == right; report parity, `p+1`, z4, mismatch.
- **Ties:** left != right; report left/right parity, left-is-p+1, mismatches.

Isolates "even has more factors" from "leftmost picks `p+1` among ties".

## Field prep (classical, non-inference)

- Eratosthenes for consecutive primes.
- Linear divisor accumulation for `tau`.

No Miller-Rabin, `isprime`, `gcd`, product closure, or random fallback in the
decision path.

## Regimes (deterministic enumeration)

| Label | p range | Expected gaps (order) |
| --- | --- | --- |
| S | `[11, 1e5]` | ~9.5k smoke |
| M | `[11, 2e6]` | ~149k mid |
| F | `(2.5e7, 5.0e7]` | ~1.4e6 fresh large |

Prefer full enumeration. No sampling.

## Output

JSON under `artifacts/` plus `FINDINGS.md` with exact counts, rates, and
pass/fail of each disconfirmation criterion. Status labels only.
