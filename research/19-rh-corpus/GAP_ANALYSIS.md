# RH Corpus: Gap Analysis

**Date:** 2026-07-09 (updated)  
**Method:** `python3 research/19-rh-corpus/scripts/scan_rh_references.py`  
**Index:** 39 rows in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md)

---

## High-signal paths: indexed vs deferred (with boundaries)

| Path | Disposition | RH ID / pointer | Boundary |
|------|-------------|-----------------|----------|
| `PROOF.md` | Indexed (authority) | RH-001 to 006 | Proves L1 only; not RH |
| `research/18-derived-half-coefficient/README.md` | Indexed | RH-006 | F18-001 derived ½; not Cramér proof |
| `research/18-derived-half-coefficient/docs/FINDING_STATEMENT.md` | Indexed | RH-103 | F18-004 tested prediction; not theorem |
| `research/18-derived-half-coefficient/docs/half-scale-correspondence-hypothesis.md` | Indexed | RH-040 | Hypothesis; ½≠Re(s)=½ proved |
| `research/18-derived-half-coefficient/FORMALIZATION_PROPOSAL.md` | **Deferred** |: | Lean roadmap memo; no new finding |
| `research/18-derived-half-coefficient/30-30-30-technical-note/` | Indexed | RH-043 | Exposition of proved F18-001 |
| `research/pgs-rh-placement-empirics-2026-06/d4_fractional_position_bound.md` | Indexed | RH-030 to 032 | d=4 geometry; not RH |
| `research/pgs-rh-placement-empirics-2026-06/source_to_spectral_transfer_lemma.md` | Indexed | RH-035 | Draft lemma; explicitly not RH |
| `research/pgs-rh-placement-empirics-2026-06/pgs_chamber_budget_summary_1000000.md` | Indexed | RH-034 | Finite regime measured |
| `research/pgs-rh-placement-empirics-2026-06/pgs_rh_bridge_placement_focus_prompt.md` | **Deferred** |: | Internal prompt; not a finding |
| `experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md` | Indexed | RH-041 | Narrative; not theorem |
| `docs/rh/dni-to-zeta-compression.md` | Indexed | RH-020 to 021 | Exact compression; not placement |
| `docs/faq/**` | **Deferred** |: | Reviewer vocabulary; link via [reviewer-map](../../docs/rh/reviewer-map.md) |
| `research/12-rh-bridge/**` (beyond RH-090 to 092) | **Deferred** | RH-090 to 092 archived | Do not route new work here |
| `research-meetings/**` | **Deferred** |: | Transcript only |

Layer deferral mirrors: [04-placement-geometry.md](./by-layer/04-placement-geometry.md) § Deferred scan paths.

---

## Scan summary

| Bucket | Count (approx.) | Action |
|--------|-----------------|--------|
| FAQ / reviewer control | 28 | Deferred (see table) |
| Chapter homes partially indexed | 14 | Rows above |
| **Indexed this program** | 39 | FINDINGS_INDEX |

---

## Empirics and tests

| Artifact | Role |
|----------|------|
| [empirics/chamber_compression.py](./empirics/chamber_compression.py) | GWR→ΔD/ΔB mapping via `src/python` bridge |
| [empirics/zeta_compression_probe.py](./empirics/zeta_compression_probe.py) | RH-105 chamber + F18 max-case probe |
| `research/19-rh-corpus/tests/` | Imports shipped demo + chamber modules (see README § Tests) |

```bash
PYTHONPATH=src/python:research/19-rh-corpus/empirics python3 -m pytest research/19-rh-corpus/tests/ -q
```

---

## Maintenance

1. Re-run scan after each FINDINGS_INDEX batch.
2. Every deferred path needs a **boundary** column before closing a gap-analysis pass.
3. Proof bodies stay in canonical homes, link only in this hub.

**Last scan (2026-07-09, curation):** `python3 research/19-rh-corpus/scripts/scan_rh_references.py`
: ~28 FAQ paths + chapter homes remain **deferred** per table above; 39 rows indexed
in FINDINGS_INDEX. RH-105 multi-s surface regenerated (`s ∈ {2.0,2.5,3.0,3.5,4.0}`,
N=10⁴). No theorem promotions this pass.