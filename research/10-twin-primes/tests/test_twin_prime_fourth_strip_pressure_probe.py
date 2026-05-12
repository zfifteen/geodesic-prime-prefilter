"""Tests for the focused fourth-strip pressure probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "scripts"
    / "twin_prime_fourth_strip_pressure_probe.py"
)


def load_module():
    """Load the fourth-strip pressure probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_fourth_strip_pressure_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load fourth-strip pressure probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_input(path: Path) -> None:
    """Write a small LF-terminated next-layer input surface."""
    rows = [
        {
            "scale": 100,
            "q": 1,
            "candidate": 2,
            "factor_signature": "7*11",
            "third_factor": 7,
            "third_remainder": 77,
            "terminal_family": "multi_prime_family",
            "grammar_accounted": "False",
        },
        {
            "scale": 100,
            "q": 3,
            "candidate": 4,
            "factor_signature": "7*11*13",
            "third_factor": 7,
            "third_remainder": 1001,
            "terminal_family": "multi_prime_family",
            "grammar_accounted": "False",
        },
        {
            "scale": 100,
            "q": 5,
            "candidate": 6,
            "factor_signature": "7*11^2",
            "third_factor": 7,
            "third_remainder": 847,
            "terminal_family": "multi_prime_family",
            "grammar_accounted": "False",
        },
        {
            "scale": 100,
            "q": 7,
            "candidate": 8,
            "factor_signature": "7*11*13*17",
            "third_factor": 7,
            "third_remainder": 17017,
            "terminal_family": "multi_prime_family",
            "grammar_accounted": "False",
        },
    ]
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "third_factor",
        "third_remainder",
        "terminal_family",
        "grammar_accounted",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_fourth_strip_terminal_classes_are_exact():
    """Fourth-strip terminal classes should match remainder family."""
    module = load_module()

    assert module.fourth_strip_terminal("fixed_point") == "fourth_strip_fixed_point"
    assert module.fourth_strip_terminal("semiprime_distinct") == "fourth_strip_semiprime_distinct"
    assert (
        module.fourth_strip_terminal("prime_square")
        == "fourth_strip_prime_power_tail_prime_square"
    )
    assert module.fourth_strip_terminal("multi_prime_family") == "fifth_layer_multi_prime"
    assert module.is_fourth_strip_accounted("fixed_point") is True
    assert module.is_fourth_strip_accounted("semiprime_distinct") is True
    assert module.is_fourth_strip_accounted("prime_square") is True
    assert module.is_fourth_strip_accounted("multi_prime_family") is False


def test_fourth_strip_row_classifies_constructed_rows():
    """Rows should compress into low complexity, tail, or fifth layer."""
    module = load_module()
    fixed = module.fourth_strip_row(
        {
            "scale": "100",
            "q": "1",
            "candidate": "2",
            "factor_signature": "7*11",
            "third_factor": "7",
            "third_remainder": "77",
        }
    )
    semiprime = module.fourth_strip_row(
        {
            "scale": "100",
            "q": "3",
            "candidate": "4",
            "factor_signature": "7*11*13",
            "third_factor": "7",
            "third_remainder": "1001",
        }
    )
    tail = module.fourth_strip_row(
        {
            "scale": "100",
            "q": "5",
            "candidate": "6",
            "factor_signature": "7*11^2",
            "third_factor": "7",
            "third_remainder": "847",
        }
    )
    fifth = module.fourth_strip_row(
        {
            "scale": "100",
            "q": "7",
            "candidate": "8",
            "factor_signature": "7*11*13*17",
            "third_factor": "7",
            "third_remainder": "17017",
        }
    )

    assert fixed["fourth_remainder_family"] == "fixed_point"
    assert semiprime["fourth_remainder_family"] == "semiprime_distinct"
    assert tail["fourth_remainder_family"] == "prime_square"
    assert fifth["fourth_remainder_family"] == "multi_prime_family"
    assert fixed["fourth_strip_accounted"] is True
    assert tail["fourth_strip_accounted"] is True
    assert fifth["fourth_strip_accounted"] is False


def test_summary_counts_accounted_and_fifth_layer():
    """Summary should reconcile accounted and fifth-layer rows."""
    module = load_module()
    rows = [
        module.fourth_strip_row(
            {
                "scale": "100",
                "q": str(index),
                "candidate": str(index + 1),
                "factor_signature": "x",
                "third_factor": "7",
                "third_remainder": value,
            }
        )
        for index, value in enumerate(["77", "1001", "847", "17017"], start=1)
    ]
    summary = module.summarize(rows)

    assert summary["input_next_layer_count"] == 4
    assert summary["fourth_strip_low_complexity_count"] == 2
    assert summary["fourth_strip_prime_power_tail_count"] == 1
    assert summary["fourth_strip_accounted_count"] == 3
    assert summary["fifth_layer_count"] == 1
    assert summary["grammar_disposition"] == "FIFTH_LAYER_FOUND"


def test_entry_point_writes_lf_artifacts(tmp_path):
    """The CLI should emit LF-terminated fourth-strip artifacts."""
    module = load_module()
    input_path = tmp_path / "next_layer_rows.csv"
    write_input(input_path)

    assert module.main(["--input", str(input_path), "--scale", "100", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "fourth_strip_rows.csv"
    fifth_path = tmp_path / "fifth_layer_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert fifth_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()
    assert b"\r\n" not in fifth_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    fifth_rows = list(csv.DictReader(fifth_path.open(encoding="utf-8", newline="")))
    assert summary["input_next_layer_count"] == len(rows)
    assert summary["fifth_layer_count"] == len(fifth_rows)
