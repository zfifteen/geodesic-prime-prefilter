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
