from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test path."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_commitment_story_word_projection_preserves_zero_ordered_collisions(tmp_path):
    """Experiment 3 preserves the inverse-word zero collision surface."""
    module = load_module(V2 / "commitment_story_word_projection_probe.py")
    output_dir = tmp_path / "projection"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "projection_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == "commitment_story_word_projection_v1"
    assert summary["projection_source"] in {
        "certificate_commitment_story_rows",
        "local_minimum_story_derivation",
    }
    assert summary["projection_row_count"] == len(rows) == 50
    assert summary["projected_lag2_hit_count"] == 32
    assert summary["projected_lag3_hit_count"] == 30
    assert summary["projected_lag23_collision_count"] == 0
    assert summary["projected_recursive_reduced_collision_count"] == 0
    assert summary["component_sharing_word_exclusion_count"] == 42
    assert summary["solved_lag23_collision_count"] == 0
    assert summary["fresh_rsa_100_lag23_collision_count"] == 0
    assert summary["inverse_global_mismatch_count"] == 0
    assert summary["status"] == "preserved_zero_ordered_lag23_collisions"
    assert {row["surface"] for row in rows} == {"solved", "fresh_rsa_100"}
    for row in rows:
        assert row["rule_id"] == "commitment_story_word_projection_v1"
        assert row["target_side_index"] in {0, 1}
        assert "target_side" not in row
        assert row["story_event_kinds"] == [
            "outward_lag3",
            "outward_lag2",
            "inward_lag2",
            "inward_lag3",
        ]
        assert row["lag23_reduced_signature"] == "|".join(row["story_event_values"])
        assert not row["projected_lag23_collision"]
        assert not row["projected_recursive_reduced_collision"]
        assert row["inverse_global_consistent"]
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)


def test_commitment_story_word_projection_writes_lf_json(tmp_path):
    """Experiment 3 sidecars are LF-terminated JSON and JSONL."""
    module = load_module(V2 / "commitment_story_word_projection_probe.py")
    output_dir = tmp_path / "projection"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    for path in (output_dir / "projection_rows.jsonl", output_dir / "summary.json"):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_commitment_story_word_projection_source_stays_sidecar_only():
    """Experiment 3 keeps forbidden solver machinery out of the sidecar."""
    source = (V2 / "commitment_story_word_projection_probe.py").read_text(encoding="utf-8")
    forbidden = (
        "sympy",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "OpenSSL",
        "subprocess",
        "direct_divisor_count",
        "prime_basis",
        "trial_division",
        "Miller",
        "sieve",
        "audit_factors",
        "audit_spec",
        "random",
        "CHAMBER_RADIUS",
    )
    for token in forbidden:
        assert token not in source
