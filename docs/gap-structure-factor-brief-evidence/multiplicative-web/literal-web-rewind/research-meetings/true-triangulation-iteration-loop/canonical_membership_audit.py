#!/usr/bin/env python3
"""Canonical membership-only recovery audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_emitted_distances(path: Path) -> set[int]:
    emitted: set[int] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            emitted.add(int(row["distance"]))
    return emitted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-output", type=Path, required=True)
    parser.add_argument("--p", type=int, required=True)
    parser.add_argument("--q", type=int, required=True)
    parser.add_argument("--status-out", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    emitted_distances = load_emitted_distances(args.public_output)
    p_value = args.p
    q_value = args.q
    p_hit = p_value in emitted_distances
    q_hit = q_value in emitted_distances
    if p_hit or q_hit:
        status = "recovered"
    else:
        status = "missed"
    result = {
        "status": status,
        "p_emitted": p_hit,
        "q_emitted": q_hit,
        "recovered_factor": "both" if p_hit and q_hit else "p" if p_hit else "q" if q_hit else None,
        "public_record_count": len(emitted_distances),
        "audit_behavior": "canonical_membership_only",
    }
    args.status_out.parent.mkdir(parents=True, exist_ok=True)
    args.status_out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
