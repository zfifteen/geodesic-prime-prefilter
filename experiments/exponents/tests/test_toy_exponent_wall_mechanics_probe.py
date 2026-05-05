"""Tests for the toy exponent-wall mechanics probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "exponents" / "scripts" / "toy_exponent_wall_mechanics_probe.py"


def load_module():
    """Load the toy exponent-wall mechanics probe."""
    spec = importlib.util.spec_from_file_location("toy_exponent_wall_mechanics_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load toy exponent-wall mechanics probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_surface_is_power_of_two_walls_only():
    """The toy surface should contain only walls of the form 2^e."""
    module = load_module()
    rows = module.collect_rows(2, 6)

    assert [row["exponent"] for row in rows] == [2, 3, 4, 5, 6]
    assert all(row["wall_family"] == "power_of_2" for row in rows)
    assert all(row["wall"] == 2 ** int(row["exponent"]) for row in rows)
    assert all(row["boundary_rule_id"] == module.PGS_LEFT_BOUNDARY_RULE_ID for row in rows)


def test_left_boundary_uses_divisor_count_fixed_point():
    """Boundary recovery should stop at the nearest left tau=2 integer."""
    module = load_module()

    assert module.pgs_left_boundary(32) == 31
    assert module.pgs_left_boundary(64) == 61


def test_boundary_candidates_are_wheel_open_or_low_fixed_points():
    """The live boundary surface should use wheel-open hypotheses."""
    module = load_module()

    assert module.boundary_candidate_offsets(64, 8) == [3, 5]
    assert module.boundary_candidate_offsets(32, 4) == [1, 3]
    assert module.boundary_candidate_offsets(4, 2) == [1, 2]


def test_boundary_certificate_records_closed_candidate_offsets():
    """The certificate should record rejected candidate offsets before recovery."""
    module = load_module()
    certificate = module.pgs_left_boundary_certificate(2048)

    assert certificate["boundary_rule_id"] == module.PGS_LEFT_BOUNDARY_RULE_ID
    assert certificate["recovered_left_boundary"] == 2039
    assert certificate["boundary_distance"] == 9
    assert certificate["closed_candidate_offsets_before_boundary"] == "1;7"


def test_boundary_recovery_fails_loudly_when_bound_is_too_small():
    """A bounded PGS search should raise instead of falling back."""
    module = load_module()

    with pytest.raises(module.PGSBoundaryUnresolvedError):
        module.pgs_left_boundary(64, candidate_bound=2)


def test_boundary_distance_is_the_hit_criterion():
    """Boundary survival should be exactly boundary distance one."""
    module = load_module()
    surviving = module.wall_row(5)
    leaking = module.wall_row(6)

    assert surviving["boundary_distance"] == 1
    assert surviving["boundary_survives"] is True
    assert leaking["boundary_distance"] == 3
    assert leaking["boundary_survives"] is False


def test_factor_signature_is_post_recovery_diagnostic(monkeypatch):
    """Factor signatures should not affect the live boundary recovery helper."""
    module = load_module()

    def fail_factor_signature(_n: int) -> str:
        raise AssertionError("factor signature is diagnostic only")

    monkeypatch.setattr(module, "factor_signature", fail_factor_signature)

    assert module.pgs_left_boundary(64) == 61


def test_collect_rows_rejects_non_toy_ranges():
    """The toy probe should fail loudly on invalid exponent ranges."""
    module = load_module()

    with pytest.raises(ValueError, match="min_exponent must be at least 2"):
        module.collect_rows(1, 3)
    with pytest.raises(ValueError, match="max_exponent must be at least min_exponent"):
        module.collect_rows(5, 4)


def test_cli_outputs_lf_and_reconcile(tmp_path):
    """The CLI should emit LF-terminated CSVs and matching summary counts."""
    module = load_module()
    out = tmp_path / "out"

    assert module.main(["--min-exponent", "2", "--max-exponent", "8", "--output-dir", str(out)]) == 0

    summary_path = out / "summary.json"
    rows_path = out / "toy_wall_rows.csv"
    survival_path = out / "boundary_survival_rows.csv"
    leak_path = out / "boundary_leak_rows.csv"
    for path in [summary_path, rows_path, survival_path, leak_path]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    survivors = list(csv.DictReader(survival_path.open(encoding="utf-8", newline="")))
    leaks = list(csv.DictReader(leak_path.open(encoding="utf-8", newline="")))
    assert summary["candidate_bound"] == module.DEFAULT_CANDIDATE_BOUND
    assert summary["boundary_rule_id"] == module.PGS_LEFT_BOUNDARY_RULE_ID
    assert summary["wall_count"] == len(rows)
    assert summary["boundary_survival_count"] == len(survivors)
    assert summary["boundary_leak_count"] == len(leaks)
    assert len(rows) == len(survivors) + len(leaks)
