# Tier-3 Exact-Bit Validation

This is a diagnostic exact-bit validation report. It is not a reduction evidence surface.

## Purpose

Compare tier-3 live motif derivation against exact divisor behavior where exact behavior is computationally available.

## Results

| bits | sample | actual bits | tier-3 live motif | exact status | exact motif | match |
|---:|---:|---:|---|---|---|---|
| 80 | 0 | 80 | `o4_d4_a10_d4_odd@mid + o6_d4_odd prev` | available | `o4_d4_a10_d4_odd@mid + o6_d4_odd prev` | yes |
| 128 | 0 | 128 | `o4_d4_a10_d4_odd@early + o4_d4_even prev` | timeout after 30 seconds | - | not exact-compared |

## Conclusion

The 80-bit exact-bit fixture matches exact behavior. The 128-bit exact comparison was not computationally available in the 30-second diagnostic window; tier-3 live derivation completed, but this report does not claim exact equivalence at 128 bits.
