#!/usr/bin/env python3
"""Classical validator for the toy PGSPG factorizer."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TWO_DIGIT_PRIMES = (
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)
DEFAULT_MAX_AUDIT_FACTOR = 99
DECISION_KNOBS = (
    "pgs_endpoint_lock",
    "upper_native_width_dominance",
    "endpoint_lock_then_upper_native_width_dominance",
    "reciprocal_floor_boundary_lock",
    "both_chambers_inside",
    "reset_signature_equal",
    "carrier_lock_equal",
)
STRUCTURAL_CANDIDATES = (
    "singleton_endpoint_lock",
    "unique_diagonal_echo",
    "unique_bidirectional_containment",
    "unique_bidirectional_capacity_cover",
    "unique_capacity_vector_dominance",
    "unique_balanced_capacity_max",
    "mixed_topology_collision_blocker",
    "no_bidirectional_containment_blocker",
)
PGSPG_LAWS = (
    "reset_signature_echo",
    "deadline_kind_echo",
    "threat_presence_echo",
    "lock_carrier_echo",
    "tail_offsets_echo",
    "tail_count_echo",
    "bidirectional_chamber_containment",
    "one_sided_chamber_containment",
)


def is_prime(value: int) -> bool:
    """Return classical primality for validator-only audit surfaces."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def audit_primes(max_factor: int = DEFAULT_MAX_AUDIT_FACTOR) -> list[int]:
    """Return deterministic validator-only primes on the bounded surface."""
    if max_factor < 11:
        raise ValueError("max_factor must be at least 11")
    return [value for value in range(11, max_factor + 1) if is_prime(value)]


def prime_pairs(max_factor: int = DEFAULT_MAX_AUDIT_FACTOR) -> list[tuple[int, int]]:
    """Return the deterministic bounded semiprime audit surface."""
    primes = audit_primes(max_factor)
    return [
        (p_value, q_value)
        for index, p_value in enumerate(primes)
        for q_value in primes[index:]
    ]


def two_digit_prime_pairs() -> list[tuple[int, int]]:
    """Return the deterministic two-digit semiprime audit surface."""
    return prime_pairs(DEFAULT_MAX_AUDIT_FACTOR)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated CSV audit rows."""
    fieldnames = [
        "case_id",
        "N",
        "audit_p",
        "audit_q",
        "inference_status",
        "inferred_p",
        "inferred_q",
        "audit_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_decision_knob_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated decision-knob audit rows."""
    fieldnames = [
        "knob",
        "valid_for_pgs_factorizer",
        "validity_note",
        "total_cases",
        "resolved",
        "unresolved",
        "ambiguous",
        "no_survivor",
        "audit_pass",
        "audit_fail",
        "resolved_precision",
        "resolution_rate",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_upper_width_failure_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated upper-width failure rows."""
    fieldnames = [
        "case_id",
        "N",
        "audit_p",
        "audit_q",
        "selected_p",
        "selected_q",
        "survivor_count",
        "diagonal_echo_count",
        "off_diagonal_count",
        "selected_row_topology",
        "upper_capacity_margin",
        "lower_capacity_margin",
        "mixed_topology_collision",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_rule_audit_matrix_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated rule audit matrix rows."""
    fieldnames = [
        "case_id",
        "N",
        "knob",
        "rule_family",
        "valid_for_pgs_factorizer",
        "rule_action",
        "survivor_count",
        "endpoint_lock_state",
        "diagonal_echo_count",
        "off_diagonal_count",
        "mixed_topology_collision",
        "reciprocal_image_containment_state",
        "signature_compatibility",
        "carrier_compatibility",
        "selected_p",
        "selected_q",
        "audit_p",
        "audit_q",
        "selected_row_topology",
        "upper_capacity_margin",
        "lower_capacity_margin",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_structural_candidate_matrix_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    """Write LF-terminated structural candidate audit rows."""
    fieldnames = [
        "case_id",
        "N",
        "candidate",
        "candidate_kind",
        "structural_law",
        "rule_action",
        "survivor_count",
        "endpoint_lock_state",
        "diagonal_echo_count",
        "off_diagonal_count",
        "mixed_topology_collision",
        "selected_p",
        "selected_q",
        "audit_p",
        "audit_q",
        "selected_row_topology",
        "upper_capacity_margin",
        "lower_capacity_margin",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_pgspg_law_matrix_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated PGSPG law rows."""
    fieldnames = [
        "case_id",
        "N",
        "law",
        "law_family",
        "law_statement",
        "law_holds",
        "survivor_count",
        "audit_role",
        "lower_reset_endpoint",
        "upper_reset_endpoint",
        "audit_p",
        "audit_q",
        "selected_row_topology",
        "lower_deadline_kind",
        "upper_deadline_kind",
        "lower_threat_present",
        "upper_threat_present",
        "lower_lock_carrier_d",
        "upper_lock_carrier_d",
        "lower_tail_count",
        "upper_tail_count",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_directed_reset_replay_matrix_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    """Write LF-terminated directed reset replay rows."""
    fieldnames = [
        "case_id",
        "N",
        "direction",
        "survivor_count",
        "audit_role",
        "source_reset_endpoint",
        "target_reset_endpoint",
        "audit_p",
        "audit_q",
        "endpoint_transport",
        "endpoint_replay_state",
        "deadline_transport",
        "deadline_replay_state",
        "deadline_kind_replay_state",
        "carrier_replay_state",
        "threat_replay_state",
        "tail_replay_state",
        "first_divergence_stage",
        "selected_row_topology",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_none_none_replay_alias_csv(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    """Write LF-terminated none/none replay alias rows."""
    fieldnames = [
        "case_id",
        "N",
        "audit_role",
        "selected_p",
        "selected_q",
        "audit_p",
        "audit_q",
        "survivor_count",
        "diagonal_echo_count",
        "off_diagonal_count",
        "mixed_topology_collision",
        "selected_row_topology",
        "replay_cycle_kind",
        "same_reset_signature",
        "same_lock_carrier_d",
        "same_tail_offsets",
        "both_chambers_inside",
        "one_sided_chamber_containment",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, row: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def audit_factors_by_n(
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[int, tuple[int, int]]:
    """Return classical factors indexed by public modulus."""
    factors: dict[int, tuple[int, int]] = {}
    for p_value, q_value in prime_pairs(max_factor):
        factors[p_value * q_value] = (p_value, q_value)
    return factors


def validate_inference_row(
    row: dict[str, object],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[str, object]:
    """Classically validate one inference row."""
    n_value = int(row["N"])
    factors = audit_factors_by_n(max_factor).get(n_value)
    if factors is None:
        raise ValueError(f"N={n_value} is outside the bounded audit surface")

    p_value, q_value = factors
    inferred_p = row.get("p")
    inferred_q = row.get("q")
    audit_status = "unresolved"
    if row.get("status") == "resolved":
        if (int(inferred_p), int(inferred_q)) == (p_value, q_value):
            audit_status = "audit_pass"
        else:
            audit_status = "audit_fail"

    return {
        "case_id": str(row.get("case_id", "")),
        "N": n_value,
        "audit_p": p_value,
        "audit_q": q_value,
        "inference_status": str(row["status"]),
        "inferred_p": "" if inferred_p is None else int(inferred_p),
        "inferred_q": "" if inferred_q is None else int(inferred_q),
        "audit_status": audit_status,
    }


def validate_inference_rows(
    rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Classically validate inference rows."""
    return [validate_inference_row(row, max_factor=max_factor) for row in rows]


def decision_knob_validity(knob: str) -> tuple[bool, str]:
    """Return whether one knob is allowed inside the PGS factorizer."""
    if knob == "pgs_endpoint_lock":
        return True, "public mutual reciprocal endpoint lock"
    if knob == "upper_native_width_dominance":
        return False, "candidate public PGSPG invariant, validator-side only"
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return False, "staged validator-only candidate after endpoint lock"
    if knob == "reciprocal_floor_boundary_lock":
        return False, "divisibility-adjacent reciprocal cell boundary"
    return True, "public PGSPG certificate diagnostic"


def survivor_passes_knob(row: dict[str, object], knob: str) -> bool:
    """Return whether one survivor row passes a decision knob."""
    if knob == "pgs_endpoint_lock":
        return bool(row["mutual_reciprocal_endpoint_lock"])
    if knob == "upper_native_width_dominance":
        return upper_native_width_dominance(row)
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return upper_native_width_dominance(row)
    if knob == "reciprocal_floor_boundary_lock":
        n_value = int(row["N"])
        lower_endpoint = int(row["lower_reset_endpoint"])
        upper_endpoint = int(row["upper_reset_endpoint"])
        return (n_value - 1) // lower_endpoint < upper_endpoint
    if knob == "both_chambers_inside":
        return (
            bool(row["upper_chamber_inside_lower_image"])
            and bool(row["lower_chamber_inside_upper_image"])
        )
    if knob == "reset_signature_equal":
        return str(row["lower_reset_signature"]) == str(row["upper_reset_signature"])
    if knob == "carrier_lock_equal":
        return str(row["lower_lock_carrier_d"]) == str(row["upper_lock_carrier_d"])
    raise ValueError(f"unknown decision knob: {knob}")


def rule_family(knob: str) -> str:
    """Return the validator-side family label for one rule."""
    if knob == "pgs_endpoint_lock":
        return "endpoint_lock"
    if knob == "upper_native_width_dominance":
        return "one_sided_capacity"
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return "staged_one_sided_capacity"
    if knob == "reciprocal_floor_boundary_lock":
        return "divisibility_adjacent_boundary"
    if knob == "both_chambers_inside":
        return "reciprocal_image_containment"
    if knob == "reset_signature_equal":
        return "reset_signature_compatibility"
    if knob == "carrier_lock_equal":
        return "carrier_compatibility"
    raise ValueError(f"unknown decision knob: {knob}")


def upper_native_width_dominance(row: dict[str, object]) -> bool:
    """Return the validator-side upper native width dominance candidate."""
    upper_native_width = int(row["upper_reset_deadline_value"]) - int(
        row["upper_anchor"]
    )
    upper_image_width = int(row["upper_chamber_image_max"]) - int(
        row["upper_chamber_image_min"]
    )
    return upper_native_width >= upper_image_width


def diagonal_echo(row: dict[str, object]) -> bool:
    """Return whether one survivor is a public lower/upper echo."""
    return (
        int(row["lower_reset_endpoint"]) == int(row["upper_reset_endpoint"])
        and int(row["lower_anchor"]) == int(row["upper_anchor"])
        and int(row["lower_reset_deadline_value"])
        == int(row["upper_reset_deadline_value"])
        and str(row["lower_reset_signature"]) == str(row["upper_reset_signature"])
        and str(row["lower_lock_carrier_d"]) == str(row["upper_lock_carrier_d"])
    )


def topology_counts(rows: list[dict[str, object]]) -> tuple[int, int]:
    """Return diagonal echo and off-diagonal counts for one survivor set."""
    diagonal_count = sum(1 for row in rows if diagonal_echo(row))
    return diagonal_count, len(rows) - diagonal_count


def survivor_topology(row: dict[str, object]) -> str:
    """Return the public topology label for one survivor."""
    if diagonal_echo(row):
        return "diagonal_echo"
    return "off_diagonal"


def capacity_margins(row: dict[str, object]) -> tuple[int, int]:
    """Return upper and lower native-minus-image width margins."""
    upper_native_width = int(row["upper_reset_deadline_value"]) - int(
        row["upper_anchor"]
    )
    upper_image_width = int(row["upper_chamber_image_max"]) - int(
        row["upper_chamber_image_min"]
    )
    lower_native_width = int(row["lower_reset_deadline_value"]) - int(
        row["lower_anchor"]
    )
    lower_image_width = int(row["lower_chamber_image_max"]) - int(
        row["lower_chamber_image_min"]
    )
    return upper_native_width - upper_image_width, lower_native_width - lower_image_width


def reset_signature_field(signature: str, field: str) -> str:
    """Return one public reset-signature field."""
    prefix = f"{field}="
    for item in signature.split(";"):
        if item.startswith(prefix):
            return item[len(prefix) :]
    return ""


def reset_deadline_kind(row: dict[str, object], side: str) -> str:
    """Return one side's reset-deadline kind."""
    return reset_signature_field(str(row[f"{side}_reset_signature"]), "deadline")


def reset_threat_present(row: dict[str, object], side: str) -> bool:
    """Return one side's public threat-presence state."""
    return reset_signature_field(str(row[f"{side}_reset_signature"]), "threat") == "True"


def bidirectional_containment(row: dict[str, object]) -> bool:
    """Return whether both transported chambers sit inside reciprocal images."""
    return (
        bool(row["upper_chamber_inside_lower_image"])
        and bool(row["lower_chamber_inside_upper_image"])
    )


def endpoint_lock_state(case_survivors: list[dict[str, object]]) -> str:
    """Return the endpoint-lock survivor-set state."""
    if not case_survivors:
        return "no_survivor"
    if len(case_survivors) == 1:
        return "singleton"
    return "ambiguous"


def containment_state(case_survivors: list[dict[str, object]]) -> str:
    """Return aggregate reciprocal image containment counts."""
    both = 0
    upper_only = 0
    lower_only = 0
    neither = 0
    for survivor in case_survivors:
        upper_inside = bool(survivor["upper_chamber_inside_lower_image"])
        lower_inside = bool(survivor["lower_chamber_inside_upper_image"])
        if upper_inside and lower_inside:
            both += 1
        elif upper_inside:
            upper_only += 1
        elif lower_inside:
            lower_only += 1
        else:
            neither += 1
    return (
        f"both={both};upper_only={upper_only};"
        f"lower_only={lower_only};neither={neither}"
    )


def signature_compatibility_state(case_survivors: list[dict[str, object]]) -> str:
    """Return aggregate reset signature compatibility counts."""
    equal = sum(
        1
        for survivor in case_survivors
        if str(survivor["lower_reset_signature"])
        == str(survivor["upper_reset_signature"])
    )
    return f"equal={equal};unequal={len(case_survivors) - equal}"


def carrier_compatibility_state(case_survivors: list[dict[str, object]]) -> str:
    """Return aggregate carrier lock compatibility counts."""
    equal = sum(
        1
        for survivor in case_survivors
        if str(survivor["lower_lock_carrier_d"])
        == str(survivor["upper_lock_carrier_d"])
    )
    return f"equal={equal};unequal={len(case_survivors) - equal}"


def staged_upper_width_passing(
    case_survivors: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return staged upper-width selections from one survivor set."""
    if len(case_survivors) == 1:
        return case_survivors
    return [
        survivor
        for survivor in case_survivors
        if upper_native_width_dominance(survivor)
    ]


def passing_survivors_for_knob(
    case_survivors: list[dict[str, object]],
    knob: str,
) -> list[dict[str, object]]:
    """Return the rows passing one validator-side rule."""
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return staged_upper_width_passing(case_survivors)
    return [
        survivor
        for survivor in case_survivors
        if survivor_passes_knob(survivor, knob)
    ]


def structural_candidate_kind(candidate: str) -> str:
    """Return whether one structural candidate selects rows or blocks a class."""
    if candidate.endswith("_blocker"):
        return "blocker"
    return "selector"


def pgspg_law_family(law: str) -> str:
    """Return the PGSPG source family for one law probe."""
    if law in {
        "reset_signature_echo",
        "deadline_kind_echo",
        "tail_offsets_echo",
        "tail_count_echo",
    }:
        return "search_interval_reset"
    if law in {"threat_presence_echo", "lock_carrier_echo"}:
        return "carrier_threat_lock"
    if law in {
        "bidirectional_chamber_containment",
        "one_sided_chamber_containment",
    }:
        return "reciprocal_chamber_transport"
    raise ValueError(f"unknown PGSPG law: {law}")


def pgspg_law_statement(law: str) -> str:
    """Return the public PGSPG statement behind one law probe."""
    if law == "reset_signature_echo":
        return "transported certificates expose the same reset signature"
    if law == "deadline_kind_echo":
        return "transported certificates close by the same reset-deadline kind"
    if law == "threat_presence_echo":
        return "transported certificates agree on lower-divisor threat presence"
    if law == "lock_carrier_echo":
        return "transported certificates agree on locked carrier divisor count"
    if law == "tail_offsets_echo":
        return "transported certificates expose the same post-reset tail offsets"
    if law == "tail_count_echo":
        return "transported certificates expose the same post-reset tail count"
    if law == "bidirectional_chamber_containment":
        return "each native chamber is contained in the reciprocal image of the other"
    if law == "one_sided_chamber_containment":
        return "exactly one native chamber is contained in the reciprocal image of the other"
    raise ValueError(f"unknown PGSPG law: {law}")


def pgspg_law_holds(row: dict[str, object], law: str) -> bool:
    """Return whether one public survivor row satisfies a PGSPG law probe."""
    if law == "reset_signature_echo":
        return str(row["lower_reset_signature"]) == str(row["upper_reset_signature"])
    if law == "deadline_kind_echo":
        return reset_deadline_kind(row, "lower") == reset_deadline_kind(row, "upper")
    if law == "threat_presence_echo":
        return reset_threat_present(row, "lower") == reset_threat_present(row, "upper")
    if law == "lock_carrier_echo":
        return str(row["lower_lock_carrier_d"]) == str(row["upper_lock_carrier_d"])
    if law == "tail_offsets_echo":
        return tuple(row["lower_tail_after_reset_offsets"]) == tuple(
            row["upper_tail_after_reset_offsets"]
        )
    if law == "tail_count_echo":
        return len(row["lower_tail_after_reset_offsets"]) == len(
            row["upper_tail_after_reset_offsets"]
        )
    if law == "bidirectional_chamber_containment":
        return bidirectional_containment(row)
    if law == "one_sided_chamber_containment":
        return bool(row["upper_chamber_inside_lower_image"]) != bool(
            row["lower_chamber_inside_upper_image"]
        )
    raise ValueError(f"unknown PGSPG law: {law}")


def replay_relation_to_target_chamber(
    value: int,
    target_anchor: int,
    target_deadline: int,
) -> str:
    """Return where one transported coordinate lands against a target chamber."""
    if value < target_anchor:
        return "before_target_anchor"
    if value > target_deadline:
        return "after_target_deadline"
    return "inside_target_chamber"


def replay_tail_state(row: dict[str, object], source: str, target: str) -> str:
    """Return how source post-reset tail transports into the target chamber."""
    tail_offsets = [int(offset) for offset in row[f"{source}_tail_after_reset_offsets"]]
    if not tail_offsets:
        return "no_source_tail"
    n_value = int(row["N"])
    source_anchor = int(row[f"{source}_anchor"])
    target_anchor = int(row[f"{target}_anchor"])
    target_deadline = int(row[f"{target}_reset_deadline_value"])
    states = {
        replay_relation_to_target_chamber(
            n_value // (source_anchor + offset),
            target_anchor,
            target_deadline,
        )
        for offset in tail_offsets
    }
    if len(states) == 1:
        return next(iter(states))
    return "mixed_tail_transport"


def replay_threat_state(row: dict[str, object], source: str, target: str) -> str:
    """Return how source lower-divisor threat transports into target chamber."""
    threat_offset = row[f"{source}_d_threat_offset"]
    if threat_offset is None:
        return "no_source_threat"
    n_value = int(row["N"])
    source_anchor = int(row[f"{source}_anchor"])
    target_anchor = int(row[f"{target}_anchor"])
    target_deadline = int(row[f"{target}_reset_deadline_value"])
    transported = n_value // (source_anchor + int(threat_offset))
    return replay_relation_to_target_chamber(
        transported,
        target_anchor,
        target_deadline,
    )


def directed_reset_replay(row: dict[str, object], source: str) -> dict[str, object]:
    """Return one directed PGSPG reset replay diagnostic."""
    target = "upper" if source == "lower" else "lower"
    n_value = int(row["N"])
    endpoint_transport = n_value // int(row[f"{source}_reset_endpoint"])
    target_endpoint = int(row[f"{target}_reset_endpoint"])
    endpoint_state = (
        "aligned_endpoint"
        if endpoint_transport == target_endpoint
        else "endpoint_mismatch"
    )
    deadline_transport = n_value // int(row[f"{source}_reset_deadline_value"])
    deadline_state = replay_relation_to_target_chamber(
        deadline_transport,
        int(row[f"{target}_anchor"]),
        int(row[f"{target}_reset_deadline_value"]),
    )
    deadline_kind_state = (
        "same_deadline_kind"
        if reset_deadline_kind(row, source) == reset_deadline_kind(row, target)
        else "different_deadline_kind"
    )
    carrier_state = (
        "same_lock_carrier_d"
        if str(row[f"{source}_lock_carrier_d"])
        == str(row[f"{target}_lock_carrier_d"])
        else "different_lock_carrier_d"
    )
    threat_state = replay_threat_state(row, source, target)
    tail_state = replay_tail_state(row, source, target)
    stage_checks = (
        ("endpoint_transport", endpoint_state == "aligned_endpoint"),
        ("deadline_transport", deadline_state == "inside_target_chamber"),
        ("deadline_kind", deadline_kind_state == "same_deadline_kind"),
        ("carrier_lock", carrier_state == "same_lock_carrier_d"),
        (
            "threat_transport",
            threat_state in {"inside_target_chamber", "no_source_threat"},
        ),
        (
            "tail_transport",
            tail_state in {"inside_target_chamber", "no_source_tail"},
        ),
    )
    first_divergence = "none"
    for stage, aligned in stage_checks:
        if not aligned:
            first_divergence = stage
            break
    return {
        "direction": f"{source}_to_{target}",
        "source_reset_endpoint": int(row[f"{source}_reset_endpoint"]),
        "target_reset_endpoint": target_endpoint,
        "endpoint_transport": endpoint_transport,
        "endpoint_replay_state": endpoint_state,
        "deadline_transport": deadline_transport,
        "deadline_replay_state": deadline_state,
        "deadline_kind_replay_state": deadline_kind_state,
        "carrier_replay_state": carrier_state,
        "threat_replay_state": threat_state,
        "tail_replay_state": tail_state,
        "first_divergence_stage": first_divergence,
    }


def replay_cycle_kind(row: dict[str, object]) -> str:
    """Return the public endpoint cycle kind for a clean two-way replay."""
    if int(row["lower_reset_endpoint"]) == int(row["upper_reset_endpoint"]):
        return "diagonal_self_cycle"
    return "off_diagonal_two_cycle"


def structural_law(candidate: str) -> str:
    """Return the public structural statement behind one candidate."""
    if candidate == "singleton_endpoint_lock":
        return "one public reciprocal endpoint-lock survivor closes the toy case"
    if candidate == "unique_diagonal_echo":
        return "one survivor repeats the same lower and upper reset structure"
    if candidate == "unique_bidirectional_containment":
        return "one survivor has both transported chambers inside reciprocal images"
    if candidate == "unique_bidirectional_capacity_cover":
        return "one survivor has nonnegative native-minus-image width on both sides"
    if candidate == "unique_capacity_vector_dominance":
        return "one survivor is not capacity-dominated in either public margin"
    if candidate == "unique_balanced_capacity_max":
        return "one survivor maximizes the smaller of its two public capacity margins"
    if candidate == "mixed_topology_collision_blocker":
        return "diagonal echoes and off-diagonal rows coexist in the same survivor set"
    if candidate == "no_bidirectional_containment_blocker":
        return "no survivor has both transported chambers inside reciprocal images"
    raise ValueError(f"unknown structural candidate: {candidate}")


def capacity_vector_dominates(
    challenger: dict[str, object],
    target: dict[str, object],
) -> bool:
    """Return whether challenger dominates target by public capacity margins."""
    challenger_upper, challenger_lower = capacity_margins(challenger)
    target_upper, target_lower = capacity_margins(target)
    return (
        challenger_upper >= target_upper
        and challenger_lower >= target_lower
        and (challenger_upper > target_upper or challenger_lower > target_lower)
    )


def unique_capacity_vector_dominance(
    case_survivors: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return a unique public capacity-vector survivor, if one exists."""
    undominated = [
        survivor
        for survivor in case_survivors
        if not any(
            capacity_vector_dominates(other, survivor)
            for other in case_survivors
            if other is not survivor
        )
    ]
    if len(undominated) == 1:
        return undominated
    return []


def unique_balanced_capacity_max(
    case_survivors: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return the unique survivor with the strongest weaker-side capacity."""
    if not case_survivors:
        return []
    scored = [
        (min(capacity_margins(survivor)), survivor)
        for survivor in case_survivors
    ]
    best_score = max(score for score, _survivor in scored)
    best = [survivor for score, survivor in scored if score == best_score]
    if len(best) == 1:
        return best
    return []


def structural_candidate_passing(
    case_survivors: list[dict[str, object]],
    candidate: str,
) -> list[dict[str, object]]:
    """Return selected survivors for a public structural candidate."""
    if candidate == "singleton_endpoint_lock":
        if len(case_survivors) == 1:
            return case_survivors
        return []
    if candidate == "unique_diagonal_echo":
        echoes = [survivor for survivor in case_survivors if diagonal_echo(survivor)]
        if len(echoes) == 1:
            return echoes
        return []
    if candidate == "unique_bidirectional_containment":
        contained = [
            survivor
            for survivor in case_survivors
            if bidirectional_containment(survivor)
        ]
        if len(contained) == 1:
            return contained
        return []
    if candidate == "unique_bidirectional_capacity_cover":
        covered = [
            survivor
            for survivor in case_survivors
            if capacity_margins(survivor)[0] >= 0
            and capacity_margins(survivor)[1] >= 0
        ]
        if len(covered) == 1:
            return covered
        return []
    if candidate == "unique_capacity_vector_dominance":
        return unique_capacity_vector_dominance(case_survivors)
    if candidate == "unique_balanced_capacity_max":
        return unique_balanced_capacity_max(case_survivors)
    raise ValueError(f"not a selector candidate: {candidate}")


def structural_blocker_applies(
    case_survivors: list[dict[str, object]],
    candidate: str,
) -> bool:
    """Return whether one public structural blocker applies."""
    diagonal_count, off_diagonal_count = topology_counts(case_survivors)
    if candidate == "mixed_topology_collision_blocker":
        return diagonal_count > 0 and off_diagonal_count > 0
    if candidate == "no_bidirectional_containment_blocker":
        return not any(bidirectional_containment(survivor) for survivor in case_survivors)
    raise ValueError(f"not a blocker candidate: {candidate}")


def upper_width_failure_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return every wrong staged upper-width selection."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        case_survivors = survivors_by_case.get(case_id, [])
        passing = passing_survivors_for_knob(
            case_survivors,
            "endpoint_lock_then_upper_native_width_dominance",
        )
        if len(passing) != 1:
            continue
        survivor = passing[0]
        selected = (
            int(survivor["lower_reset_endpoint"]),
            int(survivor["upper_reset_endpoint"]),
        )
        expected = factors_by_n[n_value]
        if selected == expected:
            continue
        diagonal_count, off_diagonal_count = topology_counts(case_survivors)
        upper_margin, lower_margin = capacity_margins(survivor)
        rows.append(
            {
                "case_id": case_id,
                "N": n_value,
                "audit_p": expected[0],
                "audit_q": expected[1],
                "selected_p": selected[0],
                "selected_q": selected[1],
                "survivor_count": len(case_survivors),
                "diagonal_echo_count": diagonal_count,
                "off_diagonal_count": off_diagonal_count,
                "selected_row_topology": survivor_topology(survivor),
                "upper_capacity_margin": upper_margin,
                "lower_capacity_margin": lower_margin,
                "mixed_topology_collision": diagonal_count > 0
                and off_diagonal_count > 0,
            }
        )
    return rows


def upper_width_failure_artifact(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[str, object]:
    """Return the first wrong staged upper-width selection, if present."""
    failure_rows = upper_width_failure_rows(
        inference_rows,
        survivor_rows,
        max_factor=max_factor,
    )
    if not failure_rows:
        return {
            "status": "no_failure",
            "knob": "endpoint_lock_then_upper_native_width_dominance",
            "max_audit_factor": max_factor,
            "checked_cases": len(inference_rows),
        }

    first_failure = failure_rows[0]
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)
    checked = 0
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        case_survivors = survivors_by_case.get(case_id, [])
        passing = staged_upper_width_passing(case_survivors)
        if len(passing) != 1:
            checked += 1
            continue
        checked += 1
        if case_id == first_failure["case_id"]:
            break

    return {
        **first_failure,
        "status": "failure",
        "knob": "endpoint_lock_then_upper_native_width_dominance",
        "max_audit_factor": max_factor,
        "checked_cases_before_failure": checked,
    }


def rule_action(
    passing: list[dict[str, object]],
    expected: tuple[int, int],
) -> str:
    """Return the validator-side action class for one rule outcome."""
    if len(passing) == 0:
        return "blocker"
    if len(passing) > 1:
        return "unresolved_ambiguous"
    selected = (
        int(passing[0]["lower_reset_endpoint"]),
        int(passing[0]["upper_reset_endpoint"]),
    )
    if selected == expected:
        return "positive_certificate"
    return "invalid_selector"


def rule_audit_matrix_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return one validator-side rule audit row per case and rule."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    matrix_rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        expected = factors_by_n[n_value]
        case_survivors = survivors_by_case.get(case_id, [])
        diagonal_count, off_diagonal_count = topology_counts(case_survivors)
        common = {
            "case_id": case_id,
            "N": n_value,
            "survivor_count": len(case_survivors),
            "endpoint_lock_state": endpoint_lock_state(case_survivors),
            "diagonal_echo_count": diagonal_count,
            "off_diagonal_count": off_diagonal_count,
            "mixed_topology_collision": diagonal_count > 0
            and off_diagonal_count > 0,
            "reciprocal_image_containment_state": containment_state(case_survivors),
            "signature_compatibility": signature_compatibility_state(case_survivors),
            "carrier_compatibility": carrier_compatibility_state(case_survivors),
            "audit_p": expected[0],
            "audit_q": expected[1],
        }
        for knob in DECISION_KNOBS:
            passing = passing_survivors_for_knob(case_survivors, knob)
            selected_p = ""
            selected_q = ""
            selected_topology = ""
            upper_margin: int | str = ""
            lower_margin: int | str = ""
            if len(passing) == 1:
                selected = passing[0]
                selected_p = int(selected["lower_reset_endpoint"])
                selected_q = int(selected["upper_reset_endpoint"])
                selected_topology = survivor_topology(selected)
                upper_margin, lower_margin = capacity_margins(selected)
            valid, _note = decision_knob_validity(knob)
            matrix_rows.append(
                {
                    **common,
                    "knob": knob,
                    "rule_family": rule_family(knob),
                    "valid_for_pgs_factorizer": valid,
                    "rule_action": rule_action(passing, expected),
                    "selected_p": selected_p,
                    "selected_q": selected_q,
                    "selected_row_topology": selected_topology,
                    "upper_capacity_margin": upper_margin,
                    "lower_capacity_margin": lower_margin,
                }
            )
    return matrix_rows


def structural_candidate_action(
    candidate: str,
    case_survivors: list[dict[str, object]],
    expected: tuple[int, int],
) -> tuple[str, list[dict[str, object]]]:
    """Return action and selected rows for one predeclared structural candidate."""
    if structural_candidate_kind(candidate) == "blocker":
        if structural_blocker_applies(case_survivors, candidate):
            return "structural_blocker", []
        return "not_applicable", []

    passing = structural_candidate_passing(case_survivors, candidate)
    return rule_action(passing, expected), passing


def structural_candidate_matrix_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return audit outcomes for predeclared public structural candidates."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    matrix_rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        expected = factors_by_n[n_value]
        case_survivors = survivors_by_case.get(case_id, [])
        diagonal_count, off_diagonal_count = topology_counts(case_survivors)
        for candidate in STRUCTURAL_CANDIDATES:
            action, passing = structural_candidate_action(
                candidate,
                case_survivors,
                expected,
            )
            selected_p = ""
            selected_q = ""
            selected_topology = ""
            upper_margin: int | str = ""
            lower_margin: int | str = ""
            if len(passing) == 1:
                selected = passing[0]
                selected_p = int(selected["lower_reset_endpoint"])
                selected_q = int(selected["upper_reset_endpoint"])
                selected_topology = survivor_topology(selected)
                upper_margin, lower_margin = capacity_margins(selected)
            matrix_rows.append(
                {
                    "case_id": case_id,
                    "N": n_value,
                    "candidate": candidate,
                    "candidate_kind": structural_candidate_kind(candidate),
                    "structural_law": structural_law(candidate),
                    "rule_action": action,
                    "survivor_count": len(case_survivors),
                    "endpoint_lock_state": endpoint_lock_state(case_survivors),
                    "diagonal_echo_count": diagonal_count,
                    "off_diagonal_count": off_diagonal_count,
                    "mixed_topology_collision": diagonal_count > 0
                    and off_diagonal_count > 0,
                    "selected_p": selected_p,
                    "selected_q": selected_q,
                    "audit_p": expected[0],
                    "audit_q": expected[1],
                    "selected_row_topology": selected_topology,
                    "upper_capacity_margin": upper_margin,
                    "lower_capacity_margin": lower_margin,
                }
            )
    return matrix_rows


def pgspg_law_matrix_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return validator-side outcomes for PGSPG-derived public law probes."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    matrix_rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        expected = factors_by_n[n_value]
        for survivor in survivors_by_case.get(case_id, []):
            selected = (
                int(survivor["lower_reset_endpoint"]),
                int(survivor["upper_reset_endpoint"]),
            )
            audit_role = "true_pair" if selected == expected else "false_alias"
            for law in PGSPG_LAWS:
                matrix_rows.append(
                    {
                        "case_id": case_id,
                        "N": n_value,
                        "law": law,
                        "law_family": pgspg_law_family(law),
                        "law_statement": pgspg_law_statement(law),
                        "law_holds": pgspg_law_holds(survivor, law),
                        "survivor_count": len(survivors_by_case.get(case_id, [])),
                        "audit_role": audit_role,
                        "lower_reset_endpoint": selected[0],
                        "upper_reset_endpoint": selected[1],
                        "audit_p": expected[0],
                        "audit_q": expected[1],
                        "selected_row_topology": survivor_topology(survivor),
                        "lower_deadline_kind": reset_deadline_kind(survivor, "lower"),
                        "upper_deadline_kind": reset_deadline_kind(survivor, "upper"),
                        "lower_threat_present": reset_threat_present(
                            survivor,
                            "lower",
                        ),
                        "upper_threat_present": reset_threat_present(
                            survivor,
                            "upper",
                        ),
                        "lower_lock_carrier_d": survivor["lower_lock_carrier_d"],
                        "upper_lock_carrier_d": survivor["upper_lock_carrier_d"],
                        "lower_tail_count": len(
                            survivor["lower_tail_after_reset_offsets"]
                        ),
                        "upper_tail_count": len(
                            survivor["upper_tail_after_reset_offsets"]
                        ),
                    }
                )
    return matrix_rows


def directed_reset_replay_matrix_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return directed PGSPG reset replay diagnostics for survivor rows."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    matrix_rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        expected = factors_by_n[n_value]
        for survivor in survivors_by_case.get(case_id, []):
            selected = (
                int(survivor["lower_reset_endpoint"]),
                int(survivor["upper_reset_endpoint"]),
            )
            audit_role = "true_pair" if selected == expected else "false_alias"
            common = {
                "case_id": case_id,
                "N": n_value,
                "survivor_count": len(survivors_by_case.get(case_id, [])),
                "audit_role": audit_role,
                "audit_p": expected[0],
                "audit_q": expected[1],
                "selected_row_topology": survivor_topology(survivor),
            }
            for source in ("lower", "upper"):
                matrix_rows.append(
                    {
                        **common,
                        **directed_reset_replay(survivor, source),
                    }
                )
    return matrix_rows


def none_none_replay_alias_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return rows whose directed replay has no divergence in either direction."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    rows: list[dict[str, object]] = []
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        expected = factors_by_n[n_value]
        case_survivors = survivors_by_case.get(case_id, [])
        diagonal_count, off_diagonal_count = topology_counts(case_survivors)
        for survivor in case_survivors:
            lower_replay = directed_reset_replay(survivor, "lower")
            upper_replay = directed_reset_replay(survivor, "upper")
            if (
                lower_replay["first_divergence_stage"] != "none"
                or upper_replay["first_divergence_stage"] != "none"
            ):
                continue
            selected = (
                int(survivor["lower_reset_endpoint"]),
                int(survivor["upper_reset_endpoint"]),
            )
            rows.append(
                {
                    "case_id": case_id,
                    "N": n_value,
                    "audit_role": (
                        "true_pair" if selected == expected else "false_alias"
                    ),
                    "selected_p": selected[0],
                    "selected_q": selected[1],
                    "audit_p": expected[0],
                    "audit_q": expected[1],
                    "survivor_count": len(case_survivors),
                    "diagonal_echo_count": diagonal_count,
                    "off_diagonal_count": off_diagonal_count,
                    "mixed_topology_collision": diagonal_count > 0
                    and off_diagonal_count > 0,
                    "selected_row_topology": survivor_topology(survivor),
                    "replay_cycle_kind": replay_cycle_kind(survivor),
                    "same_reset_signature": (
                        str(survivor["lower_reset_signature"])
                        == str(survivor["upper_reset_signature"])
                    ),
                    "same_lock_carrier_d": (
                        str(survivor["lower_lock_carrier_d"])
                        == str(survivor["upper_lock_carrier_d"])
                    ),
                    "same_tail_offsets": (
                        tuple(survivor["lower_tail_after_reset_offsets"])
                        == tuple(survivor["upper_tail_after_reset_offsets"])
                    ),
                    "both_chambers_inside": bidirectional_containment(survivor),
                    "one_sided_chamber_containment": (
                        bool(survivor["upper_chamber_inside_lower_image"])
                        != bool(survivor["lower_chamber_inside_upper_image"])
                    ),
                }
            )
    return rows


def summarize_decision_knob(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    knob: str,
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[str, object]:
    """Return validator-side metrics for one decision knob."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    resolved = 0
    ambiguous = 0
    no_survivor = 0
    audit_pass = 0
    audit_fail = 0
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        case_survivors = survivors_by_case.get(case_id, [])
        passing = passing_survivors_for_knob(case_survivors, knob)
        if len(passing) == 0:
            no_survivor += 1
            continue
        if len(passing) > 1:
            ambiguous += 1
            continue
        resolved += 1
        survivor = passing[0]
        if (
            int(survivor["lower_reset_endpoint"]),
            int(survivor["upper_reset_endpoint"]),
        ) == factors_by_n[n_value]:
            audit_pass += 1
        else:
            audit_fail += 1

    total = len(inference_rows)
    valid, note = decision_knob_validity(knob)
    unresolved = total - resolved
    return {
        "knob": knob,
        "valid_for_pgs_factorizer": valid,
        "validity_note": note,
        "total_cases": total,
        "resolved": resolved,
        "unresolved": unresolved,
        "ambiguous": ambiguous,
        "no_survivor": no_survivor,
        "audit_pass": audit_pass,
        "audit_fail": audit_fail,
        "resolved_precision": 0.0 if resolved == 0 else audit_pass / resolved,
        "resolution_rate": resolved / total,
    }


def decision_knob_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return validator-side decision-knob rows."""
    return [
        summarize_decision_knob(
            inference_rows,
            survivor_rows,
            knob,
            max_factor=max_factor,
        )
        for knob in DECISION_KNOBS
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate toy PGSPG inference rows.")
    parser.add_argument("--inference", type=Path, required=True)
    parser.add_argument("--survivors", type=Path)
    parser.add_argument("--max-audit-factor", type=int, default=DEFAULT_MAX_AUDIT_FACTOR)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decision-knobs-output", type=Path)
    parser.add_argument("--upper-width-failure-output", type=Path)
    parser.add_argument("--upper-width-failure-rows-output", type=Path)
    parser.add_argument("--rule-audit-matrix-output", type=Path)
    parser.add_argument("--structural-candidate-matrix-output", type=Path)
    parser.add_argument("--pgspg-law-matrix-output", type=Path)
    parser.add_argument("--directed-reset-replay-matrix-output", type=Path)
    parser.add_argument("--none-none-replay-alias-output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the classical validator."""
    args = parse_args(argv)
    inference_rows = read_jsonl(args.inference)
    survivor_rows = [] if args.survivors is None else read_jsonl(args.survivors)
    rows = validate_inference_rows(
        inference_rows,
        max_factor=args.max_audit_factor,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.output, rows)
    if args.survivors is not None and args.decision_knobs_output is not None:
        knob_rows = decision_knob_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.decision_knobs_output.parent.mkdir(parents=True, exist_ok=True)
        write_decision_knob_csv(args.decision_knobs_output, knob_rows)
    if args.survivors is not None and args.upper_width_failure_output is not None:
        failure_artifact = upper_width_failure_artifact(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.upper_width_failure_output.parent.mkdir(parents=True, exist_ok=True)
        write_json(args.upper_width_failure_output, failure_artifact)
    if (
        args.survivors is not None
        and args.upper_width_failure_rows_output is not None
    ):
        failure_rows = upper_width_failure_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.upper_width_failure_rows_output.parent.mkdir(parents=True, exist_ok=True)
        write_upper_width_failure_csv(
            args.upper_width_failure_rows_output,
            failure_rows,
        )
    if args.survivors is not None and args.rule_audit_matrix_output is not None:
        matrix_rows = rule_audit_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.rule_audit_matrix_output.parent.mkdir(parents=True, exist_ok=True)
        write_rule_audit_matrix_csv(args.rule_audit_matrix_output, matrix_rows)
    if (
        args.survivors is not None
        and args.structural_candidate_matrix_output is not None
    ):
        matrix_rows = structural_candidate_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.structural_candidate_matrix_output.parent.mkdir(parents=True, exist_ok=True)
        write_structural_candidate_matrix_csv(
            args.structural_candidate_matrix_output,
            matrix_rows,
        )
    if args.survivors is not None and args.pgspg_law_matrix_output is not None:
        matrix_rows = pgspg_law_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.pgspg_law_matrix_output.parent.mkdir(parents=True, exist_ok=True)
        write_pgspg_law_matrix_csv(args.pgspg_law_matrix_output, matrix_rows)
    if (
        args.survivors is not None
        and args.directed_reset_replay_matrix_output is not None
    ):
        matrix_rows = directed_reset_replay_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.directed_reset_replay_matrix_output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        write_directed_reset_replay_matrix_csv(
            args.directed_reset_replay_matrix_output,
            matrix_rows,
        )
    if args.survivors is not None and args.none_none_replay_alias_output is not None:
        rows = none_none_replay_alias_rows(
            inference_rows,
            survivor_rows,
            max_factor=args.max_audit_factor,
        )
        args.none_none_replay_alias_output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        write_none_none_replay_alias_csv(
            args.none_none_replay_alias_output,
            rows,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
