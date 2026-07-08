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

## F18-002 — Finite Deterministic Verification

Pinned exhaustive enumeration (`q ≤ 10^6`): **zero** violations of `C(q)`;
50th percentile of witness distance `2`; maximum witness distance `48`.

| Axis | Value |
|------|-------|
| Logical status | `verified` (finite pinned regime) |
| Method | Deterministic GWR replay; no sampling |
| Provenance | [finite-verification-grok-509b8495.md](./finite-verification-grok-509b8495.md) |

**Boundary.** Confirms F18-001 on a stated finite surface only; does not extend
the universal proof.

---

## F18-003 — Half-Scale Correspondence (Hypothesis)

The shared factor `1/2` between `⌈0.5 · (log q)²⌉` and `Re(s) = 1/2` is
**conjectured** to mark the same scale along the divisor → ζ(s)² compression
chain. **Not proved.**

See [half-scale-correspondence-hypothesis.md](./half-scale-correspondence-hypothesis.md).