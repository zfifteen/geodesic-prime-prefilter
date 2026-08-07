"""Named GWR-carrier transport closure predicates (A1 FR-INF-05).

These predicates are PGS inference filters. They use only chamber-reset carrier
fields and public floor transport. They never call gcd, primality APIs, or
factor helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class PredicateResult:
    """One named predicate outcome with a short diagnostic."""

    name: str
    holds: bool
    detail: str


def gwr_carrier_fields_present(
    lower: Mapping[str, Any] | None,
    upper: Mapping[str, Any] | None,
) -> PredicateResult:
    """Require GWR carrier fields on both certificates."""
    name = "gwr_carrier_fields_present"
    if lower is None or upper is None:
        return PredicateResult(name, False, "missing_certificate_side")
    if lower.get("carrier_w") is None or upper.get("carrier_w") is None:
        return PredicateResult(name, False, "missing_carrier_w")
    if lower.get("carrier_d") is None or upper.get("carrier_d") is None:
        return PredicateResult(name, False, "missing_carrier_d")
    return PredicateResult(name, True, "ok")


def _public_gap_offset(side: Mapping[str, Any]) -> int:
    """Positive public gap_offset, or default 20 when missing or non-positive."""
    gap = int(side.get("gap_offset") or 0)
    if gap <= 0:
        return 20
    return gap


def gwr_carrier_floor_transport_within_gap_bound(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> PredicateResult:
    """Legacy lower-only gap bound (diagnostic / comparison only).

    Bound = max(20, floor(1.2 * lower.gap_offset)).
    Not the live residual discriminator D; see dual-gap predicate.
    """
    name = "gwr_carrier_floor_transport_within_gap_bound"
    lower_w = lower.get("carrier_w")
    upper_w = upper.get("carrier_w")
    if lower_w is None or upper_w is None:
        return PredicateResult(name, False, "missing_carrier_w")
    lw = int(lower_w)
    uw = int(upper_w)
    if lw <= 0:
        return PredicateResult(name, False, "non_positive_lower_carrier")
    transported = n_value // lw
    delta = abs(transported - uw)
    lower_gap = _public_gap_offset(lower)
    bound = max(20, (6 * lower_gap) // 5)
    holds = delta <= bound
    return PredicateResult(
        name,
        holds,
        f"delta={delta};bound={bound};transported={transported};upper_w={uw}",
    )


def gwr_dual_gap_carrier_floor_transport_bound(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> PredicateResult:
    """Public residual discriminator D: dual-gap carrier floor transport bound.

    Objects: lower/upper carrier_w and gap_offset from PGSPG certificates.
    Mechanism: floor-transport lower.carrier_w through N and require proximity
    to upper.carrier_w within a bound scaled by both public gap widths.

    T = floor(N / lower.carrier_w)
    delta = |T - upper.carrier_w|
    G = g_lo + g_up
    boundD = max(20, floor(1.2 * G))
    D holds iff delta <= boundD

    Status: hypothesis residual discriminator. Used as the transport decision
    predicate inside rsa-v3 GWR evaluation; not a theorem.
    """
    name = "gwr_dual_gap_carrier_floor_transport_bound"
    lower_w = lower.get("carrier_w")
    upper_w = upper.get("carrier_w")
    if lower_w is None or upper_w is None:
        return PredicateResult(name, False, "missing_carrier_w")
    lw = int(lower_w)
    uw = int(upper_w)
    if lw <= 0:
        return PredicateResult(name, False, "non_positive_lower_carrier")
    transported = n_value // lw
    delta = abs(transported - uw)
    g_lo = _public_gap_offset(lower)
    g_up = _public_gap_offset(upper)
    bound_d = max(20, (6 * (g_lo + g_up)) // 5)
    holds = delta <= bound_d
    excess = delta - bound_d
    return PredicateResult(
        name,
        holds,
        (
            f"delta={delta};boundD={bound_d};g_lo={g_lo};g_up={g_up};"
            f"transported={transported};upper_w={uw};excess={excess}"
        ),
    )


def gwr_first_tail_reciprocal_proximity(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> PredicateResult:
    """When deadline=tail, first tail reciprocal image must sit near upper anchor."""
    name = "gwr_first_tail_reciprocal_proximity"
    signature = str(lower.get("reset_signature") or "")
    if "deadline=tail" not in signature:
        return PredicateResult(name, True, "not_applicable")
    tails = lower.get("tail_after_reset_offsets") or []
    if not tails:
        return PredicateResult(name, False, "empty_tail")
    try:
        reset_endpoint = int(lower["reset_endpoint"])
    except (TypeError, ValueError, KeyError):
        return PredicateResult(name, False, "missing_reset_endpoint")
    first_tail_point = reset_endpoint + int(tails[0])
    if first_tail_point <= 0:
        return PredicateResult(name, False, "non_positive_tail_point")
    transported = n_value // first_tail_point
    raw_anchor = upper.get("anchor")
    if raw_anchor is None:
        return PredicateResult(name, False, "missing_upper_anchor")
    try:
        upper_anchor = int(raw_anchor)
    except (TypeError, ValueError):
        return PredicateResult(name, False, "invalid_upper_anchor")
    delta = transported - upper_anchor
    holds = -12 <= delta <= 6
    return PredicateResult(name, holds, f"delta={delta}")


def gwr_lower_lock_dominance(lower: Mapping[str, Any]) -> PredicateResult:
    """Matched lower lock sits in the right half of its gap."""
    name = "gwr_lower_lock_dominance"
    lock_off = lower.get("lock_carrier_offset")
    gap = int(lower.get("gap_offset") or 0)
    if lock_off is None or gap <= 0:
        return PredicateResult(name, False, "missing_lock_or_gap")
    holds = 2 * int(lock_off) > gap
    return PredicateResult(name, holds, f"lock={lock_off};gap={gap}")


def gwr_matched_profile_counts(
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> PredicateResult:
    """Matched pair shares active and unresolved profile counts."""
    name = "gwr_matched_profile_counts"
    holds = (
        int(lower.get("active_count") or 0) == int(upper.get("active_count") or 0)
        and int(lower.get("unresolved_count") or 0)
        == int(upper.get("unresolved_count") or 0)
    )
    return PredicateResult(
        name,
        holds,
        f"lower=({lower.get('active_count')},{lower.get('unresolved_count')});"
        f"upper=({upper.get('active_count')},{upper.get('unresolved_count')})",
    )


# STEP2 tight carrier band (measured): true mutual 64-bit has delta_c=14; false 50-bit has 30.
# Dual-gap D still holds both (30 <= 45). Rank 1 names the D-hold / tight-band gap.
TIGHT_CARRIER_BAND = 20

# Joint residual cell for the measured 50-bit pin geometry after dual-gap D.
# R = (r_carrier=1, r_tail=2, r_lock=1) -> cell C1T2L1
JOINT_CELL_PIN_CODE = "joint_cell_C1T2L1"


def _carrier_delta_vs_upper_carrier(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> int | None:
    """Public |floor(N / lower.carrier_w) - upper.carrier_w|, or None if missing."""
    lower_w = lower.get("carrier_w")
    upper_w = upper.get("carrier_w")
    if lower_w is None or upper_w is None:
        return None
    lw = int(lower_w)
    if lw <= 0:
        return None
    return abs((n_value // lw) - int(upper_w))


def _first_tail_raw_delta(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> int | None:
    """Public floor-transport first-tail delta vs upper.anchor, or None if N/A/missing."""
    signature = str(lower.get("reset_signature") or "")
    if "deadline=tail" not in signature:
        return None
    tails = lower.get("tail_after_reset_offsets") or []
    if not tails:
        return None
    try:
        reset_endpoint = int(lower["reset_endpoint"])
    except (TypeError, ValueError, KeyError):
        return None
    first_tail_point = reset_endpoint + int(tails[0])
    if first_tail_point <= 0:
        return None
    raw_anchor = upper.get("anchor")
    if raw_anchor is None:
        return None
    try:
        upper_anchor = int(raw_anchor)
    except (TypeError, ValueError):
        return None
    return (n_value // first_tail_point) - upper_anchor


def _pinch_sum(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> int | None:
    """STEP2 pinch S = |T_c - upper.anchor| + |upper.anchor - T_tail|.

    Public certificate fields + floor transport only. None when tail path N/A.
    Measured pins: 50-bit false S=54; 64-bit true S=21.
    """
    lower_w = lower.get("carrier_w")
    raw_anchor = upper.get("anchor")
    if lower_w is None or raw_anchor is None:
        return None
    lw = int(lower_w)
    if lw <= 0:
        return None
    try:
        upper_anchor = int(raw_anchor)
    except (TypeError, ValueError):
        return None
    t_c = n_value // lw
    delta_t = _first_tail_raw_delta(n_value, lower, upper)
    if delta_t is None:
        return None
    # undershoot is signed delta_t = T_tail - anchor; |anchor - T_tail| = |delta_t|
    return abs(t_c - upper_anchor) + abs(delta_t)


def residual_vector_R(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> dict[str, object]:
    """Integer residual ranks R = (r_carrier, r_tail, r_lock) from public fields.

    Rank convention (hypothesis residual cell map, measured anchors from STEP2+D):
      r_carrier: 0 if delta_c <= 20; 1 if 20 < delta_c <= boundD; 2 if delta_c > boundD
      r_tail:    -1 N/A; 0 if [-12,6]; 1 if [-21,-13]; 2 if <=-22 or >=7
      r_lock:    -1 N/A; 0 if 2*lock > gap; 1 if weak (2*lock <= gap and lock >= gap//4);
                 2 if very early lock

    Status: hypothesis residual map. Not a theorem. Not a close rule.
    """
    g_lo = _public_gap_offset(lower)
    g_up = _public_gap_offset(upper)
    bound_d = max(20, (6 * (g_lo + g_up)) // 5)
    delta_c = _carrier_delta_vs_upper_carrier(n_value, lower, upper)
    if delta_c is None:
        r_carrier = -1
    elif delta_c <= TIGHT_CARRIER_BAND:
        r_carrier = 0
    elif delta_c <= bound_d:
        r_carrier = 1
    else:
        r_carrier = 2

    delta_t = _first_tail_raw_delta(n_value, lower, upper)
    if delta_t is None:
        r_tail = -1
    elif -12 <= delta_t <= 6:
        r_tail = 0
    elif -21 <= delta_t <= -13:
        r_tail = 1
    else:
        r_tail = 2

    lock_off = lower.get("lock_carrier_offset")
    gap = int(lower.get("gap_offset") or 0)
    if lock_off is None or gap <= 0:
        r_lock = -1
    else:
        lock_i = int(lock_off)
        if 2 * lock_i > gap:
            r_lock = 0
        elif lock_i >= gap // 4:
            r_lock = 1
        else:
            r_lock = 2

    t_label = "X" if r_tail < 0 else str(r_tail)
    l_label = "X" if r_lock < 0 else str(r_lock)
    c_label = "X" if r_carrier < 0 else str(r_carrier)
    cell = f"C{c_label}T{t_label}L{l_label}"
    pinch = _pinch_sum(n_value, lower, upper)
    return {
        "r_carrier": r_carrier,
        "r_tail": r_tail,
        "r_lock": r_lock,
        "decision_cell": cell,
        "delta_c": delta_c,
        "delta_t": delta_t,
        "boundD": bound_d,
        "g_lo": g_lo,
        "g_up": g_up,
        "tight_carrier_band": TIGHT_CARRIER_BAND,
        "pinch_S": pinch,
        "lock": None if lock_off is None else int(lock_off),
        "gap": gap if gap > 0 else None,
    }


def is_joint_cell_C1T2L1(vector: Mapping[str, object]) -> bool:
    """True for the measured 50-bit pin cell: loose D-hold carrier + hard tail + weak lock."""
    return (
        int(vector.get("r_carrier", -9)) == 1
        and int(vector.get("r_tail", -9)) == 2
        and int(vector.get("r_lock", -9)) == 1
    )


# Historical mutual-closure false public endpoint class on the 50-bit pin.
# Must never be re-admitted as a public structural emit (Heavy Phase-1 anti-admission).
HISTORICAL_FALSE_ENDPOINT_CLASS_50BIT: tuple[str, str] = ("32047651", "32059633")


def is_historical_false_endpoint_class(
    endpoint_lower: str | int | None,
    endpoint_upper: str | int | None,
) -> bool:
    """True when the pair matches the known 50-bit mutual-closure false class."""
    if endpoint_lower is None or endpoint_upper is None:
        return False
    return (str(endpoint_lower), str(endpoint_upper)) == HISTORICAL_FALSE_ENDPOINT_CLASS_50BIT


def evaluate_gwr_carrier_transport_closure(
    n_value: int,
    lower: Mapping[str, Any] | None,
    upper: Mapping[str, Any] | None,
    *,
    require_lock_and_profile: bool,
) -> tuple[bool, list[PredicateResult], str | None]:
    """Run the named GWR-carrier transport closure stack.

    Residual *decision* is the first failing required public predicate (order
    preserved). Residual *diagnostics* still collect later named components when
    certificates are present so joint residual honesty is visible (Phase-1):
    dual-gap D, first-tail (when applicable), and lock/profile when
    ``require_lock_and_profile`` is true, even if an earlier gate already failed.

    Returns (all_required_hold, results, residual_code_if_failed).
    """
    results: list[PredicateResult] = []
    residual: str | None = None

    present = gwr_carrier_fields_present(lower, upper)
    results.append(present)
    if not present.holds:
        return False, results, "unresolved_by_gwr_carrier_fields_absent"

    assert lower is not None and upper is not None
    # Live residual discriminator D (dual-gap). Lower-only bound kept as diagnostic.
    legacy_lower_only = gwr_carrier_floor_transport_within_gap_bound(
        n_value, lower, upper
    )
    results.append(legacy_lower_only)
    transport = gwr_dual_gap_carrier_floor_transport_bound(n_value, lower, upper)
    results.append(transport)
    if not transport.holds and residual is None:
        residual = "unresolved_by_reciprocal_carrier_misalignment"

    # Always evaluate first-tail when certificates exist (not_applicable is a hold).
    tail = gwr_first_tail_reciprocal_proximity(n_value, lower, upper)
    results.append(tail)
    if not tail.holds and residual is None:
        residual = "unresolved_by_first_tail_misalignment"

    if require_lock_and_profile:
        # Co-primary structural components for chain-step residual honesty:
        # always evaluate lock and profile for diagnostics even if residual
        # already decided (e.g. first-tail fail on the 50-bit pin).
        lock = gwr_lower_lock_dominance(lower)
        results.append(lock)
        if not lock.holds and residual is None:
            residual = "unresolved_by_lower_lock_misalignment"
        profile = gwr_matched_profile_counts(lower, upper)
        results.append(profile)
        if not profile.holds and residual is None:
            residual = "unresolved_by_profile_count_mismatch"

    # Residual cell R (hypothesis residual map): when the sequential stack lands
    # on first-tail fail while lock was evaluated, promote joint cell C1T2L1 if
    # the full rank vector matches the measured 50-bit FP geometry. This is a
    # residual subclass migration (class B), not a public close.
    residual_vector: dict[str, object] | None = None
    if residual is not None and residual == "unresolved_by_first_tail_misalignment":
        residual_vector = residual_vector_R(n_value, lower, upper)
        if is_joint_cell_C1T2L1(residual_vector):
            residual = JOINT_CELL_PIN_CODE
            results.append(
                PredicateResult(
                    "gwr_residual_cell_R",
                    False,
                    (
                        f"cell={residual_vector['decision_cell']};"
                        f"r=({residual_vector['r_carrier']},"
                        f"{residual_vector['r_tail']},"
                        f"{residual_vector['r_lock']});"
                        f"pinch_S={residual_vector['pinch_S']};"
                        f"delta_c={residual_vector['delta_c']};"
                        f"delta_t={residual_vector['delta_t']}"
                    ),
                )
            )
        else:
            results.append(
                PredicateResult(
                    "gwr_residual_cell_R",
                    False,
                    (
                        f"cell={residual_vector['decision_cell']};"
                        f"r=({residual_vector['r_carrier']},"
                        f"{residual_vector['r_tail']},"
                        f"{residual_vector['r_lock']});"
                        f"pinch_S={residual_vector['pinch_S']};"
                        "joint_C1T2L1=false"
                    ),
                )
            )
    elif residual is None:
        # Resolve path: still record R for diagnostics when certificates exist.
        residual_vector = residual_vector_R(n_value, lower, upper)
        results.append(
            PredicateResult(
                "gwr_residual_cell_R",
                True,
                (
                    f"cell={residual_vector['decision_cell']};"
                    f"r=({residual_vector['r_carrier']},"
                    f"{residual_vector['r_tail']},"
                    f"{residual_vector['r_lock']});"
                    f"pinch_S={residual_vector['pinch_S']}"
                ),
            )
        )

    holds = residual is None
    return holds, results, residual


def predicate_results_to_json(results: list[PredicateResult]) -> dict[str, object]:
    """JSON-safe predicate map for certificates and residuals."""
    return {
        item.name: {"holds": item.holds, "detail": item.detail}
        for item in results
    }


def residual_component_ledger(
    results: list[PredicateResult],
    *,
    decision_residual: str | None,
    residual_vector: Mapping[str, object] | None = None,
) -> dict[str, object]:
    """Full named GWR component map for residual honesty packages.

    Includes every evaluated predicate plus the decision residual code and
    optional residual cell R. Pure public diagnostics; no classical fields.
    """
    out: dict[str, object] = {
        "decision_residual": decision_residual,
        "components": predicate_results_to_json(results),
    }
    if residual_vector is not None:
        out["residual_vector_R"] = dict(residual_vector)
    return out
