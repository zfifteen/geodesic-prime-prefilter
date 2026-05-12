# Zenodo Formal Proof, Phase 1 Outline

Date: 2026-05-12

## Objective

Create a publication-ready formal proof package for Zenodo without weakening
the repository's established claims.

The publication draft must preserve the full strength of the root proof. It
must also place later research in the correct proof-status layer: theorem,
finite certificate, measured surface, audit result, invalidated rule, or
unresolved theorem target.

The Zenodo proof must be entirely self-contained. Repository files, scripts,
and output artifacts can guide drafting, but the deposited proof cannot require
the reader to open any external artifact to understand the definitions, theorem
statements, proof, finite certificates, measured surfaces, invalidated routes,
or unresolved boundaries. External links are provenance only.

Grok must be included as a collaborator at every stage. Each stage requires a
second-opinion pass with the big-picture frame and the narrow technical question
for that stage. If the second-opinion MCP call fails, the failure must be
reported plainly and no Grok review may be claimed.

## Source Hierarchy

1. `PROOF.md` controls theorem status for the direct deterministic next-prime
   theorem and the prime-gap maximizer theorem.
2. `RESULTS.md` and `docs/current_headline_results.md` summarize current
   public status, tested surfaces, generator status, and current limits.
3. `research/00-index/continuity/START_HERE.md` preserves current research
   branch status and must be used to avoid stale theorem claims.
4. Chapter-local README files control chapter status for bounded compression,
   state-budget, cryptology/RSA, gap-ridge, and related branches.
5. Output JSON/CSV artifacts provide exact numeric evidence for finite
   certificates and measured surfaces.

No claim may be downgraded from `proved` to `measured` when `PROOF.md` proves
it. No measured result may be promoted to theorem status without a proof
artifact.

For the Zenodo artifact, source hierarchy controls drafting, not reader
dependency. The final proof must inline every definition, lemma, table, and
status distinction needed for review.

## Status Labels

- `proved`: a universal theorem under stated hypotheses.
- `finite certificate`: an exhaustive finite verification or finite
  branch-elimination theorem with stated bounds.
- `measured`: a reproducible tested surface with exact regime limits.
- `audit`: an implementation or recovery validation surface.
- `invalidated`: a rule or route explicitly falsified by repo evidence.
- `unresolved`: a theorem target or mechanism not yet closed.

## Proof-Impact Audit

| Claim or result | Current status | Source artifact | Zenodo placement |
| --- | --- | --- | --- |
| Exact divisor-count next-prime rule: given known prime `p`, the first later integer with `tau(n) = 2` is the next prime `q`. | proved | `PROOF.md`, "Headline Theorem" and "Why The Algorithm Returns The Next Prime" | Main theorem body |
| Prime-gap maximizer theorem: in a nonempty prime-gap interior, the leftmost integer with minimum divisor count uniquely maximizes `F(n) = (1 - tau(n)/2) log n`. | proved | `PROOF.md`, "Interior Maximizer Theorem" through "Conclusion" | Main theorem body |
| Finite base for maximizer proof: `2 <= p < 5,000,000,001`, `220,336,055` gaps, `826,172,978` earlier integers, `0` failures. | finite certificate | `PROOF.md`, "Finite Base Lemma" and "Audit Tables" | Main proof certification section |
| Stress sample near `10^12`: `137,771` gaps, `649,769` earlier integers, `0` unresolved cases. | measured certification | `PROOF.md`, "Audit Tables" | Certification appendix |
| Finite bounded-compression base below `ceil(exp(16)) = 8,886,111`: `542,081` nonempty interiors, max selected-witness offset `60`. | finite certificate | `PROOF.md`, "Finite Bounded-Compression Base" | Separate finite lemma after main theorems |
| Residual `K = 128` first-d4 branch-elimination lemma for retained odd adjacent residual branches. | finite branch-elimination theorem | `PROOF.md`, "Residual K=128 First-d4 Branch-Elimination Lemma" | Separate finite/residual theorem section |
| Square-branch characterization: selected prime-square witness iff `s^2 < P(r^2) < r^2`. | proved reduction/characterization | `PROOF.md`, "Square-Branch Reduction"; `START_HERE.md` bounded-compression status | Bounded-compression status section |
| All-scale bounded dynamic cutoff `C(q) = max(64, ceil(0.5 * log(q)^2))`. | unresolved as universal theorem | `PROOF.md`, "Square-Branch Reduction"; `research/04-bounded-compression/README.md`; `research/04-bounded-compression/docs/session_handoff_2026-05-09.md` | State explicitly as unresolved, not as a theorem |
| Exact bounded-compression compare scan through `q <= 10,000,000`: `664,575` gaps, first counterexample `None`, max exact peak offset `60`, max cutoff utilization `0.6153846153846154`. | measured finite surface | `research/04-bounded-compression/output/gwr_dni_cutoff_counterexample_scan_summary.json` | Bounded-compression evidence appendix |
| Square dynamic-cutoff search over odd prime-square roots `3 <= r <= 100,000,000`: `5,761,454` roots, first counterexample `None`, max utilization `0.8120300751879699`. | measured finite surface | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8/square_branch_dynamic_cutoff_search_summary.json` | Bounded-compression evidence appendix |
| Square dynamic-cutoff search over roots `100,000,001 <= r <= 200,000,000`: `5,317,482` roots, first counterexample `None`, max utilization `0.6784140969162996`. | measured finite surface | `research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8_2e8/square_branch_dynamic_cutoff_search_summary.json` | Bounded-compression evidence appendix |
| Old fixed cutoff map `{2:44, 4:60, 6:60}`. | invalidated | `RESULTS.md`; `research/04-bounded-compression/README.md`; failure at `q = 24,098,209` | Invalidated-routes section |
| Literal prior-square Lemma A. | invalidated | `research/04-bounded-compression/README.md`; failure at `q = 113` | Invalidated-routes section |
| Production generator surface `11..100000`: `9588 / 9588` exact outputs, `0` failures. | audit/implementation status | `RESULTS.md`; `research/01-generator/README.md` | Implementation evidence appendix |
| Production generator surface `11..1000000`: `78494 / 78494` outputted, `0` unresolved, `0` audit failures. | audit/implementation status | `docs/releases/pgs_inference_generator_v1_0.md`; `docs/releases/pgs_inference_generator_v1_1_pgs_only.md`; `docs/executive_summary_pgs_prime_generator.md` | Implementation evidence appendix |
| High-scale generator decade-window surface `10^8` through `10^18`: `2816 / 2816` exact outputs, `0` incorrect candidates. | audit/implementation status | `RESULTS.md`; `PRIME_GAP_GENERATOR.md`; `research/01-generator/README.md` | Implementation evidence appendix |
| Recursive walk: transition rule exact on `743,075 / 743,075` rows from combined `10^6 + 10^7`; recursive walk `664,578 / 664,578` exact consecutive next-prime recoveries from `11` through `10,000,121`, `0` skipped gaps; sampled decade ladder `10^2` through `10^18` hit rate `1.0` across `860` steps. | measured/audit surface; exact corollary for no-later-simpler-composite | `RESULTS.md`; `docs/current_headline_results.md`; `research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md` | Implementation and corollary evidence appendix |
| `d4_count` ordering carrier on deterministic retained `8192`-row-per-power `10^12..10^18` surface: `mod30_prev_gap_exact`, `7881` decisive pairs, `6 / 7` positive folds, signed advantage `299`, tail control `230`, edge `69`, required edge `50`, verdict `ordering_carrier_found`. | measured | `START_HERE.md`; `research/05-state-budget/README.md`; `research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json` | Later research appendix, not theorem body |
| Symbolic reason for `d4_count` carrier and disjoint high-window replication. | unresolved | `START_HERE.md`; `research/05-state-budget/README.md` | Open research appendix |
| Semiprime branch `127`-bit official gate: `12` cases, rung `2`, top-1 and top-4 routed-window recall `1.0`, exact recovery recall `0.75`, archived case recovered. | audit result | `docs/current_headline_results.md`; `research/06-cryptology-rsa/docs/semiprime_branch/pgs_127_official_gate_breakthrough.md`; `research/06-cryptology-rsa/output/semiprime_branch/pgs_127_official_audit_summary.json` | Supporting research appendix, not proof body |
| Blind factorization, generic all-regime semiprime recovery theorem, RSA-4096 break. | not claimed / unresolved | `research/06-cryptology-rsa/docs/semiprime_branch/pgs_127_official_gate_breakthrough.md` | Explicit non-claim boundary |

## Proposed Zenodo Proof Structure

### 1. Abstract

State the two universal proved theorems directly:

- exact divisor-count next-prime theorem;
- prime-gap interior maximizer theorem.

Mention that finite certificates and high-scale implementation/audit surfaces
are included for reproducibility and provenance, not as theorem limits.

### 2. Definitions And Objects

Introduce:

- known prime `p`;
- successor prime `q`;
- divisor count `tau(n)`;
- gap interior `I = {p + 1, ..., q - 1}`;
- leftmost minimum-divisor witness `w`;
- comparison function `F(n) = (1 - tau(n)/2) log n`.

### 3. Theorem 1: Direct Deterministic Next-Prime Rule

State:

```text
q = min { n > p : tau(n) = 2 }.
```

Prove from the exact characterization of primes by divisor count.

### 4. Theorem 2: Interior Maximizer

State the leftmost minimum-divisor theorem exactly as in `PROOF.md`.

Prove by:

- ordered comparison lemma for later integers;
- right-side divisor-count tail closure;
- earlier-integer comparison;
- prime-square case;
- threshold lemma;
- finite base lemma;
- witness threshold lemma;
- odd adjacent branch lemma;
- classification lemma.

### 5. Finite Certificates Used In The Proof

Include the maximizer finite base table:

```text
220,336,055 prime gaps
826,172,978 earlier integers
0 failures
```

Also include the `10^12` stress sample from `PROOF.md` as certification and
provenance.

### 6. Boundary Of The Main Theorems

State that the direct next-prime theorem and the interior maximizer theorem do
not depend on the bounded dynamic cutoff program, generator implementation
surfaces, state-budget carrier evidence, or semiprime/RSA audits.

### 7. Appendix A: Finite Certificates

Place proof-supporting finite certificates here:

- maximizer finite base table;
- `10^12` stress sample;
- finite bounded-compression base;
- residual `K = 128` first-d4 branch-elimination theorem.

### 8. Appendix B: Bounded Compression Status

Present the bounded-compression material with status separation:

- finite bounded-compression base is a finite certificate;
- residual `K = 128` first-d4 branch elimination is a finite residual theorem;
- square-branch characterization is proved;
- all-scale dynamic cutoff remains unresolved on the prime-square proximity
  theorem.

This section must not imply that the unresolved dynamic cutoff limits the two
main theorems.

### 9. Appendix C: Measured High-Scale Evidence

Include implementation and measured surfaces:

- `78494 / 78494` through `11..1000000`;
- `2816 / 2816` on `10^8` through `10^18`;
- recursive walk exact surfaces and `10^18` sampled ladder;
- bounded-compression compare scans and square-branch searches.

Each item must state its exact tested regime.

### 10. Appendix D: Later Research

Include only after theorem proof and certification:

- `d4_count` state-budget carrier as measured on the retained
  `10^12..10^18` surface;
- semiprime/RSA `127`-bit official gate as an audit result;
- gap-ridge and lexicographic revalidation as theorem-adjacent evidence where
  it directly certifies the same leftmost-minimum object.

This appendix must not be needed for the main proof.

### 11. Appendix E: Invalidated Routes And Non-Claims

List invalidated or excluded routes:

- fixed cutoff map `{2:44, 4:60, 6:60}`;
- literal prior-square Lemma A;
- dynamic cutoff as a finished universal theorem;
- state-budget carrier as a proved symbolic law;
- semiprime audit as blind factorization or RSA-4096 break.

### 12. Appendix F: Reproducibility

Include enough reproducibility detail inside the proof to identify the
computation contracts and expected outputs. External paths can be listed only
as provenance:

- proof source: `PROOF.md`;
- results map: `RESULTS.md`;
- bounded-compression scripts/tests;
- state-budget scripts/tests;
- generator validation artifacts;
- Zenodo metadata inventory:
  `research/00-index/docs/zenodo_existing_uploads_2026-05-12.md`.

## Drafting Rules For Phase 2

1. Lead with proved theorem statements.
2. Do not describe proved results as empirical, heuristic, approximate, or
   validated only by finite testing.
3. Use finite testing language only for finite certificates, measured surfaces,
   audit status, or implementation validation.
4. Keep all-scale bounded compression separate from the proved next-prime and
   maximizer theorems.
5. State invalidated routes plainly so reviewers do not confuse them with live
   claims.
6. Preserve PGS-native framing before classical comparisons.
7. Treat `PROOF.md` as the root theorem source unless the user explicitly
   promotes a newer proof artifact.
8. Make the draft self-contained: no external file may be logically required to
   validate the proof's claims.
9. Include Grok review state for each stage in a short collaboration note:
   orientation acknowledged, technical judgment received, material
   disagreements if any.

## Phase 2 Input Decision

Recommended draft strategy:

```text
Use PROOF.md as the controlling proof text.
Create a new Zenodo-facing proof document from it.
Do not copy verbatim blindly.
Do not narrow or weaken the theorem claims.
Reorganize only to improve reviewability, citation structure, and status
separation.
Inline the full proof and the needed certificate tables.
```

The new document should be a formal publication version of the existing proof,
not a replacement proof with weaker claims.
