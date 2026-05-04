"""Tests for the high-scale twin-prime decade ladder probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "twin-primes" / "scripts" / "twin_prime_decade_ladder_probe.py"


def load_module():
    """Load the decade ladder probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_decade_ladder_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_decade_ladder_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sampled_eligible_anchors_are_deterministic_and_eligible():
    """Scale sampling should be deterministic and residue-filtered."""
    module = load_module()
    first = module.sampled_eligible_anchors_near(10**6, 12)
    second = module.sampled_eligible_anchors_near(10**6, 12)

    assert first == second
    assert len(first) == 12
    assert all(q < 10**6 for q in first)
    assert all(q % 30 in module.WIDTH2_PROBE.ELIGIBLE_RESIDUES for q in first)


def test_generated_contract_record_precedes_decomposition_fields():
    """The PGS record should contain only generator-side fields."""
    module = load_module()
    record = module.generated_contract_record(47)

    assert record == {
        "q": 47,
        "candidate": 49,
        "status": module.WIDTH2_PROBE.STATUS_EXCLUDED,
    }
    assert "factor_signature" not in record
    assert "endpoint_class" not in record


def test_strip_row_audits_after_width2_status():
    """Audit and factor fields should be attached after status exists."""
    module = load_module()
    excluded = module.strip_row(module.generated_contract_record(47), 100)
    closure = module.strip_row(module.generated_contract_record(11), 100)

    assert excluded["status"] == module.WIDTH2_PROBE.STATUS_EXCLUDED
    assert excluded["endpoint_class"] == module.WIDTH2_PROBE.ENDPOINT_COMPOSITE_OBSTRUCTION
    assert excluded["factor_signature"] == "7^2"
    assert excluded["grammar_accounted"] is True
    assert closure["status"] == module.WIDTH2_PROBE.STATUS_UNRESOLVED
    assert closure["endpoint_class"] == module.WIDTH2_PROBE.ENDPOINT_PRIME_CLOSURE
    assert closure["grammar_terminal"] == "endpoint_fixed_point_closure"


def test_scale_and_ladder_summaries_reconcile():
    """Per-scale and pooled summaries should reconcile with rows."""
    module = load_module()
    rows = module.scale_rows(10**6, 16)
    scale_summary = module.summarize_scale(10**6, rows)
    summary, scale_summaries, next_layer_rows = module.run_ladder(6, 7, 8)

    assert scale_summary["eligible_anchor_count"] == 16
    assert scale_summary["prime_closure_count"] + scale_summary["endpoint_obstruction_count"] == 16
    assert summary["eligible_anchor_count"] == sum(row["eligible_anchor_count"] for row in scale_summaries)
    assert summary["endpoint_obstruction_count"] == sum(
        row["endpoint_obstruction_count"] for row in scale_summaries
    )
    assert summary["next_layer_count"] == len(next_layer_rows)


def test_entry_point_writes_lf_compact_artifacts(tmp_path):
    """The CLI should emit LF-terminated compact ladder artifacts."""
    module = load_module()

    assert module.main(
        [
            "--min-exponent",
            "6",
            "--max-exponent",
            "6",
            "--sample-size",
            "8",
            "--output-dir",
            str(tmp_path),
        ]
    ) == 0

    summary_path = tmp_path / "summary.json"
    scale_path = tmp_path / "scale_summary_rows.csv"
    next_layer_path = tmp_path / "next_layer_rows.csv"
    assert summary_path.exists()
    assert scale_path.exists()
    assert next_layer_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in scale_path.read_bytes()
    assert b"\r\n" not in next_layer_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    scale_rows = list(csv.DictReader(scale_path.open(encoding="utf-8", newline="")))
    next_layer_rows = list(csv.DictReader(next_layer_path.open(encoding="utf-8", newline="")))
    assert summary["scale_count"] == 1
    assert summary["eligible_anchor_count"] == 8
    assert len(scale_rows) == 1
    assert int(scale_rows[0]["eligible_anchor_count"]) == 8
    assert summary["next_layer_count"] == len(next_layer_rows)
