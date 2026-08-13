# Reframe changelog

Docs-only wording and status-surface work.
No code, proofs, or experimental logs deleted.

## 2026-08-13 : three-tier public status

Branch: `docs/reframe-status-tiers`

### Added

- `docs/reframe/AUDIT.md`: quoted mixture and overclaim sites on `main`.
- `docs/STATUS_TIERS.md`: Proved / Measured / Experimental map.
- This file.

### README.md

- Abstract rewritten so the project is an ordered divisor-count study plus
  an experimental walk engine, with Lean named as an audit mirror.
- Three-row Proved / Measured / Experimental table inserted immediately
  after the abstract, linking `docs/STATUS_TIERS.md`.
- Section 2 split into `2.1 What Is Proved` and `2.2 What Is Measured`.
- Restored the public heading `Bounded Compression at the Cramér Scale`
  (required by `test_public_doc_breakthrough_status.py`).
- NLSC 10^18 zero-violation ledger moved out of the proved list into 2.2.
  The GWR corollary (no later interior has smaller `tau`) stays with GWR.
- Section 5: Lean "completed" language replaced by audit-mirror language.
  Named finite bases, pinned certs, one core-path axiom
  `tau_prime_square_eq_three` (CL-003), core `sorry` count zero.
- Generator paragraph: primality audit still required after selection.
- RSA paragraph: probe only. Curated 40 / 50 / 64 / 128 / 256-bit examples.
  Removed "general deterministic PGS-native engine that scales to 1024-bit+"
  as a success claim.
- Repository map and reading list now point at `docs/STATUS_TIERS.md`.
- Lean badge text set to audit-mirror wording.

### Sub docs

- `research/06-cryptology-rsa/README.md`: louder measured/hypothesis header
  and ledger explanation (endpoint class vs factor solve).
- `docs/rh/README.md` and `docs/rh/dni-to-zeta-compression.md`: one-line
  "reading path, not RH proof" banner. Classical identities named.
- `docs/OVERVIEW.md`: link to `STATUS_TIERS.md`.
- `lean-4/README.md`: audit-only scope plus `STATUS_TIERS.md` and contract
  pointers.

### Deliberately not done

- No demotion of universal bounded compression or Prime-Square Proximity.
  Those remain Tier 1 under `PROOF.md` / `AGENTS.md`.
- No `PROOF.md` theorem-status edit.
- No deletion of `assert_results.tsv`, certificates, RSA residual packages,
  Lean inventory, or gallery assets.
- Requested path `docs/dni_rh_bridge.md` does not exist. Banner applied to
  the live public bridge page instead.
