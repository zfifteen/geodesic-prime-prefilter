# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-22T22:34:22.878617+00:00
**Mode**: `synthetic`
**Reference factor space**: 198 words
**Samples per level**: 30

## Results by Bit Length

| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |
|------|---------------|---------|-----|-----|------------|
| 48 | 71.21% | 0.00% | 71.2% | 71.2% | 0 |
| 56 | 49.75% | 8.87% | 42.4% | 71.2% | 0 |
| 64 | 60.40% | 20.98% | 15.7% | 74.8% | 0 |
| 72 | 71.21% | 0.00% | 71.2% | 71.2% | 0 |
| 80 | 40.55% | 12.03% | 15.7% | 53.5% | 0 |

## Mode Contract

Synthetic mode uses a fixed motif sequence derived from the frozen observed motif mix.
It is deterministic and does not call live public motif derivation.

## Top Motifs per Level

**48 bits**
- `o2_d4_a2_d4_odd@mid`: 30

**56 bits**
- `o4_d4_a4_d4_odd@mid`: 15
- `o2_d4_a2_d4_odd@early`: 12
- `o2_d4_a2_d4_odd@mid`: 3

**64 bits**
- `o2_d4_a2_d4_odd@mid`: 18
- `o6_d4_a6_d4_odd@mid`: 5
- `o2_d4_a2_d4_odd@mid + o4_d4_odd prev`: 4
- `o4_d4_a4_d4_odd@mid + o2_d4_odd prev`: 3

**72 bits**
- `o2_d4_a2_d4_odd@mid`: 30

**80 bits**
- `o4_d4_a4_d4_odd@mid`: 18
- `o2_d4_a2_d4_odd@early`: 7
- `o6_d4_a6_d4_odd@mid`: 5

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
