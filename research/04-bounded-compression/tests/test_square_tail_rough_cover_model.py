"""Tests for local CRT rough-cover models."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "scripts"
    / "square_tail_rough_cover_model.py"
)


def load_module():
    """Load the rough-cover model module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_rough_cover_model", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_rough_cover_model")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_rough_cover_model"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_has_consistent_local_complete_cover_model():
    """The rough-defect positions for root 509 admit a local CRT cover model."""
    module = load_module()
    payload = module.build_cover_model(509)

    assert payload["M"] == 39
    assert payload["small_prime_count"] == 11
    assert payload["rough_defect_count"] == 9
    assert payload["assigned_large_carrier_count"] == 9
    assert len(payload["model_residue"]) == payload["model_residue_digits"]
    assert len(payload["model_modulus"]) == payload["model_modulus_digits"]
    assert payload["model_residue_coprime_to_modulus"] is True
    assert payload["local_model_consistent"] is True
    assert payload["small_pattern_preserved"] is True
    assert payload["rough_carriers_cover_all_defects"] is True
    assert payload["small_cover_failures"] == []
    assert payload["rough_carrier_failures"] == []

    carriers = [row["carrier"] for row in payload["carrier_rows"]]
    assert len(carriers) == len(set(carriers))
    assert all(carrier > payload["M"] for carrier in carriers)
