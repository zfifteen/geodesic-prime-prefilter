"""Compare below-witness and above-witness adjacent terminal hits."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from collatz_pgs_reset_length_strata_probe import read_jsonl, write_json, write_jsonl
from collatz_pgs_same_gap_scale_probe import PrimeContext, Transition, first_descent_block
from collatz_pgs_terminal_contact_decomposition_probe import (
    CLASS_NO_WITNESS,
    CLASS_NONTERMINAL,
    CLASS_TERMINAL,
    classify_transitions,
    max_source_in_rows,
)
from collatz_pgs_terminal_exact_vs_adjacent_probe import (
    CLASS_EXACT_TERMINAL,
    ResetGeometryStats,
    comparison,
    comparison_summary,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "output" / "collatz_pgs_same_gap_scale_probe" / "block_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = ROOT / "output" / "collatz_pgs_terminal_adjacent_side_probe"
CLASS_BELOW_WITNESS = "below_witness_terminal_hit"
CLASS_ABOVE_WITNESS = "above_witness_terminal_hit"
MATCHED_CLASSES = (
    CLASS_BELOW_WITNESS,
    CLASS_ABOVE_WITNESS,
    CLASS_NO_WITNESS,
)
CLASS_COUNTS = (
    CLASS_EXACT_TERMINAL,
    CLASS_BELOW_WITNESS,
    CLASS_ABOVE_WITNESS,
    CLASS_NONTERMINAL,
    CLASS_NO_WITNESS,
)


def terminal_side_class(
    transitions: list[Transition],
    context: PrimeContext,
) -> str:
    """Classify terminal witness contact by side of the PGS witness."""
    block_class = classify_transitions(transitions, context)
    if block_class != CLASS_TERMINAL:
        return block_class

    final_state = context.source_state(transitions[-1].source)
    if final_state.is_prime or not final_state.odd_projected_witness_hit:
        raise ValueError(f"invalid terminal witness state n={final_state.n}")

    offset = final_state.n - final_state.witness
    if offset == -1:
        return CLASS_BELOW_WITNESS
    if offset == 1:
        return CLASS_ABOVE_WITNESS
    if offset == 0:
        return CLASS_EXACT_TERMINAL
    raise ValueError(f"unexpected terminal witness offset={offset} n={final_state.n}")


def load_strata(path: Path, context: PrimeContext):
    """Load rows into exact odd-step and final-v2 strata."""
    strata = defaultdict(
        lambda: {label: ResetGeometryStats() for label in MATCHED_CLASSES}
    )
    class_counts = {label: 0 for label in CLASS_COUNTS}

    for row in read_jsonl(path):
        seed = int(row["seed"])
        transitions = first_descent_block(seed)
        odd_steps = int(row["odd_steps_to_first_descent"])
        final_v2 = transitions[-1].v2
        if len(transitions) != odd_steps:
            raise ValueError(f"seed={seed} odd-step mismatch")
        if "final_v2" in row and int(row["final_v2"]) != final_v2:
            raise ValueError(f"seed={seed} final-v2 mismatch")

        block_class = terminal_side_class(transitions, context)
        class_counts[block_class] += 1
        if block_class in MATCHED_CLASSES:
            strata[(odd_steps, final_v2)][block_class].add(row, transitions, context)

    return strata, class_counts


def stratum_row(
    key: tuple[int, int],
    stats: dict[str, ResetGeometryStats],
) -> dict[str, object]:
    """Return one exact-step and final-v2 adjacent-side stratum row."""
    below = stats[CLASS_BELOW_WITNESS].record()
    above = stats[CLASS_ABOVE_WITNESS].record()
    no_witness = stats[CLASS_NO_WITNESS].record()
    return {
        "odd_steps_to_first_descent": key[0],
        "final_v2": key[1],
        CLASS_BELOW_WITNESS: below,
        CLASS_ABOVE_WITNESS: above,
        CLASS_NO_WITNESS: no_witness,
        "below_vs_above": comparison(below, above),
        "below_vs_no_witness": comparison(below, no_witness),
        "above_vs_no_witness": comparison(above, no_witness),
    }


def run_probe(input_path: Path, output_dir: Path) -> dict[str, object]:
    """Run the adjacent terminal side probe."""
    context = PrimeContext(max_source_in_rows(input_path))
    strata, class_counts = load_strata(input_path, context)
    rows = [stratum_row(key, strata[key]) for key in sorted(strata)]
    try:
        input_label = str(input_path.relative_to(ROOT))
    except ValueError:
        input_label = str(input_path)

    summary = {
        "input": input_label,
        "strata_count": len(rows),
        "class_counts": class_counts,
        "below_vs_above": comparison_summary(rows, "below_vs_above"),
        "below_vs_no_witness": comparison_summary(rows, "below_vs_no_witness"),
        "above_vs_no_witness": comparison_summary(rows, "above_vs_no_witness"),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(summary, output_dir / "summary.json")
    write_jsonl(rows, output_dir / "strata_rows.jsonl")
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Compare below-witness and above-witness adjacent terminal hits "
            "inside exact odd-step and final-v2 strata."
        ),
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    """Run the command-line probe."""
    args = parse_args()
    summary = run_probe(Path(args.input), Path(args.output_dir))
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
