# Public O6 Residue Bridge Probe

## Finding

The two public terminal-twin triggers have a tiny mod-30 residue bridge.

For the two trigger public keys, every observed row with balanced right
boundary:

```text
Rres=o4|o4
```

has:

```text
N mod 30 = 7
```

The endpoint residues whose first right-open offset is `4` are:

```text
7, 13, 19
```

Among those residues, the only ordered factor pairs whose product is `7` mod
`30` are:

```text
13|19
19|13
```

So the residue bridge is exact:

```text
N mod 30 = 7
and
Rres=o4|o4
    -> factor residues are 13 and 19, in some order
```

## Measured Profile

Across the current enriched output tree:

```text
trigger Rres=o4|o4 rows = 11
N mod 30 = 7 rows = 11
factor residue pair 13|19 = 6
factor residue pair 19|13 = 5
```

Terminal-twin lift is not a general consequence of the residue bridge alone:

```text
trigger Rres=o4|o4 rows with terminal-twin lift = 3
```

The supported prior-absent reentry condition is still doing real work. The
previous trigger probe isolates the stricter surface:

```text
observed replacement rows = 2
observed replacement rows with terminal-twin lift = 2
```

## Consequence

The proof target now splits into two small pieces.

First, a residue lemma:

```text
public selected residue 7
and
balanced right endpoint boundary o4|o4
    -> endpoint residues 13|19 or 19|13
```

Second, the remaining lift lemma:

```text
inside the supported prior-absent trigger cells,
endpoint residues 13|19 or 19|13 lift only through terminal twin
```

`LOWER_TERMINAL_TWIN_ORIENTATION_PROBE.md` sharpens this: in the measured
replacement rows, the terminal-twin lift is on the lower factor side.

The first piece is pure mod-30 arithmetic. The second piece is now the true
unproved object.

`PUBLIC_O6_RESIDUE_BRIDGE_LEMMA.md` records the first piece as a proved
mod-30 lemma.

## Current Proof Target

The current target is:

```text
For the two supported prior-absent public o6_d4_a6 balanced right-boundary
cells, the residue bridge forces the factor residues to 13 and 19, and any
forward reentry through those residues requires terminal-twin lift.
```

Then exact endpoint-pair absence follows because the old supported pair classes
have no terminal-twin lift in prior support.

## Reproduction

Run:

```text
python3 public_o6_residue_bridge_probe.py
```

Primary outputs:

```text
output/public_o6_residue_bridge_probe/summary.json
output/public_o6_residue_bridge_probe/trigger_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
