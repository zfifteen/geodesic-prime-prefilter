#!/usr/bin/env python3
"""Emit the transitive least-factor projection graph for a square-tail root."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_obstruction_word import build_payload  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Parent prime root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def child_roots(payload: dict[str, object]) -> list[int]:
    """Return the sorted distinct least-factor child roots for one payload."""
    return sorted(
        {int(row["least_factor"]) for row in payload["obstruction_rows"]}
    )


def node_row(root: int, payload: dict[str, object], depth: int) -> dict[str, object]:
    """Return the graph row for one square-tail root."""
    children = child_roots(payload)
    return {
        "root": root,
        "depth": depth,
        "previous_prime_offset": payload["previous_prime_offset"],
        "dynamic_cutoff": payload["dynamic_cutoff"],
        "cutoff_utilization": (
            int(payload["previous_prime_offset"]) / int(payload["dynamic_cutoff"])
        ),
        "closed_by_cutoff": payload["closed_by_cutoff"],
        "selected_square_condition": payload["selected_square_condition"],
        "obstruction_prefix_even_count": payload["obstruction_prefix_even_count"],
        "full_counterexample_even_count": payload["full_counterexample_even_count"],
        "child_count": len(children),
        "child_roots": children,
    }


def build_graph(root: int) -> dict[str, object]:
    """Return the transitive least-factor projection graph for one root."""
    queue: deque[tuple[int, int]] = deque([(root, 0)])
    rows_by_root: dict[int, dict[str, object]] = {}
    edges: set[tuple[int, int]] = set()

    while queue:
        current_root, depth = queue.popleft()
        if current_root in rows_by_root:
            continue

        payload = build_payload(current_root)
        row = node_row(current_root, payload, depth)
        rows_by_root[current_root] = row

        for child in row["child_roots"]:
            child_int = int(child)
            edges.add((current_root, child_int))
            if child_int not in rows_by_root:
                queue.append((child_int, depth + 1))

    rows = sorted(rows_by_root.values(), key=lambda row: (-int(row["depth"]), int(row["root"])))
    sinks = [row for row in rows if int(row["child_count"]) == 0]
    open_nodes = [row for row in rows if not bool(row["closed_by_cutoff"])]
    nonselected_nodes = [
        row for row in rows if not bool(row["selected_square_condition"])
    ]
    nondecreasing_edges = [
        {"parent": parent, "child": child}
        for parent, child in sorted(edges)
        if child >= parent
    ]

    return {
        "root": root,
        "node_count": len(rows),
        "edge_count": len(edges),
        "max_depth": max(int(row["depth"]) for row in rows) if rows else 0,
        "sink_count": len(sinks),
        "sink_roots": [int(row["root"]) for row in sinks],
        "all_edges_strictly_decrease": not nondecreasing_edges,
        "nondecreasing_edges": nondecreasing_edges,
        "all_nodes_closed_by_cutoff": not open_nodes,
        "open_roots": [int(row["root"]) for row in open_nodes],
        "all_nodes_selected_square_condition": not nonselected_nodes,
        "nonselected_roots": [int(row["root"]) for row in nonselected_nodes],
        "max_cutoff_utilization_row": max(
            rows,
            key=lambda row: float(row["cutoff_utilization"]),
        )
        if rows
        else None,
        "nodes": rows,
        "edges": [
            {"parent": parent, "child": child}
            for parent, child in sorted(edges)
        ],
    }


def main(argv: list[str] | None = None) -> int:
    """Run the projection graph emitter."""
    args = build_parser().parse_args(argv)
    payload = build_graph(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
