#!/usr/bin/env python3
"""Unit tests for hourly Rocket.Chat research-memo formatting."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_notify():
    path = Path(__file__).resolve().parents[3] / "scripts" / "pgs_hourly_rocketchat_notify.py"
    spec = importlib.util.spec_from_file_location("pgs_hourly_rocketchat_notify", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_format_message_reads_like_research_memo() -> None:
    notify = _load_notify()
    text = notify.format_message(
        {
            "activated_at": "2026-07-10T12:00:00Z",
            "job_id": "falsification-4e8-5e8",
            "job_type": "deterministic",
            "mechanism": "Square-branch dynamic-cutoff falsification sweep on prime roots 400M-500M",
            "research_status": "ADVANCE",
            "ops_status": "OK",
            "delta": "new falsification regime through max_prime=500000000",
            "key_numbers": {
                "min_prime": 400000001,
                "max_prime": 500000000,
                "tested_prime_count": 5019541,
                "first_counterexample": None,
                "max_utilization": 0.9341772151898734,
                "max_p": 424171123,
                "max_offset": 738,
            },
            "artifacts": [
                "python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py --min-prime 400000001",
                "research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_4e8_5e8/square_branch_dynamic_cutoff_search_summary.json",
            ],
            "commit": "b1aa094ca4bd8a7ee856fad9e2676df0d7371916",
            "task_branch": "codex/hourly-square-branch",
            "next_step": "Structural audit of recurring offset 540 on new extremal rows if no counterexample.",
        }
    )
    assert text.startswith("**PGS hourly research memo**")
    assert "Research moved forward this hour." in text
    assert "**What changed:**" in text
    assert "Extended the square-branch falsification surface through 500,000,000." in text
    assert "**Measured result:**" in text
    assert "5,019,541" in text
    assert "No counterexample" in text
    assert "r = 424,171,123" in text
    assert "**Research status:** ADVANCE" in text
    assert "**Ops status:** OK" in text
    assert "**Next pressure:**" in text
    assert "square_branch_dynamic_cutoff_search_summary.json" in text
    # Must not look like key=value log soup.
    assert "min_prime=" not in text
    assert "max_prime=" not in text
    assert "Key numbers:" not in text


def test_format_message_handles_blocked_ops() -> None:
    notify = _load_notify()
    text = notify.format_message(
        {
            "activated_at": "2026-07-10T13:00:00Z",
            "job_id": None,
            "research_status": "UNRESOLVED",
            "ops_status": "BLOCKED",
            "delta": "prior hourly run still active (single-flight lock)",
            "key_numbers": {},
            "artifacts": [],
            "commit": None,
            "next_step": "Inspect hourly.log.",
            "error": "prior hourly run still active (single-flight lock)",
        }
    )
    assert "could not start" in text.lower() or "BLOCKED" in text
    assert "**Error detail:**" in text


def test_message_fingerprint_is_stable() -> None:
    notify = _load_notify()
    text_a = "hello\nworld\n"
    text_b = "hello\nworld\n"
    text_c = "hello\nworlds\n"
    assert notify.message_fingerprint(text_a) == notify.message_fingerprint(text_b)
    assert notify.message_fingerprint(text_a) != notify.message_fingerprint(text_c)
