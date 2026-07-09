# Zero-Excess DNI Change Scope

This document consolidates the four-agent repo analysis for the
Zero-Excess DNI migration.

The migration target is definite:

```text
Make Zero-Excess DNI the preferred explanatory coordinate for live PGS docs,
while preserving existing Z-Band APIs, vectors, benchmark schemas, and
historical artifacts unless a later compatibility decision explicitly changes
them.
```

## Executive Scope

The change is an exact coordinate reformulation, not a new theorem.

Current coordinate:

$$
Z(n)=n^{1-\tau(n)/2}.
$$

New preferred coordinate:

$$
E(n)=-\log Z(n)
=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`,

$$
E(n)=0 \iff \tau(n)=2 \iff n \text{ is prime},
$$

and every composite has

$$
E(n)>0.
$$

The local theorem score in `PROOF.md` is

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n,
$$

so

$$
F(n)=-E(n).
$$

The old "log-score maximizer" language and the new "minimum-excess selected
integer" language describe the same selected integer when applied to the same
prime-gap interior.

## Non-Negotiable Guardrails

- `PROOF.md` controls the local theorem status.
- Do not imply a new theorem.
- Do not claim `PROOF.md` itself proves RH.
- Preserve the condition `n > 1` whenever saying `E(n)=0` characterizes
  primes, because `E(1)=0` by `log(1)=0`.
- Do not identify the zero-excess floor with the analytic critical line.
- Do not say RH places primes close to the zero-excess floor.
- Do not replace the DNI-to-zeta numerator with `E(n)` alone.
- Do not rename or break `Z-Band`, `proxy_z`, `FIXED_POINT_V`,
  `exact_z_normalize`, committed vectors, or benchmark schemas in the first
  migration pass.
- Do not bulk-edit historical JSON, CSV, PDF, SVG, PNG, MP3, MP4, or archived
  generated outputs.

## Bridge Formula That Controls The RH Surface

The exact DNI-to-zeta bridge currently uses

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}
$$

and

$$
v=\frac{e^2}{2}.
$$

The scaled bridge load is

$$
v\kappa(n)=\frac{\tau(n)\log n}{2}.
$$

In zero-excess language:

$$
\frac{\tau(n)\log n}{2}=\log n+E(n).
$$

Define

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Then

$$
H(s)=\sum_{n\ge1}\frac{H(n)}{n^s}
=-\frac{1}{2}D'(s),
$$

where

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The continued ratio remains

$$
R(s)=\frac{H(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

So the RH-facing docs must say:

```text
zero-excess floor: integer-side, arithmetic, exact, local
critical line: zeta-side, analytic, compressed, global
bridge load: log n + zero excess, not zero excess alone
```

## Repo-Wide Inventory Result

A local scan found `172` Markdown/Python/C/spec files with live hits for
`DNI`, `Z(n)`, `Z = 1.0`, `raw-Z`, `fixed-point locus`, `log-score`,
`proxy_z`, `FIXED_POINT_V`, `exact_z_normalize`, or related patterns.

The migration is therefore not a blanket rename. It has four different
statuses:

- **live migration**: current explanatory docs and live code should move to the
  zero-excess coordinate;
- **dual-coordinate crosswalk**: legacy/public APIs keep their names but gain
  an explanatory mapping `Z=1.0 <-> E=0`;
- **compatibility hold**: tests, vectors, and schemas keep old fields until a
  schema migration is explicitly approved;
- **historical artifact**: archived generated outputs keep old terminology.

## Definite Live-Migration Scope

### Core Root Docs

These are first-pass migration files:

- `docs/core/DIVISOR_NORMALIZATION_IDENTITY.md`
- `README.md`
- `RESULTS.md`
- `PROOF.md`
- `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`
- `docs/core/RECURSIVE_PRIME_WALK.md`
- `docs/PRIME_GAP_GENERATOR.md`
- `docs/specs/prime-gen/tech_spec_pgs_prime_generator.md`

Required changes:

- make `E(n)` the preferred explanatory coordinate;
- keep `Z(n)=e^{-E(n)}` as the dual coordinate;
- translate "primes at `Z=1.0`" to "primes at the zero-excess floor";
- translate "composites below `1.0`" to "composites have positive excess";
- translate "log-score maximizer" to "minimum-excess selected integer";
- preserve theorem status and formulas in `PROOF.md`;
- add `F(n)=-E(n)` where it clarifies the old proof notation.

### RH Bundle

These files need coordinated updates:

- `docs/rh/README.md`
- `docs/rh/source-order.md`
- `docs/rh/dni-to-zeta-compression.md`
- `docs/rh/pole-placement.md`
- `docs/rh/critical-line-and-zero-geometry.md`
- `docs/rh/off-critical-pole-exclusion.md`
- `docs/rh/status-ledger.md`
- `docs/rh/reviewer-map.md`
- `docs/rh/explicit-formula-bridge.md`

Required changes:

- insert the zero-excess floor as the integer-side source coordinate;
- update local theorem language from `F` maximizer to `E` minimizer where
  helpful;
- add the `H(n)=log n+E(n)` bridge-load relation in the compression page;
- state that the zero-excess floor is not the critical line;
- keep `D(s)`, `K(s)`, `R(s)`, and
  `R(s)=-zeta'(s)/zeta(s)` intact;
- keep off-critical-pole residual closure language intact except where excess
  should be named as source-side coordinate.

### FAQ

Live FAQ pages to migrate or add:

- `docs/faq/README.md`
- `docs/faq/core-frame/source-object.md`
- `docs/faq/core-frame/rh-downstream.md`
- `docs/faq/core-frame/zeta-compression.md`
- `docs/faq/exact-arithmetic/divisor-counts.md`
- `docs/faq/exact-arithmetic/deterministic-not-statistical.md`
- `docs/faq/exact-arithmetic/next-prime-placement.md`
- `docs/faq/exact-arithmetic/ordered-gap-interiors.md`
- `docs/faq/zeta-compression/divisor-series.md`
- `docs/faq/zeta-compression/dni-ratio.md`
- `docs/faq/zeta-compression/no-private-arithmetic-supply.md`
- `docs/faq/category-errors/not-a-reformulation.md`
- `docs/faq/category-errors/analytical-proof-expectation.md`
- `docs/faq/category-errors/pole-placement-is-not-first.md`
- `docs/faq/reviewer-guidance/status-ledger.md`
- `docs/faq/reviewer-guidance/evaluation-order.md`
- `docs/faq/reviewer-guidance/real-objections.md`

Likely new FAQ page:

```text
docs/faq/category-errors/zero-excess-floor-vs-critical-line.md
```

Purpose:

```text
Analogy: yes.
Identification: no.
Source-to-compression relation: yes.
```

### Vocabulary And Essays

Live or public-facing surfaces:

- `docs/vocabulary/nonstandard_terms_dictionary.md`
- `docs/current_headline_results.md`
- `docs/essays/01_genesis_of_dni.md`
- `docs/essays/the-riemann-hypothesis-is-obsolete.md`
- `docs/essays/primality-checks-are-overrated.md`
- `docs/essays/GWR_glossary.md`
- `docs/essays/README.md`
- `docs/essays/substack/series/essay-1-the-observation.md`

Binary document:

- `docs/essays/divisor_minimality_essay.docx`

Scope decision:

```text
Do not silently edit the DOCX binary. Either leave it historical or regenerate
from an accepted source path in a separate document-artifact pass.
```

## Research Corpus Scope

### Live Research Docs To Migrate

Primary research live docs:

- `research/02-gwr-dni/README.md`
- `research/02-gwr-dni/docs/gwr-root-readme.md`
- `research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md`
- `research/02-gwr-dni/docs/open_llm_session_synthesis.md`
- `research/02-gwr-dni/docs/pnt_gwr_prime_formula_paper.md`
- `research/02-gwr-dni/docs/closure_constraint_findings.md`
- `research/02-gwr-dni/docs/dominant_d4_arrival_reduction_findings.md`
- `research/02-gwr-dni/docs/why_the_dominant_d4_reduction_matters.md`
- `research/02-gwr-dni/docs/gap_anatomy_decomposition.md`

RH bridge research (classical completion material, archived externally May 2026 due to drift/steering concerns):

- See external archive: `/Users/velocityworks/prime-gap-structure-archives/2026-05-classical-rh-bridge-completion-route/12-rh-bridge/`
- Live pointer inside repo: `research/12-rh-bridge/README.md` + ARCHIVAL_HANDOFF.md in the external archive.

Continuity and index surfaces:

- `research/00-index/continuity/START_HERE.md`
- `research/00-index/status-map.md`
- `research/00-index/README.md`

Status-map label:

```text
zero-excess DNI: exact coordinate reformulation
```

### Research Docs To Crosswalk Lightly

These should receive light wording only where they are still used as live
navigation or current findings:

- `research/01-generator/docs/*`
- `research/03-gap-types/README.md`
- `research/03-gap-types/docs/gap_type_catalog_through_1e18.md`
- `research/04-bounded-compression/README.md`
- `research/04-bounded-compression/docs/current_completion_audit.md`
- `research/04-bounded-compression/docs/dynamic_cutoff_proof_skeleton.md`
- `research/04-bounded-compression/docs/square_obstruction_lemma_targets.md`
- `research/06-cryptology-rsa/docs/cryptology/pgs_cryptologic_implications_whitepaper.md`
- `research/06-cryptology-rsa/docs/semiprime_branch/d4_layer_baseline.md`
- `research/06-cryptology-rsa/docs/semiprime_branch/gwr_dni_semiprime_large_rsa_research_note.md`
- `research/09-exponents/docs/mersenne_prime_gap_type_probe_findings.md`
- `research/10-twin-primes/CERTIFICATE.md`
- `research/10-twin-primes/docs/twin_prime_gap_type_probe_findings.md`
- `research/11-gap-ridge/docs/dni_gap_ridge.md`
- `research/11-gap-ridge/docs/gap_ridge/raw_composite_z_gap_edge.md`

### Historical Or Generated Research Surfaces

Preserve unless republished:

- `research/02-gwr-dni/experiments/chatgpt/`
- `research/02-gwr-dni/experiments/chatgpt/lexicographic_rule_revalidation_results.json`
- `research/00-index/docs/zenodo-peer-review-2026-05-12/`
- generated outputs under `research/04-bounded-compression/docs/generated/`
- generated JSON/CSV outputs under `research/*/output/`
- existing `.png`, `.svg`, `.mp3`, `.mp4`, and PDF outputs unless source is
  migrated and regeneration is intentional.

## Code Scope

### Invariant Package

Files:

- `src/python/z_band_prime_invariant/core.py`
- `src/python/z_band_prime_invariant/__init__.py`

First-pass code addition:

```text
add exact_zero_excess(n)
preserve exact_z_normalize(n)
preserve FIXED_POINT_V
preserve FIXED_POINT_TOLERANCE
```

Required tests:

```text
E(n) = (tau(n)/2 - 1)log n
E(n) = -log Z(n) where Z(n) > 0
E(n) = 0 for primes n > 1
E(n) > 0 for composites
n = 1 is explicitly guarded or documented
```

### Gap Ridge And GWR/DNI Scripts

Files and packages:

- `src/python/z_band_prime_gap_ridge/runs.py`
- `src/python/z_band_prime_gap_ridge/__init__.py`
- `research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py`
- `research/02-gwr-dni/scripts/gwr_dni_transition_probe.py`
- `research/02-gwr-dni/scripts/gwr_dni_direct_rule_probe.py`
- `research/02-gwr-dni/scripts/gwr_dni_recursive_gap_scaling_sweep.py`
- `research/02-gwr-dni/scripts/plot_gwr_dni_recursive_gap_scaling_sweep.py`
- `research/02-gwr-dni/scripts/proof/no_early_spoiler_margin_scan.py`
- `research/02-gwr-dni/scripts/proof/parallel_no_early_spoiler_scan.py`
- `research/02-gwr-dni/scripts/proof/prime_gap_admissibility_frontier.py`
- `research/02-gwr-dni/scripts/proof/residual_odd_winner_branch_scan.py`
- `research/02-gwr-dni/experiments/chatgpt/lexi_validation_runs.py`

Current terms:

- `raw-Z`
- `log-score`
- `score_strictly_greater`
- `log_score_margin`
- `min_log_score_margin`
- `next_peak_offset`
- `current_peak_offset`
- `best_n_z`
- `best_d_z`

Migration decision:

```text
Rename or alias schema fields only after compatibility tests are in place.
For phase 1, docs can say old peak/score fields are dual-coordinate names.
```

Equivalence tests:

```text
old raw-Z argmax = new zero-excess argmin
old log_score_margin = new excess_margin
old next_peak_offset = new minimum-excess selected offset
```

### RH Bridge Code

File:

- `src/python/z_band_prime_rh_bridge/bridge.py`

Decision:

```text
Do not replace normalization_load_coefficients_up_to with E(n).
The bridge depends on kappa(n)=tau(n)log(n)/e^2.
Add a separate helper or test for H(n)=log n+E(n) only if useful.
```

### Legacy Prefilter and Generator Scaffolding Paths (z_band_prime_predictor: historical only; see chapter 15 documentation-correction and 06-cryptology-rsa legacy prefilter boundary)

Files:

- `src/python/z_band_prime_predictor/simple_pgs_generator.py`
- `src/python/z_band_prime_predictor/gwr_boundary_walk.py`
- `src/python/z_band_prime_predictor/gpe_boundary_selector.py`
- `src/python/z_band_prime_predictor/gpe_nlsc_selector.py`
- `src/python/z_band_prime_composite_field/field.py`

Decision:

```text
No first-pass logic change. These are divisor-count or generator paths.
The production generator output remains exactly {"p": ..., "q": ...}.
```

## Legacy Prefilter And Compatibility Scope

### Must Preserve

Public package and API:

- `src/python/pyproject.toml`
- `src/python/z_band_prime_prefilter/__init__.py`
- `src/python/z_band_prime_prefilter/prefilter.py`
- `src/python/z_band_prime_invariant/core.py`
- `spec/contract.md`
- `spec/vectors/fixed_points_small_n.json`
- `spec/vectors/prefilter_decisions_32.json`
- `tests/python/prefilter/test_prefilter.py`
- `tests/python/prefilter/test_vectors.py`

Names and fields to preserve:

- `z-band-prime-prefilter`
- `Z-Band`
- `CDLPrimeZBandPrefilter`
- `proxy_z`
- `z_hat`
- `fixed_point_v`
- `z_at_fixed_point`
- `FIXED_POINT_V`
- `FIXED_POINT_TOLERANCE`
- `exact_z_normalize`
- `is_prime_candidate`
- `is_probable_prime`

First-pass action:

```text
Add crosswalk docs. Do not break or rename.
```

Crosswalk sentence:

```text
Under exact divisor counting, Z=1.0 corresponds to E=0. In the legacy
prefilter, proxy_z=1.0 remains a survivor convention, not a primality proof.
```

### Legacy Docs To Crosswalk

- `research/06-cryptology-rsa/legacy-prefilter/docs/LEGACY_PREFILTER.md`
- `research/06-cryptology-rsa/legacy-prefilter/docs/dni_prefilter.md`
- `research/06-cryptology-rsa/legacy-prefilter/docs/benchmarks.md`
- `research/06-cryptology-rsa/legacy-prefilter/docs/manual_validation.md`
- `research/06-cryptology-rsa/legacy-prefilter/technical-note/technical_note.md`
- `research/06-cryptology-rsa/legacy-prefilter/scripts/candidate_benchmark.py`
- `research/06-cryptology-rsa/legacy-prefilter/scripts/rsa_keygen_benchmark.py`
- `research/06-cryptology-rsa/legacy-prefilter/scripts/rsa_sweep_benchmark.py`

Stale doc fix discovered during analysis:

```text
research/06-cryptology-rsa/legacy-prefilter/docs/manual_validation.md
references tests/python/test_vectors.py, but the live file is
tests/python/prefilter/test_vectors.py.
```

### Legacy Artifacts To Preserve

- `research/06-cryptology-rsa/legacy-prefilter/output/prefilter/BENCHMARK_REPORT.md`
- `research/06-cryptology-rsa/legacy-prefilter/technical-note/export/z-band-prime-prefilter-technical-note.pdf`
- Bouncy Castle reports and JSON under
  `research/06-cryptology-rsa/legacy-prefilter/tests/bouncycastle-keygen-baseline/results/`
- `spec/vectors/*.json` until a schema migration is explicitly approved.

## C And High-Scale Scope

Files:

- `src/c/high-scale-pgs/src/pgs_chamber.c`
- `src/c/high-scale-pgs/src/pgs_emit.c`
- `src/c/high-scale-pgs/src/pgs_diagnostics.c`
- `src/c/high-scale-pgs/include/pgs_high_scale.h`
- `src/c/high-scale-pgs/Makefile`

Decision:

```text
Low code impact. The high-scale path is divisor-count and chamber based, not
raw-Z based. Do not change minimal C output. If zero-excess diagnostics are
added later, keep them sidecar-only.
```

Verification if touched:

```text
make -C src/c/high-scale-pgs test
```

## Generated And Visual Assets

Live-facing source assets to consider:

- `pgs-math-explainer/index.html`
- `pgs-math-explainer/narration.txt`
- `pgs-math-explainer/scene-narration.json`
- `research/02-gwr-dni/story/story/README.md`
- `research/02-gwr-dni/story/story/plot_gwr_story.py`
- `research/02-gwr-dni/story/story/storyboards/gwr_explainer_plan.json`
- `research/02-gwr-dni/story/story/storyboards/gwr_explainer_storyboard.md`
- `research/02-gwr-dni/story/story/storyboards/gwr_explainer_storyboard_sheet.svg`

Generated assets:

- existing PNGs in `research/02-gwr-dni/story/story/plots/`
- existing media in `pgs-math-explainer/`
- existing x-post image assets

Decision:

```text
Update source labels first. Regenerate only when the visual surface is still
public-facing. Leave historical images and media intact until regeneration is
intentional.
```

## Symbol Collision

The symbol `E(q)` already appears as a bounded-compression offset/cutoff
quantity, for example:

- `RESULTS.md`
- `docs/core/RECURSIVE_PRIME_WALK.md`
- `research/04-bounded-compression/README.md`
- `research/00-index/docs/zenodo-peer-review-2026-05-12/proof.md`
- `pgs-math-explainer/index.html`
- `research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py`

Decision needed before global use of `E(n)`:

```text
Either rename the bounded-compression E(q) notation, or explicitly reserve
E(n) for zero-excess and relabel the cutoff/offset quantity.
```

Preferred direction:

```text
Use E(n) for zero-excess.
Rename bounded-compression E(q) to an offset-specific symbol in live docs.
Leave historical artifacts unchanged.
```

## Implementation Phases

### Phase 1: Canonical Docs And Status

1. Rewrite `docs/core/DIVISOR_NORMALIZATION_IDENTITY.md`.
2. Update `README.md`, `RESULTS.md`, `docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md`, and
   `docs/core/RECURSIVE_PRIME_WALK.md`.
3. Add the `F(n)=-E(n)` reading to `PROOF.md` without changing theorem claims.
4. Resolve live `E(q)` notation collisions or reserve them for later with a
   visible note.
5. Update vocabulary with `Zero-Excess DNI` and `zero-excess floor`.

### Phase 2: RH And FAQ

1. Update `docs/rh` with zero-excess source coordinate.
2. Add `H(n)=log n+E(n)` to `docs/rh/dni-to-zeta-compression.md`.
3. Add or update FAQ category-error guidance for zero-excess floor versus
   critical line.
4. Update FAQ status ledger with `exact coordinate reformulation`.

### Phase 3: Research Navigation And Live Notes

1. Update `research/02-gwr-dni` live docs.
2. Update `research/12-rh-bridge` workbench docs.
3. Update `research/00-index/continuity/START_HERE.md` and
   `research/00-index/status-map.md`.
4. Add crosswalks to cryptology and semiprime live docs.

### Phase 4: Code Support Without Schema Break

1. Add `exact_zero_excess(n)` to the invariant package.
2. Add tests for `E(n)=-log Z(n)` and prime/composite behavior.
3. Add optional helper/tests for `H(n)=log n+E(n)` if used by RH bridge docs.
4. Preserve prefilter APIs and vectors.

### Phase 5: Script And Schema Migration

1. Migrate raw-Z/log-score presentation in gap-ridge scripts.
2. Alias or rename `peak`/`best_n_z`/`log_score_margin` fields with tests.
3. Update generated schemas only after compatibility decisions.
4. Regenerate public plots after labels stabilize.

### Phase 6: Legacy Crosswalk And Public Artifacts

1. Add Z-Band crosswalks in legacy prefilter docs.
2. Leave historical benchmark reports and PDFs intact.
3. Regenerate visual/media artifacts only from source.

## Verification Plan

### Documentation Scans

Old-coordinate scan:

```bash
rg -n "Z\\(n\\)|Z\\(p\\)|Z = 1|Z=1|fixed-point|fixed point|fixed-point locus|prime baseline|below 1|raw-Z|log-score|log score|DNI ratio|E\\(q\\)" \
  README.md RESULTS.md PROOF.md docs/core/DIVISOR_NORMALIZATION_IDENTITY.md \
  docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md docs/core/RECURSIVE_PRIME_WALK.md \
  docs research pgs-math-explainer spec
```

New-coordinate coverage scan:

```bash
rg -n "zero-excess|minimum-excess|zero-excess floor|E\\(n\\)|H\\(n\\)" \
  README.md RESULTS.md PROOF.md docs/core/DIVISOR_NORMALIZATION_IDENTITY.md \
  docs/core/LEFTMOST_MINIMUM_DIVISOR_RULE.md docs/core/RECURSIVE_PRIME_WALK.md docs research
```

Whitespace:

```bash
git diff --check
```

### Tests For Doc-Only Phases

```bash
python3 -m pytest tests/python/test_doc_proof_status_surface.py
# RH bridge tests archived externally: see research/12-rh-bridge/README.md and external archive
```

### Tests If Invariant Package Changes

```bash
python3 -m pip install -e ./src/python
python3 -m pytest tests/python/prefilter -q
```

### Tests If GWR/DNI Scripts Change

```bash
python3 -m pytest research/02-gwr-dni/tests
python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py \
  research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py
```

### Tests If Legacy Prefilter Changes

```bash
python3 -m pytest research/06-cryptology-rsa/legacy-prefilter/tests -q
```

### Tests If C High-Scale Changes

```bash
make -C src/c/high-scale-pgs test
```

## Open Decisions

- Canonical code function name: `exact_zero_excess`, `zero_excess`, or
  `exact_excess`.
- Whether the bounded-compression `E(q)` notation is renamed before or during
  Phase 1.
- Whether live output schemas keep old names as aliases or migrate to
  `minimum_excess_*` names.
- Whether `spec/vectors/*.json` get zero-excess aliases or remain pure legacy
  Z-Band vectors.
- Whether the prefilter gets a new optional zero-excess report column.
- Whether the DOCX essay is left historical or regenerated.
- Whether `docs/zero-excess-dni/README.md` remains a planning doc or becomes a
  standing migration index after implementation starts.

## Agent Findings Used

- Agent 1: public docs, `docs/rh`, FAQ, essays, vocabulary.
- Agent 2: research corpus, generated assets, continuity/status surfaces.
- Agent 3: runtime code, Python packages, tests, output schemas.
- Agent 4: legacy prefilter, compatibility surfaces, C/high-scale generator.

Combined decision:

```text
Proceed as a phased migration. Do not start with a schema-breaking rename.
Make the source-side explanation zero-excess first, then add code helpers and
compatibility tests, then decide whether output schemas should migrate.
```
