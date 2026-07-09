# Layer 1: Divisor source

**Status mix:** `proved`, `narrative`, `measured`  
**Proves RH?** No: this is the upstream arithmetic authority

Layer 1 is the **proved local mechanism**: divisor counts on integers, ordered gap
interiors, GWR selection, and Cramér-scale bounded compression. Every RH-facing
claim downstream assumes this layer is correct.

**Authority:** [PROOF.md](../../../PROOF.md): do not duplicate proof bodies here.

---

## Structural invariants

| Invariant | Statement | ID |
|-----------|-----------|-----|
| Next-prime read | $q=\min\{n>p:\tau(n)=2\}$ | [RH-001](../FINDINGS_INDEX.md) |
| GWR witness | $w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}$ maximizes $F(n)=-E(n)$ | [RH-002](../FINDINGS_INDEX.md) |
| Bounded compression | $w-p\le C(q)=\max(64,\lceil\tfrac12(\log q)^2\rceil)$ | [RH-003](../FINDINGS_INDEX.md) |
| Square branch | Prime-Square Proximity closes $\tau(w)=3$ case | [RH-004](../FINDINGS_INDEX.md) |
| Twin termination | $w\equiv 0\pmod{30}$ with 4+ remainder zeros $\Rightarrow$ gap $=2$ | [RH-005](../FINDINGS_INDEX.md) |
| Half-coefficient | $0.5$ in $C(q)$ from divisor-average closure, not calibration | [RH-006](../FINDINGS_INDEX.md) |
| NLSC corollary | No later interior point has strictly smaller $\tau$ after $w$ | [RH-104](../FINDINGS_INDEX.md) |

---

## Gap interior as ordered field

Between primes $p<q$, the interior $I=\{p+1,\ldots,q-1\}$ carries an **ordered
divisor-count row**. This is not empty distance, it is the data that selects
$w$ and fixes $q$.

```text
p ──[ τ(p+1), τ(p+2), …, τ(q-1) ]── q
         ↑
    GWR witness w (leftmost min-τ)
```

Chapter home: [04-bounded-compression](../../04-bounded-compression/README.md)

---

## F18 refinements (chapter 18)

| Finding | Status | RH link |
|---------|--------|---------|
| F18-001 derived $\tfrac12$ | proved | [RH-006](../FINDINGS_INDEX.md) |
| F18-002 finite $C(q)$ audit | measured | [RH-070](../FINDINGS_INDEX.md) |
| F18-003 half-scale correspondence | hypothesis | [RH-040](../FINDINGS_INDEX.md) |
| F18-004 rough-witness signature | measured | [RH-103](../FINDINGS_INDEX.md) |

F18-004 matters for compression exposition: it shows **non-square** near-maximal
witnesses must be divisor-rough, while **square** witnesses follow a separate
tiling lane, see [03-zeta-compression.md](./03-zeta-compression.md).

---

## Indexed findings

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-001](../FINDINGS_INDEX.md) | proved | Direct next-prime rule | [PROOF.md](../../../PROOF.md) |
| [RH-002](../FINDINGS_INDEX.md) | proved | Interior maximizer (GWR) | [PROOF.md](../../../PROOF.md) |
| [RH-003](../FINDINGS_INDEX.md) | proved | Universal bounded compression | [PROOF.md](../../../PROOF.md), [04-bounded-compression](../../04-bounded-compression/README.md) |
| [RH-004](../FINDINGS_INDEX.md) | proved | Prime-Square Proximity | [PROOF.md](../../../PROOF.md) |
| [RH-005](../FINDINGS_INDEX.md) | invalidated | Twin-Prime Resonance (universal implication) | [twin-prime-resonance-technical-note-2026-07](../../twin-prime-resonance-technical-note-2026-07/TECHNICAL_NOTE.md) |
| [RH-006](../FINDINGS_INDEX.md) | proved | Derived ½ coefficient | [18-derived-half-coefficient](../../18-derived-half-coefficient/README.md) |
| [RH-041](../FINDINGS_INDEX.md) | narrative | Integer order before zeta | [WHITEPAPER.md](../../../experiments/integer-order-before-zeta-whitepaper-2026-07/WHITEPAPER.md) |
| [RH-042](../FINDINGS_INDEX.md) | narrative | RH is obsolete essay | [docs/essays/the-riemann-hypothesis-is-obsolete.md](../../../docs/essays/the-riemann-hypothesis-is-obsolete.md) |
| [RH-043](../FINDINGS_INDEX.md) | narrative | Derived ½ tech note | [30-30-30-technical-note](../../18-derived-half-coefficient/30-30-30-technical-note/TECHNICAL_NOTE.md) |
| [RH-070](../FINDINGS_INDEX.md) | measured | GWR bound audit (F18-002) | [experiments/grok-share-509b8495/safari_transcript.txt](../../../experiments/grok-share-509b8495/safari_transcript.txt) |
| [RH-102](../FINDINGS_INDEX.md) | narrative | Source order | [docs/rh/source-order.md](../../../docs/rh/source-order.md) |
| [RH-103](../FINDINGS_INDEX.md) | measured | F18-004 rough-witness | [FINDING_STATEMENT.md](../../18-derived-half-coefficient/docs/FINDING_STATEMENT.md) |
| [RH-104](../FINDINGS_INDEX.md) | proved | NLSC corollary | [docs/RESULTS.md](../../../docs/RESULTS.md) |

---

## What L1 does **not** establish

- Critical-line zero placement (L5)
- Prime Number Theorem as a new proof
- Statistical random-gap models

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md)