"""Regression: mod-30-adjacent high-tau GWR carriers must still resolve.

When p+1 is a multiple of 30 and the GWR carrier sits at p+1 with tau>2,
the gap need not be twin. The generator must emit the correct q via the
full chamber path (guarded truncation applies only when tau(p+2)==2).
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


def test_resolve_q_on_mod30_adjacent_carrier_17666309():
    """p+1 divisible by 30, gap=8; generator must still emit correct q."""
    p = 17_666_309
    q, source, certificate = resolve_q(p)
    assert q == 17_666_317
    assert source == "PGS"
    assert int(certificate["p"]) == p
    assert int(certificate["q"]) == 17_666_317
    assert int(certificate["gap_offset"]) == 8
    assert int(certificate["carrier_w"]) == 17_666_310
    assert int(certificate["carrier_d"]) == 16


def test_resolve_q_on_mod30_adjacent_carrier_22284029():
    """Second independent mod-30-adjacent non-twin gap; same generator contract."""
    p = 22_284_029
    q, _source, certificate = resolve_q(p)
    assert q == 22_284_037
    assert int(certificate["gap_offset"]) == 8
    assert int(certificate["carrier_w"]) == 22_284_030
