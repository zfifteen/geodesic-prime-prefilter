"""Tests for the PGS exponent-tail probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "exponents" / "scripts" / "pgs_exponent_tail_probe.py"


def load_module():
    """Load the exponent-tail probe."""
    spec = importlib.util.spec_from_file_location("pgs_exponent_tail_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load exponent-tail probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path]:
    """Write tiny input surfaces for the probe."""
    base = tmp_path / "third_strip_higher_rows.csv"
    fourth = tmp_path / "fourth_strip_rows.csv"
    fifth = tmp_path / "fifth_strip_rows.csv"
    sixth = tmp_path / "sixth_strip_rows.csv"
    write_csv(
        base,
        [
            {
                "q": 123821,
                "candidate": 123823,
                "factor_signature": "7^3*19^2",
                "third_remainder": 361,
                "third_remainder_family": "prime_square",
                "third_strip_prime_power_tail": "True",
            },
            {
                "q": 19,
                "candidate": 21,
                "factor_signature": "3*7",
                "third_remainder": "",
                "third_remainder_family": "",
                "third_strip_prime_power_tail": "False",
            },
        ],
    )
    write_csv(
        fourth,
        [
            {
                "scale": 1000,
                "q": 11,
                "candidate": 13,
                "factor_signature": "7^4*13^2",
                "fourth_remainder": 1183,
                "fourth_remainder_family": "two_prime_power_family",
                "fourth_remainder_signature": "7*13^2",
            }
        ],
    )
    write_csv(
        fifth,
        [
            {
                "scale": 1000,
                "q": 17,
                "candidate": 19,
                "factor_signature": "7^5",
                "fifth_remainder": 49,
                "fifth_remainder_family": "prime_square",
                "fifth_remainder_signature": "7^2",
            }
        ],
    )
    write_csv(
        sixth,
        [
            {
                "scale": 1000,
                "q": 29,
                "candidate": 31,
                "factor_signature": "11^6",
                "sixth_remainder": 121,
                "sixth_remainder_family": "prime_square",
                "sixth_remainder_signature": "11^2",
            }
        ],
    )
    return base, fourth, fifth, sixth


def test_factor_signature_and_exponent_helpers_are_exact():
    """Factor helpers should expose exponent patterns."""
    module = load_module()

    assert module.parse_factor_signature("7^3*19^2") == [(7, 3), (19, 2)]
    assert module.factor_signature([(19, 2), (7, 3)]) == "7^3*19^2"
    assert module.exponent_pattern([(7, 3), (19, 2)]) == "2,3"
    assert module.max_tail_exponent([(7, 3), (19, 2)]) == 3
    assert module.peeled_factor_residue_path("7^3*19^2", 3) == "7->7->7"


def test_tail_row_records_depth_residue_and_exponent_pattern():
    """One normalized tail row should carry exponent and residue state."""
    module = load_module()
    row = module.tail_row(
        source_surface="base_third_strip",
        scale=1_000_000,
        q=123821,
        candidate=123823,
        candidate_signature="7^3*19^2",
        strip_depth=3,
        tail_family="prime_square",
        tail_remainder=361,
        tail_signature="19^2",
    )

    assert row["q_mod30"] == 11
    assert row["candidate_mod30"] == 13
    assert row["tail_remainder_mod30"] == 1
    assert row["tail_exponent_pattern"] == "2"
    assert row["max_tail_exponent"] == 2
    assert row["peeled_factor_residue_path"] == "7->7->7"


def test_tail_row_rejects_non_tail_family():
    """The normalizer should fail on non-tail material."""
    module = load_module()
    with pytest.raises(ValueError, match="unexpected tail family"):
        module.tail_row(
            source_surface="bad",
            scale=1,
            q=1,
            candidate=3,
            candidate_signature="3",
            strip_depth=1,
            tail_family="semiprime_distinct",
            tail_remainder=3,
            tail_signature="3",
        )


def test_collect_tail_rows_from_all_surfaces(tmp_path):
    """The collector should read base and high-scale tail surfaces."""
    module = load_module()
    base, fourth, fifth, sixth = write_inputs(tmp_path)
    args = module.build_parser().parse_args(
        [
            "--base-input",
            str(base),
            "--fourth-input",
            str(fourth),
            "--fifth-input",
            str(fifth),
            "--sixth-input",
            str(sixth),
            "--output-dir",
            str(tmp_path / "out"),
        ]
    )
    rows = module.collect_tail_rows(args)

    assert [row["strip_depth"] for row in rows] == [3, 4, 5, 6]
    assert [row["tail_exponent_pattern"] for row in rows] == ["2", "2", "2", "2"]
    assert rows[1]["tail_signature"] == "7*13^2"


def test_summary_and_cli_outputs_reconcile_with_lf(tmp_path):
    """The CLI should emit LF-terminated rows and matching summaries."""
    module = load_module()
    base, fourth, fifth, sixth = write_inputs(tmp_path)
    out = tmp_path / "out"

    assert (
        module.main(
            [
                "--base-input",
                str(base),
                "--fourth-input",
                str(fourth),
                "--fifth-input",
                str(fifth),
                "--sixth-input",
                str(sixth),
                "--output-dir",
                str(out),
            ]
        )
        == 0
    )

    summary_path = out / "summary.json"
    tail_path = out / "exponent_tail_rows.csv"
    dominant_path = out / "dominant_residue_path_rows.csv"
    high_path = out / "high_exponent_tail_rows.csv"
    depth_path = out / "depth_exponent_rows.csv"
    residue_path = out / "residue_exponent_rows.csv"
    for path in [summary_path, tail_path, dominant_path, high_path, depth_path, residue_path]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    tails = list(csv.DictReader(tail_path.open(encoding="utf-8", newline="")))
    dominant_rows = list(csv.DictReader(dominant_path.open(encoding="utf-8", newline="")))
    high_rows = list(csv.DictReader(high_path.open(encoding="utf-8", newline="")))
    depth_rows = list(csv.DictReader(depth_path.open(encoding="utf-8", newline="")))
    residue_rows = list(csv.DictReader(residue_path.open(encoding="utf-8", newline="")))
    assert summary["total_exponent_tail_rows"] == len(tails) == 4
    assert summary["dominant_residue_path_count"] == len(dominant_rows)
    assert summary["high_exponent_tail_count"] == len(high_rows)
    assert sum(int(row["count"]) for row in depth_rows) == 4
    assert sum(int(row["count"]) for row in residue_rows) == 4
