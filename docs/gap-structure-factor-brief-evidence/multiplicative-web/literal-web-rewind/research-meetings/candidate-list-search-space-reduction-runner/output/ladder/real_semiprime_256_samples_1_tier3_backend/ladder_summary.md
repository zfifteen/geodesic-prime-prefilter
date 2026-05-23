# PGA Grammar Pruner Scaling Ladder

**Date**: 2026-05-23T04:53:18.549228+00:00
**Mode**: `real`
**Artifact type**: `ladder_summary`
**Scale claim**: `True`
**Reference factor space**: 198 words
**Samples per level**: 1

## Backend

- name: `gmp_tier3_public_coordinate_backend`
- kind: `pgs_live_tier3`
- classification: `classical_assisted_public_coordinate`
- scale_capable: `True`
- pgs_native: `False`
- classical_assisted: `True`

## Results by Bit Length

| Bits | Measured | Avg Reduction | Std Dev | Min | Max | Unresolved | Derivation Blocked | Backend Error | Bit Mismatch |
|------|----------|---------------|---------|-----|-----|------------|--------------------|---------------|--------------|
| 256 | 1/1 | 59.60% | 0.00% | 59.6% | 59.6% | 0 | 0 | 0 | 0 |

## Mode Contract

Real mode derives motifs from deterministic public semiprimes.
The corpus is constructed using gmpy2.next_prime **only for fixture generation**.
p and q are discarded before any call to derive_public_motif or prune_factor_space.
Implementation-blocked derivations are reported as derivation_blocked, not unresolved.
Backend errors are reported as backend_error and do not contribute to averages.
No synthetic motif is substituted.

## Top Motifs per Level

**256 bits**
- `o2_d4_a44_d4_odd@late + o4_d4_odd prev`: 1


## Summary (Real Derivation)

- Total cases: 1
- Measured cases: 1
- Resolved cases: 1
- Unresolved cases: 0
- Derivation-blocked cases: 0
- Backend-error cases: 0
- Actual bit-length mismatches: 0
- Average reduction (measured cases): 59.60%
- Average reduction (all cases): 59.60%
- Average reduction (resolved cases): 59.60%
- Min / Max reduction: 59.60% / 59.60%
- Motifs with coverage gaps: 0

## Motif Breakdown

| motif | frequency | avg reduction | coverage gap cases |
|-------|-----------|---------------|--------------------|
| `o2_d4_a44_d4_odd@late + o4_d4_odd prev` | 1 | 59.60% | 0 |

## Top Rules

- PG-061: 1
- PG-062: 1
- PG-063: 1
- PG-064: 1
- PG-065: 1

## Per-Case Results (Real Derivation)

### 256 bits

| case_id | target_bits | actual_bits | N | motif | source | factors_discarded | pruning | rules | pruned | remaining | % | status | gap | error |
|---------|-------------|-------------|---|-------|--------|-------------------|---------|-------|--------|-----------|---|--------|-----|-------|
| semiprime_256_0 | 256 | 256 | 65133050195990359925758679067388231134923074306013959392135727524498631094129 | `o2_d4_a44_d4_odd@late + o4_d4_odd prev` | derive_public_motif(N_only) | yes | attempted | PG-061,PG-062,PG-063,PG-064,PG-065,PG-066,PG-067,PG-068,PG-069,PG-070,PG-071,PG-072,PG-073,PG-074,PG-075,PG-076,PG-077,PG-078,PG-082,PG-083,PG-084 | 118 | 80 | 59.60% | resolved | no | - |

## Interpretation

This ladder measures grammar-rule reduction after a public motif is available.
Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures
the live raw-N public derivation path plus rule coverage.
