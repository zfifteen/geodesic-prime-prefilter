from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXPERIMENTS = ROOT / "research" / "06-cryptology-rsa" / "experiments"
DATA_V2 = EXPERIMENTS / "data-ladder" / "rsa-v2"
TRANSPORTED_V2 = EXPERIMENTS / "transported-sidecars" / "rsa-v2"
SCRIPT_PATH = TRANSPORTED_V2 / "transported_threat_tail_images_probe.py"
VALID_POSITIONS = {
    "before_upper_reset",
    "inside_upper_interval",
    "after_upper_deadline",
    "missing",
}


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test fixture path."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def build_fixtures(tmp_path: Path) -> None:
    """Write public fixture rows into one temporary directory."""
    module = load_module(DATA_V2 / "build_ladder_fixtures.py")
    assert module.main(["--output-dir", str(tmp_path)]) == 0


def expected_position(value: object, reset: object, deadline: object) -> str:
    """Return the expected interval-position label for one row value."""
    if value is None or reset is None or deadline is None:
        return "missing"
    value_int = int(str(value))
    reset_int = int(str(reset))
    deadline_int = int(str(deadline))
    if value_int < reset_int:
        return "before_upper_reset"
    if value_int <= deadline_int:
        return "inside_upper_interval"
    return "after_upper_deadline"


def test_probe_emits_public_threat_tail_interval_positions(tmp_path):
    """The threat/tail image probe should emit public interval diagnostics only."""
    build_fixtures(tmp_path)
    module = load_module(SCRIPT_PATH)
    output_dir = tmp_path / "threat_tail"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--measured-rows",
            "4",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["rule_id"] == "transported_threat_tail_images_v1"
    assert summary["row_count"] == 8
    assert summary["measured_rows_per_case"] == 4
    assert summary["position_fields"] == [
        "threat_image_position",
        "tail_image_position",
        "induced_threat_position",
        "induced_tail_position",
    ]
    assert summary["broad_regime_threshold"] == {"numerator": 9, "denominator": 10}
    assert summary["diagnostic_status"] in {
        "positions_constant_or_broad_regime_only",
        "positions_have_multiple_regimes",
    }
    assert sum(summary["position_signature_counts"].values()) == len(rows)
    for field_summary in summary["position_field_summaries"]:
        assert sum(field_summary["counts"].values()) == len(rows)
        assert field_summary["dominant_count"] <= len(rows)

    for row in rows:
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)
        assert row["rule_id"] == "transported_threat_tail_images_v1"
        assert row["threat_image_position"] in VALID_POSITIONS
        assert row["tail_image_position"] in VALID_POSITIONS
        assert row["induced_threat_position"] in VALID_POSITIONS
        assert row["induced_tail_position"] in VALID_POSITIONS
        assert row["position_signature"] == "|".join(
            [
                row["threat_image_position"],
                row["tail_image_position"],
                row["induced_threat_position"],
                row["induced_tail_position"],
            ]
        )
        if row["source_threat_value"] is None:
            assert row["transported_threat_image"] is None
        else:
            assert int(row["transported_threat_image"]) == (
                int(row["N"]) // int(row["source_threat_value"])
            )
        if row["source_tail_value"] is None:
            assert row["transported_tail_image"] is None
        else:
            assert int(row["transported_tail_image"]) == (
                int(row["N"]) // int(row["source_tail_value"])
            )

        assert row["threat_image_position"] == expected_position(
            row["transported_threat_image"],
            row["induced_reset_endpoint"],
            row["induced_reset_deadline_value"],
        )
        assert row["tail_image_position"] == expected_position(
            row["transported_tail_image"],
            row["induced_reset_endpoint"],
            row["induced_reset_deadline_value"],
        )
        assert row["induced_threat_position"] == expected_position(
            row["induced_threat_value"],
            row["induced_reset_endpoint"],
            row["induced_reset_deadline_value"],
        )
        assert row["induced_tail_position"] == expected_position(
            row["induced_tail_value"],
            row["induced_reset_endpoint"],
            row["induced_reset_deadline_value"],
        )


def test_probe_writes_lf_json_sidecars(tmp_path):
    """The threat/tail probe should write LF-only JSON artifacts."""
    build_fixtures(tmp_path)
    module = load_module(SCRIPT_PATH)
    output_dir = tmp_path / "threat_tail"

    assert module.main(
        [
            "--cases",
            str(tmp_path / "ladder_cases.jsonl"),
            "--measured-rows",
            "2",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (output_dir / "rows.jsonl", output_dir / "summary.json"):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_probe_source_has_no_forbidden_inference_constructs():
    """The threat/tail probe should stay out of forbidden inference machinery."""
    source = SCRIPT_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_tokens = (
        "sympy",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "direct_divisor_count",
        "prime_basis",
        "trial_division",
        "Miller",
        "audit_factors",
        "audit_spec",
        "random",
    )
    for token in forbidden_tokens:
        assert token not in source
    for node in ast.walk(tree):
        assert not isinstance(node, ast.Mod)
