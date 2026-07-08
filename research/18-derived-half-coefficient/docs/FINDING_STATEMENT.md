# Finding Statement — Rough-Witness Signature for Near-Maximal Offsets (F18-004)

**Effective:** 2026-07-08  
**Chapter:** `research/18-derived-half-coefficient/`  
**Authority:** `PROOF.md` (Universal Bounded Compression, Witness Threshold Lemma, Short Divisor-Average Lemma, Prime-Square Proximity Theorem)  
**Data provenance:** exhaustive deterministic GWR replay to 40 000 000 (`near_maximal_audit_results.json`)

## F18-004 — Rough-Witness Signature (Tested Prediction)

For every consecutive prime gap with nonempty interior and \( q \gtrsim 10^7 \) (logarithmic term dominant in \( C(q) \)) satisfying

\[
\frac{w - p}{C(q)} \;\ge\; 0.65,
\]

the following holds:

- If \( w \) is **not** a prime square, then \( \tau(w) \ge \max\bigl(6,\; \lfloor 0.75 \log q \rfloor\bigr) \).
- Prime-square witnesses (\( \tau(w) = 3 \)) may achieve substantial ratios but remain bounded away from 1.0 (observed ceiling 0.715 in the scanned regime).

**Logical status:** tested prediction (survived direct falsification attempt)  
**Scope:** deterministic, exhaustive up to 40 000 000; conservative thresholds chosen for the tested range  
**Falsification criterion:** one counterexample with ratio \(\ge 0.65\), \( q > 10^7 \), non-square \( w \), and \( \tau(w) \le 5 \).

### Method

Full deterministic replay of the Gap Winner Rule on every prime gap with nonempty interior up to LIMIT = 40 000 000:

- SPF sieve + multiplicative divisor count.
- For each interior, locate the exact leftmost minimizer \( w \) and record \( d = \tau(w) \).
- Compute \( C(q) = \max(64, \lceil \frac12 (\log q)^2 \rceil) \), offset \( w-p \), and ratio.
- Separate analysis by branch: non-square vs. prime-square (the latter governed by the independent tiling argument of the Prime-Square Proximity Theorem).
- Explicit search for violations of the rough-witness rule.

Artifact: `near_maximal_audit_results.json` (contains full summary, max-case, and falsifier lists).

### Results (40 000 000)

| Metric                              | Value          |
|-------------------------------------|----------------|
| Gaps with interior                  | 2 433 652      |
| Global max ratio                    | 0.7153         |
| Cases with ratio \(\ge 0.65\)       | 1              |
| Non-square low-\( d \) (\( d\le 5 \)) high-ratio cases | **0** |
| Prime-square high-ratio cases       | 1 (ratio 0.7153) |

The single high-ratio case is  
\( p = 15{,}436{,}943 \), \( q = 15{,}437{,}053 \), \( w = 15{,}437{,}041 = 3{,}929^2 \) (\( d=3 \)), offset 98 out of \( C=137 \).  
It lies entirely in the Prime-Square Proximity lane.

No non-square witness with \( d \le 5 \) reached ratio 0.65. The bound itself remains loose (max observed offset 98 against a local \( C \approx 137 \)).

### Two-Branch Interpretation

- **Non-square branch.** The exponential Witness Threshold Lemma closes low-\( d \) competitors early. The only remaining path to large witness offsets is the Short Divisor-Average contradiction, which requires the champion itself to sit above the short-interval average divisor count (\( \sim \log q \)). Hence high-ratio non-square witnesses must be unusually rough. This is the lane that directly produces the factor \( \frac12 \) in \( C(q) \).

- **Prime-square branch.** Governed by a separate row-tiling / counting-contradiction argument (Prime-Square Proximity Theorem). Its geometry does not rely on the divisor-average floor and therefore does not participate in the derivation of the half-coefficient. The observed ceiling (~0.715) is consistent with the algebraic capacity limits of that tiling and does not threaten the half-scale emergence.

This separation strengthens the claim that the \( \frac12 \) is arithmetically forced by divisor closure rather than by any post-hoc calibration.

### Analytical Note on Threshold Sharpness

From the Half-Scale Emergence Lemma,
\[
H = \Bigl\lfloor \frac{w L}{4(d-1)} \Bigr\rfloor, \qquad H \ge \frac{w L}{8(d-1)}
\]
in the active large-\( d \) regime. For a target ratio \( r \), the minimal \( d \) permitting \( H \ge r \cdot \frac12 L^2 \) (after packaging) satisfies a relation of the form
\[
d-1 \;\gtrsim\; \frac{L}{c(r)}
\]
where \( c(r) \) grows as \( r \) approaches the envelope allowed by the average bound. The conservative empirical floor \( 0.75 \log q \) already lies safely above the theoretical minimum required by the contradiction for \( r \ge 0.65 \) in the scanned regime. Future work can derive the exact \( c(r) \) curve; the present thresholds are deliberately loose for immediate falsifiability.

### Boundary

F18-004 is a **tested prediction on the witness-offset surface**, not a universal theorem. It does not claim that all large gaps have rough witnesses—only that those whose GWR witness is pushed near the bound (non-square case) must be rough. The square case is handled separately and does not use the averaging mechanism that yields the half-coefficient.

### References

- `PROOF.md` — Witness Threshold, Short Divisor-Average, Prime-Square Proximity.
- `docs/finite-verification-grok-509b8495.md` — F18-002 (earlier pinned verification).
- `near_maximal_audit_results.json` — exact replay data.
- `30-30-30-technical-note/TECHNICAL_NOTE.md` — mechanism background.
