#!/usr/bin/env python3
"""Measure one-cell chamber closure and obstruction geometry for twin candidates."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment

DEFAULT_OUTPUT_DIR = ROOT / "research" / "10-twin-primes" / "output" / "twin_prime_one_cell_closure_probe"
DEFAULT_MAX_RIGHT_PRIME = 1_000_000
ELIGIBLE_RESIDUES = (11, 17, 29)
GAP_TYPE_PROBE_PATH = Path(__file__).with_name("gwr_dni_gap_type_probe.py")


def load_gap_type_probe():
    """Load the experiment-local gap-type probe."""
    spec = importlib.util.spec_from_file_location("gwr_dni_gap_type_probe", GAP_TYPE_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load gwr_dni_gap_type_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GAP_TYPE_PROBE = load_gap_type_probe()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Measure PGS one-cell closure for twin-prime candidates.",
    )
    parser.add_argument(
        "--max-right-prime",
        type=int,
        default=DEFAULT_MAX_RIGHT_PRIME,
        help="Largest eligible current prime q included in the closure surface.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for summary and CSV artifacts.",
    )
    return parser


def divisor_count_at(n: int) -> int:
    """Return the exact divisor count at one integer."""
    return int(divisor_counts_segment(n, n + 1)[0])


def score_f(n: int, tau_n: int) -> float:
    """Return the logarithmic comparison score used by the PGS proof surface."""
    return (1.0 - tau_n / 2.0) * math.log(n)


def factor_family(n: int, tau_n: int) -> str:
    """Return the factor family label for one integer."""
    if tau_n == 2:
        return "prime"
    return str(GAP_TYPE_PROBE.carrier_family(n, tau_n))


def obstruction_relation(tau_endpoint: int, tau_w: int) -> str:
    """Compare the candidate endpoint divisor count against forced interior load."""
    if tau_endpoint < tau_w:
        return "tau_endpoint_lt_tau_w"
    if tau_endpoint == tau_w:
        return "tau_endpoint_eq_tau_w"
    return "tau_endpoint_gt_tau_w"


def first_later_le_tau_w(q: int, next_prime: int, tau_w: int) -> dict[str, object]:
    """Return first post-candidate interior integer with divisor count <= tau_w."""
    start = q + 3
    if start >= next_prime:
        return {
            "first_later_le_tau_w": None,
            "first_later_le_tau_w_offset": None,
            "first_later_le_tau_w_tau": None,
            "first_later_le_tau_w_family": None,
        }

    counts = divisor_counts_segment(start, next_prime)
    for index, tau_value in enumerate(counts):
        tau_int = int(tau_value)
        if tau_int <= tau_w:
            value = start + index
            return {
                "first_later_le_tau_w": value,
                "first_later_le_tau_w_offset": value - q,
                "first_later_le_tau_w_tau": tau_int,
                "first_later_le_tau_w_family": factor_family(value, tau_int),
            }

    return {
        "first_later_le_tau_w": None,
        "first_later_le_tau_w_offset": None,
        "first_later_le_tau_w_tau": None,
        "first_later_le_tau_w_family": None,
    }


def closure_row(gap_row: dict[str, object]) -> dict[str, object]:
    """Return one one-cell closure row for one eligible prime q."""
    q = int(gap_row["current_right_prime"])
    q_mod30 = q % 30
    if q_mod30 not in ELIGIBLE_RESIDUES:
        raise ValueError(f"q={q} is not eligible for a one-cell twin candidate")

    w = q + 1
    endpoint = q + 2
    tau_w = divisor_count_at(w)
    tau_endpoint = divisor_count_at(endpoint)
    next_prime = int(gap_row["next_right_prime"])
    endpoint_class = "prime_closure" if tau_endpoint == 2 else "composite_obstruction"
    row: dict[str, object] = {
        "q": q,
        "q_mod30": q_mod30,
        "w": w,
        "forced_selected_integer": w,
        "tau_w": tau_w,
        "w_family": factor_family(w, tau_w),
        "f_w": score_f(w, tau_w),
        "candidate_endpoint": endpoint,
        "tau_endpoint": tau_endpoint,
        "endpoint_family": factor_family(endpoint, tau_endpoint),
        "endpoint_class": endpoint_class,
        "obstruction_relation": obstruction_relation(tau_endpoint, tau_w),
        "actual_next_prime": next_prime,
        "actual_gap_width": next_prime - q,
    }

    if endpoint_class == "composite_obstruction":
        row.update(first_later_le_tau_w(q, next_prime, tau_w))
    else:
        row.update(
            {
                "first_later_le_tau_w": None,
                "first_later_le_tau_w_offset": None,
                "first_later_le_tau_w_tau": None,
                "first_later_le_tau_w_family": None,
            }
        )
    return row


def closure_rows(max_right_prime: int) -> list[dict[str, object]]:
    """Return all one-cell closure rows through one current-prime cutoff."""
    rows = []
    for gap_row in GAP_TYPE_PROBE.type_rows(max_right_prime):
        q = int(gap_row["current_right_prime"])
        if q > max_right_prime:
            continue
        if q % 30 not in ELIGIBLE_RESIDUES:
            continue
        rows.append(closure_row(gap_row))
    if not rows:
        raise ValueError("no eligible one-cell chamber anchors found")
    return rows


def count_by(rows: list[dict[str, object]], *fields: str) -> list[dict[str, object]]:
    """Return sorted counts for one field tuple."""
    counter = Counter(tuple(row[field] for field in fields) for row in rows)
    output = []
    for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        payload = {field: value for field, value in zip(fields, key, strict=True)}
        payload["count"] = int(count)
        output.append(payload)
    return output


def closure_rate_by_residue(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return closure rates by q residue mod 30."""
    payload = []
    for residue in ELIGIBLE_RESIDUES:
        residue_rows = [row for row in rows if int(row["q_mod30"]) == residue]
        closures = [row for row in residue_rows if row["endpoint_class"] == "prime_closure"]
        payload.append(
            {
                "q_mod30": residue,
                "eligible_anchor_count": len(residue_rows),
                "prime_closure_count": len(closures),
                "closure_rate": len(closures) / len(residue_rows) if residue_rows else 0.0,
            }
        )
    return payload


def obstruction_family_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return compact obstruction-family rows for composite endpoint candidates."""
    obstructions = [row for row in rows if row["endpoint_class"] == "composite_obstruction"]
    fields = ("q_mod30", "tau_w", "w_family", "tau_endpoint", "endpoint_family", "obstruction_relation")
    return count_by(obstructions, *fields)


def summarize(rows: list[dict[str, object]], runtime_seconds: float) -> dict[str, object]:
    """Return summary metrics for the closure surface."""
    closures = [row for row in rows if row["endpoint_class"] == "prime_closure"]
    obstructions = [row for row in rows if row["endpoint_class"] == "composite_obstruction"]
    later_hits = [row for row in obstructions if row["first_later_le_tau_w"] is not None]
    return {
        "eligible_residues": list(ELIGIBLE_RESIDUES),
        "eligible_anchor_count": len(rows),
        "prime_closure_count": len(closures),
        "composite_obstruction_count": len(obstructions),
        "closure_rate": len(closures) / len(rows),
        "closure_rate_by_q_mod30": closure_rate_by_residue(rows),
        "tau_w_distribution_for_closures": count_by(closures, "tau_w"),
        "tau_w_distribution_for_obstructions": count_by(obstructions, "tau_w"),
        "w_family_distribution": count_by(rows, "w_family"),
        "tau_endpoint_obstruction_distribution": count_by(obstructions, "tau_endpoint"),
        "tau_endpoint_relation_to_tau_w": count_by(rows, "obstruction_relation"),
        "first_later_le_tau_w_count": len(later_hits),
        "first_later_le_tau_w_rate_among_obstructions": (
            len(later_hits) / len(obstructions) if obstructions else 0.0
        ),
        "first_later_le_tau_w_offset_distribution": count_by(later_hits, "first_later_le_tau_w_offset"),
        "top_obstruction_families": obstruction_family_rows(rows)[:50],
        "runtime_seconds": runtime_seconds,
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the one-cell chamber closure probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    rows = closure_rows(args.max_right_prime)
    summary = summarize(rows, runtime_seconds=time.perf_counter() - started)

    closure_fieldnames = [
        "q",
        "q_mod30",
        "w",
        "forced_selected_integer",
        "tau_w",
        "w_family",
        "f_w",
        "candidate_endpoint",
        "tau_endpoint",
        "endpoint_family",
        "endpoint_class",
        "obstruction_relation",
        "actual_next_prime",
        "actual_gap_width",
        "first_later_le_tau_w",
        "first_later_le_tau_w_offset",
        "first_later_le_tau_w_tau",
        "first_later_le_tau_w_family",
    ]
    obstruction_fieldnames = [
        "q_mod30",
        "tau_w",
        "w_family",
        "tau_endpoint",
        "endpoint_family",
        "obstruction_relation",
        "count",
    ]
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_csv(args.output_dir / "closure_rows.csv", rows, closure_fieldnames)
    write_csv(args.output_dir / "obstruction_family_rows.csv", obstruction_family_rows(rows), obstruction_fieldnames)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
