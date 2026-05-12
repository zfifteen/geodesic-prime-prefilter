#!/usr/bin/env python3
"""Measure public modulus gap grammar and downstream target-side correlations."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from run_experiment import (  # noqa: E402
    LadderCase,
    divisor_counts_segment,
    load_cases,
    previous_endpoint,
    read_jsonl,
)


RULE_ID = "modulus_gap_grammar_correlation_v1"
SCAN_BLOCK = 128
FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
DEFAULT_MAX_CASE_BITS = 62


@dataclass(frozen=True)
class LabeledTarget:
    """One downstream target coordinate used only after public grammar exists."""

    case_id: str
    side: str
    value: gmpy2.mpz


@dataclass(frozen=True)
class LabeledCase:
    """One known target-labeled modulus row for downstream cataloging."""

    case_id: str
    bits: int
    n: gmpy2.mpz
    p: gmpy2.mpz
    q: gmpy2.mpz
    source: str
    family: str | None


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def next_endpoint(value: gmpy2.mpz, block: int = SCAN_BLOCK) -> gmpy2.mpz:
    """Return the first public endpoint at or after one coordinate."""
    if block < 1:
        raise ValueError("block must be positive")
    lo = int(value)
    while True:
        hi = lo + block
        counts = divisor_counts_segment(lo, hi)
        for index, raw_count in enumerate(counts):
            if int(raw_count) == 2:
                return gmpy2.mpz(lo + index)
        lo = hi


def first_open_offset(left_endpoint: gmpy2.mpz) -> int:
    """Return the first wheel-open even offset after one endpoint."""
    residue = int(left_endpoint % 30)
    for offset in FIRST_OPEN_OFFSETS:
        candidate = (residue + offset) % 30
        if candidate not in (0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27):
            return offset
    raise RuntimeError(f"no wheel-open offset found after residue {residue}")


def divisor_bucket(divisor_count: int | None) -> str:
    """Return the reduced grammar divisor bucket."""
    if divisor_count is None:
        return "empty"
    if divisor_count <= 4:
        return "d<=4"
    if divisor_count <= 16:
        return "5<=d<=16"
    if divisor_count <= 64:
        return "17<=d<=64"
    return "d>64"


def carrier_family(value: gmpy2.mpz | None, divisor_count: int | None) -> str:
    """Return the PGS carrier family without splitting hidden d=4 subfamilies."""
    if value is None or divisor_count is None:
        return "empty"
    if divisor_count == 3:
        return "prime_square"
    if divisor_count == 4:
        if int(value % 2) == 0:
            return "d4_even"
        return "d4_odd"
    if int(value % 2) == 0:
        return "higher_divisor_even"
    return "higher_divisor_odd"


def gap_grammar(
    role: str,
    left_endpoint: gmpy2.mpz,
    right_endpoint: gmpy2.mpz,
    coordinate: gmpy2.mpz | None = None,
) -> dict[str, object]:
    """Return one deterministic PGS gap grammar payload."""
    width = int(right_endpoint - left_endpoint)
    interior_count = max(0, width - 1)
    first_open = first_open_offset(left_endpoint)
    contains_coordinate = (
        coordinate is not None
        and left_endpoint < coordinate < right_endpoint
    )

    if interior_count == 0:
        return {
            "role": role,
            "left_endpoint": str(left_endpoint),
            "right_endpoint": str(right_endpoint),
            "gap_width": width,
            "contains_coordinate": contains_coordinate,
            "coordinate_offset_from_left": None,
            "coordinate_offset_from_right": None,
            "first_open_offset": first_open,
            "winner_value": None,
            "winner_offset": None,
            "winner_d": None,
            "carrier_family": "empty",
            "exact_type_key": f"o{first_open}_empty",
            "reduced_state": f"o{first_open}_empty|empty",
        }

    counts = [
        int(value)
        for value in divisor_counts_segment(int(left_endpoint + 1), int(right_endpoint))
    ]
    winner_d = min(counts)
    winner_index = counts.index(winner_d)
    winner_offset = winner_index + 1
    winner_value = left_endpoint + winner_offset
    family = carrier_family(winner_value, winner_d)
    exact_type_key = f"o{first_open}_d{winner_d}_a{winner_offset}_{family}"
    reduced_state = f"o{first_open}_{family}|{divisor_bucket(winner_d)}"

    return {
        "role": role,
        "left_endpoint": str(left_endpoint),
        "right_endpoint": str(right_endpoint),
        "gap_width": width,
        "contains_coordinate": contains_coordinate,
        "coordinate_offset_from_left": (
            None if coordinate is None else int(coordinate - left_endpoint)
        ),
        "coordinate_offset_from_right": (
            None if coordinate is None else int(right_endpoint - coordinate)
        ),
        "first_open_offset": first_open,
        "winner_value": str(winner_value),
        "winner_offset": winner_offset,
        "winner_d": winner_d,
        "carrier_family": family,
        "exact_type_key": exact_type_key,
        "reduced_state": reduced_state,
    }


def neighboring_gaps(coordinate: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    """Return previous, left, right, and following endpoints around one coordinate."""
    left = previous_endpoint(coordinate - 1)
    if left is None:
        raise ValueError(f"no left endpoint found for {coordinate}")
    right = next_endpoint(coordinate + 1)
    previous = previous_endpoint(left - 1)
    if previous is None:
        raise ValueError(f"no previous endpoint found for {coordinate}")
    following = next_endpoint(right + 1)
    return previous, left, right, following


def public_grammar_row(case: LadderCase) -> dict[str, object]:
    """Return one public grammar row around the modulus coordinate."""
    previous, left, right, following = neighboring_gaps(case.n)
    previous_gap = gap_grammar("previous", previous, left)
    containing_gap = gap_grammar("containing", left, right, case.n)
    following_gap = gap_grammar("following", right, following)
    return {
        "case_id": case.case_id,
        "bits": case.bits,
        "N": str(case.n),
        "rule_id": RULE_ID,
        "n_previous_gap_reduced_state": previous_gap["reduced_state"],
        "n_containing_gap_reduced_state": containing_gap["reduced_state"],
        "n_following_gap_reduced_state": following_gap["reduced_state"],
        "n_previous_gap_exact_type_key": previous_gap["exact_type_key"],
        "n_containing_gap_exact_type_key": containing_gap["exact_type_key"],
        "n_following_gap_exact_type_key": following_gap["exact_type_key"],
        "n_containing_gap_width": containing_gap["gap_width"],
        "n_offset_from_left": containing_gap["coordinate_offset_from_left"],
        "n_offset_from_right": containing_gap["coordinate_offset_from_right"],
        "gaps": [previous_gap, containing_gap, following_gap],
    }


def load_labeled_targets(path: Path) -> list[LabeledTarget]:
    """Load downstream target labels from a physically separate file."""
    targets: list[LabeledTarget] = []
    for row in read_jsonl(path):
        targets.append(
            LabeledTarget(
                case_id=str(row["case_id"]),
                side="p",
                value=gmpy2.mpz(str(row["p"])),
            )
        )
        targets.append(
            LabeledTarget(
                case_id=str(row["case_id"]),
                side="q",
                value=gmpy2.mpz(str(row["q"])),
            )
        )
    return targets


def labeled_case_rows_from_payload(path: Path) -> list[LabeledCase]:
    """Load known target-labeled modulus rows from JSON or JSONL."""
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix == ".jsonl":
        raw_rows = read_jsonl(path)
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            raw_rows = payload
        elif isinstance(payload, dict) and all(isinstance(value, list) for value in payload.values()):
            raw_rows = []
            for rows in payload.values():
                raw_rows.extend(rows)
        else:
            raise ValueError(f"unsupported labeled corpus shape: {path}")

    cases: list[LabeledCase] = []
    for index, row in enumerate(raw_rows):
        if not {"p", "q"}.issubset(row):
            continue
        n_text = row.get("n", row.get("N"))
        if n_text is None:
            continue
        n_value = gmpy2.mpz(str(n_text))
        p_value = gmpy2.mpz(str(row["p"]))
        q_value = gmpy2.mpz(str(row["q"]))
        case_id = str(row.get("case_id", f"{path.stem}_{index + 1}"))
        cases.append(
            LabeledCase(
                case_id=case_id,
                bits=int(row.get("case_bits", row.get("bits", n_value.bit_length()))),
                n=n_value,
                p=p_value,
                q=q_value,
                source=str(path),
                family=None if row.get("family") is None else str(row["family"]),
            )
        )
    return cases


def load_labeled_cases(paths: list[Path], max_case_bits: int) -> list[LabeledCase]:
    """Load and de-duplicate supported known target-labeled modulus rows."""
    seen: set[tuple[str, str]] = set()
    cases: list[LabeledCase] = []
    for path in paths:
        for row in labeled_case_rows_from_payload(path):
            if row.bits > max_case_bits:
                continue
            key = (str(row.n), str(row.p))
            if key in seen:
                continue
            seen.add(key)
            cases.append(row)
    return cases


def public_row_from_labeled_case(row: LabeledCase) -> dict[str, object]:
    """Return a public grammar row from a known labeled case without target fields."""
    return public_grammar_row(LadderCase(row.case_id, row.bits, row.n)) | {
        "catalog_source": row.source,
        "catalog_family": row.family,
    }


def targets_from_labeled_case(row: LabeledCase) -> list[LabeledTarget]:
    """Return downstream target labels from one known labeled case."""
    return [
        LabeledTarget(row.case_id, "p", row.p),
        LabeledTarget(row.case_id, "q", row.q),
    ]


def target_grammar_row(
    target: LabeledTarget,
    public_by_case: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Return one downstream target-side grammar correlation row."""
    previous = previous_endpoint(target.value - 1)
    if previous is None:
        raise ValueError(f"no previous endpoint found for target {target.case_id}")
    following = next_endpoint(target.value + 1)
    left_gap = gap_grammar("target_left", previous, target.value)
    right_gap = gap_grammar("target_right", target.value, following)
    public_row = public_by_case[target.case_id]

    n_reduced = str(public_row["n_containing_gap_reduced_state"])
    n_previous = str(public_row["n_previous_gap_reduced_state"])
    n_following = str(public_row["n_following_gap_reduced_state"])
    left_reduced = str(left_gap["reduced_state"])
    right_reduced = str(right_gap["reduced_state"])

    return {
        "case_id": target.case_id,
        "bits": public_row["bits"],
        "N": public_row["N"],
        "rule_id": RULE_ID,
        "target_side": target.side,
        "target_value": str(target.value),
        "n_containing_gap_reduced_state": n_reduced,
        "n_previous_gap_reduced_state": n_previous,
        "n_following_gap_reduced_state": n_following,
        "target_left_gap_reduced_state": left_reduced,
        "target_right_gap_reduced_state": right_reduced,
        "n_containing_matches_target_left": n_reduced == left_reduced,
        "n_containing_matches_target_right": n_reduced == right_reduced,
        "n_previous_matches_target_left": n_previous == left_reduced,
        "n_following_matches_target_right": n_following == right_reduced,
        "transition_key": f"{n_reduced} -> {left_reduced} / {right_reduced}",
        "target_left_gap": left_gap,
        "target_right_gap": right_gap,
    }


def summarize(
    public_rows: list[dict[str, object]],
    correlation_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact grammar-correlation counts."""
    transition_counts: dict[str, int] = {}
    for row in correlation_rows:
        key = str(row["transition_key"])
        transition_counts[key] = transition_counts.get(key, 0) + 1
    top_transitions = [
        {"transition_key": key, "count": count}
        for key, count in sorted(
            transition_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]

    def state_counts(key: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        """Return sorted reduced-state frequency rows."""
        counts = Counter(str(row[key]) for row in rows)
        return [
            {"state": state, "count": count}
            for state, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        ]

    return {
        "rule_id": RULE_ID,
        "public_case_count": len(public_rows),
        "target_side_row_count": len(correlation_rows),
        "public_n_containing_state_counts": state_counts(
            "n_containing_gap_reduced_state",
            public_rows,
        ),
        "public_n_previous_state_counts": state_counts(
            "n_previous_gap_reduced_state",
            public_rows,
        ),
        "public_n_following_state_counts": state_counts(
            "n_following_gap_reduced_state",
            public_rows,
        ),
        "target_left_state_counts": state_counts(
            "target_left_gap_reduced_state",
            correlation_rows,
        ),
        "target_right_state_counts": state_counts(
            "target_right_gap_reduced_state",
            correlation_rows,
        ),
        "public_n_containing_higher_divisor_count": sum(
            1
            for row in public_rows
            if "higher_divisor" in str(row["n_containing_gap_reduced_state"])
        ),
        "target_side_higher_divisor_row_count": sum(
            1
            for row in correlation_rows
            if (
                "higher_divisor" in str(row["target_left_gap_reduced_state"])
                or "higher_divisor" in str(row["target_right_gap_reduced_state"])
            )
        ),
        "n_containing_match_target_left_count": sum(
            1 for row in correlation_rows if row["n_containing_matches_target_left"]
        ),
        "n_containing_match_target_right_count": sum(
            1 for row in correlation_rows if row["n_containing_matches_target_right"]
        ),
        "n_previous_match_target_left_count": sum(
            1 for row in correlation_rows if row["n_previous_matches_target_left"]
        ),
        "n_following_match_target_right_count": sum(
            1 for row in correlation_rows if row["n_following_matches_target_right"]
        ),
        "distinct_transition_count": len(transition_counts),
        "top_transitions": top_transitions,
    }


def run_probe(
    cases_path: Path,
    target_labels_path: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run public grammar measurement and downstream target correlation."""
    cases = load_cases(cases_path)
    public_rows = [public_grammar_row(case) for case in cases]
    public_by_case = {str(row["case_id"]): row for row in public_rows}
    correlation_rows = [
        target_grammar_row(target, public_by_case)
        for target in load_labeled_targets(target_labels_path)
        if target.case_id in public_by_case
    ]
    return public_rows, correlation_rows, summarize(public_rows, correlation_rows)


def run_catalog(
    labeled_case_paths: list[Path],
    max_case_bits: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the grammar catalog over known target-labeled rows."""
    labeled_cases = load_labeled_cases(labeled_case_paths, max_case_bits)
    public_rows = [public_row_from_labeled_case(row) for row in labeled_cases]
    public_by_case = {str(row["case_id"]): row for row in public_rows}
    targets = [
        target
        for labeled_case in labeled_cases
        for target in targets_from_labeled_case(labeled_case)
    ]
    correlation_rows = [
        target_grammar_row(target, public_by_case)
        for target in targets
        if target.case_id in public_by_case
    ]
    summary = summarize(public_rows, correlation_rows)
    summary["max_case_bits"] = max_case_bits
    summary["labeled_case_source_count"] = len(labeled_case_paths)
    return public_rows, correlation_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Probe modulus-to-target gap grammar.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=THIS_DIR / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--target-labels",
        type=Path,
        default=THIS_DIR / "fixtures" / "audit_factors.jsonl",
        help="Downstream target labels JSONL path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "modulus_gap_grammar",
        help="Directory for public rows, correlation rows, and summary.",
    )
    parser.add_argument(
        "--labeled-case-source",
        action="append",
        type=Path,
        default=[],
        help="Known target-labeled JSON or JSONL corpus for catalog expansion.",
    )
    parser.add_argument(
        "--max-case-bits",
        type=int,
        default=DEFAULT_MAX_CASE_BITS,
        help="Exact grammar backend limit for catalog expansion.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar grammar probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.labeled_case_source:
        public_rows, correlation_rows, summary = run_catalog(
            args.labeled_case_source,
            args.max_case_bits,
        )
    else:
        public_rows, correlation_rows, summary = run_probe(args.cases, args.target_labels)
    write_jsonl(args.output_dir / "public_grammar_rows.jsonl", public_rows)
    write_jsonl(args.output_dir / "target_correlation_rows.jsonl", correlation_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
