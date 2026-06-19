"""Tests for weak L_FCL sufficient-bound probe."""

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

from certificate_replay import replay_selection_at_bound  # noqa: E402
from demoted_audit import demoted_zero_excess_signature, tau_le_2_implies_tau_eq_2  # noqa: E402
from weak_lfcl_probe import build_tau_table, q_ref_from_tau  # noqa: E402


def test_tau_le_2_lemma_bridge():
    assert tau_le_2_implies_tau_eq_2(13)
    assert not tau_le_2_implies_tau_eq_2(1)


def test_replay_matches_cert_on_p73():
    p = 73
    gap = 6
    replay = replay_selection_at_bound(p, gap)
    assert replay is not None
    assert int(replay["q"]) == 79


def test_demoted_audit_on_anchor_table():
    anchors = [11, 23, 73, 89, 113, 127, 541]
    tau = build_tau_table(600)
    for p in anchors:
        # next prime after p from tau
        q_ref = None
        for n in range(p + 1, 600):
            if tau[n] == 2:
                q_ref = n
                break
        assert q_ref is not None
        gap = q_ref - p
        replay = replay_selection_at_bound(p, gap)
        assert replay is not None
        assert demoted_zero_excess_signature(replay)
        assert tau[q_ref] == 2


def test_demoted_audit_does_not_read_tau_q(monkeypatch):
    p = 47
    gap = 6
    replay = replay_selection_at_bound(p, gap)
    assert replay is not None

    def boom(_: int) -> int:
        raise AssertionError("demoted audit must not read tau[q]")

    monkeypatch.setitem(sys.modules, "tau_access_guard", None)
    assert demoted_zero_excess_signature(replay)