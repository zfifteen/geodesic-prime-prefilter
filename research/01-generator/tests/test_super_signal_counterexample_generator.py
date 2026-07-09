"""Regression: Super-Signal CE must not break the shipped generator path.

The universal Super-Signal implication is invalidated. The generator may still
use a guarded truncation when (p+1)%30==0 and d(p+2)==2; that is an
implementation optimization, not a theorem. This test drives the real
resolve_q entry on a pinned counterexample.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_predictor.simple_pgs_generator_v2 import (  # noqa: E402
    resolve_q,
)


def test_resolve_q_on_super_signal_counterexample_17666309():
    """Pinned CE: z(GWR)>=4 but gap=8; generator must still emit correct q."""
    p = 17_666_309
    q, source, certificate = resolve_q(p)
    assert q == 17_666_317
    assert source == "PGS"
    assert int(certificate["p"]) == p
    assert int(certificate["q"]) == 17_666_317
    assert int(certificate["gap_offset"]) == 8
    assert int(certificate["carrier_w"]) == 17_666_310
    assert int(certificate["carrier_d"]) == 16


def test_resolve_q_on_second_counterexample_22284029():
    """Second independent class-A CE; same generator contract."""
    p = 22_284_029
    q, _source, certificate = resolve_q(p)
    assert q == 22_284_037
    assert int(certificate["gap_offset"]) == 8
    assert int(certificate["carrier_w"]) == 22_284_030
