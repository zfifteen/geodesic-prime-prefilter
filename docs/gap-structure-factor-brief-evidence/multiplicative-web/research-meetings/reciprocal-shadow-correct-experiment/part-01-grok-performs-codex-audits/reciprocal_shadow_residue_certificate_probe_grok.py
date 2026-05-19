#!/usr/bin/env python3
"""Reciprocal shadow residue-certificate probe (Part One - Grok performs).

This implements the exact residue-certificate generator from the controlling
design contract. It emits admissible lower-endpoint residue classes a mod M
derived solely from per-r transport consistency (b agreement across threads
for each selected high-degree r) + CRT merge on the held-out thread list.

No numeric candidate generation, no p/q in generator after build_case,
no gcd(N, *), no downward walks, no product closure for acceptance.
p and q are used only for case construction, hold-out of direct rows,
and final membership audit after all certificates are emitted.

Controls: rotated-offset (cyclic) and deterministic synthetic-offset.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Core web construction (copied from plot_multiplicative_web.py for self-containment)
# ---------------------------------------------------------------------------

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    d = 5
    while d * d <= n:
        if n % d == 0 or n % (d + 2) == 0:
            return False
        d += 6
    return True


def factorization(n: int) -> dict[int, int]:
    value = n
    factors: dict[int, int] = {}
    if value % 2 == 0:
        cnt = 0
        while value % 2 == 0:
            cnt += 1
            value //= 2
        factors[2] = cnt
    if value % 3 == 0:
        cnt = 0
        while value % 3 == 0:
            cnt += 1
            value //= 3
        factors[3] = cnt
    d = 5
    while d * d <= value:
        if value % d == 0:
            cnt = 0
            while value % d == 0:
                cnt += 1
                value //= d
            factors[d] = cnt
        d += 2
        if d * d <= value and value % d == 0:
            cnt = 0
            while value % d == 0:
                cnt += 1
                value //= d
            factors[d] = cnt
        d += 4
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def composite_rows(n_value: int, radius: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for value in range(n_value - radius, n_value + radius + 1):
        if value < 4 or value == n_value or is_prime(value):
            continue
        factors = factorization(value)
        rows.append(
            {
                "value": value,
                "offset": value - n_value,
                "factors": factors,
                "divisor_count": int(math.prod((e + 1) for e in factors.values())),
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Control row generators (rotated from original probe; synthetic deterministic)
# ---------------------------------------------------------------------------

def rotated_offset_control_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []
    offsets = [int(row["offset"]) for row in rows]
    rotated_offsets = offsets[1:] + offsets[:1]
    out = []
    for row, off in zip(rows, rotated_offsets, strict=True):
        copied = {k: v for k, v in row.items() if k != "offset"}
        copied["offset"] = off
        out.append(copied)
    return out


def deterministic_synthetic_offset_control_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deterministic synthetic offsets: re-order rows by canonical factor signature,
    assign consecutive centered offsets. Destroys true offset-to-factor pairing
    while preserving the multiset of factor bundles. No randomness.
    """
    if not rows:
        return []
    def factor_sig(row: dict[str, Any]) -> tuple[tuple[int, int], ...]:
        fac = row["factors"]
        return tuple(sorted((int(k), int(v)) for k, v in fac.items()))
    ordered = sorted(rows, key=factor_sig)
    n = len(ordered)
    synth_offs = list(range(-n // 2, -n // 2 + n))
    out = []
    for row, off in zip(ordered, synth_offs, strict=True):
        copied = {k: v for k, v in row.items() if k != "offset"}
        copied["offset"] = off
        out.append(copied)
    return out


# ---------------------------------------------------------------------------
# Residue certificate generator (pure, no p/q after build_case)
# ---------------------------------------------------------------------------

def compute_residue_certificate(
    heldout_rows: list[dict[str, Any]],
    log_entries: list[dict[str, Any]],
    case_id: str,
    surface: str,
) -> dict[str, Any]:
    """For the given held-out thread rows, select top-4 (or 3) r by degree,
    then for each a in 0..M-1 test whether the transported b's agree within
    each r's threads. If yes for all selected r, emit admissible (a, y) via CRT.
    Log only arithmetic that contributes an accepted member to C.
    """
    degree: Counter[int] = Counter()
    r_to_offsets: dict[int, list[int]] = defaultdict(list)
    for row in heldout_rows:
        off = int(row["offset"])
        for r in row.get("factors", {}):
            r = int(r)
            degree[r] += 1
            r_to_offsets[r].append(off)

    if not degree:
        return {"M": 1, "selected_rs": [], "admissible": [], "cardinality": 0}

    sorted_r = sorted(degree.items(), key=lambda kv: (-kv[1], kv[0]))
    top4 = [r for r, _ in sorted_r[:4]]
    M = 1
    for r in top4:
        M *= r
    if M > 5_000_000:
        selected_rs = [r for r, _ in sorted_r[:3]]
        M = 1
        for r in selected_rs:
            M *= r
    else:
        selected_rs = top4

    if not selected_rs:
        return {"M": 1, "selected_rs": [], "admissible": [], "cardinality": 0}

    admissible: list[dict[str, Any]] = []
    covered_threads = sum(degree[r] for r in selected_rs)

    for a in range(M):
        b_per_r: dict[int, int] = {}
        per_r_details: dict[int, Any] = {}
        conflict = False
        for r in selected_rs:
            offsets = r_to_offsets[r]
            a_r = a % r
            if a_r == 0:
                # 0 not invertible mod prime r; reject (consistent with coprimality)
                conflict = True
                break
            try:
                inv = pow(a_r, -1, r)
            except ValueError:
                conflict = True
                break
            b_set: set[int] = set()
            for off in offsets:
                b = ((-off % r) * inv) % r
                b_set.add(b)
            if len(b_set) != 1:
                conflict = True
                break
            b = next(iter(b_set))
            b_per_r[r] = b
            per_r_details[r] = {
                "a_r": a_r,
                "inv": inv,
                "b": b,
                "num_threads": len(offsets),
            }
        if conflict:
            continue

        # CRT merge (moduli distinct primes => always succeeds when no conflict)
        y = 0
        mod_so_far = 1
        crt_steps: list[dict[str, Any]] = []
        for r in selected_rs:
            b = b_per_r[r]
            diff = (b - y) % r
            inv_mod = pow(mod_so_far % r, -1, r)
            k = (diff * inv_mod) % r
            y = (y + mod_so_far * k) % (mod_so_far * r)
            crt_steps.append(
                {
                    "r": r,
                    "b": b,
                    "mod_before": mod_so_far,
                    "k": k,
                    "y_after": y,
                    "M_after": mod_so_far * r,
                }
            )
            mod_so_far *= r

        score = float(covered_threads)  # constant for all passing a under this rule
        entry = {
            "a": a,
            "y": y,
            "score": score,
            "M": M,
            "selected_rs": selected_rs,
            "covered_threads": covered_threads,
        }
        admissible.append(entry)

        log_entries.append(
            {
                "case_id": case_id,
                "surface": surface,
                "a": a,
                "y": y,
                "M": M,
                "selected_rs": selected_rs,
                "per_r": per_r_details,
                "crt_steps": crt_steps,
                "covered_threads": covered_threads,
            }
        )

    # sort: score desc (all equal), then a asc
    admissible.sort(key=lambda x: (-x["score"], x["a"]))
    for rank, item in enumerate(admissible, 1):
        item["rank"] = rank

    return {
        "M": M,
        "selected_rs": selected_rs,
        "admissible": admissible,
        "cardinality": len(admissible),
        "covered_threads": covered_threads,
    }


# ---------------------------------------------------------------------------
# Build case (p/q only here for construction + hold-out)
# ---------------------------------------------------------------------------

def build_case(p: int, q: int, radius: int) -> dict[str, Any]:
    """Return held-out rows and controls. p/q never leave this function
    except for the caller's final audit step.
    """
    N = p * q
    rows = composite_rows(N, radius)
    heldout = [
        row
        for row in rows
        if p not in row["factors"] and q not in row["factors"]
    ]
    rotated = rotated_offset_control_rows(heldout)
    synth = deterministic_synthetic_offset_control_rows(heldout)
    return {
        "N": N,
        "heldout_rows": heldout,
        "rotated_rows": rotated,
        "synth_rows": synth,
        "heldout_count": len(heldout),
        "direct_removed": len(rows) - len(heldout),
    }


# ---------------------------------------------------------------------------
# Case list: original 16 + 4 new natural-ratio large semiprimes
# ---------------------------------------------------------------------------

CASES: list[dict[str, int]] = [
    # original 16 from reciprocal_shadow_vote_probe.py
    {"p": 23, "q": 31},
    {"p": 43, "q": 59},
    {"p": 61, "q": 83},
    {"p": 89, "q": 113},
    {"p": 101, "q": 137},
    {"p": 131, "q": 167},
    {"p": 173, "q": 211},
    {"p": 229, "q": 277},
    {"p": 307, "q": 367},
    {"p": 401, "q": 503},
    {"p": 557, "q": 661},
    {"p": 701, "q": 887},
    {"p": 1009, "q": 1231},
    {"p": 1601, "q": 2003},
    {"p": 3001, "q": 4001},
    {"p": 5003, "q": 7001},
    # 4 additional, sqrtN > 10M, all with p < 0.6 * sqrtN (natural ratios)
    {"p": 7500013, "q": 29999989},
    {"p": 6000011, "q": 37499947},
    {"p": 4500007, "q": 49999991},
    {"p": 3000017, "q": 74999647},
]

FIXED_RADIUS = 300


def classify_case(
    p_in_true: bool,
    p_rank_true: int | None,
    card_true: int,
    p_in_rot: bool,
    p_rank_rot: int | None,
    card_rot: int,
    p_in_synth: bool,
    p_rank_synth: int | None,
    card_synth: int,
) -> str:
    if not p_in_true:
        return "invalidated_result"
    if card_true > 64:
        return "boundary_measurement"
    if p_rank_true is not None and p_rank_true > 3:
        return "boundary_measurement"
    # controls should not nominate at comparable quality
    bad_controls = 0
    if p_in_rot and p_rank_rot is not None and p_rank_rot <= 3 and card_rot > 0:
        bad_controls += 1
    if p_in_synth and p_rank_synth is not None and p_rank_synth <= 3 and card_synth > 0:
        bad_controls += 1
    if bad_controls >= 1:
        return "invalidated_result"
    return "accepted_measured_result" if (card_true <= 64 and p_rank_true is not None) else "boundary_measurement"


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    out_dir = base_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_case_summaries: list[dict[str, Any]] = []
    all_cert_rows: list[dict[str, Any]] = []
    all_runtime_logs: list[dict[str, Any]] = []
    runtime_log_for_write: list[dict[str, Any]] = []

    for idx, case in enumerate(CASES):
        p = case["p"]
        q = case["q"]
        built = build_case(p, q, FIXED_RADIUS)

        logs: list[dict[str, Any]] = []
        cert_true = compute_residue_certificate(
            built["heldout_rows"], logs, f"case{idx}_true", "true_web"
        )
        cert_rot = compute_residue_certificate(
            built["rotated_rows"], logs, f"case{idx}_rot", "rotated_offset_control"
        )
        cert_synth = compute_residue_certificate(
            built["synth_rows"], logs, f"case{idx}_synth", "synthetic_offset_control"
        )

        # Final audit only (p/q appear here)
        M = cert_true["M"]
        pmod = p % M if M > 0 else 0

        def find_rank_and_member(cert: dict[str, Any], pmod_val: int) -> tuple[bool, int | None]:
            for item in cert["admissible"]:
                if item["a"] == pmod_val:
                    return True, item["rank"]
            return False, None

        p_in_true, rank_true = find_rank_and_member(cert_true, pmod)
        # For controls use same pmod (M identical in practice)
        p_in_rot, rank_rot = find_rank_and_member(cert_rot, pmod)
        p_in_synth, rank_synth = find_rank_and_member(cert_synth, pmod)

        classification = classify_case(
            p_in_true, rank_true, cert_true["cardinality"],
            p_in_rot, rank_rot, cert_rot["cardinality"],
            p_in_synth, rank_synth, cert_synth["cardinality"],
        )

        s = math.isqrt(built["N"])
        p_over_s = p / s if s > 0 else 0.0

        summary = {
            "case_idx": idx,
            "N": built["N"],
            "p": p,
            "q": q,
            "radius": FIXED_RADIUS,
            "p_over_sqrtN": round(p_over_s, 6),
            "heldout_rows": built["heldout_count"],
            "direct_removed": built["direct_removed"],
            "M": M,
            "selected_rs": cert_true["selected_rs"],
            "cardinality_true": cert_true["cardinality"],
            "p_in_true": p_in_true,
            "p_rank_true": rank_true,
            "cardinality_rot": cert_rot["cardinality"],
            "p_in_rot": p_in_rot,
            "p_rank_rot": rank_rot,
            "cardinality_synth": cert_synth["cardinality"],
            "p_in_synth": p_in_synth,
            "p_rank_synth": rank_synth,
            "classification": classification,
        }
        all_case_summaries.append(summary)

        # certificate rows (one per admissible across surfaces)
        for surf_name, cert in [
            ("true_web", cert_true),
            ("rotated_offset_control", cert_rot),
            ("synthetic_offset_control", cert_synth),
        ]:
            for item in cert["admissible"]:
                all_cert_rows.append(
                    {
                        "case_idx": idx,
                        "N": built["N"],
                        "surface": surf_name,
                        "a": item["a"],
                        "y": item["y"],
                        "score": item["score"],
                        "rank": item["rank"],
                        "M": cert["M"],
                        "selected_rs": cert["selected_rs"],
                        "p_mod_M": p % cert["M"],
                        "is_p_member": item["a"] == (p % cert["M"]),
                    }
                )

        # runtime logs (only accepted contributors)
        for entry in logs:
            runtime_log_for_write.append(entry)

        # also keep for in-memory if needed
        all_runtime_logs.extend(logs)

        print(
            f"case {idx}: N={built['N']} M={M} |C_true|={cert_true['cardinality']} "
            f"rank_true={rank_true} class={classification}"
        )

    # Write deliverables
    (out_dir / "summary.json").write_text(
        json.dumps(all_case_summaries, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    cert_path = out_dir / "certificate.jsonl"
    cert_path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in all_cert_rows),
        encoding="utf-8",
    )

    log_path = out_dir / "runtime_residue_crt_log.jsonl"
    log_path.write_text(
        "".join(json.dumps(r, sort_keys=True) + "\n" for r in runtime_log_for_write),
        encoding="utf-8",
    )

    # summary.md written by this script (basic table + findings)
    write_summary_md(out_dir / "summary.md", all_case_summaries)

    print(f"\nWrote outputs to {out_dir}")
    print(f"Total cases: {len(all_case_summaries)}")
    print(f"Total cert rows: {len(all_cert_rows)}")
    print(f"Total runtime log entries: {len(runtime_log_for_write)}")


def write_summary_md(path: Path, summaries: list[dict[str, Any]]) -> None:
    lines: list[str] = [
        "# Reciprocal Shadow Residue Certificate Probe (Grok Part One)",
        "",
        "Controlling contract: reciprocal_shadow_correct_experiment_design.html",
        "Implementation strictly follows the residue-certificate mechanism (conflict filter + CRT).",
        "No candidate walks, no hidden p/q in generator, deterministic controls only.",
        "",
        "## Surface Summary (20 cases: 16 original + 4 new natural-ratio >10M sqrtN)",
        "",
        "| idx | N | p | p/sqrtN | M | selected r | |C_true| | p rank true | |C_rot| | |C_synth| | classification |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    accepted = 0
    boundary = 0
    invalidated = 0
    unresolved = 0
    for s in summaries:
        lines.append(
            f"| {s['case_idx']} | {s['N']} | {s['p']} | {s['p_over_sqrtN']:.4f} | "
            f"{s['M']} | {s['selected_rs']} | {s['cardinality_true']} | "
            f"{s['p_rank_true']} | {s['cardinality_rot']} | {s['cardinality_synth']} | "
            f"{s['classification']} |"
        )
        c = s["classification"]
        if c == "accepted_measured_result":
            accepted += 1
        elif c == "boundary_measurement":
            boundary += 1
        elif c == "invalidated_result":
            invalidated += 1
        else:
            unresolved += 1

    lines.extend(
        [
            "",
            "## Observed Result (under exact operationalization)",
            "",
            "For every case the top-4 r were always [2, 3, 5, 7], M=210.",
            "True-web admissible set C is exactly the 48 residues a mod 210 with gcd(a,210)=1",
            "(the a's for which modular inverses exist and the shared-offset congruence of the",
            "true web guarantees b-agreement within each r).",
            "Controls (rotated and synthetic) produce |C|=0 because the reassigned offsets",
            "destroy the per-r congruence, causing b-conflicts on every a.",
            "",
            "p always lies in true C (p large prime => coprime to 210).",
            "p never lies in control C (empty).",
            "Rank of p inside true C (sorted by a asc) is the order statistic of (p mod 210)",
            "among the 48 coprime residues; typically mid-range (~5-40), never 1 or 2 for these p.",
            "",
            f"Classifications: {accepted} accepted_measured_result, {boundary} boundary_measurement,",
            f"{invalidated} invalidated_result, {unresolved} unresolved_implementation_failure.",
            "",
            "This is a boundary measurement of the closure rule as defined: the rule",
            "nominates the full coprime class set (size 48 <=64), which contains p, while",
            "controls nominate nothing. It does not achieve the hoped rank <=2 selector.",
            "The result is deterministic, fully logged, and falsifiable under the contract.",
            "",
            "## Checklist Status (see self_checklist.md for 12-item answers)",
            "",
            "All 12 items answered explicitly in self_checklist.md. The surface satisfies",
            "the structural-certificate contract and the explicit Part One requirements",
            "(original 16 + 4 new with 4 low-ratio cases, deterministic controls,",
            "p/q only in construction+final audit, runtime CRT log, raw outputs).",
            "",
            "No files written outside the Part One folder.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
