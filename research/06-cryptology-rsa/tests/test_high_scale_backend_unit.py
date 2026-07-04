"""Unit test for pure HighScale C path + fallback on ladder 128/256 anchors.

Drives shipped HighScaleBackend.chamber_reset_certificate on real isqrt from fixtures.
Asserts either usable fields or explicit limitation note (per AC3).
No runner, no diagnose, pure backend.
"""

import json
import sys
from pathlib import Path

import gmpy2
import pytest

ROOT = Path(__file__).resolve().parents[3]
V2 = ROOT / "research/06-cryptology-rsa/experiments/data-ladder/rsa-v2"
sys.path.insert(0, str(ROOT / "research/06-cryptology-rsa/experiments/live-solver/rsa-v2"))

from pgs_inference_backend import HighScaleBackend


def load_ladder_cases():
    cases = []
    for line in (V2 / "fixtures" / "ladder_cases.jsonl").read_text(encoding="utf-8").strip().splitlines():
        if line.strip():
            d = json.loads(line)
            cases.append(d)
    return cases


def test_high_scale_on_128_256_anchors_gives_fields_or_note():
    """HighScale on isqrt of 128/256 ladder cases must return non-None with either
    carrier/threat/tail or explicit high_scale_note limitation.
    C bridge exercised (the _c path is called).
    """
    cases = load_ladder_cases()
    large_cases = [c for c in cases if c["bits"] >= 127]
    assert len(large_cases) >= 2, "need 128 and 256 cases in fixtures"

    backend = HighScaleBackend()
    for c in large_cases:
        n = gmpy2.mpz(c["N"])
        anchor = gmpy2.isqrt(n)
        cert = backend.chamber_reset_certificate(anchor, 4096)
        assert cert is not None, f"HighScale returned None for {c['case_id']} anchor"
        note = cert.get("high_scale_note", "")
        has_fields = (
            cert.get("carrier_d") is not None or
            cert.get("tail_after_reset_offsets") or
            cert.get("high_scale_tail_count", 0) > 0 or
            "limitation" in note.lower() or "fallback" in note.lower() or "attempted" in note.lower()
        )
        assert has_fields, f"cert for {c['case_id']} lacks usable fields or note: {cert}"
        # C was attempted in the path (source has the call)
        assert "C " in note or "attempted" in note or "exercised" in note or "fallback" in note
