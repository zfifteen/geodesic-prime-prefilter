"""Tests for the cross-regime DNI exact-bundle probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "benchmarks" / "python" / "predictor" / "gwr_dni_cross_regime_bundle_probe.py"


def load_module():
    """Load the cross-regime probe script from its file path."""
    spec = importlib.util.spec_from_file_location("gwr_dni_cross_regime_bundle_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load gwr_dni_cross_regime_bundle_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_detail_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write one synthetic transition detail CSV."""
    fieldnames = [
        "next_dmin",
        "next_peak_offset",
        "residue_mod30",
        "first_open_offset",
        "current_gap_width",
        "current_dmin",
        "current_peak_offset",
    ]
    fieldnames.extend(f"prefix_d_{offset}" for offset in range(1, 13))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def synthetic_rows() -> list[dict[str, object]]:
    """Return rows whose minimal exact bundle is current_gap_width + prefix_d_1."""
    base = {
        "residue_mod30": 1,
        "first_open_offset": 2,
        "current_dmin": 4,
        "current_peak_offset": 1,
    }
    rows = [
        {
            **base,
            "current_gap_width": 2,
            "next_dmin": 4,
            "next_peak_offset": 1,
            **{f"prefix_d_{offset}": (8 if offset == 1 else 12) for offset in range(1, 13)},
        },
        {
            **base,
            "current_gap_width": 4,
            "next_dmin": 6,
            "next_peak_offset": 2,
            **{f"prefix_d_{offset}": (8 if offset == 1 else 12) for offset in range(1, 13)},
        },
        {
            **base,
            "current_gap_width": 2,
            "next_dmin": 4,
            "next_peak_offset": 1,
            **{f"prefix_d_{offset}": (8 if offset == 1 else 16) for offset in range(1, 13)},
        },
    ]
    return rows


def test_family_minima_find_smallest_exact_bundle(tmp_path):
    """The summary should report the minimal exact bundles for each configured family."""
    module = load_module()
    detail_path = tmp_path / "detail.csv"
    write_detail_csv(detail_path, synthetic_rows())

    summary = module.summarize([detail_path])

    unrestricted = summary["family_minima"]["unrestricted"]
    assert unrestricted is not None
    assert unrestricted["best_score"]["total_key_count"] == 2
    assert unrestricted["best_score"]["prefix_cutoff"] == 1

    wheel_free = summary["family_minima"]["no_residue_no_first_open"]
    assert wheel_free is not None
    assert wheel_free["best_score"]["total_key_count"] == 2
    assert wheel_free["bundles"][0]["component_keys"] == ["current_gap_width"]


def test_entry_point_writes_json_summary(tmp_path):
    """The CLI entry point should emit the cross-regime summary JSON."""
    module = load_module()
    detail_path = tmp_path / "detail.csv"
    output_path = tmp_path / "summary.json"
    write_detail_csv(detail_path, synthetic_rows())

    assert module.main(["--detail-csv", str(detail_path), "--output-json", str(output_path)]) == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["row_count"] == 3
    assert payload["family_minima"]["unrestricted"] is not None
