# RH Corpus — Start Here

**Time:** ~5 minutes  
**Goal:** Know what PGS claims about RH, what is proved, and where to click next.

---

## The one rule

RH language is **downstream**. Integer divisor structure is **upstream**.

```text
divisor counts → PGS local theorems → DNI-to-zeta compression
→ source-to-spectral placement → pole placement / RH sentence
```

Nothing in layer 1–3 is a proof of the Riemann Hypothesis. Layer 5 is where RH
actually lives — and it remains **open** in this program.

---

## Three sentences of program position

1. **Proved:** Given prime `p`, divisor-count traversal finds the next prime;
   gap interiors have GWR structure; bounded compression holds at Cramér scale
   (including derived factor ½). See [PROOF.md](../../PROOF.md).

2. **Exact:** The same divisor field compresses to `ζ(s)²` and
   `R(s) = -ζ'(s)/ζ(s)`. See
   [docs/rh/dni-to-zeta-compression.md](../../docs/rh/dni-to-zeta-compression.md).

3. **Open:** Showing every nontrivial pole of `R(s)` lies on `Re(s)=½` —
   equivalently RH — requires a source-to-spectral placement theorem not yet
   closed. See
   [docs/rh/off-critical-pole-exclusion.md](../../docs/rh/off-critical-pole-exclusion.md).

---

## Where to click

| I want to… | Go to |
|------------|-------|
| See every finding in one table | [FINDINGS_INDEX.md](./FINDINGS_INDEX.md) |
| Understand the stack | [SOURCE_STACK.md](./SOURCE_STACK.md) |
| Prepare an X post / public thread | [READING_PATHS.md](./READING_PATHS.md) § Public |
| Review as a skeptic | [READING_PATHS.md](./READING_PATHS.md) § Reviewer + [docs/rh/reviewer-map.md](../../docs/rh/reviewer-map.md) |
| Work placement geometry | [by-layer/04-placement-geometry.md](./by-layer/04-placement-geometry.md) |
| Avoid overclaiming | Every row in [FINDINGS_INDEX.md](./FINDINGS_INDEX.md) has a **Boundary** column — read it |

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
- Not a revival of archived [12-rh-bridge](../12-rh-bridge/) completion machinery
- Not a mirror of [docs/rh/](../../docs/rh/) — that bundle stays the public spine