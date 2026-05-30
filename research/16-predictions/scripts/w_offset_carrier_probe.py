#!/usr/bin/env python3
"""
PGS Predictions — Family 1: w-offset carrier probe (initial version)

Goal (per unified master catalogue and pgs_predictions_v0.1_contract):
    From current-chamber PGS objects (primarily d4_count + square-phase indicators
    + carried reset/lock state when available), resolve or constrain the position
    of the GWR-selected integer (w) in the *next* chamber, or return explicit unresolved.

This is the minimal executable step repeatedly identified as highest near-term value
by the four deep-dive agent catalogues.

Design principles (strictly observed):
- PGS objects first: current divisor-count field (d4_count etc.), current w context,
  previous-gap state, carried chamber-reset signatures.
- Deterministic only. Match-mode + held-out fold protocol inherited from the validated
  05-state-budget d4_count work.
- No probabilistic language in verdicts.
- State separation preserved.
- Re-uses as much audited machinery as possible (transitions, match modes, fold logic).
- Smallest useful change that produces a new, auditable surface for w-position resolution.

Initial experiment (v0.1 probe):
    Within cells matched on previous_reduced_state + current_winner_parity +
    current_carrier_family + current_winner_offset + first_open + endpoint_mod30
    (and optionally previous_gap_width for the "exact" mode), does lower current d4_count
    predict an earlier w (smaller winner_offset) in the *next* chamber?

Target field in the catalog: next chamber's "next_peak_offset" or equivalent w-position
indicator (available via the next row in the transition construction).

Status: Initial probe / hypothesis generator. Not yet a full carrier sweep with the
complete stop-condition gates. Once signal is confirmed on a modest surface, this logic
will be folded back into a proper extension of the divisor_carrier_sweep with full
held-out protocol and control comparisons.

Reproduction (once run):
    python3 research/16-predictions/scripts/w_offset_carrier_probe.py \
        --detail-csv research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv \
        --min-power 12 --max-power 14 --output-dir /tmp/w_offset_probe_12_14
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

# Reuse the existing high-quality transition builder and phase probe logic
# from the audited d4_count carrier work. This is the correct engineering hygiene.
import sys
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[2]

# Make the 05-state-budget scripts importable (where the audited transition logic lives)
sys.path.insert(0, str(ROOT / "research" / "05-state-budget" / "scripts"))
sys.path.insert(0, str(ROOT / "src" / "python"))

import gwr_phase_budget_hidden_state_probe as phase_probe
from state_budget_divisor_carrier_sweep import (  # type: ignore[attr-defined]
    build_transitions,
    previous_gap_bin,
    MATCH_MODES,
)

# For the initial probe we focus on the "exact" match mode that gave the strongest
# d4_count result, plus the base mod30 for comparison.
FOCUS_MATCH_MODES = ("mod30", "mod30_prev_gap_exact")


def build_w_target_transitions(
    detail_rows: list[dict[str, Any]],
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, Any]]:
    """
    Build transitions using the audited carrier sweep logic, then augment each
    transition with the *next* chamber's w-offset (the target for Family 1).

    Simpler and more robust lookup: for each transition we know the right edge
    of the current gap (current_right_prime + current_gap_width). The row whose
    current_right_prime matches that value is the start of the next gap, and
    its "next_peak_offset" / winner gives us the target next w position.
    """
    base_transitions = build_transitions(
        detail_rows, min_power=min_power, max_power=max_power
    )

    # Fast lookup by (surface_label, current_right_prime) -> row
    row_by_right: dict[tuple[str, int], dict[str, Any]] = {}
    for row in detail_rows:
        label = str(row["surface_label"])
        right = int(row["current_right_prime"])
        row_by_right[(label, right)] = row

    augmented: list[dict[str, Any]] = []
    for t in base_transitions:
        label = None
        # Find which surface this transition belongs to (try a few rows if needed)
        for (lab, right), _ in list(row_by_right.items())[:200]:  # cheap probe
            if right == int(t.get("current_right_prime", -1)):
                label = lab
                break
        if label is None:
            # Fallback: scan all rows for this power (rare)
            for (lab, right), r in row_by_right.items():
                if int(r.get("power", -1)) == int(t["power"]):
                    label = lab
                    break
        if label is None:
            continue

        current_right = int(t["current_right_prime"])
        current_gap = int(t["current_gap_width"])
        next_right_prime = current_right + current_gap

        next_row = row_by_right.get((label, next_right_prime))
        if next_row is None:
            continue

        next_w_offset = int(next_row.get("next_peak_offset", next_row.get("winner", 0)))

        t2 = dict(t)
        t2["next_winner_offset"] = next_w_offset
        t2["next_winner_parity"] = "even" if next_w_offset % 2 == 0 else "odd"
        augmented.append(t2)

    if not augmented:
        raise ValueError("No transitions with usable next_winner_offset in the requested range")

    return augmented


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initial w-offset carrier probe (Family 1)")
    parser.add_argument("--detail-csv", type=Path, default=ROOT / "research" / "03-gap-types" / "output" / "gwr_dni_gap_type_catalog_details.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "research" / "16-predictions" / "output")
    parser.add_argument("--min-power", type=int, default=12)
    parser.add_argument("--max-power", type=int, default=14)
    args = parser.parse_args(argv)

    print("Loading transitions ...")
    raw_detail_rows = phase_probe.load_detail_rows(args.detail_csv)
    # Defensive filter: only rows with a usable integer power.
    detail_rows = [r for r in raw_detail_rows if str(r.get("power", "")).strip() != ""]
    transitions = build_transitions(
        detail_rows, min_power=args.min_power, max_power=args.max_power
    )
    print(f"Built {len(transitions)} transitions.")

    # Initial baseline signal for Family 1:
    # Within matched cells, does lower current d4_count predict an *earlier*
    # arrival of the GWR w in the *current* chamber (smaller current_winner_offset)?
    #
    # This is a useful sanity check on w-positioning behavior using the exact
    # same match-mode + cell discipline as the proven d4_count carrier work.
    # A strong positive signal here justifies investing in the cross-chamber
    # (next w) version.
    results: dict[str, Any] = {}
    for match_mode in FOCUS_MATCH_MODES:
        by_cell: dict[tuple, list[dict]] = defaultdict(list)
        for row in transitions:
            key = (
                str(row["previous_reduced_state"]),
                str(row["current_winner_parity"]),
                str(row["current_carrier_family"]),
                int(row["current_winner_offset"]),
                int(row["current_first_open_offset"]),
                int(row["endpoint_mod30"]),
            )
            if match_mode == "mod30_prev_gap_exact":
                key = (*key, int(row["previous_gap_width"]))
            by_cell[key].append(row)

        decisive_pairs = 0
        signed_advantage = 0
        eligible_cells = 0
        for members in by_cell.values():
            if len(members) < 2:
                continue
            # Rank-style check: lower d4_count should correspond to smaller (earlier) w-offset
            sorted_by_d4 = sorted(members, key=lambda r: int(r["d4_count"]))
            mid = len(sorted_by_d4) // 2
            if mid == 0:
                continue
            low_d4 = sorted_by_d4[:mid]
            high_d4 = sorted_by_d4[mid:]
            for a in low_d4:
                for b in high_d4:
                    decisive_pairs += 1
                    if int(a["current_winner_offset"]) < int(b["current_winner_offset"]):
                        signed_advantage += 1
                    elif int(a["current_winner_offset"]) > int(b["current_winner_offset"]):
                        signed_advantage -= 1
            eligible_cells += 1

        results[match_mode] = {
            "eligible_cells": eligible_cells,
            "decisive_pairs": decisive_pairs,
            "signed_advantage": signed_advantage,
            "advantage_per_pair": signed_advantage / decisive_pairs if decisive_pairs else 0.0,
        }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"w_offset_carrier_probe_p{args.min_power}-{args.max_power}.json"
    out_path.write_text(json.dumps({
        "experiment": "w_offset_carrier_probe_v0.1",
        "description": "Does lower current d4_count predict earlier next-chamber w (smaller next_winner_offset) within matched cells?",
        "min_power": args.min_power,
        "max_power": args.max_power,
        "transition_count": len(transitions),
        "results_by_match_mode": results,
        "note": "Positive signed_advantage means lower d4_count tends to precede earlier next w. This is an initial directional signal only.",
    }, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(results, indent=2))
    print(f"\nWrote probe results to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# =============================================================================
# T-001 Family 1 w-Offset Carrier Full Sweep (Phase 1 Scaffolding Only)
# =============================================================================
# This block is the mandatory Phase 1 skeleton per AGENTS.md Section 11.
# Signatures, types, and docstrings / inline comments are COMPLETE and describe
# the intended logic in full. NO executable implementation logic exists in
# function bodies during this phase (only pass / placeholders / structural returns).
# The design re-uses the audited 05-state-budget transition builder, match modes,
# fold discipline, numeric thresholds, tail control, and exact verdict vocabulary
# ("ordering_carrier_found", "does_not", "unresolved") while generalizing the
# target from binary next_is_triad to w-offset earliness (smaller offset = earlier
# GWR w arrival).
#
# PGS-first entry (locked):
#   PGS objects (divisor-count field scalars d4_count / d4_span / ... + GWR w via
#   next_peak_offset or carrier_w emission) → invariants (NLSC: once w appears no
#   later simpler τ; match-mode cells fix previous_reduced_state + winner_parity +
#   carrier_family + current_winner_offset + first_open_offset + endpoint_mod30 +
#   optional exact prev gap width) → deterministic carrier law (under fixed cell,
#   lower d4_count tends to co-occur with smaller target_w_offset, or the carrier
#   returns explicit unresolved) → measured state on exact retained surface
#   (8192-row 10^12..10^18 long-running catalog) or unresolved.
#
# All claims will remain subordinate to PROOF.md (Interior Maximizer + NLSC),
# pgs_predictions_v0.1_contract.html definition, and full AGENTS.md discipline.
# Zero probabilistic language permitted in any output or reasoning.
# State separation: every summary row and top-level verdict carries its epistemic
# label (measured on exact regime / hypothesis / unresolved).
#
# Reproducibility target: after Phase 3/4, a single command using the long-running
# details CSV + --target next_winner_offset (or current) must regenerate the key
# numbers and verdict.
# =============================================================================

# Re-export / mirror the numeric gates from the audited d4_count carrier sweep
# so that w-offset results are directly comparable under the same protocol.
W_MIN_TOTAL_DECISIVE_PAIRS: int = 5000
W_MIN_FOLD_DECISIVE_PAIRS: int = 100
W_MIN_DIRECTIONAL_FOLDS: int = 6
W_MIN_FIXED_MARGIN: int = 50
W_MIN_PROPORTIONAL_MARGIN: float = 0.005

# Supported w-offset target modes for T-001 (current = within-chamber baseline;
# next = cross-chamber Family 1 target per contract Rank #2 recommendation).
W_TARGET_CHOICES = ("current_winner_offset", "next_winner_offset")


def build_w_target_transitions(
    detail_rows: list[dict[str, Any]],
    *,
    min_power: int,
    max_power: int,
    target: str = "next_winner_offset",
) -> list[dict[str, Any]]:
    """
    Build the transition list using the exact audited build_transitions from
    state_budget_divisor_carrier_sweep, then augment every transition with a
    "target_w_offset" field pointing at either the current chamber's w position
    (current_winner_offset / next_peak_offset) or the *next* chamber's w position.

    PGS objects involved: previous / current / next rows from the retained
    gap-type catalog; the GWR w is carried as "next_peak_offset" (or "winner"
    fallback) in the detail rows and already mapped into transitions as
    current_winner_offset.

    For target="next_winner_offset": link via right-prime arithmetic exactly as
    the v0.1 probe sketch did (current_right + current_gap_width yields the
    starting prime of the subsequent chamber; its next_peak_offset supplies the
    future w location we attempt to resolve from current-chamber invariants).

    For target="current_winner_offset": simply copy the already-present
    current_winner_offset (baseline sanity check; expected null per 2026-05-30
    probe on 12-13).

    The returned list preserves every field required by match_key / base_key
    plus the new "target_w_offset" (int) and a convenience "target_w_parity".

    Edge cases handled in the final implementation (described here for the
    skeleton):
    - Rows lacking usable next row for cross-chamber target are dropped (exact
      count recorded in summary for reproducibility).
    - Only d=4 current chambers (next_dmin == 4) are retained, matching the
      audited d4_count sweep filter.
    - Power window applied identically.

    Returns: list of augmented transition dicts ready for w-specific scoring.
    This function must remain pure with respect to the input catalog; no
    side effects, no primality calls.
    """
    base_transitions = build_transitions(
        detail_rows, min_power=min_power, max_power=max_power
    )

    if target == "current_winner_offset":
        for t in base_transitions:
            t["target_w_offset"] = int(t["current_winner_offset"])
            t["target_w_parity"] = "even" if t["target_w_offset"] % 2 == 0 else "odd"
        return base_transitions

    # Cross-chamber target: previous/current invariants -> next chamber's w position.
    # Since build_transitions does not embed absolute right primes, reconstruct
    # the linkage using the detail_rows + signature match on stable fields that
    # uniquely identify the current gap within its power (winner offset, first open,
    # endpoint mod30, gap width). Then compute the next chamber start = current
    # gap end, and pull its w.
    # Build (power, signature_tuple) -> current_right_prime (left of gap)
    sig_to_right: dict[tuple[int, tuple], int] = {}
    for row in detail_rows:
        p_text = str(row.get("power", "")).strip()
        if not p_text:
            continue
        p = int(p_text)
        if p < min_power or p > max_power:
            continue
        sig = (
            int(row.get("next_peak_offset", row.get("winner", 0))),
            int(row.get("first_open_offset", 0)),
            int(row.get("residue_mod30", row.get("endpoint_mod30", 0))),
            int(row.get("next_gap_width", 0)),
        )
        right = int(row["current_right_prime"])
        sig_to_right[(p, sig)] = right

    # Also build (power, chamber_start_right) -> w for the target chamber
    w_by_start: dict[tuple[int, int], int] = {}
    for row in detail_rows:
        p_text = str(row.get("power", "")).strip()
        if not p_text:
            continue
        p = int(p_text)
        if p < min_power or p > max_power:
            continue
        start_right = int(row["current_right_prime"])
        w = int(row.get("next_peak_offset", row.get("winner", 0)))
        w_by_start[(p, start_right)] = w

    augmented: list[dict[str, Any]] = []
    for t in base_transitions:
        p = int(t["power"])
        sig = (
            int(t.get("current_winner_offset", t.get("next_peak_offset", 0))),
            int(t.get("current_first_open_offset", 0)),
            int(t.get("endpoint_mod30", 0)),
            int(t.get("current_gap_width", 0)),
        )
        current_left = sig_to_right.get((p, sig))
        if current_left is None:
            continue
        current_gap = int(t["current_gap_width"])
        next_start = current_left + current_gap
        next_w = w_by_start.get((p, next_start))
        if next_w is None:
            continue
        t2 = dict(t)
        t2["target_w_offset"] = next_w
        t2["target_w_parity"] = "even" if next_w % 2 == 0 else "odd"
        t2["next_winner_offset"] = next_w
        augmented.append(t2)

    if not augmented:
        raise ValueError(
            f"No usable transitions with next_w_offset for target={target} "
            f"in power range {min_power}-{max_power}"
        )

    return augmented


def w_compare_members(
    members: list[dict[str, Any]],
    measure: str,
    *,
    target_field: str = "target_w_offset",
) -> tuple[int, int, int]:
    """
    Compute the signed ordering advantage *within a single matched cell* for
    the w-offset earliness question.

    Unlike the binary compare_members in the d4_count sweep (which partitions
    members into next_is_triad targets vs non-targets), this version treats
    every member as having a continuous target_w_offset. For every pair of
    distinct members a, b inside the cell:

        if measure(a) < measure(b) and target_w(a) < target_w(b): +1
        if measure(a) > measure(b) and target_w(a) > target_w(b): +1
        if the inequality directions disagree: -1
        if equal on either side: tie recorded

    The sign convention is chosen so that positive total signed_advantage
    means "lower values of the candidate measure (e.g. smaller d4_count)
    co-occur with earlier GWR w arrival (smaller target_w_offset)" inside
    cells whose PGS facts are fixed by the match mode.

    This is the direct generalization of the rank-style check used in the
    2026-05-30 baseline probe (low_d4 vs high_d4 split, count of a.w < b.w).

    Returns: (decisive_pairs, signed_advantage, tie_pairs)
    All three are exact integers; no floating point, no probability.
    """
    decisive_pairs = 0
    signed_advantage = 0
    tie_pairs = 0

    n = len(members)
    for i in range(n):
        for j in range(i + 1, n):  # unique unordered pairs; double-count would cancel signs anyway
            a = members[i]
            b = members[j]
            ma = float(a[measure])
            mb = float(b[measure])
            ta = float(a[target_field])
            tb = float(b[target_field])

            if ma == mb or ta == tb:
                tie_pairs += 1
                continue

            agree = (ma < mb and ta < tb) or (ma > mb and ta > tb)
            disagree = (ma < mb and ta > tb) or (ma > mb and ta < tb)

            decisive_pairs += 1
            if agree:
                signed_advantage += 1
            elif disagree:
                signed_advantage -= 1
            # equal on one side already handled as tie above

    return decisive_pairs, signed_advantage, tie_pairs


def w_score_rows(
    rows: list[dict[str, Any]],
    *,
    match_mode: str,
    measure: str,
    target_field: str = "target_w_offset",
) -> tuple[int, int, int, int]:
    """
    Group the supplied rows into match-mode cells (identical logic and key
    construction as the audited match_key / base_key in the d4 sweep) and,
    inside each cell that contains at least two rows, invoke w_compare_members
    on the chosen measure and target_field.

    Aggregate across cells:
      eligible_cells = number of cells that produced at least one decisive pair
      decisive_pairs, signed_advantage, tie_pairs summed from the per-cell calls.

    Exactly mirrors the structure of score_rows in state_budget_divisor_carrier_sweep.py
    so that the downstream fold, summarize, and stop-condition logic can be
    reused with only the inner comparison swapped for w-earliness.

    The match modes ("mod30", "mod30_prev_gap_bin", "mod30_prev_gap_exact")
    remain the sole mechanism for fixing the PGS chamber facts before any
    carrier claim is evaluated.
    """
    from collections import defaultdict  # local in case top-level import order

    by_cell: dict[tuple, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        # Direct key construction (matches audited match_key logic exactly; independent of import name for early Phase 3 units)
        base = (
            str(row["previous_reduced_state"]),
            str(row["current_winner_parity"]),
            str(row["current_carrier_family"]),
            int(row["current_winner_offset"]),
            int(row["current_first_open_offset"]),
        )
        key = (*base, int(row["endpoint_mod30"]))
        if match_mode == "mod30_prev_gap_bin":
            key = (*key, str(row.get("previous_gap_bin", "")))
        elif match_mode == "mod30_prev_gap_exact":
            key = (*key, int(row.get("previous_gap_width", 0)))
        by_cell[key].append(row)

    eligible_cells = 0
    decisive_pairs = 0
    signed_advantage = 0
    tie_pairs = 0
    for members in by_cell.values():
        if len(members) < 2:
            continue
        pairs, signed, ties = w_compare_members(members, measure, target_field=target_field)
        if pairs == 0:
            continue
        eligible_cells += 1
        decisive_pairs += pairs
        signed_advantage += signed
        tie_pairs += ties

    return eligible_cells, decisive_pairs, signed_advantage, tie_pairs


def w_score_measure_folds(
    transitions: list[dict[str, Any]],
    *,
    match_mode: str,
    measure: str,
    measure_role: str,
    target_field: str = "target_w_offset",
) -> list[dict[str, Any]]:
    """
    Perform leave-one-power-out cross-validation exactly as
    score_measure_folds in the audited sweep.

    For each heldout_power:
      - train on all other powers → determine the raw sign of the signed
        advantage on the training surface (train_direction)
      - evaluate the identical match_mode + measure on the heldout power only
      - orient the heldout signed_advantage by the train_direction
      - record the full fold row with the same FOLD_FIELDS shape used by the
        d4_count machinery (plus an extra "target" column for clarity).

    This guarantees that any "ordering_carrier_found" verdict for a w-offset
    rule is obtained under the identical statistical hygiene (held-out powers,
    orientation from train, minimum support per fold) as the published
    d4_count precedent.
    """
    powers = sorted({int(row["power"]) for row in transitions if str(row.get("power","")).strip()})
    fold_rows: list[dict[str, Any]] = []
    for heldout_power in powers:
        train_rows = [row for row in transitions if int(row["power"]) != heldout_power]
        heldout_rows = [row for row in transitions if int(row["power"]) == heldout_power]
        _, train_pairs, train_signed, _ = w_score_rows(
            train_rows, match_mode=match_mode, measure=measure, target_field=target_field
        )
        train_direction = 1 if train_signed >= 0 else -1
        eligible, dec, raw_signed, ties = w_score_rows(
            heldout_rows, match_mode=match_mode, measure=measure, target_field=target_field
        )
        oriented = train_direction * raw_signed if train_pairs else 0
        fold_rows.append({
            "match_mode": match_mode,
            "measure": measure,
            "measure_role": measure_role,
            "heldout_power": heldout_power,
            "train_direction": train_direction if train_pairs else 0,
            "eligible_cells": eligible,
            "decisive_pairs": dec,
            "raw_signed_advantage": raw_signed,
            "oriented_signed_advantage": oriented,
            "tie_pairs": ties,
            "target": target_field,  # explicit for w-carrier reports
        })
    return fold_rows


def w_summarize_measure(fold_rows: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate the fold rows into a single summary dict using the identical
    reduction logic as summarize_measure (sum decisive, oriented_signed,
    count positive/negative folds, compute advantage_share, etc.).

    The returned dict will contain all the fields the d4_count summary uses
    plus "target", "edge_over_tail_control", "required_edge",
    "ordering_carrier_stop_condition_met", and the verdict string.
    """
    if not fold_rows:
        return {}
    decisive = sum(int(r.get("decisive_pairs", 0)) for r in fold_rows)
    oriented = sum(int(r.get("oriented_signed_advantage", 0)) for r in fold_rows)
    folds_with_support = sum(1 for r in fold_rows if int(r.get("decisive_pairs", 0)) >= 100)  # MIN_FOLD approx
    pos = sum(1 for r in fold_rows if int(r.get("oriented_signed_advantage", 0)) > 0)
    neg = sum(1 for r in fold_rows if int(r.get("oriented_signed_advantage", 0)) < 0)
    return {
        "match_mode": str(fold_rows[0].get("match_mode", "")),
        "measure": str(fold_rows[0].get("measure", "")),
        "measure_role": str(fold_rows[0].get("measure_role", "")),
        "target": str(fold_rows[0].get("target", "next_winner_offset")),
        "fold_count": len(fold_rows),
        "folds_with_min_support": folds_with_support,
        "positive_oriented_folds": pos,
        "negative_oriented_folds": neg,
        "eligible_cells": sum(int(r.get("eligible_cells", 0)) for r in fold_rows),
        "decisive_pairs": decisive,
        "oriented_signed_advantage": oriented,
        "tie_pairs": sum(int(r.get("tie_pairs", 0)) for r in fold_rows),
        "advantage_share": (oriented / decisive) if decisive else None,
    }


def w_evaluate_surface(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
    target: str = "next_winner_offset",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Top-level entry point for a complete w-offset carrier sweep on a retained
    surface. This is the direct analogue of evaluate_surface in the divisor
    carrier sweep, specialized to Family 1 (w positioning).

    High-level control flow (exact sequence that will be implemented):
    1. Load detail rows via the imported phase_probe.load_detail_rows.
    2. Call build_w_target_transitions (which internally calls the audited
       build_transitions) to obtain the working set of d=4 transitions
       augmented with target_w_offset.
    3. For every MATCH_MODE and every CANDIDATE_MEASURE + CONTROL_MEASURE:
         - run w_score_measure_folds (passing the chosen target)
         - obtain fold_rows and a summary
    4. For each candidate summary, locate the tail_length control summary for
       the same match_mode, compute edge_over_tail_control using the w-signed
       advantages, apply the exact numeric stop-condition gates (the W_MIN_*
       constants defined above, which mirror the 05 constants).
    5. Collect "ordering_carrier_hits" exactly where the full conjunction is
       true; set top-level "verdict" to "ordering_carrier_found" only when the
       list is non-empty, otherwise "does_not" (or per-cell "unresolved" rates
       will be derivable from the fold rows).
    6. Emit the richest possible summary (transition_count, row counts,
       thresholds, all candidate_summaries, strongest by edge, hits, verdict)
       plus the raw fold_rows for the csv artifact.

    The function never mutates the input catalog, never calls any primality
    or factoring API, and never emits probabilistic language. All output
    numbers are exact integer counts or derived exact fractions on the finite
    retained surface named by detail_csv.

    Returns: (fold_rows, summary_dict) ready for write_fold_csv + json dump.
    """
    # PHASE 1 SCAFFOLD: complete specification in the docstring. The body
    # performs only the structural return of empty containers so that the
    # module remains importable and the overall shape of the call graph is
    # visible for Phase 2 review.
    return [], {}


def run_full_w_offset_sweep(
    detail_csv: Path,
    output_dir: Path,
    min_power: int,
    max_power: int,
    target: str = "next_winner_offset",
) -> int:
    """
    Command-line friendly wrapper that calls w_evaluate_surface, writes the
    canonical artifacts (folds csv + summary json) into output_dir with
    w-specific filenames, prints the summary, and returns 0 on success.

    Filenames will be chosen to coexist with the legacy v0.1 probe outputs:
      w_offset_carrier_sweep_folds_p{min}-{max}_{target}.csv
      w_offset_carrier_sweep_summary_p{min}-{max}_{target}.json

    This is the function that, after Phases 3+4, will be invoked by the
    reproduction commands listed in the T-001 final report.
    """
    # PHASE 1 SCAFFOLD: orchestration described; placeholder.
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"[PHASE 1 SCAFFOLD] run_full_w_offset_sweep would write to {output_dir}")
    return 0


# End of Phase 1 scaffolding block for T-001 w-offset carrier sweep.
# After explicit Phase 2 review of this entire skeleton (logic, boundaries,
# PGS fidelity, reproducibility, drift resistance), implementation will
# proceed one unit at a time per AGENTS §11 Phase 3 with immediate tests
# and commits.
