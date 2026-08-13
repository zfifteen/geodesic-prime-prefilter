# Reframe audit (2026-08-13)

Phase 1 only. No code, proofs, or experimental logs were deleted.
This file records where public language can be misread as a single grand claim.

Authority for theorem status remains `PROOF.md`.
This audit does not demote universal pillars.

Corrected public surface: [docs/STATUS_TIERS.md](../STATUS_TIERS.md).

## Method

Read on `main` at `a94e937ff2d62bfb32e176e6c60e39c18152d3be`:

- `README.md`, `PROOF.md`, `AGENTS.md`
- `docs/OVERVIEW.md`, `docs/RESULTS.md`, `docs/core/*.md`
- `docs/rh/README.md`, `docs/rh/dni-to-zeta-compression.md`
- `lean-4/README.md`, `lean-4/LEAN_PGS_VERIFICATION_CONTRACT.md`,
  `lean-4/DEFINITION_OF_DONE.md`, `lean-4/SORRY_AXIOM_INVENTORY.md`,
  `lean-4/peer/M5_DOD_ACCEPT.md`
- `research/06-cryptology-rsa/README.md`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/README.md`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/README.md`
- `visualizations/gallery/index.html` header

Requested path `docs/dni_rh_bridge.md` does not exist.
Public bridge page: `docs/rh/dni-to-zeta-compression.md`.
Workbench pointer `research/12-rh-bridge/docs/dni_rh_bridge.md` is archived.
Live stub: `research/12-rh-bridge/README.md`.

Exact forbidden phrases `breaks RSA`, `factors RSA`, `proves RH`, and
`no primality test needed` do **not** appear as those strings.
Overclaim is by mixture and scale language, not those four slogans.

## Claim classes requested by the reframe packet

| Class | Verdict on `main` |
| --- | --- |
| Deterministic prime generation without testing | Root README implies selection needs no primality test. Audit confirmation is mentioned, but a reader can miss it. |
| RSA factorization | Root README can be read as a general engine that scales to 1024-bit. The RSA chapter already denies a factorization claim. |
| 256 / 512 / 1024-bit scaling as success | Root README presents those widths as engine scale. Committed ladder is curated 40 / 50 / 64 / 128 / 256-bit probes. 50-bit is unresolved under the v2 runner. |
| RH proof | Root README and `docs/rh/` already say `PROOF.md` does not prove RH. Mixing RH into the abstract still invites a 30-second misread. |
| Lean fully self-contained proof | Lean DoD is complete as an **audit program**. Finite bases enter as named hypotheses. One core-path axiom remains. |

## Quoted overclaim or mixture sites

### README.md

**Abstract mixes proved local theorems with a 10^18 measured surface and an RH reading path.**

```text
README.md:12
Prime Gap Structure demonstrates that the integers between consecutive primes
form an ordered divisor-count field whose internal minimum (the Gap Winner)
and return to divisor count = 2 together locate the next prime deterministically.
```

```text
README.md:14
Local theorems are formally proved and computationally validated. These theorems
include the Gap Winner Rule (GWR), bounded compression at Cramér scale, the
Prime-Square Proximity Theorem (proved 2026-07-05), and the No-Later-Simpler-
Composite Theorem (zero violations through 10¹⁸).
```

NLSC's 10^18 zero-violation ledger is a measured surface.
Listing it in the same "formally proved" sentence as GWR and UBC is the
mixture this reframe exists to stop.

```text
README.md:16
The same core stack also has a **completed Lean 4 machine-checked mirror**
under `lean-4/` (program Definition of Done M0-M5, 2026-07-23)
```

True as an audit-program DoD. Easy to misread as a fully self-contained
proof of the prose theorems with no remaining hypotheses.

```text
README.md:131
The following local theorems are formally proved in `PROOF.md` and have been
computationally validated with zero violations through 10¹⁸.
```

This applies one 10^18 measured predicate to the whole proved list.
`PROOF.md` does not bound universal pillars by that scan.

```text
README.md:138
- **No-Later-Simpler-Composite Theorem**: Once the minimal divisor count has
  appeared, no simpler composite occurs later in the gap.
```

NLSC as "no later interior integer has smaller `tau`" is an immediate
corollary of leftmost min-`tau` selection (GWR). The infinite-proof status
of a separately named NLSC theorem is not a `PROOF.md` headline pillar.
The 10^18 stress surface belongs in Measured.

```text
README.md:181
**Status: complete (program Definition of Done, M0-M5, 2026-07-23).**
```

```text
README.md:257
No trial division, no Miller-Rabin rounds, no probabilistic guesses are needed
to choose the answer. The arithmetic structure itself shows where the gap ends.
Any verification testing that follows is only confirmation; it is not part of
the generation step.
```

PGS selection is a `tau`-scan, not Miller-Rabin. The sentence is still too
easy to read as "no primality audit is required." Confirmation audit remains
required after selection.

```text
README.md:261
The program has completed the transition from rung-specific measured
demonstrations to a general, deterministic PGS-native engine. ...
It scales to representative 256-bit, 512-bit, and 1024-bit+ examples
```

This is the primary RSA-scale overclaim on the public front page.
The RSA chapter does not claim a 1024-bit factor solve.

### PROOF.md

No RSA-break or RH-proof claim. Headline already separates:

- universal pillars (next-prime, GWR, UBC including PSPT)
- certified finite premises
- downstream RH reading (`PROOF.md` does not itself prove RH)
- bound is on selected-witness offset `w - p`, not raw gap `q - p`

Lean is described as an in-progress independent mirror, not as theorem authority.

### AGENTS.md

Does not overclaim. It **forbids** the failure modes this reframe is fixing:

- do not downgrade proved PGS theorems
- do not declare RSA-scale or RH resolution
- theorem / measured / audit / unresolved must stay separated
- `PROOF.md` controls theorem status

A literal Meta AI packet that moved UBC and PSPT into "measured, not infinite
proof" would violate this contract. That demotion was rejected.

### docs/OVERVIEW.md

Honest on RH: "exploratory and kept separate from the proved local results."
Missing a 30-second status table. No `STATUS_TIERS.md` link before this reframe.

### docs/RESULTS.md

Already separates theorem / validated implementation / regime-bounded rows.
RSA section already says measured endpoint structure, not a universal
RSA-scale theorem. 50-bit V3 path is labeled hypothesis, not factorization.

### docs/core/*.md

No RSA-break, RH-proof, or 1024-bit success language.
`RECURSIVE_PRIME_WALK.md` states NLSC as the GWR closure condition and then
gives finite walk counts. That is consistent with corollary plus measurement.

### docs/rh/

`docs/rh/README.md` already says `PROOF.md` does not itself prove RH and
marks pole placement as an unresolved proof target.
`docs/rh/dni-to-zeta-compression.md` already labels `D(s)=zeta(s)^2` and
`(e^2/2)K(s)/D(s) = -zeta'/zeta` as exact zeta compression (classical
identities) and the RH sentence as unresolved source-to-spectral placement.

Missing: a one-line banner a skimming reader cannot miss.

### lean-4/

`LEAN_PGS_VERIFICATION_CONTRACT.md` is already audit-only and PGS-first.
`DEFINITION_OF_DONE.md` already says finite bases stay hypotheses and
`PROOF.md` is never rewritten by a green build.
`SORRY_AXIOM_INVENTORY.md` already records:

- core `sorry` count 0
- one core-path axiom: `tau_prime_square_eq_three` (CL-003)
- three named finite-base packages with pinned cert paths and hashes
- Lean does not re-prove exhaustions

`lean-4/README.md` lead line "Program DoD met" is accurate for the audit
program and still needs an explicit "not a self-contained proof" pointer
plus a link to `docs/STATUS_TIERS.md`.

### research/06-cryptology-rsa/

Chapter README and v2/v3 READMEs already deny an RSA-scale resolver theorem
and a factorization claim unless audit reports `factor_found=true`.

Ledger already on the chapter README:

```text
rsa_v2_40bit_static_001: factor_found = true
rsa_v2_50bit_static_001: factor_found = false   (v2 runner pin)
rsa_v2_64bit_static_001: factor_found = true
```

40-bit and 64-bit `true` rows are audit-confirmed endpoint classes.
50-bit `false` under v2 is the expected unresolved baseline.
V3 pair `(32047633, 32059651)` is already labeled
`carrier_reciprocal_closure` / measured-on-regime-only / hypothesis.

The chapter needed a still louder header, not a status rewrite.
The root README was the file that overclaimed.

### visualizations/gallery/index.html

Header is a plot catalog with status chips and regimes.
No RSA, RH, or Lean proof claim.

## Evidence artifacts (inventory, not deleted)

| Artifact | Role | Notes on this checkout |
| --- | --- | --- |
| `assert_results.tsv` | Named public assertion ledger | Present. Current committed content is a short FAIL row set (S1-P4), not the 10^18 NLSC table. |
| `docs/proof-enhancements/certificates/gwr_finite_base_v1.json` | Finite premise for GWR earlier-integer side | Present. Hash pinned in `PROOF.md` and Lean inventory. |
| `docs/proof-enhancements/certificates/bounded_compression_base_v1.json` | Finite premise for UBC small-`q` base | Present. |
| `docs/proof-enhancements/certificates/residual_k128_v1.json` | Residual K=128 elimination premise | Present. |
| `docs/proof-enhancements/certificates/gwr_stress_10e12_v1.json` | Measured GWR stress near 10^12 | Present. Not a theorem bound. |
| `research/03-gap-types/docs/gap_type_catalog_through_1e18.md` | 10^18 catalog prose | Present. |
| `data/external/primegap_list_records_1e12_1e18.csv` | External gap-record input | Present. |
| `docs/RESULTS.md` | Measured / theorem map | Present. Decade ladder `10^8` through `10^18`, 2816 / 2816. |
| `visualizations/gallery/` | Status-chipped plot library | Present. |
| Lean build logs | Mechanical DoD evidence | Not committed as log files. Peer accept is `lean-4/peer/M5_DOD_ACCEPT.md`. |
| `research/06-cryptology-rsa/output/` | RSA run output | Gitignored (`research/**/output/**`). |
| `residuals.jsonl` | V3 residual ledger per run | Runtime under each run's `output/`. Not a root committed file. |
| `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/` | Residual discriminator package | Present. |
| `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/DOCUMENTATION_LOCK_50BIT_V3.md` | 50-bit V3 lock note | Present in this checkout. |

## What this reframe will change

Language, structure, and status reporting only.

- Add `docs/STATUS_TIERS.md` with three tiers. UBC and PSPT stay **proved**.
- Rewrite the root README so a 30-second reader sees Proved / Measured / Experimental.
- Banner the RSA chapter and `docs/rh/` so probe and reading-path status cannot be missed.
- Clarify Lean as an audit mirror with named finite bases and one core-path axiom.
- Track wording in `docs/reframe/CHANGELOG_REFRAME.md`.

What this reframe will **not** change:

- No file deleted.
- No `PROOF.md` theorem-status edit.
- No demotion of UBC or PSPT to measured-only.
- No new RSA or RH claim.
