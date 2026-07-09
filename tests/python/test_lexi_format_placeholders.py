"""Guard missing-value placeholders in lexi_validation_runs format helpers.

Drives the shipped functions in
``research/02-gwr-dni/experiments/chatgpt/lexi_validation_runs.py`` so a
dash-remediation pass cannot silently reintroduce ``":"`` as the None marker.
"""

from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
LEXI_PATH = (
    REPO_ROOT
    / "research"
    / "02-gwr-dni"
    / "experiments"
    / "chatgpt"
    / "lexi_validation_runs.py"
)


def _load_lexi_module():
    """Load the shipped module with only its local helper dependencies mocked."""
    assert LEXI_PATH.is_file(), f"missing shipped path: {LEXI_PATH}"

    # The module imports optional experiment helpers at import time; stub them so
    # we exercise the real file without requiring the full chatgpt experiment dir
    # on sys.path for this unit check.
    stubs = {
        "runs": types.ModuleType("runs"),
        "z_band_prime_composite_field": types.ModuleType(
            "z_band_prime_composite_field"
        ),
    }
    stubs["z_band_prime_composite_field"].divisor_counts_segment = lambda *a, **k: []
    saved = {name: sys.modules.get(name) for name in stubs}
    try:
        for name, mod in stubs.items():
            sys.modules[name] = mod
        # Provide the experiment directory so relative imports behave as at runtime.
        exp_dir = str(LEXI_PATH.parent)
        if exp_dir not in sys.path:
            sys.path.insert(0, exp_dir)
        spec = importlib.util.spec_from_file_location(
            "lexi_validation_runs_under_test", LEXI_PATH
        )
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        for name, prior in saved.items():
            if prior is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = prior


@pytest.fixture(scope="module")
def lexi():
    return _load_lexi_module()


def test_format_int_none_is_not_colon(lexi):
    assert lexi.format_int(None) != ":"
    assert lexi.format_int(None) == "N/A"


def test_format_float_none_is_not_colon(lexi):
    assert lexi.format_float(None) != ":"
    assert lexi.format_float(None) == "N/A"


def test_format_helpers_render_present_values(lexi):
    assert lexi.format_int(1234) == "1,234"
    assert lexi.format_float(0.5, digits=2) == "0.50"
