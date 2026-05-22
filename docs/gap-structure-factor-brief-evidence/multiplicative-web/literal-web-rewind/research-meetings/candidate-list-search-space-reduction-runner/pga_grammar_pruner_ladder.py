#!/usr/bin/env python3
"""
PGA Grammar Pruner Scaling Ladder

Measures how much of the 198-word factor-neighborhood hypothesis space the
current public grammar rules remove at increasing bit lengths.

Modes:
- synthetic: deterministic motif sequence from the frozen observed motif mix.
- real: deterministic public semiprime sequence, live public motif derivation, explicit
  unresolved rows on derivation failure.

No hidden randomness, no synthetic substitution in real mode, and no private
factor information.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import gmpy2

from pga_grammar_pruner import REFERENCE_FACTOR_SPACE, prune_factor_space

try:
    from public_motif_derivation import derive_public_motif
except Exception as exc:
    derive_public_motif = None  # type: ignore[assignment]
    DERIVATION_IMPORT_ERROR = exc
else:
    DERIVATION_IMPORT_ERROR = None


DEFAULT_BIT_LENGTHS = [24, 28, 32, 36, 40, 44, 48]
DEFAULT_SAMPLES_PER_LEVEL = 30

SYNTHETIC_MOTIF_COUNTS: tuple[tuple[str, int], ...] = (
    ("o2_d4_a2_d4_odd@mid", 55),
    ("o2_d4_a2_d4_odd@early", 12),
    ("o4_d4_a4_d4_odd@mid", 18),
    ("o6_d4_a6_d4_odd@mid", 8),
    ("o2_d4_a2_d4_odd@mid + o4_d4_odd prev", 4),
    ("o4_d4_a4_d4_odd@mid + o2_d4_odd prev", 3),
)

SYNTHETIC_MOTIF_SEQUENCE: tuple[str, ...] = tuple(
    motif for motif, count in SYNTHETIC_MOTIF_COUNTS for _ in range(count)
)


def synthetic_motif(bits: int, sample_index: int) -> str:
    """Return a deterministic motif from the frozen observed mix."""
    offset = (bits * 17) % len(SYNTHETIC_MOTIF_SEQUENCE)
    return SYNTHETIC_MOTIF_SEQUENCE[(offset + sample_index) % len(SYNTHETIC_MOTIF_SEQUENCE)]


def deterministic_public_semiprime_n(bits: int, sample_index: int) -> int:
    """
    Return a deterministic public semiprime N = p * q at the requested bit length.

    p and q are constructed deterministically from (bits, sample_index) and
    are guaranteed primes (via gmpy2.next_prime). They are used only to
    build the public corpus fixture. The runner discards them immediately
    after computing N. The measured path is strictly:
        N -> derive_public_motif(N) -> prune_factor_space(motif)
    """
    if bits < 4:
        raise ValueError("bit length must be at least 4")
    half = max(2, (bits + 1) // 2)
    # Deterministic, well-separated starting points for p and q
    base_p = (1 << (half - 1)) + (sample_index * 2) + 1
    base_q = base_p + (1 << (half // 2)) + 2

    p = gmpy2.next_prime(base_p)
    q = gmpy2.next_prime(base_q)

    # Ensure they land in the target bit-length range
    while p.bit_length() < half:
        p = gmpy2.next_prime(p + 2)
    while q.bit_length() < half:
        q = gmpy2.next_prime(q + 2)

    return int(p * q)



def real_motif(bits: int, sample_index: int) -> tuple[str, int, str | None]:
    """Derive a motif from a deterministic public semiprime, or return explicit unresolved."""
    n_value = deterministic_public_semiprime_n(bits, sample_index)
    if derive_public_motif is None:
        return (
            f"UNRESOLVED:{n_value}",
            n_value,
            f"public_motif_derivation import failed: {DERIVATION_IMPORT_ERROR}",
        )
    try:
        motif = derive_public_motif(n_value)
    except Exception as exc:
        return f"UNRESOLVED:{n_value}", n_value, f"{type(exc).__name__}: {exc}"
    if motif.startswith("UNRESOLVED:"):
        return motif, n_value, "public motif derivation returned unresolved"
    return motif, n_value, None


def motif_for_sample(mode: str, bits: int, sample_index: int) -> tuple[str, int | None, str | None]:
    if mode == "synthetic":
        return synthetic_motif(bits, sample_index), None, None
    if mode == "real":
        return real_motif(bits, sample_index)
    raise ValueError(f"unknown mode: {mode}")


def run_ladder(bit_lengths: list[int], samples_per_level: int, mode: str) -> dict[str, Any]:
    results: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": mode,
        "reference_space": REFERENCE_FACTOR_SPACE,
        "samples_per_level": samples_per_level,
        "levels": {},
    }

    for bits in bit_lengths:
        reductions: list[float] = []
        rule_usage: Counter[str] = Counter()
        unresolved_count = 0
        unresolved_examples: list[dict[str, Any]] = []
        motif_usage: Counter[str] = Counter()

        per_case: list[dict[str, Any]] = []

        for sample_index in range(samples_per_level):
            motif, n_value, error = motif_for_sample(mode, bits, sample_index)
            res = prune_factor_space(motif)
            motif_usage[motif] += 1

            case_record = {
                "case_id": f"semiprime_{bits}_{sample_index}",
                "target_bits": bits,
                "N": n_value,
                "motif": motif,
                "rules_fired": res.get("rules_fired", []),
                "pruned": res.get("pruned", 0),
                "remaining": res.get("remaining", REFERENCE_FACTOR_SPACE),
                "reduction_percent": round(float(res.get("reduction_percent", 0.0)), 2),
                "status": "unresolved" if res.get("status") == "unresolved" else "resolved",
                "derivation_error": error,
            }
            per_case.append(case_record)

            if res.get("status") == "unresolved":
                unresolved_count += 1
                reductions.append(0.0)
                if len(unresolved_examples) < 5:
                    unresolved_examples.append(
                        {
                            "sample_index": sample_index,
                            "N": n_value,
                            "motif": motif,
                            "error": error or res.get("reason", "unresolved"),
                        }
                    )
                continue

            reductions.append(float(res["reduction_percent"]))
            for rid in res["rules_fired"]:
                rule_usage[str(rid)] += 1

        avg = sum(reductions) / len(reductions) if reductions else 0.0
        std = (
            (sum((r - avg) ** 2 for r in reductions) / len(reductions)) ** 0.5
            if len(reductions) > 1
            else 0.0
        )

        level_data = {
            "bit_length": bits,
            "samples": samples_per_level,
            "average_reduction_percent": round(avg, 2),
            "std_dev": round(std, 2),
            "min_reduction": round(min(reductions), 2) if reductions else 0.0,
            "max_reduction": round(max(reductions), 2) if reductions else 0.0,
            "unresolved_count": unresolved_count,
            "unresolved_examples": unresolved_examples,
            "top_motifs": motif_usage.most_common(8),
            "top_rules": rule_usage.most_common(8),
            "reduction_distribution": {
                "0-20%": sum(1 for r in reductions if r < 20),
                "20-40%": sum(1 for r in reductions if 20 <= r < 40),
                "40-60%": sum(1 for r in reductions if 40 <= r < 60),
                "60-80%": sum(1 for r in reductions if 60 <= r < 80),
                "80%+": sum(1 for r in reductions if r >= 80),
            },
        }

        if mode == "real":
            level_data["per_case"] = per_case

        results["levels"][str(bits)] = level_data

    return results


def write_reports(results: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ladder_summary.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    mode = results["mode"]
    md_lines = [
        "# PGA Grammar Pruner Scaling Ladder",
        "",
        f"**Date**: {results['timestamp']}",
        f"**Mode**: `{mode}`",
        f"**Reference factor space**: {results['reference_space']} words",
        f"**Samples per level**: {results['samples_per_level']}",
        "",
        "## Results by Bit Length",
        "",
        "| Bits | Avg Reduction | Std Dev | Min | Max | Unresolved |",
        "|------|---------------|---------|-----|-----|------------|",
    ]

    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        md_lines.append(
            f"| {bits} | {data['average_reduction_percent']:.2f}% | "
            f"{data['std_dev']:.2f}% | {data['min_reduction']:.1f}% | "
            f"{data['max_reduction']:.1f}% | {data['unresolved_count']} |"
        )

    md_lines += ["", "## Mode Contract", ""]
    if mode == "synthetic":
        md_lines += [
            "Synthetic mode uses a fixed motif sequence derived from the frozen observed motif mix.",
            "It is deterministic and does not call live public motif derivation.",
        ]
    else:
        md_lines += [
            "Real mode derives motifs from deterministic public semiprimes.",
            "Derivation failures are recorded as unresolved rows. No synthetic motif is substituted.",
        ]

    # Add per-level top motifs table (makes motif-mix sensitivity explicit)
    md_lines += ["", "## Top Motifs per Level", ""]

    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        md_lines.append(f"**{bits} bits**")
        if data.get("top_motifs"):
            for motif, count in data["top_motifs"]:
                md_lines.append(f"- `{motif}`: {count}")
        else:
            md_lines.append("- (no motif data)")
        md_lines.append("")

    # Per-case detail for real mode (small probes)
    if mode == "real":
        md_lines += ["", "## Per-Case Results (Real Derivation)", ""]
        for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
            per_case = data.get("per_case", [])
            if not per_case:
                continue
            md_lines.append(f"### {bits} bits")
            md_lines.append("")
            md_lines.append("| case_id | N | motif | rules | pruned | remaining | % | status | error |")
            md_lines.append("|---------|---|-------|-------|--------|-----------|---|--------|-------|")
            for case in per_case:
                rules_str = ",".join(case.get("rules_fired", [])) or "-"
                error = case.get("derivation_error") or "-"
                md_lines.append(
                    f"| {case['case_id']} | {case['N']} | `{case['motif']}` | {rules_str} | "
                    f"{case['pruned']} | {case['remaining']} | {case['reduction_percent']:.2f}% | "
                    f"{case['status']} | {error} |"
                )
            md_lines.append("")

    md_lines += [
        "## Interpretation",
        "",
        "This ladder measures grammar-rule reduction after a public motif is available.",
        "Synthetic mode measures rule-set shape under a fixed motif mix. Real mode measures",
        "the live raw-N public derivation path plus rule coverage.",
    ]

    (out_dir / "ladder_summary.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"Ladder results written to: {out_dir}")


def parse_levels(levels: str) -> list[int]:
    parsed = [int(x.strip()) for x in levels.split(",") if x.strip()]
    if not parsed:
        raise ValueError("at least one bit length is required")
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description="PGA Grammar Pruner Scaling Ladder")
    parser.add_argument(
        "--levels",
        type=str,
        default=",".join(map(str, DEFAULT_BIT_LENGTHS)),
        help="Comma-separated bit lengths, for example 32,40,48",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=DEFAULT_SAMPLES_PER_LEVEL,
        help="Number of deterministic samples per bit length",
    )
    parser.add_argument(
        "--mode",
        choices=("synthetic", "real"),
        default="synthetic",
        help="synthetic uses fixed motifs; real derives motifs from deterministic public semiprimes",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="Explicit output directory. If omitted, a mode-derived path is used (e.g. output/ladder/synthetic_48_80_samples_30/).",
    )
    args = parser.parse_args()

    bit_lengths = parse_levels(args.levels)

    print("=== PGA Grammar Pruner Scaling Ladder ===")
    print(f"Mode: {args.mode}")
    print(f"Bit lengths: {bit_lengths}")
    print(f"Samples per level: {args.samples}")
    print()

    results = run_ladder(bit_lengths, args.samples, mode=args.mode)

    if args.out_dir:
        out_dir = Path(args.out_dir)
    else:
        min_b = min(bit_lengths)
        max_b = max(bit_lengths)
        prefix = "real_semiprime" if args.mode == "real" else args.mode
        out_dir = (
            Path(__file__).resolve().parent
            / "output"
            / "ladder"
            / f"{prefix}_{min_b}_{max_b}_samples_{args.samples}"
        )

    write_reports(results, out_dir)

    print("\n=== Ladder Summary ===")
    for bits, data in sorted(results["levels"].items(), key=lambda x: int(x[0])):
        print(
            f"{bits:>3} bits : {data['average_reduction_percent']:6.2f}% avg "
            f"(+/-{data['std_dev']:.1f}%) "
            f"[{data['min_reduction']:.0f}% to {data['max_reduction']:.0f}%] "
            f"unresolved={data['unresolved_count']}"
        )

    print(f"\nDetailed reports: {out_dir / 'ladder_summary.md'}")


if __name__ == "__main__":
    main()
