"""Tests for the width-2 PGS chamber generator side probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "10-twin-primes" / "scripts" / "twin_prime_width2_pgs_generator_probe.py"


def load_module():
    """Load the width-2 generator probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_width2_pgs_generator_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_width2_pgs_generator_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_width2_record_has_only_generator_contract_fields():
    """The generated record should stay separate from audit fields."""
    module = load_module()

    assert module.width2_record(11) == {
        "q": 11,
        "candidate": 13,
        "status": module.STATUS_UNRESOLVED,
    }
    assert set(module.width2_record(47)) == {"q", "candidate", "status"}


def test_width2_record_excludes_composite_candidate():
    """For q=47, q+2=49 is excluded by the width-2 PGS contract."""
    module = load_module()
    record = module.width2_record(47)

    assert record == {
        "q": 47,
        "candidate": 49,
        "status": module.STATUS_EXCLUDED,
    }


def test_width2_record_rejects_ineligible_anchor():
    """Only q residues with q+2 wheel-open belong to the width-2 contract."""
    module = load_module()

    try:
        module.width2_record(13)
    except ValueError as exc:
        assert "not eligible" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_audit_is_downstream_from_generated_record():
    """Audit should identify true closure/composite status outside generation."""
    module = load_module()
    prime_row = module.audit_record(module.width2_record(11))
    composite_row = module.audit_record(module.width2_record(47))

    assert prime_row["endpoint_class"] == "prime_closure"
    assert prime_row["w"] == 12
    assert prime_row["tau_w"] > 2
    assert prime_row["tau_candidate"] == 2
    assert prime_row["forced_interior_carrier"] is True
    assert prime_row["endpoint_fixed_point"] is True
    assert prime_row["false_exclusion"] is False
    assert prime_row["unresolved_composite"] is False
    assert composite_row["endpoint_class"] == "composite_obstruction"
    assert composite_row["tau_candidate"] > 2
    assert composite_row["endpoint_fixed_point"] is False
    assert composite_row["false_exclusion"] is False
    assert composite_row["unresolved_composite"] is False


def test_decision_knobs_identify_the_exact_width2_knob():
    """Only the endpoint fixed-point knob should reproduce the full contract."""
    module = load_module()
    rows = module.audited_rows(module.generated_records(200))
    knob_rows = {row["knob"]: row for row in module.knob_rows(rows)}

    assert knob_rows["pgs_width2_full"]["audit_status"] == "PASS"
    assert knob_rows["endpoint_fixed_point"]["audit_status"] == "PASS"
    assert knob_rows["endpoint_fixed_point"]["excluded_count"] == knob_rows["pgs_width2_full"]["excluded_count"]
    assert knob_rows["endpoint_fixed_point"]["unresolved_count"] == knob_rows["pgs_width2_full"]["unresolved_count"]
    assert knob_rows["forced_interior_carrier"]["false_exclusion_count"] > 0
    assert knob_rows["forced_interior_carrier"]["exclusion_coverage_among_composites"] == 1.0
    assert knob_rows["endpoint_below_forced_load"]["unresolved_composite_count"] > 0


def test_small_surface_has_no_false_exclusions_or_unresolved_composites():
    """The specialized width-2 contract should be audit-exact on a small surface."""
    module = load_module()
    rows = module.audited_rows(module.generated_records(200))
    summary = module.summarize(rows)

    assert summary["eligible_anchor_count"] > 0
    assert summary["false_exclusion_count"] == 0
    assert summary["unresolved_composite_count"] == 0
    assert summary["audit_status"] == "PASS"


def test_entry_point_writes_lf_generator_and_audit_artifacts(tmp_path):
    """The CLI should emit LF-terminated generated rows and audit artifacts."""
    module = load_module()

    assert module.main(["--max-right-prime", "200", "--output-dir", str(tmp_path)]) == 0

    generated_path = tmp_path / "generated_records.jsonl"
    audit_path = tmp_path / "audit_rows.csv"
    knob_path = tmp_path / "decision_knob_rows.csv"
    summary_path = tmp_path / "summary.json"
    assert generated_path.exists()
    assert audit_path.exists()
    assert knob_path.exists()
    assert summary_path.exists()
    assert b"\r\n" not in generated_path.read_bytes()
    assert b"\r\n" not in audit_path.read_bytes()
    assert b"\r\n" not in knob_path.read_bytes()
    assert b"\r\n" not in summary_path.read_bytes()

    generated = [
        json.loads(line)
        for line in generated_path.read_text(encoding="utf-8").splitlines()
    ]
    audit_rows = list(csv.DictReader(audit_path.open(encoding="utf-8", newline="")))
    knob_rows = list(csv.DictReader(knob_path.open(encoding="utf-8", newline="")))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert all(set(row) == {"q", "candidate", "status"} for row in generated)
    assert len(generated) == summary["eligible_anchor_count"]
    assert len(audit_rows) == summary["eligible_anchor_count"]
    assert {row["knob"] for row in knob_rows} == set(module.KNOBS)
    assert summary["audit_status"] == "PASS"
