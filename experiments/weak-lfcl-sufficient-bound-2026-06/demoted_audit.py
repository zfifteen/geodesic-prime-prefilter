"""Audit-demoted τ=2 lemma: structural certificate → zero-excess signature."""

from __future__ import annotations


def tau_le_2_implies_tau_eq_2(n: int) -> bool:
    """Lemma bridge: for n > 1, τ(n) ≤ 2 implies τ(n) = 2."""
    return n > 1


def demoted_zero_excess_signature(replay: dict[str, object]) -> bool:
    """
    Derive zero-excess signature from selection-time record only.
    Does not read τ(q) from a divisor table.
    """
    if replay is None:
        return False
    record = replay["selection_record"]
    if str(record["status"]) != "RESOLVED_SURVIVOR":
        return False
    if bool(record["composite_witness_at_selection"]):
        return False
    if int(record["unresolved_wheel_open_before"]) > 0:
        return False
    if not bool(replay["wheel_open"]):
        return False
    q = int(replay["q"])
    return tau_le_2_implies_tau_eq_2(q)


def structural_unique_resolved(replay: dict[str, object]) -> bool:
    """Exactly one resolved survivor at sufficient bound."""
    if replay is None:
        return False
    return int(replay["resolved_count"]) == 1