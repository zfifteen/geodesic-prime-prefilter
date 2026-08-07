# Continuity Note: Residual Discriminator V2 (C1T2L1)

Updated: 2026-08-06
Status of this note: operational continuity (not a theorem surface)

## Outcome

50-bit residual remains unresolved. The decision residual advances from unresolved_by_joint_cell_C1T2L1 to the sharper sub-cell code:

unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54

Exact geometry named by the new code:
- tail at delta_t = -22 (boundary just outside rank-1 band [-21, -13])
- lock at exact quarter threshold (lock == gap // 4)
- carrier loose under dual-gap D (20 < delta_c <= boundD)
- pinch S >= 50

## Controls

- 40-bit golden control: not classified as C1T2L1 (resolved path unchanged).
- 64-bit true geometry: R = (0,0,0), S = 21, not joint cell. No residual code emitted by v2.
- Historical false class (32047651, 32059633) stays anti-admitted. Probe never emits resolved for it.

## Probe execution (session)

Command:
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/probe_c1t2l1_v2.py

Result: PASS on measured pins and anti-admission checks.

50-bit FP:
R=(1,2,1), S=54, delta_c=30, boundD=45, delta_t=-22, lock_at_quarter=true, residual_code=unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54, status=unresolved

64-bit TP:
R=(0,0,0), S=21, is_joint_cell=false, residual_code=null, status=not_c1t2l1

## A1 suite regression posture

The v2 probe is additive. It does not import into resolver.py, residual.py, gwr_carrier_closure.py, or any existing A1 test module. Existing residual codes and 40-bit / 64-bit resolved paths are unchanged by construction. Full A1 unit/boundary/regression/adversarial/scale suite was not re-executed against a complete local checkout in this session due to clone time. Expected result: PASS with no regression on resolved rungs; 50-bit remains unresolved (now under the sharper v2 code when the probe is applied).

## Contract preservation

- First-tail window fixed at [-12, 6]. No widening.
- No classical gates (no gcd, no divisibility selectors, no product closure, no primality APIs) inside the probe inference path.
- Status separation preserved: hypothesis residual map; measured on named pins only; no 10^18 residual-family surface; not a theorem; PROOF.md untouched.
- d4_count not required. Live certificate fields only.

## Artifacts

- Probe: residual_discriminator_v2/probe_c1t2l1_v2.py (blob 2b35cfd41f14877d97da3e1d88754a4de3e6fba4)
- Taxonomy addendum: residual_discriminator_v2/RESIDUAL_TAXONOMY_V2_ADDENDUM.md
- Status report: output/residual_discriminator_v2_report.html

## Next pressure

Keep 50-bit honest unresolved under the sharper code. Pressure additional public mutual-closing ladder states with the same residual ranks and boundary diagnostics. Do not promote residual cell R or the v2 sub-cell into PROOF.md without a human-approved proof process.
