#!/usr/bin/env python3
"""Build a gap-grammar compatibility catalog from measured evidence rows."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "grammar_compatibility_catalog_v1"
ORIENTATIONS = ("p_outward", "p_inward", "q_inward", "q_outward")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def is_higher(state: str) -> bool:
    """Return whether one reduced grammar state is higher-divisor grammar."""
    return "higher_divisor" in state


def n_context_key(row: dict[str, object]) -> str:
    """Return the three-chamber public N grammar context key."""
    return "|".join(
        [
            str(row["n_previous"]),
            str(row["n_containing"]),
            str(row["n_following"]),
        ]
    )


def low_regime_rows(path: Path) -> list[dict[str, object]]:
    """Return normalized compatibility rows from the exact low-regime catalog."""
    rows: list[dict[str, object]] = []
    for source in read_jsonl(path):
        normalized = {
            "rule_id": RULE_ID,
            "source_rule_id": source["rule_id"],
            "surface": "exact_low_regime",
            "case_id": source["case_id"],
            "bits": source["bits"],
            "public_status": "exact_closed",
            "n_previous": source["n_previous"],
            "n_containing": source["n_containing"],
            "n_following": source["n_following"],
            "n_previous_exact": source["n_previous_exact"],
            "n_containing_exact": source["n_containing_exact"],
            "n_following_exact": source["n_following_exact"],
            "p_outward": source["p_left"],
            "p_inward": source["p_right"],
            "q_inward": source["q_left"],
            "q_outward": source["q_right"],
            "p_outward_exact": source["p_left_exact"],
            "p_inward_exact": source["p_right_exact"],
            "q_inward_exact": source["q_left_exact"],
            "q_outward_exact": source["q_right_exact"],
            "unresolved_public_roles": [],
        }
        normalized["n_context_key"] = n_context_key(normalized)
        normalized["target_orientation_key"] = "|".join(
            str(normalized[orientation]) for orientation in ORIENTATIONS
        )
        rows.append(normalized)
    return rows


def rsa_challenge_rows(public_path: Path, target_path: Path) -> list[dict[str, object]]:
    """Return normalized compatibility rows from solved RSA challenge grammar outputs."""
    public_by_case: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in read_jsonl(public_path):
        public_by_case[str(row["case_id"])][str(row["role"])] = row

    target_by_case: dict[str, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in read_jsonl(target_path):
        target_by_case[str(row["case_id"])][str(row["role"])] = row

    rows: list[dict[str, object]] = []
    for case_id in sorted(public_by_case):
        public = public_by_case[case_id]
        target = target_by_case[case_id]
        if not {"n_previous", "n_containing", "n_following"}.issubset(public):
            continue
        if not {"p_left", "p_right", "q_left", "q_right"}.issubset(target):
            continue

        unresolved_roles = [
            role
            for role in ("n_previous", "n_containing", "n_following")
            if public[role]["status"] != "exact_closed"
        ]
        normalized = {
            "rule_id": RULE_ID,
            "source_rule_id": public["n_containing"]["rule_id"],
            "surface": "rsa_challenge",
            "case_id": case_id,
            "bits": public["n_containing"]["bits"],
            "public_status": (
                "exact_closed" if not unresolved_roles else "unresolved_public_context"
            ),
            "n_previous": public["n_previous"]["reduced_state"],
            "n_containing": public["n_containing"]["reduced_state"],
            "n_following": public["n_following"]["reduced_state"],
            "n_previous_exact": public["n_previous"]["exact_type_key"],
            "n_containing_exact": public["n_containing"]["exact_type_key"],
            "n_following_exact": public["n_following"]["exact_type_key"],
            "p_outward": target["p_left"]["reduced_state"],
            "p_inward": target["p_right"]["reduced_state"],
            "q_inward": target["q_left"]["reduced_state"],
            "q_outward": target["q_right"]["reduced_state"],
            "p_outward_exact": target["p_left"]["exact_type_key"],
            "p_inward_exact": target["p_right"]["exact_type_key"],
            "q_inward_exact": target["q_left"]["exact_type_key"],
            "q_outward_exact": target["q_right"]["exact_type_key"],
            "unresolved_public_roles": unresolved_roles,
        }
        normalized["n_context_key"] = n_context_key(normalized)
        normalized["target_orientation_key"] = "|".join(
            str(normalized[orientation]) for orientation in ORIENTATIONS
        )
        rows.append(normalized)
    return rows


def count_rows(counter: Counter[str], key_name: str) -> list[dict[str, object]]:
    """Return sorted count rows for one counter."""
    return [
        {key_name: key, "count": count}
        for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    ]


def observed_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed N-context to oriented target-state rows."""
    counter: Counter[tuple[str, str, str]] = Counter()
    examples: dict[tuple[str, str, str], str] = {}
    for row in rows:
        for orientation in ORIENTATIONS:
            key = (str(row["n_context_key"]), orientation, str(row[orientation]))
            counter[key] += 1
            examples.setdefault(key, str(row["case_id"]))
    return [
        {
            "rule_id": RULE_ID,
            "n_context_key": key[0],
            "orientation": key[1],
            "target_state": key[2],
            "count": count,
            "example_case_id": examples[key],
        }
        for key, count in sorted(counter.items(), key=lambda item: (item[0][0], item[0][1], item[0][2]))
    ]


def absence_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return measured absence rows for future PGS incompatibility review."""
    states_by_orientation: dict[str, set[str]] = {orientation: set() for orientation in ORIENTATIONS}
    observed_by_context: dict[tuple[str, str], set[str]] = defaultdict(set)
    context_counts: Counter[str] = Counter()
    for row in rows:
        context = str(row["n_context_key"])
        context_counts[context] += 1
        for orientation in ORIENTATIONS:
            state = str(row[orientation])
            states_by_orientation[orientation].add(state)
            observed_by_context[(context, orientation)].add(state)

    output: list[dict[str, object]] = []
    for context in sorted(context_counts):
        for orientation in ORIENTATIONS:
            observed = observed_by_context[(context, orientation)]
            for state in sorted(states_by_orientation[orientation] - observed):
                output.append(
                    {
                        "rule_id": RULE_ID,
                        "n_context_key": context,
                        "orientation": orientation,
                        "target_state": state,
                        "context_case_count": context_counts[context],
                        "status": "not_observed_on_measured_surface",
                    }
                )
    return output


def summarize(rows: list[dict[str, object]], observed: list[dict[str, object]], absent: list[dict[str, object]]) -> dict[str, object]:
    """Return compact compatibility-catalog summary."""
    n_containing = Counter(str(row["n_containing"]) for row in rows)
    n_context = Counter(str(row["n_context_key"]) for row in rows)
    orientation_higher = {
        orientation: sum(1 for row in rows if is_higher(str(row[orientation])))
        for orientation in ORIENTATIONS
    }
    outward_higher = orientation_higher["p_outward"] + orientation_higher["q_outward"]
    inward_higher = orientation_higher["p_inward"] + orientation_higher["q_inward"]
    return {
        "rule_id": RULE_ID,
        "case_count": len(rows),
        "surface_counts": count_rows(Counter(str(row["surface"]) for row in rows), "surface"),
        "public_unresolved_context_count": sum(
            1 for row in rows if row["public_status"] != "exact_closed"
        ),
        "n_containing_state_counts": count_rows(n_containing, "state"),
        "n_context_count": len(n_context),
        "n_context_counts": count_rows(n_context, "n_context_key"),
        "observed_compatibility_count": len(observed),
        "measured_absence_count": len(absent),
        "orientation_higher_counts": orientation_higher,
        "outward_higher_count": outward_higher,
        "inward_higher_count": inward_higher,
        "outward_fraction": (
            None if outward_higher + inward_higher == 0 else outward_higher / (outward_higher + inward_higher)
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build measured gap-grammar compatibility rows.")
    parser.add_argument(
        "--low-regime-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_evidence" / "exact_low_regime_grammar_rows.jsonl",
        help="Exact low-regime grammar evidence rows.",
    )
    parser.add_argument(
        "--rsa-public-rows",
        type=Path,
        default=THIS_DIR / "output" / "rsa_challenge_exact_grammar" / "public_grammar_rows.jsonl",
        help="Solved RSA challenge public grammar rows.",
    )
    parser.add_argument(
        "--rsa-target-rows",
        type=Path,
        default=THIS_DIR / "output" / "rsa_challenge_exact_grammar" / "target_grammar_rows.jsonl",
        help="Solved RSA challenge target grammar rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "grammar_compatibility",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the compatibility catalog builder."""
    args = parse_args(argv)
    rows = low_regime_rows(args.low_regime_rows)
    rows.extend(rsa_challenge_rows(args.rsa_public_rows, args.rsa_target_rows))
    observed = observed_rows(rows)
    absent = absence_rows(rows)
    summary = summarize(rows, observed, absent)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "compatibility_rows.jsonl", rows)
    write_jsonl(args.output_dir / "observed_compatibility_rows.jsonl", observed)
    write_jsonl(args.output_dir / "measured_absence_rows.jsonl", absent)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
