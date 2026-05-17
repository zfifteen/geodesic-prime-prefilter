# Shared Load Reentry Cell Probe

## Finding

The shared-load phase shift collapses to a smaller arithmetic object.

The previous probe counted `90` supported candidate exact-pair classes blocked
inside reentered right-boundary cells. This probe looks at the actual forward
rows that reenter those boundary cells.

There are only two reentered boundary cells and two exact forward replacement
rows. In both rows:

```text
right boundary residues = o4|o4
one left-side factor gap has its selected point two units before the right endpoint
```

That is the concrete source of the `very_late` phase shift.

## Measured Profile

```text
candidate load-match reentry rows = 90
distinct reentered boundary cells = 2
observed forward exact rows in reentered cells = 2
```

The observed right boundary is fixed:

```text
Rres=o4|o4: 2
```

The observed replacement left phases are:

```text
early|very_late: 1
mid|very_late:   1
```

The `very_late` side is not an abstract label here. In both exact forward
replacement rows, the selected point in that left-side factor gap is exactly
two units before the right endpoint:

```text
left offset from right = 2: 2
```

## Consequence

The proof target is now sharper:

```text
first public load 4
and
right endpoint boundary 4
and
right-boundary reentry
    -> a replacement left-side factor gap is selected two units before its
       right endpoint
```

For the current measured surface, that exact two-from-right condition is what
appears as a `very_late` left phase. The old supported candidate classes do not
contain a `very_late` left phase, so they cannot be the exact rows that reenter.

## Current Proof Target

The theorem target can be stated without the broad grammar catalog:

```text
Shared load equality forces any reentered right-boundary cell to lift through
an extreme left-side endpoint approach.
```

In the measured rows, "extreme" is literal:

```text
winner offset from right endpoint = 2
```

This is the smallest arithmetic obstruction currently exposed.

## Reproduction

Run:

```text
python3 shared_load_reentry_cell_probe.py
```

Primary outputs:

```text
output/shared_load_reentry_cell_probe/summary.json
output/shared_load_reentry_cell_probe/candidate_rows.jsonl
output/shared_load_reentry_cell_probe/observed_forward_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
