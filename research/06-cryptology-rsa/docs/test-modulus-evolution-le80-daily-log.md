# le80 live-solver daily log

Branch: `feat/test-modulus-evolution-le80`

## 2026-08-21 pin

- Action: created long-lived branch and plan file.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline
- Outcome: PASS (docs pin only)
- Commands: github create_branch from main; push plan + log
- Next: A1 rebuild ladder fixtures and pin 40/50/64 audit row

## 2026-08-22 A1 attempt

- Action: rebuild data-ladder fixtures via `build_ladder_fixtures.py`; run `run_experiment.py` on 40/50/64; run `audit_experiment.py` on filtered cases.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline (unchanged)
- Outcome: BLOCKED
- Commands:
  - `python3 research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/build_ladder_fixtures.py`
  - fixture hashes: ladder_cases.jsonl `36e95fc5b4cd32a9ca0961ff619d3708a80c500ddeb19ee58c3087cf2bbd9184`; audit_factors.jsonl `0622b1db3131233f5679734bd96a7cade2d894d2641e220140d4054833fc9fa8`
  - `python3 run_experiment.py --case-ids rsa_v2_40bit_static_001` → public_endpoint_class_found / endpoint_class_by_reciprocal_deadline_signature_correction
  - `python3 run_experiment.py --case-ids rsa_v2_50bit_static_001` → unresolved_by_reciprocal_carrier_misalignment
  - `python3 run_experiment.py --case-ids rsa_v2_64bit_static_001` → unresolved_by_profile_count_mismatch (endpoint_chain_steps=1162)
  - `python3 audit_experiment.py` on filtered 40/50/64 inference: factor_found true / false / false
- Exit criterion gap: required 40-true / 50-v2-false / 64-true; measured 40-true / 50-false / 64-false
- Evidence: 64-bit public_closure_status=`unresolved_by_profile_count_mismatch` (SESSION_BOOTSTRAP expected mutual certificate closure / factor_found=true)
- Next: operator diagnosis of profile_count_mismatch on rsa_v2_64bit_static_001 before A1 can pin

## 2026-08-23 A1 re-check

- Action: confirm fixtures rebuild hashes; re-attempt 40-bit and 64-bit public runs; confirm plan blocker still active.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline (unchanged)
- Outcome: BLOCKED
- Commands:
  - `python3 research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/build_ladder_fixtures.py`
  - fixture hashes confirmed identical: ladder_cases.jsonl `36e95fc5b4cd32a9ca0961ff619d3708a80c500ddeb19ee58c3087cf2bbd9184`; audit_factors.jsonl `0622b1db3131233f5679734bd96a7cade2d894d2641e220140d4054833fc9fa8`
  - `python3 run_experiment.py --case-ids rsa_v2_40bit_static_001` → public_closure_status=endpoint_class_by_reciprocal_deadline_signature_correction
  - 64-bit run initiated but long-running (endpoint_chain_steps high); prior evidence of unresolved_by_profile_count_mismatch retained
- Exit criterion gap unchanged: required 40-true / 50-v2-false / 64-true; measured surface still fails 64-true
- Evidence: profile_count_mismatch on rsa_v2_64bit_static_001 persists as blocker; no discriminator or bound edits applied
- Next: operator diagnosis of profile_count_mismatch on 64-bit fixture before A1 can pin

## 2026-08-24 A1 re-check

- Action: rebuild fixtures; confirm hashes; re-run 40-bit public inference; code-path inspection of matched_profile_counts_hold; confirm 64-bit still subject to profile_count_mismatch rejection path.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline (unchanged)
- Outcome: BLOCKED
- Commands:
  - `python3 research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/build_ladder_fixtures.py`
  - fixture hashes confirmed identical: ladder_cases.jsonl `36e95fc5b4cd32a9ca0961ff619d3708a80c500ddeb19ee58c3087cf2bbd9184`; audit_factors.jsonl `0622b1db3131233f5679734bd96a7cade2d894d2641e220140d4054833fc9fa8`
  - `python3 run_experiment.py --case-ids rsa_v2_40bit_static_001` → public_closure_status=endpoint_class_by_reciprocal_deadline_signature_correction
  - code inspection: matched_profile_counts_hold requires lower.active_count == upper.active_count and lower.unresolved_count == upper.unresolved_count; rejection path active for 64-bit after high chain steps
- Exit criterion gap unchanged: required 40-true / 50-v2-false / 64-true; measured surface still fails 64-true
- Evidence: profile_count_mismatch on rsa_v2_64bit_static_001 persists as blocker (SESSION_BOOTSTRAP expects mutual_certificate_closure); no discriminator, boundD, or window edits applied
- Next: operator diagnosis of profile_count_mismatch / active_count mismatch on 64-bit fixture before A1 can pin

## 2026-08-25 A1 re-check

- Action: rebuild fixtures; confirm hashes identical to prior pins; re-run 40-bit public inference (closes); confirm 64-bit remains subject to profile_count_mismatch rejection after high chain steps; no discriminator, boundD or window edits.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline (unchanged)
- Outcome: BLOCKED
- Commands:
  - `python3 research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/build_ladder_fixtures.py`
  - fixture hashes confirmed identical: ladder_cases.jsonl `36e95fc5b4cd32a9ca0961ff619d3708a80c500ddeb19ee58c3087cf2bbd9184`; audit_factors.jsonl `0622b1db3131233f5679734bd96a7cade2d894d2641e220140d4054833fc9fa8`
  - `python3 run_experiment.py --case-ids rsa_v2_40bit_static_001` → public_closure_status=endpoint_class_by_reciprocal_deadline_signature_correction
  - 64-bit probe (max_steps limited / timeout) retains prior surface: unresolved_by_profile_count_mismatch path active
- Exit criterion gap unchanged: required 40-true / 50-v2-false / 64-true; measured surface still fails 64-true
- Evidence: matched_profile_counts_hold rejection (active_count / unresolved_count mismatch) on rsa_v2_64bit_static_001 persists; SESSION_BOOTSTRAP expects mutual certificate closure / factor_found=true for the pin; no code change
- Next: operator diagnosis of profile_count_mismatch / active_count mismatch on 64-bit fixture before A1 can pin

## 2026-08-26 A1 re-check

- Action: rebuild fixtures; confirm hashes identical to prior pins; re-run 40-bit and 50-bit public inference; confirm 64-bit remains subject to profile_count_mismatch rejection after high chain steps; no discriminator, boundD or window edits.
- PHASE: A
- NEXT_SLICE: A1-rebuild-and-pin-baseline (unchanged)
- Outcome: BLOCKED
- Commands:
  - `python3 research/06-cryptology-rsa/experiments/data-ladder/rsa-v2/build_ladder_fixtures.py`
  - fixture hashes confirmed identical: ladder_cases.jsonl `36e95fc5b4cd32a9ca0961ff619d3708a80c500ddeb19ee58c3087cf2bbd9184`; audit_factors.jsonl `0622b1db3131233f5679734bd96a7cade2d894d2641e220140d4054833fc9fa8`
  - `python3 run_experiment.py --case-ids rsa_v2_40bit_static_001` → public_closure_status=endpoint_class_by_reciprocal_deadline_signature_correction
  - `python3 run_experiment.py --case-ids rsa_v2_50bit_static_001` → public_closure_status=unresolved_by_reciprocal_carrier_misalignment
  - 64-bit probe retains prior surface: unresolved_by_profile_count_mismatch path active (matched_profile_counts_hold requires active_count and unresolved_count equality)
- Exit criterion gap unchanged: required 40-true / 50-v2-false / 64-true; measured surface still fails 64-true
- Evidence: matched_profile_counts_hold rejection (active_count / unresolved_count mismatch) on rsa_v2_64bit_static_001 persists; SESSION_BOOTSTRAP expects mutual certificate closure / factor_found=true for the pin; no code change
- Next: operator diagnosis of profile_count_mismatch / active_count mismatch on 64-bit fixture before A1 can pin
