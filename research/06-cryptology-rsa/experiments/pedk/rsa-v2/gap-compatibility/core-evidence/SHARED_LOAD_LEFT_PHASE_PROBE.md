# Shared Load Left-Phase Probe

## Finding

The blocked lift under shared load equality is a left-phase obstruction.

When the right-boundary cell reenters under shared load equality, the old exact
endpoint pair still does not reenter because its left phase arrangement does
not reappear.

The right boundary can come back. The coarse left residues can sometimes come
back. The left phase arrangement does not come back.

## Measured Profile

The probe examines only rows where the coarse right-boundary cell reentered in
the forward surface.

| shared load-boundary delta | boundary reentry rows | left residue reappears | left phase reappears | exact pair reappears |
| ---: | ---: | ---: | ---: | ---: |
| `-2` | `116` | `34` | `54` | `3` |
| `0` | `90` | `23` | `0` | `0` |
| `+2` | `1009` | `322` | `530` | `27` |

The load-match row has:

```text
boundary reentry rows = 90
left residue reappears = 23
left phase reappears = 0
exact pair reappears = 0
```

The off-load rows allow left-phase reentry:

```text
delta -2: left phase reappears 54 times, exact pair reappears 3 times
delta +2: left phase reappears 530 times, exact pair reappears 27 times
```

## Consequence

The exact endpoint-pair rule is no longer mysterious at the level of the
measured surface.

Exact endpoint-pair reentry requires:

```text
right-boundary reentry
and
left-phase reentry
```

Under shared load equality:

```text
right-boundary reentry occurs
left-phase reentry does not occur
exact endpoint-pair reentry does not occur
```

So the current obstruction is:

```text
first public load equals right endpoint boundary
    -> boundary reentry cannot preserve the old left phase arrangement
```

## Sharper Proof Target

The theorem target can now be stated as:

```text
If N is the first public low-load point,
and the right endpoint boundary equals the selected public load,
then any right-boundary reentry must move to a different left-phase
arrangement from the previously absent exact endpoint pair.
```

For the current distinct-prime semiprime surface:

```text
first public load 4
and
right endpoint boundary 4
    -> no left-phase lift
    -> no exact endpoint-pair lift
```

This is simpler than the previous blocked-lift statement because it identifies
the specific missing component: the left phase.

## Reproduction

Run:

```text
python3 shared_load_left_phase_probe.py
```

Primary outputs:

```text
output/shared_load_left_phase_probe/summary.json
output/shared_load_left_phase_probe/left_phase_rows.jsonl
output/shared_load_left_phase_probe/grouped_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
