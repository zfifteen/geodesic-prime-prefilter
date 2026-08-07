# Codex Continuity Start Here — 50-bit residual path update (2026-08-07)

This file is the canonical bootstrap. The 50-bit residual status has changed.

## 50-bit measured resolve (rsa-v3, 2026-08-07)

V2 kept the pin unresolved under
`unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54`.

V3 carrier reciprocal closure finds public pair `(32047633, 32059651)`:
- N//L == U and N//U == L
- remainder 6170868
- delta_c = 30 ≤ boundD = 45
- deadline=tail signatures match
- historical false class (32047651, 32059633) blocked
- closure_status = endpoint_class_by_reciprocal_deadline_signature_correction

Status: **measured-on-regime-only / hypothesis**.
Not a theorem. Not a factorisation claim.
First-tail window remains fixed at [-12, 6].

Continuity pin:
`research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`

Artifacts:
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/`
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/`

The older residual history (carrier misalignment → first-tail → joint cell)
remains valid chronology. The V3 path is the current measured disposition.

Do not edit PROOF.md. Do not claim verified language without a 10^18 residual-family surface.
