from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"
CASE_40_ID = "rsa_v2_40bit_static_001"
CASE_50_ID = "rsa_v2_50bit_static_001"
P_VALUE = "1048559"
Q_VALUE = "1048589"
GENERATED_50_P = "30729371"
GENERATED_50_Q = "33434981"


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


def test_width_diagnostic_emits_public_sidecar_rows(tmp_path):
    """As a reviewer, I want width diagnostics to stay public sidecar evidence."""
    module = load_module(V2 / "transported_width_diagnostic_probe.py")
    output_dir = tmp_path / "width"

    assert module.main(
        [
            "--cases",
            str(V2 / "fixtures" / "ladder_cases.jsonl"),
            "--measured-rows",
            "8",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["rule_id"] == "transported_width_diagnostic_v1"
    assert summary["diagnostic_status"] == "diagnostic_only_no_closure_claim"
    assert summary["row_count"] == 16
    assert summary["measured_rows_per_case"] == 8
    assert {row["case_id"] for row in rows} == {CASE_40_ID, CASE_50_ID}
    assert {
        "carrier_false_positive_against_static_frontier_count",
        "carrier_false_positive_against_unresolved_count",
        "carrier_symmetric_width_match_count",
        "exact_false_positive_against_static_frontier_count",
        "exact_false_positive_against_unresolved_count",
        "exact_symmetric_width_match_count",
        "static_frontier_class_match_count",
    }.issubset(summary)

    for row in rows:
        assert row["rule_id"] == "transported_width_diagnostic_v1"
        assert {"p", "q", "audit_integrity_status", "inference_audit_status"}.isdisjoint(row)
        if row["induced_anchor"] is None:
            assert not row["exact_symmetric_width_match"]
            assert not row["carrier_symmetric_width_match"]
            continue
        source_delta = abs(int(row["source_transported_width"]) - int(row["induced_width"]))
        induced_delta = abs(int(row["induced_transported_width"]) - int(row["source_width"]))
        assert row["source_to_induced_delta_abs"] == source_delta
        assert row["induced_to_source_delta_abs"] == induced_delta
        assert row["exact_source_to_induced_width_match"] == (source_delta <= 1)
        assert row["exact_induced_to_source_width_match"] == (induced_delta <= 1)
        assert row["exact_symmetric_width_match"] == (
            source_delta <= 1 and induced_delta <= 1
        )
        tolerance = max(int(row["source_carrier_d"]), int(row["induced_carrier_d"]))
        assert row["carrier_tolerance"] == tolerance
        assert row["carrier_source_to_induced_width_match"] == (
            source_delta <= tolerance
        )
        assert row["carrier_induced_to_source_width_match"] == (
            induced_delta <= tolerance
        )
        assert row["carrier_symmetric_width_match"] == (
            source_delta <= tolerance and induced_delta <= tolerance
        )
        assert row["static_frontier_class_match"] == (
            row["source_frontier_class"] == row["induced_frontier_class"]
        )


def test_width_diagnostic_reconstructs_documented_static_frontier_surface(tmp_path):
    """As a reviewer, I want the comparator surface to match the documented count."""
    module = load_module(V2 / "transported_width_diagnostic_probe.py")
    output_dir = tmp_path / "width"

    assert module.main(
        [
            "--cases",
            str(V2 / "fixtures" / "ladder_cases.jsonl"),
            "--measured-rows",
            "256",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    case_counts = {
        row["case_id"]: row["static_frontier_class_match_count"]
        for row in summary["case_summaries"]
    }
    assert case_counts == {
        CASE_40_ID: 172,
        CASE_50_ID: 186,
    }
    assert summary["exact_false_positive_against_unresolved_count"] == (
        summary["exact_symmetric_width_match_count"]
    )
    assert summary["carrier_false_positive_against_unresolved_count"] == (
        summary["carrier_symmetric_width_match_count"]
    )


def test_width_diagnostic_writes_lf_json_sidecars(tmp_path):
    """As a reviewer, I want width diagnostic artifacts to be LF-only."""
    module = load_module(V2 / "transported_width_diagnostic_probe.py")
    output_dir = tmp_path / "width"

    assert module.main(
        [
            "--cases",
            str(V2 / "fixtures" / "ladder_cases.jsonl"),
            "--measured-rows",
            "2",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    for path in (
        output_dir / "rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_width_diagnostic_source_has_no_forbidden_inference_constructs():
    """As a reviewer, I want the width diagnostic free of forbidden machinery."""
    forbidden = (
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
        "sieve",
        "audit_factors",
        "audit_spec",
        "random",
        "CHAMBER_RADIUS",
        P_VALUE,
        Q_VALUE,
        GENERATED_50_P,
        GENERATED_50_Q,
    )
    source = (V2 / "transported_width_diagnostic_probe.py").read_text(encoding="utf-8")
    for token in forbidden:
        assert token not in source
