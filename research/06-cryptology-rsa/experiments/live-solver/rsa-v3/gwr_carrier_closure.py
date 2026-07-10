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


def gwr_carrier_floor_transport_within_gap_bound(
    n_value: int,
    lower: Mapping[str, Any],
    upper: Mapping[str, Any],
) -> PredicateResult:
    """Transported lower carrier_w must land within a gap-scaled bound of upper carrier_w.

    Bound = max(20, floor(1.2 * lower.gap_offset)).
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
    lower_gap = int(lower.get("gap_offset") or 0)
    if lower_gap <= 0:
        lower_gap = 20
    bound = max(20, (6 * lower_gap) // 5)
    holds = delta <= bound
    return PredicateResult(
        name,
        holds,
        f"delta={delta};bound={bound};transported={transported};upper_w={uw}",
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


def evaluate_gwr_carrier_transport_closure(
    n_value: int,
    lower: Mapping[str, Any] | None,
    upper: Mapping[str, Any] | None,
    *,
    require_lock_and_profile: bool,
) -> tuple[bool, list[PredicateResult], str | None]:
    """Run the named GWR-carrier transport closure stack.

    Returns (all_required_hold, results, residual_code_if_failed).
    """
    results: list[PredicateResult] = []

    present = gwr_carrier_fields_present(lower, upper)
    results.append(present)
    if not present.holds:
        return False, results, "unresolved_by_gwr_carrier_fields_absent"

    assert lower is not None and upper is not None
    transport = gwr_carrier_floor_transport_within_gap_bound(n_value, lower, upper)
    results.append(transport)
    if not transport.holds:
        return False, results, "unresolved_by_reciprocal_carrier_misalignment"

    tail = gwr_first_tail_reciprocal_proximity(n_value, lower, upper)
    results.append(tail)
    if not tail.holds:
        return False, results, "unresolved_by_first_tail_misalignment"

    if require_lock_and_profile:
        lock = gwr_lower_lock_dominance(lower)
        results.append(lock)
        if not lock.holds:
            return False, results, "unresolved_by_lower_lock_misalignment"
        profile = gwr_matched_profile_counts(lower, upper)
        results.append(profile)
        if not profile.holds:
            return False, results, "unresolved_by_profile_count_mismatch"

    return True, results, None


def predicate_results_to_json(results: list[PredicateResult]) -> dict[str, object]:
    """JSON-safe predicate map for certificates and residuals."""
    return {
        item.name: {"holds": item.holds, "detail": item.detail}
        for item in results
    }
