# PGS Prediction Inventory (audit-ready)

**Updated:** 2026-07-14 (H1′-H4′ merge, Schedule, certificate pins)  
**Authority:** `PROOF.md` for theorem status; `docs/RESULTS.md` / `AGENTS.md` for surfaces; residual pins for research hypotheses  
**Advance note:** `ADVANCE_2026-07-14.md`  
**Rule:** finite checks **corroborate** implementations and finite premises; they do **not** re-prove universal theorems.  
**Forbidden as predictions:** twin-prime infinitude, RH solve, RSA factor recovery as PGS inference, Rowland/gcd engines, Zhang-Maynard gap bound as PGS theorem.

How to read columns:

- **Status:** theorem | finite-certified premise | implementation | measured | hypothesis | invalidated
- **Check:** command or criterion that can fail in CI or a harness
- **Kill condition:** what would falsify the *prediction as stated* (for theorems: contradiction of claim under hypotheses; usually means proof error or broken implementation, not a single mid-scale miss of a universal law)

---

## Soft wording corrections to Grok’s draft

| Draft risk | Correction |
| --- | --- |
| “Empty or structured gap interior” as a separate mystery theorem | Composite interior is the definition of consecutive primes; the **checkable** content is next-prime via first `τ=2` (**theorem**). |
| “validated surface” for recursive walk counts | Prefer **measured** / **implementation** exactness on the named regime; program-level **verified** requires executed `10^18` surface in the same package (`AGENTS.md`). |
| Residual D “holds” as if universal | **Measured** on named fixtures; D as a general law stays **hypothesis**. |
| Dual-gap constants as if predicted free laws | **Hypothesis** gates only until derived or killed. |
| NLSC “stress surface zero violations” | Corollary is **theorem**; stress surface is **audit corroboration**, not the proof. |

---

## A. Theorem-level predictions

### T1. Direct next-prime operator
- **Statement:** For prime `p` under `PROOF.md` hypotheses, `q = min{n > p : τ(n) = 2}` is the next prime.
- **Status:** theorem (`PROOF.md` Headline / next-prime rule)
- **Check:** `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py -q` (implementation of the rule on test fixtures); certificate replay `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma gwr_finite_base_v1` for the finite premise side
- **Kill:** A prime `p` and integer `n` with `p < n < q_true` and `τ(n)=2`, or generator `q ≠` true successor on a correct divisor oracle (implementation kill if oracle is exact)

### T2. Interior maximizer (GWR)
- **Statement:** In a nonempty gap `(p,q)`, the leftmost interior min-`τ` integer `w` uniquely maximizes the named score (`F = -E` in zero-excess form).
- **Status:** theorem (`PROOF.md` Interior Maximizer)
- **Check:** `python3 -m pytest research/02-gwr-dni/tests -q` (and any GWR-specific unit tests in that tree)
- **Kill:** Interior point `w' < w` with `τ(w') ≤ τ(w)`, or another min-`τ` point left of the claimed maximizer under the stated score

### T3. Universal bounded compression (selected-witness offset)
- **Statement:** For every consecutive gap with nonempty interior, `w - p ≤ max(64, ceil(0.5 * (log q)^2))`.
- **Status:** theorem (`PROOF.md` UBC, 2026-07-05). **Not** a bound on raw gap `q - p`. **Not** RH/PNT.
- **Finite check ≠ re-proof:** Audit bands, decade samples, and certificate replay **corroborate** the implementation and finite premises; they do **not** re-prove the universal statement. Proof-spine / Lean pressure is **proof-support**, not a silent demotion (`PROOF.md` still controls).
- **Check:** Square-branch / compression audit harnesses under `research/04-bounded-compression/` (regime-bounded corroboration); finite premise replay under F2
- **Kill:** A consecutive gap with nonempty interior whose GWR witness violates the inequality (theorem kill). Implementation miss on a named band without a true counterexample is **implementation** failure only.

### T4. Prime-Square Proximity (square branch)
- **Statement:** On square-branch witnesses (`τ(w)=3`, `w=r^2`), the dynamic cutoff / PSP binds the offset as stated in `PROOF.md`.
- **Status:** theorem (`PROOF.md` Prime-Square Proximity)
- **Finite check ≠ re-proof:** Green square-branch audits on new regimes are **audit corroboration** only. Do not treat them as re-proof or as RH/gap-size claims. Open Lean/spine hygiene stays proof-support unless a human-approved status process runs.
- **Check:** Square-branch audit jobs / queue items under `research/04-bounded-compression/output/` and chapter tests
- **Kill:** Square-branch gap whose certified GWR witness violates PSP/UBC as stated

### T5. No-later-simpler-composite (NLSC)
- **Statement:** After GWR witness `w`, no later interior composite with strictly smaller `τ` appears before `q`.
- **Status:** theorem (exact corollary of GWR; `docs/RESULTS.md` Recursive Walk section)
- **Check:** Generator / GWR tests that assert NLSC on fixtures; optional stress surfaces are **audit corroboration** only
- **Kill:** Interior `n` with `w < n < q` and `τ(n) < τ(w)`

### T6. Modular zero lemma on `M_v1` (vector-fixed)
- **Statement:** On fixed modulus vector `M_v1 = {2,3,5,7,30,210,2310}`, `z(w) ≥ 4 ⇔ 30 | w`.
- **Status:** theorem (`PROOF.md` modular zero lemma; scope **vector only**)
- **Check:** Unit tests covering the modular lemma / Super-Signal counterexample package that assert the biconditional on `M_v1` without reviving Super-Signal
- **Kill:** `w` with `z(w)≥4` but `30 ∤ w`, or `30|w` but `z(w)<4`, on that exact vector

### T7. Super-Signal universal twin lock stays dead
- **Statement:** The universal implication `z(w) ≥ 4 ⇒ g = 2` is **false**.
- **Status:** invalidated (`PROOF.md` Twin-Prime Resonance / Super-Signal section; 2026-07-09)
- **Check:** `python3 -m pytest research/01-generator/tests/test_super_signal_counterexample_generator.py -q` (and residual FP catalog under `research/16-predictions/probes/super-signal-fp-signature-2026-07/`)
- **Kill:** A proof that restores the universal implication (would require overturning known counterexamples). Scans claiming zero FPs past known counterexample surfaces without those FPs are **truncated or wrong** (process kill)

### T8. Fixed cutoff map stays dead
- **Statement:** The old fixed cutoff map `{2:44, 4:60, 6:60}` is not a universal law.
- **Status:** invalidated (`PROOF.md` / `AGENTS.md` / continuity)
- **Check:** Any revival PR that re-installs fixed cutoffs as theorem language fails review; regression tests should not depend on that map as universal
- **Kill:** N/A as positive prediction; **revival** is the failure mode

---

## B. Finite-certified premises (proof machinery, not universal theorems)

### F1. `gwr_finite_base_v1`
- **Statement:** Exhaustive earlier-integer / GWR finite closure on the stated range (`2 ≤ p < 5_000_000_001` per `PROOF.md`).
- **Status:** finite-certified premise
- **Certificate path:** `docs/proof-enhancements/certificates/gwr_finite_base_v1.json`
- **Pinned SHA-256 (2026-07-14):** `3e93899f6eac87478b60559547edc150545c3db998665d89b2b5bb8c291e2e8a`
- **Check:** `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma gwr_finite_base_v1` then `shasum -a 256 docs/proof-enhancements/certificates/gwr_finite_base_v1.json` must match the pin (or an intentionally re-pinned update with proof-process note)
- **Kill:** Certificate replay mismatch or a gap inside the named finite range violating the closed claim

### F2. `bounded_compression_base_v1`
- **Statement:** Finite bounded-compression base for `q < ceil(exp(16))` as in `PROOF.md`.
- **Status:** finite-certified premise
- **Certificate path:** `docs/proof-enhancements/certificates/bounded_compression_base_v1.json`
- **Pinned SHA-256 (2026-07-14):** `c7f25f74d0ad0d20f70b1755712ac133fb25162f126b65350a4882288baa6f0c`
- **Check:** `python3 docs/proof-enhancements/scripts/emit_certificates.py --lemma bounded_compression_base_v1` then `shasum -a 256 docs/proof-enhancements/certificates/bounded_compression_base_v1.json` must match the pin
- **Kill:** Replay mismatch or counterexample inside the finite base range

---

## C. Implementation-level predictions

### I1. Generator stream purity
- **Statement:** Resolved outputs are exactly `{"p","q"}`; unresolved is explicit; no confidence fields; audit does not choose `q`.
- **Status:** implementation (Minimal PGS Generator contract; `docs/PRIME_GAP_GENERATOR.md`, `AGENTS.md`)
- **Check:** `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/01-generator/tests/test_prime_inference_generator.py -q`
- **Kill:** Emitted diagnostics in the main stream, classical fallback selecting `q`, or silent wrong `q`

### I2. Full-exact mid band
- **Statement:** On committed full-exact bands reported in `docs/RESULTS.md` (e.g. `11..100000` class and larger exact surfaces named there), exact PGS outputs with zero unresolved and zero audit failures for the production path.
- **Status:** implementation / measured on those regimes (`docs/RESULTS.md`: e.g. `9588/9588` on `11..100000`; AGENTS also cites `11..1000000`)
- **Check:** Production generator audit command documented in `docs/PRIME_GAP_GENERATOR.md` / generator chapter; unit suite above for smoke
- **Kill:** Any mismatch or unresolved on the named band under the production rule

### I3. Decade ladder through `10^18`
- **Statement:** 256 consecutive input primes per decade, decades `10^8`..`10^18` (2816 primes): exact next-prime recoveries, zero incorrect candidates on that committed surface.
- **Status:** implementation surface (required for program-level **verified/validated** generator language per `AGENTS.md`)
- **Check:** High-scale decade-window validation path in `research/01-generator/output/` / commands in `docs/PRIME_GAP_GENERATOR.md`; do not claim verified if the ladder was not executed
- **Kill:** Incorrect `q` or unresolved on any ladder prime when run with the production rule

### I4. Audit separation
- **Statement:** Classical primality APIs may confirm after generation; they must not select `q` in the generation path.
- **Status:** implementation / process contract
- **Check:** Code review of generation path + tests that fail if `isprime`/`nextprime`/MR appear in selection; generator docs exclusion list
- **Kill:** Import of classical primality into the selection branch of production generator

### I5. Recursive walk exactness (named regimes)
- **Statement:** Exact consecutive next-prime recoveries on the regimes reported in `docs/RESULTS.md` (e.g. `11` through `10_000_121` walk counts; sampled recursive decade steps).
- **Status:** measured / implementation on exact regimes (not a new theorem)
- **Check:** Recursive walk tests under `research/02-gwr-dni/tests` (e.g. `test_gwr_dni_recursive_walk.py` when present) and chapter commands in continuity START_HERE
- **Kill:** Skipped gap or wrong successor on the named measured regime

### I6. Anti-admission of false RSA public class
- **Statement:** Historical false class `(32047651, 32059633)` is never emitted as a structural endpoint class.
- **Status:** implementation (rsa-v3 residual honesty package)
- **Check:** `python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py -q` (phase-1 anti-admission)
- **Kill:** Emit path admits that pair as endpoint class

---

## D. Hypothesis-level predictions (falsifiable research; anti-gaming)

Merged from Claude rewrites (H1′-H4′). Prior soft H1-H4 rows are **replaced** by these.

### H1′. Constant-neighborhood residual honesty (50-bit pin)
- **Statement:** On the golden 50-bit pin, for dual-gap form `boundD = max(C1, floor(α(g_lo+g_up)))` with `(C1, α)` in a named neighborhood of the fitted gate (default grid C1 ∈ [10,40], α ∈ [0.8, 2.0]), under an **unchanged** first-tail window and no classical smuggle, the **decision residual** stays `unresolved_by_first_tail_misalignment` (not a silent false endpoint). Dual-gap D may still pass as a gate on the fixture; that pass is **measured**, not a universal law.
- **Status:** measured on fixtures for the fitted gate; neighborhood stability and D-as-law = **hypothesis** (`ACTIVE_GOAL_50bit_residual_discriminator.md`)
- **Check:** `python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py -q` plus residual honesty package under `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/`; constant-neighborhood sweep when harness lands (Schedule driver 3)
- **Kill (honesty):** Endpoint class emit without new public geometry; residual changes only via window widen or classical gate
- **Kill (neighborhood):** Some in-grid `(C1,α)` yields honest endpoint close with fixed first-tail window (then document the geometry or accept D-form break)

### H2′. No close by monotone constant relaxation
- **Statement:** Closing 50-bit by **only** loosening `boundD` / first-tail constants (monotone relaxation), without a new public geometric law or derived gate, is a **falsification of residual honesty**, not a success.
- **Status:** hypothesis / process prediction
- **Check:** Any “green” close must ship a ledger with first-tail pass under **unchanged** window; constant-gaming sweep (Schedule driver 3): pure retune must not emit endpoint class
- **Kill:** Documented structural “resolution” that only changes free constants or widens windows

### H3′. Free constants break or are derived
- **Statement:** Forms such as `boundD = max(20, floor(1.2*(g_lo+g_up)))` are **hypothesis gates**. They are predicted either to **break** at some scale with honest residuals, or to be **replaced by a derivation**. Larger-surface revalidation alone does **not** promote them to law.
- **Status:** hypothesis
- **Check:** Fixed-window scale/fixture sweeps; derivation PR or named break with residual codes
- **Kill:** Systematic honest breaks at higher bit length (constants die); or derivation retires the hypothesis upward

### H4′. Super-Signal stays dead under reparameterization
- **Statement:** No reparameterization restores universal zero-FP Super-Signal on surfaces that still include known class-B counterexamples. Narrowing scope to hide CEs is not restoration. Catalog “FPs in R0” remains **measured/hypothesis**, not `z≥4 ⇒ (g=2 or R0)` as theorem.
- **Status:** Super-Signal universal lock **invalidated**; R0 universality **unresolved** / hypothesis (`research/16-predictions/probes/super-signal-fp-signature-2026-07/`)
- **Check:** `python3 -m pytest research/01-generator/tests/test_super_signal_counterexample_generator.py -q`; probe anti-revival README + measure scripts
- **Kill:** Restored universal zero-FP claim that still covers known CE regimes (false); or FP outside R0 on a complete claimed scan; or theorem promotion without proof process

### H5. Constellation non-merge
- **Statement:** PGS residual / gap measurements do not predict twin-prime infinitude, free 0,2,4 triples beyond (3,5,7), or Hardy-Littlewood.
- **Status:** process / non-claim (classical comparison notes under `experiments/constellation-vs-pgs-next-prime-2026-07/`)
- **Check:** Continuity review of any residual writeup for constellation slogan merge
- **Kill:** N/A as math prediction; **documentation failure** if claims appear

### H-cell. Joint residual cell R + pinch S (C1T2L1 breakthrough candidate)
- **Statement:** Public residual geometry is ranked as `R = (r_carrier, r_tail, r_lock)` with decision cell `C*T*L*` and pinch `S = |T_c - upper.anchor| + |delta_t|` (floor transport only). On the golden 50-bit false pin the joint cell is **C1T2L1** with measured `pinch_S = 54`, and the decision residual migrates to taxonomy code `unresolved_by_joint_cell_C1T2L1` (not a silent endpoint class). On the 64-bit true close pin the cell is **C0T0L0** with measured `pinch_S = 21` and the closure stack holds. Dual-gap D may still hold on the false pin; the joint cell names the real obstruction. Rank cut thresholds and pinch as a separator on broader fixtures remain **hypothesis**.
- **Status:** residual map + cell rule = **hypothesis**; 50-bit vs 64-bit unit-pin separation = **measured** on those fixtures only; implementation in rsa-v3 GWR stack. **Not** theorem. **Not** verified residual-family (no residual 10^18). **Not** RSA solve.
- **Taxonomy:** `unresolved_by_joint_cell_C1T2L1` in `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/RESIDUAL_TAXONOMY.md` and `residual.py` (present; no code-taxonomy lag). Continuity pin `ACTIVE_GOAL_50bit_residual_discriminator.md` updated 2026-07-14 for joint-cell decision residual (first-tail remains underlying fail).
- **Check:** `python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py -q`; collab writeup `experiments/residual-cell-R-breakthrough-collab-2026-07/FINDINGS.md`; e2e package re-run (Agy); constant-gaming sweep must not endpoint-emit on 50-bit (H2'/Claude)
- **Kill:** C1T2L1 on a known true close under fixed first-tail window; constant-only endpoint emit on 50-bit; pinch fails to separate expanded true vs false sets; e2e residual code lag with only unit path green
- **Collab charter:** `experiments/residual-cell-R-breakthrough-collab-2026-07/CHARTER.md`

---

## E. Explicit non-predictions (do not schedule as PGS forecasts)

| Non-prediction | Why |
| --- | --- |
| RSA factors recovered by PGS inference | Unresolved residual is allowed; solve is not a current prediction |
| RH proved in `PROOF.md` | Downstream reading only; source-to-spectral placement open |
| Rowland/gcd or LCM recurrences as next-prime engines | Classical encounter maps; forbidden as inference |
| Zhang-Maynard “gap ≤ 246 i.o.” as PGS theorem | Different object from UBC witness offset |
| Finite scan “validates” a universal residual law | Needs analytic closure; verified/validated implementation words need `10^18` when used |
| Fixed cutoff or Super-Signal revival | Invalidated |

---

## F. Schedule (Agy drivers  -  adopted)

Execution order this cycle. After a green run, use the **status after green** label only (no silent upgrade to theorem / verified).

### Driver 1  -  50-bit residual honesty + anti-admission (H1′, H2′, I6)

- **Commands:**
  - `python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py -q`
  - Optional package re-run under `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/` (phase1 residual honesty / RESULT.md path)
- **Pass:** Decision residual remains first-tail misalignment (or honest joint residual as pinned); no emit of false class `(32047651, 32059633)`; first-tail window not widened
- **Fail:** Endpoint class without new geometry; anti-admission regression; constant-only “close”
- **Status after green:** **measured** on fixture; D-as-law still **hypothesis**

### Driver 2  -  Generator decade ladder + contract integrity (I3, I1, I4)

- **Commands:**
  - Smoke: `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/01-generator/tests/test_prime_inference_generator.py -q`
  - Ladder: high-scale decade-window path documented in `docs/PRIME_GAP_GENERATOR.md` / `research/01-generator/output/` (256 primes/decade, `10^8`..`10^18`, 2816 primes). Do not claim program-level **verified** without an **executed** ladder in the package (`AGENTS.md`).
- **Pass:** Exact `q` on ladder surface; stream purity `{"p","q"}`; audit does not select `q`
- **Fail:** Wrong/unresolved ladder entry; classical selection in generation path; diagnostics in main stream
- **Status after green:** **measured** / **implementation** surface (enables verified *language* only when ladder is in the same evidence package)

### Driver 3  -  Constant-gaming sweep (H2′, H3′)

- **Commands:** Harness TBD under `experiments/` or rsa-v3 tests (Claude/Agy spec): grid `(C1, α)` default C1∈[10,40], α∈[0.8,2.0]; **fixed** first-tail window; no classical close
- **Pass:** No grid point yields structural endpoint emit by constant retune alone; decision residual stays honest first-tail (or documented D-form break without false endpoint)
- **Fail:** Any constant-only close
- **Status after green:** **hypothesis** hardened if sweep holds; still not a theorem

**Reject schedule:** twin/constellation campaign, Rowland engine, sieve-first generator, RH proof sprint, RSA-solve as PGS inference.

**Secondary (not drivers 1-3):** T3/T4 audit corroboration on new regimes only; optional proof-spine/Lean hygiene for UBC/PSP without status flip.

**Collab overlay (live):** residual cell R breakthrough (`H-cell`)  -  finish FINDINGS, expand fixtures, constant sweep, e2e joint residual emit. See `experiments/residual-cell-R-breakthrough-collab-2026-07/`. Does not replace drivers 1-3; sharpens driver 1.

---

## Paths cited

- `PROOF.md`
- `docs/RESULTS.md`
- `docs/PRIME_GAP_GENERATOR.md`
- `AGENTS.md` (10^18 evidence surface)
- `docs/proof-enhancements/certificates/gwr_finite_base_v1.json`
- `docs/proof-enhancements/certificates/bounded_compression_base_v1.json`
- `research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`
- `research/16-predictions/probes/super-signal-fp-signature-2026-07/`
- `experiments/constellation-vs-pgs-next-prime-2026-07/COMPARISON.md`
- `experiments/rowland-pgs-category-split-2026-07/COMPARISON.md`
- `experiments/pgs-prediction-inventory-2026-07/ADVANCE_2026-07-14.md`
- `experiments/residual-cell-R-breakthrough-collab-2026-07/CHARTER.md`
- `experiments/residual-cell-R-breakthrough-collab-2026-07/FINDINGS.md`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/RESIDUAL_TAXONOMY.md`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/gwr_carrier_closure.py`
