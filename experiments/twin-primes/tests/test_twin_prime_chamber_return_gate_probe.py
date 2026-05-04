"""Tests for the twin-prime chamber return-gate probe."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "twin-primes" / "scripts" / "twin_prime_chamber_return_gate_probe.py"


def load_module():
    """Load the return-gate probe script from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_chamber_return_gate_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_chamber_return_gate_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_labeled_rows_do_not_use_future_gap_fields_in_signature():
    """The predictor signature should contain only completed chamber fields."""
    module = load_module()
    rows = module.labeled_rows(1_000, 500)

    assert rows
    first = rows[0]
    assert first["signature"]
    assert "next_gap" not in first["signature"]
    assert "next_right_prime" not in first
    assert "next_gap_width" not in first
    assert "next_gap_is_twin" in first


def test_signature_rows_reconcile_split_counts():
    """Aggregated signature support should reconcile with labeled rows."""
    module = load_module()
    rows = module.labeled_rows(1_000, 500)
    signatures = module.signature_rows(rows, tier="exact")

    assert signatures
    assert sum(int(row["train_count"]) for row in signatures) == sum(
        1 for row in rows if row["split"] == "train"
    )
    assert sum(int(row["test_count"]) for row in signatures) == sum(
        1 for row in rows if row["split"] == "test"
    )
    assert sum(int(row["train_twin_return_count"]) for row in signatures) == sum(
        int(row["next_gap_is_twin"]) for row in rows if row["split"] == "train"
    )
    assert sum(int(row["test_twin_return_count"]) for row in signatures) == sum(
        int(row["next_gap_is_twin"]) for row in rows if row["split"] == "test"
    )


def test_signature_tiers_reduce_or_preserve_signature_count():
    """Coarser tiers should not create more signatures than exact signatures."""
    module = load_module()
    rows = module.labeled_rows(1_000, 500)
    exact_count = len(module.signature_rows(rows, tier="exact"))

    assert exact_count > 0
    for tier in ("type_pair", "family_width", "current_type"):
        assert len(module.signature_rows(rows, tier=tier)) <= exact_count


def test_candidate_gate_rule_requires_out_of_sample_lift():
    """Candidate gates should satisfy train and test support plus lift thresholds."""
    module = load_module()
    rows = [
        {
            "signature": "strong",
            "train_count": 10,
            "test_count": 10,
            "train_lift": 2.0,
            "test_lift": 1.5,
        },
        {
            "signature": "train_only",
            "train_count": 10,
            "test_count": 10,
            "train_lift": 2.0,
            "test_lift": 1.0,
        },
        {
            "signature": "weak_support",
            "train_count": 1,
            "test_count": 10,
            "train_lift": 3.0,
            "test_lift": 3.0,
        },
    ]

    candidates = module.candidate_gate_rows(
        rows,
        min_train_count=5,
        min_test_count=5,
        min_train_lift=1.5,
        min_test_lift=1.25,
    )

    assert [row["signature"] for row in candidates] == ["strong"]


def test_entry_point_writes_return_gate_artifacts(tmp_path):
    """The CLI should write a compact summary and signature table."""
    module = load_module()

    assert module.main(
        [
            "--max-right-prime",
            "1000",
            "--train-max-right-prime",
            "500",
            "--output-dir",
            str(tmp_path),
            "--min-train-count",
            "1",
            "--min-test-count",
            "1",
        ]
    ) == 0

    summary_path = tmp_path / "summary.json"
    signature_path = tmp_path / "exact_signature_rows.csv"
    assert summary_path.exists()
    assert signature_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["row_count"] > 0
    assert summary["distinct_signature_count"] > 0
    assert summary["no_leakage_contract"]["label_field"] == "next_gap_is_twin"
    assert summary["signature_tiers"] == ["exact", "type_pair", "family_width", "current_type"]
    assert "tier_summaries" in summary
    assert (tmp_path / "type_pair_signature_rows.csv").exists()
    assert (tmp_path / "family_width_signature_rows.csv").exists()
    assert (tmp_path / "current_type_signature_rows.csv").exists()
