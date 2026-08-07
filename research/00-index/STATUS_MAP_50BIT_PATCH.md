# Status-map patch — 50-bit residual (2026-08-07)

The row for `06-cryptology-rsa/experiments/live-solver/rsa-v3` previously stated:

```text
Live 50-bit residual (measured, still unresolved): unresolved_by_joint_cell_C1T2L1
```

Update to:

```text
Live 50-bit residual (measured-on-regime-only / hypothesis):
  V2: unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54
  V3: resolved under carrier reciprocal closure
       endpoint_class = [32047633, 32059651]
       closure_status = endpoint_class_by_reciprocal_deadline_signature_correction
  First-tail window fixed [-12, 6]. Not a factorisation claim. PROOF.md untouched.
```

Full continuity pin:
`research/00-index/continuity/notes/ACTIVE_GOAL_50bit_residual_discriminator.md`

Artifacts:
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/`
`research/06-cryptology-rsa/experiments/live-solver/rsa-v3/output/`
