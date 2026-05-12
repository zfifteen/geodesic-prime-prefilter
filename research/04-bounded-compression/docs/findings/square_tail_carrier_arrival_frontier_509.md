# Square-Tail Carrier Arrival Frontier For Root 509 Representative

## Status

Audit evidence. Not a proof.

## Finding

The ordered carrier-arrival frontier is sparse for the first prime
selected-square representative of the `509` CRT rough-cover class.

After repeat-capable carriers through `M = 4444`, there are `569` rough rows.
Scanning prime carriers above `M` through `1,000,000` gives first arrivals for
only `222` of those rows. The remaining `347` rows have no carrier arrival in
that range.

| Carrier bound | Arrived rows | Unarrived rows |
|---:|---:|---:|
| `5,000` | `14` | `555` |
| `10,000` | `63` | `506` |
| `20,000` | `93` | `476` |
| `50,000` | `136` | `433` |
| `100,000` | `158` | `411` |
| `500,000` | `203` | `366` |
| `1,000,000` | `222` | `347` |

The closing row is

```text
m = 169, offset = 338.
```

It has no carrier arrival through `1,000,000`.

The first unarrived offsets are:

```text
80, 114, 128, 182, 194, 332, 338, 360, 390, 428,
458, 462, 464, 474, 500, 540, 560, 608, 642, 644,
650, 674, 684, 708, 770, 792, 824, 842, 848, 864
```

## Boundary

This audit does not prove that the closing row is prime. It does show the next
ordered object:

```text
first carrier arrival for each rough row
```

The full-cutoff CRT model proves that arbitrary singleton carrier assignment
is locally consistent. The carrier-arrival frontier records the ordered
integer-line condition that the CRT model omits: actual carriers arrive in
prime order, and many rough rows receive no early carrier.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_carrier_arrival_frontier_509_1e6.json
```

The boundary-gap audit in

```text
research/04-bounded-compression/docs/findings/square_tail_arrival_boundary_gap_509.md
```

records the proof boundary: no arrival through `1,000,000` is not the same as
no arrival before the square-root boundary.

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_carrier_arrival_frontier.py
```
