"""A1 scale corpus well-formedness (SC). Resolution rates are measured only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from residual import TAXONOMY, is_resolved_status  # noqa: E402
from resolver import load_public_cases, resolve_case  # noqa: E402


def _assert_well_formed(result: dict) -> None:
    summary = result["summary"]
    assert "algorithm_version" in summary
    assert "git_commit" in summary
    assert "closure_status" in summary
    assert "rule_id" in summary
    status = str(summary["closure_status"])
    if is_resolved_status(status):
        assert result["structural_certificate"] is not None
        assert result["inference"]["endpoint_class"] is not None
        assert summary["residual_code"] is None
    else:
        assert summary["residual_code"] is not None
        assert summary["residual_code"] in TAXONOMY
        residual = result["residual"]
        assert residual is not None
        assert residual["residual_code"] == summary["residual_code"]
        assert residual["stage"]
        assert "lower_certificate_present" in residual
        assert "upper_certificate_present" in residual
        assert residual["diagnostics"] is not None


def _run_corpus(path: Path, *, max_steps: int, timeout_s: float, limit: int | None = None):
    cases = load_public_cases(path)
    if limit is not None:
        cases = cases[:limit]
    results = []
    for case in cases:
        results.append(
            resolve_case(
                case,
                max_steps=max_steps,
                timeout_s=timeout_s,
                commit="scale-test",
            )
        )
    return results


def test_tp_sc_128_well_formed():
    path = V3 / "corpora" / "corpus_128bit.jsonl"
    assert path.is_file()
    # Full 32-case corpus; instrumentation timeout keeps residual emit honest.
    results = _run_corpus(path, max_steps=8, timeout_s=5.0)
    assert len(results) == 32
    for result in results:
        _assert_well_formed(result)


def test_tp_sc_256_well_formed():
    path = V3 / "corpora" / "corpus_256bit.jsonl"
    assert path.is_file()
    results = _run_corpus(path, max_steps=4, timeout_s=4.0)
    assert len(results) == 16
    for result in results:
        _assert_well_formed(result)


def test_tp_sc_512_instrumentation_path():
    path = V3 / "corpora" / "corpus_512bit.jsonl"
    assert path.is_file()
    results = _run_corpus(path, max_steps=2, timeout_s=3.0)
    assert len(results) == 4
    for result in results:
        _assert_well_formed(result)


def test_tp_sc_res_residual_codes_in_taxonomy():
    path = V3 / "corpora" / "corpus_128bit.jsonl"
    results = _run_corpus(path, max_steps=4, timeout_s=4.0, limit=4)
    for result in results:
        code = result["summary"]["residual_code"]
        if code is not None:
            assert code in TAXONOMY
