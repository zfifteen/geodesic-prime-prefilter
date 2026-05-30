#!/usr/bin/env python3
"""
PGS Predictions — T-002: Chamber-Reset Signature + Lock Transport Sidecar Emitter (Agent B)

This script emits richer reset-signature, lock_carrier, lower_d_threat, and related
sidecars onto the existing 8192-row retained catalog surface (10^12..10^18) without
mutating the authoritative catalog builders.

PGS-First Entry Point (per all governing contracts):
  PGS objects (ordered chamber after p, divisor-count field, GWR carrier_w,
  lock_carrier from first resolved-survivor that captured a carrier, lower_d_threat
  as first post-lock d-strictly-between, tail_after_reset_offsets, carried
  previous-chamber reset state) → PGS invariants (Interior Maximizer + NLSC
  proved base; load-bearing carrier/lock/threat cut in every chamber reset) →
  deterministic carrier hypothesis for next-chamber reset or boundary behavior →
  resolved / unresolved / invalidated state on exact retained surface.

Strict constraints observed at every step:
- Deterministic language only. No "likely", "on average", probabilistic, or heuristic framing.
- State separation: every output row and every claim in downstream analysis carries
  explicit epistemic label (measured on regime X, hypothesis, unresolved).
- Sidecar-only: this script never writes to ch03 or ch05 retained artifacts.
- All inference begins from the named PGS objects above; the generator certificate
  function is the sole source of reset/lock fields.
- Reproduction must be a short, one-command sequence.

Design modeled directly on the audited transition logic in
research/05-state-budget/scripts/state_budget_divisor_carrier_sweep.py and the
Family-1 probe in research/16-predictions/scripts/w_offset_carrier_probe.py for
maximum reuse and hygiene.

Phase authoring note: This file was created under the mandatory 4-phase procedure
(AGENTS.md §11). The current content is Phase-1 scaffolding only.

Reproduction (after full implementation):
  python3 research/16-predictions/scripts/reset_lock_transport_sidecar_emitter.py \
    --detail-csv research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv \
    --min-power 12 --max-power 13 \
    --output-dir research/16-predictions/output/reset_lock_sidecars_12_13

  # Then a tiny analysis pass (or built-in --analyze) will be added in later increments.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ----------------------------------------------------------------------------
# Path hygiene — identical pattern to audited w_offset and divisor-carrier probes.
# We import only the generator certificate (PGS-native) and the transition
# builder helpers (already validated on the exact surface we are enriching).
# ----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[2]

# Make 05-state-budget scripts and the PGS generator importable.
# This is deliberate reuse, not duplication.
sys.path.insert(0, str(ROOT / "research" / "05-state-budget" / "scripts"))
sys.path.insert(0, str(ROOT / "src" / "python"))

import gwr_phase_budget_hidden_state_probe as phase_probe  # type: ignore[import]
from state_budget_divisor_carrier_sweep import (  # type: ignore[attr-defined]
    build_transitions,
    previous_gap_bin,
    MATCH_MODES,
)

# The single PGS-native source of truth for all chamber-reset sidecar fields.
# We import only this; we never call legacy predictor paths or classical APIs.
from z_band_prime_predictor.simple_pgs_generator import (
    pgs_chamber_reset_state_certificate,
)

# Match the generator default so certificate calls are identical to production
# chamber-reset behavior on the retained surfaces.
DEFAULT_CANDIDATE_BOUND: int = 128

# ----------------------------------------------------------------------------
# Output schema (sidecar columns that will be attached).
# These names are chosen to read as clear technical English when scanned.
# All are derived deterministically from the certificate or from consecutive
# chamber linking (previous-to-current transport).
# ----------------------------------------------------------------------------

RESET_SIDECAR_FIELDS: Tuple[str, ...] = (
    "reset_signature",                 # Compact deterministic encoding, e.g. "carrier_d=4;lock_carrier_d=4;lower_d_threat_present=False;tail_after_reset_count=2"
    "carrier_d",                       # From certificate (first min-d>2 after p)
    "lock_carrier_offset",
    "lock_carrier_d",
    "lower_d_threat_offset",           # None or integer; presence is itself a carrier bit
    "tail_after_reset_count",
    "all_unresolved_after_reset",      # bool from certificate
    "previous_reset_signature",        # Carried from the immediately preceding chamber (transport)
    "previous_lock_carrier_d",
    "previous_lower_d_threat_present",
)

# ----------------------------------------------------------------------------
# Function: build_reset_signature
# Responsibility (scaffolding description only):
#   Given a fully populated chamber-reset certificate dict (or None for unresolved
#   chambers), return a single compact, deterministic, human-auditable string that
#   encodes the load-bearing reset/lock/threat/tail policy components. The encoding
#   must be stable across runs, contain only exact integer or boolean values from
#   the certificate, and contain no derived statistics.
#
#   When certificate is None the function must return the explicit string
#   "unresolved" so that downstream carrier logic can treat it as a first-class
#   unresolved state (per Predictions contract definition).
#
#   Edge cases documented here for later implementation:
#   - Missing keys inside certificate → treat as unresolved for that component.
#   - tail_after_reset_offsets may be empty list → count 0, policy "no_tail".
#   - lower_d_threat_offset may legitimately be None (no threat activated).
#
#   This string becomes the primary "reset_signature" carrier object for
#   hypothesis formulation in T-002.
# ----------------------------------------------------------------------------
def build_reset_signature(certificate: Optional[Dict[str, Any]]) -> str:
    """Return compact deterministic reset/lock/threat signature string or 'unresolved'."""
    if certificate is None:
        return "unresolved"

    # Extract the four load-bearing components exactly as emitted by the generator
    # certificate (see simple_pgs_generator.py:140-146). All values are already
    # integers or None; we perform no further computation.
    carrier_d = certificate.get("carrier_d")
    lock_carrier_d = certificate.get("lock_carrier_d")
    lower_d_threat_offset = certificate.get("lower_d_threat_offset")
    tail_offsets = certificate.get("tail_after_reset_offsets", [])

    # Presence of threat is a pure boolean derived only from the offset being non-None.
    # This is the same test the generator itself uses for final_status decisions.
    lower_d_threat_present = lower_d_threat_offset is not None

    # Tail length is the exact count of unresolved offsets after the reset point.
    # This is the policy-relevant quantity for next-chamber boundary hypotheses.
    tail_count = len(tail_offsets) if isinstance(tail_offsets, (list, tuple)) else 0

    # Guard against any partially-populated certificate row (state-separation hygiene).
    if carrier_d is None or lock_carrier_d is None:
        return "unresolved"

    # Produce the stable, auditable, four-component encoding.
    # Order is fixed: carrier_d;lock_carrier_d;threat_present;tail_count.
    # No whitespace, no extra fields, no floating-point.
    return (
        f"carrier_d={int(carrier_d)};"
        f"lock_carrier_d={int(lock_carrier_d)};"
        f"lower_d_threat_present={lower_d_threat_present};"
        f"tail_after_reset_count={tail_count}"
    )


# ----------------------------------------------------------------------------
# Function: extract_p_from_detail_row
# Responsibility (scaffolding):
#   Given one row from the authoritative gap-type details CSV, return the integer
#   left endpoint p of the current chamber (the value that will be fed to the
#   generator certificate function). Must handle both the "current_right_prime"
#   naming used in transition construction and the raw row shape.
#
#   Must raise an explicit, descriptive error on missing or non-integer data so
#   that any catalog shape drift is caught immediately (state-separation hygiene).
# ----------------------------------------------------------------------------
def extract_p_from_detail_row(row: Dict[str, Any]) -> int:
    """Return the integer left prime p that opens the chamber described by row."""
    # Preferred key coming from the transition builder and the 03-gap-type rows.
    for key in ("current_right_prime", "left_prime", "p"):
        if key in row:
            try:
                value = int(row[key])
                if value > 1:
                    return value
            except (TypeError, ValueError):
                pass

    # Fallback: some raw detail rows use different naming for the left edge.
    for key in ("current_left_prime", "right_prime_of_previous"):
        if key in row:
            try:
                value = int(row[key])
                if value > 1:
                    return value
            except (TypeError, ValueError):
                pass

    # Explicit failure with context for catalog-drift detection (state separation).
    sample = {k: row.get(k) for k in list(row.keys())[:6]}
    raise ValueError(
        f"extract_p_from_detail_row: could not locate integer left-prime p in row. "
        f"Keys present (first 6): {list(row.keys())[:6]}. Sample: {sample}"
    )


# ----------------------------------------------------------------------------
# Function: augment_transitions_with_reset_sidecars
# Responsibility (scaffolding — the core of T-002):
#   Take the list of transition dicts already produced by the audited
#   build_transitions(...) (which gives us previous/current/next linking under
#   the exact match-mode discipline), and for each transition:
#
#     - Extract p for the *current* chamber.
#     - Call pgs_chamber_reset_state_certificate(p) → obtain the native PGS
#       certificate containing carrier/lock/threat/tail fields.
#     - Build the current reset_signature via the helper above.
#     - Look back one transition (if present) to obtain the carried
#       previous_reset_signature / previous_lock_carrier_d / previous threat bit.
#       This is the explicit previous-to-current transport carrier surface.
#     - Attach all RESET_SIDECAR_FIELDS as new keys on the transition dict.
#     - Preserve every original key (full state separation — the enrichment is
#       strictly additive).
#
#   The resulting augmented list is the exact artifact on which the first
#   reset/lock transport carrier hypothesis will be measured.
#
#   Must document (in comments) the precise point at which an "unresolved"
#   certificate produces an explicit unresolved sidecar value rather than
#   inventing data.
#
#   Must never mutate the input list in place (immutability for auditability).
# ----------------------------------------------------------------------------
def augment_transitions_with_reset_sidecars(
    base_transitions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Return a new list of transitions, each augmented with the full set of
    reset/lock/threat transport sidecars plus carried previous-chamber state.
    """
    # SCAFFOLDING ONLY — detailed control-flow description:
    #   1. Create an empty result list.
    #   2. For i, trans in enumerate(base_transitions):
    #        a. p = extract_p_from_detail_row(...)  (current chamber left edge)
    #        b. cert = pgs_chamber_reset_state_certificate(p, candidate_bound=DEFAULT...)
    #        c. current_sig = build_reset_signature(cert)
    #        d. If i > 0: previous_sig = ... from result[i-1] (already augmented)
    #           else: previous_sig = "no_previous_chamber"
    #        e. Build a fresh dict that copies trans + all new sidecar keys.
    #        f. Append the fresh dict.
    #   3. Return the new list.
    #
    # All certificate calls happen here; this is the single controlled surface
    # that brings the richer fields (already present in the generator and in the
    # C header) into the Predictions retained-surface protocol.
    #
    # Edge: when the generator returns None inside a d=4 transition row, we still
    # emit the sidecar row with explicit "unresolved" so the carrier hypothesis
    # can count unresolved rate exactly (contract requirement).
    raise NotImplementedError("Phase-1 scaffolding: implementation forbidden until Phase 3")


# ----------------------------------------------------------------------------
# Function: write_enriched_csv
# Responsibility (scaffolding):
#   Given the augmented transition list and an output path, write a CSV whose
#   columns are the original transition columns followed by RESET_SIDECAR_FIELDS
#   in the declared order. Must use UTF-8, LF endings, and quote only when
#   necessary. Must create parent directories.
#
#   The header row must be written exactly once; every subsequent row must
#   contain values for all declared sidecar columns (empty string only for truly
#   missing previous-chamber data on the very first row of a surface).
# ----------------------------------------------------------------------------
def write_enriched_csv(path: Path, augmented_rows: List[Dict[str, Any]]) -> None:
    """Write the sidecar-enriched transitions to CSV (sidecar columns appended)."""
    # SCAFFOLDING ONLY
    # Future implementation will:
    #   - Determine full field list = list(augmented_rows[0].keys()) preserving order
    #     with sidecar fields guaranteed at the end.
    #   - Open path with newline="\n", write DictWriter.
    #   - For each row emit format_value (None → "", float pretty, else str).
    #   - mkdir parents, atomic write where easy.
    raise NotImplementedError("Phase-1 scaffolding: implementation forbidden until Phase 3")


# ----------------------------------------------------------------------------
# Function: write_summary_json
# Responsibility (scaffolding):
#   Emit a small machine-readable summary alongside the CSV: input window,
#   number of transitions processed, number of chambers that produced a live
#   certificate vs explicit unresolved, basic counts of lock_carrier_d values,
#   lower_d_threat presence rate, etc. All numbers exact. No derived statistics
#   that would imply a model.
#
#   This summary becomes part of the reproducible artifact for the report.
# ----------------------------------------------------------------------------
def write_summary_json(path: Path, summary_payload: Dict[str, Any]) -> None:
    """Write exact counts and surface metadata for the emitted sidecar run."""
    # SCAFFOLDING ONLY
    raise NotImplementedError("Phase-1 scaffolding: implementation forbidden until Phase 3")


# ----------------------------------------------------------------------------
# CLI & main
# Responsibility (scaffolding):
#   Parse --detail-csv, --min-power, --max-power, --output-dir exactly as the
#   sibling w_offset probe and the divisor-carrier sweep do.
#   Load the raw detail rows using the audited phase_probe loader.
#   Call build_transitions (reused).
#   Call the new augment function.
#   Write CSV + summary JSON into the requested output dir.
#   Print the reproduction command and the summary path to stdout.
#
#   Must support the same power windows used in the d4_count precedent so that
#   any future joint carrier (d4_count + reset_signature) can be measured on
#   identical cells.
# ----------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    """Return the argument parser for the T-002 sidecar emitter."""
    parser = argparse.ArgumentParser(
        description=(
            "Emit chamber-reset signature, lock_carrier, lower_d_threat and "
            "previous-to-current transport sidecars on the retained 8192-row surface."
        )
    )
    parser.add_argument(
        "--detail-csv",
        type=Path,
        default=ROOT / "research" / "03-gap-types" / "output" / "gwr_dni_gap_type_catalog_details.csv",
        help="Source detail catalog (authoritative 8192-row surface).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "research" / "16-predictions" / "output",
        help="Directory that will receive the enriched CSV and summary JSON.",
    )
    parser.add_argument("--min-power", type=int, default=12)
    parser.add_argument("--max-power", type=int, default=13)
    return parser


def main(argv: List[str] | None = None) -> int:
    """Entry point. Orchestrates load → augment → write for T-002 sidecars."""
    # SCAFFOLDING ONLY — high-level English description of future control flow:
    #   1. Parse args.
    #   2. Ensure output_dir exists.
    #   3. Load raw detail rows (phase_probe.load_detail_rows).
    #   4. Build base transitions using the exact audited helper (build_transitions).
    #   5. Augment with reset/lock/transport sidecars (the new function).
    #   6. Write CSV + summary.
    #   7. Print one-line reproduction + artifact locations.
    #   8. Return 0 on success.
    #
    # Every step after 4 is new code for T-002; each will be implemented and
    # tested in its own Phase-3 increment with its own commit.
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # The following lines are placeholders only; real bodies arrive in Phase 3.
    print("[T-002] Phase-1 skeleton executing — no sidecar data produced yet.")
    print(f"[T-002] Would process {args.min_power}..{args.max_power} on {args.detail_csv}")
    print(f"[T-002] Artifacts would land in {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())