# 19: RH Corpus (Navigation Hub)

**Purpose:** One door to every RH-facing aspect of the PGS program.

This chapter is a **card catalog**, not a second copy of the proofs. Canonical
content stays in [PROOF.md](../../PROOF.md), [docs/rh/](../../docs/rh/README.md), and the
linked research folders below. This hub indexes those sources with stable IDs,
status labels, and boundaries.

## Start here

1. [START_HERE.md](./START_HERE.md), five-minute orientation
2. [FINDINGS_INDEX.md](./FINDINGS_INDEX.md), master table (primary navigation)
3. [SOURCE_STACK.md](./SOURCE_STACK.md), layer diagram and claim types
4. [READING_PATHS.md](./READING_PATHS.md), curated routes by audience

## Browse by status

| File | Tier |
|------|------|
| [by-status/proved.md](./by-status/proved.md) | `proved` |
| [by-status/exact-compression.md](./by-status/exact-compression.md) | `exact` |
| [by-status/measured.md](./by-status/measured.md) | `measured` |
| [by-status/hypothesis.md](./by-status/hypothesis.md) | `hypothesis` |
| [by-status/unresolved.md](./by-status/unresolved.md) | `unresolved` |
| [by-status/invalidated.md](./by-status/invalidated.md) | `invalidated` |
| [by-status/archived.md](./by-status/archived.md) | `archived` |
| [by-status/narrative.md](./by-status/narrative.md) | `narrative` |

## Browse by source layer

| Layer | File |
|-------|------|
| 1. Divisor source | [by-layer/01-divisor-source.md](./by-layer/01-divisor-source.md) |
| 2. DNI coordinate | [by-layer/02-dni-coordinate.md](./by-layer/02-dni-coordinate.md) |
| 3. Zeta compression | [by-layer/03-zeta-compression.md](./by-layer/03-zeta-compression.md) |
| 4. Placement geometry | [by-layer/04-placement-geometry.md](./by-layer/04-placement-geometry.md) |
| 5. Pole placement / RH | [by-layer/05-pole-placement-rh.md](./by-layer/05-pole-placement-rh.md) |
| 6. Explicit formula | [by-layer/06-explicit-formula-bridge.md](./by-layer/06-explicit-formula-bridge.md) |

## Public narrative spine (not duplicated here)

Reviewer-facing prose lives in [docs/rh/README.md](../../docs/rh/README.md).
Use this hub for **program navigation**; use [docs/rh/](../../docs/rh/README.md) for
**external review**.

## Related chapters (canonical homes)

| Chapter / folder | RH role |
|------------------|---------|
| [04-bounded-compression](../04-bounded-compression/README.md) | Cramér-scale witness bound (source) |
| [18-derived-half-coefficient](../18-derived-half-coefficient/README.md) | Derived ½ coefficient + F18-003 hypothesis |
| [pgs-rh-placement-empirics-2026-06](../pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md) | d=4 placement geometry + audits |
| [12-rh-bridge](../12-rh-bridge/README.md) | Archived pointer only |
| [experiments/integer-order-before-zeta-whitepaper-2026-07](../../experiments/integer-order-before-zeta-whitepaper-2026-07/README.md) | Public explanatory whitepaper |

## Tests

```bash
PYTHONPATH=src/python:research/19-rh-corpus/empirics \
  python3 -m pytest research/19-rh-corpus/tests/ -q
```

Imports and exercises shipped logic in `integer_order_demo.py`,
`chamber_compression.py`, and `zeta_compression_probe.py` via `src/python`
bridge API (no re-implementation).

## Empirics

| Script | Finding | Output |
|--------|---------|--------|
| [empirics/zeta_compression_probe.py](./empirics/zeta_compression_probe.py) | [RH-105](./FINDINGS_INDEX.md) | [empirics/output/compression_probe_results.json](./empirics/output/compression_probe_results.json) |

### RH-105 F18 max-case scale extension (Q10 / #48)

**Deferred regime:** chamber Dirichlet increments at `q ≈ 1.5×10^7` (F18 max gap) with
pinned partial sum `N = 10^4`.

**Pinned empiric design (next run):**

1. **Segmented partial sums**: increase `N` to `10^5` or `10^6` with segmented
   prime sieve for primes up to `q`; record `ΔD/ΔB` at five pinned `s` values.
2. **Repro command:**
   ```bash
   PYTHONPATH=src/python:research/19-rh-corpus/empirics \
     python3 research/19-rh-corpus/empirics/zeta_compression_probe.py \
     --q-max 16000000 --partial-sum-n 100000 --emit-json
   ```
3. **Acceptance:** RH-105 row in FINDINGS_INDEX gains explicit `q ~ 10^7` regime
   with artifact path under `empirics/output/`.
4. **Boundary:** partial sums ≠ analytic continuation proof.

Flagship public demo (whitepaper companion):
`experiments/integer-order-before-zeta-whitepaper-2026-07/integer_order_demo.py`

## Maintenance

- Add new RH-facing rows to [FINDINGS_INDEX.md](./FINDINGS_INDEX.md) with the next `RH-###` ID.
- Run [scripts/scan_rh_references.py](./scripts/scan_rh_references.py) to surface candidate paths not yet indexed.
- Record scan gaps in [GAP_ANALYSIS.md](./GAP_ANALYSIS.md).
- Do **not** copy proof bodies into this folder: link only.

## Provenance

- **2026-07-08:** Chapter created to consolidate scattered RH-facing findings.
- **2026-07-08:** Population pass: layer docs expanded, RH-103 to 105 indexed, whitepaper §10 to 12, L3 empiric.