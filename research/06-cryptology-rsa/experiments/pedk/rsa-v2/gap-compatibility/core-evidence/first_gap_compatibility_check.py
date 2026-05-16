#!/usr/bin/env python3
"""Search small-scale PEDK gap-type compatibility patterns."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import gmpy2


THIS_DIR = Path(__file__).resolve().parent
ROOT = next(
    parent
    for parent in THIS_DIR.parents
    if (parent / "src" / "python").exists() and (parent / "research").exists()
)
EXPERIMENTS_DIR = ROOT / "research" / "06-cryptology-rsa" / "experiments"
SOURCE_DIR = ROOT / "src" / "python"
LIVE_SOLVER_DIR = EXPERIMENTS_DIR / "live-solver" / "rsa-v2"
GRAMMAR_DIR = EXPERIMENTS_DIR / "modulus-recursive-catalogs" / "rsa-v2"
for import_dir in (SOURCE_DIR, LIVE_SOLVER_DIR, GRAMMAR_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from modulus_gap_grammar_probe import gap_grammar, neighboring_gaps  # noqa: E402
from run_experiment import divisor_counts_segment  # noqa: E402


RULE_ID = "pedk_gap_compatibility_search_v1"
DEFAULT_MIN_FACTOR = 31
DEFAULT_MAX_FACTOR = 600
DEFAULT_MAX_RATIO_NUMERATOR = 4
DEFAULT_MAX_RATIO_DENOMINATOR = 1
DEFAULT_MIN_SUPPORT = 50
POSITION_BUCKET_COUNT = 10
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "gap_compatibility_search"


@dataclass(frozen=True)
class SemiprimeTriple:
    """One known semiprime triple used for downstream corpus labeling."""

    case_id: str
    bits: int
    n: int
    p: int
    q: int


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def pgs_endpoints_through(limit: int) -> list[int]:
    """Return exact endpoint coordinates through a small divisor-count interval."""
    if limit < 2:
        return []
    counts = divisor_counts_segment(2, limit + 1)
    return [
        2 + index
        for index, raw_count in enumerate(counts)
        if int(raw_count) == 2
    ]


def semiprime_triples(
    min_factor: int,
    max_factor: int,
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> list[SemiprimeTriple]:
    """Return deterministic semiprime triples from exact endpoint coordinates."""
    endpoints = [
        endpoint
        for endpoint in pgs_endpoints_through(max_factor)
        if endpoint >= min_factor
    ]
    triples: list[SemiprimeTriple] = []
    for left_index, p_value in enumerate(endpoints):
        for q_value in endpoints[left_index + 1 :]:
            if q_value * max_ratio_denominator > p_value * max_ratio_numerator:
                break
            n_value = p_value * q_value
            triples.append(
                SemiprimeTriple(
                    case_id=f"small_semiprime_{p_value}_{q_value}",
                    bits=n_value.bit_length(),
                    n=n_value,
                    p=p_value,
                    q=q_value,
                )
            )
    return triples


def grammar_around_coordinate(role_prefix: str, coordinate: int) -> dict[str, object]:
    """Return previous, containing, and following gap grammar around a coordinate."""
    previous, left, right, following = neighboring_gaps(gmpy2.mpz(coordinate))
    previous_gap = gap_grammar(f"{role_prefix}_previous", previous, left)
    containing_gap = gap_grammar(f"{role_prefix}_containing", left, right, gmpy2.mpz(coordinate))
    following_gap = gap_grammar(f"{role_prefix}_following", right, following)
    return {
        "previous": previous_gap,
        "containing": containing_gap,
        "following": following_gap,
    }


def factor_neighborhood(side: str, value: int) -> dict[str, object]:
    """Return left and right gap grammar around a known factor endpoint."""
    endpoint = gmpy2.mpz(value)
    previous, _left, _right, following = neighboring_gaps(endpoint)
    return {
        "left": gap_grammar(f"{side}_left", previous, endpoint),
        "right": gap_grammar(f"{side}_right", endpoint, following),
    }


def ordered_factor_signature(p_state: dict[str, object], q_state: dict[str, object]) -> str:
    """Return orientation-stable factor-neighborhood signature."""
    p_signature = (
        f"L={p_state['left']['reduced_state']}|"
        f"R={p_state['right']['reduced_state']}"
    )
    q_signature = (
        f"L={q_state['left']['reduced_state']}|"
        f"R={q_state['right']['reduced_state']}"
    )
    return " || ".join(sorted((p_signature, q_signature)))


def relative_position_mpermille(containing_gap: dict[str, object]) -> int:
    """Return N position inside its containing gap as integer thousandths."""
    gap_width = int(containing_gap["gap_width"])
    offset = containing_gap["coordinate_offset_from_left"]
    if offset is None:
        raise ValueError("containing gap is missing coordinate offset")
    if gap_width < 1:
        raise ValueError("gap width must be positive")
    return int(offset) * 1000 // gap_width


def relative_position_bucket(containing_gap: dict[str, object]) -> str:
    """Return a stable decile bucket for N's position inside its gap."""
    mpermille = relative_position_mpermille(containing_gap)
    bucket_index = min(POSITION_BUCKET_COUNT - 1, mpermille * POSITION_BUCKET_COUNT // 1000)
    low = bucket_index * 100
    high = low + 99
    return f"pos{low:03d}_{high:03d}"


def phase_bucket(mpermille: int | None) -> str:
    """Return a coarse early/mid/late phase bucket."""
    if mpermille is None:
        return "empty"
    if mpermille < 250:
        return "early"
    if mpermille < 750:
        return "mid"
    if mpermille < 900:
        return "late"
    return "very_late"


def relative_phase_bucket(containing_gap: dict[str, object]) -> str:
    """Return a coarse phase bucket for N's position inside its gap."""
    return phase_bucket(relative_position_mpermille(containing_gap))


def winner_position_mpermille(gap: dict[str, object]) -> int | None:
    """Return a gap winner position as integer thousandths when present."""
    winner_offset = gap["winner_offset"]
    if winner_offset is None:
        return None
    gap_width = int(gap["gap_width"])
    if gap_width < 1:
        raise ValueError("gap width must be positive")
    return int(winner_offset) * 1000 // gap_width


def winner_position_bucket(gap: dict[str, object]) -> str:
    """Return a stable decile bucket for a gap winner position."""
    mpermille = winner_position_mpermille(gap)
    if mpermille is None:
        return "empty"
    bucket_index = min(POSITION_BUCKET_COUNT - 1, mpermille * POSITION_BUCKET_COUNT // 1000)
    low = bucket_index * 100
    high = low + 99
    return f"winpos{low:03d}_{high:03d}"


def positioned_gap_state(gap: dict[str, object]) -> str:
    """Return reduced gap state refined by its winner position."""
    return f"{gap['reduced_state']}@{winner_position_bucket(gap)}"


def phased_gap_state(gap: dict[str, object]) -> str:
    """Return reduced gap state refined by its winner phase."""
    return f"{gap['reduced_state']}@{phase_bucket(winner_position_mpermille(gap))}"


def ordered_factor_positioned_signature(
    p_state: dict[str, object],
    q_state: dict[str, object],
) -> str:
    """Return orientation-stable factor-neighborhood signature with winner positions."""
    p_signature = (
        f"L={positioned_gap_state(p_state['left'])}|"
        f"R={positioned_gap_state(p_state['right'])}"
    )
    q_signature = (
        f"L={positioned_gap_state(q_state['left'])}|"
        f"R={positioned_gap_state(q_state['right'])}"
    )
    return " || ".join(sorted((p_signature, q_signature)))


def ordered_factor_phased_signature(
    p_state: dict[str, object],
    q_state: dict[str, object],
) -> str:
    """Return orientation-stable factor-neighborhood signature with winner phases."""
    p_signature = (
        f"L={phased_gap_state(p_state['left'])}|"
        f"R={phased_gap_state(p_state['right'])}"
    )
    q_signature = (
        f"L={phased_gap_state(q_state['left'])}|"
        f"R={phased_gap_state(q_state['right'])}"
    )
    return " || ".join(sorted((p_signature, q_signature)))


def corpus_row(triple: SemiprimeTriple) -> dict[str, object]:
    """Return one typed compatibility-corpus row."""
    n_gaps = grammar_around_coordinate("n", triple.n)
    p_gaps = factor_neighborhood("p", triple.p)
    q_gaps = factor_neighborhood("q", triple.q)
    factor_signature = ordered_factor_signature(p_gaps, q_gaps)
    factor_positioned_signature = ordered_factor_positioned_signature(p_gaps, q_gaps)
    factor_phased_signature = ordered_factor_phased_signature(p_gaps, q_gaps)
    n_containing_gap = n_gaps["containing"]
    n_state = str(n_containing_gap["reduced_state"])
    n_position_bucket = relative_position_bucket(n_containing_gap)
    n_positioned_state = f"{n_state}@{n_position_bucket}"
    n_phase_bucket = relative_phase_bucket(n_containing_gap)
    n_phased_state = f"{n_state}@{n_phase_bucket}"
    return {
        "case_id": triple.case_id,
        "bits": triple.bits,
        "N": str(triple.n),
        "p": str(triple.p),
        "q": str(triple.q),
        "rule_id": RULE_ID,
        "n_containing_gap_reduced_state": n_state,
        "n_containing_gap_position_bucket": n_position_bucket,
        "n_containing_gap_phase_bucket": n_phase_bucket,
        "n_containing_gap_position_mpermille": relative_position_mpermille(n_containing_gap),
        "n_containing_gap_positioned_state": n_positioned_state,
        "n_containing_gap_phased_state": n_phased_state,
        "n_containing_gap_width": n_containing_gap["gap_width"],
        "n_offset_from_left": n_containing_gap["coordinate_offset_from_left"],
        "n_offset_from_right": n_containing_gap["coordinate_offset_from_right"],
        "n_previous_gap_reduced_state": n_gaps["previous"]["reduced_state"],
        "n_following_gap_reduced_state": n_gaps["following"]["reduced_state"],
        "p_left_gap_reduced_state": p_gaps["left"]["reduced_state"],
        "p_right_gap_reduced_state": p_gaps["right"]["reduced_state"],
        "q_left_gap_reduced_state": q_gaps["left"]["reduced_state"],
        "q_right_gap_reduced_state": q_gaps["right"]["reduced_state"],
        "p_left_gap_winner_position_bucket": winner_position_bucket(p_gaps["left"]),
        "p_right_gap_winner_position_bucket": winner_position_bucket(p_gaps["right"]),
        "q_left_gap_winner_position_bucket": winner_position_bucket(q_gaps["left"]),
        "q_right_gap_winner_position_bucket": winner_position_bucket(q_gaps["right"]),
        "p_left_gap_winner_phase_bucket": phase_bucket(winner_position_mpermille(p_gaps["left"])),
        "p_right_gap_winner_phase_bucket": phase_bucket(winner_position_mpermille(p_gaps["right"])),
        "q_left_gap_winner_phase_bucket": phase_bucket(winner_position_mpermille(q_gaps["left"])),
        "q_right_gap_winner_phase_bucket": phase_bucket(winner_position_mpermille(q_gaps["right"])),
        "p_left_gap_winner_position_mpermille": winner_position_mpermille(p_gaps["left"]),
        "p_right_gap_winner_position_mpermille": winner_position_mpermille(p_gaps["right"]),
        "q_left_gap_winner_position_mpermille": winner_position_mpermille(q_gaps["left"]),
        "q_right_gap_winner_position_mpermille": winner_position_mpermille(q_gaps["right"]),
        "factor_neighborhood_signature": factor_signature,
        "factor_positioned_neighborhood_signature": factor_positioned_signature,
        "factor_phased_neighborhood_signature": factor_phased_signature,
        "compatibility_key": f"{n_state} -> {factor_signature}",
        "positioned_compatibility_key": f"{n_positioned_state} -> {factor_signature}",
        "phased_compatibility_key": f"{n_phased_state} -> {factor_signature}",
        "positioned_factor_compatibility_key": (
            f"{n_positioned_state} -> {factor_positioned_signature}"
        ),
        "phased_factor_compatibility_key": f"{n_phased_state} -> {factor_phased_signature}",
        "n_gaps": n_gaps,
        "p_neighborhood": p_gaps,
        "q_neighborhood": q_gaps,
        "analysis_role": "p_q_are_downstream_labels_for_corpus_construction",
    }


def compatibility_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed compatibility counts by public N-gap type."""
    return compatibility_rows_for_field(rows, "n_containing_gap_reduced_state")


def positioned_compatibility_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed compatibility counts by public N-gap type and position."""
    return compatibility_rows_for_field(rows, "n_containing_gap_positioned_state")


def phased_compatibility_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed compatibility counts by public N-gap type and coarse phase."""
    return compatibility_rows_for_field(rows, "n_containing_gap_phased_state")


def compatibility_rows_for_field(
    rows: list[dict[str, object]],
    n_state_field: str,
) -> list[dict[str, object]]:
    """Return observed compatibility counts for one public N-state field."""
    return compatibility_rows_for_fields(rows, n_state_field, "factor_neighborhood_signature")


def positioned_factor_compatibility_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed compatibility counts with N position and factor winner positions."""
    return compatibility_rows_for_fields(
        rows,
        "n_containing_gap_positioned_state",
        "factor_positioned_neighborhood_signature",
    )


def phased_factor_compatibility_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed compatibility counts with N phase and factor winner phases."""
    return compatibility_rows_for_fields(
        rows,
        "n_containing_gap_phased_state",
        "factor_phased_neighborhood_signature",
    )


def compatibility_rows_for_fields(
    rows: list[dict[str, object]],
    n_state_field: str,
    factor_signature_field: str,
) -> list[dict[str, object]]:
    """Return observed compatibility counts for public N-state and factor fields."""
    counts: Counter[tuple[str, str]] = Counter()
    examples: dict[tuple[str, str], str] = {}
    for row in rows:
        key = (
            str(row[n_state_field]),
            str(row[factor_signature_field]),
        )
        counts[key] += 1
        examples.setdefault(key, str(row["case_id"]))
    return [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_reduced_state": n_state,
            "factor_neighborhood_signature": signature,
            "observed_count": count,
            "example_case_id": examples[(n_state, signature)],
        }
        for (n_state, signature), count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0][0], item[0][1]),
        )
    ]


def exclusion_candidate_rows(
    rows: list[dict[str, object]],
    min_support: int,
) -> list[dict[str, object]]:
    """Return candidate incompatibilities absent from supported N-gap classes."""
    return exclusion_candidate_rows_for_field(rows, min_support, "n_containing_gap_reduced_state")


def positioned_exclusion_candidate_rows(
    rows: list[dict[str, object]],
    min_support: int,
) -> list[dict[str, object]]:
    """Return candidate incompatibilities absent from supported positioned N classes."""
    return exclusion_candidate_rows_for_field(rows, min_support, "n_containing_gap_positioned_state")


def phased_exclusion_candidate_rows(
    rows: list[dict[str, object]],
    min_support: int,
) -> list[dict[str, object]]:
    """Return candidate incompatibilities absent from supported phased N classes."""
    return exclusion_candidate_rows_for_field(rows, min_support, "n_containing_gap_phased_state")


def exclusion_candidate_rows_for_field(
    rows: list[dict[str, object]],
    min_support: int,
    n_state_field: str,
) -> list[dict[str, object]]:
    """Return candidate incompatibilities absent from supported public classes."""
    by_n_state: dict[str, set[str]] = defaultdict(set)
    n_state_counts: Counter[str] = Counter()
    all_signatures: set[str] = set()
    for row in rows:
        n_state = str(row[n_state_field])
        signature = str(row["factor_neighborhood_signature"])
        by_n_state[n_state].add(signature)
        n_state_counts[n_state] += 1
        all_signatures.add(signature)

    output: list[dict[str, object]] = []
    for n_state, support in sorted(n_state_counts.items()):
        if support < min_support:
            continue
        observed = by_n_state[n_state]
        for signature in sorted(all_signatures - observed):
            output.append(
                {
                    "rule_id": RULE_ID,
                    "candidate_status": "candidate_incompatibility_absent_in_small_corpus",
                    "n_containing_gap_reduced_state": n_state,
                    "excluded_factor_neighborhood_signature": signature,
                    "n_state_support": support,
                    "observed_signature_count_for_n_state": len(observed),
                    "global_signature_count": len(all_signatures),
                }
            )
    return output


def summarize(
    triples: list[SemiprimeTriple],
    rows: list[dict[str, object]],
    compatibilities: list[dict[str, object]],
    exclusions: list[dict[str, object]],
    positioned_compatibilities: list[dict[str, object]],
    positioned_exclusions: list[dict[str, object]],
    positioned_factor_compatibilities: list[dict[str, object]],
    phased_compatibilities: list[dict[str, object]],
    phased_exclusions: list[dict[str, object]],
    phased_factor_compatibilities: list[dict[str, object]],
    min_factor: int,
    max_factor: int,
    max_ratio_numerator: int,
    max_ratio_denominator: int,
    min_support: int,
) -> dict[str, object]:
    """Return compact corpus and compatibility-search summary."""
    n_counts = Counter(str(row["n_containing_gap_reduced_state"]) for row in rows)
    positioned_n_counts = Counter(str(row["n_containing_gap_positioned_state"]) for row in rows)
    position_bucket_counts = Counter(str(row["n_containing_gap_position_bucket"]) for row in rows)
    phased_n_counts = Counter(str(row["n_containing_gap_phased_state"]) for row in rows)
    phase_bucket_counts = Counter(str(row["n_containing_gap_phase_bucket"]) for row in rows)
    signature_counts = Counter(str(row["factor_neighborhood_signature"]) for row in rows)
    phased_factor_signature_counts = Counter(
        str(row["factor_phased_neighborhood_signature"]) for row in rows
    )
    positioned_factor_signature_counts = Counter(
        str(row["factor_positioned_neighborhood_signature"]) for row in rows
    )
    supported_n_states = {
        state
        for state, count in n_counts.items()
        if count >= min_support
    }
    supported_positioned_states = {
        state
        for state, count in positioned_n_counts.items()
        if count >= min_support
    }
    supported_phased_states = {
        state
        for state, count in phased_n_counts.items()
        if count >= min_support
    }
    return {
        "rule_id": RULE_ID,
        "status": "measured_correlation_search",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "sidecar_only_not_live_pedk_rule",
        "position_status": "n_position_inside_containing_gap_added_as_measured_sidecar_feature",
        "min_factor": min_factor,
        "max_factor": max_factor,
        "max_factor_ratio": f"{max_ratio_numerator}/{max_ratio_denominator}",
        "semiprime_triple_count": len(triples),
        "corpus_row_count": len(rows),
        "n_containing_state_count": len(n_counts),
        "factor_neighborhood_signature_count": len(signature_counts),
        "observed_compatibility_count": len(compatibilities),
        "candidate_exclusion_count": len(exclusions),
        "position_bucket_count": len(position_bucket_counts),
        "positioned_n_state_count": len(positioned_n_counts),
        "phased_n_state_count": len(phased_n_counts),
        "observed_positioned_compatibility_count": len(positioned_compatibilities),
        "candidate_positioned_exclusion_count": len(positioned_exclusions),
        "observed_phased_compatibility_count": len(phased_compatibilities),
        "candidate_phased_exclusion_count": len(phased_exclusions),
        "factor_phased_neighborhood_signature_count": len(phased_factor_signature_counts),
        "observed_phased_factor_compatibility_count": len(phased_factor_compatibilities),
        "factor_positioned_neighborhood_signature_count": len(positioned_factor_signature_counts),
        "observed_positioned_factor_compatibility_count": len(positioned_factor_compatibilities),
        "min_support_for_exclusion": min_support,
        "supported_n_state_count": len(supported_n_states),
        "supported_positioned_n_state_count": len(supported_positioned_states),
        "supported_phased_n_state_count": len(supported_phased_states),
        "top_n_containing_states": [
            {"state": state, "count": count}
            for state, count in n_counts.most_common(12)
        ],
        "top_position_buckets": [
            {"bucket": bucket, "count": count}
            for bucket, count in position_bucket_counts.most_common(12)
        ],
        "top_phase_buckets": [
            {"bucket": bucket, "count": count}
            for bucket, count in phase_bucket_counts.most_common(12)
        ],
        "top_positioned_n_states": [
            {"state": state, "count": count}
            for state, count in positioned_n_counts.most_common(12)
        ],
        "top_phased_n_states": [
            {"state": state, "count": count}
            for state, count in phased_n_counts.most_common(12)
        ],
        "top_factor_neighborhood_signatures": [
            {"signature": signature, "count": count}
            for signature, count in signature_counts.most_common(12)
        ],
        "top_factor_phased_neighborhood_signatures": [
            {"signature": signature, "count": count}
            for signature, count in phased_factor_signature_counts.most_common(12)
        ],
        "top_factor_positioned_neighborhood_signatures": [
            {"signature": signature, "count": count}
            for signature, count in positioned_factor_signature_counts.most_common(12)
        ],
        "top_compatibilities": compatibilities[:12],
        "top_positioned_compatibilities": positioned_compatibilities[:12],
        "top_phased_compatibilities": phased_compatibilities[:12],
        "top_phased_factor_compatibilities": phased_factor_compatibilities[:12],
        "top_positioned_factor_compatibilities": positioned_factor_compatibilities[:12],
    }


def preliminary_candidate_exclusion_rule(
    phased_exclusions: list[dict[str, object]],
    summary: dict[str, object],
) -> dict[str, object]:
    """Return the preliminary phase-state exclusion rule as a sidecar artifact."""
    states: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in phased_exclusions:
        states[str(row["n_containing_gap_reduced_state"])].append(
            {
                "excluded_factor_neighborhood_signature": row[
                    "excluded_factor_neighborhood_signature"
                ],
                "n_state_support": row["n_state_support"],
                "observed_signature_count_for_n_state": row[
                    "observed_signature_count_for_n_state"
                ],
                "global_signature_count": row["global_signature_count"],
            }
        )

    return {
        "candidate_rule_id": "pedk_phase_gap_exclusion_candidate_v1",
        "source_rule_id": RULE_ID,
        "status": "candidate_sidecar_rule_not_live_pedk_inference",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_promoted",
        "corpus_scope": {
            "min_factor": summary["min_factor"],
            "max_factor": summary["max_factor"],
            "max_factor_ratio": summary["max_factor_ratio"],
            "semiprime_triple_count": summary["semiprime_triple_count"],
            "min_support_for_exclusion": summary["min_support_for_exclusion"],
        },
        "public_input": [
            "n_containing_gap_reduced_state",
            "n_containing_gap_phase_bucket",
        ],
        "downstream_label": [
            "factor_neighborhood_signature",
        ],
        "formal_candidate_rule": (
            "For a supported public phase state S = reduced_state(gap(N)) @ "
            "phase(N in gap(N)), exclude a factor-neighborhood signature F as "
            "a candidate if F is absent from all corpus rows labeled by S while "
            "S has support at least min_support_for_exclusion."
        ),
        "application_boundary": (
            "This rule filters only sidecar compatibility hypotheses. It does "
            "not identify p or q, does not close a factor pair, and is not a "
            "live PEDK resolver rule."
        ),
        "promotion_requirement": [
            "preserve the same public phase-state definition unchanged",
            "rerun on a larger exact corpus",
            "confirm each promoted exclusion survives held-out rows",
            "reject any exclusion falsified by one valid held-out row",
            "keep audit labels physically separate from live inference",
        ],
        "excluded_signature_count": len(phased_exclusions),
        "state_count_with_candidate_exclusions": len(states),
        "exclusions_by_public_phase_state": {
            state: rows
            for state, rows in sorted(states.items())
        },
    }


def run_search(
    min_factor: int,
    max_factor: int,
    max_ratio_numerator: int,
    max_ratio_denominator: int,
    min_support: int,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    dict[str, object],
    dict[str, object],
]:
    """Run the first small-scale PEDK compatibility search."""
    triples = semiprime_triples(
        min_factor,
        max_factor,
        max_ratio_numerator,
        max_ratio_denominator,
    )
    rows = [corpus_row(triple) for triple in triples]
    compatibilities = compatibility_rows(rows)
    exclusions = exclusion_candidate_rows(rows, min_support)
    positioned_compatibilities = positioned_compatibility_rows(rows)
    positioned_exclusions = positioned_exclusion_candidate_rows(rows, min_support)
    positioned_factor_compatibilities = positioned_factor_compatibility_rows(rows)
    phased_compatibilities = phased_compatibility_rows(rows)
    phased_exclusions = phased_exclusion_candidate_rows(rows, min_support)
    phased_factor_compatibilities = phased_factor_compatibility_rows(rows)
    summary = summarize(
        triples,
        rows,
        compatibilities,
        exclusions,
        positioned_compatibilities,
        positioned_exclusions,
        positioned_factor_compatibilities,
        phased_compatibilities,
        phased_exclusions,
        phased_factor_compatibilities,
        min_factor,
        max_factor,
        max_ratio_numerator,
        max_ratio_denominator,
        min_support,
    )
    candidate_rule = preliminary_candidate_exclusion_rule(phased_exclusions, summary)
    return (
        rows,
        compatibilities,
        exclusions,
        positioned_compatibilities,
        positioned_exclusions,
        positioned_factor_compatibilities,
        phased_compatibilities,
        phased_exclusions,
        phased_factor_compatibilities,
        candidate_rule,
        summary,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Search PEDK gap-type compatibilities.")
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--min-support", type=int, default=DEFAULT_MIN_SUPPORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the compatibility search and write LF-terminated artifacts."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if args.min_support < 1:
        raise ValueError("min-support must be positive")

    (
        rows,
        compatibilities,
        exclusions,
        positioned_compatibilities,
        positioned_exclusions,
        positioned_factor_compatibilities,
        phased_compatibilities,
        phased_exclusions,
        phased_factor_compatibilities,
        candidate_rule,
        summary,
    ) = run_search(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
        args.min_support,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "corpus_rows.jsonl", rows)
    write_jsonl(args.output_dir / "observed_compatibility_rows.jsonl", compatibilities)
    write_jsonl(args.output_dir / "candidate_exclusion_rows.jsonl", exclusions)
    write_jsonl(args.output_dir / "observed_positioned_compatibility_rows.jsonl", positioned_compatibilities)
    write_jsonl(args.output_dir / "candidate_positioned_exclusion_rows.jsonl", positioned_exclusions)
    write_jsonl(args.output_dir / "observed_phased_compatibility_rows.jsonl", phased_compatibilities)
    write_jsonl(args.output_dir / "candidate_phased_exclusion_rows.jsonl", phased_exclusions)
    write_jsonl(
        args.output_dir / "observed_phased_factor_compatibility_rows.jsonl",
        phased_factor_compatibilities,
    )
    write_json(args.output_dir / "preliminary_candidate_exclusion_rule.json", candidate_rule)
    write_jsonl(
        args.output_dir / "observed_positioned_factor_compatibility_rows.jsonl",
        positioned_factor_compatibilities,
    )
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
