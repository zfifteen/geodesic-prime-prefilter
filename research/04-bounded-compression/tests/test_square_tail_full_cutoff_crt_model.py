"""Tests for full-cutoff CRT obstruction models."""

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
    / "square_tail_full_cutoff_crt_model.py"
)


def load_module():
    """Load the full-cutoff CRT model module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_full_cutoff_crt_model", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_full_cutoff_crt_model")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_full_cutoff_crt_model"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_representative_full_cutoff_crt_model_is_consistent():
    """The prime representative admits a full-cutoff local CRT obstruction model."""
    module = load_module()
    payload = module.build_full_cutoff_crt_model(509)

    assert payload["M"] == 4444
    assert payload["repeat_capable_prime_count"] == 602
    assert payload["repeat_capable_covered_count"] == 3875
    assert payload["rough_defect_count"] == 569
    assert payload["assigned_large_carrier_count"] == 569
    assert payload["first_assigned_carrier"] == 4451
    assert payload["last_assigned_carrier"] == 14741
    assert payload["model_residue_digits"] == 4136
    assert payload["model_modulus_digits"] == 4136
    assert payload["model_residue_coprime_to_modulus"] is True
    assert payload["local_model_consistent"] is True
    assert payload["small_pattern_preserved"] is True
    assert payload["rough_carriers_cover_all_defects"] is True
    assert payload["small_cover_failures"] == []
    assert payload["rough_carrier_failures"] == []
