# RH Corpus — Gap Analysis

**Date:** 2026-07-08  
**Method:** `python3 research/19-rh-corpus/scripts/scan_rh_references.py`  
**Baseline index:** 35 rows in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md)

This document records what the scan surfaced, what is already indexed, and what
the first population pass added or deferred.

---

## Scan summary

The scan lists repository paths whose text mentions RH-facing vocabulary but whose
path string does **not** appear verbatim in `FINDINGS_INDEX.md`. That is a
**candidate** list, not a mandate to index every FAQ page.

| Bucket | Count (approx.) | Action |
|--------|-----------------|--------|
| Already indexed via authority link | 12 | No new row (e.g. `PROOF.md`, `dni-to-zeta-compression.md`) |
| FAQ / reviewer control | 28 | Link from layer docs; no duplicate RH-### |
| Chapter homes (04, 12, 18, placement) | 14 | Partially indexed; extend layer bullets |
| Experiments / meetings | 6 | Index when finding is stable |
| Lean / formalization | 2 | Indexed as RH-080/081 |
| **New rows this pass** | 3 | RH-103, RH-104, RH-105 |

---

## Indexed in first population pass (2026-07-08)

| ID | Title | Why indexed |
|----|-------|-------------|
| [RH-103](./FINDINGS_INDEX.md) | F18-004 rough-witness signature | 40M exhaustive audit; compression-layer branch discipline |
| [RH-104](./FINDINGS_INDEX.md) | NLSC corollary + 10¹⁸ stress | Exact GWR corollary with pinned finite surface |
| [RH-105](./FINDINGS_INDEX.md) | Multi-s compression probe | Reproducible L3 partial-sum validation |

---

## Deferred (intentionally not indexed)

| Path | Reason |
|------|--------|
| `docs/faq/**` | Reviewer vocabulary; cite via [docs/rh/reviewer-map.md](../../docs/rh/reviewer-map.md) |
| `docs/essays/01_genesis_of_dni.md` | Historical narrative |
| `research/12-rh-bridge/**` (beyond RH-090–092) | Archived; cite workbench only |
| `research-meetings/**` | Transcript, not finding |
| `docs/earth-shattering-advancement-proposal.md` | Internal strategy memo |
| `experiments/chamber-tension-*`, `prefix-state-*` | Falsification designs; link when promoted |

---

## Layer coverage after pass

| Layer | Before | After |
|-------|--------|-------|
| L1 Divisor source | Table only | + structural invariants, F18/NLSC cross-links |
| L2 DNI coordinate | Table only | + worked examples, E/Z/H dictionary |
| L3 Zeta compression | Table only | + full mapping spec, branch notes, empiric hook |
| L4 Placement geometry | Table only | + chamber/resonance pointers |
| L5 Pole placement | Table only | + conditional map, obstruction summary |
| L6 Explicit formula | Table only | + super-signal oscillatory hook (labeled) |

---

## Whitepaper integration

Flagship narrative: [experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md](../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md)  
Indexed as [RH-041](./FINDINGS_INDEX.md). This pass extended §10–12 (bounded compression, F18, hub map).

---

## Next maintenance

1. Re-run scan after each `FINDINGS_INDEX` batch.
2. Promote FAQ-only material only when it states a **new** falsifiable claim.
3. Keep proof bodies in [PROOF.md](../../PROOF.md) and [docs/rh/](../../docs/rh/README.md) — link only here.