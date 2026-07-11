# RH Corpus: Start Here

**Time:** ~5 minutes  
**Goal:** Know what PGS claims about RH, what is proved, and where to click next.

---

## Hard frame rule (not optional)

**PGS is upstream. RH is downstream.** Full contract:
[FRAME_CONTRACT.md](./FRAME_CONTRACT.md).

RH language must never set the research driver. Work that starts from zeros,
poles, the critical line, or “prove RH,” then hunts for PGS objects that fit,
is a **contract violation**. It is not an alternate style.

```text
divisor counts → PGS local theorems → DNI-to-zeta compression
→ (optional) summatory source laws still free of zeros
→ only then source-to-spectral transfer, if forced by source
→ only then pole placement / RH sentence, if transfer closes
```

Nothing in layer 1 to 4 is a proof of the Riemann Hypothesis. Layer 5 is only
the **catalog** of the open downstream RH sentence. That sentence remains
**open**. New work must deepen upstream source laws, not optimize L5 packaging.

---

## Three sentences of program position

1. **Proved:** Given prime `p`, divisor-count traversal finds the next prime;
   gap interiors have GWR structure; bounded compression holds at Cramér scale
   (including derived factor ½). See [PROOF.md](../../PROOF.md).

2. **Exact:** The same divisor field compresses to `ζ(s)²` and
   `R(s) = -ζ'(s)/ζ(s)`. See
   [docs/rh/dni-to-zeta-compression.md](../../docs/rh/dni-to-zeta-compression.md).

3. **Open (downstream only):** Whether every nontrivial pole of `R(s)` lies on
   `Re(s)=½` (equivalently RH) is an unresolved *reading* of the source after
   compression. It is not an input to source work. See
   [docs/rh/off-critical-pole-exclusion.md](../../docs/rh/off-critical-pole-exclusion.md).

---

## Where to click

| I want to… | Go to |
|------------|-------|
| Read the **hard frame contract** | [FRAME_CONTRACT.md](./FRAME_CONTRACT.md) |
| Read the flagship narrative | [WHITEPAPER.md](../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md) ([RH-041](./FINDINGS_INDEX.md)) |
| See every finding in one table | [FINDINGS_INDEX.md](./FINDINGS_INDEX.md) (39 rows) |
| Understand the stack | [SOURCE_STACK.md](./SOURCE_STACK.md) |
| See what the scan found | [GAP_ANALYSIS.md](./GAP_ANALYSIS.md) |
| Prepare an X post / public thread | [READING_PATHS.md](./READING_PATHS.md) § Public |
| Review as a skeptic | [READING_PATHS.md](./READING_PATHS.md) § Reviewer + [docs/rh/reviewer-map.md](../../docs/rh/reviewer-map.md) |
| Work zeta compression (L3) | [by-layer/03-zeta-compression.md](./by-layer/03-zeta-compression.md) |
| Work **chamber / source** geometry (L4) | [by-layer/04-placement-geometry.md](./by-layer/04-placement-geometry.md) |
| Reproduce compression empirics | `PYTHONPATH=src/python:research/19-rh-corpus/empirics python3 research/19-rh-corpus/empirics/zeta_compression_probe.py` |
| Avoid overclaiming | Every row in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md) has a **Boundary** column: read it |

---

## Status vocabulary (fixed)

| Label | Means |
|-------|-------|
| `proved` | Universal theorem under stated hypotheses |
| `exact` | Identity-level compression or coordinate reformulation |
| `measured` | Finite computational audit, pinned regime |
| `hypothesis` | Interpretive bridge; not proved |
| `unresolved` | Named proof target; not closed |
| `invalidated` | Falsified conjecture with named artifact |
| `archived` | Off live surface; external pointer |
| `narrative` | Explanatory / public prose |

---

## What this folder is not

- Not a proof of RH
- Not a replacement for [PROOF.md](../../PROOF.md)
- Not a place to run RH-first research under PGS labels
- Not a revival of archived [12-rh-bridge](../12-rh-bridge/README.md) completion machinery
- Not a mirror of [docs/rh/](../../docs/rh/README.md), that bundle stays the public spine