# Square Envelope Record Table Through 3e8

## Measured Result

This table records every new square-envelope utilization record through

```text
p <= 300,000,000
```

where `p` is the prime root of the square witness candidate `p^2`.

The standing record remains isolated in the first surface:

```text
p = 82,357,433
utilization = 0.8120300751879699
```

The later tested segments did not set a new record:

```text
100,000,000 <= p <= 200,000,000: max utilization 0.6784140969162996
200,000,000 <= p <= 300,000,000: max utilization 0.7209612817089452
```

## Record Rows

| Rank | Root p | Square p^2 | Previous right prime q | Offset | Cutoff | Utilization | Segment/source finding | Record status |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| `1` | `3` | `9` | `7` | `2` | `64` | `0.03125` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `2` | `11` | `121` | `113` | `8` | `64` | `0.125` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `3` | `41` | `1,681` | `1,669` | `12` | `64` | `0.1875` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `4` | `109` | `11,881` | `11,867` | `14` | `64` | `0.21875` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `5` | `157` | `24,649` | `24,631` | `18` | `64` | `0.28125` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `6` | `199` | `39,601` | `39,581` | `20` | `64` | `0.3125` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `7` | `397` | `157,609` | `157,579` | `30` | `72` | `0.4166666666666667` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `8` | `509` | `259,081` | `259,033` | `48` | `78` | `0.6153846153846154` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `9` | `3,929` | `15,437,041` | `15,436,943` | `98` | `137` | `0.7153284671532847` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `10` | `6,424,279` | `41,271,360,669,841` | `41,271,360,669,481` | `360` | `492` | `0.7317073170731707` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `11` | `33,701,407` | `1,135,784,833,779,649` | `1,135,784,833,779,203` | `446` | `601` | `0.7420965058236273` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `new record` |
| `12` | `82,357,433` | `6,782,746,770,349,489` | `6,782,746,770,348,949` | `540` | `665` | `0.8120300751879699` | [`p <= 1e8`](./square_offset_envelope_surface_1e8.md) | `standing record` |

## Status

This is a finite measured record table, not a proof of the square-offset
envelope. Through `p <= 300,000,000`, the record utilization remains below `1`
and has not been exceeded after the `p <= 100,000,000` surface.
