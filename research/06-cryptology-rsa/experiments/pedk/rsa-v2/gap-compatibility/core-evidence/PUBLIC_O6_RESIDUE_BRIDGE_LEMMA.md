# Public O6 Residue Bridge Lemma

## Statement

For a semiprime `N = pq` with both factor endpoints in the balanced
right-boundary class:

```text
Rres=o4|o4
```

and with public containing gap selected at:

```text
o6_d4_a6
```

the factor endpoint residues must be:

```text
13 and 19, in some order
```

In symbols:

```text
public o6 selected offset 6
and
balanced right endpoint boundary o4|o4
    -> {p mod 30, q mod 30} = {13, 19}
```

## Proof

The wheel-open residues modulo `30` are:

```text
1, 7, 11, 13, 17, 19, 23, 29
```

The endpoint residues with first right-open offset `4` are:

```text
7, 13, 19
```

Therefore `Rres=o4|o4` implies:

```text
p mod 30, q mod 30 are both in {7, 13, 19}
```

The possible products are:

| p residue | q residue | product mod 30 |
| ---: | ---: | ---: |
| `7` | `7` | `19` |
| `7` | `13` | `1` |
| `7` | `19` | `13` |
| `13` | `7` | `1` |
| `13` | `13` | `19` |
| `13` | `19` | `7` |
| `19` | `7` | `13` |
| `19` | `13` | `7` |
| `19` | `19` | `1` |

So under `Rres=o4|o4`:

```text
N mod 30 is in {1, 7, 13, 19}
```

Now use the public condition. A public containing gap with first-open offset
`6` has left endpoint residue `1` or `23`:

```text
1 + 6  = 7  mod 30
23 + 6 = 29 mod 30
```

Since the selected public offset is `6`, the public condition gives:

```text
N mod 30 is in {7, 29}
```

Intersect the two constraints:

```text
{1, 7, 13, 19} intersection {7, 29} = {7}
```

Therefore:

```text
N mod 30 = 7
```

Among the `o4|o4` factor residue pairs, the only ordered pairs with product
`7` modulo `30` are:

```text
13|19
19|13
```

Thus:

```text
{p mod 30, q mod 30} = {13, 19}
```

## Role In The Current Proof Target

This lemma proves the residue bridge. It does not prove terminal-twin lift.

The remaining unproved object is:

```text
inside the supported prior-absent trigger cells,
the forced {13, 19} balanced residue bridge reenters only when the lower factor
is the right endpoint of a terminal twin endpoint pair
```

So the current proof has split cleanly:

```text
residue bridge: proved by mod-30 arithmetic
terminal-twin lift: measured, not proved
```

## Evidence Link

The corresponding measurement surface is:

```text
PUBLIC_O6_RESIDUE_BRIDGE_PROBE.md
```

That probe verifies the lemma on the current trigger rows and records the
remaining terminal-twin boundary.
