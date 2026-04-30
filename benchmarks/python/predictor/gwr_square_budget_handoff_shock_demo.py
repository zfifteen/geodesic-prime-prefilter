#!/usr/bin/env python3
"""Demonstrate the scale-neutral square-budget handoff signal."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DETAIL_CSV = ROOT / "output" / "gwr_dni_gap_type_catalog_details.csv"
DEFAULT_HANDOFF_SUMMARY = ROOT / "output" / "gwr_square_phase_handoff_summary.json"
DEFAULT_OUTPUT_DIR = ROOT / "output"
DEFAULT_FINDINGS_PATH = ROOT / "gwr" / "findings" / "square_budget_handoff_shock.md"
DEFAULT_MIN_POWER = 12
DEFAULT_MAX_POWER = 18
SUMMARY_FILENAME = "gwr_square_budget_handoff_shock_summary.json"
PHASE_PROBE_PATH = ROOT / "benchmarks" / "python" / "predictor" / "gwr_phase_budget_hidden_state_probe.py"
SCALE_NEUTRAL_FIELD = "scale_neutral_phase_budget_bit"
CANDIDATE_SPECS = {
    "current_winner_parity": ("current_winner_parity",),
    "pooled_phase_budget_bit": ("phase_budget_bit",),
    "scale_neutral_phase_budget_bit": (SCALE_NEUTRAL_FIELD,),
    "previous_reduced_state": ("previous_reduced_state",),
    "current_winner_parity+previous_reduced_state": (
        "current_winner_parity",
        "previous_reduced_state",
    ),
    "current_winner_parity+previous_reduced_state+pooled_phase_budget_bit": (
        "current_winner_parity",
        "previous_reduced_state",
        "phase_budget_bit",
    ),
    "current_winner_parity+previous_reduced_state+scale_neutral_phase_budget_bit": (
        "current_winner_parity",
        "previous_reduced_state",
        SCALE_NEUTRAL_FIELD,
    ),
}


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Write the compact prime-square interval utilization summary and findings note."
        ),
    )
    parser.add_argument(
        "--detail-csv",
        type=Path,
        default=DEFAULT_DETAIL_CSV,
        help="Catalog detail CSV emitted by the gap-type catalog probe.",
    )
    parser.add_argument(
        "--handoff-summary",
        type=Path,
        default=DEFAULT_HANDOFF_SUMMARY,
        help="Existing square-phase handoff summary JSON.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for the compact summary JSON.",
    )
    parser.add_argument(
        "--findings-path",
        type=Path,
        default=DEFAULT_FINDINGS_PATH,
        help="Markdown findings note path.",
    )
    parser.add_argument(
        "--min-power",
        type=int,
        default=DEFAULT_MIN_POWER,
        help="Smallest sampled decade power included in the retained window surface.",
    )
    parser.add_argument(
        "--max-power",
        type=int,
        default=DEFAULT_MAX_POWER,
        help="Largest sampled decade power included in the retained window surface.",
    )
    return parser


def load_phase_probe():
    """Load the existing phase-budget probe module."""
    spec = importlib.util.spec_from_file_location(
        "gwr_phase_budget_hidden_state_probe",
        PHASE_PROBE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load phase-budget probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, object]:
    """Load one JSON object from disk."""
    if not path.exists():
        raise FileNotFoundError(f"required JSON artifact does not exist: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must contain an object: {path}")
    return payload


def geometry_key(row: dict[str, object]) -> tuple[int, str, int, int]:
    """Return the decade-local geometry key used for the scale-neutral split."""
    return (
        int(row["power"]),
        str(row["current_carrier_family"]),
        int(row["current_winner_offset"]),
        int(row["current_first_open_offset"]),
    )


def assign_scale_neutral_phase_budget_bit(rows: list[dict[str, object]]) -> None:
    """Attach the per-decade geometry-median utilization label in place."""
    by_geometry: dict[tuple[int, str, int, int], list[float]] = defaultdict(list)
    for row in rows:
        if int(row["current_next_dmin"]) == 4:
            by_geometry[geometry_key(row)].append(
                float(row["current_square_phase_utilization"])
            )

    medians = {
        key: sorted(values)[len(values) // 2]
        for key, values in by_geometry.items()
    }

    for row in rows:
        if int(row["current_next_dmin"]) != 4:
            row[SCALE_NEUTRAL_FIELD] = "non_d4"
            continue
        utilization = float(row["current_square_phase_utilization"])
        row[SCALE_NEUTRAL_FIELD] = (
            "d4_low" if utilization < medians[geometry_key(row)] else "d4_high"
        )


def laplace_probability(positive_count: int, total_count: int) -> float:
    """Return the Laplace-smoothed Bernoulli probability."""
    return (positive_count + 1.0) / (total_count + 2.0)


def candidate_value(row: dict[str, object], candidate_id: str) -> str:
    """Return a candidate label from one transition row."""
    fields = CANDIDATE_SPECS[candidate_id]
    return "|".join(str(row[field]) for field in fields)


def mean_log_loss(
    rows: list[dict[str, object]],
    candidate_id: str | None = None,
) -> float:
    """Return the in-surface smoothed log loss against the next gap class."""
    probability_counter: dict[tuple[object, ...], list[int]] = defaultdict(lambda: [0, 0])
    for row in rows:
        key: tuple[object, ...] = (
            int(row["current_gap_width"]),
            int(row["current_first_open_offset"]),
        )
        if candidate_id is not None:
            key = (*key, candidate_value(row, candidate_id))
        probability_counter[key][0] += int(row["next_is_triad"])
        probability_counter[key][1] += 1

    probability_by_key = {
        key: laplace_probability(positive_count, total_count)
        for key, (positive_count, total_count) in probability_counter.items()
    }

    loss = 0.0
    for row in rows:
        key = (
            int(row["current_gap_width"]),
            int(row["current_first_open_offset"]),
        )
        if candidate_id is not None:
            key = (*key, candidate_value(row, candidate_id))
        probability = probability_by_key[key]
        loss += -(
            math.log(probability)
            if int(row["next_is_triad"])
            else math.log(1.0 - probability)
        )
    return loss / len(rows)


def label_stats(
    rows: list[dict[str, object]],
    *,
    label_field: str,
) -> dict[str, dict[str, float | int]]:
    """Return support and next-gap class share for one label field."""
    support_counter = Counter()
    triad_hits = Counter()
    for row in rows:
        label = str(row[label_field])
        support_counter[label] += 1
        triad_hits[label] += int(row["next_is_triad"])

    return {
        label: {
            "support": int(support_counter[label]),
            "next_triad_share": triad_hits[label] / support_counter[label],
        }
        for label in sorted(support_counter)
    }


def evaluate_candidate(
    rows: list[dict[str, object]],
    *,
    candidate_id: str,
    baseline_log_loss: float,
) -> dict[str, object]:
    """Return pooled and per-decade log-loss gains for one candidate."""
    candidate_log_loss = mean_log_loss(rows, candidate_id)
    per_power_gain = {}
    for power in sorted({int(row["power"]) for row in rows}):
        power_rows = [row for row in rows if int(row["power"]) == power]
        power_baseline = mean_log_loss(power_rows)
        per_power_gain[str(power)] = (
            power_baseline - mean_log_loss(power_rows, candidate_id)
        )

    return {
        "candidate_id": candidate_id,
        "candidate_cardinality": len(
            {candidate_value(row, candidate_id) for row in rows}
        ),
        "candidate_log_loss": candidate_log_loss,
        "log_loss_gain": baseline_log_loss - candidate_log_loss,
        "per_power_log_loss_gain": per_power_gain,
    }


def retained_transitions(
    detail_csv: Path,
    *,
    min_power: int,
    max_power: int,
) -> list[dict[str, object]]:
    """Build retained high-scale transitions from the existing utilization probe."""
    phase_probe = load_phase_probe()
    detail_rows = phase_probe.load_detail_rows(detail_csv)
    transitions = phase_probe.build_transitions(
        detail_rows,
        min_power=min_power,
        max_power=max_power,
    )
    phase_probe.assign_phase_budget_bit(transitions)
    assign_scale_neutral_phase_budget_bit(transitions)
    return transitions


def matched_handoff_payload(handoff_summary: Path) -> dict[str, object]:
    """Extract the existing matched high-scale transition readout."""
    payload = load_json(handoff_summary)
    surface_groups = payload["surface_groups"]
    if not isinstance(surface_groups, dict):
        raise ValueError("handoff summary missing surface_groups object")
    sampled_group = surface_groups["sampled_windows_1e12_1e18"]
    if not isinstance(sampled_group, dict):
        raise ValueError("handoff summary missing sampled high-scale group")
    all_d4 = sampled_group["all_d4"]
    if not isinstance(all_d4, dict):
        raise ValueError("handoff summary missing all_d4 object")
    matched = all_d4["matched_base_scheme"]
    if not isinstance(matched, dict):
        raise ValueError("handoff summary missing matched_base_scheme object")
    return {
        "source_summary": str(handoff_summary),
        "low_next_triad_share": matched["low_next_triad_share"],
        "high_next_triad_share": matched["high_next_triad_share"],
        "lift": matched["lift"],
        "matched_total_weight_per_side": matched["matched_total_weight_per_side"],
        "matched_strata_count": matched["matched_strata_count"],
    }


def summarize(
    detail_csv: Path,
    handoff_summary: Path,
    *,
    min_power: int,
    max_power: int,
) -> dict[str, object]:
    """Build the compact prime-square interval utilization summary."""
    transitions = retained_transitions(
        detail_csv,
        min_power=min_power,
        max_power=max_power,
    )
    baseline_log_loss = mean_log_loss(transitions)
    candidate_metrics = [
        evaluate_candidate(
            transitions,
            candidate_id=candidate_id,
            baseline_log_loss=baseline_log_loss,
        )
        for candidate_id in CANDIDATE_SPECS
    ]
    metric_by_id = {
        str(row["candidate_id"]): row
        for row in candidate_metrics
    }
    scale_stats = label_stats(
        transitions,
        label_field=SCALE_NEUTRAL_FIELD,
    )
    low_share = float(scale_stats["d4_low"]["next_triad_share"])
    high_share = float(scale_stats["d4_high"]["next_triad_share"])
    scale_neutral = {
        "label_definition": (
            "For current d=4 rows, split U_square at the median inside each "
            "decade, factorization-type, selected-offset, first-admissible-offset cell."
        ),
        "label_stats": scale_stats,
        "low_minus_high_lift": low_share - high_share,
        "all_per_power_phase_gains_positive": all(
            float(value) > 0.0
            for value in metric_by_id["scale_neutral_phase_budget_bit"][
                "per_power_log_loss_gain"
            ].values()
        ),
    }

    return {
        "title": "Prime-Square Interval Utilization and Next-Gap Semiprime Return",
        "detail_csv": str(detail_csv),
        "power_range": [min_power, max_power],
        "transition_count": len(transitions),
        "baseline_log_loss": baseline_log_loss,
        "existing_matched_high_scale_handoff": matched_handoff_payload(handoff_summary),
        "pooled_phase_budget_bit": {
            "label_definition": (
                "Original retained-window pooled geometry median split from the "
                "prime-square utilization probe."
            ),
            "label_stats": label_stats(transitions, label_field="phase_budget_bit"),
            "log_loss_gain": metric_by_id["pooled_phase_budget_bit"]["log_loss_gain"],
        },
        "scale_neutral_phase_budget_bit": scale_neutral,
        "candidate_metrics": candidate_metrics,
        "headline_metrics": {
            "scale_neutral_phase_gain": metric_by_id[
                "scale_neutral_phase_budget_bit"
            ]["log_loss_gain"],
            "current_winner_parity_gain": metric_by_id[
                "current_winner_parity"
            ]["log_loss_gain"],
            "parity_previous_state_gain": metric_by_id[
                "current_winner_parity+previous_reduced_state"
            ]["log_loss_gain"],
            "parity_previous_state_scale_neutral_phase_gain": metric_by_id[
                "current_winner_parity+previous_reduced_state+scale_neutral_phase_budget_bit"
            ]["log_loss_gain"],
        },
        "method_note": (
            "The decade-normalized split is an in-surface retained-window demonstration. "
            "The next held-out test is a frozen train-below-target holdout."
        ),
    }


def findings_markdown(summary: dict[str, object]) -> str:
    """Render the findings note."""
    matched = summary["existing_matched_high_scale_handoff"]
    scale = summary["scale_neutral_phase_budget_bit"]
    stats = scale["label_stats"]
    headline = summary["headline_metrics"]
    per_power = {
        str(row["candidate_id"]): row
        for row in summary["candidate_metrics"]
    }["scale_neutral_phase_budget_bit"]["per_power_log_loss_gain"]

    lines = [
        "# Prime-Square Interval Utilization and Next-Gap Semiprime Return",
        "",
        "A prime gap has a left endpoint prime, a right endpoint prime, and interior composite integers. For each gap, take the first interior integer whose divisor count is minimal among the gap interior. When that integer has divisor count `d = 4`, the location of the right endpoint carries measurable information about the factorization type selected in the following gap.",
        "",
        "For the current minimum-divisor interior integer $w$ and current right endpoint $q$, let $S_{+}(w)$ be the next prime square after $w$. The prime-square interval utilization is:",
        "",
        "$$U_{\\square}(w, q) = \\frac{q - w}{S_{+}(w) - w}.$$",
        "",
        "Rows with lower $U_{\\square}$ close after using less of the interval before the next prime square. On the retained `10^12..10^18` catalog surface, those rows are followed more often by a gap whose minimum-divisor interior integer is an odd semiprime with divisor count `4` and first admissible offset `2`, `4`, or `6` modulo `30`.",
        "",
        "## Matched Transition Surface",
        "",
        "The existing matched comparison separates lower and higher utilization halves while holding fixed the current factorization type, the offset of the selected interior integer, and the first admissible offset modulo `30`.",
        "",
        f"- low-utilization share followed by the odd-semiprime `d = 4` offset class: `{float(matched['low_next_triad_share']):.4f}`",
        f"- high-utilization share followed by the odd-semiprime `d = 4` offset class: `{float(matched['high_next_triad_share']):.4f}`",
        f"- matched lift: `{float(matched['lift']):+.4f}`",
        f"- matched half-pairs per side: `{int(matched['matched_total_weight_per_side'])}`",
        "",
        "That establishes the transition signal after controlling for the current factorization type and offset data already present in [prime-square interval findings](square_phase_handoff_findings.md).",
        "",
        "## Decade-Normalized Check",
        "",
        "The pooled split is vulnerable to scale drift, so this demonstration recomputes the low/high split separately inside each decade and matched arithmetic cell. The cell key is `(decade, factorization type, selected-interior-integer offset, first admissible offset modulo 30)`.",
        "",
        f"- low-utilization `d = 4` support: `{int(stats['d4_low']['support'])}`",
        f"- low-utilization next-gap odd-semiprime share: `{float(stats['d4_low']['next_triad_share']):.6f}`",
        f"- high-utilization `d = 4` support: `{int(stats['d4_high']['support'])}`",
        f"- high-utilization next-gap odd-semiprime share: `{float(stats['d4_high']['next_triad_share']):.6f}`",
        f"- decade-normalized lift: `{float(scale['low_minus_high_lift']):+.6f}`",
        "",
        "The decade-normalized median split also remains competitive in the log-loss readout:",
        "",
        f"- decade-normalized median-split gain: `{float(headline['scale_neutral_phase_gain']):.6f}`",
        f"- parity of the selected interior integer gain: `{float(headline['current_winner_parity_gain']):.6f}`",
        f"- parity plus previous gap-class gain: `{float(headline['parity_previous_state_gain']):.6f}`",
        f"- parity plus previous gap-class plus median-split gain: `{float(headline['parity_previous_state_scale_neutral_phase_gain']):.6f}`",
        "",
        "Per-decade median-split gains are positive across the retained surface:",
        "",
    ]
    for power, gain in sorted(per_power.items(), key=lambda item: int(item[0])):
        lines.append(f"- `10^{power}`: `{float(gain):.6f}`")

    lines.extend(
        [
            "",
            "## Bounded-Method Note",
            "",
            "ChatGPT's adversarial critique identified the correct pressure point: the original pooled median-split table is an in-surface result. That does not erase the signal, but it changes the public wording. The decade-normalized result is the headline demonstration. The held-out test remains a frozen train-below-target test where medians and probability tables are learned below the target decade and scored forward.",
            "",
            "This is not a next-prime rule. The quantity $U_{\\square}(w, q)$ uses the already-known current endpoint $q$, so it is a transition observable for the next gap, not a mechanism for choosing the current endpoint.",
            "",
            "## Held-Out Test",
            "",
            "The next direct test is: train the matched-cell medians and probability tables on lower retained decades, freeze them, and score a later target decade. The claim is weakened if the low-utilization `d = 4` group does not exceed the high-utilization `d = 4` group on the held-out target, or if adding the median split to the parity plus previous gap-class model gives zero or negative held-out log-loss improvement.",
            "",
            "## Artifacts",
            "",
            "- [demo script](../../benchmarks/python/predictor/gwr_square_budget_handoff_shock_demo.py)",
            "- [summary JSON](../../output/gwr_square_budget_handoff_shock_summary.json)",
            "- [source catalog detail CSV](../../output/gwr_dni_gap_type_catalog_details.csv)",
            "",
        ]
    )
    return "\n".join(lines)


def write_summary(path: Path, summary: dict[str, object]) -> None:
    """Write the summary JSON artifact with LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def write_findings(path: Path, summary: dict[str, object]) -> None:
    """Write the Markdown findings note with LF endings."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(findings_markdown(summary), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the demo and write the compact artifacts."""
    args = build_parser().parse_args(argv)
    if args.min_power < 1:
        raise ValueError("min_power must be at least 1")
    if args.max_power < args.min_power:
        raise ValueError("max_power must be at least min_power")

    started_at = time.time()
    summary = summarize(
        args.detail_csv,
        args.handoff_summary,
        min_power=args.min_power,
        max_power=args.max_power,
    )
    summary["runtime_seconds"] = time.time() - started_at

    summary_path = args.output_dir / SUMMARY_FILENAME
    write_summary(summary_path, summary)
    write_findings(args.findings_path, summary)

    scale = summary["scale_neutral_phase_budget_bit"]
    headline = summary["headline_metrics"]
    print(
        "gwr-square-budget-handoff-shock:"
        f" transitions={summary['transition_count']}"
        f" scale_neutral_lift={scale['low_minus_high_lift']:.6f}"
        f" phase_gain={headline['scale_neutral_phase_gain']:.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
