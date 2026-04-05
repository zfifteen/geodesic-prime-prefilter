"""Smoke tests for the SHA nonce carry-reset probe."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT / "benchmarks" / "python" / "sha_nonce" / "carry_reset_window_probe.py"
)


def load_module():
    """Load the probe module directly from its file path."""
    spec = importlib.util.spec_from_file_location(
        "carry_reset_window_probe",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load SHA nonce carry-reset probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_carry_reset_probe_emits_expected_artifacts(tmp_path):
    """The probe should emit JSON and SVG artifacts for a tiny deterministic run."""
    module = load_module()
    output_dir = tmp_path / "carry_reset_window_probe"

    assert (
        module.main(
            [
                "--output-dir",
                str(output_dir),
                "--window-sizes",
                "16",
                "32",
                "--headers",
                "1",
                "--windows-per-header",
                "8",
            ]
        )
        == 0
    )

    json_path = output_dir / "carry_reset_window_probe.json"
    svg_path = output_dir / "carry_reset_window_probe_first_eighth_share.svg"
    assert json_path.exists()
    assert svg_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["headers"] == 1
    assert payload["windows_per_header"] == 8
    assert payload["window_sizes"] == [16, 32]
    assert len(payload["rows"]) == 2
    assert payload["rows"][0]["alignments"][0]["label"] == "aligned"
    assert payload["rows"][0]["alignments"][1]["label"] == "half_shifted"
    assert payload["rows"][0]["alignments"][0]["total_windows"] == 8
    assert payload["rows"][0]["alignments"][0]["prefix_summaries"][0]["denominator"] == 2


def test_header_prefixes_are_deterministic_and_80_byte_ready():
    """Header prefix generation should be stable and leave room for a 4-byte nonce."""
    module = load_module()
    first = module.deterministic_header_prefix(0)
    second = module.deterministic_header_prefix(0)
    third = module.deterministic_header_prefix(1)

    assert first == second
    assert first != third
    assert len(first) == 76
