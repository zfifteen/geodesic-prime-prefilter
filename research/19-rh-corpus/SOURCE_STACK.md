# RH Source Stack

Fixed reading order for every RH-facing claim in PGS. Layer number matches
`by-layer/` folders and the **Layer** column in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md).

**Hard rule:** [FRAME_CONTRACT.md](./FRAME_CONTRACT.md). Layers L5 and L6 are
downstream *catalog* layers. They must not drive L1 to L4 research design.

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
│ L4  CHAMBER / SOURCE GEOMETRY (proved + measured)           │
│     Integer gap placement: GWR, frac_pos, budgets, d=4      │
│     Authority: pgs-rh-placement-empirics-2026-06/           │
│     (Transfer drafts are not L4 drivers; see FRAME_CONTRACT)│
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L5  POLE PLACEMENT / RH SENTENCE (downstream catalog only)  │
│     Open reading of continued R; not a research entrypoint  │
│     Authority: docs/rh/off-critical-pole-exclusion.md       │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│ L6  EXPLICIT FORMULA BRIDGE (downstream translation only)   │
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

| Layer | What you get | Typical status | Proves RH? | May drive new work? |
|-------|--------------|----------------|------------|---------------------|
| L1 | Integer mechanism | `proved` | No | **Yes** (source) |
| L2 | Coordinate rewrite | `exact` | No | **Yes** (source coords) |
| L3 | Zeta identities | `exact` | No | **Yes** (compression audit) |
| L4 | Chamber geometry | `proved` / `measured` | No | **Yes** (source geometry) |
| L5 | RH sentence catalog | `unresolved` | Open; would *be* RH if closed | **No** (downstream only) |
| L6 | Classical restatement | `narrative` | No | **No** (translation only) |

---

## Common category errors (avoid)

| Error | Correction |
|-------|------------|
| **RH-first design** (zeros/poles drive the experiment) | **Frame violation.** Restate a source law first. See [FRAME_CONTRACT.md](./FRAME_CONTRACT.md) |
| Bounded compression ⇒ RH | Witness offset bound only; not zero placement |
| ζ(s)² identity ⇒ RH | Exact compression; placement still open |
| ½ in C(q) ⇒ critical line proved | F18-001 is arithmetic; F18-003 is quarantined hypothesis (RH-040) |
| frac_pos geometry ⇒ RH | Local *integer* placement only |
| Chamber ρ_I aligned to R(s) | ρ_I tracks ½ log m; not a sample of R |
| Interior H·Λ kernel “carries” GWR | Support mismatch; design-invalid as transfer |
| Trillions of zeros on line ⇒ PGS proved RH | Computational RH evidence; not PGS theorem |

---

## Cross-links

- Status detail: [docs/rh/status-ledger.md](../../docs/rh/status-ledger.md)
- Public bundle index: [docs/rh/README.md](../../docs/rh/README.md)
- Master finding list: [FINDINGS_INDEX.md](./FINDINGS_INDEX.md)
- Gap analysis (scan audit): [GAP_ANALYSIS.md](./GAP_ANALYSIS.md)
- Flagship whitepaper: [integer-order-before-zeta WHITEPAPER.md](../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md)
- F18 branch discipline: [RH-103](./FINDINGS_INDEX.md) (rough-witness signature)
- L3 empiric: [zeta_compression_probe.py](./empirics/zeta_compression_probe.py) ([RH-105](./FINDINGS_INDEX.md), five $s$-values, $N=10^4$)
- Whitepaper status table: [WHITEPAPER.md §7](../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md) (hub-linked IDs)