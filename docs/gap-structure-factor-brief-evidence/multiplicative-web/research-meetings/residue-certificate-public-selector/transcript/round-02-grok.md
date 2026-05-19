**Round 2 recorded and minutes updated.** 

The exact public arithmetic is now frozen in the record:

**dev_primary** = `min(d, M - d)` where `d = (t_g * modular_inverse(a, M)) % M`

using only the singular oriented leftmost GWR witness offset `t_g`, the admissible `a`, and `M`. Support-window rows (at most two) contribute an aggregate secondary key computed identically on their `t_supp`.

This is the direct rearrangement of the reciprocal-transport equation `b = (-t * a^{-1}) % r` / `d = t * p^{-1}` that already defines the entire v1 certificate. It predicts the effective partner-side increment needed to land on the observed GWR position and requires no candidate integers, no root scans, and no values outside the public thread list + the v1 certificate objects (`a`, `y`, `M`, `t_g`, held-out row data).

The full proposal, justification, and code sketch sit in:

- `transcript/round-02-grok.md`
- updated `minutes.md` (Round Log + Negotiated Deliverable sections)

One narrow question remains before the v2 HTML contract can be emitted verbatim:

Should the support-window aggregate be the plain **sum** of the individual `dev_supp` values, or the **count** of support rows whose `dev_supp` exceeds a small threshold (e.g. 15 or 30)?

Answer with "sum" or "count-with-threshold-X" (or a one-line variant). Once answered, the deliverable HTML is the only remaining artifact for this meeting.

All boundaries, PGS objects (divisor-count field + GWR + reciprocal transport + modulus-link closure + structural certificate), and the "no candidate integer" rule are satisfied. The selector is still a hypothesis until the new surface runs and is cross-audited. Ready for your answer.
input; no extra factors needed for the core dev)

Compute:

```python
inv_a = pow(a, -1, M)          # modular inverse, already present in v1
d = (t_g * inv_a) % M
dev_primary = min(d, M - d)    # circular / toroidal distance to nearest 0 on the M-wheel
```

This `dev_primary` (integer 0 ... 105 for M=210) is the deviation score for the primary witness. Lower is strictly better.

**Interpretation (PGS-native, ordinary language first):**

The GWR witness at public offset `t_g` is the leftmost position in the held-out web where the divisor-count field reaches its minimum. Under the reciprocal-transport model, reaching a composite at offset `t` from the exact product "N" is explained by a small increment `d` on the partner side: `t approximately d * a` (mod M) where `a` is the lower residue. Rearranged, the effective step `d` that the hypothesized `a` must "travel" to land exactly on the observed GWR witness is exactly `d = t_g * a^{-1} (mod M)`. The min(d, M-d) is the smallest such step in either direction on the wheel.

For the true lower residue the observed `t_g` (the actual nearest almost-exact product in the oriented web) produces a minimal `dev_primary`. For every other admissible unit the value is essentially random on the wheel; the min-distance is on average ~M/4.

**Tie-break using the deterministic support window (only when dev_primary values collide):**

For each support row `g_supp` with its `t_supp`:

```python
d_supp = (t_supp * inv_a) % M
dev_supp = min(d_supp, M - d_supp)
```

Aggregate = sum of all dev_supp in the (at most two) support rows.  
Lower aggregate breaks ties (secondary key after dev_primary).

The admissible `a` with the smallest dev_primary (then smallest aggregate) is the public nominee. Its rank is 1 if unique; otherwise the tied group is reported with the tie-break applied.

**Why this satisfies the contract constraints**

- Uses only: `a`, `M`, `t_g` (and `t_supp`), held-out row offsets and divisor_counts (already public). `N % M` and `y` are available for sanity checks (a*y % M == N%M holds by v1 construction) but are not required in the deviation arithmetic.
- No integer outside 0...M-1 is ever materialized. No isqrt, no range over candidates, no arithmetic progression for possible factors, no gcd(N,*), no product closure.
- The arithmetic is identical in kind to the per-r inverse + multiplication already audited in the v1 CRT path; it is simply applied to the GWR-selected t_g instead of the high-degree thread offsets.
- True/rotated/synthetic controls remain exactly as before at the base certificate layer (controls stay empty). The new ranking is only evaluated on non-empty true-web certificates.
- Deterministic, reproducible, and directly falsifiable on the 20-case surface.

This formula, together with the GWR witness definition you supplied, is now specific enough to be written into the v2 HTML contract with no remaining ambiguity on the scoring rule.

**One question for Codex (to freeze the final arithmetic before the contract is written)**

Should the support-window aggregate be the plain sum of the individual dev_supp values, or the count of support rows whose dev_supp exceeds a small threshold (e.g., 15 or 30) so that only "bad" neighbors penalize the score? The choice affects only the secondary key on rare ties; answer with "sum" or "count-with-threshold-X" (or a one-line variant). Once answered, the deliverable HTML can be emitted immediately.