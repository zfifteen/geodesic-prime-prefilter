# PGS Research Corpus Status Map

This file tracks the repository reorganization state. It records migration
status only. It does not upgrade measured results to proof results.

## Phase 1 Skeleton

Status: complete.

Created chapter homes:

- `research/01-generator/`
- `research/02-gwr-dni/`
- `research/03-gap-types/`
- `research/04-bounded-compression/`
- `research/05-state-budget/`
- `research/06-cryptology-rsa/`
- `research/07-oeis/`
- `research/08-collatz/`
- `research/09-exponents/`
- `research/10-twin-primes/`
- `research/11-gap-ridge/`
- `research/12-rh-bridge/`
- `research/13-prime-spiral/`
- `research/14-sha-nonce/`
- `research/15-documentation-correction/`

## Current Center Of Gravity

**Note (2026-05):** The previous "active project center" (`research/12-rh-bridge/`, the DNI/PGS Prime-Structure Program / classical completion assembly route) has been archived.

See `research/archive/2026-05-classical-rh-bridge-completion-route/ARCHIVAL_HANDOFF.md` for the full record of the decision and preserved results.

The archival was performed because the volume and routing language of the classical analytic strategy material created persistent steering (prompt injection) away from direct work on local PGS objects and invariants.

### Retained Direction

Active focus has returned to local PGS-native objects that have not yet received sustained large-scale pressure using PGS methods:

- Chain-horizon closure and PGS-visible divisor-horizon laws
- Endpoint-chain traversal and modulus-link closure (floor transport + reciprocal conditions)
- Chamber reset mechanics, endpoint determinacy, boundary-drop behavior, and related local geometry

These are the objects aligned with the program's historical source of durable progress.

Primary documentation-correction artifact remains:

```text
research/15-documentation-correction/index.html
```

(The documentation-correction project audits and repairs wording that makes RH, PNT, zeta, statistics, or audit language appear upstream of PGS source structure.)

## Phase 2 Contained Families

Status: complete.

Moved and validated:

- `research/08-collatz/`
- `research/09-exponents/`
- `research/10-twin-primes/`

## Phase 3 GWR And Generator Surfaces

Status: complete.

Production implementation code remained in place. The chapter homes now route
generator evidence and GWR/DNI evidence without moving `src/`, `tests/`, or
`benchmarks/`.

## Phase 4 Bounded Compression And State Budget

Status: complete.

The chapter homes now preserve the dynamic-cutoff unresolved state, the fixed
cutoff invalidation, the square-branch blocker, and the measured `d4_count`
state-budget carrier without upgrading measured evidence to proof.

## Phase 5 Cryptology And RSA

Status: complete.

The chapter home now routes RSA v2/v3, semiprime, modulus-link, reciprocal
closure, and structural-certificate surfaces while preserving unresolved
survivor/blocker status.

## Phase 6 OEIS

Status: complete.

The OEIS chapter now has a candidate workflow and packet template. No candidate
sequence has been selected in this branch.

## Phase 7 PGS-Shor Order Entropy Topic

Status: topic added.

The cryptology chapter now includes a PGS-Shor order entropy topic page at
`research/06-cryptology-rsa/docs/shor_order_entropy/index.html`. It records the
measured sidecar finding that the resolved 40-bit RSA v2 ladder rung collapses
from `80` baseline phase bits to `0` residual phase bits after public PGS
reciprocal endpoint closure, while the unresolved 50-bit rung remains at
`100` residual phase bits.

## Phase 8 Documentation Correction

Status: active.

The documentation-correction chapter lives at:

```text
research/15-documentation-correction/
```

Its first artifact is the correction audit:

```text
research/15-documentation-correction/index.html
```

The track exists to keep the repository language aligned with the PGS-first
order:

```text
divisor counts -> DNI/GWR prime placement -> zeta compression -> RH language
```

## Phase 9 Chapters 11-15 Routing

Status: mapped, with explicit validation state.

Chapters 11 through 15 are now routed in the corpus map. A chapter marked
`not-yet-gated` has a home and a status description, but no status-map
validation gate has been recorded for that chapter in this file.

The C high-scale implementation has its own validation entrypoint:

```text
make -C src/c/high-scale-pgs test
```

That command builds and runs the Apple Silicon GMP/MPFR C high-scale tests. It
confirms the C implementation surface; it does not change theorem status.

## Migration Status

| Chapter | Status | Validation | Next Action |
| --- | --- | --- | --- |
| `01-generator` | mapped | `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py` passed, 36 tests | Production code remains in place. |
| `02-gwr-dni` | mapped | `python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py` passed, 36 tests | GWR/DNI evidence routed. |
| `03-gap-types` | mapped | `python3 -m pytest research/03-gap-types/tests/test_gwr_dni_gap_type_catalog.py research/03-gap-types/tests/test_gwr_dni_gap_type_sequence_probe.py research/03-gap-types/tests/test_gwr_dni_gap_type_engine_synthesis.py` passed, 9 tests | Gap-type model remains measured. |
| `04-bounded-compression` | mapped | Bounded/state focused command passed, 20 tests | Square branch remains unresolved. |
| `05-state-budget` | mapped | Bounded/state focused command passed, 20 tests | `d4_count` remains measured. |
| `06-cryptology-rsa` | mapped | Focused RSA command passed, 102 tests | RSA v2 unresolved states preserved. |
| `06-cryptology-rsa/docs/shor_order_entropy` | topic added | `python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py -q` passed, 51 tests | Add 17-bit toy row and next higher rung without changing the rule. |
| `07-oeis` | workflow initialized | template audit passed by file presence | First candidate packet remains open. |
| `08-collatz` | migrated | `python3 -m pytest research/08-collatz/tests` passed, 55 tests | Contained-family migration complete. |
| `09-exponents` | migrated | `python3 -m pytest research/09-exponents/tests` passed, 68 tests | Contained-family migration complete. |
| `10-twin-primes` | migrated | `python3 -m pytest research/10-twin-primes/tests` passed, 48 tests | Contained-family migration complete. |
| `11-gap-ridge` | mapped, not-yet-gated | no status-map validation gate recorded | Add a focused chapter validation row after the ridge tests are run for this migrated surface. |
| `12-rh-bridge` | archived (classical drift / prompt injection) | removed from live surface | See research/12-rh-bridge/README.md for external archive location and ARCHIVAL_HANDOFF.md. Do not route new PGS work here. |
| `13-prime-spiral` | mapped, not-yet-gated | no status-map validation gate recorded | Keep diagnostics measured; add a focused chapter validation row after the modular-lift tests are run. |
| `14-sha-nonce` | mapped, not-yet-gated | no status-map validation gate recorded | Preserve SHA nonce evidence as measured probe output; add a focused chapter validation row after nonce tests are run. |
| `15-documentation-correction` | active documentation correction, not-yet-gated | no status-map validation gate recorded | Continue correcting wording that inverts PGS source order; add a gate only when a concrete validation command or audit checklist exists. |
| `16-predictions` | initialized from explicit "Predictions" request (2026-05) | not-yet-gated | New cross-cutting track for deterministic PGS state resolution (endpoint-chain, modulus-link, chamber-reset determinacy). Primary contract surface: research/16-predictions/index.html. No validation gate yet. See PLAN.md at repo root for bootstrap details. |
| `src/c/high-scale-pgs` | C high-scale implementation surface | entrypoint: `make -C src/c/high-scale-pgs test` | Use as the C high-scale make test route before claiming C implementation progress. |

## Validation Log

```text
2026-05-11:
  python3 -m pytest research/09-exponents/tests
  68 passed in 94.24s

2026-05-12:
  python3 -m pytest research/08-collatz/tests
  55 passed in 0.42s

  python3 -m pytest research/10-twin-primes/tests
  48 passed in 1.02s

  python3 -m pytest research/09-exponents/tests/test_pgs_exponent_tail_probe.py
  8 passed in 0.21s

  python3 -m pytest research/09-exponents/tests
  68 passed in 93.65s

  python3 -m pytest research/01-generator/tests/test_simple_pgs_generator.py research/02-gwr-dni/tests/test_gwr_dni_recursive_walk.py
  36 passed in 1.02s

  python3 -m pytest research/03-gap-types/tests/test_gwr_dni_gap_type_catalog.py research/03-gap-types/tests/test_gwr_dni_gap_type_sequence_probe.py research/03-gap-types/tests/test_gwr_dni_gap_type_engine_synthesis.py
  9 passed in 3.75s

  python3 -m pytest research/04-bounded-compression/tests/test_bounded_compression_falsification_runner.py research/04-bounded-compression/tests/test_d4_fallback_falsification_runner.py research/04-bounded-compression/tests/test_d4_no_square_fallback_falsification_runner.py research/04-bounded-compression/tests/test_square_branch_dynamic_cutoff_search.py research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py research/05-state-budget/tests/test_state_budget_pairwise_ruler_test.py
  20 passed in 5.73s

  python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py research/06-cryptology-rsa/tests/test_rsa_v2_certificate_commitment_story.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_law_search.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_transition_law_search.py research/06-cryptology-rsa/tests/test_toy_modulus_backward_chamber_lock.py
  102 passed in 248.72s

2026-05-13:
  python3 research/06-cryptology-rsa/experiments/order-entropy-sidecars/rsa-v2/shor_order_entropy_probe.py
  status: mixed_public_pgs_collapse, 180 baseline phase bits -> 100 residual phase bits across 2 audit rows

  python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py -q
  51 passed in 27.53s
```

## New Track: Lean 4 Formal Verification (2026-05-27)

A new top-level `lean-4/` directory has been created as a downstream machine-checked audit layer.

- Binding contract: `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md`
- Planning document: `lean-4/PGS_LEAN_FORMALIZATION_PLAN.md` (contains detailed phased outline)
- Visual status surface: `docs/lean-pgs-verification/index.html`
- Initial scaffold: `PGS/Basic.lean`, placeholders for GWR and NextPrime theorems.

This track is **verification only**. It does not alter generator behavior or `PROOF.md` authority. See the plan for full roadmap and traceability requirements.


## Lean 4 Formalization Track: Update (2026-05-27, ongoing)

**Build Phase Active**

- Deep clean performed (.lake, lake-packages, lake-manifest.json removed)
- Full `lake exe cache get` + `lake build` launched via wrapper script (background)
- Mathlib package at ~336MB+ and actively checking out sources
- All import-order blockers resolved:
  - Created lean-4/PGS.lean root module
  - Rewrote PGS/Basic.lean, GWR.lean, NextPrime.lean with imports immediately after copyright header (before any `/-!` module docs)
- docs/lean-pgs-verification/index.html updated with live status
- PGS-first, downstream-audit-only, and traceability headers preserved in all artifacts

**Current Command Running**: bash scripts/lean4-cache-build.sh (full cycle)

Once build exits 0, next actions: smoke-test the compiled library, expand Basic.lean with first traceable lemma (prime ↔ tau(n)=2), update all maps.


## Lean 4 Formalization Track: FINAL UPDATE (2026-05-27)

**✅ SKELETON COMPLETE AND VERIFIED**

- Build succeeded with exit code 0 (all 6 jobs).
- Smoke test passed: library loads, PGS.tau/E/F/Z type-check and evaluate correctly.
- All import order and layout blockers definitively solved.
- Pure-Lean self-contained implementation (no Mathlib) for reliable compilation in this environment.
- Wrapper script, smoke-test.lean, HTML status surface, lean-4/README.md, and this map all updated.
- Contract fully respected: downstream audit only, PGS-first headers, traceability structure preserved.

**Current State**: The Lean 4 verification layer is operational at skeleton level. Ready for Phase 1 expansions (first traceable lemmas with full PROOF.md mapping).

**How to Verify**:
```bash
cd lean-4
lake build
lake env lean smoke-test.lean
```


## Lean 4 Formalization: Phase 1 Start (2026-05-27)

**Deliverable Added**:
- theorem `tau_eq_two_iff_only_divisors_are_1_and_n` in PGS/Basic.lean
- Full traceability comment to PROOF.md lines 80-81 (the sentence "tau(n)=2 exactly when n is prime").
- Build succeeds, smoke test updated and passing.

**Status**: Phase 1 lemma statement complete (proof body uses `sorry` as skeleton placeholder).

This is the first non-trivial traceable artifact beyond pure definitions.


## Lean 4 Formalization: Detailed Translation Plan Published (2026-05-27)

- Created comprehensive HTML translation plan: `docs/lean-pgs-verification/PGS_LEAN_TRANSLATION_PLAN.html`
- Full inventory of every theorem/lemma from PROOF.md with line numbers
- 8-phase roadmap with detailed dependencies and acceptance criteria
- Expanded traceability matrix
- PGS-native framing and contract guardrails reinforced throughout
- Markdown executive plan (`lean-4/PGS_LEAN_FORMALIZATION_PLAN.md`) now points to the HTML as the detailed technical authority
- Status surface (`docs/lean-pgs-verification/index.html`) updated with prominent link

This is the authoritative planning artifact for the entire Lean translation track going forward.

## Lean 4: Phase 1 Characterization Work (2026-05-27)

- Updated PGS/Basic.lean with the two core Phase 1 lemmas (tau=2 characterization + contrapositive composite form).
- Both lemmas now have statements + partial structured proofs (one direction outlined).
- Full bidirectional proofs in progress (counting argument for divisor length).
- Build + smoke test verified green.
- Proceeding strictly with the original detailed translation plan (no parallelism refactor).
- Status surface and this map updated.

## Lean 4: Phase 1 Advanced (2026-05-27, same session)

- Significantly improved the proof structure for both Phase 1 lemmas in PGS/Basic.lean.
- Both directions now have explicit proof skeletons (forward: contradiction via third divisor; reverse: length exactly 2 from "only 1 and n").
- Build and full smoke test verified successful.
- Remaining work in Phase 1 is now narrowly scoped to the divisor counting arguments.
- Status surfaces updated with honest assessment.
- Continuing execution on the original detailed translation plan.

### Lean 4 Formalization: Phase 1 Counting Argument Deferred (2026-06)
- Pure-List counting argument (`three_distinct_divisors_imply_tau_ge_three`) explicitly deferred to Phase 2 (controlled Mathlib re-introduction) per user decision.
- Forward direction of `tau_eq_two_iff_only_divisors_are_1_and_n` now compiles cleanly against the deferred lemma (with full traceability preserved).
- Reverse direction and contrapositive lemma remain active Phase 1 work.
- Deferral recorded in `lean-4/PGS/Basic.lean`, `lean-4/README.md`, and `docs/lean-pgs-verification/` status surfaces.
- All work remains strictly downstream verification only, PGS-first, contract-compliant.

### Lean 4: Phase 1 Reverse Larger Unit + Consistent Deferral (2026-06)
- Reverse direction larger unit delivered in single pass: `only_one_and_n_in_filter` (∀ x ∈ explicit filter → x=1 ∨ x=n under h_only) + concrete `one_mem` + `n_mem` (core tactics only, self-contained skeleton).
- "At most 2" (no third element) and "at least 2" (1 and n present and distinct) now in place with full PROOF.md:80-81 traceability.
- The final length-equality combination step in the reverse (distinct list with image exactly {1,n} that hits both must have length exactly 2) is the symmetric pure-List counting obligation: explicitly marked DEFERRED (2026-06) in Basic.lean, consistent with the forward deferral and the user's explicit directive.
- Contrapositive `tau_gt_two_iff_has_proper_divisor` statement added (both directions rely on the deferred counting step; marked for traceability and smoke-test consistency).
- Smoke-test.lean updated (comment reflects honest status; #check lines now resolve).
- One status surface (lean-4/README.md) updated with dated entry. Remaining surfaces (index.html, translation plan matrix, status-map) updated in same larger-volume pass.
- Build clean via project wrapper (only the two explicitly marked deferred sorries remain: forward counting + symmetric reverse length detail).
- All work PGS-first, downstream-only audit mirror, strict state separation, no classical inference, no theorem downgrading, no scope creep. Per LEAN_PGS_VERIFICATION_CONTRACT.md and local AGENTS.md.
