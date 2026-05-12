# Square-Tail Arrival Boundary Gap For Root 509 Representative

## Status

Audit evidence. Not a proof.

## Finding

The first unarrived rough rows show the difference between a finite carrier
frontier and a prime proof.

The carrier-arrival frontier was scanned through `1,000,000`. The first seven
unarrived offsets are:

```text
80, 114, 128, 182, 194, 332, 338
```

Six of those rows are composite with first arrivals beyond `1,000,000`. The
seventh row, offset `338`, is prime.

| Offset | Status | Actual least factor |
|---:|---|---:|
| `80` | composite | `6736351` |
| `114` | composite | `1714849` |
| `128` | composite | `665241324811967767` |
| `182` | composite | `1614712643` |
| `194` | composite | `13214687` |
| `332` | composite | `170450107` |
| `338` | prime | none |

For each row, the square-root carrier boundary has `29` decimal digits. The
representative dynamic cutoff is `8889`.

## Boundary

No arrival through `1,000,000` is not a primality certificate. A rough row is
prime exactly when it has no carrier arrival before its own square-root
boundary.

The proof target is therefore:

```text
selected-square root
-> at least one M-rough row before the dynamic cutoff
-> no carrier arrival before that row's square-root boundary
```

The artifact is:

```text
research/04-bounded-compression/output/square_tail_arrival_boundary_gap_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_arrival_boundary_gap.py
```
