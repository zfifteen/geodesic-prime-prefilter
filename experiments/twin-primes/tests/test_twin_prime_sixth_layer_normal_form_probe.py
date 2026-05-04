"""Tests for the focused sixth-layer normal-form probe."""

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
    / "twin_prime_sixth_layer_normal_form_probe.py"
)


def load_module():
    """Load the sixth-layer normal-form probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_sixth_layer_normal_form_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load sixth-layer normal-form probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_input(path: Path) -> None:
    """Write a small LF-terminated sixth-layer input surface."""
    rows = [
        {
            "scale": 100,
            "q": 1,
            "candidate": 2,
            "factor_signature": "7^2*11*13*17*19",
            "fifth_remainder": 4199,
            "fifth_remainder_tau": 8,
            "fifth_remainder_family": "multi_prime_family",
            "fifth_remainder_signature": "13*17*19",
            "fifth_strip_terminal": "sixth_layer_multi_prime",
            "fifth_strip_accounted": "False",
        },
        {
            "scale": 100,
            "q": 3,
            "candidate": 4,
            "factor_signature": "7^2*11^2*13*17*19",
            "fifth_remainder": 46189,
            "fifth_remainder_tau": 16,
            "fifth_remainder_family": "multi_prime_family",
            "fifth_remainder_signature": "11*13*17*19",
            "fifth_strip_terminal": "sixth_layer_multi_prime",
            "fifth_strip_accounted": "False",
        },
        {
            "scale": 100,
            "q": 5,
            "candidate": 6,
            "factor_signature": "7^2*11*13^2*17*19",
            "fifth_remainder": 55861,
            "fifth_remainder_tau": 24,
            "fifth_remainder_family": "multi_prime_family",
            "fifth_remainder_signature": "13^2*17*19",
            "fifth_strip_terminal": "sixth_layer_multi_prime",
            "fifth_strip_accounted": "False",
        },
    ]
    fields = [
        "scale",
        "q",
        "candidate",
        "factor_signature",
        "fifth_remainder",
        "fifth_remainder_tau",
        "fifth_remainder_family",
        "fifth_remainder_signature",
        "fifth_strip_terminal",
        "fifth_strip_accounted",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def test_factor_signature_parser_and_normal_form():
    """Factor signatures should parse into the expected normal forms."""
    module = load_module()

    assert module.parse_factor_signature("7^2*11") == [(7, 2), (11, 1)]
    assert module.expanded_factors([(7, 2), (11, 1)]) == [7, 7, 11]
    assert module.factor_signature([(13, 2), (7, 1)]) == "7*13^2"
    assert (
        module.sixth_layer_remainder_normal_form([(13, 1), (17, 1), (19, 1)])
        == "distinct_3_prime_product"
    )
    assert (
        module.sixth_layer_remainder_normal_form([(11, 1), (13, 1), (17, 1), (19, 1)])
        == "distinct_4_prime_product"
    )
    assert (
        module.sixth_layer_remainder_normal_form([(13, 2), (17, 1), (19, 1)])
        == "one_square_2_distinct_prime_product"
    )


def test_normal_form_rows_extract_strip_prefix_and_counts(tmp_path):
    """Normal-form rows should expose prefix and multiplicity counts."""
    module = load_module()
    input_path = tmp_path / "sixth_layer_rows.csv"
    write_input(input_path)
    rows = [module.normal_form_row(row) for row in module.load_sixth_layer_rows(input_path, 100)]

    assert rows[0]["endpoint_big_omega"] == 6
    assert rows[0]["endpoint_omega"] == 5
    assert rows[0]["strip_prefix_5"] == "7*7*11*13*17"
    assert rows[0]["fifth_remainder_big_omega"] == 3
    assert rows[0]["sixth_layer_normal_form"] == "distinct_3_prime_product"
    assert rows[2]["sixth_layer_normal_form"] == "one_square_2_distinct_prime_product"


def test_summary_groups_normal_form_counts(tmp_path):
    """Summary should reconcile normal-form grouped counts."""
    module = load_module()
    input_path = tmp_path / "sixth_layer_rows.csv"
    write_input(input_path)
    rows = [module.normal_form_row(row) for row in module.load_sixth_layer_rows(input_path, 100)]
    summary = module.summarize(rows)

    assert summary["sixth_layer_count"] == 3
    assert summary["normal_form_disposition"] == "TIGHT_NORMAL_FORM"
    assert summary["sixth_layer_normal_form_distribution"] == [
        {"sixth_layer_normal_form": "distinct_3_prime_product", "count": 1},
        {"sixth_layer_normal_form": "distinct_4_prime_product", "count": 1},
        {"sixth_layer_normal_form": "one_square_2_distinct_prime_product", "count": 1},
    ]


def test_entry_point_writes_lf_artifacts(tmp_path):
    """The CLI should emit LF-terminated normal-form artifacts."""
    module = load_module()
    input_path = tmp_path / "sixth_layer_rows.csv"
    write_input(input_path)

    assert module.main(["--input", str(input_path), "--scale", "100", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "sixth_layer_normal_form_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    assert summary["sixth_layer_count"] == len(rows)


def test_input_contract_rejects_non_sixth_layer_rows(tmp_path):
    """The input gate should reject rows outside the sixth-layer contract."""
    module = load_module()
    input_path = tmp_path / "bad_rows.csv"
    write_input(input_path)
    rows = list(csv.DictReader(input_path.open(encoding="utf-8", newline="")))
    rows[0]["fifth_remainder_family"] = "semiprime_distinct"
    with input_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with pytest.raises(ValueError, match="non-sixth-layer family"):
        module.load_sixth_layer_rows(input_path, 100)
