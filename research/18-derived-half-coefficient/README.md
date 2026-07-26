# 18: Derived Half-Coefficient

Formalizes finding **F18-001**: the `0.5` in `C(q) = max(64, ceil(0.5 * log(q)^2))` is
arithmetically derived from divisor closure, not chosen to match Cramér or `Re(s)=1/2`.

PGS is fully deterministic: every claim here is either a universal theorem or a
pinned finite replay on an exact regime.

| Artifact | Path |
|----------|------|
| Finding IDs | [docs/FINDING_STATEMENT.md](./docs/FINDING_STATEMENT.md) |
| Derivation | [docs/derivation-chain-digest.md](./docs/derivation-chain-digest.md) |
| Finite verification (F18-002) | [docs/finite-verification-grok-509b8495.md](./docs/finite-verification-grok-509b8495.md) |
| F18-004 threshold analysis (issue #45) | [docs/f18_004_threshold_analysis.md](./docs/f18_004_threshold_analysis.md) |
| Near-max audit script | [scripts/near_maximal_witness_audit.py](./scripts/near_maximal_witness_audit.py) |
| Hypothesis (quarantined) | [docs/half-scale-correspondence-hypothesis.md](./docs/half-scale-correspondence-hypothesis.md) |
| 30/30/30 bundle | [30-30-30-technical-note/TECHNICAL_NOTE.md](./30-30-30-technical-note/TECHNICAL_NOTE.md) |

Proof authority: [PROOF.md](../../PROOF.md) · theorem home: [research/04-bounded-compression/](../04-bounded-compression/README.md)

### F18-004 / RH-103 audit (measured)

```bash
# Unit checks (local)
python3 -m pytest research/18-derived-half-coefficient/tests/ -q

# Smoke
python3 research/18-derived-half-coefficient/scripts/near_maximal_witness_audit.py \
  --limit 1000000 \
  --output research/18-derived-half-coefficient/output/near_maximal_audit_results_1M.json

# Pinned campaign parameters (expensive; existing 40M artifact may be retained)
python3 research/18-derived-half-coefficient/scripts/near_maximal_witness_audit.py \
  --limit 40000000 --ratio-threshold 0.65 --q-min 10000000 --d-log-coeff 0.75 \
  --output research/18-derived-half-coefficient/output/near_maximal_audit_results_40M.json
```

Status: **measured** prediction. Not promoted to theorem. RH-103 stays measured.