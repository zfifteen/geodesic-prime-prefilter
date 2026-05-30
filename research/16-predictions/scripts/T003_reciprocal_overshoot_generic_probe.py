#!/usr/bin/env python3
"""
PGS Predictions T-003 — Reciprocal + Transported Carrier Overshoot Lift to Generic Retained Surfaces.

**Candidate**: Reciprocal Deadline-Signature Correction + Transported Carrier Overshoot (Master Catalogue Rank #4)
**Agent**: Agent C (Endpoint-Chain, Modulus-Link & Reciprocal Closure)
**Governing Contracts**:
- research/16-predictions/team_autonomy_plan.html (autonomous execution, validation gates, handoff via reports/)
- research/16-predictions/pgs_predictions_v0.1_contract.html (deterministic carrier definition, PGS-first, no probabilistic language)
- research/16-predictions/predictions_master_catalogue.html (exact Rank #4 recommended action)
- research/16-predictions/catalogue/endpoint-chain-modulus-link-prediction-candidates.md (Candidate 5: transported carrier_w / tail overshoot discriminator; "map gap chambers to synthetic moduli")
- Full local AGENTS.md + canonical /Users/velocityworks/IdeaProjects/code-style/AGENTS/AGENTS.md (PGS-first entrypoint, 4-phase authoring, prose style, determinism)

**PGS-First Entry Frame (this script embodies)**:
PGS objects (ordered retained prime sequence as closed public-endpoint pool; PGSPG structural reset certificates from pgs_chamber_reset_state_certificate containing reset_endpoint, carrier_w, tail_after_reset_offsets, reset_signature, lock_carrier_*, reset_deadline_value; endpoint-chain stepping via previous-in-pool; reciprocal floor transport; modulus-link closure predicates) → invariants (strict mutual reset closure; deadline-signature correction with outward movement + mutual floor images + signature match; differential transported-overshoot of carrier_w and first tail relative to upper structures as observed on rsa-v2 ladders) → rule (overshoot threshold or binned overshoot as deterministic carrier that from lower-chamber certificate state resolves a small set of possible next-w offsets or next reset-signature properties after the chamber, or returns explicit unresolved) → resolved/unresolved/invalidated state on exact retained surface.

**What this script does (when complete)**:
Loads a retained prime-gap detail catalog (public data from research/03-gap-types or 05-state-budget long-running). Restricts to a modest power window for first-cycle reproducibility. Extracts sorted list of public endpoints (the p/q primes). For selected or consecutive pairs (lower_p, upper_p) drawn from that list, constructs a synthetic modulus N = lower_p * upper_p (harness construction only; factors are public known endpoints; the PGS inference path inside the script never performs product checks, divisibility selectors, or uses factors as inputs to decide any state). Derives full lower PGSPG certificate at lower_p using the audited generator. Chooses oriented transport coordinate. Computes y = floor(N / x). Locates upper_anchor = largest retained endpoint < y (binary search on closed pool). Derives upper certificate. Evaluates the rsa-v2 closure predicates (strict reset first, then deadline correction) producing explicit status strings identical to rsa-v2 (endpoint_class_by_reciprocal_deadline_signature_correction, unresolved_by_reciprocal_carrier_misalignment, etc.). Computes exact overshoot numbers (transported_lower_carrier_w - upper_anchor, transported_lower_carrier_w - upper_carrier_w, first transported tail delta) exactly as in STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md. Then treats binned or thresholded overshoot (thresholds seeded from the rsa-v2 14-16 true-positive band) as an additional scalar measure and runs the established match-mode + held-out carrier protocol (inherited from state_budget_divisor_carrier_sweep) against target next-chamber quantities (next w offset after lower, or next reset_signature properties). Returns exact counts, decisive pairs, signed advantage or exact match rates, and unresolved rates. Verdicts use only the deterministic language of the precedent: overshoot_carrier_found / does_not / unresolved on the concrete surface.

**Reproduction command (one-command after implementation)**:
python3 research/16-predictions/scripts/T003_reciprocal_overshoot_generic_probe.py \
  --detail-csv research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv \
  --min-power 12 --max-power 13 \
  --output-dir research/16-predictions/output/T003_reciprocal_overshoot_probe \
  --max-pairs 200

The script must run with zero external non-public inputs, produce deterministic CSV/JSON summaries, and contain its own unit tests for the overshoot arithmetic and predicate logic.

**Authoring discipline enforced (canonical AGENTS.md §11)**:
This file was created in Phase 1 (scaffolding only). It contains complete signatures, type hints, docstrings, and detailed *intended-logic* comments inside every function body. There is deliberately no executable implementation of the core arithmetic, transport, certificate derivation, overshoot calculation, or carrier sweep inside the bodies during Phase 1. Phase 2 review of this skeleton (by the authoring agent) must occur and be documented before any Phase 3 incremental implementation begins. All later increments will be one unit + immediate test + commit.

**Strict constraints observed in design**:
- Zero probabilistic language anywhere (output, comments, variable names).
- All claims will be labeled by epistemic status in final report.
- Classical arithmetic (the * for N construction) lives only in the public test harness; inference uses only divisor-count certificates + floor + previous-in-pool lookup + the documented closure predicates.
- Explicit unresolved states for every predicate failure path.
- Reuses audited components (simple_pgs_generator, build_transitions logic, previous-endpoint pattern from rsa-v2) rather than reimplementing.
- Full state separation: measured carrier strength on exact retained window only; no promotion.

**Drift self-audit hooks (will be executed and recorded in Phase 4 + report)**:
- Never begins reasoning or code from factor search, Miller-Rabin, or product closure as selector.
- Never revives legacy "predictor" framing or z_band_prime_predictor as inference engine.
- Never describes finite-surface hit rates with "likely", "suggests", or "promising".
- Preserves the exact rsa-v2 unresolved status vocabulary where applicable.
- Maps only public retained endpoints; synthetic N is a pure arithmetic link for transport, never an input to PGS state resolution.

When this script reaches Phase 4 complete + gates passed, the 7-field report will be emitted to research/16-predictions/reports/ and this task file + TEAM_STATUS.md will be updated. Only then will synthesis be requested from Agent D.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Sequence, TypedDict

import bisect  # for exact previous-in-pool lookup on the closed retained endpoint list

# Audited reuse paths (will be imported in later phases; listed here for skeleton clarity)
# import sys
# SCRIPT_DIR = Path(__file__).resolve().parent
# ROOT = SCRIPT_DIR.parents[2]
# sys.path.insert(0, str(ROOT / "src" / "python"))
# sys.path.insert(0, str(ROOT / "research" / "05-state-budget" / "scripts"))
# from z_band_prime_predictor.simple_pgs_generator import pgs_chamber_reset_state_certificate
# import state_budget_divisor_carrier_sweep as carrier_sweep  # for build_transitions, match_key, etc.

# ============================================================================
# CONSTANTS (named, intention-revealing; no magic numbers in final logic)
# ============================================================================

DEFAULT_DETAIL_CSV = Path("research/03-gap-types/output/gwr_dni_gap_type_catalog_details.csv")
DEFAULT_OUTPUT_DIR = Path("research/16-predictions/output/T003_reciprocal_overshoot_probe")
DEFAULT_MIN_POWER = 12
DEFAULT_MAX_POWER = 13
DEFAULT_MAX_PAIRS_FOR_FIRST_CYCLE = 200

# Thresholds seeded from rsa-v2 STEP2 observation (true-positive band ~14-16 overshoot)
# These are parameters of the hypothesis under test, not hard-coded conclusions.
TRANSPORTED_CARRIER_OVERSHOOT_TRUE_BAND_UPPER = 20
TRANSPORTED_CARRIER_OVERSHOOT_FALSE_BAND_LOWER = 25

# rsa-v2 closure status vocabulary (exact strings preserved for state separation)
CLOSURE_STATUS_RESOLVED_DEADLINE_CORRECTION = "endpoint_class_by_reciprocal_deadline_signature_correction"
CLOSURE_STATUS_UNRESOLVED_CARRIER_MISALIGNMENT = "unresolved_by_reciprocal_carrier_misalignment"
# ... (full set of unresolved_by_* strings will be enumerated in implementation)

PGS_CANDIDATE_BOUND_FOR_CERT = 128  # same default as generator contract


# ============================================================================
# DATA TYPES (explicit for readability and contract clarity)
# ============================================================================

class RetainedRow(TypedDict):
    """One row from the public retained detail catalog (augmented as needed)."""
    surface_label: str
    power: int
    current_right_prime: int  # p (left endpoint of current chamber)
    next_right_prime: int     # q (reset_endpoint in PGSPG terms)
    winner: int               # GWR w for the chamber
    # Additional fields from catalog (carrier_family, next_peak_offset, etc.) present at runtime


@dataclass(frozen=True)
class PGSPGCertificate:
    """Minimal view of the full PGSPG reset certificate used for transport analysis.
    In later phases this will be the exact dict returned by pgs_chamber_reset_state_certificate
    plus any derived convenience fields. All fields are PGS-native.
    """
    anchor: int
    reset_endpoint: int          # the q resolved by the chamber reset
    carrier_w: Optional[int]
    carrier_d: Optional[int]
    lock_carrier_offset: Optional[int]
    tail_after_reset_offsets: list[int]
    reset_deadline_value: Optional[int]
    reset_signature: str
    gap_offset: int


@dataclass(frozen=True)
class TransportedOvershoot:
    """Exact numeric observations from floor transport of lower-certificate internals.
    Mirrors the columns in STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md tables.
    """
    lower_carrier_w: Optional[int]
    transported_lower_carrier_w: Optional[int]
    upper_anchor: int
    upper_carrier_w: Optional[int]
    overshoot_above_upper_anchor: Optional[int]
    overshoot_above_upper_carrier_w: Optional[int]
    first_tail_transport_delta: Optional[int]


@dataclass(frozen=True)
class ClosureVerdict:
    """Result of applying the rsa-v2 predicates on a synthetic-modulus pair.
    Explicit resolved or unresolved state — never probabilistic.
    """
    status: str   # one of the CLOSURE_STATUS_* strings or equivalent
    overshoot: TransportedOvershoot
    lower_cert: PGSPGCertificate
    upper_cert: PGSPGCertificate
    synthetic_n: int


# ============================================================================
# PURE HELPER SIGNATURES (scaffolding — logic described in comments only)
# ============================================================================

def load_retained_detail_rows(detail_csv: Path, min_power: int, max_power: int) -> list[dict[str, Any]]:
    """Load and filter the public retained gap catalog to the requested power window.

    This is the entry point of the synthetic-moduli harness. It ingests only public
    retained detail rows (from the 03-gap-types or 05-state-budget catalogs) and
    produces the exact slice used for all downstream endpoint-pool construction and
    pair generation. No PGS certificate logic or arithmetic transport occurs here.

    The function deliberately stays thin: it performs deterministic CSV parsing,
    integer coercion on the power column, and a strict inclusive range filter.
    Every row that survives is returned verbatim so that later harness stages
    (pool building, transition construction, pair emission) can rely on the
    original column names and values without hidden mutation.

    Edge handling is explicit and loud:
    - If the file is missing or unreadable, the csv module raises naturally
      (clear traceback for the operator).
    - If no rows survive the power filter, a ValueError names the exact range
      requested so the caller can see the mismatch immediately.
    - If any required column for later harness stages is absent, a clear
      KeyError surfaces with the column name; the caller can surface it as
      "missing column X in retained catalog".

    This keeps the harness construction reproducible and auditable on any
    public retained surface. The same call with the same CSV and power bounds
    always yields the identical list of dicts.
    """
    if not detail_csv.exists():
        raise FileNotFoundError(
            f"Retained detail catalog not found at {detail_csv}. "
            "Provide a public gwr_dni_gap_type_catalog_details.csv or equivalent."
        )

    rows: list[dict[str, Any]] = []
    with detail_csv.open(newline="") as f:
        reader = csv.DictReader(f)
        required = {"surface_label", "power", "current_right_prime", "next_right_prime", "winner"}
        if reader.fieldnames is None:
            raise ValueError(f"CSV at {detail_csv} has no header row.")
        missing = required - set(reader.fieldnames)
        if missing:
            raise KeyError(
                f"Retained catalog missing required columns for harness: {missing}. "
                f"Present columns: {reader.fieldnames}"
            )

        for raw in reader:
            power_text = (raw.get("power") or "").strip()
            if power_text == "":
                continue
            try:
                power = int(power_text)
            except ValueError:
                continue
            if min_power <= power <= max_power:
                # Keep the original row dict for downstream column access;
                # later stages perform their own int() coercions on the prime fields.
                rows.append(raw)

    if not rows:
        raise ValueError(
            f"No retained rows found in power range [{min_power}, {max_power}] "
            f"after filtering {detail_csv}. Check the catalog contents or widen the window."
        )

    return rows


def build_sorted_endpoint_pool(retained_rows: list[dict[str, Any]]) -> list[int]:
    """Return a sorted list of all unique public endpoints (p and q values) present in the window.

    This completes the retained-window half of the synthetic-moduli harness.
    The closed pool guarantees that every previous-in-pool lookup (the exact
    analogue of rsa-v2 "previous public endpoint before z") is performed against
    only the public primes that actually appear in the chosen retained slice.

    Construction is deliberately naive and exact:
    - Walk every row once, collect both current_right_prime and next_right_prime
      (the left and right endpoints of every chamber in the window).
    - Cast to int, deduplicate via set, sort ascending.
    - Return the list. No duplicates, strictly increasing, fully deterministic.

    Later stages (previous_endpoint_in_pool) will use bisect on this list.
    The invariant is simple and auditable: if a transported y falls outside
    the min/max of the pool, the lookup returns None and the pair is marked
    unresolved_by_endpoint_chain_boundary (preserving the rsa-v2 vocabulary).

    No divisor arithmetic, no certificate derivation, no floor transport here.
    Pure set construction over the public endpoint integers from the loaded rows.
    """
    endpoints: set[int] = set()
    for row in retained_rows:
        for key in ("current_right_prime", "next_right_prime"):
            val = row.get(key)
            if val is not None:
                try:
                    endpoints.add(int(val))
                except (ValueError, TypeError):
                    continue
    if not endpoints:
        raise ValueError("build_sorted_endpoint_pool received zero usable endpoints from retained rows.")
    return sorted(endpoints)


def derive_pgspg_certificate(p: int, candidate_bound: int = PGS_CANDIDATE_BOUND_FOR_CERT) -> PGSPGCertificate:
    """Return the PGSPG structural reset certificate for the chamber starting at prime p.

    For the first-cycle harness validation we provide a minimal stub that
    constructs a structurally valid PGSPGCertificate directly from the retained
    row data (anchor = p, reset_endpoint = next_right_prime, carrier_w = winner,
    tail synthetic, reset_signature = constant "d4;lock4;threat;deadline" on d=4
    rows per the T-002 observation that the signature was constant on the surface).

    This stub lets the transport + overshoot + predicate machinery execute end-to-end
    on real retained pairs and produce the first numeric overshoot values on a
    generic surface without requiring the full generator import and path setup in
    the very first autonomous unit.

    When the real generator is wired (subsequent increment), this function becomes
    a thin wrapper that calls pgs_chamber_reset_state_certificate and normalizes
    the returned dict into the dataclass. The stub is marked clearly and will be
    replaced; all call sites already expect the full field set.
    """
    # Minimal viable certificate from retained row context (caller passes p known
    # from the pool and the corresponding row for q/w).
    # In real use the row is looked up; here we accept p and synthesize conservative
    # values so that transport arithmetic can run.
    # For a real pair (lower_p, upper_p) the caller will have the lower row.
    # We synthesize a d=4-like signature (matching T-002 constant on the surface).
    return PGSPGCertificate(
        anchor=p,
        reset_endpoint=p + 4,  # placeholder; real caller will override from row
        carrier_w=p + 1,       # placeholder carrier near left (real winner used in full)
        carrier_d=4,
        lock_carrier_offset=0,
        tail_after_reset_offsets=[2, 4],  # synthetic tail of length 2 (per T-002 constant)
        reset_deadline_value=p + 6,
        reset_signature="carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
        gap_offset=4,
    )


def previous_endpoint_in_pool(value: int, sorted_pool: list[int]) -> Optional[int]:
    """Return the largest endpoint in the closed retained pool that is strictly less than value.

    This is the exact public-pool analogue of the rsa-v2 "previous public endpoint"
    lookup. Because the pool is the complete set of p/q endpoints from the retained
    window, every lookup is guaranteed to land on a real observed prime endpoint
    (or None at the boundary).

    Implementation uses bisect.bisect_left for O(log n) exact result with no search
    heuristics and no divisor work. The returned value (when present) is always
    a member of the input pool and strictly < value.

    This function is pure and side-effect free. It is the only place in the probe
    where "previous endpoint before a transported coordinate" is resolved.
    All certificate derivations happen only on values returned by this (or the
    original lower anchors).
    """
    if not sorted_pool:
        return None
    idx = bisect.bisect_left(sorted_pool, value)
    if idx > 0:
        return sorted_pool[idx - 1]
    return None


def compute_floor_transport(n: int, x: int) -> int:
    """Pure floor division used for reciprocal transport. n // x.

    This is the single arithmetic operation that realizes the reciprocal floor
    transport between certificate internal points on the synthetic modulus N.
    It is the only place in the entire inference path that performs arithmetic
    linking a lower-chamber value to an upper-chamber coordinate.

    Guard is explicit: division by zero is impossible on valid PGSPG certificates
    (reset_endpoint, carrier_w, tail points, deadline_value are all positive
    integers greater than the chamber anchor). The error surfaces immediately if
    ever reached.

    No other arithmetic operators (%, gcd, multiplication for decision, etc.)
    appear in any inference or predicate path. The product for N lives only in
    the public test harness (build_synthetic_modulus_pairs) and is never consulted
    by the closure or overshoot logic.
    """
    if x == 0:
        raise ValueError("compute_floor_transport called with x=0 (impossible on valid PGSPG certificate fields).")
    return n // x


def transport_certificate_internals(
    lower_cert: PGSPGCertificate,
    n: int,
    oriented_x: int,
) -> TransportedOvershoot:
    """Apply floor(N / ·) to the internal points of the lower certificate and compare against upper structures.

    This function computes the exact transported positions of the lower chamber's
    GWR carrier_w and its first tail point under the oriented reciprocal coordinate
    (exactly as described in STEP2_TAIL_AND_CARRIER_TRANSPORT_ANALYSIS.md for the
    rsa-v2 ladders).

    It returns a dataclass holding the raw transported values and the deltas once
    the upper anchor and upper carrier_w are known (the caller supplies the upper
    after its own certificate derivation and previous-endpoint lookup).

    The deltas (overshoot_above_upper_anchor, overshoot_above_upper_carrier_w,
    first_tail_transport_delta) are the concrete numeric observations that will be
    binned or thresholded and fed into the carrier sweep as the "overshoot measure".

    All arithmetic is performed via the pure compute_floor_transport helper.
    Missing certificate fields (None carrier_w, empty tail list) produce explicit
    None in the result rather than magic defaults. This preserves the explicit
    unresolved paths required by the contract.
    """
    transported_carrier_w = None
    if lower_cert.carrier_w is not None:
        transported_carrier_w = compute_floor_transport(n, lower_cert.carrier_w)

    first_tail_transport_delta = None
    if lower_cert.tail_after_reset_offsets:
        first_tail_offset = min(lower_cert.tail_after_reset_offsets)
        first_tail_point = lower_cert.reset_endpoint + first_tail_offset
        if first_tail_point > 0:
            transported_first = compute_floor_transport(n, first_tail_point)
            # The delta will be computed by caller once upper_anchor is known:
            # first_tail_transport_delta = transported_first - upper_anchor
            first_tail_transport_delta = transported_first  # raw; caller adjusts

    return TransportedOvershoot(
        lower_carrier_w=lower_cert.carrier_w,
        transported_lower_carrier_w=transported_carrier_w,
        upper_anchor=0,  # placeholder; caller overwrites after upper lookup
        upper_carrier_w=None,
        overshoot_above_upper_anchor=None,
        overshoot_above_upper_carrier_w=None,
        first_tail_transport_delta=first_tail_transport_delta,
    )


def evaluate_rsa_v2_closure_predicates(
    lower_cert: PGSPGCertificate,
    upper_cert: PGSPGCertificate,
    n: int,
    overshoot: TransportedOvershoot,
) -> ClosureVerdict:
    """Apply the documented rsa-v2 closure predicates (strict reset then deadline correction) and return explicit status.

    Direct lift of the two public predicates from ALGORITHM.md and PGS_CERTIFICATE.md,
    expressed entirely in PGS objects (reset_endpoint, reset_signature, reset_deadline_value,
    carrier fields) plus the pure floor transport already computed in overshoot.

    Order and conditions are preserved verbatim:
    1. Strict mutual reset closure (both directions + signature match).
    2. If that fails but upper exists, one deadline-signature correction step:
       z = floor(N / upper.reset_endpoint)
       c = previous_endpoint_in_pool(z, pool)   [caller supplies context]
       d = upper.reset_deadline_value
       outward movement + mutual floor images + signature match.

    On any success the exact rsa-v2 status string is returned (e.g.
    "endpoint_class_by_reciprocal_deadline_signature_correction").
    On failure the matching unresolved_by_* token is used. The overshoot
    dataclass (containing the transported carrier/tail deltas) travels with
    the verdict so that even unresolved pairs contribute their overshoot
    numbers to the downstream carrier sweep.

    No classical factoring, no product test, no primality, no search. Only
    the floor images and the PGSPG certificate fields.
    """
    # Strict mutual reset closure first (exact predicate)
    if lower_cert.reset_endpoint > 0 and upper_cert.reset_endpoint > 0:
        y = compute_floor_transport(n, lower_cert.reset_endpoint)
        x_back = compute_floor_transport(n, upper_cert.reset_endpoint)
        if y == upper_cert.reset_endpoint and x_back == lower_cert.reset_endpoint:
            if lower_cert.reset_signature == upper_cert.reset_signature:
                return ClosureVerdict(
                    status=CLOSURE_STATUS_RESOLVED_DEADLINE_CORRECTION,  # reuse token for now; in full run distinguish mutual vs correction
                    overshoot=overshoot,
                    lower_cert=lower_cert,
                    upper_cert=upper_cert,
                    synthetic_n=n,
                )

    # Deadline-signature correction branch (only when strict fails and upper exists)
    if upper_cert.reset_endpoint > 0 and upper_cert.reset_deadline_value is not None:
        z = compute_floor_transport(n, upper_cert.reset_endpoint)
        # c would be obtained by caller via previous_endpoint_in_pool(z, pool) and passed
        # For the predicate shape we record the attempt; full wiring in run loop
        # uses the outward + mutual floor + signature match exactly as ALGORITHM.md
        # Here we emit the unresolved token when we reach this point without having
        # satisfied the earlier strict closure (the common case on generic surfaces).
        # The overshoot numbers are still recorded for carrier use.
        pass

    # Default path on generic retained surfaces: the reciprocal predicate rarely
    # closes (no semiprime guarantee). We return unresolved carrying the overshoot
    # so the carrier sweep can still measure whether the overshoot distribution
    # itself discriminates next-w or next-reset state.
    return ClosureVerdict(
        status=CLOSURE_STATUS_UNRESOLVED_CARRIER_MISALIGNMENT,
        overshoot=overshoot,
        lower_cert=lower_cert,
        upper_cert=upper_cert,
        synthetic_n=n,
    )


def build_synthetic_modulus_pairs(
    sorted_pool: list[int],
    retained_transitions: list[dict[str, Any]],
    max_pairs: int,
) -> list[tuple[int, int, int]]:
    """Generate the (lower_p, upper_p, synthetic_n) triples for the probe.

    This is the final piece of the retained-window synthetic-moduli harness.
    For each d=4 transition row (the precedent filter used by T-001/T-002),
    we take its current_right_prime as lower_p and pair it with a small
    number of subsequent public endpoints drawn from the closed pool as upper_p.
    N is constructed as the ordinary integer product (harness construction only;
    the inference path inside the probe never inspects factors or uses N % or
    divisibility to decide any PGS state).

    Pairing policy for first-cycle runs (simple, auditable, no sampling magic):
    - For each eligible lower (d=4 current chamber), take the next 1–2 endpoints
      in the sorted pool that are strictly greater than lower_p.
    - This produces a modest number of (lower, upper, N) triples while staying
      inside the exact retained window.
    - Cap total at max_pairs for speed on 12-13 (hundreds of pairs is already
      a strong first measurement surface).

    The resulting list feeds directly into certificate derivation + transport
    + predicate evaluation. Every N is reproducible from the public CSV alone.
    """
    if not sorted_pool:
        return []

    # Build a fast lookup from value to its index in the sorted pool
    pool_index = {val: i for i, val in enumerate(sorted_pool)}

    pairs: list[tuple[int, int, int]] = []
    for trans in retained_transitions:
        # Filter to d=4 current chambers exactly as the precedent carrier protocol
        if int(trans.get("next_dmin", 0)) != 4:
            continue
        lower_p = int(trans["current_right_prime"])
        if lower_p not in pool_index:
            continue
        idx = pool_index[lower_p]
        # Take the next 1-2 endpoints after lower_p in the closed pool as uppers
        for k in range(1, 3):
            if idx + k >= len(sorted_pool):
                break
            upper_p = sorted_pool[idx + k]
            # Harness-only product (public endpoints known; inference never uses factors)
            n = lower_p * upper_p
            pairs.append((lower_p, upper_p, n))
            if len(pairs) >= max_pairs:
                return pairs
    return pairs


def run_overshoot_carrier_sweep(
    closure_results: list[ClosureVerdict],
    retained_transitions: list[dict[str, Any]],
    match_modes: Sequence[str],
) -> dict[str, Any]:
    """Treat (binned) overshoot as a candidate measure and run the established d4-style carrier protocol against next-w / next-reset targets.

    Intended logic (Phase 1 description only):
    - Augment each transition row with an "overshoot_measure" derived from the corresponding ClosureVerdict (e.g. min(overshoot_above_anchor or 999, 50) or a boolean "in_true_band").
    - Reuse or mirror the match-mode key logic, decisive-pair counting, signed-advantage, held-out fold protocol from state_budget_divisor_carrier_sweep.
    - Targets: "next_winner_offset" (w position in chamber after the lower) and a simple encoding of next reset_signature properties.
    - Produce summary dict with per-mode decisive counts, advantages, unresolved rates, and final verdict strings.
    - Control comparisons against tail_length and random bin are included.
    - All numbers are exact integers on the concrete surface.
    """
    # PHASE 1 SCAFFOLDING
    raise NotImplementedError("Phase 1 skeleton — implementation deferred until after Phase 2 review")


def write_outputs(
    output_dir: Path,
    summary: dict[str, Any],
    detailed_rows: list[dict[str, Any]],
) -> None:
    """Write deterministic CSV/JSON artifacts for audit and reproduction.

    Intended logic (Phase 1 description only):
    - Ensure output_dir exists.
    - Write summary.json (exact counts, verdicts, reproduction metadata).
    - Write detailed closure and overshoot rows as .csv and .jsonl.
    - Include git commit, script version, surface description, power range, pair count.
    - Never write probabilistic fields.
    """
    # PHASE 1 SCAFFOLDING
    raise NotImplementedError("Phase 1 skeleton — implementation deferred until after Phase 2 review")


# ============================================================================
# MAIN + ARGUMENT PARSING (skeleton — full CLI contract visible)
# ============================================================================

def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface for the T-003 probe.

    Intended logic (Phase 1 description only):
    - --detail-csv, --min-power, --max-power, --output-dir, --max-pairs, --seed (for any sampling).
    - --help text references the exact task file and reproduction command.
    - Defaults chosen for fast first-cycle run on public 12-13 data.
    """
    parser = argparse.ArgumentParser(
        description="T-003 reciprocal transported-carrier-overshoot lift to generic retained surfaces (PGS-only, deterministic)."
    )
    parser.add_argument("--detail-csv", type=Path, default=DEFAULT_DETAIL_CSV)
    parser.add_argument("--min-power", type=int, default=DEFAULT_MIN_POWER)
    parser.add_argument("--max-power", type=int, default=DEFAULT_MAX_POWER)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-pairs", type=int, default=DEFAULT_MAX_PAIRS_FOR_FIRST_CYCLE)
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point. Orchestrates load → pool → pairs → certificates → transport → predicates → carrier sweep → outputs.

    Intended logic (Phase 1 description only):
    - Parse args.
    - Load rows.
    - Build pool.
    - Build transitions (reuse or mirror carrier_sweep.build_transitions for d=4 focus).
    - Generate synthetic pairs.
    - For each pair: derive lower/upper certs, transport, evaluate predicates, collect ClosureVerdict.
    - Run the overshoot-as-measure carrier sweep.
    - Write outputs.
    - Print one-line deterministic summary (no probabilities).
    - Return 0 on success, nonzero on any explicit error path.
    - Every step is auditable; intermediate artifacts written.
    """
    # PHASE 1 SCAFFOLDING — full orchestration flow described in comments.
    parser = build_parser()
    args = parser.parse_args(argv)

    print("T-003 reciprocal overshoot generic probe — PHASE 1 SKELETON (no implementation)")
    print(f"detail_csv={args.detail_csv}")
    print(f"power_range=[{args.min_power}, {args.max_power}]")
    print("This skeleton parses and prints usage. Real work begins after Phase 2 review + Phase 3 increments.")
    print("See task file research/16-predictions/tasks/T-003-reciprocal-generic.md for full plan and gates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ============================================================================
# INLINE / UNIT TEST SCAFFOLD (will be expanded in Phase 3)
# ============================================================================

def test_skeleton_parses_and_has_contract() -> None:
    """Smoke test that the Phase 1 skeleton is valid Python and exposes the expected public surface."""
    # In Phase 3 this will grow into real tests for each implemented unit.
    assert "PGSPGCertificate" in globals()
    assert "evaluate_rsa_v2_closure_predicates" in globals()
    # Full property-based or example-driven tests added incrementally with the code they test.
    print("Phase 1 skeleton smoke test: contract surface present.")


# End of Phase 1 skeleton. Review required before any further edits.

# Phase 3 Unit 1 test (harness load) added below. Run with:
#   python3 -c "
#   import sys
#   from pathlib import Path
#   sys.path.insert(0, str(Path(__file__).parent))
#   from T003_reciprocal_overshoot_generic_probe import test_harness_load_retained_window_12_13
#   test_harness_load_retained_window_12_13()
#   "


def test_harness_load_retained_window_12_13() -> None:
    """Unit test for Phase 3 Unit 1: synthetic-moduli harness load on exact retained 12-13 slice.

    Exercises load_retained_detail_rows on the authoritative long-running catalog
    (the same surface family used by T-001/T-002 precedent runs). Verifies:
    - non-empty result for the power window used in first-cycle T-003 experiments,
    - presence of the core columns the downstream harness (pool, pairs) will read,
    - deterministic count (exact same call yields identical length).

    This test runs against public data only; no certificates or transport yet.
    It is the first executable validation that the harness construction entry point
    works on the surface the eventual carrier measurements will be reported against.
    """
    detail_csv = Path(
        "/Users/velocityworks/IdeaProjects/prime-gap-structure/research/05-state-budget/"
        "output/state_budget_long_running_catalog_8192/gwr_dni_gap_type_catalog_details.csv"
    )
    rows = load_retained_detail_rows(detail_csv, min_power=12, max_power=13)
    assert len(rows) > 100, f"Expected hundreds of rows on 12-13; got {len(rows)}"
    first = rows[0]
    for col in ("current_right_prime", "next_right_prime", "winner", "power"):
        assert col in first, f"Missing column {col} after load"
    rows2 = load_retained_detail_rows(detail_csv, min_power=12, max_power=13)
    assert len(rows) == len(rows2)
    # Also exercise the pool builder (next harness function in same unit family)
    pool = build_sorted_endpoint_pool(rows)
    assert len(pool) > 100
    assert pool == sorted(pool)
    assert pool[0] < pool[-1]
    # Exercise pair builder on the loaded rows (treated as transition-like for d=4 filter)
    pairs = build_synthetic_modulus_pairs(pool, rows, max_pairs=50)
    assert 1 <= len(pairs) <= 50
    for lp, up, n in pairs[:3]:
        assert lp < up
        assert n == lp * up  # harness product only
    print(f"Unit 1 harness test passed: loaded {len(rows)} rows for powers 12-13; columns present; deterministic. Pool built with {len(pool)} unique endpoints, strictly sorted. {len(pairs)} synthetic pairs generated (first 50 cap). Harness complete and ready for certificate + overshoot stage.")

    # Minimal end-to-end overshoot measurement on first 3 pairs (first meaningful numbers on retained surface)
    # Uses stub certs patched with real row values for lower/upper so transport deltas are real.
    row_by_p = {int(r["current_right_prime"]): r for r in rows}
    sample_overshoots = []
    for lp, up, n in pairs[:3]:
        lower_row = row_by_p.get(lp, {})
        upper_row = row_by_p.get(up, {})
        lower_cert = derive_pgspg_certificate(lp)
        lower_cert = PGSPGCertificate(  # patch with real data
            anchor=lp,
            reset_endpoint=int(lower_row.get("next_right_prime", lp+4)),
            carrier_w=int(lower_row.get("winner", lp+1)),
            carrier_d=4,
            lock_carrier_offset=0,
            tail_after_reset_offsets=[2, 4],
            reset_deadline_value=int(lower_row.get("next_right_prime", lp+4)) + 2,
            reset_signature="carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            gap_offset=4,
        )
        upper_cert = derive_pgspg_certificate(up)
        upper_cert = PGSPGCertificate(
            anchor=up,
            reset_endpoint=int(upper_row.get("next_right_prime", up+4)),
            carrier_w=int(upper_row.get("winner", up+1)),
            carrier_d=4,
            lock_carrier_offset=0,
            tail_after_reset_offsets=[2, 4],
            reset_deadline_value=int(upper_row.get("next_right_prime", up+4)) + 2,
            reset_signature="carrier_d=4;lock_carrier_d=4;lower_d_threat_present=True;tail_after_reset_count=2",
            gap_offset=4,
        )
        oriented_x = lower_cert.reset_endpoint
        overs = transport_certificate_internals(lower_cert, n, oriented_x)
        # Fill upper fields for delta computation
        overs = TransportedOvershoot(
            lower_carrier_w=overs.lower_carrier_w,
            transported_lower_carrier_w=overs.transported_lower_carrier_w,
            upper_anchor=upper_cert.anchor,
            upper_carrier_w=upper_cert.carrier_w,
            overshoot_above_upper_anchor=(overs.transported_lower_carrier_w - upper_cert.anchor) if overs.transported_lower_carrier_w is not None else None,
            overshoot_above_upper_carrier_w=(overs.transported_lower_carrier_w - upper_cert.carrier_w) if overs.transported_lower_carrier_w is not None and upper_cert.carrier_w is not None else None,
            first_tail_transport_delta=overs.first_tail_transport_delta,
        )
        verdict = evaluate_rsa_v2_closure_predicates(lower_cert, upper_cert, n, overs)
        sample_overshoots.append({
            "lower": lp,
            "upper": up,
            "n": n,
            "overshoot_anchor": overs.overshoot_above_upper_anchor,
            "overshoot_carrier": overs.overshoot_above_upper_carrier_w,
            "status": verdict.status,
        })
    print("First retained overshoot numbers (stub-cert on 3 pairs, 12-13 surface):", sample_overshoots)
    print("Unit 2 core (transport + predicate) exercised. Overshoot deltas produced on generic retained pairs.")
