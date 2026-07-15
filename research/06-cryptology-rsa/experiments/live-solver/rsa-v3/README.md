# RSA Endpoint Resolver v3 (A1)

Deterministic PGS-native modulus endpoint resolver implementing enhancement A1.

## Claim boundary

This track reads and certifies deterministic endpoint structure under
locked endpoint chains, floor transport, reciprocal closure, and named
GWR-carrier transport closure. It does **not** claim to factor RSA, break
cryptography, or prove new universal theorems. Classical factor checks
belong only in a separate audit sidecar after inference.

## Required frame

```text
locked PGS endpoint chain
  -> floor transport through modulus
  -> reciprocal endpoint closure
  -> GWR-selected carrier transport closure
  -> modulus-link residual
  -> structural certificate OR unresolved state
```

## Entry points

```bash
# Resolve public fixtures (inference only)
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/run_resolver.py \
  --cases research/06-cryptology-rsa/experiments/live-solver/rsa-v3/fixtures/regression_cases.jsonl \
  --output-dir research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/regression

# Verify structural certificates
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/verifier.py \
  --certs research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/regression/structural_certificates.jsonl
```

## Documents

| File | Role |
| --- | --- |
| [ALGORITHM.md](ALGORITHM.md) | Inference stages in PGS objects |
| [RESIDUAL_TAXONOMY.md](RESIDUAL_TAXONOMY.md) | Stable residual codes |
| [PGS_CERTIFICATE.md](PGS_CERTIFICATE.md) | Certificate field contract |
| [METRICS.md](METRICS.md) | Measured summary fields |
| [schema/structural_certificate_v3.json](schema/structural_certificate_v3.json) | JSON schema |

## Requirements / test plan

- `research/20-enhancement-roadmap/a1-rsa-endpoint-resolver/index.html`
- `research/20-enhancement-roadmap/a1-rsa-endpoint-resolver/test-plan.html` (A1-TP)

## Algorithm version

```text
algorithm_version = pgs_rsa_endpoint_resolver_v3.1
rule_id = reciprocal_pgs_gwr_carrier_transport_v3
```

## Residual ledger

Unresolved cases emit residual codes listed in `RESIDUAL_TAXONOMY.md` and
appear in run `residuals.jsonl` under the output directory.

### Residual packages (measured evolution; 50-bit still unresolved)

| Package | Residual story | Class |
| --- | --- | --- |
| `output/baseline_freeze_goal/` | Pre-D residual pin | honesty freeze |
| `output/discriminator_D/` | Dual-gap D holds; residual → `unresolved_by_first_tail_misalignment` | **(B)** subclass |
| `output/phase1_residual_honesty/` | Joint component ledger + anti-admission | **(C)** diagnostics |
| `output/residual_cell_C1T2L1/` | Residual vector R; decision residual → `unresolved_by_joint_cell_C1T2L1` | **(B)** subclass |

Live decision residual on `rsa_v2_50bit_static_001` under the residual-cell
stack: **`unresolved_by_joint_cell_C1T2L1`** with
`R = (r_carrier=1, r_tail=2, r_lock=1)`, `pinch_S=54`. Residual maps (D, R, joint
cell) stay **hypothesis**. 40-bit control still resolves. No residual-family
`10^18` surface; no verified/validated residual language.

Continuity pin:
`research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`.
