"""Tests for the focused fifth-strip pressure probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "twin-primes"
    / "scripts"
    / "twin_prime_fifth_strip_pressure_probe.py"
)


def load_module():
    """Load the fifth-strip pressure probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_fifth_strip_pressure_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load fifth-strip pressure probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_input(path: Path) -> None:
    """Write a small LF-terminated fifth-layer input surface."""
    rows = [
        {
            "scale": 100,
            "q": 1,
            "candidate": 2,
            "factor_signature": "7*11",
            "fourth_factor": 7,
            "fourth_remainder": 77,
            "fourth_remainder_family": "multi_prime_family",
            "fourth_strip_accounted": "False",
        },
        {
            "scale": 100,
            "q": 3,
            "candidate": 4,
            "factor_signature": "7*11*13",
            "fourth_factor": 7,
            "fourth_remainder": 1001,
            "fourth_remainder_family": "multi_prime_family",
            "fourth_strip_accounted": "False",
        },
        {
            "scale": 100,
            "q": 5,
            "candidate": 6,
            "factor_signature": "7*11^2",
            "fourth_factor": 7,
            "fourth_remainder": 847,
            "fourth_remainder_family": "multi_prime_family",
            "fourth_strip_accounted": "False",
        },
        {
            "scale": 100,
            "q": 7,
            "candidate": 8,
            "factor_signature": "7*11*13*17",
            "fourth_factor": 7,
            "fourth_remainder": 17017,
            "fourth_remainder_family": "multi_prime_family",
            "fourth_strip_accounted": "False",
        },
    ]
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "fourth_factor",
        "fourth_remainder",
        "fourth_remainder_family",
        "fourth_strip_accounted",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_fifth_strip_terminal_classes_are_exact():
    """Fifth-strip terminal classes should match remainder family."""
    module = load_module()

    assert module.fifth_strip_terminal("fixed_point") == "fifth_strip_fixed_point"
    assert module.fifth_strip_terminal("semiprime_distinct") == "fifth_strip_semiprime_distinct"
    assert (
        module.fifth_strip_terminal("prime_square")
        == "fifth_strip_prime_power_tail_prime_square"
    )
    assert module.fifth_strip_terminal("multi_prime_family") == "sixth_layer_multi_prime"
    assert module.is_fifth_strip_accounted("fixed_point") is True
    assert module.is_fifth_strip_accounted("semiprime_distinct") is True
    assert module.is_fifth_strip_accounted("prime_square") is True
    assert module.is_fifth_strip_accounted("multi_prime_family") is False


def test_fifth_strip_row_classifies_constructed_rows():
    """Rows should compress into low complexity, tail, or sixth layer."""
    module = load_module()
    fixed = module.fifth_strip_row(
        {
            "scale": "100",
            "q": "1",
            "candidate": "2",
            "factor_signature": "7*11",
            "fourth_factor": "7",
            "fourth_remainder": "77",
        }
    )
    semiprime = module.fifth_strip_row(
        {
            "scale": "100",
            "q": "3",
            "candidate": "4",
            "factor_signature": "7*11*13",
            "fourth_factor": "7",
            "fourth_remainder": "1001",
        }
    )
    tail = module.fifth_strip_row(
        {
            "scale": "100",
            "q": "5",
            "candidate": "6",
            "factor_signature": "7*11^2",
            "fourth_factor": "7",
            "fourth_remainder": "847",
        }
    )
    sixth = module.fifth_strip_row(
        {
            "scale": "100",
            "q": "7",
            "candidate": "8",
            "factor_signature": "7*11*13*17",
            "fourth_factor": "7",
            "fourth_remainder": "17017",
        }
    )

    assert fixed["fifth_remainder_family"] == "fixed_point"
    assert semiprime["fifth_remainder_family"] == "semiprime_distinct"
    assert tail["fifth_remainder_family"] == "prime_square"
    assert sixth["fifth_remainder_family"] == "multi_prime_family"
    assert fixed["fifth_strip_accounted"] is True
    assert tail["fifth_strip_accounted"] is True
    assert sixth["fifth_strip_accounted"] is False


def test_summary_counts_accounted_and_sixth_layer():
    """Summary should reconcile accounted and sixth-layer rows."""
    module = load_module()
    rows = [
        module.fifth_strip_row(
            {
                "scale": "100",
                "q": str(index),
                "candidate": str(index + 1),
                "factor_signature": "x",
                "fourth_factor": "7",
                "fourth_remainder": value,
            }
        )
        for index, value in enumerate(["77", "1001", "847", "17017"], start=1)
    ]
    summary = module.summarize(rows)

    assert summary["input_fifth_layer_count"] == 4
    assert summary["fifth_strip_low_complexity_count"] == 2
    assert summary["fifth_strip_prime_power_tail_count"] == 1
    assert summary["fifth_strip_accounted_count"] == 3
    assert summary["sixth_layer_count"] == 1
    assert summary["grammar_disposition"] == "SIXTH_LAYER_FOUND"


def test_entry_point_writes_lf_artifacts(tmp_path):
    """The CLI should emit LF-terminated fifth-strip artifacts."""
    module = load_module()
    input_path = tmp_path / "fifth_layer_rows.csv"
    write_input(input_path)

    assert module.main(["--input", str(input_path), "--scale", "100", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "fifth_strip_rows.csv"
    sixth_path = tmp_path / "sixth_layer_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert sixth_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()
    assert b"\r\n" not in sixth_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    sixth_rows = list(csv.DictReader(sixth_path.open(encoding="utf-8", newline="")))
    assert summary["input_fifth_layer_count"] == len(rows)
    assert summary["sixth_layer_count"] == len(sixth_rows)


def test_input_contract_rejects_non_fifth_layer_rows(tmp_path):
    """The input gate should reject rows outside the fifth-layer contract."""
    module = load_module()
    input_path = tmp_path / "bad_rows.csv"
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "fourth_factor",
        "fourth_remainder",
        "fourth_remainder_family",
        "fourth_strip_accounted",
    ]
    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerow(
            {
                "scale": 100,
                "q": 1,
                "candidate": 2,
                "factor_signature": "7*11",
                "fourth_factor": 7,
                "fourth_remainder": 77,
                "fourth_remainder_family": "semiprime_distinct",
                "fourth_strip_accounted": "False",
            }
        )

    with pytest.raises(ValueError, match="non-fifth-layer family"):
        module.load_fifth_layer_rows(input_path, 100)
