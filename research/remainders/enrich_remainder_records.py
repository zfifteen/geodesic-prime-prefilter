"""Lightweight feature engineering / schema enrichment for remainder records.

This is the Phase 1 data-preparation step of the Remainder-Gap-Prime Placement
Correlation Analysis Plan.

It reads line-delimited JSON records produced by collect_remainder_stats.py
(which already contain distance_to_next_prime and is_current_min_d) and
emits an enriched version with:

- termination_distance (alias for distance_to_next_prime for plan schema)
- is_gwr_winner (alias for is_current_min_d, named explicitly "computed once
  per gap" semantics even if already marked per-record)
- Derived remainder scalars:
  * num_zeros_in_vector
  * residue_sum_parity (sum(R) % 2)
  * dist_nearest_zero_mod30 (min dist of any slot's residue to 0 mod the modulus)
  * dist_nearest_zero_mod210
  * coprime_to_210 (True if the first four residues (mod 2,3,5,7) are all nonzero)
  * (optional future) other minimal scalars

The output remains line-delimited JSON for streaming compatibility.

All work is post-collection measurement. No change to collector core or to
PGS inference paths. Enrichment is deterministic given the input vector.

This file follows the 4-phase authoring procedure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# The parent remainder_utils is pure and already validated.
# We import only for the default moduli knowledge if needed for derived.
try:
    # Relative import friendly when run as module or script
    from remainder_utils import MODULI_PRIMORIAL_V1  # type: ignore
except Exception:
    MODULI_PRIMORIAL_V1 = [2, 3, 5, 7, 30, 210, 2310]


def compute_derived_remainder_scalars(
    remainder_vector: tuple[int, ...] | list[int],
    moduli: list[int] | None = None,
) -> dict[str, Any]:
    """Return a dict of derived scalar features from one remainder vector.

    Phase-1 scaffold: signature + detailed comments describing exact logic.
    No arithmetic is performed in the body yet.

    Intended logic (to be implemented in Phase 3):
    1. If moduli is None use MODULI_PRIMORIAL_V1 (or first len(remainder_vector) slots).
    2. num_zeros = count of r == 0 for r in vector.
    3. parity = sum(vector) % 2
    4. For mod 30 and 210: find the positions in moduli that match, then
       for the corresponding residues compute min(r, m-r) or simply the
       residue value itself if "distance to nearest forbidden" means dist to 0
       (i.e. the residue when aligned to 0 class). Plan uses "distance to nearest
       forbidden class", here we take the actual r for the 30 and 210 slots
       (r is already the distance to 0 mod that m).
    5. coprime_to_210: look at first 4 entries (corresponding to 2,3,5,7) :
       all(r != 0 for those).
    6. Return dict with stable key names.

    The function must be pure, handle short vectors gracefully (for custom moduli),
    and never mutate inputs.
    """
    if moduli is None:
        moduli = list(MODULI_PRIMORIAL_V1)
    # Truncate or pad awareness: use only as many as we have in vector
    m = moduli[: len(remainder_vector)]

    vec = [int(x) for x in remainder_vector]
    num_zeros = sum(1 for r in vec if r == 0)
    res_sum = sum(vec)
    parity = res_sum % 2

    # dist to 0 mod m is exactly the remainder value itself for that slot
    def _get_dist_for_mod(target: int) -> int | None:
        try:
            idx = m.index(target)
            return vec[idx]
        except ValueError:
            return None

    dist30 = _get_dist_for_mod(30)
    dist210 = _get_dist_for_mod(210)

    coprime_to_210 = False
    if len(vec) >= 4:
        coprime_to_210 = all(r != 0 for r in vec[:4])

    return {
        "num_zeros_in_vector": num_zeros,
        "residue_sum_parity": parity,
        "dist_nearest_zero_mod30": dist30,
        "dist_nearest_zero_mod210": dist210,
        "coprime_to_210": coprime_to_210,
    }


def enrich_record(record: dict[str, Any]) -> dict[str, Any]:
    """Add the plan-mandated fields to one record (non-mutating).

    Adds:
      termination_distance = record.get("distance_to_next_prime")
      is_gwr_winner = record.get("is_current_min_d")
      plus the derived scalars under key "derived_remainder" or flat keys
      (decide flat for streaming ease; document choice).

    Phase-1 scaffold: full signature and control-flow comments.
    """
    out: dict[str, Any] = dict(record)  # shallow; vectors and ints are immutable or copied by value on use
    out["termination_distance"] = record.get("distance_to_next_prime")
    out["is_gwr_winner"] = record.get("is_current_min_d")

    vec = record.get("remainder_vector", ())
    derived = compute_derived_remainder_scalars(vec)
    # flat merge for easy streaming / pandas later; prefix to avoid collision
    for k, v in derived.items():
        out[k] = v
    return out


def enrich_jsonl_stream(
    input_path: Path | str,
    output_path: Path | str,
) -> dict[str, int]:
    """Stream read raw records, enrich each, write new JSONL.

    Returns counts for logging. Designed for large files (no full load).

    Phase-1: comments describe streaming loop, error handling for bad lines,
    preservation of all original fields + new ones.
    """
    in_path = Path(input_path)
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count_in = count_out = 0
    with in_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            count_in += 1
            try:
                rec = json.loads(line)
                enriched = enrich_record(rec)
                json.dump(enriched, fout, separators=(",", ":"))
                fout.write("\n")
                count_out += 1
            except Exception as exc:
                # Keep going; log bad line count in real use
                print(f"Warning: skipping bad record {count_in}: {exc}", file=sys.stderr)
    return {"records_in": count_in, "records_out": count_out}


def main(argv: list[str] | None = None) -> int:
    """CLI for the enrich step.

    Example:
      python research/remainders/enrich_remainder_records.py \
        --input research/remainders/output/tiny_val/raw_records.jsonl \
        --output research/remainders/correlations/enriched/tiny_enriched.jsonl

    Phase-1 scaffold only.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Enrich collector JSONL with termination + derived remainder scalars.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)

    counts = enrich_jsonl_stream(args.input, args.output)
    print("Enrichment complete:", counts)
    print("Output:", args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
