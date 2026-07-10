#!/usr/bin/env python3
"""Classify research progress for the PGS hourly relay."""

from __future__ import annotations

from typing import Any


RESEARCH_ADVANCE = "ADVANCE"
RESEARCH_NO_DELTA = "NO_DELTA"
RESEARCH_FAILED = "FAILED"
RESEARCH_UNRESOLVED = "UNRESOLVED"

OPS_OK = "OK"
OPS_PARTIAL = "PARTIAL"
OPS_BLOCKED = "BLOCKED"
OPS_FAILED = "FAILED"


def summary_signature(summary: dict[str, Any] | None) -> dict[str, Any] | None:
    """Return the comparable scientific signature of one falsification summary."""
    if not summary:
        return None
    max_row = summary.get("max_row") or {}
    return {
        "min_prime": summary.get("min_prime"),
        "max_prime": summary.get("max_prime"),
        "tested_prime_count": summary.get("tested_prime_count"),
        "first_counterexample": summary.get("first_counterexample"),
        "max_dynamic_cutoff_utilization": summary.get("max_dynamic_cutoff_utilization"),
        "max_p": max_row.get("p"),
        "max_offset": max_row.get("offset"),
    }


def signatures_equal(a: dict[str, Any] | None, b: dict[str, Any] | None) -> bool:
    """Return True when both signatures exist and match on all tracked fields."""
    if a is None or b is None:
        return False
    keys = (
        "min_prime",
        "max_prime",
        "tested_prime_count",
        "first_counterexample",
        "max_dynamic_cutoff_utilization",
        "max_p",
        "max_offset",
    )
    return all(a.get(key) == b.get(key) for key in keys)


def classify_deterministic(
    *,
    command_ok: bool,
    pytest_ok: bool,
    current_signature: dict[str, Any] | None,
    prior_signature: dict[str, Any] | None,
    baseline_signature: dict[str, Any] | None,
) -> tuple[str, str]:
    """
    Return (research_status, delta_line) for one deterministic job.

    ADVANCE requires a scientific signature that is new relative to the prior
    run signature and the frozen baseline (when present).
    """
    if not command_ok:
        return RESEARCH_FAILED, "command exited nonzero"
    if not pytest_ok:
        return RESEARCH_FAILED, "pytest exited nonzero"

    if current_signature is None:
        return (
            RESEARCH_UNRESOLVED,
            "command and pytest passed but no summary signature was produced",
        )

    if current_signature.get("first_counterexample") not in (None, "none", ""):
        return (
            RESEARCH_ADVANCE,
            f"first counterexample observed: {current_signature.get('first_counterexample')}",
        )

    if signatures_equal(current_signature, prior_signature):
        return (
            RESEARCH_NO_DELTA,
            "summary signature matches prior hourly run (replay)",
        )

    if signatures_equal(current_signature, baseline_signature):
        return (
            RESEARCH_NO_DELTA,
            "summary signature matches frozen certified baseline (replay)",
        )

    prior_max = None if prior_signature is None else prior_signature.get("max_prime")
    baseline_max = None if baseline_signature is None else baseline_signature.get("max_prime")
    current_max = current_signature.get("max_prime")
    anchors = [value for value in (prior_max, baseline_max) if isinstance(value, int)]
    if isinstance(current_max, int) and anchors and current_max > max(anchors):
        return (
            RESEARCH_ADVANCE,
            f"new falsification regime through max_prime={current_max}",
        )

    if prior_signature is None and baseline_signature is None:
        return (
            RESEARCH_ADVANCE,
            "first recorded summary signature for this relay path",
        )

    if not signatures_equal(current_signature, prior_signature) and not signatures_equal(
        current_signature, baseline_signature
    ):
        return (
            RESEARCH_ADVANCE,
            "summary signature changed versus prior/baseline",
        )

    return RESEARCH_NO_DELTA, "no scientific signature delta"


def key_numbers_from_signature(signature: dict[str, Any] | None) -> dict[str, Any]:
    """Project signature fields used in Rocket.Chat and last_run.json."""
    if not signature:
        return {}
    return {
        "min_prime": signature.get("min_prime"),
        "max_prime": signature.get("max_prime"),
        "tested_prime_count": signature.get("tested_prime_count"),
        "first_counterexample": signature.get("first_counterexample"),
        "max_utilization": signature.get("max_dynamic_cutoff_utilization"),
        "max_p": signature.get("max_p"),
        "max_offset": signature.get("max_offset"),
    }
