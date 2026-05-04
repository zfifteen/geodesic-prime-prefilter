"""Tests for the focused sixth-strip pressure probe."""

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
    / "twin_prime_sixth_strip_pressure_probe.py"
)


def load_module():
    """Load the sixth-strip pressure probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_sixth_strip_pressure_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load sixth-strip pressure probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_input(path: Path) -> None:
    """Write a small LF-terminated normal-form input surface."""
    rows = [
        {
            "scale": 100,
            "q": 1,
            "candidate": 2,
            "sixth_layer_normal_form": "distinct_3_prime_product",
            "fifth_remainder": 4199,
            "fifth_remainder_signature": "13*17*19",
        },
        {
            "scale": 100,
            "q": 3,
            "candidate": 4,
            "sixth_layer_normal_form": "distinct_4_prime_product",
            "fifth_remainder": 46189,
            "fifth_remainder_signature": "11*13*17*19",
        },
        {
            "scale": 100,
            "q": 5,
            "candidate": 6,
            "sixth_layer_normal_form": "one_square_3_distinct_prime_product",
            "fifth_remainder": 55861,
            "fifth_remainder_signature": "13^2*17*19",
        },
    ]
    fields = [
        "scale",
        "q",
        "candidate",
        "sixth_layer_normal_form",
        "fifth_remainder",
        "fifth_remainder_signature",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_factor_helpers_and_terminal_classes_are_exact():
    """Factor helpers should produce exact sixth-strip classes."""
    module = load_module()

    assert module.parse_factor_signature("13^2*17") == [(13, 2), (17, 1)]
    assert module.decrement_least_factor([(13, 2), (17, 1)]) == (13, [(13, 1), (17, 1)])
    assert module.factor_signature([(17, 1), (13, 1)]) == "13*17"
    assert module.endpoint_family([(17, 1)], 2) == "fixed_point"
    assert module.endpoint_family([(13, 1), (17, 1)], 4) == "semiprime_distinct"
    assert module.endpoint_family([(13, 1), (17, 1), (19, 1)], 8) == "multi_prime_family"
    assert module.sixth_strip_terminal("semiprime_distinct") == "sixth_strip_semiprime_distinct"
    assert module.sixth_strip_terminal("prime_square") == "sixth_strip_prime_power_tail_prime_square"
    assert module.sixth_strip_terminal("multi_prime_family") == "seventh_layer_multi_prime"


def test_sixth_strip_rows_classify_constructed_rows():
    """Rows should compress or carry into the seventh layer exactly."""
    module = load_module()
    semiprime = module.sixth_strip_row(
        {
            "scale": "100",
            "q": "1",
            "candidate": "2",
            "sixth_layer_normal_form": "distinct_3_prime_product",
            "fifth_remainder": "4199",
            "fifth_remainder_signature": "13*17*19",
        }
    )
    still_multi = module.sixth_strip_row(
        {
            "scale": "100",
            "q": "3",
            "candidate": "4",
            "sixth_layer_normal_form": "distinct_4_prime_product",
            "fifth_remainder": "46189",
            "fifth_remainder_signature": "11*13*17*19",
        }
    )
    semiprime_from_square = module.sixth_strip_row(
        {
            "scale": "100",
            "q": "5",
            "candidate": "6",
            "sixth_layer_normal_form": "one_square_3_distinct_prime_product",
            "fifth_remainder": "55861",
            "fifth_remainder_signature": "13^2*17*19",
        }
    )

    assert semiprime["sixth_remainder_signature"] == "17*19"
    assert semiprime["sixth_remainder_family"] == "semiprime_distinct"
    assert still_multi["sixth_remainder_signature"] == "13*17*19"
    assert still_multi["sixth_remainder_family"] == "multi_prime_family"
    assert semiprime_from_square["sixth_remainder_signature"] == "13*17*19"
    assert semiprime_from_square["sixth_remainder_family"] == "multi_prime_family"
    assert semiprime["sixth_strip_accounted"] is True
    assert still_multi["sixth_strip_accounted"] is False
    assert semiprime_from_square["sixth_strip_accounted"] is False


def test_summary_counts_accounted_and_seventh_layer(tmp_path):
    """Summary should reconcile accounted and seventh-layer rows."""
    module = load_module()
    input_path = tmp_path / "normal_form_rows.csv"
    write_input(input_path)
    rows = [module.sixth_strip_row(row) for row in module.load_normal_form_rows(input_path, 100)]
    summary = module.summarize(rows)

    assert summary["input_sixth_layer_count"] == 3
    assert summary["sixth_strip_low_complexity_count"] == 1
    assert summary["sixth_strip_prime_power_tail_count"] == 0
    assert summary["sixth_strip_accounted_count"] == 1
    assert summary["seventh_layer_count"] == 2
    assert summary["grammar_disposition"] == "SEVENTH_LAYER_FOUND"


def test_entry_point_writes_lf_artifacts(tmp_path):
    """The CLI should emit LF-terminated sixth-strip artifacts."""
    module = load_module()
    input_path = tmp_path / "normal_form_rows.csv"
    write_input(input_path)

    assert module.main(["--input", str(input_path), "--scale", "100", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "sixth_strip_rows.csv"
    seventh_path = tmp_path / "seventh_layer_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert seventh_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()
    assert b"\r\n" not in seventh_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    seventh_rows = list(csv.DictReader(seventh_path.open(encoding="utf-8", newline="")))
    assert summary["input_sixth_layer_count"] == len(rows)
    assert summary["seventh_layer_count"] == len(seventh_rows)


def test_input_contract_rejects_unexpected_normal_form(tmp_path):
    """The input gate should reject rows outside the sixth-layer normal form."""
    module = load_module()
    input_path = tmp_path / "bad_rows.csv"
    write_input(input_path)
    rows = list(csv.DictReader(input_path.open(encoding="utf-8", newline="")))
    rows[0]["sixth_layer_normal_form"] = "unexpected"
    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match="unexpected sixth-layer normal form"):
        module.load_normal_form_rows(input_path, 100)
