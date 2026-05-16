#!/usr/bin/env python3
"""Build the supported public-word pivot for PEDK rule extraction."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    corpus_row,
    semiprime_triples,
    write_json,
    write_jsonl,
)
from gwr_relative_all_o6_boundary import gwr_signed_distance
from multiplication_map_law_surface import DEFAULT_BANDS, public_word as surface_public_word
from public_feature_all_o6_boundary import parse_bands


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_MAP_DIR = THIS_DIR / "output" / "multiplication_map_law_surface_601_5500"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_pivot_601_5500"
RULE_ID = "pedk_public_grammar_pivot_v1"
PUBLIC_PATTERN = re.compile(r"^prev=(?P<prev>.+)\|containing=(?P<containing>.+)@(?P<phase>[^@|]+)\|next=(?P<next>.+)$")
FACTOR_SIDE_PATTERN = re.compile(r"[LR]=(?P<residue>o[246])_.*?@(?P<phase>early|mid|late|very_late|empty)")


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON document."""
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def parse_public_word(public_word: str) -> dict[str, str]:
    """Return coordinate fields from the public grammar word."""
    match = PUBLIC_PATTERN.match(public_word)
    if not match:
        raise ValueError(f"invalid public word: {public_word}")
    return match.groupdict()


def factor_residue_multiset(factor_word: str) -> str:
    """Return sorted residue multiset for a factor word."""
    residues = sorted(match.group("residue") for match in FACTOR_SIDE_PATTERN.finditer(factor_word))
    if len(residues) != 4:
        raise ValueError(f"expected four factor residues: {factor_word}")
    counts = Counter(residues)
    return "|".join(f"{residue}:{counts[residue]}" for residue in ("o2", "o4", "o6") if counts[residue])


def factor_phase_multiset(factor_word: str) -> str:
    """Return sorted winner-phase multiset for a factor word."""
    phases = sorted(match.group("phase") for match in FACTOR_SIDE_PATTERN.finditer(factor_word))
    if len(phases) != 4:
        raise ValueError(f"expected four factor phases: {factor_word}")
    counts = Counter(phases)
    order = ("early", "mid", "late", "very_late", "empty")
    return "|".join(f"{phase}:{counts[phase]}" for phase in order if counts[phase])


def is_uniform_residue(factor_word: str) -> bool:
    """Return true when all four factor residues match."""
    return len(set(match.group("residue") for match in FACTOR_SIDE_PATTERN.finditer(factor_word))) == 1


def is_all_o6(factor_word: str) -> bool:
    """Return true when all four factor residues are o6."""
    return factor_residue_multiset(factor_word) == "o6:4"


def top_rows(counter: Counter[str], limit: int) -> list[dict[str, object]]:
    """Return top counter entries."""
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def load_gwr_distances(
    bands: list[tuple[int, int]],
    supported_public_words: set[str],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> dict[str, Counter[int]]:
    """Return GWR distance support by full public word."""
    distances: dict[str, Counter[int]] = defaultdict(Counter)
    for min_factor, max_factor in bands:
        triples = semiprime_triples(
            min_factor,
            max_factor,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        for triple in triples:
            row = corpus_row(triple)
            word = surface_public_word(row)
            if word in supported_public_words:
                distances[word][gwr_signed_distance(row)] += 1
    return distances


def build_pivot(
    map_dir: Path,
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return one row per supported public grammar word."""
    map_summary = read_json(map_dir / "summary.json")
    supported_public_count = int(map_summary["supported_public_word_count"])
    supported_factor_count = int(map_summary["supported_factor_word_count"])
    public_rows = read_jsonl(map_dir / "public_word_rows.jsonl")
    cell_rows = read_jsonl(map_dir / "map_cell_rows.jsonl")

    supported_public_words = {
        str(row["public_word"])
        for row in public_rows
        if int(row["forward_row_count"]) >= int(map_summary["min_public_support"])
    }
    if len(supported_public_words) != supported_public_count:
        raise ValueError("supported public word count mismatch")
    gwr_distances = load_gwr_distances(
        bands,
        supported_public_words,
        max_ratio_numerator,
        max_ratio_denominator,
    )

    observed_factor_count = Counter()
    exclusion_count = Counter()
    residue_multisets: dict[str, Counter[str]] = defaultdict(Counter)
    phase_multisets: dict[str, Counter[str]] = defaultdict(Counter)
    uniform_counts = Counter()
    all_o6_counts = Counter()

    for row in cell_rows:
        public_word = str(row["public_word"])
        if public_word not in supported_public_words:
            continue
        factor_word = str(row["factor_word"])
        if row.get("status") == "candidate_exclusion_not_observed":
            exclusion_count[public_word] += 1
            continue
        count = int(row["forward_row_count"])
        observed_factor_count[public_word] += 1
        residue_multisets[public_word][factor_residue_multiset(factor_word)] += count
        phase_multisets[public_word][factor_phase_multiset(factor_word)] += count
        if is_uniform_residue(factor_word):
            uniform_counts[public_word] += count
        if is_all_o6(factor_word):
            all_o6_counts[public_word] += count

    pivot_rows = []
    for row in public_rows:
        public_word = str(row["public_word"])
        if public_word not in supported_public_words:
            continue
        parsed = parse_public_word(public_word)
        distance_counter = gwr_distances[public_word]
        pivot_rows.append(
            {
                "rule_id": RULE_ID,
                "public_word": public_word,
                "previous_reduced_state": parsed["prev"],
                "containing_exact_type": parsed["containing"],
                "n_phase": parsed["phase"],
                "next_reduced_state": parsed["next"],
                "forward_row_count": int(row["forward_row_count"]),
                "observed_factor_word_count": observed_factor_count[public_word],
                "candidate_exclusions_covered": exclusion_count[public_word],
                "uniform_factor_row_count": uniform_counts[public_word],
                "all_o6_row_count": all_o6_counts[public_word],
                "top_gwr_signed_distances": top_rows(
                    Counter({str(distance): count for distance, count in distance_counter.items()}),
                    8,
                ),
                "top_factor_residue_multisets": top_rows(residue_multisets[public_word], 8),
                "top_factor_phase_multisets": top_rows(phase_multisets[public_word], 8),
                "top_factor_words": row["top_factor_words"],
            }
        )

    pivot_rows.sort(key=lambda item: (-int(item["candidate_exclusions_covered"]), item["public_word"]))
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_pivot",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "pivot_public_word_count": len(pivot_rows),
        "supported_factor_word_count": supported_factor_count,
        "candidate_exclusion_count": int(map_summary["candidate_exclusion_count"]),
        "min_public_support": int(map_summary["min_public_support"]),
        "min_factor_support": int(map_summary["min_factor_support"]),
    }
    return pivot_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build supported public grammar pivot.")
    parser.add_argument("--map-dir", type=Path, default=DEFAULT_MAP_DIR)
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run public grammar pivot extraction."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    pivot_rows, summary = build_pivot(
        args.map_dir,
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "public_grammar_pivot_rows.jsonl", pivot_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
