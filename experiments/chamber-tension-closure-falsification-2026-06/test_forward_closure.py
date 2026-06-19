"""Tests for chamber-tension-closure experiment lanes."""

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
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)

from audit_utils import (  # noqa: E402
    elimination_slice_violations,
    forbidden_tau_selection_violations,
)
from f2rx_selector import f2rx_certificate  # noqa: E402
from forward_chamber_closure_probe import gwr_offset_from_counts  # noqa: E402

PROBE_PATH = (
    ROOT
    / "research/01-generator/scripts/prime_inference_generator/composite_exclusion_boundary_probe.py"
)
F2RX_PATH = EXPERIMENT_DIR / "f2rx_selector.py"


def test_f0_gwr_offset_fails_on_p73():
    p = 73
    q = 79
    gap = q - p
    counts = [int(v) for v in divisor_counts_segment(p + 1, p + gap + 1)]
    off = gwr_offset_from_counts(counts)
    assert off is not None
    assert p + off != q


def test_f2rx_matches_production_on_anchor_table():
    anchors = [11, 23, 73, 89, 113, 127, 541, 7919]
    for p in anchors:
        cert_prod = pgs_chamber_reset_state_certificate(p, 128)
        assert cert_prod is not None
        bound = int(cert_prod["gap_offset"])
        counts = [int(v) for v in divisor_counts_segment(p + 1, p + bound + 1)]
        cert_rx = f2rx_certificate(p, counts, bound)
        assert cert_rx is not None
        assert int(cert_rx["q"]) == int(cert_prod["q"])


def test_f2rx_module_has_no_forbidden_tau_selection_compare():
    violations = forbidden_tau_selection_violations(F2RX_PATH)
    assert violations == []


def test_exclusion_elimination_slice_has_no_forbidden_dependencies():
    violations = elimination_slice_violations(PROBE_PATH)
    assert violations == []