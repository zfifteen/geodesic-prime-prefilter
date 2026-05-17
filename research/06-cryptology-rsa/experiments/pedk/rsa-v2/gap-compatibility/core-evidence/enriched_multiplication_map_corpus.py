#!/usr/bin/env python3
"""Build an enriched PEDK multiplication-map corpus without early compression."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    corpus_row,
    phase_bucket,
    semiprime_triples,
    winner_position_mpermille,
    write_json,
    write_jsonl,
)
from gwr_relative_all_o6_boundary import gwr_side, gwr_signed_distance
from multiplication_map_law_surface import factor_word, public_word
from public_feature_all_o6_boundary import band_key, parse_bands
from public_grammar_pivot import factor_phase_multiset, factor_residue_multiset


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_7501_9000"
DEFAULT_BANDS = ((7501, 9000),)
RULE_ID = "pedk_enriched_multiplication_map_corpus_v1"


def gap_summary(gap: dict[str, object]) -> dict[str, object]:
    """Return stable public fields from one gap grammar object."""
    return {
        "reduced_state": gap["reduced_state"],
        "exact_type_key": gap["exact_type_key"],
        "gap_width": gap["gap_width"],
        "winner_offset": gap["winner_offset"],
        "winner_d": gap["winner_d"],
        "winner_offset_from_right": gap.get("winner_offset_from_right"),
        "first_open_offset": gap["first_open_offset"],
    }


def factor_side_word(side_state: dict[str, object]) -> str:
    """Return ordered left/right factor-side grammar without p/q sorting."""
    return "|".join(
        (
            f"L={side_state['left']['reduced_state']}@{side_state['left']['winner_offset']}",
            f"R={side_state['right']['reduced_state']}@{side_state['right']['winner_offset']}",
        )
    )


def factor_side_phase_word(side_state: dict[str, object]) -> str:
    """Return ordered left/right factor-side phase grammar without p/q sorting."""
    return "|".join(
        (
            f"L={side_state['left']['reduced_state']}@{phase_bucket(winner_position_mpermille(side_state['left']))}",
            f"R={side_state['right']['reduced_state']}@{phase_bucket(winner_position_mpermille(side_state['right']))}",
        )
    )


def side_features(prefix: str, side_state: dict[str, object]) -> dict[str, object]:
    """Return flat fields for one factor endpoint's two neighboring gaps."""
    left = side_state["left"]
    right = side_state["right"]
    return {
        f"{prefix}_left_reduced_state": left["reduced_state"],
        f"{prefix}_right_reduced_state": right["reduced_state"],
        f"{prefix}_left_exact_type_key": left["exact_type_key"],
        f"{prefix}_right_exact_type_key": right["exact_type_key"],
        f"{prefix}_left_gap_width": left["gap_width"],
        f"{prefix}_right_gap_width": right["gap_width"],
        f"{prefix}_left_winner_offset": left["winner_offset"],
        f"{prefix}_right_winner_offset": right["winner_offset"],
        f"{prefix}_left_winner_phase": phase_bucket(winner_position_mpermille(left)),
        f"{prefix}_right_winner_phase": phase_bucket(winner_position_mpermille(right)),
        f"{prefix}_left_winner_d": left["winner_d"],
        f"{prefix}_right_winner_d": right["winner_d"],
    }


def enriched_row(row: dict[str, object], band: str) -> dict[str, object]:
    """Return one enriched row that preserves public and factor-side grammar."""
    n_gaps = row["n_gaps"]
    p_state = row["p_neighborhood"]
    q_state = row["q_neighborhood"]
    n_word = public_word(row)
    pq_word = factor_word(row)
    distance = gwr_signed_distance(row)
    p_phase_word = factor_side_phase_word(p_state)
    q_phase_word = factor_side_phase_word(q_state)
    p_position_word = factor_side_word(p_state)
    q_position_word = factor_side_word(q_state)
    out = {
        "rule_id": RULE_ID,
        "band": band,
        "case_id": row["case_id"],
        "N": row["N"],
        "p": row["p"],
        "q": row["q"],
        "public_word": n_word,
        "public_previous_reduced_state": n_gaps["previous"]["reduced_state"],
        "public_containing_reduced_state": n_gaps["containing"]["reduced_state"],
        "public_containing_exact_type_key": n_gaps["containing"]["exact_type_key"],
        "public_containing_phase_bucket": row["n_containing_gap_phase_bucket"],
        "public_following_reduced_state": n_gaps["following"]["reduced_state"],
        "public_containing_gap_width": row["n_containing_gap_width"],
        "public_n_offset_from_left": row["n_offset_from_left"],
        "public_n_offset_from_right": row["n_offset_from_right"],
        "public_n_position_mpermille": row["n_containing_gap_position_mpermille"],
        "public_gwr_winner_offset": n_gaps["containing"]["winner_offset"],
        "public_gwr_signed_distance": distance,
        "public_gwr_side": gwr_side(distance),
        "public_previous_gap": gap_summary(n_gaps["previous"]),
        "public_containing_gap": gap_summary(n_gaps["containing"]),
        "public_following_gap": gap_summary(n_gaps["following"]),
        "factor_residue_multiset": factor_residue_multiset(pq_word),
        "factor_phase_multiset": factor_phase_multiset(pq_word),
        "factor_reduced_word": row["factor_neighborhood_signature"],
        "factor_phased_word": row["factor_phased_neighborhood_signature"],
        "factor_positioned_word": row["factor_positioned_neighborhood_signature"],
        "p_phase_word": p_phase_word,
        "q_phase_word": q_phase_word,
        "oriented_factor_phase_word": f"p={p_phase_word} || q={q_phase_word}",
        "oriented_factor_phase_word_swapped": f"p={q_phase_word} || q={p_phase_word}",
        "p_position_word": p_position_word,
        "q_position_word": q_position_word,
        "oriented_factor_position_word": f"p={p_position_word} || q={q_position_word}",
        "analysis_role": "p_q_are_downstream_labels_for_corpus_construction",
    }
    out.update(side_features("p", p_state))
    out.update(side_features("q", q_state))
    return out


def projection_key(row: dict[str, object], projection: str) -> str:
    """Return a deterministic projection key for one enriched row."""
    if projection == "current_compressed":
        return " || ".join(
            (
                str(row["public_word"]),
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
        )
    if projection == "current_plus_gwr_side":
        return " || ".join(
            (
                str(row["public_word"]),
                str(row["public_gwr_side"]),
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
        )
    if projection == "current_plus_gwr_distance":
        return " || ".join(
            (
                str(row["public_word"]),
                str(row["public_gwr_signed_distance"]),
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
        )
    if projection == "factor_phased_word":
        return " || ".join((str(row["public_word"]), str(row["factor_phased_word"])))
    if projection == "factor_positioned_word":
        return " || ".join((str(row["public_word"]), str(row["factor_positioned_word"])))
    if projection == "oriented_factor_phase_word":
        return " || ".join((str(row["public_word"]), str(row["oriented_factor_phase_word"])))
    if projection == "oriented_factor_position_word":
        return " || ".join((str(row["public_word"]), str(row["oriented_factor_position_word"])))
    raise ValueError(f"unknown projection: {projection}")


def projection_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return compression diagnostics for several map projections."""
    projections = (
        "current_compressed",
        "current_plus_gwr_side",
        "current_plus_gwr_distance",
        "factor_phased_word",
        "factor_positioned_word",
        "oriented_factor_phase_word",
        "oriented_factor_position_word",
    )
    out = []
    total = len(rows)
    for projection in projections:
        counts = Counter(projection_key(row, projection) for row in rows)
        collision_counts = [count for count in counts.values() if count > 1]
        out.append(
            {
                "rule_id": RULE_ID,
                "projection": projection,
                "row_count": total,
                "distinct_key_count": len(counts),
                "collision_key_count": len(collision_counts),
                "keys_with_multiplicity_at_least_3": sum(
                    1 for count in counts.values() if count >= 3
                ),
                "keys_with_multiplicity_at_least_5": sum(
                    1 for count in counts.values() if count >= 5
                ),
                "keys_with_multiplicity_at_least_10": sum(
                    1 for count in counts.values() if count >= 10
                ),
                "max_rows_per_key": max(counts.values()) if counts else 0,
                "mean_rows_per_key_mpermille": total * 1000 // len(counts) if counts else 0,
                "top_keys": [
                    {"value": value, "count": count}
                    for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]
                ],
            }
        )
    return out


def build_corpus(
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return enriched rows, projection diagnostics, and summary."""
    rows = []
    semiprime_counts = {}
    for min_factor, max_factor in bands:
        band = band_key(min_factor, max_factor)
        triples = semiprime_triples(
            min_factor,
            max_factor,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        semiprime_counts[band] = len(triples)
        for triple in triples:
            rows.append(enriched_row(corpus_row(triple), band))

    projections = projection_rows(rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_enriched_multiplication_map_corpus",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "row_count": len(rows),
        "semiprime_counts_by_band": semiprime_counts,
        "public_word_count": len({row["public_word"] for row in rows}),
        "factor_residue_phase_class_count": len(
            {
                (row["factor_residue_multiset"], row["factor_phase_multiset"])
                for row in rows
            }
        ),
        "factor_phased_word_count": len({row["factor_phased_word"] for row in rows}),
        "factor_positioned_word_count": len({row["factor_positioned_word"] for row in rows}),
        "projection_distinct_key_counts": {
            row["projection"]: row["distinct_key_count"]
            for row in projections
        },
    }
    return rows, projections, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build enriched PEDK multiplication-map corpus.")
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Build and write enriched multiplication-map corpus."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    rows, projections, summary = build_corpus(
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    summary["bands"] = [
        {
            "min_factor": min_factor,
            "max_factor": max_factor,
            "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
        }
        for min_factor, max_factor in bands
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "enriched_rows.jsonl", rows)
    write_jsonl(args.output_dir / "projection_rows.jsonl", projections)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
