# Collatz-PGS First-Descent Probe

## Strongest Measured Result

For odd Collatz seeds `3 <= s <= 19999`, first-descent source states are
enriched at prime endpoints and enriched at PGS-selected interior witness cells.
The interior signal survives the same-prime-gap control and every measured
`v2(3n+1)` stratum.

The accelerated odd map is

$$C(n)=\frac{3n+1}{2^{v_2(3n+1)}}$$

For each odd seed `s`, the probe follows odd iterates until the first target
below `s`. For each source state in that block, it records the containing prime
gap, exact divisor count, PGS witness, endpoint distance, and transition
`v2`.

The `20000` surface measured:

| Quantity | Collatz source states | Deterministic block background | Ratio |
|---|---:|---:|---:|
| Prime endpoint hit rate | `0.28317203524483603` | `0.16571965535827357` | `1.7087413960199178` |
| Composite interior odd-projected witness hit rate | `0.23673074597992988` | `0.19777698835109048` | `1.1969579876486405` |
| Final-source prime endpoint hit rate | `0.2745274527452745` | `0.16571965535827357` | `1.6565775022387452` |
| Final-source composite interior odd-projected witness hit rate | `0.23614557485525228` | `0.19777698835109048` | `1.1939992454331974` |

Against the same-prime-gap background, the interior signal is stronger:

| Quantity | Collatz source states | Same-gap background | Ratio |
|---|---:|---:|---:|
| Composite interior odd-projected witness hit rate | `0.23673074597992988` | `0.1489803136927796` | `1.589006897032753` |
| Final-source composite interior odd-projected witness hit rate | `0.23614557485525228` | `0.15952551981207166` | `1.4802996732650835` |

The same-gap background compares each composite Collatz source state only
against odd composite interior integers in its own containing prime gap, counted
with source multiplicity.

The same-gap witness ratio by transition `v2` stratum is:

| `v2(3n+1)` stratum | Source composite count | Same-gap background composite count | Ratio |
|---|---:|---:|---:|
| `1` | `12329` | `94378` | `1.7529488673287874` |
| `2` | `6219` | `46587` | `1.4675000302182195` |
| `3-4` | `4715` | `36666` | `1.3810570046013555` |
| `>=5` | `1550` | `11790` | `1.3912139699704087` |

The prime-endpoint signal is still the larger global effect. The interior
witness signal is now a real measured feature of this regime rather than a
global-background artifact.

## Exact Regime

- Odd seeds: `3 <= s <= 19999`
- Odd seed count: `9999`
- Total Collatz source states: `34615`
- Total deterministic background states: `139480383`
- Maximum odd steps to first descent: `66`
- Median odd steps to first descent: `2`
- Maximum value seen in first-descent blocks: `9038141`
- Maximum source-over-seed ratio: `935.3348856462796`

The deterministic background for one seed is every odd integer in the interval
from that seed through the maximum odd source reached before first descent.
Background intervals are counted with seed multiplicity.

## Artifact Surface

- Probe: `scripts/collatz_pgs_first_descent_probe.py`
- Contract test: `tests/test_collatz_pgs_first_descent_probe.py`
- Summary: `output/collatz_pgs_first_descent_probe/summary.json`
- Block rows: `output/collatz_pgs_first_descent_probe/block_rows.jsonl`
- State rows: `output/collatz_pgs_first_descent_probe/state_rows.jsonl`
- Plot: `assets/collatz_pgs_first_descent_profile.png`

## Status

This is an empirical probe result.

The naive one-step prime-ladder monovariant is not the live claim. Under the
accelerated odd Collatz map, examples such as `3 -> 5`, `7 -> 11`, and
`27 -> 41` move upward in prime-ladder position.

The live claim is a block-certificate hypothesis: Collatz first-descent blocks
thread prime endpoints and PGS-selected low-divisor interior cells at rates
above the deterministic local backgrounds measured here.

## Next Concrete Question

Scale the same-gap and `v2`-conditioned check without the full block-background
pass. The direct target is `200000` consecutive odd seeds with the same
composite interior same-gap control.
