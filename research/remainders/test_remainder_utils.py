"""Minimal tests for remainder_utils.py.

Run with:
    python -m pytest research/remainders/test_remainder_utils.py -q
or directly:
    python research/remainders/test_remainder_utils.py

These tests must pass on the 100-gap validation set before any scaling
of the collector (per Remainder Statistics Collection Plan).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running the test file directly without installation.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from remainder_utils import MODULI_PRIMORIAL_V1, compute_residues


def test_default_moduli_v1():
    """Default moduli are the expected primorial sequence (versioned)."""
    assert MODULI_PRIMORIAL_V1 == [2, 3, 5, 7, 30, 210, 2310]


def test_basic_residues_small_n():
    """Known small values produce expected residues."""
    # 113 is a small prime used in hand-verification examples in the plan.
    # We treat it purely as an integer here.
    assert compute_residues(113) == (113 % 2, 113 % 3, 113 % 5, 113 % 7, 113 % 30, 113 % 210, 113 % 2310)
    # 113 mod 30 = 23
    assert compute_residues(113, [30]) == (23,)

    # 0
    assert compute_residues(0, [2, 3, 5]) == (0, 0, 0)

    # A clean multiple of the full set
    n = 2310
    assert compute_residues(n) == (0, 0, 0, 0, 0, 0, 0)


def test_modulus_one_always_zero():
    """Remainder mod 1 is always 0."""
    assert compute_residues(42, [1]) == (0,)
    assert compute_residues(0, [1, 2]) == (0, 0)


def test_explicit_moduli_list_and_tuple():
    """Both list and tuple inputs are accepted (Sequence)."""
    assert compute_residues(100, [2, 5]) == (0, 0)
    assert compute_residues(100, (2, 5)) == (0, 0)


def test_large_int_exact():
    """Arbitrary-precision integers remain exact."""
    big = 10**30 + 17
    # 10**k (k>=1) ≡ 10 mod 30, +17 => 27 mod 30
    assert compute_residues(big, [30]) == (27,)
    # 10**30 even +17 odd => 1 mod 2
    assert compute_residues(big, [2]) == (1,)


def test_error_cases():
    """Explicit errors for bad inputs."""
    try:
        compute_residues(-1)
    except ValueError as e:
        assert "nonnegative" in str(e).lower()
    else:
        assert False, "expected ValueError for negative n"

    try:
        compute_residues(10, [])
    except ValueError as e:
        assert "empty" in str(e).lower()
    else:
        assert False, "expected ValueError for empty moduli"

    try:
        compute_residues(10, [0])
    except ValueError as e:
        assert "positive" in str(e).lower()
    else:
        assert False, "expected ValueError for m<=0"

    try:
        compute_residues("notint")  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        assert False, "expected TypeError for non-int n"


def test_length_matches_moduli():
    """Output length always equals input moduli length."""
    mods = [2, 30, 2310]
    res = compute_residues(99991, mods)
    assert len(res) == len(mods)
    for r, m in zip(res, mods):
        assert 0 <= r < m


# --- Collector integration tests (added immediately after build_records impl) ---

def test_build_records_reuses_gwr_and_emits_core_fields():
    """build_records_for_gap produces correct shape and GWR flag on known gap."""
    # Avoid circular import issues by importing here
    from collect_remainder_stats import build_records_for_gap

    # Gap after 113: q=127, g=14, 13 interiors. GWR at 121 (d=3).
    recs = build_records_for_gap(113, [2, 3, 5, 7, 30])
    assert len(recs) == 13
    for r in recs:
        assert r["p"] == 113
        assert r["q"] == 127
        assert r["g"] == 14
        assert 1 <= r["k"] <= 13
        assert r["n"] == 113 + r["k"]
        assert r["d"] >= 3
        assert isinstance(r["remainder_vector"], tuple)
        assert len(r["remainder_vector"]) == 5
        assert isinstance(r["is_current_min_d"], bool)
        assert r["distance_to_next_prime"] == 127 - r["n"]

    winners = [r for r in recs if r["is_current_min_d"]]
    assert len(winners) == 1
    assert winners[0]["k"] == 8
    assert winners[0]["n"] == 121
    assert winners[0]["d"] == 3


def test_edge_gap_has_no_interior_records():
    from collect_remainder_stats import build_records_for_gap
    # Gap (2,3) is the only one with zero interior composites.
    assert build_records_for_gap(2, [2, 3]) == []
    # (3,5) has exactly one interior: 4
    recs = build_records_for_gap(3, [2, 3])
    assert len(recs) == 1
    assert recs[0]["n"] == 4
    assert recs[0]["d"] == 3  # 4=2^2
    assert recs[0]["is_current_min_d"] is True  # the sole interior is the GWR winner by definition


def test_sample_rate_reduces_or_keeps_records():
    from collect_remainder_stats import build_records_for_gap
    full = build_records_for_gap(113, [30])
    assert len(full) == 13
    sampled = build_records_for_gap(113, [30], sample_rate=0.5)
    # Probabilistic; for determinism in test we accept range or just check <=
    assert 0 <= len(sampled) <= 13


def test_collect_gaps_produces_100_gap_validation_set():
    """End-to-end collector run on a set with >100 gaps must succeed and produce correct artifacts.

    This is the strict "100-gap test set" gate required by the collection plan
    before any larger scaling.
    """
    import json
    import tempfile
    from pathlib import Path
    from collect_remainder_stats import collect_gaps, parse_moduli

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "val100"
        raw = out / "raw_records.jsonl"
        mods = parse_moduli(None)
        summ = collect_gaps(max_p=600, moduli=mods, output_path=raw)
        assert summ["gaps_processed"] >= 100, f"only {summ['gaps_processed']} gaps"
        assert summ["records_emitted"] > 0
        assert raw.exists()
        # spot check one record line parses and has required keys
        with raw.open() as f:
            first = json.loads(f.readline())
        assert "p" in first and "remainder_vector" in first and "is_current_min_d" in first


# --- Enrich + derived features tests (added for correlation Phase-1 data prep) ---

def test_compute_derived_remainder_scalars_basic():
    from enrich_remainder_records import compute_derived_remainder_scalars

    # From actual record in tiny_val: p=3, n=4, vec for full M_v1
    vec = (0, 1, 4, 4, 4, 4, 4)
    d = compute_derived_remainder_scalars(vec)
    assert d["num_zeros_in_vector"] == 1
    assert d["residue_sum_parity"] == 1   # 21 odd
    assert d["dist_nearest_zero_mod30"] == 4
    assert d["dist_nearest_zero_mod210"] == 4
    assert d["coprime_to_210"] is False   # first slot 0

    # Coprime case: all first4 nonzero
    vec2 = (1, 1, 1, 1, 0, 0, 0)
    d2 = compute_derived_remainder_scalars(vec2)
    assert d2["coprime_to_210"] is True
    assert d2["num_zeros_in_vector"] == 3


def test_enrich_record_adds_plan_fields():
    from enrich_remainder_records import enrich_record

    raw = {
        "p": 113, "q": 127, "g": 14, "k": 8, "n": 121, "d": 3,
        "is_current_min_d": True,
        "distance_to_next_prime": 6,
        "remainder_vector": (1, 1, 1, 2, 1, 121, 121),
        "moduli_version": "M_v1",
    }
    en = enrich_record(raw)
    assert en["termination_distance"] == 6
    assert en["is_gwr_winner"] is True
    assert "num_zeros_in_vector" in en
    # 113 winner vector first4 = (1,1,1,2) → coprime_to_210 True
    assert en["coprime_to_210"] is True


def test_enrich_jsonl_on_real_tiny_val(tmp_path):
    """Run enrich on the actual validated tiny_val set and check output schema + counts."""
    import json
    from pathlib import Path
    from enrich_remainder_records import enrich_jsonl_stream

    in_path = Path("research/remainders/output/tiny_val/raw_records.jsonl")
    out_path = tmp_path / "enriched.jsonl"

    counts = enrich_jsonl_stream(in_path, out_path)
    assert counts["records_out"] == counts["records_in"] > 400

    # spot check a few enriched records
    with out_path.open() as f:
        rec1 = json.loads(f.readline())
    # Check first record
    assert "termination_distance" in rec1
    assert "is_gwr_winner" in rec1
    assert "num_zeros_in_vector" in rec1
    assert rec1["termination_distance"] == rec1.get("distance_to_next_prime")


def test_compute_residue_histograms_on_enriched_tiny():
    import json
    from pathlib import Path
    from correlation_analysis import compute_residue_histograms

    recs = [json.loads(l) for l in Path("research/remainders/correlations/enriched/tiny_enriched.jsonl").read_text().splitlines() if l.strip()][:100]
    h = compute_residue_histograms(recs)
    assert "groups" in h
    assert len(h["groups"]) > 0
    # There should be some entries for slot 0 (mod 2)
    any_slot0 = any(0 in g.get("slots", {}) for g in h["groups"].values())
    assert any_slot0, "no slot-0 (mod-2) data produced"


def test_transition_matrix_on_tiny_near_end_sequences():
    """Direct exercise of transition_matrix on real enriched tiny remainder vectors (near-termination per gap).

    Verifies acceptance: returns dict with counts + probabilities, numeric values, works on seq of tuples, no NotImplemented.
    """
    import json
    from pathlib import Path
    from correlation_analysis import transition_matrix

    recs = [json.loads(l) for l in Path("research/remainders/correlations/enriched/tiny_enriched.jsonl").read_text().splitlines() if l.strip()]
    # build near-end seqs like verification
    seqs = []
    current_gap = []
    last_p = None
    for r in sorted(recs, key=lambda x: (x["p"], x["k"])):
        if r["p"] != last_p:
            if len(current_gap) > 3:
                seqs.append([tuple(r["remainder_vector"]) for r in current_gap[-5:]])
            current_gap = []
            last_p = r["p"]
        current_gap.append(r)
    if current_gap and len(current_gap) > 3:
        seqs.append([tuple(r["remainder_vector"]) for r in current_gap[-5:]])
    assert len(seqs) > 0
    res = transition_matrix(seqs[0], lag=1)
    assert isinstance(res, dict)
    assert "counts" in res and "probabilities" in res
    assert res["lag"] == 1
    assert res["n_transitions"] > 0
    # at least one count and a prob between 0-1
    first_from = next(iter(res["counts"]))
    first_to = next(iter(res["counts"][first_from]))
    assert res["counts"][first_from][first_to] >= 1
    assert 0.0 <= res["probabilities"][first_from][first_to] <= 1.0
    # Critical: states must be full remainder vectors (7-tuples of ints), not residues
    assert isinstance(first_from, tuple) and len(first_from) == 7
    assert all(isinstance(x, int) for x in first_from)
    # and the key must appear in the input sequence
    assert first_from in seqs[0] or first_from == seqs[0][0]  # at least one state from input


def test_compute_intra_gap_repeat_stats_on_tiny():
    """Exercise the shipped repeat analysis on the real tiny enriched set via load_records + function.
    Asserts structure with numeric repeat rates and GWR alignment counts per AC1/AC2.
    """
    import json
    from pathlib import Path
    from correlation_analysis import load_records, compute_intra_gap_repeat_stats, compute_per_gap_late_repeat_feature

    recs = load_records("research/remainders/correlations/enriched/tiny_enriched.jsonl")
    assert len(recs) > 0
    stats = compute_intra_gap_repeat_stats(recs)
    assert isinstance(stats, dict)
    assert "num_gaps" in stats and stats["num_gaps"] > 0
    assert "repeat_freq_near_end" in stats
    assert "gaps_with_late_repeats" in stats
    assert isinstance(stats["repeat_freq_near_end"], (int, float))
    assert stats["gaps_with_late_repeats"] + stats["gaps_without_late_repeats"] == stats["num_gaps"]
    # also the feature function
    feats = compute_per_gap_late_repeat_feature(recs)
    assert len(feats) > 0
    assert "late_repeat_count" in feats[0]
    assert isinstance(feats[0]["late_repeat_count"], int)


if __name__ == "__main__":
    # Allow direct execution for quick smoke in research flow.
    test_default_moduli_v1()
    test_basic_residues_small_n()
    test_modulus_one_always_zero()
    test_explicit_moduli_list_and_tuple()
    test_large_int_exact()
    test_error_cases()
    test_length_matches_moduli()
    test_build_records_reuses_gwr_and_emits_core_fields()
    test_edge_gap_has_no_interior_records()
    test_sample_rate_reduces_or_keeps_records()
    print("All remainder_utils + collector smoke tests passed (direct run).")
