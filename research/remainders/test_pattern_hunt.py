from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

from pattern_hunt_core import (  # noqa: E402
    aggregate_cells,
    k_offset_bin,
    mod210_class,
    primorial_level,
    record_features,
    run_extended_analysis,
    structural_laws,
)
from pattern_hunt import run_probe  # noqa: E402


def _feat(**kwargs):
    base = {
        "p_mod_30": 1,
        "position_bin": 0,
        "gap_regime": "small_g3_6",
        "zero_pattern_code": 0,
        "primorial_level": 0,
        "mod210_class": 0,
        "k_offset_bin": "k_1_3",
        "is_gwr": False,
        "dist_eq_1": False,
        "g": 4,
        "k": 1,
        "p": 31,
    }
    base.update(kwargs)
    return base


def test_core_record_features():
    rec = {
        "p": 29,
        "g": 2,
        "k": 1,
        "n": 30,
        "remainder_vector": [0, 0, 0, 2, 0, 30, 30],
        "is_current_min_d": True,
        "distance_to_next_prime": 1,
    }
    feat = record_features(rec)
    assert feat["p_mod_30"] == 29
    assert feat["mod210_class"] == mod210_class(rec["remainder_vector"])
    assert primorial_level(30) == 30


def test_mod210_and_koffset_helpers():
    assert mod210_class([0, 0, 0, 1, 5, 10, 20]) == 0b0111
    assert k_offset_bin(8) == "k_7_10"


def test_aggregate_cells_counts_and_rates():
    feats = [
        _feat(p_mod_30=29, gap_regime="medium_g7_20", is_gwr=True, dist_eq_1=False),
        _feat(p_mod_30=29, gap_regime="medium_g7_20", is_gwr=False, dist_eq_1=True),
        _feat(p_mod_30=1, position_bin=5, is_gwr=True, dist_eq_1=True),
    ]
    agg = aggregate_cells(feats)
    assert agg["record_count"] == 3
    assert agg["cell_count"] == 2


def test_structural_laws_detects_tautology_and_p29():
    summary = {
        "global_dist_eq_1_rate": 0.1,
        "cells": [
            {"p_mod_30": 29, "position_bin": 0, "gap_regime": "medium_g7_20", "count": 500, "dist_eq_1_rate": 0.0, "gwr_rate": 0.1},
            {"p_mod_30": 7, "position_bin": 9, "gap_regime": "small_g3_6", "count": 300, "dist_eq_1_rate": 1.0, "gwr_rate": 0.05},
        ],
    }
    ids = {law["id"] for law in structural_laws(summary)}
    assert "p29_doorstep_decoy" in ids
    assert "position_bin_9_tautology" in ids


def test_run_extended_analysis_mod210_and_p29():
    feats = [
        _feat(is_gwr=True, mod210_class=0, dist_eq_1=False),
        _feat(is_gwr=True, mod210_class=7, dist_eq_1=True),
        _feat(p_mod_30=29, g=10, k=1, is_gwr=False, zero_pattern_code=0b10111, primorial_level=30),
    ]
    ext = run_extended_analysis(feats)
    assert ext["gwr_mod210_classes"]["0"]["rate"] == 0.0
    assert ext["gwr_mod210_classes"]["7"]["rate"] == 1.0
    assert ext["p29_wide_k1_doorstep"]["total"] == 1


def test_runner_tiny_jsonl():
    j = HERE / "correlations/enriched/tiny_enriched.jsonl"
    if not j.is_file():
        pytest.skip("no tiny enriched jsonl")
    o = HERE / "correlations/investigation/pattern_partition_tiny_test.json"
    e = HERE / "correlations/investigation/pattern_extended_tiny_test.json"
    p = subprocess.run(
        [sys.executable, str(HERE / "pattern_hunt.py"), "--jsonl", str(j), "--output", str(o), "--extended-output", str(e)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, p.stderr
    assert "mod210_class" in json.loads(o.read_text())["joint_features"]
    assert "analysis" in json.loads(e.read_text())


def test_real_surface_smoke():
    j = HERE / "output/pattern_hunt_surface/raw_records.jsonl"
    if not j.is_file():
        pytest.skip("surface not collected")
    out = HERE / "correlations/investigation/pattern_partition_smoke_test.json"
    ext = HERE / "correlations/investigation/pattern_extended_smoke_test.json"
    run_probe(j, out, ext, max_records=5000)
    assert json.loads(out.read_text())["summary"]["record_count"] == 5000
    out.unlink(missing_ok=True)
    ext.unlink(missing_ok=True)


def test_build_report_generates_rich_html():
    build = HERE / "pattern_hunt_build_report.py"
    part = HERE / "correlations/investigation/pattern_partition_summary.json"
    ext = HERE / "correlations/investigation/pattern_extended_analysis.json"
    agy = HERE / "collaboration/agy_round_excerpts.json"
    if not all(p.is_file() for p in (build, part, ext, agy)):
        pytest.skip("report inputs missing")
    out = HERE / "correlations/investigation/pattern_report_test.html"
    p = subprocess.run([sys.executable, str(build), "--output", str(out)], cwd=str(ROOT), capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    html = out.read_text()
    assert len(html) > 8000
    assert "round-card" in html
    out.unlink(missing_ok=True)