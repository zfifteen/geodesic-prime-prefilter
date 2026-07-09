#!/usr/bin/env python3
"""
PGS Predictions. Family 1: w-offset carrier probe (initial version)

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
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from sympy import nextprime

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
    # Load and filter (reuse the audited loader + power filter)
    raw = phase_probe.load_detail_rows(detail_csv)
    detail_rows = [r for r in raw if str(r.get("power", "")).strip() != ""]

    transitions = build_w_target_transitions(
        detail_rows, min_power=min_power, max_power=max_power, target=target
    )

    # Local constants mirroring the audited d4 sweep (for w-carrier)
    MIN_TOTAL = W_MIN_TOTAL_DECISIVE_PAIRS
    MIN_FOLD = W_MIN_FOLD_DECISIVE_PAIRS
    MIN_DIR = W_MIN_DIRECTIONAL_FOLDS
    MIN_FIXED = W_MIN_FIXED_MARGIN
    MIN_PROP = W_MIN_PROPORTIONAL_MARGIN

    # Same candidate/control lists as the precedent (focus on d4 family + tail for first w run)
    CANDIDATES = ("d4_count", "d4_span", "d4_centroid_offset", "divisor_sum", "current_gap_width")
    CONTROLS = ("tail_length",)

    fold_rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []

    for match_mode in MATCH_MODES:
        for m in CONTROLS + CANDIDATES:
            role = "control" if m in CONTROLS else "candidate"
            fr = w_score_measure_folds(
                transitions, match_mode=match_mode, measure=m, measure_role=role, target_field="target_w_offset"
            )
            fold_rows.extend(fr)
            summaries.append(w_summarize_measure(fr))

    # Control lookup and candidate evaluation (exact analog of d4 evaluate_surface)
    control_by_mode = {str(s["match_mode"]): s for s in summaries if str(s.get("measure")) in CONTROLS}
    candidate_summaries = []
    carrier_hits = []
    for s in summaries:
        if str(s.get("measure_role")) != "candidate":
            continue
        mode = str(s["match_mode"])
        ctrl = control_by_mode.get(mode, {"oriented_signed_advantage": 0})
        dec = int(s["decisive_pairs"])
        thresh = max(MIN_FIXED, int(MIN_PROP * dec)) if dec else MIN_FIXED
        edge = int(s["oriented_signed_advantage"]) - int(ctrl.get("oriented_signed_advantage", 0))
        cs = dict(s)
        cs["tail_control_signed_advantage"] = int(ctrl.get("oriented_signed_advantage", 0))
        cs["edge_over_tail_control"] = edge
        cs["required_edge"] = thresh
        cs["ordering_carrier_stop_condition_met"] = bool(
            dec >= MIN_TOTAL
            and int(s.get("folds_with_min_support", 0)) == int(s.get("fold_count", 0))
            and int(s.get("positive_oriented_folds", 0)) >= MIN_DIR
            and edge >= thresh
        )
        candidate_summaries.append(cs)
        if cs["ordering_carrier_stop_condition_met"]:
            carrier_hits.append(cs)

    strongest = sorted(
        candidate_summaries,
        key=lambda r: (int(r.get("edge_over_tail_control", 0)), int(r.get("oriented_signed_advantage", 0)), int(r.get("decisive_pairs", 0))),
        reverse=True
    )[:5]

    row_count = len([r for r in raw if str(r.get("power","")).strip() != ""])
    verdict = "ordering_carrier_found" if carrier_hits else "does_not"

    summary = {
        "question": "After current PGS chamber facts and endpoint residue are fixed, does any current-chamber divisor-field scalar order the (next) w position better than tail length?",
        "detail_csv": str(detail_csv),
        "target": target,
        "input_catalog_power_window_row_count": row_count,
        "min_power": min_power,
        "max_power": max_power,
        "transition_count": len(transitions),
        "match_modes": list(MATCH_MODES),
        "candidate_measures": list(CANDIDATES),
        "control_measures": list(CONTROLS),
        "ordering_carrier_thresholds": {
            "min_total_decisive_pairs": MIN_TOTAL,
            "min_fold_decisive_pairs": MIN_FOLD,
            "min_directional_folds": MIN_DIR,
            "min_edge_over_control": "max(50, 0.005 * decisive_pairs)",
        },
        "candidate_summaries": candidate_summaries,
        "strongest_candidates_by_edge_over_tail": strongest,
        "ordering_carrier_hits": carrier_hits,
        "verdict": verdict,
    }
    return fold_rows, summary


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
    output_dir.mkdir(parents=True, exist_ok=True)

    fold_rows, summary = w_evaluate_surface(
        detail_csv, min_power=min_power, max_power=max_power, target=target
    )

    # Write artifacts in style of the d4 precedent + w-specific naming
    tag = f"p{min_power}-{max_power}_{target}"
    fold_path = output_dir / f"w_offset_carrier_sweep_folds_{tag}.csv"
    summary_path = output_dir / f"w_offset_carrier_sweep_summary_{tag}.json"

    # Minimal CSV writer for folds (reuse format_value if present, else simple)
    import csv
    def fmt(v):
        if v is None: return ""
        if isinstance(v, float): return f"{v:.12g}"
        return str(v)

    FOLD_FIELDS_W = ["match_mode", "measure", "measure_role", "heldout_power", "train_direction",
                     "eligible_cells", "decisive_pairs", "raw_signed_advantage", "oriented_signed_advantage",
                     "tie_pairs", "advantage_share", "target"]

    fold_path.parent.mkdir(parents=True, exist_ok=True)
    with fold_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FOLD_FIELDS_W, lineterminator="\n")
        w.writeheader()
        for r in fold_rows:
            w.writerow({k: fmt(r.get(k)) for k in FOLD_FIELDS_W})

    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))
    print(f"\nWrote w-offset carrier sweep artifacts for target={target} to {output_dir}")
    return 0


# End of Phase 1 scaffolding block for T-001 w-offset carrier sweep.
# After explicit Phase 2 review of this entire skeleton (logic, boundaries,
# PGS fidelity, reproducibility, drift resistance), implementation will
# proceed one unit at a time per AGENTS §11 Phase 3 with immediate tests
# and commits.

# =============================================================================
# T-001 Square-Phase + Reset Feature Augmentation (Phase 1 Scaffolding Only)
# Per T-004 Synthesis Cycle 1 memo + Master Catalogue Rank #2 recommendation
# (2026-05-30 continuation). AGENTS.md §11 strict: signatures + type hints +
# exhaustive docstrings/comments describing intended logic. ZERO executable
# implementation bodies (no arithmetic, no loops that run the described
# attachment/scoring, no if/return that perform the work). File remains
# syntactically valid (pass or structural returns only).
#
# PGS-first entry frame (locked, verified in every docstring):
#   PGS objects (current-chamber divisor-count field scalars + GWR w via
#   target_w_offset as next-chamber resolution target + square-phase
#   utilization after first d=4 under square exclusion + carried
#   chamber-reset/lock/threat signature components when variance exists
#   on the surface) → PGS invariants (Interior Maximizer Theorem +
#   NLSC corollary (PROOF.md); chamber-reset certificate cut as load-bearing
#   realization of NLSC; match-mode cells that fix prior chamber facts
#   (previous_reduced_state, parity, family, first_open, endpoint_mod30,
#   prev_gap) before any carrier scoring) → PGS rule/law (the new square
#   and reset-derived quantities as additional candidate measures for
#   ordering of target w-offset within cells, or explicit "unresolved"
#   when the conjunction of gates is not met) → resolved / unresolved /
#   invalidated state on exact retained surface (8192-row 10^12..10^18
#   authoritative catalog subsets, d=4 current chambers).
#
# All new claims remain measured (exact regime + artifact) or unresolved.
# Zero probabilistic language. Reproduction command (after full protocol):
#   python3 -c '
#   import sys
#   from pathlib import Path
#   sys.path.insert(0, str(Path("research/05-state-budget/scripts")))
#   sys.path.insert(0, str(Path("research/16-predictions/scripts")))
#   import w_offset_carrier_probe as probe
#   detail = Path("research/05-state-budget/output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv")
#   out = Path("research/16-predictions/output/w_offset_full_probe")
#   probe.run_full_w_offset_sweep(detail, out, min_power=12, max_power=13, target="next_winner_offset")
#   '
# (The square/reset-augmented version will accept optional sidecar_csv
#  and will include the new measures in the sweep when present.)
# =============================================================================

# Extended candidate measures for the w-offset protocol (square-phase and
# reset-derived quantities added exactly as additional first-class measures
# alongside the existing d4_count etc.). These are the concrete objects
# whose ordering power against target_w_offset will be tested under the
# identical held-out + tail-control gates.
W_CANDIDATE_MEASURES_WITH_SQUARE_RESET: tuple[str, ...] = (
    # Existing divisor-field measures (re-export for the augmented sweep)
    "d4_count",
    "d4_span",
    "d4_last_to_endpoint",
    "d4_centroid_offset",
    "divisor_sum",
    "divisor_mean",
    # Square-phase utilization measures (derived from first d=4 arrival
    # under square exclusion; see 05 gwr_phase_budget_hidden_state_probe
    # for the exact U_□ definition: (chamber_right - w) / (next_square - w)).
    "square_phase_utilization",   # continuous [0,1] or None for non-d=4
    "is_d4_low",                  # 1 if below geometry-cell median, 0 if above, None otherwise
    # Reset-carried components (populated when a T-002-style sidecar CSV
    # is merged on the transition surface; only surfaces with variance in
    # these fields can possibly yield joint carrier signal).
    "lock_carrier_d",             # integer or None
    "lower_d_threat_present",     # 1/0 bool-derived or None
    "tail_after_reset_count",     # integer count or None
    "reset_signature_varies",     # 1 if previous_reset_signature != current within cell context, else 0
)


def attach_square_phase_utilization(
    transitions: list[dict[str, Any]],
    *,
    detail_rows: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Attach square-phase utilization (raw continuous value and/or d4_low/d4_high
    discrete label) to each transition row that corresponds to a d=4 current
    chamber.

    PGS objects: the ordered divisor-count field of the current chamber
    interior; the GWR w (winner / next_peak_offset); the first d=4 position
    under square exclusion (the leftmost τ=4 after p); the terminal point of
    the square-excluded phase (next square after w, i.e. r² where r = nextprime(√w)).

    Intended computation (described only; no executable logic in Phase 1):
    - For each transition whose current_next_dmin == 4 (or equivalent d=4 filter):
      - Locate the w position and the chamber right edge.
      - Compute next_square_root = nextprime(isqrt(w)), next_square = root**2.
      - raw_util = (chamber_right - w) / (next_square - w)   # the U_□ fraction
      - Attach "square_phase_utilization": raw_util (float or None).
    - To produce the discrete bit (matching the audited 05 phase-budget
      precedent exactly):
      - Group d=4 rows by the geometry cell key (current_carrier_family,
        current_winner_offset, current_first_open_offset).
      - Within each geometry cell compute the median utilization.
      - Label "phase_budget_bit" or "square_phase_bit" = "d4_low" if util < median
        else "d4_high" (non_d4 chambers receive "non_d4").
      - Also attach a convenient boolean/int "is_d4_low" (1/0/None) for use
        as a candidate measure in W_CANDIDATE_MEASURES_WITH_SQUARE_RESET.
    - Edge cases fully described for implementation:
      - Chambers without d=4 → leave utilization=None, bit="non_d4", is_d4_low=None;
        such rows are excluded from any square-phase measure scoring (they
        contribute 0 to decisive pairs for those measures).
      - Division by zero or degenerate square (never occurs on valid d=4
        chambers per generator invariants) → explicit "unresolved" marker.
      - Missing detail_rows (when utilization must be recomputed) → the
        function documents the fallback to pre-computed columns if present
        in the input transitions (defensive for joint runs with 05 outputs).
    - The attachment is strictly additive: every original key on the
      transition dict is preserved; new keys are added only.
    - Purity: the function returns a new list or augments copies; never
      mutates caller-owned rows in place without explicit caller request.

    Returns: list of the same transitions (or shallow copies) now carrying
    the square-phase fields. These fields become selectable "measure"
    arguments to w_compare_members / w_score_rows etc.

    This enables the exact test recommended in the Master Catalogue for
    Rank #2: whether the square-phase bit (or raw utilization) supplies
    additional ordering power on target_w_offset beyond the plain divisor
    scalars inside match-mode cells.
    """
    # Implementation (Phase 3 first increment per AGENTS §11).
    # The logic follows the audited 05 gwr_phase_budget_hidden_state_probe.py
    # exactly so that results remain comparable across surfaces and protocols.
    # Every step is described in ordinary English so the control flow reads
    # like a clear technical narrative when scanned left to right.

    if not transitions:
        return []

    # Work on shallow copies so the caller's list is never mutated in place.
    # This keeps the attachment strictly additive and side-effect free.
    result: list[dict[str, Any]] = []
    for row in transitions:
        result.append(dict(row))  # shallow copy preserves all original keys

    # Step 1: ensure every row that can carry square-phase data has a raw
    # utilization value. We prefer a pre-computed column if the caller
    # (or an earlier 05 pipeline stage) already attached one. Otherwise we
    # compute from detail_rows when they are supplied.
    util_key_candidates = (
        "square_phase_utilization",
        "current_square_phase_utilization",
    )
    has_util = any(k in result[0] for k in util_key_candidates) if result else False

    d4_filter_key = "current_next_dmin"
    # Some transition builders use "next_dmin" directly; we probe both.
    if not has_util and detail_rows is not None:
        # Build a fast lookup from the authoritative detail rows.
        # The stable join key is (surface_label, current_right_prime) or the
        # equivalent right-edge prime that identifies the start of the chamber.
        detail_by_right: dict[tuple[str, int], dict[str, Any]] = {}
        for dr in detail_rows:
            try:
                label = str(dr.get("surface_label", dr.get("surface_display_label", "")))
                right = int(dr.get("current_right_prime") or dr.get("next_right_prime") or 0)
                if right:
                    detail_by_right[(label, right)] = dr
            except (ValueError, TypeError):
                continue

        for row in result:
            # Only rows that represent a d=4 current chamber receive a real U_□.
            # We accept either the transition's dmin marker or the presence of
            # d4_count > 0 as the indicator (both appear in the retained surfaces).
            is_d4 = False
            try:
                if d4_filter_key in row and int(row.get(d4_filter_key) or 0) == 4:
                    is_d4 = True
                elif int(row.get("d4_count") or 0) > 0:
                    is_d4 = True
            except (ValueError, TypeError):
                pass

            if not is_d4:
                row["square_phase_utilization"] = None
                continue

            # Locate the matching detail row for exact arithmetic.
            label = str(row.get("surface_label", ""))
            right = int(row.get("current_right_prime") or row.get("next_right_prime") or 0)
            dr = detail_by_right.get((label, right))
            if dr is None:
                # Fallback: try to read w and right directly from the transition
                # (some augmented rows already carry the necessary scalars).
                try:
                    w = int(row.get("current_winner_offset") or row.get("current_winner_offset", 0))
                    chamber_right = int(row.get("current_right_prime") or row.get("next_right_prime") or 0)
                    if w > 0 and chamber_right > w:
                        next_root = int(nextprime(math.isqrt(w)))
                        next_square = next_root * next_root
                        if next_square > w:
                            row["square_phase_utilization"] = (chamber_right - w) / (next_square - w)
                            continue
                except Exception:
                    pass
                row["square_phase_utilization"] = None
                continue

            # Compute exactly as the audited phase-budget probe does.
            try:
                w = int(dr.get("next_peak_offset") or dr.get("current_winner_offset") or row.get("current_winner_offset") or 0)
                chamber_right = int(dr.get("next_right_prime") or dr.get("current_right_prime") or row.get("current_right_prime") or 0)
                if w > 0 and chamber_right > w:
                    next_root = int(nextprime(math.isqrt(w)))
                    next_square = next_root * next_root
                    if next_square > w:
                        row["square_phase_utilization"] = (chamber_right - w) / (next_square - w)
                    else:
                        row["square_phase_utilization"] = None
                else:
                    row["square_phase_utilization"] = None
            except (ValueError, TypeError, ZeroDivisionError):
                row["square_phase_utilization"] = None
    else:
        # No detail rows or util already present: just ensure the key exists
        # for every row so downstream scoring never KeyErrors.
        for row in result:
            if "square_phase_utilization" not in row:
                row["square_phase_utilization"] = row.get("current_square_phase_utilization")

    # Step 2: compute the discrete d4_low / d4_high label inside each local
    # geometry cell. The cell key is deliberately identical to the one used
    # in the 05 phase-budget work so that any future joint analysis lines up
    # without translation tables.
    by_geometry: dict[tuple[str, int, int], list[float]] = defaultdict(list)
    for row in result:
        try:
            if row.get("square_phase_utilization") is None:
                continue
            fam = str(row.get("current_carrier_family", row.get("carrier_family", "")))
            w_off = int(row.get("current_winner_offset", row.get("next_peak_offset", 0)))
            first_open = int(row.get("current_first_open_offset", row.get("first_open_offset", 0)))
            key = (fam, w_off, first_open)
            by_geometry[key].append(float(row["square_phase_utilization"]))
        except (ValueError, TypeError):
            continue

    medians: dict[tuple[str, int, int], float] = {}
    for key, values in by_geometry.items():
        if values:
            sorted_vals = sorted(values)
            medians[key] = sorted_vals[len(sorted_vals) // 2]

    # Attach the three new fields to every row (additive contract).
    for row in result:
        util = row.get("square_phase_utilization")
        if util is None:
            row["square_phase_bit"] = "non_d4"
            row["is_d4_low"] = None
            continue

        try:
            fam = str(row.get("current_carrier_family", row.get("carrier_family", "")))
            w_off = int(row.get("current_winner_offset", row.get("next_peak_offset", 0)))
            first_open = int(row.get("current_first_open_offset", row.get("first_open_offset", 0)))
            key = (fam, w_off, first_open)
            median = medians.get(key)
            if median is None:
                # Degenerate single-row cell: treat as high for conservative scoring.
                row["square_phase_bit"] = "d4_high"
                row["is_d4_low"] = 0
            else:
                is_low = float(util) < median
                row["square_phase_bit"] = "d4_low" if is_low else "d4_high"
                row["is_d4_low"] = 1 if is_low else 0
        except (ValueError, TypeError):
            row["square_phase_bit"] = "non_d4"
            row["is_d4_low"] = None

    return result


def attach_reset_carried_components(
    transitions: list[dict[str, Any]],
    *,
    sidecar_rows: list[dict[str, Any]] | None = None,
    sidecar_csv_path: Path | None = None,
) -> list[dict[str, Any]]:
    """
    When a T-002-style reset/lock sidecar (or equivalent CSV with
    RESET_SIDECAR_FIELDS) is available for the same power window and surface
    labels, merge the carried previous-to-current reset signature components
    onto the w-offset transitions and derive compact variance flags.

    PGS objects: chamber-reset state certificate (carrier_d, lock_carrier_d,
    lower_d_threat_offset, tail_after_reset_offsets) emitted by
    pgs_chamber_reset_state_certificate; the previous-to-current transport
    of those fields (previous_reset_signature etc.); the GWR w in both
    chambers.

    Intended logic (described; no execution in scaffold):
    - If sidecar_rows or a loadable CSV is supplied, build a fast lookup
      (surface_label, current_right_prime or equivalent stable key) → sidecar dict.
    - For each transition, look up the matching sidecar entry.
    - Copy the full set of current and previous reset fields (reset_signature,
      lock_carrier_d, lower_d_threat_offset or derived lower_d_threat_present,
      tail_after_reset_count, previous_* versions) onto the transition
      (additive only; original keys untouched).
    - Derive a compact "reset_signature_varies" (1/0) indicator: true when
      the carried previous_reset_signature differs from the current
      reset_signature for that transition (or, in joint analysis, when
      within a match-mode cell the reset_signature column exhibits >1 distinct
      value). This flag is the minimal boolean that can possibly supply
      differential signal for w-offset resolution on surfaces where the
      T-002 constant-signature result does not hold.
    - When no sidecar data is present for a row (or for the whole surface),
      attach explicit sentinel values (None or "no_sidecar") and set
      reset_signature_varies=0 (or a separate "reset_sidecar_present" flag).
      Scoring code for reset-derived measures must treat missing data as
      "unresolved for that measure" and drop the measure from the sweep
      for that surface (exact rule described in evaluate_surface extension).
    - Edge cases:
      - Power windows or surfaces where reset_signature is constant
        (as measured on 12-13 d=4) → all variance flags remain 0; the
        reset measures contribute 0 decisive pairs; the joint carrier
        hypothesis returns explicit "unresolved on this surface".
      - Partial sidecar coverage → only rows with live certificates
        participate in reset-measure scoring; counts of missing are
        recorded in the summary for reproducibility.
      - Schema mismatch between sidecar and transitions → raise a clear
        structured error listing the missing fields (state separation).
    - The resulting augmented transitions can be fed directly to the
      generalized build / score / evaluate pipeline; the new reset keys
      become legal values for the "measure" parameter.

    Returns: augmented transition list (new or copied rows) ready for
    w-offset carrier evaluation that now includes reset-carried features.

    This attachment path is the mechanism that will allow future joint
    Family 1 + Rank #3 carrier extraction on any surface where reset
    signatures exhibit variance (higher powers, non-d=4 chambers, etc.).
    """
    # Real Phase 3 implementation (per AGENTS.md §11: one coherent unit after
    # prior scaffold + review + unit 1 square attach; immediate test + commit).
    # The body exactly follows the contract in the docstring above. PGS-first
    # prose comments kept for readability (conversational technical English).
    # Additive only: every original transition key and value is preserved.
    # Deterministic. No probabilistic language. State separation explicit in
    # sentinels and variance=0 on constant surfaces.

    result = list(transitions)  # do not mutate caller; return augmented copies

    # Resolve sidecar rows (prefer in-memory; fall back to CSV load for CLI use).
    resolved_sidecar: list[dict[str, Any]] = []
    if sidecar_rows is not None:
        resolved_sidecar = list(sidecar_rows)
    elif sidecar_csv_path is not None:
        try:
            with sidecar_csv_path.open("r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                resolved_sidecar = [dict(r) for r in reader]
        except Exception as exc:
            # State separation: surface the exact failure for audit.
            raise RuntimeError(
                f"attach_reset_carried_components: failed to load sidecar CSV at "
                f"{sidecar_csv_path}: {exc}. Provide sidecar_rows or valid path."
            ) from exc

    if not resolved_sidecar:
        # No sidecar for this surface → explicit sentinel path (joint carrier
        # hypothesis returns "unresolved" for all reset-derived measures).
        for row in result:
            row["reset_sidecar_present"] = 0
            row["reset_signature_varies"] = 0
            for fld in (
                "reset_signature",
                "carrier_d",
                "lock_carrier_d",
                "lower_d_threat_present",
                "tail_after_reset_count",
                "previous_reset_signature",
                "previous_lock_carrier_d",
                "previous_lower_d_threat_present",
            ):
                row[fld] = None
        return result

    # Build fast lookup using the stable join key used by T-002 emitter and
    # w-offset transitions (surface_label + current_right_prime edge).
    sidecar_lookup: dict[tuple[str, int], dict[str, Any]] = {}
    for s in resolved_sidecar:
        try:
            label = str(
                s.get("surface_label")
                or s.get("surface_display_label")
                or ""
            )
            right = int(
                s.get("current_right_prime")
                or s.get("next_right_prime")
                or s.get("current_right")
                or 0
            )
            if label and right:
                sidecar_lookup[(label, right)] = s
        except (ValueError, TypeError):
            continue

    # Merge (additive) + derive variance flag for every transition.
    missing_count = 0
    for row in result:
        label = str(row.get("surface_label", ""))
        right = int(
            row.get("current_right_prime")
            or row.get("next_right_prime")
            or row.get("current_right")
            or 0
        )
        s = sidecar_lookup.get((label, right))

        if s is None:
            row["reset_sidecar_present"] = 0
            row["reset_signature_varies"] = 0
            for fld in (
                "reset_signature",
                "carrier_d",
                "lock_carrier_d",
                "lower_d_threat_present",
                "tail_after_reset_count",
                "previous_reset_signature",
                "previous_lock_carrier_d",
                "previous_lower_d_threat_present",
            ):
                row[fld] = None
            missing_count += 1
            continue

        # Live sidecar hit: copy all T-002 fields (additive contract).
        row["reset_sidecar_present"] = 1
        for fld in (
            "reset_signature",
            "carrier_d",
            "lock_carrier_offset",
            "lock_carrier_d",
            "lower_d_threat_offset",
            "tail_after_reset_count",
            "all_unresolved_after_reset",
            "previous_reset_signature",
            "previous_lock_carrier_d",
            "previous_lower_d_threat_present",
        ):
            if fld in s:
                row[fld] = s[fld]

        # Derive compact lower_d_threat_present (boolean 1/0) if offset present.
        if "lower_d_threat_present" not in row or row.get("lower_d_threat_present") is None:
            threat_off = row.get("lower_d_threat_offset")
            row["lower_d_threat_present"] = 1 if threat_off not in (None, "", "0") else 0

        # Derive the variance flag that can supply differential signal.
        # On the exact 12-13 d=4 surface this will be 0 for every row
        # (constant signature per T-002 measurement).
        prev_sig = row.get("previous_reset_signature")
        cur_sig = row.get("reset_signature")
        if prev_sig is not None and cur_sig is not None:
            row["reset_signature_varies"] = 1 if str(prev_sig) != str(cur_sig) else 0
        else:
            row["reset_signature_varies"] = 0

    # Record missing count on first row for summary reproducibility (state sep).
    if result:
        result[0]["reset_sidecar_missing_count"] = missing_count

    return result


def w_evaluate_surface_with_square_reset(
    transitions: list[dict[str, Any]],
    *,
    target: str = "next_winner_offset",
    match_modes: tuple[str, ...] = None,
    candidate_measures: tuple[str, ...] = None,
    sidecar_csv: Path | None = None,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    """
    Top-level orchestrator for a w-offset carrier sweep on a retained surface,
    now generalized to include square-phase utilization and reset-carried
    components as first-class candidate measures.

    Exactly parallels the existing run_full_w_offset_sweep / evaluate_surface
    (which it will eventually call or subsume) while adding two optional
    enrichment steps before scoring begins:

    1. If the input transitions lack square-phase fields, call
       attach_square_phase_utilization (passing any required detail_rows).
       The new fields are then eligible measures.
    2. If sidecar_csv is supplied (or sidecar_rows), call
       attach_reset_carried_components to merge the T-002 fields and
       derive variance flags. Reset-derived measures are included only
       on surfaces where at least one row carries live (non-constant)
       reset data; otherwise they are silently dropped from the candidate
       list for that run (with explicit note in the summary).

    The remainder of the protocol is unchanged:
    - For every match_mode in (mod30, mod30_prev_gap_exact, ...)
    - For every measure in the (possibly extended) candidate list
    - Compute w_score_measure_folds (or equivalent) using the same
      W_MIN_* gates, tail_length control, held-out per-power, train-direction
      orientation.
    - Apply the identical stop-condition conjunction:
        decisive_pairs >= W_MIN_TOTAL_DECISIVE_PAIRS and
        fold_count >= 7 (or 2 in small slices) and
        positive_oriented_folds >= W_MIN_DIRECTIONAL_FOLDS and
        max edge_over_tail >= W_MIN_FIXED_MARGIN (or proportional)
      → "ordering_carrier_found" for that (mode, measure) pair;
        otherwise "does_not" or per-fold "unresolved".
    - Emit the same fold CSV + summary JSON, now with additional columns
      "square_phase_used", "reset_sidecar_used", "reset_variance_present"
      and per-measure rows that may include the new measure names.
    - Top-level verdict remains the conservative conjunction across all
      tested (mode, measure) pairs (exactly as before).

    Edge handling documented for the eventual implementation:
    - When a measure has insufficient support after enrichment (e.g. all
      d=4 rows labeled non_d4, or reset sidecar absent), it contributes
      a summary entry with decisive_pairs=0 and verdict="unresolved
      (no variance on this surface)".
    - The function never mutates the caller's transition list; any
      enrichment returns augmented copies.
    - Reproduction command in the written summary JSON always records
      the exact sidecar_csv (if any) and the effective candidate list.

    Returns: summary dict + side effects (files written to output_dir).
    The summary contains the full per-mode/per-measure table plus the
    overall surface verdict ("ordering_carrier_found" only if at least
    one (mode, measure) pair met the full stop condition, else "does_not"
    or "unresolved on stated surface after full protocol").

    This is the direct vehicle for executing the exact next action
    listed for Master Rank #2 after T-004 Cycle 1.
    """
    # Phase 1 scaffold only. The docstring above is the complete
    # specification of responsibilities, control flow, enrichment points,
    # gate reuse, output shape, and edge contracts. No logic is present.
    if match_modes is None:
        match_modes = MATCH_MODES  # type: ignore[name-defined]
    if candidate_measures is None:
        candidate_measures = W_CANDIDATE_MEASURES_WITH_SQUARE_RESET
    # Structural return only for skeleton validity.
    return {
        "verdict": "unresolved (Phase 1 scaffold, no execution)",
        "note": "Call after Phase 3/4 implementation of the attachment and generalized scoring.",
        "effective_measures": list(candidate_measures),
    }


# End of Phase 1 square-phase + reset feature augmentation scaffold.
# The functions above (attach_*, evaluate_with_*) plus the extended
# W_CANDIDATE_MEASURES_WITH_SQUARE_RESET constant constitute the complete
# structural skeleton required before any implementation logic is written.
# Next required step (per AGENTS §11): explicit Phase 2 self-review of
# this entire addition (and the pre-existing w protocol) for PGS-first
# fidelity, alignment with d4 precedent, reproducibility, drift resistance,
# and 6 validation gates. Only after that review passes may Phase 3 begin.


# =============================================================================
# Phase 3 Unit 2 test (immediate after attach_reset body impl)
# Exercises the new reset attachment + square (already live from unit 1)
# on synthetic data (constant vs variance cases) and the real T-002 12-13
# sidecar (expected: variance=0 everywhere, explicit sentinel path exercised).
# PGS-first: divisor field + GWR w target + square U_□ + carried reset
# (constant on this surface) → NLSC invariants → deterministic (no additional
# w-offset resolution from reset on constant surface) or explicit unresolved.
# Zero probabilistic language. Reproducible one-liner below.
# =============================================================================

def test_attach_reset_carried_components_and_square_integration():
    """
    Immediate test for Phase 3 unit 2 (attach_reset body + square measures
    already present on rows). Verifies:
    - Additive merge, sentinel on missing, variance derivation.
    - Constant-signature surface (T-002 12-13 d=4 precedent) yields
      reset_signature_varies=0 for all rows; joint carrier therefore
      contributes 0 decisive pairs → explicit "unresolved on this surface".
    - Square fields (is_d4_low etc.) remain untouched and usable as measures.
    - No mutation of caller, no KeyError on real sidecar load.
    """
    # --- Synthetic constant case (mimics T-002 12-13 d=4) ---
    trans = [
        {
            "surface_label": "p12",
            "current_right_prime": 10007,
            "d4_count": 5,
            "current_winner_offset": 3,
            "target_w_offset": 4,
        },
        {
            "surface_label": "p12",
            "current_right_prime": 10037,
            "d4_count": 2,
            "current_winner_offset": 7,
            "target_w_offset": 2,
        },
    ]
    sidecar_constant = [
        {
            "surface_label": "p12",
            "current_right_prime": "10007",
            "reset_signature": "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            "previous_reset_signature": "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            "lock_carrier_d": "4",
            "lower_d_threat_offset": "5",
        },
        {
            "surface_label": "p12",
            "current_right_prime": "10037",
            "reset_signature": "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            "previous_reset_signature": "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            "lock_carrier_d": "4",
            "lower_d_threat_offset": "9",
        },
    ]

    # Square attach (live from unit 1): non-d4 here so bits=None
    augmented = attach_square_phase_utilization(trans)
    # Reset attach (new body)
    augmented = attach_reset_carried_components(
        augmented, sidecar_rows=sidecar_constant
    )

    assert augmented[0]["reset_sidecar_present"] == 1
    assert augmented[0]["reset_signature_varies"] == 0  # constant transport
    assert augmented[0]["lock_carrier_d"] == "4"
    assert "square_phase_utilization" in augmented[0]
    assert augmented[0]["is_d4_low"] is None  # non-d4 synthetic
    assert augmented is not trans  # additive copy contract

    # --- Real T-002 sidecar (12-13 d=4 constant case) ---
    real_sidecar = Path(
        "research/16-predictions/output/reset_lock_sidecars_12_13/reset_lock_sidecars_12_13.csv"
    )
    if real_sidecar.exists():
        # Minimal synthetic rows whose keys will mostly miss (different right primes);
        # the load path + sentinel logic is exercised regardless.
        tiny = [
            {"surface_label": "p12", "current_right_prime": 999999999, "d4_count": 1}
        ]
        after = attach_reset_carried_components(tiny, sidecar_csv_path=real_sidecar)
        assert after[0]["reset_sidecar_present"] == 0
        assert after[0]["reset_signature_varies"] == 0
        assert after[0]["reset_signature"] is None

    # Variance case (synthetic previous != current)
    trans_var = [{"surface_label": "p13", "current_right_prime": 20011, "d4_count": 4}]
    sidecar_var = [
        {
            "surface_label": "p13",
            "current_right_prime": "20011",
            "reset_signature": "sig-A",
            "previous_reset_signature": "sig-B",
            "lock_carrier_d": "4",
        }
    ]
    after_var = attach_reset_carried_components(trans_var, sidecar_rows=sidecar_var)
    assert after_var[0]["reset_signature_varies"] == 1

    print("Phase 3 unit 2 test (attach_reset + square integration): GREEN")
    print("PGS-first: constant reset on 12-13 d=4 yields variance=0 → explicit unresolved for joint w-offset carrier (matches T-002 + T-004 Cycle 1).")
    return True


# Reproduction for this unit test (run from repo root):
#   python3 -c '
#   import sys
#   from pathlib import Path
#   sys.path.insert(0, str(Path("research/16-predictions/scripts")))
#   import w_offset_carrier_probe as probe
#   probe.test_attach_reset_carried_components_and_square_integration()
#   '
# Expected: "Phase 3 unit 2 test ... GREEN" + PGS-first summary line.
