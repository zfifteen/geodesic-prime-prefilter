"""Collector for remainder statistics inside prime gaps.

Per the Remainder Statistics Collection Plan (Phase 2).

This script walks successive prime gaps using the project's existing
exact divisor-count routines (reuse, no duplication of d(n) logic),
attaches remainder vectors (via the pure remainder_utils), and emits
one JSON record per interior composite.

Usage examples (after tiny validation):
  python research/remainders/collect_remainder_stats.py \
      --max-p 2000 --output-dir research/remainders/output/tiny/

  python research/remainders/collect_remainder_stats.py \
      --max-p 1000000 --moduli 2,3,5,7,30,210,2310 \
      --output-dir research/remainders/output/1e6/ --sample-rate 0.1

Contract:
- Left endpoints p are successive primes obtained from the divisor-field
  walk (gwr_next_gap_profile). No external prime list or nextprime().
- For every interior n = p+k (1 <= k < g), emit a minimal record.
- Raw output is append-only line-delimited JSON (one object per line)
  for streaming reproducibility.
- Aggregates (histograms, simple corrs) produced in same or follow-on pass.
- All runs logged exactly in RUN_LOG.md beside the dataset.
- 100-gap test set must execute cleanly (exact shape, hand-checkable
  records) before any larger bound.

PGS framing reminder:
Start from ordered gap state + divisor-count field + GWR winner location.
Remainder vectors are additional attributes collected for measurement.
The script never uses residues to select the next prime q or the GWR winner.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- Path setup for research script (standard in repo) ---
# When run as research/remainders/collect_....py :
# parents[0]=remainders, [1]=research, [2]=repo root
ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

# Local pure module (same dir)
if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from remainder_utils import MODULI_PRIMORIAL_V1, compute_residues  # noqa: E402

# Reuse of current gap / d(n) machinery (Phase 2 Step 2)
from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.gwr_boundary_walk import (  # noqa: E402
    DEFAULT_SCAN_BLOCK,
    gwr_next_gap_profile,
)


def parse_moduli(spec: str | None) -> list[int]:
    """Parse --moduli comma-separated string into list of ints.

    Falls back to the versioned default when spec is None or empty.
    """
    if not spec:
        return list(MODULI_PRIMORIAL_V1)
    try:
        vals = [int(x.strip()) for x in spec.split(",") if x.strip()]
        if not vals:
            raise ValueError("no moduli after parsing")
        return vals
    except Exception as exc:
        raise argparse.ArgumentTypeError(
            f"invalid --moduli value {spec!r}: {exc}"
        ) from exc


def build_records_for_gap(
    p: int,
    moduli: list[int],
    sample_rate: float = 1.0,
) -> list[dict[str, Any]]:
    """Return list of interior remainder records for the gap after prime p.

    Reuses:
      - gwr_next_gap_profile(p) to obtain q, gap size, and the GWR winner
        (leftmost minimum-d(n) carrier) without reimplementing min tracking.
      - divisor_counts_segment to obtain exact d(n) for every interior point.

    For each interior n = p + k:
      - k (relative offset)
      - d = d(n)
      - is_current_min_d : True exactly at the GWR winner offset
      - distance_to_next_prime = q - n
      - remainder_vector

    The is_current_min_d flag is set using the winner_offset returned by
    the GWR profile (leftmost by construction of the rule).

    sample_rate (0 < rate <= 1.0) allows probabilistic subsampling of
    interior records for very large bounds. 1.0 = all records.

    Detailed logic (scaffolded description):
    1. Validate p is treated as prime by the field (d(p)==2) via profile call.
    2. Obtain profile; extract q and winner_offset.
    3. If gap has no interior (q == p+1), return [] .
    4. Fetch exact counts for [p+1 .. q-1].
    5. For each offset 0..len(counts)-1:
         k = offset + 1
         d = int(counts[offset])
         is_winner = (k == winner_offset)
         dist = q - (p + k)
         if random() < sample_rate (or always when rate==1):
             rem = compute_residues(p + k, moduli)
             record = {
                 "p": p,
                 "q": q,
                 "g": q - p,
                 "k": k,
                 "n": p + k,
                 "d": d,
                 "is_current_min_d": bool(is_winner),
                 "distance_to_next_prime": dist,
                 "remainder_vector": rem,
                 "moduli_version": "M_v1",   # or derive from actual list
             }
             append
    6. Return the list (or generator in later refinement).
    """
    if sample_rate <= 0 or sample_rate > 1.0:
        raise ValueError(f"sample_rate must be in (0, 1.0], got {sample_rate}")

    # Reuse the GWR profile to obtain the right endpoint q and the exact
    # leftmost minimum-d(n) offset (winner) for this gap.
    profile = gwr_next_gap_profile(p)
    q: int = int(profile["next_prime"])
    winner_offset: int | None = profile.get("winner_offset")  # None for twin gaps

    if q <= p + 1:
        # Twin prime gap or degenerate: no interior composites.
        return []

    # Reuse the project's segmented exact divisor count for the full interior.
    # This guarantees identical d(n) values used by GWR walk and generator.
    counts = divisor_counts_segment(p + 1, q)

    # Optional import only when sampling < 1 (kept out of hot path for rate=1)
    import random

    records: list[dict[str, Any]] = []
    for offset, raw_d in enumerate(counts):
        k = offset + 1
        n = p + k
        d = int(raw_d)
        is_current_min_d = (winner_offset is not None and k == winner_offset)
        dist = q - n

        if sample_rate < 1.0:
            if random.random() >= sample_rate:
                continue

        rem_vec = compute_residues(n, moduli)
        rec: dict[str, Any] = {
            "p": p,
            "q": q,
            "g": q - p,
            "k": k,
            "n": n,
            "d": d,
            "is_current_min_d": bool(is_current_min_d),
            "distance_to_next_prime": dist,
            "remainder_vector": rem_vec,
            "moduli_version": "M_v1",
        }
        records.append(rec)

    return records


def collect_gaps(
    max_p: int,
    moduli: list[int],
    output_path: Path,
    sample_rate: float = 1.0,
) -> dict[str, Any]:
    """Drive the gap walk from p=2, emit records for all p <= max_p.

    Writes raw line-delimited JSON records to output_path (append mode
    recommended for safety, or truncate at start).

    Returns summary dict with counts for logging.

    High-level flow (scaffolded):
    - open output file for writing (jsonl)
    - p = 2
    - gaps_processed = 0
    - records_emitted = 0
    - while p <= max_p:
        records = build_records_for_gap(p, moduli, sample_rate)
        for rec in records:
            json.dump(rec, f); f.write("\n")
            records_emitted += 1
        # advance
        profile = gwr_next_gap_profile(p)
        p = profile["next_prime"]
        gaps_processed += 1
        (optional progress)
    - flush, close
    - return {"gaps": gaps_processed, "records": records_emitted, ...}
    """
    raise NotImplementedError(
        "collector scaffold: collect_gaps not implemented yet"
    )


def compute_basic_aggregates(
    records: list[dict[str, Any]] | None = None,
    jsonl_path: Path | None = None,
) -> dict[str, Any]:
    """Produce marginal frequency tables and simple correlation sketches.

    Either in-memory records or streamed from jsonl_path.

    Initial aggregates (plan Phase 2 step 4):
    - Per-modulus residue counts (overall + conditioned on is_current_min_d)
    - Simple counts vs gap-size bins or normalized position bins
    - Placeholder for mutual-info / chi2 ready numbers

    Returns nested dict suitable for JSON summary.
    """
    # Scaffold only.
    raise NotImplementedError(
        "collector scaffold: compute_basic_aggregates not implemented yet"
    )


def write_run_log(
    log_path: Path,
    command_line: str,
    params: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    """Append a reproducible run record to RUN_LOG.md .

    Records exact command, python version, date, moduli used,
    machine hint, summary counts.
    """
    # Scaffold.
    raise NotImplementedError("collector scaffold: write_run_log not yet")


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Parses args per plan:
      --max-p (int, required for first)
      --moduli (str)
      --output-dir (dir, will contain raw_records.jsonl + summary + RUN_LOG)
      --sample-rate (float 0< <=1 default 1.0)

    Steps performed by main (scaffolded description):
    1. Parse + validate.
    2. Ensure output dir exists.
    3. Resolve moduli (versioned tag).
    4. Define raw file = output_dir / "raw_records.jsonl"
    5. Call collect_gaps(...)
    6. Optionally run compute_basic_aggregates on small sets or stream.
    7. Write RUN_LOG.md with full details.
    8. Print summary to stdout.
    """
    parser = argparse.ArgumentParser(
        description="Collect remainder statistics inside prime gaps (PGS measurement layer)."
    )
    parser.add_argument(
        "--max-p",
        type=int,
        required=True,
        help="Upper bound on left-endpoint prime p (inclusive). Gaps after p<=max-p are processed.",
    )
    parser.add_argument(
        "--moduli",
        type=str,
        default=None,
        help="Comma-separated moduli (default: 2,3,5,7,30,210,2310 = M_v1)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/remainders/output"),
        help="Directory for raw_records.jsonl, aggregates, and RUN_LOG.md",
    )
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=1.0,
        help="Fraction of interior records to emit (for large bounds). 1.0 = all.",
    )
    args = parser.parse_args(argv)

    # Scaffold body: validation, setup, delegation described in comments.
    # Implementation added one piece at a time with tests.
    print("collector scaffold: main not fully implemented; see comments.")
    print(f"Parsed: max_p={args.max_p}, moduli_spec={args.moduli}, out={args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
