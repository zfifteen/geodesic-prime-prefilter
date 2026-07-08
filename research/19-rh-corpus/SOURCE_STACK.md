# RH Source Stack

Fixed reading order for every RH-facing claim in PGS. Layer number matches
`by-layer/` folders and the **Layer** column in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md).

---

## Stack diagram

```text
┌─────────────────────────────────────────────────────────────┐
│ L1  DIVISOR SOURCE (proved local theorems)                  │
│     τ(n), gap interiors, GWR, bounded compression, …      │
│     Authority: PROOF.md                                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L2  DNI COORDINATE (exact reformulation)                    │
│     E(n), Z(n), H(n)=log n+E(n), primes at E=0              │
│     Authority: docs/core/, docs/rh/dni-to-zeta-compression  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L3  ZETA COMPRESSION (exact identities)                     │
│     D(s)=ζ², R(s)=-ζ'/ζ, Re(s)>1 then continuation         │
│     Authority: docs/rh/dni-to-zeta-compression.md           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L4  PLACEMENT GEOMETRY (proved corollaries + empirics)      │
│     Chamber invariants, d=4 frac_pos, transfer lemma draft  │
│     Authority: pgs-rh-placement-empirics-2026-06/           │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L5  POLE PLACEMENT / RH SENTENCE (unresolved target)        │
│     Every nontrivial pole of R(s) on Re(s)=½                │
│     Authority: docs/rh/off-critical-pole-exclusion.md       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L6  EXPLICIT FORMULA BRIDGE (downstream translation)        │
│     R(s) → Λ(n) → ψ(x) → zero-term language                │
│     Authority: docs/rh/explicit-formula-bridge.md           │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer authority links

| Layer | Primary authority |
|-------|-------------------|
| L1 | [PROOF.md](../../PROOF.md) |
| L2 | [docs/core/DIVISOR_NORMALIZATION_IDENTITY.md](../../docs/core/DIVISOR_NORMALIZATION_IDENTITY.md), [docs/rh/dni-to-zeta-compression.md](../../docs/rh/dni-to-zeta-compression.md) |
| L3 | [docs/rh/dni-to-zeta-compression.md](../../docs/rh/dni-to-zeta-compression.md) |
| L4 | [research/pgs-rh-placement-empirics-2026-06/](../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) |
| L5 | [docs/rh/off-critical-pole-exclusion.md](../../docs/rh/off-critical-pole-exclusion.md) |
| L6 | [docs/rh/explicit-formula-bridge.md](../../docs/rh/explicit-formula-bridge.md) |

---

## Layer → typical status

| Layer | What you get | Typical status | Proves RH? |
|-------|--------------|----------------|------------|
| L1 | Integer mechanism | `proved` | No |
| L2 | Coordinate rewrite | `exact` | No |
| L3 | Zeta identities | `exact` | No |
| L4 | Chamber placement | `proved` / `measured` / `hypothesis` | No |
| L5 | Critical-line poles | `unresolved` | **Would imply RH** |
| L6 | Classical restatement | `narrative` | No |

---

## Common category errors (avoid)

| Error | Correction |
|-------|------------|
| Bounded compression ⇒ RH | Witness offset bound only; not zero placement |
| ζ(s)² identity ⇒ RH | Exact compression; placement still open |
| ½ in C(q) ⇒ critical line proved | F18-001 is arithmetic; F18-003 is hypothesis |
| frac_pos geometry ⇒ RH | Local placement corollaries; partial only |
| Trillions of zeros on line ⇒ PGS proved RH | Computational RH evidence; not PGS theorem |

---

## Cross-links

- Status detail: [docs/rh/status-ledger.md](../../docs/rh/status-ledger.md)
- Public bundle index: [docs/rh/README.md](../../docs/rh/README.md)
- Master finding list: [FINDINGS_INDEX.md](./FINDINGS_INDEX.md)
- Gap analysis (scan audit): [GAP_ANALYSIS.md](./GAP_ANALYSIS.md)
- Flagship whitepaper: [integer-order-before-zeta WHITEPAPER.md](../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md)
- F18 branch discipline: [RH-103](./FINDINGS_INDEX.md) (rough-witness signature)
- L3 empiric: [zeta_compression_probe.py](./empirics/zeta_compression_probe.py) ([RH-105](./FINDINGS_INDEX.md))