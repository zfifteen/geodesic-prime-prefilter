"""Tests for rough-cover CRT prime-class audits."""

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
    / "square_tail_rough_cover_prime_class_audit.py"
)


def load_module():
    """Load the prime-class audit module directly from its path."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_rough_cover_prime_class_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_rough_cover_prime_class_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_rough_cover_prime_class_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_crt_class_has_prime_selected_square_representative():
    """The local CRT class for root 509 survives prime and selected-square checks."""
    module = load_module()
    payload = module.build_prime_class_audit(509)
    row = payload["first_prime_representative"]

    assert payload["prime_representative_found"] is True
    assert payload["model_residue_coprime_to_modulus"] is True
    assert row["k"] == 4
    assert row["root"] == "89726961223544427015292389839"
    assert row["previous_root_gap"] == 112
    assert row["previous_prime_offset"] == 338
    assert row["dynamic_cutoff"] == 8889
    assert row["modeled_even_window"] == 78
    assert row["no_prime_in_modeled_window"] is True
    assert row["closed_by_cutoff"] is True
    assert row["selected_square_condition"] is True
