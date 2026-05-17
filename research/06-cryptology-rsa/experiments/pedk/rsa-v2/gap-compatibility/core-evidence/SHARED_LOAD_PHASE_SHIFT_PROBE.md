# Shared Load Phase-Shift Probe

## Finding

Under shared load equality, blocked exact-pair reentry is a phase shift.

When the right-boundary cell reenters under shared load equality, every
observed replacement left phase contains `very_late`. The previously absent
candidate left phases do not contain `very_late`.

In the measured rows, that is the exact obstruction preventing the endpoint
pair from reappearing.

## Measured Profile

The probe examines rows where the right-boundary cell reentered in the forward
surface.

| shared load-boundary delta | boundary reentry rows | candidate left phases with `very_late` | observed rows whose left phases all contain `very_late` | candidate left phase reappears |
| ---: | ---: | ---: | ---: | ---: |
| `-2` | `116` | `0` | `0` | `54` |
| `0` | `90` | `0` | `90` | `0` |
| `+2` | `1009` | `0` | `0` | `530` |

For the load-match row:

```text
boundary reentry rows = 90
candidate left phases with very_late = 0
observed rows whose left phases all contain very_late = 90
candidate left phase reappears = 0
```

The observed replacement phase families under load match are only:

```text
early|very_late: 46
mid|very_late:   44
```

The candidate left phase families under load match are:

```text
early|late: 4
early|mid: 18
late|late: 1
late|mid: 25
mid|mid: 42
```

The sets are disjoint because the observed side always contains `very_late`
and the candidate side never does.

## Consequence

The current blocked-lift statement can be sharpened:

```text
shared load equality
    -> right-boundary reentry shifts the left phase into a very_late family
    -> the old left phase cannot reappear
    -> the old exact endpoint pair cannot reappear
```

The off-load rows do not obey this shift:

```text
delta -2: candidate left phase reappears 54 times
delta +2: candidate left phase reappears 530 times
```

So the `very_late` phase shift is specific to the shared load-boundary match.

## Current Proof Target

The theorem target is now:

```text
If N is the first public low-load point,
and the right endpoint boundary equals the selected public load,
then any reentry of that right-boundary cell must move the left endpoint phase
into a very_late-containing family.
```

For the current distinct-prime semiprime surface:

```text
first public load 4
and
right endpoint boundary 4
    -> left phase shifts to early|very_late or mid|very_late
    -> no old left phase lift
    -> no exact endpoint-pair lift
```

This is the smallest obstruction currently exposed.

## Reproduction

Run:

```text
python3 shared_load_phase_shift_probe.py
```

Primary outputs:

```text
output/shared_load_phase_shift_probe/summary.json
output/shared_load_phase_shift_probe/phase_shift_rows.jsonl
output/shared_load_phase_shift_probe/grouped_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
