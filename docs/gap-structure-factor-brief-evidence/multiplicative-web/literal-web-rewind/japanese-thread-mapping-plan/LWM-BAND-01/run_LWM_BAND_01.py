#!/usr/bin/env python3
"""
LWM-BAND-01 (Banded Diagonal Support) — Primary experiment runner.

Isolated implementation under the literal multiplicative web / thread triangulation contract.
PGS-first: operates exclusively on the public ordered thread web (small-prime factors r
observed at public composites around N). Direct p/q rows held out before any support or
coherence scoring. Nomination uses only public thread data.

Band partition B and coherence C are pure deterministic functions of public r values only.
No GWR/DNI used in this first implementation (reserved for follow-on per plan).
No classical methods (no gcd, no isprime, no trial on N, no candidate generation, no ranking
by divisibility) participate in thread selection, band assignment, or offset nomination.

Baseline flat logic copied from literal_web_hole_trace.py (sqrt-radius public window).
Extended with:
  - band_for_r(r): public B
  - per-offset band support vectors S(t)
  - coherence C(t)
  - dual emission: flat max-support holes + banded max-C holes
  - rank comparison for true direct offsets under both sort orders
  - full public artifacts + manifest before/after comparison data

See japanese-thread-mapping-plan/index.html sections 5.1-5.5 for exact spec.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "LWM_BAND_01"
OUT.mkdir(parents=True, exist_ok=True)

# === Toy cases (identical to baseline literal_web_hole_trace.py) ===
TOY_CASES = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
]

# === First ladder rungs (using 6*p radius per ladder convention for scale) ===
# These are the "first two ladder rungs" referenced in task.
# Window uses explicit radius when provided; otherwise falls back to public sqrt rule.
LADDER_RUNGS = [
    {"name": "ladder_101x137", "p": 101, "q": 137, "radius": 6 * 101},
    {"name": "ladder_131x167", "p": 131, "q": 167, "radius": 6 * 131},
]

ALL_CASES = TOY_CASES + LADDER_RUNGS

WINDOW_SQRT_RATIO = (1, 1)


def public_radius(n: int) -> int:
    """Baseline public window radius = floor(sqrt(N))."""
    numerator, denominator = WINDOW_SQRT_RATIO
    return (math.isqrt(n) * numerator) // denominator


def factor_label(factors: dict[int, int]) -> str:
    return " * ".join(
        str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
    )


def rows_around(n: int, radius: int) -> list[dict[str, Any]]:
    """Public web construction: factor all composites in [N-r, N+r] except N itself."""
    rows = []
    for value in range(n - radius, n + radius + 1):
        if value < 4 or value == n:
            continue
        factors = {int(k): int(v) for k, v in factorint(value).items()}
        if factors == {value: 1}:
            continue
        divisor_count = math.prod(e + 1 for e in factors.values())
        rows.append({
            "value": value,
            "offset": value - n,
            "factors": factors,
            "factorization": factor_label(factors),
            "divisor_count": divisor_count,
        })
    return rows


def thread_slots(n: int, radius: int, r: int) -> list[int]:
    """All offsets t in window where (N + t) ≡ 0 mod r, t != 0."""
    start = -radius
    residue = (-n) % r
    first = start + ((residue - start) % r)
    return [t for t in range(first, radius + 1, r) if t != 0 and n + t >= 4]


def direct_kind(row: dict[str, Any], p: int, q: int) -> str | None:
    """Classify rows containing the audit factors (used only for holdout + final audit table)."""
    has_p = p in row["factors"]
    has_q = q in row["factors"]
    if has_p and has_q:
        return "center"
    if has_p:
        return "p_thread"
    if has_q:
        return "q_thread"
    return None


# ============================================================
# LWM-BAND-01: Pure public banded support (PGS-native, literal web only)
# ============================================================

def band_for_r(r: int) -> int:
    """Deterministic public band partition function B(r).

    Exact rule (LWM-BAND-01 v1, log2(bit-length) bands):
        if r < 2: return 0
        bl = r.bit_length()
        return math.floor(math.log2(bl))

    This is a pure function of the public small-prime thread label r only.
    No dependence on N, p, q, offsets, or any audit labels.
    Produces logarithmically widening scale bands:
      - band 1: bl=2 (r=2,3)
      - band 1: bl=3 (r=4..7)
      - band 2: bl=4 (r=8..15)
      - band 2: bl=5..7 (r=16..127)
      - band 3: bl=8..15 (r=128..32767) etc.

    Contract note: GWR/DNI thread typing is explicitly reserved for later
    experiments (LWM-BAND-01 uses only raw public r bit-length).
    """
    if r < 2:
        return 0
    bl = r.bit_length()
    return math.floor(math.log2(bl))


def coherence_from_band_counts(band_counts: dict[int, int]) -> int:
    """Coherence score C(t): count of distinct bands with positive support at t.

    This directly encodes the Japanese "diagonal" / cross-band coherence invariant
    mapped to the literal web: true factor-distance holes are expected to draw
    threads from multiple scale classes, while spurious spikes often concentrate
    in a single band.
    """
    return sum(1 for c in band_counts.values() if c > 0)


def compute_banded_view(support: dict[int, list[int]]) -> dict[int, dict[str, Any]]:
    """Pure post-processing: from flat public support lists, emit per-offset banded data.

    Returns mapping offset -> {
        "flat_support": int,
        "band_support": dict[band, count],
        "coherence": C(t),
        "bands": sorted list of bands present
    }
    All inputs are already public (post-holdout) thread data.
    """
    banded: dict[int, dict[str, Any]] = {}
    for offset, rs in support.items():
        flat = len(rs)
        band_counts = Counter(band_for_r(r) for r in rs)
        c = coherence_from_band_counts(band_counts)
        banded[offset] = {
            "flat_support": flat,
            "band_support": dict(sorted(band_counts.items())),  # deterministic order
            "coherence": c,
            "bands": sorted(band_counts.keys()),
        }
    return banded


def select_max_c_offsets(banded: dict[int, dict[str, Any]], support: dict[int, list[int]]) -> set[int]:
    """Nomination rule for LWM-BAND-01: all offsets achieving the global max C(t).

    Tie-break for secondary ordering (when emitting lists): higher flat_support,
    then smaller |offset|, then smaller offset. This is public and deterministic.
    """
    if not banded:
        return set()
    max_c = max(b["coherence"] for b in banded.values())
    return {
        offset for offset, b in banded.items()
        if b["coherence"] == max_c
    }


def rank_of_true_offsets(
    all_offsets: list[int],
    true_offsets: set[int],
    key_func: callable
) -> dict[int, int]:
    """Return 1-based rank of each true offset under the given public sort key.

    key_func(offset) -> tuple for sorting (higher better for first components).
    Only offsets that have support >0 are ranked.
    """
    ranked = sorted(all_offsets, key=key_func, reverse=True)  # convention: key higher = better
    ranks = {}
    for i, off in enumerate(ranked, 1):
        if off in true_offsets:
            ranks[off] = i
    return ranks


def analyze_case_banded(case: dict[str, Any]) -> dict[str, Any]:
    """Core analysis for LWM-BAND-01.

    1. Build public web exactly as baseline (factor visible composites).
    2. Hold out direct p/q rows (audit only; never used for threads or bands).
    3. Compute flat public support from heldout threads only.
    4. Apply pure B and C to produce banded view.
    5. Nominate TWO public sets:
       - flat_max_support_set (baseline rule)
       - banded_max_c_set (new rule)
    6. Compute ranks of true direct offsets under both public sort orders.
    7. Attach audit labels ONLY for the final comparison table / findings (after
       all public nomination decisions are complete).
    """
    p, q = case["p"], case["q"]
    n = p * q
    # Radius: explicit if provided (ladder rungs), else baseline public sqrt
    radius = case.get("radius", public_radius(n))

    rows = rows_around(n, radius)
    by_offset = {row["offset"]: row for row in rows}

    direct_offsets = {
        row["offset"]: direct_kind(row, p, q)
        for row in rows
        if direct_kind(row, p, q)
    }
    heldout = [row for row in rows if row["offset"] not in direct_offsets]
    heldout_offsets = {row["offset"] for row in heldout}

    # Public threads only (from heldout rows)
    factors = sorted({r for row in heldout for r in row["factors"]})
    support: dict[int, list[int]] = defaultdict(list)
    for r in factors:
        for offset in thread_slots(n, radius, r):
            if offset not in heldout_offsets:
                support[offset].append(r)

    # === Flat baseline (exact copy of original nomination logic) ===
    flat_max_support = max((len(s) for s in support.values()), default=0)
    flat_top_offsets = {
        offset for offset, s in support.items() if len(s) == flat_max_support
    }

    # === Banded view (new, pure) ===
    banded = compute_banded_view(support)
    banded_max_c = max((b["coherence"] for b in banded.values()), default=0)
    banded_top_offsets = select_max_c_offsets(banded, support)

    # All supported offsets (public)
    all_supported_offsets = sorted(support.keys())

    # True direct offsets (the p/q thread positions we hope to surface)
    true_direct_offsets = {
        off for off, kind in direct_offsets.items()
        if kind in {"p_thread", "q_thread"}
    }

    # Public sort keys (higher = better)
    def flat_key(off: int):
        s = support.get(off, [])
        return (len(s), -abs(off), -off)  # support desc, |t| asc, t asc for determinism

    def banded_key(off: int):
        b = banded.get(off, {"coherence": 0, "flat_support": 0})
        return (b["coherence"], len(support.get(off, [])), -abs(off), -off)

    flat_ranks = rank_of_true_offsets(all_supported_offsets, true_direct_offsets, flat_key)
    banded_ranks = rank_of_true_offsets(all_supported_offsets, true_direct_offsets, banded_key)

    # Build full hole records (public scores + audit labels attached post-nomination)
    holes = []
    for offset, rs in sorted(support.items(), key=lambda item: (-len(item[1]), abs(item[0]), item[0])):
        row = by_offset.get(offset)
        audit = direct_offsets.get(offset)
        b = banded[offset]
        holes.append({
            "offset": offset,
            "value": n + offset,
            "flat_support": len(rs),
            "supporting_factors": rs,
            "band_support": b["band_support"],
            "coherence": b["coherence"],
            "bands": b["bands"],
            "audit_kind": audit if audit else ("other_composite" if row else "not_composite"),
            "audit_factorization": row["factorization"] if row else None,
        })

    flat_top_holes = [h for h in holes if h["offset"] in flat_top_offsets]
    banded_top_holes = [h for h in holes if h["offset"] in banded_top_offsets]

    # Emitted set sizes (cardinality under each rule)
    flat_emitted_size = len(flat_top_holes)
    banded_emitted_size = len(banded_top_holes)

    # Hits inside emitted sets (for audit table only)
    flat_hits = sum(1 for h in flat_top_holes if h["audit_kind"] in {"p_thread", "q_thread"})
    banded_hits = sum(1 for h in banded_top_holes if h["audit_kind"] in {"p_thread", "q_thread"})

    # Direct row support stats (baseline style)
    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        row = by_offset[offset]
        direct_rows.append({
            "offset": offset,
            "kind": kind,
            "value": row["value"],
            "factorization": row["factorization"],
            "flat_support": len(support.get(offset, [])),
            "coherence": banded.get(offset, {}).get("coherence", 0),
            "band_support": banded.get(offset, {}).get("band_support", {}),
        })

    supported_direct = sum(1 for d in direct_rows if d["flat_support"] > 0)
    true_direct_with_support = [d for d in direct_rows if d["flat_support"] > 0 and d["kind"] in {"p_thread", "q_thread"}]

    # Coherence differential for true vs nearest false high-flat points (for findings)
    true_coherences = [d["coherence"] for d in true_direct_with_support]
    # Find a false high-support point for comparison (highest flat among non-true)
    false_high = sorted(
        [(off, len(support[off]), banded[off]["coherence"]) for off in support
         if off not in true_direct_offsets],
        key=lambda x: (-x[1], -x[2], abs(x[0]))
    )[:3] if support else []

    return {
        "name": case["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "row_count_full": len(rows),
        "row_count_heldout": len(heldout),
        # Flat baseline metrics
        "flat_max_support": flat_max_support,
        "flat_emitted_size": flat_emitted_size,
        "flat_direct_hits": flat_hits,
        # Banded metrics
        "banded_max_c": banded_max_c,
        "banded_emitted_size": banded_emitted_size,
        "banded_direct_hits": banded_hits,
        # Comparison
        "flat_ranks_of_true": flat_ranks,
        "banded_ranks_of_true": banded_ranks,
        "true_direct_offsets": sorted(true_direct_offsets),
        "true_coherences": true_coherences,
        "false_high_flat_examples": false_high,
        # Full data for artifacts
        "direct_rows": direct_rows,
        "flat_top_holes": flat_top_holes,
        "banded_top_holes": banded_top_holes,
        "all_holes_public_view": holes,  # contains both scores + audit for this report only
    }


# ============================================================
# Public artifact writers (JSONL, summary, manifest)
# ============================================================

def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_public_jsonl(results: list[dict]) -> None:
    """Emit machine-readable public records with both flat and banded scores."""
    flat_records = []
    banded_records = []
    for res in results:
        for h in res["flat_top_holes"]:
            flat_records.append({
                "case": res["name"],
                "view": "flat_baseline",
                "offset": h["offset"],
                "flat_support": h["flat_support"],
                "coherence": h.get("coherence", None),
                "band_support": h.get("band_support"),
            })
        for h in res["banded_top_holes"]:
            banded_records.append({
                "case": res["name"],
                "view": "banded_LWM-BAND-01",
                "offset": h["offset"],
                "flat_support": h["flat_support"],
                "coherence": h["coherence"],
                "band_support": h["band_support"],
                "bands": h["bands"],
            })
    write_jsonl(OUT / "flat_top_holes.jsonl", flat_records)
    write_jsonl(OUT / "banded_top_holes.jsonl", banded_records)

    # Also full public view per case (all supported offsets with dual scores)
    all_public = []
    for res in results:
        for h in res["all_holes_public_view"]:
            all_public.append({
                "case": res["name"],
                "offset": h["offset"],
                "flat_support": h["flat_support"],
                "coherence": h["coherence"],
                "band_support": h["band_support"],
                "bands": h["bands"],
            })
    write_jsonl(OUT / "all_supported_offsets.jsonl", all_public)


def write_summary_md(results: list[dict]) -> None:
    lines = [
        "# LWM-BAND-01 Banded Diagonal Support — Public Summary",
        "",
        "Experiment: Banded support via public log2(bit-length) partition B(r) + coherence C(t) = # active bands.",
        "Contract: literal web only. Public threads → holdout direct p/q rows → public B/C scoring → emit max-C set.",
        "Baseline comparison: identical public web input; flat max-support vs. banded max-C nomination.",
        "",
        "Band rule (exact, public): B(r) = floor(log2(r.bit_length())) for r>=2.",
        "Coherence: C(t) = number of distinct bands with >=1 thread at offset t.",
        "Nomination (both views): the full set of offsets achieving the global maximum score under that view.",
        "",
        "| case | radius | flat_max_supp | flat_emitted | flat_hits | banded_max_C | banded_emitted | banded_hits |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in results:
        lines.append(
            f"| {r['name']} | {r['radius']} | {r['flat_max_support']} | {r['flat_emitted_size']} | "
            f"{r['flat_direct_hits']} | {r['banded_max_c']} | {r['banded_emitted_size']} | {r['banded_direct_hits']} |"
        )

    lines += ["", "## Per-Case Public Comparison (before/after)", ""]
    for r in results:
        lines.append(f"### {r['name']} (N={r['N']}, radius={r['radius']})")
        lines.append("")
        lines.append(f"- True direct offsets (p/q thread positions): {r['true_direct_offsets']}")
        lines.append(f"- Flat baseline: max support = {r['flat_max_support']}, emitted set size = {r['flat_emitted_size']}")
        lines.append(f"  Ranks of true offsets under flat sort: {r['flat_ranks_of_true']}")
        lines.append(f"- Banded (LWM-BAND-01): max C = {r['banded_max_c']}, emitted set size = {r['banded_emitted_size']}")
        lines.append(f"  Ranks of true offsets under banded sort: {r['banded_ranks_of_true']}")
        lines.append(f"- True offset coherence values: {r['true_coherences']}")
        if r["false_high_flat_examples"]:
            lines.append(f"- Example high-flat false points (offset, flat_supp, coherence): {r['false_high_flat_examples']}")
        lines.append("")
        lines.append("Flat top holes (baseline):")
        for h in r["flat_top_holes"]:
            lines.append(f"  - offset {h['offset']}: flat_support={h['flat_support']}, coherence={h.get('coherence')}, audit={h['audit_kind']}")
        lines.append("Banded top holes (new):")
        for h in r["banded_top_holes"]:
            lines.append(f"  - offset {h['offset']}: flat_support={h['flat_support']}, C={h['coherence']}, bands={h['bands']}, audit={h['audit_kind']}")
        lines.append("")

    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def write_manifest(results: list[dict]) -> None:
    """SHA256 manifest of all inputs (this script + baseline copy) and outputs."""
    manifest = {
        "experiment": "LWM-BAND-01",
        "contract": "literal-web-rewind / japanese-thread-mapping-plan",
        "band_rule": "B(r) = floor(log2(r.bit_length())) for r>=2 (see source)",
        "coherence_rule": "C(t) = count of bands with positive support",
        "nomination": "full set achieving global max score (flat or C)",
        "files": {},
    }

    # Inputs (for reproducibility)
    for rel in ["run_LWM_BAND_01.py", "literal_web_hole_trace_baseline.py"]:
        p = HERE / rel
        if p.exists():
            manifest["files"][f"input/{rel}"] = compute_sha256(p)

    # Outputs
    for name in [
        "flat_top_holes.jsonl",
        "banded_top_holes.jsonl",
        "all_supported_offsets.jsonl",
        "summary.md",
    ]:
        p = OUT / name
        if p.exists():
            manifest["files"][f"output/{name}"] = compute_sha256(p)

    # Per-case result digests (lightweight)
    manifest["case_digests"] = {}
    for r in results:
        # Include only public nomination info in digest
        manifest["case_digests"][r["name"]] = {
            "N": r["N"],
            "radius": r["radius"],
            "flat_emitted_size": r["flat_emitted_size"],
            "banded_emitted_size": r["banded_emitted_size"],
            "flat_ranks": r["flat_ranks_of_true"],
            "banded_ranks": r["banded_ranks_of_true"],
            "true_offsets": r["true_direct_offsets"],
        }

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Also write a plain text manifest for humans
    lines = ["# LWM-BAND-01 SHA256 Manifest", "", "All paths relative to LWM-BAND-01/"]
    for k, v in sorted(manifest["files"].items()):
        lines.append(f"{v}  {k}")
    lines += ["", "## Case Digests (public nomination summary)"]
    for name, d in manifest["case_digests"].items():
        lines.append(f"{name}: {json.dumps(d, sort_keys=True)}")
    (OUT / "MANIFEST.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    print("LWM-BAND-01: starting banded diagonal support experiment (literal web contract)...")
    results = [analyze_case_banded(case) for case in ALL_CASES]

    # Write public artifacts (dual view)
    write_public_jsonl(results)
    write_summary_md(results)
    write_manifest(results)

    # Also raw full results for audit (internal to this experiment dir)
    (OUT / "LWM_BAND_01_full_results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(f"LWM-BAND-01: wrote artifacts for {len(results)} cases to {OUT}")
    print("Key public files: summary.md, manifest.json, *_top_holes.jsonl")


if __name__ == "__main__":
    main()
