#!/usr/bin/env python3
"""Project commitment-story rows onto recursive lag-2 and lag-3 words."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "commitment_story_word_projection_v1"
SIGNATURE_KEYS = (
    "lag2_reduced_signature",
    "lag3_reduced_signature",
    "lag23_reduced_signature",
    "recursive_reduced_signature",
)
LOCAL_STORY_KINDS = (
    "outward_lag3",
    "outward_lag2",
    "inward_lag2",
    "inward_lag3",
)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read a required JSONL file."""
    if not path.exists():
        raise FileNotFoundError(path)
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_optional_jsonl(path: Path) -> list[dict[str, object]]:
    """Read optional Experiment 1 story rows when they exist."""
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON document."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def expanded_signature_sets(
    expanded_rows: list[dict[str, object]],
) -> dict[str, set[str]]:
    """Return global expanded recursive signature sets."""
    return {
        key: {str(row[key]) for row in expanded_rows}
        for key in SIGNATURE_KEYS
    }


def inverse_global_index(
    inverse_rows: list[dict[str, object]],
) -> dict[tuple[str, str], dict[str, object]]:
    """Return global-scope inverse rows by case and target side."""
    output: dict[tuple[str, str], dict[str, object]] = {}
    for row in inverse_rows:
        if str(row["scope"]) != "global":
            continue
        key = (str(row["case_id"]), str(row["target_side"]))
        if key in output:
            raise ValueError(f"duplicate global inverse row for {key}")
        output[key] = row
    return output


def story_index(
    story_rows: list[dict[str, object]],
) -> dict[tuple[str, str | None], list[dict[str, object]]]:
    """Return story rows grouped by case and optional target side."""
    grouped: dict[tuple[str, str | None], list[dict[str, object]]] = defaultdict(list)
    for row in story_rows:
        target_side = None if "target_side" not in row else str(row["target_side"])
        grouped[(str(row["case_id"]), target_side)].append(row)
    return dict(grouped)


def event_rows_for(
    recursive_row: dict[str, object],
    stories: dict[tuple[str, str | None], list[dict[str, object]]],
) -> list[dict[str, object]]:
    """Return available story rows for one recursive target row."""
    case_id = str(recursive_row["case_id"])
    target_side = str(recursive_row["target_side"])
    return stories.get((case_id, target_side), stories.get((case_id, None), []))


def local_story_values(row: dict[str, object]) -> list[str]:
    """Return the minimum ordered lag-2 plus lag-3 story projection."""
    return [str(row[key]) for key in LOCAL_STORY_KINDS]


def public_target_side_index(target_side: str) -> int:
    """Return a public side index without carrying factor-side labels into output."""
    if target_side == "p":
        return 0
    if target_side == "q":
        return 1
    raise ValueError(f"unexpected target side label: {target_side}")


def projection_row(
    surface: str,
    row: dict[str, object],
    expanded_sets: dict[str, set[str]],
    inverse_rows: dict[tuple[str, str], dict[str, object]],
    stories: dict[tuple[str, str | None], list[dict[str, object]]],
    projection_source: str,
) -> dict[str, object]:
    """Return one commitment-story word projection row."""
    key = (str(row["case_id"]), str(row["target_side"]))
    if key not in inverse_rows:
        raise ValueError(f"missing global inverse row for {key}")

    inverse_row = inverse_rows[key]
    events = event_rows_for(row, stories)
    if events:
        event_kinds = [str(event.get("event_kind", "")) for event in events]
        event_values = [str(event.get("event_value", "")) for event in events]
    else:
        event_kinds = list(LOCAL_STORY_KINDS)
        event_values = local_story_values(row)

    hits = {
        "projected_lag2_hit": str(row["lag2_reduced_signature"]) in expanded_sets["lag2_reduced_signature"],
        "projected_lag3_hit": str(row["lag3_reduced_signature"]) in expanded_sets["lag3_reduced_signature"],
        "projected_lag23_collision": str(row["lag23_reduced_signature"]) in expanded_sets["lag23_reduced_signature"],
        "projected_recursive_reduced_collision": (
            str(row["recursive_reduced_signature"]) in expanded_sets["recursive_reduced_signature"]
        ),
    }
    component_piece_hit = hits["projected_lag2_hit"] or hits["projected_lag3_hit"]
    component_exclusion = component_piece_hit and not hits["projected_lag23_collision"]
    inverse_match = (
        hits["projected_lag2_hit"] == bool(inverse_row["lag2_reduced_signature_hit"])
        and hits["projected_lag3_hit"] == bool(inverse_row["lag3_reduced_signature_hit"])
        and hits["projected_lag23_collision"] == bool(inverse_row["lag23_reduced_signature_hit"])
        and hits["projected_recursive_reduced_collision"]
        == bool(inverse_row["recursive_reduced_signature_hit"])
        and component_exclusion == bool(inverse_row["component_sharing_word_exclusion"])
    )

    return {
        "rule_id": RULE_ID,
        "surface": surface,
        "projection_source": projection_source,
        "case_id": str(row["case_id"]),
        "bits": int(row["bits"]),
        "target_side_index": public_target_side_index(str(row["target_side"])),
        "target_direction_class": str(row["target_direction_class"]),
        "cell_key": str(row["cell_key"]),
        "story_event_count": len(event_kinds),
        "story_event_kinds": event_kinds,
        "story_event_values": event_values,
        "lag2_reduced_signature": str(row["lag2_reduced_signature"]),
        "lag3_reduced_signature": str(row["lag3_reduced_signature"]),
        "lag23_reduced_signature": str(row["lag23_reduced_signature"]),
        "recursive_reduced_signature": str(row["recursive_reduced_signature"]),
        "component_piece_hit": component_piece_hit,
        "component_sharing_word_exclusion": component_exclusion,
        "inverse_global_consistent": inverse_match,
    } | hits


def projection_rows(
    surface: str,
    recursive_rows: list[dict[str, object]],
    inverse_rows: dict[tuple[str, str], dict[str, object]],
    expanded_sets: dict[str, set[str]],
    stories: dict[tuple[str, str | None], list[dict[str, object]]],
    projection_source: str,
) -> list[dict[str, object]]:
    """Return projection rows for one measured recursive surface."""
    return [
        projection_row(
            surface,
            row,
            expanded_sets,
            inverse_rows,
            stories,
            projection_source,
        )
        for row in recursive_rows
    ]


def surface_summary(surface: str, rows: list[dict[str, object]]) -> dict[str, object]:
    """Return projection counts for one surface."""
    return {
        "rule_id": RULE_ID,
        "surface": surface,
        "row_count": len(rows),
        "projected_lag2_hit_count": sum(1 for row in rows if row["projected_lag2_hit"]),
        "projected_lag3_hit_count": sum(1 for row in rows if row["projected_lag3_hit"]),
        "projected_lag23_collision_count": sum(
            1 for row in rows if row["projected_lag23_collision"]
        ),
        "projected_recursive_reduced_collision_count": sum(
            1 for row in rows if row["projected_recursive_reduced_collision"]
        ),
        "component_sharing_word_exclusion_count": sum(
            1 for row in rows if row["component_sharing_word_exclusion"]
        ),
        "inverse_global_mismatch_count": sum(
            1 for row in rows if not row["inverse_global_consistent"]
        ),
    }


def summary(
    rows: list[dict[str, object]],
    story_row_count: int,
    projection_source: str,
) -> dict[str, object]:
    """Return the Experiment 3 falsification summary."""
    surfaces = sorted({str(row["surface"]) for row in rows})
    surface_summaries = [
        surface_summary(surface, [row for row in rows if str(row["surface"]) == surface])
        for surface in surfaces
    ]
    projected_lag23_collision_count = sum(
        1 for row in rows if row["projected_lag23_collision"]
    )
    fresh_rows = [row for row in rows if str(row["surface"]) == "fresh_rsa_100"]
    solved_rows = [row for row in rows if str(row["surface"]) == "solved"]
    return {
        "rule_id": RULE_ID,
        "projection_source": projection_source,
        "certificate_commitment_story_row_count": story_row_count,
        "projection_row_count": len(rows),
        "surface_summaries": surface_summaries,
        "projected_lag2_hit_count": sum(1 for row in rows if row["projected_lag2_hit"]),
        "projected_lag3_hit_count": sum(1 for row in rows if row["projected_lag3_hit"]),
        "projected_lag23_collision_count": projected_lag23_collision_count,
        "projected_recursive_reduced_collision_count": sum(
            1 for row in rows if row["projected_recursive_reduced_collision"]
        ),
        "component_sharing_word_exclusion_count": sum(
            1 for row in rows if row["component_sharing_word_exclusion"]
        ),
        "solved_lag23_collision_count": sum(
            1 for row in solved_rows if row["projected_lag23_collision"]
        ),
        "fresh_rsa_100_lag23_collision_count": sum(
            1 for row in fresh_rows if row["projected_lag23_collision"]
        ),
        "inverse_global_mismatch_count": sum(
            1 for row in rows if not row["inverse_global_consistent"]
        ),
        "status": (
            "preserved_zero_ordered_lag23_collisions"
            if projected_lag23_collision_count == 0
            else "falsified_by_projected_ordered_word_collision"
        ),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Project commitment stories onto recursive words.")
    parser.add_argument(
        "--story-rows",
        type=Path,
        default=THIS_DIR / "output" / "certificate_commitment_story" / "story_rows.jsonl",
        help="Optional Experiment 1 certificate commitment story rows.",
    )
    parser.add_argument(
        "--solved-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_solved_surface" / "recursive_target_rows.jsonl",
        help="Existing solved recursive target rows.",
    )
    parser.add_argument(
        "--fresh-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "fresh_rsa_challenge_recursive_surface" / "recursive_target_rows.jsonl",
        help="Fresh RSA challenge recursive target rows.",
    )
    parser.add_argument(
        "--expanded-recursive-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_recursive_target_catalog" / "recursive_target_rows.jsonl",
        help="Expanded recursive target catalog rows.",
    )
    parser.add_argument(
        "--solved-inverse-rows",
        type=Path,
        default=THIS_DIR / "output" / "grammar_inverse_word_exclusion" / "inverse_word_rows.jsonl",
        help="Existing solved inverse word rows.",
    )
    parser.add_argument(
        "--fresh-inverse-rows",
        type=Path,
        default=THIS_DIR / "output" / "fresh_rsa_challenge_inverse_word_exclusion" / "inverse_word_rows.jsonl",
        help="Fresh RSA challenge inverse word rows.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=THIS_DIR / "output" / "commitment_story_word_projection",
        help="Output directory.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the commitment-story word projection probe."""
    args = parse_args(argv)
    story_rows = read_optional_jsonl(args.story_rows)
    projection_source = (
        "certificate_commitment_story_rows"
        if args.story_rows.exists()
        else "local_minimum_story_derivation"
    )
    stories = story_index(story_rows)
    expanded_sets = expanded_signature_sets(read_jsonl(args.expanded_recursive_rows))
    rows = []
    rows.extend(
        projection_rows(
            "solved",
            read_jsonl(args.solved_recursive_rows),
            inverse_global_index(read_jsonl(args.solved_inverse_rows)),
            expanded_sets,
            stories,
            projection_source,
        )
    )
    rows.extend(
        projection_rows(
            "fresh_rsa_100",
            read_jsonl(args.fresh_recursive_rows),
            inverse_global_index(read_jsonl(args.fresh_inverse_rows)),
            expanded_sets,
            stories,
            projection_source,
        )
    )
    payload = summary(rows, len(story_rows), projection_source)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "projection_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
