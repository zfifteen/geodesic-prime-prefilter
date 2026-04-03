"""Tests for the GWR proof-pursuit finite-remainder attempt script."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "finite_remainder_attempt.py"


def load_module():
    """Load the proof-pursuit script directly from its file path."""
    spec = importlib.util.spec_from_file_location("finite_remainder_attempt", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load finite_remainder_attempt")
    module = importlib.util.module_from_spec(spec)
    sys.modules["finite_remainder_attempt"] = module
    spec.loader.exec_module(module)
    return module


def test_witness_family_is_unresolved_and_has_exact_divisor_identity():
    """The obstruction family should remain unresolved for the current reduction."""
    module = load_module()
    witness = module.witness_row(7)

    assert witness.winner_divisor_count == 13
    assert witness.earlier_divisor_count == 14
    assert witness.earlier_value == 192
    assert witness.earlier_value_divisor_count == 14
    assert witness.theorem_threshold == 2048
    assert not witness.theorem_eliminates_candidate


def test_finite_remainder_attempt_emits_json_and_reports_class_only_limit(tmp_path, capsys):
    """The finite-remainder attempt should report only the class-only obstruction."""
    module = load_module()
    output_path = tmp_path / "proof" / "finite_remainder_attempt.json"

    assert module.main(["--max-m", "10", "--output", str(output_path)]) == 0

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["route_b3_closed"] is None
    assert "leaves an infinite unresolved divisor-class family" in payload["result"]
    assert "does not construct an actual prime gap" in payload["scope_limit"]
    assert len(payload["witness_rows"]) == 7

    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload["proof_note_target"] == "class-only earlier-spoiler inequality test"
