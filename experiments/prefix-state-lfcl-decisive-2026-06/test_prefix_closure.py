"""Tests for prefix-state L_FCL decisive probe."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_PYTHON = ROOT / "src" / "python"
EXPERIMENT_DIR = Path(__file__).resolve().parent
if str(SRC_PYTHON) not in sys.path:
    sys.path.insert(0, str(SRC_PYTHON))
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402

from closure_laws import first_fire_for_law, scan_all_laws  # noqa: E402
from prefix_state import PrefixStateTracker, composite_witness  # noqa: E402
from prefix_state_closure_probe import build_tau_table, q_ref_from_tau  # noqa: E402
from semantic_audit import static_audit  # noqa: E402

CLOSURE_LAWS_PATH = EXPERIMENT_DIR / "closure_laws.py"
PREFIX_STATE_PATH = EXPERIMENT_DIR / "prefix_state.py"


def test_l0_gwr_offset_fails_on_p73():
    p = 73
    q = 79
    tau = build_tau_table(q + 1)
    gap = q - p
    fire = first_fire_for_law("L0", p, tau, list(range(1, gap)))
    assert fire is not None
    assert fire.r_declare != q


def test_closure_modules_have_no_forbidden_tau_selection():
    audit = static_audit([CLOSURE_LAWS_PATH, PREFIX_STATE_PATH])
    assert audit["semantic_audit_pass"] is True
    assert audit["violations"] == []


def test_laws_do_not_reference_q_ref_or_gap_identifiers():
    import ast

    tree = ast.parse(CLOSURE_LAWS_PATH.read_text(encoding="utf-8"))
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    assert "q_ref" not in names
    assert "gap" not in names


def test_prefix_tracker_admissible_uses_composite_witness_only():
    p = 11
    tau = build_tau_table(40)
    tracker = PrefixStateTracker(p, tau)
    snap = tracker.advance_to(10)
    for k in snap.admissible:
        assert composite_witness(tau[p + k])


def test_scan_all_laws_returns_all_ids():
    p = 23
    q = 29
    tau = build_tau_table(q + 1)
    fires = scan_all_laws(p, tau, list(range(1, q - p)))
    assert set(fires) == {"L0", "L1", "L2", "L3", "L4"}


def test_l2_can_mismatch_early_on_p47():
    """Known falsification shape: unique admissible composite ≠ next prime."""
    p = 47
    q = 53
    tau = build_tau_table(q + 1)
    fire = first_fire_for_law("L2", p, tau, list(range(1, q - p)))
    assert fire is not None
    assert fire.B_declare < q - p
    assert fire.r_declare != q