# Experiment design: leftmost-min modular closure falsification

## Target

Falsify the Core insight from  
`https://x.com/i/grok/share/1f4cf4bbb79542c3af9957e0dd043553`

Theme: leftmost minimal-divisor selection is what converts modular remainder-zero
counts into gap-closure rules; alternative probes lose that sufficiency.

## Minimal decisive comparison

Hold the modular rule fixed (`z >= 4` on `M_v1`). Vary only the witness selector.

```text
same gaps, same tau field, same z threshold
  GWR  leftmost min-tau
  A    global min-tau without leftmost (rightmost + unique-only)
  B    first interior
count mismatches: z(w)>=4 and g>2
```

One of:

- GWR mismatch present, or
- A or B strictly fewer mismatches than GWR, or
- A or B zero mismatches on multi-thousand-gap regime while prediction required >=1

is enough to pressure or kill the insight.

## Regimes

| Label | p range | Role |
| --- | --- | --- |
| S | `[11, 1e5]` | smoke, multi-thousand gaps |
| M | `[11, 2e6]` | historical Super-Signal "looks perfect" surface |
| D | `[11, 2.5e7]` | includes pinned GWR CEs |

## Out of scope

- Re-proving or demoting GWR / modular zero lemma
- RSA / modulus-link work
- Claiming verified status without `10^18`
