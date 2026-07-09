# Derivation Chain Digest: Where `0.5` Emerges

**Finding:** F18-001 · **Authority:** `PROOF.md`

## Target

```text
w - p ≤ C(q) = max(64, ceil(0.5 * log(q)^2))
```

## Chain

1. **Witness Threshold**: close earlier high-τ competitors via `T(d,e)`.
2. **Interval choice**: `H = floor(wL / (4(d−1)))`, hence `H ≥ wL / (8(d−1))`.
3. **Short Divisor-Average**: average on `J = {w−H,…,w−1}` is `< d`; forces `w−p ≤ H`.
4. **Log closure**: all earlier competitors have `F(k) < F(w)`.
5. **Half-scale**: `H = O(L²)` with constant `1/8` → `w−p ≲ 0.5 · (log q)²`.

The `0.5` propagates from the inequality chain, not from fitting Cramér.