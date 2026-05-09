# Bounded Compression Findings

The bounded-compression conjecture uses

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

as the finite window for the exact GWR/DNI selected witness.

## Falsification Surfaces

| Surface | Gaps | First failure | Max witness offset | Max cutoff utilization | Extremal witness |
|---|---:|---|---:|---:|---|
| [`1e6`](./dynamic_cutoff_falsification_surface_1e6.md) | `78,494` | `none` | `48` | `0.6153846153846154` | `509^2` |
| [`1e7`](./dynamic_cutoff_falsification_surface_1e7.md) | `664,575` | `none` | `60` | `0.6153846153846154` | `509^2` |

## Current Read

The tested surface grew by an order of magnitude from `1e6` to `1e7`.
The maximum witness offset increased from `48` to `60`, but the maximum
cutoff utilization stayed fixed at `0.6153846153846154`.

The current sharp observed obstruction is the same prime-square witness:

```text
q = 259,033
witness = 259,081 = 509^2
offset = 48
cutoff = 78
utilization = 0.6153846153846154
```

This is measured evidence, not a proof of the dynamic cutoff law.

## Square-Envelope Pressure Surface

The square-envelope search has now tested through `p <= 700,000,000` in
documented surfaces, with no counterexample. The record-law table through
`p <= 500,000,000` identifies the standing utilization record. The `4e8` to
`5e8` segment created a new record below `1`; the `5e8` to `6e8` segment
and `6e8` to `7e8` segment preserved that record.

| Surface | Square roots tested | First counterexample | Max utilization | Extremal square |
|---|---:|---|---:|---|
| [`1e8 square branch`](./square_offset_envelope_surface_1e8.md) | `5,761,454` | `none` | `0.8120300751879699` | `82,357,433^2` |
| [`1e8 to 2e8 square segment`](./square_offset_envelope_segment_1e8_to_2e8.md) | `5,317,482` | `none` | `0.6784140969162996` | `102,017,779^2` |
| [`2e8 to 3e8 square segment`](./square_offset_envelope_segment_2e8_to_3e8.md) | `5,173,388` | `none` | `0.7209612817089452` | `251,066,071^2` |
| [`3e8 to 4e8 square segment`](./square_offset_envelope_segment_3e8_to_4e8.md) | `5,084,001` | `none` | `0.7036082474226805` | `358,018,553^2` |
| [`4e8 to 5e8 square segment`](./square_offset_envelope_segment_4e8_to_5e8.md) | `5,019,541` | `none` | `0.9341772151898734` | `424,171,123^2` |
| [`5e8 to 6e8 square segment`](./square_offset_envelope_segment_5e8_to_6e8.md) | `4,968,836` | `none` | `0.6691449814126395` | `526,336,897^2` |
| [`6e8 to 7e8 square segment`](./square_offset_envelope_segment_6e8_to_7e8.md) | `4,928,228` | `none` | `0.7161997563946407` | `622,805,873^2` |

Record-law artifact:

```text
square_envelope_record_table_to_5e8.md
```

Active record anatomy:

```text
square_record_anatomy_424171123.md
```

## Lemma A Falsification

| Surface | Gaps tested before failure | First failure | Missing obstruction |
|---|---:|---|---|
| [`d=4 fallback 1e7`](./d4_fallback_surface_1e7.md) | `26` | `q = 113` | later square `121 = 11^2` |

## Lemma A' No-Square Fallback

| Surface | Cases | Square-present cases | First failure | Branch status |
|---|---:|---:|---|---|
| [`d=4 no-square fallback 1e7`](./d4_no_square_fallback_surface_1e7.md) | `499,896` | `444` | `none` | non-square branch survives on measured surface |
