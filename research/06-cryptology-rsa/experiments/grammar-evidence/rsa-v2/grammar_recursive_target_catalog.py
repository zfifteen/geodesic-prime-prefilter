#!/usr/bin/env python3
"""Catalog recursive oriented target grammar around generated factor labels."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
ROOT = THIS_DIR.parents[4]
EXPERIMENTS_DIR = THIS_DIR.parents[1]
MODULUS_DIR = EXPERIMENTS_DIR / "modulus-recursive-catalogs" / "rsa-v2"
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
for import_dir in (THIS_DIR, MODULUS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from grammar_cell_expander import primes_from  # noqa: E402
from modulus_gap_grammar_probe import gap_grammar, next_endpoint, previous_endpoint  # noqa: E402


RULE_ID = "grammar_recursive_target_catalog_v1"
ORIENTATIONS = ("p_outward", "p_inward", "q_inward", "q_outward")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from one path."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON document."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    payload = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def is_higher(state: str) -> bool:
    """Return whether one reduced grammar state is higher-divisor grammar."""
    return "higher_divisor" in state


def state_class(state: str) -> str:
    """Return the low/higher class for one reduced grammar state."""
    return "H" if is_higher(state) else "L"


def row_direction_class(row: dict[str, object]) -> str:
    """Return case-level higher-divisor direction class."""
    outward = int(is_higher(str(row["p_outward"]))) + int(is_higher(str(row["q_outward"])))
    inward = int(is_higher(str(row["p_inward"]))) + int(is_higher(str(row["q_inward"])))
    if outward and inward:
        return "both"
    if outward:
        return "outward_only"
    if inward:
        return "inward_only"
    return "none"


def target_direction_class(row: dict[str, object], target_side: str) -> str:
    """Return target-local higher-divisor direction class."""
    if target_side == "p":
        outward = is_higher(str(row["p_outward"]))
        inward = is_higher(str(row["p_inward"]))
    elif target_side == "q":
        outward = is_higher(str(row["q_outward"]))
        inward = is_higher(str(row["q_inward"]))
    else:
        raise ValueError(f"unknown target side: {target_side}")
    if outward and inward:
        return "both"
    if outward:
        return "outward_only"
    if inward:
        return "inward_only"
    return "none"


def target_values(rows: list[dict[str, object]], block: int) -> dict[str, tuple[int, int]]:
    """Return generated p/q labels for each expanded compatibility row."""
    needed_by_start: dict[int, int] = {}
    for row in rows:
        start = int(row["prime_start"])
        needed = int(row["prime_left_index"]) + int(row["prime_pair_offset"]) + 1
        needed_by_start[start] = max(needed_by_start.get(start, 0), needed)

    primes_by_start = {
        start: primes_from(start, needed, block)
        for start, needed in sorted(needed_by_start.items())
    }
    values: dict[str, tuple[int, int]] = {}
    for row in rows:
        start = int(row["prime_start"])
        left_index = int(row["prime_left_index"])
        pair_offset = int(row["prime_pair_offset"])
        primes = primes_by_start[start]
        values[str(row["case_id"])] = (
            primes[left_index],
            primes[left_index + pair_offset],
        )
    return values


def side_gaps(target_value: int) -> dict[str, dict[str, object]]:
    """Return three left and three right chamber grammar payloads around one target."""
    left_1 = previous_endpoint(target_value - 1)
    if left_1 is None:
        raise ValueError(f"no left endpoint found for target {target_value}")
    left_2 = previous_endpoint(left_1 - 1)
    if left_2 is None:
        raise ValueError(f"no lag-2 left endpoint found for target {target_value}")
    left_3 = previous_endpoint(left_2 - 1)
    if left_3 is None:
        raise ValueError(f"no lag-3 left endpoint found for target {target_value}")
    right_1 = next_endpoint(target_value + 1)
    right_2 = next_endpoint(right_1 + 1)
    right_3 = next_endpoint(right_2 + 1)
    return {
        "left_lag3": gap_grammar("left_lag3", left_3, left_2),
        "left_lag2": gap_grammar("left_lag2", left_2, left_1),
        "left_lag1": gap_grammar("left_lag1", left_1, target_value),
        "right_lag1": gap_grammar("right_lag1", target_value, right_1),
        "right_lag2": gap_grammar("right_lag2", right_1, right_2),
        "right_lag3": gap_grammar("right_lag3", right_2, right_3),
    }


def oriented_gaps(target_side: str, gaps: dict[str, dict[str, object]]) -> dict[str, dict[str, object]]:
    """Return side gaps in outward/inward orientation."""
    if target_side == "p":
        return {
            "outward_lag3": gaps["left_lag3"],
            "outward_lag2": gaps["left_lag2"],
            "outward_lag1": gaps["left_lag1"],
            "inward_lag1": gaps["right_lag1"],
            "inward_lag2": gaps["right_lag2"],
            "inward_lag3": gaps["right_lag3"],
        }
    if target_side == "q":
        return {
            "outward_lag3": gaps["right_lag3"],
            "outward_lag2": gaps["right_lag2"],
            "outward_lag1": gaps["right_lag1"],
            "inward_lag1": gaps["left_lag1"],
            "inward_lag2": gaps["left_lag2"],
            "inward_lag3": gaps["left_lag3"],
        }
    raise ValueError(f"unknown target side: {target_side}")


def recursive_target_row(
    source_row: dict[str, object],
    target_side: str,
    target_value: int,
) -> dict[str, object]:
    """Return one oriented recursive target grammar row."""
    oriented = oriented_gaps(target_side, side_gaps(target_value))
    states = {
        key: str(gap["reduced_state"])
        for key, gap in oriented.items()
    }
    exact = {
        f"{key}_exact": str(gap["exact_type_key"])
        for key, gap in oriented.items()
    }
    widths = {
        f"{key}_width": int(gap["gap_width"])
        for key, gap in oriented.items()
    }
    prime_start = source_row.get("prime_start")
    prime_left_index = source_row.get("prime_left_index")
    prime_pair_offset = source_row.get("prime_pair_offset")
    row = {
        "rule_id": RULE_ID,
        "source_rule_id": str(source_row["rule_id"]),
        "case_id": str(source_row["case_id"]),
        "bits": int(source_row["bits"]),
        "surface": str(source_row["surface"]),
        "target_side": target_side,
        "target_value": str(target_value),
        "cell_key": str(source_row["cell_key"]),
        "n_context_key": str(source_row["n_context_key"]),
        "n_previous": str(source_row["n_previous"]),
        "n_containing": str(source_row["n_containing"]),
        "n_following": str(source_row["n_following"]),
        "prime_start": None if prime_start is None else int(prime_start),
        "prime_left_index": None if prime_left_index is None else int(prime_left_index),
        "prime_pair_offset": None if prime_pair_offset is None else int(prime_pair_offset),
        "prime_pair_offset_group": (
            None if source_row.get("prime_pair_offset_group") is None else str(source_row["prime_pair_offset_group"])
        ),
        "case_direction_class": row_direction_class(source_row),
        "target_direction_class": target_direction_class(source_row, target_side),
        "outward_lag3": states["outward_lag3"],
        "outward_lag2": states["outward_lag2"],
        "outward_lag1": states["outward_lag1"],
        "inward_lag1": states["inward_lag1"],
        "inward_lag2": states["inward_lag2"],
        "inward_lag3": states["inward_lag3"],
        "outward_class_signature": "|".join(
            [state_class(states["outward_lag2"]), state_class(states["outward_lag1"])]
        ),
        "inward_class_signature": "|".join(
            [state_class(states["inward_lag1"]), state_class(states["inward_lag2"])]
        ),
        "lag2_class_signature": "|".join(
            [state_class(states["outward_lag2"]), state_class(states["inward_lag2"])]
        ),
        "lag2_reduced_signature": "|".join(
            [states["outward_lag2"], states["inward_lag2"]]
        ),
        "lag3_class_signature": "|".join(
            [state_class(states["outward_lag3"]), state_class(states["inward_lag3"])]
        ),
        "lag3_reduced_signature": "|".join(
            [states["outward_lag3"], states["inward_lag3"]]
        ),
        "lag23_reduced_signature": "|".join(
            [
                states["outward_lag3"],
                states["outward_lag2"],
                states["inward_lag2"],
                states["inward_lag3"],
            ]
        ),
        "recursive_reduced_signature": "|".join(
            [
                states["outward_lag3"],
                states["outward_lag2"],
                states["outward_lag1"],
                states["inward_lag1"],
                states["inward_lag2"],
                states["inward_lag3"],
            ]
        ),
        "recursive_class_signature": "|".join(
            [
                state_class(states["outward_lag3"]),
                state_class(states["outward_lag2"]),
                state_class(states["outward_lag1"]),
                state_class(states["inward_lag1"]),
                state_class(states["inward_lag2"]),
                state_class(states["inward_lag3"]),
            ]
        ),
    }
    row.update(exact)
    row.update(widths)
    return row


def build_recursive_rows(rows: list[dict[str, object]], block: int) -> list[dict[str, object]]:
    """Return oriented recursive target grammar rows."""
    values = target_values(rows, block)
    output: list[dict[str, object]] = []
    for row in rows:
        p_value, q_value = values[str(row["case_id"])]
        output.append(recursive_target_row(row, "p", p_value))
        output.append(recursive_target_row(row, "q", q_value))
    return output


def split_key(row: dict[str, object], feature: str) -> str:
    """Return one split key for recursive target rows."""
    if feature == "cell_key+target_side+recursive_class_signature":
        return f"{row['cell_key']}|{row['target_side']}|class={row['recursive_class_signature']}"
    if feature == "cell_key+target_side+recursive_reduced_signature":
        return f"{row['cell_key']}|{row['target_side']}|reduced={row['recursive_reduced_signature']}"
    if feature == "cell_key+target_side+outward_class_signature+inward_class_signature":
        return (
            f"{row['cell_key']}|{row['target_side']}|out={row['outward_class_signature']}"
            f"|in={row['inward_class_signature']}"
        )
    if feature == "cell_key+target_side+prime_pair_offset_group+recursive_class_signature":
        return (
            f"{row['cell_key']}|{row['target_side']}|offset_group={row['prime_pair_offset_group']}"
            f"|class={row['recursive_class_signature']}"
        )
    if feature == "cell_key+target_side+lag2_class_signature":
        return f"{row['cell_key']}|{row['target_side']}|lag2_class={row['lag2_class_signature']}"
    if feature == "cell_key+target_side+lag2_reduced_signature":
        return f"{row['cell_key']}|{row['target_side']}|lag2_reduced={row['lag2_reduced_signature']}"
    if feature == "cell_key+target_side+prime_pair_offset_group+lag2_class_signature":
        return (
            f"{row['cell_key']}|{row['target_side']}|offset_group={row['prime_pair_offset_group']}"
            f"|lag2_class={row['lag2_class_signature']}"
        )
    if feature == "cell_key+target_side+lag2_reduced_signature+lag3_reduced_signature":
        return (
            f"{row['cell_key']}|{row['target_side']}|lag2_reduced={row['lag2_reduced_signature']}"
            f"|lag3_reduced={row['lag3_reduced_signature']}"
        )
    if feature == "cell_key+target_side+lag23_reduced_signature":
        return f"{row['cell_key']}|{row['target_side']}|lag23_reduced={row['lag23_reduced_signature']}"
    raise ValueError(f"unknown feature: {feature}")


def split_rows(rows: list[dict[str, object]], features: tuple[str, ...]) -> list[dict[str, object]]:
    """Return split summaries for recursive target rows."""
    output: list[dict[str, object]] = []
    for feature in features:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for row in rows:
            grouped[split_key(row, feature)].append(row)
        for key, group in sorted(grouped.items()):
            direction_counts = Counter(str(row["target_direction_class"]) for row in group)
            output.append(
                {
                    "rule_id": RULE_ID,
                    "feature": feature,
                    "key": key,
                    "case_count": len(group),
                    "target_direction_class_counts": dict(sorted(direction_counts.items())),
                    "mixed_direction": sum(1 for count in direction_counts.values() if count) > 1,
                    "case_ids": [str(row["case_id"]) for row in group],
                }
            )
    return output


def feature_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return per-feature split quality counts."""
    by_feature: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_feature[str(row["feature"])].append(row)
    output: list[dict[str, object]] = []
    for feature, group in sorted(by_feature.items()):
        repeated = [row for row in group if int(row["case_count"]) > 1]
        output.append(
            {
                "rule_id": RULE_ID,
                "feature": feature,
                "group_count": len(group),
                "singleton_group_count": sum(1 for row in group if int(row["case_count"]) == 1),
                "repeated_group_count": len(repeated),
                "repeated_mixed_group_count": sum(1 for row in repeated if row["mixed_direction"]),
                "repeated_pure_group_count": sum(1 for row in repeated if not row["mixed_direction"]),
            }
        )
    return output


def summary(target_rows: list[dict[str, object]], grouped_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact recursive catalog summary."""
    direction_counts = Counter(str(row["target_direction_class"]) for row in target_rows)
    class_counts = Counter(str(row["recursive_class_signature"]) for row in target_rows)
    feature_rows = feature_summary(grouped_rows)
    return {
        "rule_id": RULE_ID,
        "target_row_count": len(target_rows),
        "target_direction_class_counts": dict(sorted(direction_counts.items())),
        "recursive_class_signature_counts": dict(
            sorted(class_counts.items(), key=lambda item: (-item[1], item[0]))
        ),
        "feature_summaries": feature_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Catalog recursive target-side grammar.")
    parser.add_argument(
        "--rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_cell_expansion" / "expanded_compatibility_rows.jsonl",
        help="Expanded compatibility rows.",
    )
    parser.add_argument(
        "--block",
        type=int,
        default=8192,
        help="Exact divisor-count scan block for reconstructing generated labels.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_target_catalog",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the recursive target-side grammar catalog."""
    args = parse_args(argv)
    rows = read_jsonl(args.rows)
    target_rows = build_recursive_rows(rows, args.block)
    features = (
        "cell_key+target_side+recursive_class_signature",
        "cell_key+target_side+recursive_reduced_signature",
        "cell_key+target_side+outward_class_signature+inward_class_signature",
        "cell_key+target_side+prime_pair_offset_group+recursive_class_signature",
        "cell_key+target_side+lag2_class_signature",
        "cell_key+target_side+lag2_reduced_signature",
        "cell_key+target_side+prime_pair_offset_group+lag2_class_signature",
        "cell_key+target_side+lag2_reduced_signature+lag3_reduced_signature",
        "cell_key+target_side+lag23_reduced_signature",
    )
    grouped_rows = split_rows(target_rows, features)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "recursive_target_rows.jsonl", target_rows)
    write_jsonl(args.output_dir / "recursive_split_rows.jsonl", grouped_rows)
    write_jsonl(args.output_dir / "feature_summary_rows.jsonl", feature_summary(grouped_rows))
    payload = summary(target_rows, grouped_rows)
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
