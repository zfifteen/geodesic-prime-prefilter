# Public O6 Terminal-Twin Trigger Probe

## Finding

The terminal-twin lift is attached to two public balanced reentry triggers.

The active blocked-lift surface is not every public `o6_d4_a6` row. It is the
supported prior-absent balanced right-boundary cells for two exact public keys:

```text
prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner
prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner
```

For these two public keys, right-boundary reentry appears only through a
terminal-twin lift.

## Measured Profile

Across the two public triggers:

```text
candidate load-match reentry rows = 90
public-key prior pair support rows = 16143
public-key prior pair support rows with terminal-twin lift = 0
observed replacement rows = 2
observed replacement rows with terminal-twin lift = 2
```

Per public key:

| public trigger | candidate rows | prior support rows | prior terminal-twin rows | observed replacements | observed terminal-twin replacements |
| --- | ---: | ---: | ---: | ---: | ---: |
| `o4 even -> o6@mid -> o4 odd` | `46` | `8080` | `0` | `1` | `1` |
| `o4 odd -> o6@early -> o6 odd` | `44` | `8063` | `0` | `1` | `1` |

The observed factor residues are:

```text
13|19
19|13
```

`PUBLIC_O6_RESIDUE_BRIDGE_PROBE.md` shows why these are the only possible
balanced residues under the two trigger public keys: `Rres=o4|o4` restricts the
endpoint residues to `7, 13, 19`, and product residue `7` leaves only `13|19`
or `19|13`.

The observed terminal-twin lifts are:

```text
width=24, distance=2, preceding=22
width=20, distance=2, preceding=18
```

## Consequence

The current proof target is now a two-trigger statement:

```text
For the two supported prior-absent public o6_d4_a6 balanced right-boundary
cells, any forward reentry of Rres=o4|o4 requires terminal-twin lift.
```

This is sharper than saying "`o6_d4_a6` causes terminal twin." The broader
public type has many ordinary rows. The trigger is the supported prior-absent
balanced reentry cell.

## Current Proof Target

The theorem target can be stated as:

```text
public selected load 4
and
public o6 selected offset 6 in one of the two supported trigger neighborhoods
and
balanced right endpoint boundary o4|o4
and
supported prior exact-pair absence
and
right-boundary reentry
    -> terminal-twin lift
```

Then exact endpoint-pair absence follows because the old supported pair classes
have no terminal-twin lift in prior support.

## Reproduction

Run:

```text
python3 public_o6_terminal_twin_trigger_probe.py
```

Primary outputs:

```text
output/public_o6_terminal_twin_trigger_probe/summary.json
output/public_o6_terminal_twin_trigger_probe/public_trigger_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
