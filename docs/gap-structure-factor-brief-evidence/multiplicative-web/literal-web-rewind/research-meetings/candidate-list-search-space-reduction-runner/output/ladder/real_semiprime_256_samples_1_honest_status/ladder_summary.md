# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-23T03:21:42.300736+00:00
**Mode**: `real`
**Reference factor space**: 198 words
**Samples per level**: 1

## Results by Bit Length

| Bits | Measured | Avg Reduction | Std Dev | Min | Max | Unresolved | Derivation Blocked |
|------|----------|---------------|---------|-----|-----|------------|--------------------|
| 256 | 0/1 | - | - | - | - | 0 | 1 |

## Mode Contract

Real mode derives motifs from deterministic public semiprimes.
The corpus is constructed using gmpy2.next_prime **only for fixture generation**.
p and q are discarded before any call to derive_public_motif or prune_factor_space.
Implementation-blocked derivations are reported as derivation_blocked, not unresolved.
No synthetic motif is substituted.

## Top Motifs per Level

**256 bits**
- `DERIVATION_BLOCKED:28948022309329048859031297119865317363610638691744651245472758103663360084211`: 1


## Summary (Real Derivation)

- Total cases: 1
- Measured cases: 0
- Resolved cases: 0
- Unresolved cases: 0
- Derivation-blocked cases: 1
- Average reduction (measured cases): -
- Average reduction (all cases): -
- Average reduction (resolved cases): -
- Min / Max reduction: - / -
- Motifs with coverage gaps: 0

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `derivation_blocked` | 1 | - | 0 |

## Top Rules


## Per-Case Results (Real Derivation)

### 256 bits

| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |
|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_256_0 | 256 | 255 | 28948022309329048859031297119865317363610638691744651245472758103663360084211 | `-` | derive_public_motif(N_only) | yes | not_attempted | - | - | - | - | derivation_blocked | no | PublicMotifBackendLimitExceeded: GMP gap grammar exact divisor horizon exceeds configured public motif limit (30704801884924481768605764 > 70000000) |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
