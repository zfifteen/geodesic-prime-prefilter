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

The chapter homes now preserve **universal bounded compression as proved**
(`PROOF.md`, 2026-07-05: selected-witness offset `w - p`, not raw gap size
`q - p`, not RH/PNT), the fixed-cutoff invalidation, square-branch audit
corroboration surfaces, and the measured `d4_count` state-budget carrier.
Audit tables and falsification sweeps remain implementation evidence; they do
not bound the universal theorem.

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
reciprocal endpoint closure, while the 50-bit rung (v2 runner pin unresolved; rsa-v3 V3 measured reciprocal candidate) remains historically documented at
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
| `06-cryptology-rsa` | mapped | Focused RSA command passed, 102 tests | RSA v2 unresolved states preserved; rsa-v3 V3 measured resolve for 50-bit. |
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
| `20-enhancement-roadmap` | formalized program enhancement catalog + A1 requirements + A1 test plan | documentation-only; open `research/20-enhancement-roadmap/index.html` | Not-yet-gated. HTML catalog of candidates A-H; full requirements for A1 at `a1-rsa-endpoint-resolver/index.html`; formal test plan at `a1-rsa-endpoint-resolver/test-plan.html` (A1-TP). Does not change theorem status. |
| `21-modular-residual-salvage` | residual partition + broader measure + H-210/H-tau16 pressure + dynamic wheel (2026-07) | `python3 -m pytest research/21-modular-residual-salvage/tests -q`; measure: `python3 research/21-modular-residual-salvage/scripts/measure_modular_closed.py --p-max 250000`; pressure: `python3 research/21-modular-residual-salvage/scripts/pressure_h210_htau16.py`; CE audit: `python3 -m pytest research/01-generator/tests/test_mod30_adjacent_carrier_generator.py -q` | Soft density outside spine. Broader measure [11,250000) measured-only (1/843 closed). H-210/H-tau16 not_falsified_in_tested_regime on [11,200000) (hypothesis only). Dynamic wheel optional/hypothesis. Does not change theorem status. |
| `06-cryptology-rsa/experiments/live-solver/rsa-v3` | A1 PGS-native RSA modulus endpoint resolver v3 | `python3 -m pytest research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_unit.py research/06-cryptology-rsa/tests/test_a1_certificate_verifier.py research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_boundary.py research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_regression.py research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_adversarial.py research/06-cryptology-rsa/tests/test_a1_endpoint_resolver_scale.py -q` | Implementation of enhancement A1. Residual ledger: run `residuals.jsonl` under output dir; taxonomy in `rsa-v3/RESIDUAL_TAXONOMY.md`. Live 50-bit residual (measured-on-regime-only / hypothesis): V2 joint cell C1T2L1; V3 carrier reciprocal closure resolves under `resolved_by_carrier_reciprocal_closure` endpoint_class=[32047633,32059651]. See residual_discriminator_v2/ and DOCUMENTATION_LOCK_50BIT_V3.md. Launch: `rsa-v3/run_resolver.py`. Does not claim factorization. |

## Validation Log

```text
2026-05-11 through 2026-07: see historical validation blocks in git history.
2026-08-07: 50-bit residual documentation updated for V3 carrier reciprocal measured resolve.
```

## Lean 4 Formalization Track: M0–M5 CLOSED (2026-07-23)

Core-stack program DoD complete. See `lean-4/peer/M5_DOD_ACCEPT.md` and
`docs/lean-pgs-verification/index.html`. Parent #53 DONE.

**How to verify:**
```bash
cd lean-4
lake build
lake env lean smoke-test.lean
rg 'sorry' PGS/*.lean   # expect: no matches
rg -n '^\s*axiom ' PGS/*.lean   # expect: tau_prime_square_eq_three only
```
