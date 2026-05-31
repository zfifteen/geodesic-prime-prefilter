# State-Budget Carriers Prediction Candidates Catalogue

**PGS Predictions v0.1 track — deterministic carrier laws only**

**Observable object:** After a known prime `p`, the finite ordered sequence of integers from `p+1` to `q-1` (where `q` is the next prime returned by the divisor-count traversal) carries a complete divisor-count field `τ(n)`. The integer `w` is the leftmost position in that interval that attains the global minimum `τ` value inside the interval. The current chamber is the gap interval whose divisor-count field, selected-integer properties, square-phase utilization `U_□(w, q) = (q - w) / (S₊(w) - w)`, and any carried reset signature or previous reduced state are the PGS objects under study.

**PGS Predictions definition (from research/16-predictions/pgs_predictions_v0.1_contract.html):** A deterministic rule or measurable carrier law, built only from already-proved or explicitly measured PGS objects (divisor-count field, DNI coordinate `E(n)`, GWR leftmost-minimizer `w`, endpoint chains, modulus links, chamber-reset signatures, reciprocal transport), that from the current chamber state (or a short, fully determined preceding window) either resolves one or more future PGS states exactly (position of next `w`, next gap type after `w`, next chamber-reset signature, next modulus-link residual, etc.) or returns an explicit unresolved state when the carrier does not decide.

**Strict constraints applied throughout this catalogue:**
- PGS objects and invariants first: divisor-count field (specifically `d4_count` = number of positions with `τ(n)=4` inside the current ordered prime-gap chamber interior), GWR `w`, square-phase flag and utilization `U_□`, chamber invariants (selected-integer family/offset, first-open offset, carrier_family, previous_reduced_state), reset signatures.
- No probabilistic language.
- State separation mandatory: theorem (only in PROOF.md), measured result on exact regime, hypothesis, unresolved state, invalidated rule.
- All claims subordinate to PROOF.md (Interior Maximizer Theorem and direct next-prime theorem) for theorem status and to AGENTS.md / local Agents.md for reasoning discipline.
- Carriers operate on current-chamber facts under explicit match modes; they do not invoke candidate testing, primality APIs, or product closure to choose the resolved state.

**Primary surfaces used for extraction:**
- `research/05-state-budget/output/state_budget_long_running_catalog_8192/` (57344 deterministic retained rows, 8192 rows per power, `10^12..10^18`, 45603 current `d=4` transition rows scored).
- `research/05-state-budget/output/state_budget_forbidden_transition_catalog_2048/` (2048 rows per power, same powers).
- Supporting probes on `10^12..10^15` and pooled retained windows.

**Proved foundation (PROOF.md, relevant GWR parts):**
The Interior Maximizer Theorem states: given prime `p` and next prime `q` returned by the deterministic divisor-count traversal, let `I = {p+1, …, q−1}` (nonempty). Then `w = min { n ∈ I : τ(n) = min_{m ∈ I} τ(m) }` is the unique integer in `I` that maximizes `F(n) = −E(n)`. The No-Later-Simpler-Composite corollary follows directly: once `w` has appeared, no later integer in the same interior has strictly smaller `τ`. These are universal under the stated hypotheses; finite surfaces certify implementations only.

## Candidate 1: d4_count as Next-Triad Ordering Carrier

**PGS Objects & Invariant:** Current-chamber divisor-count field (specifically the scalar `d4_count` = count of interior positions with `τ(n) = 4`). The carrier law operates under the match mode `mod30_prev_gap_exact` (current PGS chamber facts + endpoint residue modulo 30 + exact previous gap width fixed). It orders the next triad state (next gap reduced type after the current chamber).

**File:line + exact quote or data:**
- `research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_divisor_carrier_sweep_summary.json:731` (decisive row):
  ```json
  {
    "match_mode": "mod30_prev_gap_exact",
    "measure": "d4_count",
    ...
    "eligible_cells": 3646,
    "decisive_pairs": 7881,
    "oriented_signed_advantage": 299,
    "tail_control_signed_advantage": 230,
    "edge_over_tail_control": 69,
    "required_edge": 50,
    "ordering_carrier_stop_condition_met": true
  }
  ```
- `research/05-state-budget/output/state_budget_long_running_catalog_8192/state_budget_long_running_research_report.md:5`:
  > the current chamber's `d4_count` orders the next triad state with `7881` decisive matched pairs, all seven held-out powers above `100` decisive pairs, six positive held-out folds, `299` oriented signed wins, and a `69` signed-win edge over the endpoint-tail control. The required edge on this support is `50`.
- Script definition: `research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py:107`:
  ```python
  d4_count = len(d4_offsets)
  ```
  where `d4_offsets` are offsets inside the current chamber where `divisor_counts_segment` yields exactly 4 (lines 99-105).

**Current Status (measured with exact regime / hypothesis / etc.):** Measured result. On the deterministic retained 8192-row-per-power `10^12..10^18` surface (45603 current `d=4` transition rows), under `mod30_prev_gap_exact`, `d4_count` meets the full ordering-carrier stop condition (`decisive_pairs >= 5000`, all 7 folds >=100 decisive pairs, >=6 positive oriented folds, edge over tail control >= required). Verdict in summary: `"ordering_carrier_found"`. All other candidate measures in the same sweep (including `d4_span`, `d4_centroid_offset`, `divisor_sum`) failed at least one gate. This is the strongest existing precedent cited in `research/16-predictions/pgs_predictions_v0.1_contract.html`.

**Best next falsification experiment (specific script + command if possible):**
```
python3 research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py \
  --detail-csv research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv \
  --output-dir /tmp/d4_count_replication_8192 \
  --min-power 12 --max-power 18
python3 -m pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py -q
```
Replicate on a fresh disjoint 8192-row-per-power construction (different row selection within each power) or on the 2048-row catalog for cross-surface check. Extend the sweep to emit `w_offset` alongside `d4_count` for Family 1 unification.

**Strength as deterministic forward resolver:** Highest in catalogue. Resolves next-triad state (a concrete future chamber state) on 7881 decisive matched pairs after full held-out protocol and tail-length control. Returns explicit `"no_ordering_carrier_found"` or per-fold `"unresolved"` when gates fail. Directly implements the Predictions definition on current-chamber divisor-count field objects only.

**Drift risks:** Reinterpretation of the match-mode discipline as a statistical model; extension of the carrier claim beyond current `d=4` transition rows or outside the exact `mod30_prev_gap_exact` cells; treating the measured edge (+69) as a universal constant rather than surface-specific.

## Candidate 2: Square-Phase Budget Bit (d4_low / d4_high) as Current-Chamber Extension to Hidden State

**PGS Objects & Invariant:** For current chambers with `next_dmin == 4`, the square-phase utilization `U_□(w, q) = (q - w) / (S₊(w) - w)` (where `S₊(w)` is the smallest prime square strictly above `w`). Split at the exact pooled median of this utilization inside local-geometry cells keyed by selected-integer family, selected-integer offset, and first-open offset. Produces the ternary label `non_d4` / `d4_low` (utilization below median) / `d4_high` (at or above median). This is a current-chamber signature carried forward to resolve next-is-triad state.

**File:line + exact quote or data:**
- `research/05-state-budget/docs/phase_budget_hidden_state_probe_findings.md:17`:
  > For current `d = 4` rows, compute prime-square interval utilization `U_□(w, q) = (q - w) / (S₊(w) - w)`. Then, inside each current local-geometry cell (selected-integer family, selected-integer offset, first-open offset), split rows at the exact pooled median of `U_□(w, q)`. Rows below that median are labeled `d4_low`. Rows at or above it are labeled `d4_high`.
- Script: `research/05-state-budget/scripts/gwr_phase_budget_hidden_state_probe.py:212`:
  ```python
  row["phase_budget_bit"] = (
      "d4_low" if utilization < medians[key] else "d4_high"
  )
  ```
- Pooled readout (same findings.md:43):
  > when appended to the current parity-plus-previous-state model, it adds `0.023067` more pooled gain. ... the low-budget and high-budget `d = 4` halves are separated by a next-triad gap of `0.057217`.
- Held-out status (research/00-index/continuity/START_HERE.md:427):
  > With `configured_balance_floor = 0.10`, the current retained surface does not promote the state-budget bit. Four held-out folds are unresolved from low/high imbalance. Three folds are balanced enough to score, and all three return `does_not`.

**Current Status (measured with exact regime / hypothesis / etc.):** Measured result on pooled `10^12..10^18` retained window (gains and separation as above). Hypothesis on the bit as a one-bit record of square-budget usage. Unresolved on the strict held-out ruler test surface (`research/05-state-budget/output/state_budget_heldout_ruler_test.csv` and pairwise/residue extensions); the balanced folds return `does_not`. Not promoted to carrier.

**Best next falsification experiment (specific script + command if possible):**
```
python3 research/05-state-budget/scripts/gwr_phase_budget_hidden_state_probe.py \
  --detail-csv research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv \
  --output-dir /tmp/phase_budget_replication
python3 research/05-state-budget/scripts/state_budget_heldout_ruler_test.py \
  --detail-csv ... --output-dir /tmp/heldout_phase_budget_check --configured_balance_floor 0.10
```
Re-run the probe on a balanced-construction retained surface (explicitly target equal `d4_low`/`d4_high` support per cell) and apply the identical ruler protocol with `min_control_margin=15`.

**Strength as deterministic forward resolver:** Moderate. The bit is computed strictly from current-chamber `w`, `q`, and next square (PGS objects). It separates next-triad share by 0.057217 inside already-matched hidden-state cells on the pooled surface. Returns no resolution on the held-out balanced folds. Could be unified with d4_count for a joint carrier on w-position or gap-type once a balanced surface exists.

**Drift risks:** Treating the pooled gain (0.023067) as a per-power monotonic law; conflating the utilization split (a current-chamber fact) with a next-chamber label; allowing log-loss framing to replace the required match-mode + decisive-pairs protocol.

## Candidate 3: w-Offset Positioning Carrier (Family 1)

**PGS Objects & Invariant:** The offset `w − p` (GWR-selected integer position) inside the current chamber. Proposed deterministic function of the local structure visible at or before the first `d(n)=4` arrival (under square exclusion) plus any active chamber-reset or modulus-link signature carried from the previous gap. Explicitly: given current-chamber `d4_count` + square-phase flag (`d4_low`/`d4_high` or raw `U_□`) + previous-gap tail length (under fixed match), the next `w` offset lies in a stated small integer set, or the carrier returns unresolved.

**File:line + exact quote or data:**
- `research/16-predictions/pgs_predictions_v0.1_contract.html:84` (Family 1):
  > In the ordered divisor-count field of the gap after `p`, the offset `w − p` is a deterministic function of the local structure visible before or at the first `d(n)=4` arrival (under square exclusion) plus any active chamber-reset or modulus-link signature carried from the previous gap.
- Contract recommendation (same file:105):
  > The generator already emits the selected integer position. Chapter 05 already has the retained-surface machinery, the match-mode discipline, the held-out fold protocol, and the exact "ordering_carrier_found / does_not / unresolved" verdict language. Extending that exact protocol to the `w` offset (instead of next-triad gap type) is the smallest step...
- Current implementation note (contract): the generator already computes `carrier_w` (or equivalent) as part of chamber-reset state.

**Current Status (measured with exact regime / hypothesis / etc.):** Latent hypothesis / recommended first executable path. No explicit carrier law or retained-surface measurement for `w` offset resolution has been executed under the Predictions protocol. The existing d4_count ordering carrier and the divisor-payload scalars already computed in the 8192 catalog provide the direct instrumentation path. The Interior Maximizer Theorem (PROOF.md) guarantees `w` is uniquely determined by the divisor-count field; the carrier question is whether a short preceding window of chamber invariants suffices to resolve its offset before the full traversal.

**Best next falsification experiment (specific script + command if possible):**
Instrument `research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py` (or a narrow fork) to also emit `w_offset` (or `next_peak_offset` from the gap-type catalog details) as the target. Run the identical match-mode + held-out protocol:
```
python3 research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py \
  --detail-csv ...8192.../gwr_dni_gap_type_catalog_details.csv \
  --output-dir /tmp/w_offset_carrier_8192 --target w_offset
```
Then apply the stop-condition logic (decisive pairs, 6/7 positive folds, edge over appropriate control) and the held-out ruler test. Reproduction baseline: `python3 -m pytest research/05-state-budget/tests/test_state_budget_divisor_carrier_sweep.py`.

**Strength as deterministic forward resolver:** High potential (contract identifies it as minimal executable step that re-uses the entire audited 05-state-budget machinery). Directly resolves a concrete future PGS state (position of next `w`) from current-chamber divisor-count field objects plus carried previous state. Returns explicit unresolved when the small-set prediction fails.

**Drift risks:** Allowing the generator's internal `carrier_w` computation to become the inference engine instead of an auditable post-hoc carrier law on retained surfaces; classical framing of "offset prediction" instead of exact small-set resolution under match mode.

## Candidate 4: d=4 Square-Ceiling Closure Margin Rules

**PGS Objects & Invariant:** For the earliest non-cube `d=4` semiprime selected integer `w` in a gap, let `r` be the smallest prime with `r² > w`. The square-threat ceiling is `S₊(w) = r²`. The closure margin is `M_□(p, q, w) = r² − q`. The branch facts (whether `r² − 2` is prime) plus the measured jump behavior partition possible `q` values into the floor package or a bounded deeper set.

**File:line + exact quote or data:**
- `research/05-state-budget/docs/d4_square_ceiling_branch_note.md:100`:
  > So the first exact non-floor branch currently visible is: `q = r² − 6`.
- Same file:160 (candidate local lemma):
  > Let `(p, q)` be a prime gap whose implemented score maximizer `w` is the earliest non-cube `d=4` semiprime after `p`, and let `r` be the smallest prime with `r² > w`. Then closure at `r² − 4` does not occur.
- Measured surfaces cited: `research/04-bounded-compression/output/d4_square_threat_frontier_summary.json` (floor package at margin 2), `d4_square_threat_nonfloor_frontier_summary.json` (first non-floor at 6 through 10^8), `d4_square_threat_r2_minus_4_obstruction_summary.json` (zero margin-4 closures on the live branch through 10^8; 814228 floor-package cases).
- PROOF.md cross-ref (square-branch characterization): `s² < P(r²) < r²`.

**Current Status (measured with exact regime / hypothesis / etc.):** Measured result on exact scanned surfaces (full to 10^6 + even-band ladder 10^8..10^18 for floor; exact 10^8 non-floor branch). Hypothesis: the algebraic floor `M_□ >= 2` (from `r²-1` composite for odd `r`) plus the observed jump from 2 to 6 (zero margins 3/4/5) plus the `r²-4` obstruction (zero observed) will close into a deterministic partition once the `r²-4` lemma is proved. Currently: proved algebraic floor + measured branch decomposition on the stated regimes; the `r²-4` exclusion remains open (unresolved theorem target).

**Best next falsification experiment (specific script + command if possible):**
Use the existing bounded-compression frontier scanners (or the d4_square threat probes referenced in the note) on a larger exact surface, e.g. through 10^9 or the 8192-row catalog windows. Command skeleton (adapt from chapter 04 scripts):
```
python3 research/04-bounded-compression/scripts/..._d4_square_threat...py \
  --max-prime 1000000000 --output-dir /tmp/square_ceiling_1e9_check
```
Cross-check against the 05-state-budget 8192 catalog details (which already contain `winner`, `next_right_prime`, and square-root data). Test the candidate lemma directly: count any `q == r²-4` rows on the live earliest-non-cube-d4 branch.

**Strength as deterministic forward resolver:** Strong on the measured regime. Once the current `w` is known to be the earliest non-cube `d=4` semiprime and `r` is identified from the divisor field, the possible `q` positions are partitioned into a singleton floor or a bounded deeper set (`<= r²-6`). This resolves the future endpoint (gap closure) exactly or returns the open obstruction. Directly extends the Interior Maximizer Theorem with square-phase invariants.

**Drift risks:** Generalizing the measured jump (2 → 6) into an unconditional theorem without the `r²-4` exclusion; classical analytic tail bounds presented as the primary output instead of the integer-level partition on the live branch.

## Candidate 5: Phase-Reset Signatures as Chamber Transition Carriers

**PGS Objects & Invariant:** Chamber-reset signatures (rules such as `reset_on_odd_winner`, `reset_on_odd_semiprime`, `reset_on_higher_divisor`, `reset_on_even_winner`). These label the transition from previous reduced state to current chamber state and are scored for their effect on downstream concentration of the reduced gap-type model (pooled-window L1 and three-step concentration) plus explicit reset-signature gain.

**File:line + exact quote or data:**
- `research/05-state-budget/docs/phase_reset_hunter_findings.md:3`:
  > The best reset law over the `hidden_state_augmented_rotor` base recipe is `reset_on_odd_winner` with pooled-window concentration L1 `0.0196`, three-step concentration `0.3970`, and reset-signature gain `0.7611`.
- Rule table (same file:9):
  ```
  reset_on_odd_winner:      pooled L1 0.0196, three-step 0.3970, reset gain 0.7611
  reset_on_odd_semiprime:   pooled L1 0.0203, three-step 0.4046, reset gain 0.9592
  ...
  no_reset:                 pooled L1 0.0231, three-step 0.4502, reset gain 0.0000
  ```
- Artifacts: `research/05-state-budget/output/gwr_phase_reset_hunter_rules.csv`, `gwr_phase_reset_hunter_summary.json`, script `gwr_phase_reset_hunter.py`.

**Current Status (measured with exact regime / hypothesis / etc.):** Measured result on the `10^12..10^15` surface (or the hidden-state-augmented retained window used by the hunter). The rules are explicit deterministic functions of current-chamber facts (winner parity, carrier family, next_dmin). They improve concentration and carry measurable reset gain. No held-out carrier-gate protocol (decisive pairs, ordering-carrier stop condition) has been applied to them in the 8192/2048 catalogs; they remain probe-level measurements.

**Best next falsification experiment (specific script + command if possible):**
```
python3 research/05-state-budget/scripts/gwr_phase_reset_hunter.py \
  --detail-csv research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv \
  --output-dir /tmp/reset_hunter_8192
```
Then feed the emitted reset labels into the divisor-carrier sweep or held-out ruler machinery as an additional match key or candidate measure. Compare reset-augmented cells against the plain `mod30_prev_gap_exact` baseline on the same 8192 surface.

**Strength as deterministic forward resolver:** Moderate-to-high. Reset signatures are current-chamber (or immediate-previous) objects that deterministically label the state transition and measurably alter the distribution of the next reduced state. They can serve as additional match dimensions or direct carriers for next-chamber reset signature or gap-type resolution. The explicit gain numbers provide a clear falsification surface.

**Drift risks:** Conflating concentration improvement (a model-fit metric) with exact state resolution under the Predictions match-mode protocol; allowing the hidden_state_augmented_rotor base to drift into a statistical generator.

## Candidate 6: Other d4-Derived Scalars as Ordering Candidates (d4_span, d4_last_to_endpoint, d4_centroid_offset, ...)

**PGS Objects & Invariant:** Current-chamber divisor-count field scalars derived alongside `d4_count`: `d4_span` (distance between first and last `d=4` position), `d4_last_to_endpoint` (distance from last `d=4` to right endpoint), `d4_centroid_offset` (average offset of all `d=4` positions), plus `divisor_sum`, `divisor_mean`, `low_divisor_load`.

**File:line + exact quote or data:**
- Script definition (research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py:113):
  ```python
  return {
      "d4_count": d4_count,
      "d4_span": d4_last - d4_first,
      "d4_last_to_endpoint": right_prime - (left_prime + d4_last),
      "d4_centroid_offset": sum(d4_offsets) / d4_count,
      ...
  }
  ```
- Sweep summary (state_budget_divisor_carrier_sweep_summary.json, multiple rows): all non-`d4_count` measures under all three match modes failed at least one ordering-carrier gate (either directional consistency < 6/7 or edge over tail control below threshold). Example `mod30_prev_gap_exact` `d4_span` row shows negative or sub-threshold oriented advantage.

**Current Status (measured with exact regime / hypothesis / etc.):** Measured non-carriers on the identical 8192-row `10^12..10^18` surface and protocol that promoted `d4_count`. They are explicit "does_not" results under the same decisive-pairs and held-out discipline. They remain available as negative controls or for joint-carrier constructions (e.g., `d4_count` + `d4_last_to_endpoint`).

**Best next falsification experiment (specific script + command if possible):** The same replication command as Candidate 1 already exercises the full set. Any future run of the sweep on a new retained surface falsifies (or potentially promotes) them uniformly.

**Strength as deterministic forward resolver:** Low individually (failed the stop condition). Useful as contrast: they demonstrate that not every scalar derived from the current divisor-count field carries ordering information at the required strength. Joint use with `d4_count` or the budget bit is an open measured-surface question.

**Drift risks:** Cherry-picking post-hoc the single measure that passed while ignoring the full candidate list; elevating any sub-threshold edge into a "weak carrier" claim without repeating the full gate protocol.

## Candidate 7: In-Gap d=4 Carriers for Witness Recovery (GWR/DNI Recursive Walk)

**PGS Objects & Invariant:** The sequence of `d=4` positions inside the current gap interior (the "carriers" in the witness-search sense). The GWR witness walk uses the first (or dominant) in-gap `d=4` arrival after a seed to recover the selected integer `w` and thereby the next prime without full re-traversal of the entire interval.

**File:line + exact quote or data:**
- `research/02-gwr-dni/tests/test_pnt_gwr_d4_candidate_sweep.py:45`:
  ```python
  assert summary["blocked_by_pre_gap_d4_count"] == summary["gap_has_d4_count"]
  ```
- `research/02-gwr-dni/tests/test_pnt_gwr_predictor.py:72` (profile fields):
  ```python
  "gap_has_target_carrier": True,
  "last_pre_gap_carrier": 12,
  "first_in_gap_carrier": 18,
  "last_in_gap_carrier": 18,
  ```
- Dominant d4 arrival reduction findings and recursive walk scripts (`research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py`, `gwr_witness_walk.py`).
- PROOF.md cross-reference: the residual K=128 first-d4 branch-elimination theorem and square-branch characterization.

**Current Status (measured with exact regime / hypothesis / etc.):** Measured on multiple exact surfaces (full scans through 10^7, even-band ladders to 10^18, square-adjacent probes). The witness recovery is exact on the tested regimes when the target carrier remains ahead of the seed. The dominant-d4 reduction is a measured optimization of the divisor-field work. Not yet framed as an explicit Predictions-style carrier law that, from a short preceding window, resolves the exact location of the next `w` or next prime.

**Best next falsification experiment (specific script + command if possible):**
```
python3 -m pytest research/02-gwr-dni/tests/test_gwr_witness_walk.py research/02-gwr-dni/tests/test_pnt_gwr_predictor.py -q
python3 research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py --start 11 --count 100000 --output /tmp/witness_walk_check.json
```
Instrument the walk to emit, for each resolved gap, the preceding-window d4 carrier state (count, first offset, span) and test whether a small-set rule on that state resolves the observed `winner_offset` on the 8192 catalog surface.

**Strength as deterministic forward resolver:** High on the witness-recovery contract (exact recovery when carrier ahead). Provides a concrete mechanism for resolving the position of the next `w` (and therefore the next prime) from the divisor-count field objects already visible early in the chamber. Directly aligns with Family 1.

**Drift risks:** Re-introducing classical candidate-testing language around the "witness search"; allowing the optimization (pre-sieve or interval reduction) to alter the exact GWR output records.

## Candidate 8: Reciprocal Reset-Signature / Endpoint-Cell Closure (Endpoint Determinacy)

**PGS Objects & Invariant:** Reset endpoints, reset signatures, and reciprocal transport between lower and upper cells in an endpoint chain. A mutual-reset endpoint cell (both directions satisfy the reciprocal deadline-signature and floor-transport closure) resolves the public endpoint class exactly. Misalignment returns the explicit state `unresolved_by_reciprocal_carrier_misalignment`.

**File:line + exact quote or data:**
- `pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility-probe.py:52` (cell source logic):
  ```python
  if status in {
      "endpoint_class_by_mutual_certificate_closure",
      "unresolved_by_reciprocal_carrier_misalignment",
  }:
      ...
      "mutual_reset_endpoint_cell",
  ```
- `pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility.html` (table rows):
  - `(3221225473, 3221275501)` marked "mutual reset endpoint cell" with closure flags `(1,1)`.
  - `(32047651, 32059633)` rejected.
- Cross-ref: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/` artifacts (PGS_CERTIFICATE.md, METRICS.md) and START_HERE.md RSA v2 state summary (40-bit and 64-bit resolved by public mutual certificate closure; 50-bit unresolved by reciprocal carrier misalignment).

**Current Status (measured with exact regime / hypothesis / etc.):** Measured result on the live RSA v2 ladder rungs (explicit 40-bit/64-bit resolutions after reciprocal correction; 50-bit unresolved). The carrier is the mutual satisfaction of the reciprocal transport equations on the reset endpoints and signatures. Not a universal theorem; exact on the tested endpoint-chain instances.

**Best next falsification experiment (specific script + command if possible):**
Run the boundary-drop probe and the live-solver experiment on additional semiprime or RSA-scale endpoint chains drawn from the same high-window regime as the 8192 catalog:
```
python3 pgs-unsolved-problems/endpoint-determinacy/2026-05-20-boundary-drop-admissibility-probe.py
python3 research/06-cryptology-rsa/experiments/live-solver/rsa-v2/run_experiment.py
```
Count resolutions vs. explicit `unresolved_by_reciprocal_carrier_misalignment` on fresh chains. Feed reset-signature labels from the 05-state-budget phase-reset hunter as an additional carrier dimension.

**Strength as deterministic forward resolver:** High on the endpoint-determinacy contract. When the reciprocal carrier conditions hold, the future public endpoint class (a concrete structural state) is resolved exactly from the chain invariants and reset signatures. Returns explicit unresolved on misalignment. Directly uses chamber-reset signatures and reciprocal transport (core PGS objects named in the Predictions definition).

**Drift risks:** Re-interpreting the RSA v2 ladder as ordinary factorization search; allowing audit labels (factor_found) to leak into the inference rule; treating the 50-bit unresolved case as a statistical failure instead of an explicit carrier-misalignment state.

## Invalidated or Sub-Threshold Candidates (for Completeness)

- **Square-room side as forbidden-transition exclusion carrier:** Tested on both 2048-row and 8192-row catalogs (`research/05-state-budget/scripts/state_budget_forbidden_transition_test.py`). On the 2048 surface: base violation rate 0.169292 (10030 eligible, 1698 violations); all modes rejected exact next-state exclusion. Verdict: invalidated rule on the retained high-window surfaces (START_HERE.md:499).
- **Prime-square boundary vs. endpoint tail as independent ordering carrier (pairwise ruler test):** On 8192 surface, square-ruler signed advantage tracks tail length too closely (edge +2 or +14 below the min_control_margin=15 gate in most matched modes). Verdict: unresolved as an independent carrier (the signal exists but does not isolate the square boundary).
- **Parity + previous_reduced_state as base hidden state (early miner):** Produced measurable log-loss gains on `10^12..10^15` (best candidate lift 0.057152 over width/open baseline). Later held-out and pairwise tests on larger surfaces returned unresolved or sub-margin for promotion. Remains a measured observation, not a carrier under the current protocol.

These provide clean negative surfaces for any future joint-carrier work.

## Top 5 Strongest Candidates (Ranked by Strength as Deterministic Forward Resolver under Predictions Definition)

1. **d4_count as Next-Triad Ordering Carrier** (Candidate 1)  
   Exact numbers on the largest audited retained surface (8192 rows/power, 10^12..10^18): 7881 decisive pairs, 6/7 positive folds, +69 edge over tail control (required 50), full stop-condition met, verdict `ordering_carrier_found`. Pure current-chamber divisor-count field object. Highest strength.

2. **Reciprocal Reset-Signature / Endpoint-Cell Closure** (Candidate 8)  
   Resolves concrete public endpoint classes exactly (40-bit and 64-bit rungs) or returns explicit `unresolved_by_reciprocal_carrier_misalignment` (50-bit). Uses reset signatures and reciprocal transport directly. Audited on live RSA v2 ladder.

3. **d=4 Square-Ceiling Closure Margin Rules** (Candidate 4)  
   Once earliest non-cube d=4 `w` and `r` are fixed from the divisor field, partitions the future endpoint `q` into proved floor singleton or measured bounded deeper set on exact surfaces through 10^18 (floor) / 10^8 (non-floor). Direct extension of the Interior Maximizer Theorem with square-phase invariants. Strong measured partition; one open local lemma.

4. **w-Offset Positioning Carrier (Family 1)** (Candidate 3)  
   Highest latent potential. Re-uses the entire audited 05-state-budget match-mode + held-out machinery. Directly targets resolution of next `w` position (core GWR object) from current d4_count + square-phase + carried previous state. Explicitly recommended in the Predictions contract as the minimal next executable step.

5. **Square-Phase Budget Bit (d4_low / d4_high)** (Candidate 2)  
   Computed strictly from current `w`, `q`, and next square. Adds 0.023067 pooled gain and 0.057217 next-triad separation inside existing hidden-state cells on the retained surface. Held-out ruler test currently returns unresolved/does_not on balanced folds; therefore lower rank than the above, but the object is PGS-native and the falsification path is narrow and existing.

All other candidates (reset signatures, in-gap d4 witness carriers, sub-threshold d4 scalars) are useful supporting surfaces or joint-construction opportunities but rank below the top five on current evidence strength under the strict Predictions carrier-gate protocol.

**Reproduction and verification of this catalogue:**
- Full state-budget tests: `python3 -m pytest research/05-state-budget/tests -q`
- 8192 catalog artifacts and the divisor-carrier sweep summary supply the primary numbers.
- Cross-check against `research/00-index/continuity/START_HERE.md` (state-budget hidden-state section) and `research/16-predictions/pgs_predictions_v0.1_contract.html` (definition and Family 1 recommendation).
- `git status --short --untracked-files=all` before any extension work.

This catalogue exhausts the state-budget, hidden-state, d4_count, ordering-carrier, and next-state material discovered in the mandated bootstrap reads and deep exploration targets. Every entry respects the PGS-first frame, deterministic language, and state separation. No entry has been promoted beyond its exact measured regime or the proved theorems in PROOF.md.

*Catalogue written on the predictions branch. All claims subordinate to PROOF.md for theorem status.*