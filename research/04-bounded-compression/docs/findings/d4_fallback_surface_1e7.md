# d=4 Fallback Surface Through 1e7

## Measured Result

The literal d=4 fallback lemma was falsified on the requested
`q <= 10,000,000` scan.

The tested rule was:

```text
If no prime-square obstruction appears before the first d=4 carrier, then the
first d=4 carrier is the exact GWR/DNI selected witness.
```

The first failure occurs at `q = 113`.

## Command

```bash
python3 research/04-bounded-compression/scripts/d4_fallback_falsification_runner.py \
  --min-right-prime 11 \
  --max-right-prime 10000000 \
  --output-dir output/bounded_compression/d4_fallback_1e7
```

## Facts

| Field | Value |
|---|---:|
| Requested range | `11 <= q <= 10,000,000` |
| Gaps tested before first failure | `26` |
| First tested q | `11` |
| Last tested q | `113` |
| d=4 fallback cases before failure | `15` |
| Square-obstructed cases before failure | `2` |
| No-d=4-carrier cases before failure | `9` |
| First failure | `q = 113` |

## First Failure

| Field | Value |
|---|---:|
| q | `113` |
| Next prime | `127` |
| Gap width | `14` |
| First d=4 carrier | `115` |
| First d=4 offset | `2` |
| Prior prime square before first d=4 | `none` |
| Exact witness | `121 = 11^2` |
| Exact witness offset | `8` |
| Exact witness divisor count | `3` |

## Status

This falsifies the literal prior-square formulation of Lemma A. The missing
obstruction type is a later prime square inside the same gap: the square does
not appear before the first `d=4` carrier, but it still undercuts that carrier
because its divisor count is `3`.

The viable fallback target is narrower:

```text
If no interior prime square appears in the gap, then the first d=4 carrier wins.
```
