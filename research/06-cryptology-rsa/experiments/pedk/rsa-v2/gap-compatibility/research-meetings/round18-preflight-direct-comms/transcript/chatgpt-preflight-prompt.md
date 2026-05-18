# ChatGPT Pre-Flight Prompt

ROUND18 PREFLIGHT BRIEF

ATC has handed ChatGPT comms to Codex. Treat this as the first officer pre-flight check for the next PGS/PEDK experiment. Codex is pilot, Grok is co-pilot, user is ATC. We are no longer copy/pasting through ATC unless comms fail.

Current runway:
- Repo: https://github.com/zfifteen/prime-gap-structure
- Post-flight course correction meeting: https://github.com/zfifteen/prime-gap-structure/blob/main/research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/research-meetings/post-flight-course-correction/minutes.md
- Round 17 finite certificate: https://github.com/zfifteen/prime-gap-structure/blob/main/research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/codex_round17_partial_width_certificate.py
- Round 17 debrief: https://github.com/zfifteen/prime-gap-structure/blob/main/research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/ROUND17_FLIGHT_DEBRIEF.md

Flight status before takeoff:
- Round 17 landed a finite-scope certificate for the 163|19/a10 near-miss.
- Landed finite chain: finite a10 -> width 14 -> previous_left_mod30 17 -> first_open_offset 2 -> not prev_open_offset 4.
- theorem_status remains hypothesis_not_proved.
- universal_proof_complete remains false.
- Do not claim factor_found.
- Do not add premises.
- Do not descend into another singleton lane unless the matrix proves that is unavoidable.

Round 18 target:
Build a mechanically auditable 12-lane mechanism compression matrix over the current same-phase evidence surface.

Primary question:
Are the four Round 10/11 component laws genuinely distinct public obstructions, or do they collapse into one or two reusable width/residue/offset/parity selector mechanisms when all 12 same-phase lanes are examined uniformly?

Expected Codex/Grok deliverables:
- core-evidence/codex_round18_component_obstruction_compression.py
- core-evidence/grok_round18_component_obstruction_compression.py
- output/codex_round18_component_obstruction_compression/lane_mechanism_matrix.jsonl
- output/codex_round18_component_obstruction_compression/mechanism_groups.json
- output/codex_round18_component_obstruction_compression/compression_summary.json
- output/codex_round18_component_obstruction_compression/proposed_next_proof_object.json
- output/codex_round18_component_obstruction_compression/falsifier_contracts.jsonl
- matching Grok output folder with same file names.

One row per theoretical same-phase lane. Required fields:
- lane
- orientation
- phase coordinate or a_mod6/b_mod6
- survivor/excluded status
- first failing public predicate, or survives
- representative row or prior surface status
- previous_gap_width / following_gap_width
- containing-left / containing-right residues
- next_winner_offset / previous_winner_offset where present
- computed first-open offsets
- parity source
- terminal image status
- factor_relevance_under_current_operational_definition
- mechanism_features
- derived_mechanism_class
- prior_component_law_label
- mechanism_class_rule
- falsifier contract

Important tightening from the post-flight meeting:
- derived_mechanism_class must be computed from mechanism_features, not copied from Round 10/11 labels.
- prior_component_law_label is comparison only.
- Add enough deterministic evidence that the class rule is auditable.
- factor relevance means: public selector survivor -> terminal image -> lower-terminal four-slot lift -> candidate factor-side endpoint class. This is structural alignment, not factor_found.

Candidate hypothesis H18:
The four Round 10 component laws are projections of fewer public grammar mechanisms, likely:
A. entry-side width/residue/open-offset mismatch
B. exit-side offset/parity mismatch
with the survivor lanes being exactly the lanes that avoid both.

Null H18:
The four component laws are genuinely distinct, so the best next route is to prove them separately, but with extracted width/residue/parity mechanisms attached.

Requested response:
1. PRE_FLIGHT_STATUS: GO or NO-GO.
2. If GO, state the exact implementation contract you want Codex/Grok to obey.
3. If NO-GO, name the single blocker and the smallest correction.
4. Give one cockpit-style sentence: are we climbing back to the 12-lane selector, level in cruise, or already overfitting again?

Keep the response tight and theorem-status disciplined.
