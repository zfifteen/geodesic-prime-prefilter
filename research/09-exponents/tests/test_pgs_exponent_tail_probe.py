"""Tests for the PGS exponent-tail probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "09-exponents" / "scripts" / "pgs_exponent_tail_probe.py"


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


def write_inputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    """Write tiny input surfaces for the probe."""
    base = tmp_path / "third_strip_higher_rows.csv"
    base_decomposition = tmp_path / "endpoint_decomposition_rows.csv"
    decade_next_layer = tmp_path / "next_layer_rows.csv"
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
        decade_next_layer,
        [
            {
                "scale": 1_000_000,
                "q": 84719,
                "candidate": 84721,
                "factor_signature": "7^3*13*19",
                "third_remainder": 247,
                "third_remainder_family": "multi_prime_family",
            },
            {
                "scale": 10_000_000,
                "q": 9930191,
                "candidate": 9930193,
                "factor_signature": "7^3*13*17*131",
                "third_remainder": 28951,
                "third_remainder_family": "multi_prime_family",
            },
            {
                "scale": 10_000_000,
                "q": 9999719,
                "candidate": 9999721,
                "factor_signature": "11^3*7513",
                "third_remainder": 7513,
                "third_remainder_family": "fixed_point",
            },
        ],
    )
    write_csv(
        base_decomposition,
        [
            {
                "q": 123821,
                "candidate": 123823,
                "endpoint_class": "composite_obstruction",
                "factor_signature": "7^3*19^2",
                "second_strip_family": "second_factor_times_higher_remainder",
                "third_remainder": 361,
                "third_remainder_family": "prime_square",
                "third_strip_prime_power_tail": "True",
            },
            {
                "q": 84719,
                "candidate": 84721,
                "endpoint_class": "composite_obstruction",
                "factor_signature": "7^3*13*19",
                "second_strip_family": "second_factor_times_higher_remainder",
                "third_remainder": 247,
                "third_remainder_family": "semiprime_distinct",
                "third_strip_prime_power_tail": "False",
            },
            {
                "q": 31,
                "candidate": 33,
                "endpoint_class": "composite_obstruction",
                "factor_signature": "3*11",
                "second_strip_family": "not_second_stripped",
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
    return base, base_decomposition, decade_next_layer, fourth, fifth, sixth


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
    base, _base_decomposition, _decade_next_layer, fourth, fifth, sixth = write_inputs(tmp_path)
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


def test_base_path_pressure_rows_measure_denominator_surface(tmp_path):
    """The pressure surface should keep tail rows and denominator rows."""
    module = load_module()
    _base, base_decomposition, _decade_next_layer, _fourth, _fifth, _sixth = write_inputs(tmp_path)
    rows = module.base_path_pressure_rows(base_decomposition)
    summary = module.path_pressure_summary(rows)
    capacity = module.carrier_capacity_summary(rows)

    assert len(rows) == 2
    assert rows[0]["peeled_factor_residue_path"] == "7->7->7"
    assert rows[0]["residue_path_shape"] == "repeated_7"
    assert rows[0]["third_remainder_signature"] == "19^2"
    assert rows[0]["third_strip_prime_power_tail"] is True
    assert summary[0]["peeled_factor_residue_path"] == "7->7->7"
    assert summary[0]["third_higher_count"] == 2
    assert summary[0]["tail_count"] == 1
    assert summary[0]["tail_rate"] == 0.5
    assert capacity == [
        {
            "residue_path_shape": "repeated_7",
            "carrier_prime": 7,
            "third_higher_count": 2,
            "third_higher_share": 1.0,
            "post_triple_capacity": 2915,
            "integer_cube_base_count": 13,
            "integer_fourth_base_count": 6,
            "tail_count": 1,
            "tail_rate": 0.5,
            "high_exponent_tail_count": 0,
            "high_exponent_tail_rate": 0.0,
            "fixed_point_count": 0,
            "semiprime_distinct_count": 1,
            "prime_square_count": 1,
            "prime_cube_count": 0,
            "prime_power_count": 0,
            "two_prime_power_family_count": 0,
        }
    ]


def test_integer_power_base_count_is_exact():
    """Carrier-capacity power counts should use integer power thresholds."""
    module = load_module()

    assert module.integer_power_base_count(1, 3) == 0
    assert module.integer_power_base_count(8, 3) == 1
    assert module.integer_power_base_count(26, 3) == 1
    assert module.integer_power_base_count(27, 3) == 2
    assert module.integer_power_base_count(2915, 3) == 13
    assert module.integer_power_base_count(2915, 4) == 6


def test_decade_next_layer_pressure_rows_measure_scaled_carriers(tmp_path):
    """The decade next-layer surface should expose repeated carrier capacity."""
    module = load_module()
    _base, _base_decomposition, decade_next_layer, _fourth, _fifth, _sixth = write_inputs(tmp_path)
    rows = module.decade_next_layer_pressure_rows(decade_next_layer)
    capacity = module.decade_carrier_capacity_summary(rows)

    assert len(rows) == 3
    assert rows[0]["peeled_factor_residue_path"] == "7->7->7"
    assert rows[0]["residue_path_shape"] == "repeated_7"
    assert rows[2]["peeled_factor_residue_path"] == "11->11->11"
    assert capacity == [
        {
            "scale": 1_000_000,
            "residue_path_shape": "repeated_7",
            "carrier_prime": 7,
            "next_layer_count": 1,
            "scale_next_layer_count": 1,
            "scale_next_layer_share": 1.0,
            "post_triple_capacity": 2915,
            "integer_cube_base_count": 13,
            "integer_fourth_base_count": 6,
        },
        {
            "scale": 10_000_000,
            "residue_path_shape": "repeated_7",
            "carrier_prime": 7,
            "next_layer_count": 1,
            "scale_next_layer_count": 2,
            "scale_next_layer_share": 0.5,
            "post_triple_capacity": 29154,
            "integer_cube_base_count": 29,
            "integer_fourth_base_count": 12,
        },
        {
            "scale": 10_000_000,
            "residue_path_shape": "repeated_11",
            "carrier_prime": 11,
            "next_layer_count": 1,
            "scale_next_layer_count": 2,
            "scale_next_layer_share": 0.5,
            "post_triple_capacity": 7513,
            "integer_cube_base_count": 18,
            "integer_fourth_base_count": 8,
        },
    ]


def test_summary_and_cli_outputs_reconcile_with_lf(tmp_path):
    """The CLI should emit LF-terminated rows and matching summaries."""
    module = load_module()
    base, base_decomposition, decade_next_layer, fourth, fifth, sixth = write_inputs(tmp_path)
    out = tmp_path / "out"

    assert (
        module.main(
            [
                "--base-input",
                str(base),
                "--base-decomposition-input",
                str(base_decomposition),
                "--decade-next-layer-input",
                str(decade_next_layer),
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
    base_pressure_path = out / "base_path_pressure_rows.csv"
    pressure_summary_path = out / "path_pressure_rows.csv"
    shape_summary_path = out / "path_shape_pressure_rows.csv"
    carrier_capacity_path = out / "carrier_capacity_rows.csv"
    decade_pressure_path = out / "decade_next_layer_pressure_rows.csv"
    decade_capacity_path = out / "decade_carrier_capacity_rows.csv"
    depth_path = out / "depth_exponent_rows.csv"
    residue_path = out / "residue_exponent_rows.csv"
    for path in [
        summary_path,
        tail_path,
        dominant_path,
        high_path,
        base_pressure_path,
        pressure_summary_path,
        shape_summary_path,
        carrier_capacity_path,
        decade_pressure_path,
        decade_capacity_path,
        depth_path,
        residue_path,
    ]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    tails = list(csv.DictReader(tail_path.open(encoding="utf-8", newline="")))
    dominant_rows = list(csv.DictReader(dominant_path.open(encoding="utf-8", newline="")))
    high_rows = list(csv.DictReader(high_path.open(encoding="utf-8", newline="")))
    base_pressure_rows = list(csv.DictReader(base_pressure_path.open(encoding="utf-8", newline="")))
    pressure_summary_rows = list(csv.DictReader(pressure_summary_path.open(encoding="utf-8", newline="")))
    shape_summary_rows = list(csv.DictReader(shape_summary_path.open(encoding="utf-8", newline="")))
    carrier_capacity_rows = list(csv.DictReader(carrier_capacity_path.open(encoding="utf-8", newline="")))
    decade_pressure_rows = list(csv.DictReader(decade_pressure_path.open(encoding="utf-8", newline="")))
    decade_capacity_rows = list(csv.DictReader(decade_capacity_path.open(encoding="utf-8", newline="")))
    depth_rows = list(csv.DictReader(depth_path.open(encoding="utf-8", newline="")))
    residue_rows = list(csv.DictReader(residue_path.open(encoding="utf-8", newline="")))
    assert summary["total_exponent_tail_rows"] == len(tails) == 4
    assert summary["dominant_residue_path_count"] == len(dominant_rows)
    assert summary["high_exponent_tail_count"] == len(high_rows)
    assert summary["base_third_higher_count"] == len(base_pressure_rows)
    assert summary["decade_next_layer_count"] == len(decade_pressure_rows)
    assert sum(int(row["third_higher_count"]) for row in pressure_summary_rows) == len(base_pressure_rows)
    assert sum(int(row["third_higher_count"]) for row in shape_summary_rows) == len(base_pressure_rows)
    assert sum(int(row["third_higher_count"]) for row in carrier_capacity_rows) == len(base_pressure_rows)
    assert summary["carrier_capacity_distribution"][0]["post_triple_capacity"] == 2915
    assert sum(int(row["next_layer_count"]) for row in decade_capacity_rows) == len(decade_pressure_rows)
    assert summary["decade_repeated_carrier_distribution"][0]["residue_path_shape"] == "repeated_7"
    assert sum(int(row["count"]) for row in depth_rows) == 4
    assert sum(int(row["count"]) for row in residue_rows) == 4
