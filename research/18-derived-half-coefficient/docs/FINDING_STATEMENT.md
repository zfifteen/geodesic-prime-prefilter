# Finding Statement — Derived Half-Coefficient

**Effective:** 2026-07-08  
**Chapter:** `research/18-derived-half-coefficient/`

---

## F18-001 — Derived Half-Coefficient (Principal Finding)

For consecutive primes `p < q` with nonempty interior, the GWR witness `w`
satisfies

```text
w - p ≤ C(q) = max(64, ceil(0.5 * log(q)^2))
```

The coefficient `0.5` is **derived** from Short Divisor-Average closure
(`H ≲ L²/8`), not chosen to match Cramér or `Re(s) = 1/2`.

| Axis | Value |
|------|-------|
| Logical status | `proved` |
| Scope | `universal` |
| Proof authority | `PROOF.md` §305–520, §574–679 |

**Boundary.** Bounds selected witness offset `w − p` only.

---

## F18-002 — Independent External Corroboration

Independent Grok audit (2026-07): zero violations of `C(q)` for `q ≤ 10^6`;
median distance 2; max distance 48.

| Axis | Value |
|------|-------|
| Logical status | `measured` |
| Provenance | [external-validation-grok-509b8495.md](./external-validation-grok-509b8495.md) |

---

## F18-003 — Half-Scale Correspondence (Hypothesis)

Shared factor `1/2` between `⌈0.5 · (log q)²⌉` and `Re(s) = 1/2` may reflect
compression-chain structure. **Not proved.**

See [half-scale-correspondence-hypothesis.md](./half-scale-correspondence-hypothesis.md).