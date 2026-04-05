"""Smoke tests for the reduced-round SHA-256 block-rank probe."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT / "benchmarks" / "python" / "sha_nonce" / "reduced_round_block_rank_probe.py"
)


def load_module():
    """Load the probe module directly from its file path."""
    spec = importlib.util.spec_from_file_location(
        "reduced_round_block_rank_probe",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load reduced-round block-rank probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reduced_round_probe_emits_expected_artifacts(tmp_path):
    """The probe should emit JSON and SVG artifacts for a small deterministic run."""
    module = load_module()
    output_dir = tmp_path / "reduced_round_block_rank_probe"

    assert (
        module.main(
            [
                "--output-dir",
                str(output_dir),
                "--rounds",
                "4",
                "8",
                "--headers",
                "1",
                "--blocks-per-header",
                "4",
                "--block-size",
                "16",
                "--keep-fraction",
                "0.5",
            ]
        )
        == 0
    )

    json_path = output_dir / "reduced_round_block_rank_probe.json"
    svg_path = output_dir / "reduced_round_block_rank_probe_retention.svg"
    assert json_path.exists()
    assert svg_path.exists()

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["headers"] == 1
    assert payload["blocks_per_header"] == 4
    assert payload["block_size"] == 16
    assert payload["rounds"] == [4, 8]
    assert len(payload["rows"]) == 2
    assert payload["rows"][0]["selected_blocks"] == 2


def test_second_block_words_only_varies_in_nonce_word():
    """The second-block constructor should keep every word but the nonce lane fixed."""
    module = load_module()
    prefix = module.deterministic_header_prefix(0)
    tail12 = prefix[64:76]
    first = module.second_block_words(tail12, 1)
    second = module.second_block_words(tail12, 2)

    assert first[:3] == second[:3]
    assert first[4:] == second[4:]
    assert first[3] != second[3]
