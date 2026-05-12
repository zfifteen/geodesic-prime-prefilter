# d=4 No-Square Fallback Surface Through 1e7

## Measured Result

Lemma A' survived the exact consecutive right-prime surface through
`q <= 10,000,000`.

The tested rule was:

```text
If a right-prime gap contains no interior prime square, then the exact
unbounded GWR/DNI selected witness is the first interior d=4 carrier.
```

## Command

```bash
python3 research/04-bounded-compression/scripts/d4_no_square_fallback_falsification_runner.py \
  --min-right-prime 11 \
  --max-right-prime 10000000 \
  --output-dir output/bounded_compression/d4_no_square_fallback_1e7
```

## Facts

| Field | Value |
|---|---:|
| Range tested | `11 <= q <= 10,000,000` |
| First tested q | `11` |
| Last tested q | `9,999,991` |
| Gaps tested | `664,575` |
| First failure | `none` |
| No-square d=4 fallback cases | `499,896` |
| Square-present cases | `444` |
| No-d=4-carrier cases | `164,235` |

## Status

This is a finite measured surface, not a proof. It provisionally closes the
non-square branch on the tested range:

```text
no interior prime square -> first d=4 carrier wins
```

The remaining measured theorem pressure is the square branch.
