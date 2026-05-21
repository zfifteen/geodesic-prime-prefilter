#!/usr/bin/env python3
"""Literal multiplicative-web hole trace experiment.

This deliberately avoids residue certificates and ranking machinery. It reads
the visible factor-thread web around N, removes direct p/q rows for audit, then
asks which public threads point to missing offsets.
"""

from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from sympy import factorint

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"

CASES = [
    {"name": "toy_23x31", "p": 23, "q": 31},
    {"name": "toy_43x59", "p": 43, "q": 59},
    {"name": "toy_61x83", "p": 61, "q": 83},
    {"name": "toy_89x113", "p": 89, "q": 113},
]

WINDOW_N_RATIO = (1, 18)
EMITTED_HOLE_RATIO = (1, 20)
SUPPORT_PREVIEW_RATIO = (8, 9)
MD_PREVIEW_RATIO = (4, 9)
HTML_PREVIEW_RATIO = (5, 9)


def ceil_ratio(value, numerator, denominator):
    return (value * numerator + denominator - 1) // denominator


def public_radius(n):
    return ceil_ratio(n, *WINDOW_N_RATIO)


def emitted_hole_count(radius):
    return ceil_ratio(radius, *EMITTED_HOLE_RATIO)


def support_preview_count(emitted_count):
    return ceil_ratio(emitted_count, *SUPPORT_PREVIEW_RATIO)


def md_preview_count(emitted_count):
    return ceil_ratio(emitted_count, *MD_PREVIEW_RATIO)


def html_preview_count(emitted_count):
    return ceil_ratio(emitted_count, *HTML_PREVIEW_RATIO)


def factor_label(factors):
    return " * ".join(
        str(p) if e == 1 else f"{p}^{e}" for p, e in sorted(factors.items())
    )


def rows_around(n, radius):
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


def thread_slots(n, radius, r):
    start = -radius
    residue = (-n) % r
    first = start + ((residue - start) % r)
    return [t for t in range(first, radius + 1, r) if t != 0 and n + t >= 4]


def direct_kind(row, p, q):
    has_p = p in row["factors"]
    has_q = q in row["factors"]
    if has_p and has_q:
        return "center"
    if has_p:
        return "p_thread"
    if has_q:
        return "q_thread"
    return None


def analyze_case(case):
    p, q = case["p"], case["q"]
    n = p * q
    radius = public_radius(n)
    emitted_count = emitted_hole_count(radius)
    support_preview = support_preview_count(emitted_count)
    rows = rows_around(n, radius)
    by_offset = {row["offset"]: row for row in rows}
    direct_offsets = {
        row["offset"]: direct_kind(row, p, q)
        for row in rows
        if direct_kind(row, p, q)
    }
    heldout = [row for row in rows if row["offset"] not in direct_offsets]
    heldout_offsets = {row["offset"] for row in heldout}

    factors = sorted({r for row in heldout for r in row["factors"]})
    support = defaultdict(list)
    for r in factors:
        for offset in thread_slots(n, radius, r):
            if offset not in heldout_offsets:
                support[offset].append(r)

    holes = []
    for offset, supporters in sorted(support.items(), key=lambda item: (-len(item[1]), abs(item[0]), item[0])):
        row = by_offset.get(offset)
        audit = direct_offsets.get(offset)
        holes.append({
            "offset": offset,
            "value": n + offset,
            "support": len(supporters),
            "supporting_factors": supporters[:support_preview],
            "support_truncated": len(supporters) > support_preview,
            "audit_kind": audit if audit else ("other_composite" if row else "not_composite"),
            "audit_factorization": row["factorization"] if row else None,
        })

    top_holes = holes[:emitted_count]
    direct_rows = []
    for offset, kind in sorted(direct_offsets.items(), key=lambda item: item[0]):
        row = by_offset[offset]
        direct_rows.append({
            "offset": offset,
            "kind": kind,
            "value": row["value"],
            "factorization": row["factorization"],
            "support": len(support.get(offset, [])),
            "supporting_factors": support.get(offset, [])[:support_preview],
        })

    emitted_direct_hits = sum(1 for hole in top_holes if hole["audit_kind"] in {"p_thread", "q_thread"})
    supported_direct = sum(1 for row in direct_rows if row["support"] > 0)
    return {
        "name": case["name"],
        "N": n,
        "p": p,
        "q": q,
        "radius": radius,
        "row_count_full": len(rows),
        "row_count_heldout": len(heldout),
        "emitted_hole_count": len(top_holes),
        "direct_row_count": len(direct_rows),
        "supported_direct_count": supported_direct,
        "emitted_direct_hits": emitted_direct_hits,
        "direct_rows": direct_rows,
        "top_holes": top_holes,
    }


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_summary_md(results):
    lines = [
        "# Literal Web Hole Trace",
        "",
        "This resets the experiment to the original multiplicative-web object: factor threads around N, direct p/q rows held out for audit, and public thread holes left behind by those held-out intersections.",
        "",
        "| case | radius | emitted holes | heldout rows | direct rows | supported direct rows | direct hits in emitted holes |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        lines.append(
            f"| {result['name']} | {result['radius']} | {result['emitted_hole_count']} | "
            f"{result['row_count_heldout']} | {result['direct_row_count']} | "
            f"{result['supported_direct_count']} | {result['emitted_direct_hits']} |"
        )
    lines += ["", "## Per-Case Notes", ""]
    for result in results:
        lines.append(f"### {result['name']}")
        lines.append("")
        lines.append("Top supported holes:")
        for hole in result["top_holes"][:md_preview_count(result["emitted_hole_count"])]:
            lines.append(
                f"- offset {hole['offset']}: support {hole['support']}, "
                f"audit `{hole['audit_kind']}`"
            )
        lines.append("")
    (OUT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def html_escape(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_axis(result):
    radius = result["radius"]
    width = 980
    height = 92
    mid = width / 2
    scale = (width - 60) / (2 * radius)
    parts = [
        f'<svg viewBox="0 0 {width} {height}" role="img">',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        f'<line x1="30" y1="46" x2="{width-30}" y2="46" stroke="#94a3b8" stroke-width="1"/>',
        f'<line x1="{mid}" y1="20" x2="{mid}" y2="72" stroke="#0f766e" stroke-width="2"/>',
    ]
    for hole in result["top_holes"]:
        if abs(hole["offset"]) > radius:
            continue
        x = mid + hole["offset"] * scale
        color = "#dc2626" if hole["audit_kind"] in {"p_thread", "q_thread"} else "#2563eb"
        r = min(12, 3 + hole["support"])
        parts.append(f'<circle cx="{x:.1f}" cy="46" r="{r}" fill="{color}" opacity="0.72"/>')
    parts.append('</svg>')
    return "".join(parts)


def write_index_html(results):
    cards = []
    for result in results:
        rows = []
        for hole in result["top_holes"][:html_preview_count(result["emitted_hole_count"])]:
            rows.append(
                "<tr>"
                f"<td>{hole['offset']}</td>"
                f"<td>{hole['support']}</td>"
                f"<td>{html_escape(hole['audit_kind'])}</td>"
                f"<td>{html_escape(', '.join(map(str, hole['supporting_factors'][:8])))}</td>"
                "</tr>"
            )
        cards.append(
            f"""
            <section class="case">
              <h2>{html_escape(result['name'])}</h2>
              <p>N={result['N']}, radius={result['radius']}. Direct audit rows held out: {result['direct_row_count']}. Supported direct audit rows: {result['supported_direct_count']}.</p>
              {render_axis(result)}
              <table>
                <tr><th>hole offset</th><th>support</th><th>audit label</th><th>public supporting factors</th></tr>
                {''.join(rows)}
              </table>
            </section>
            """
        )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Literal Web Hole Trace</title>
<style>
body {{ margin:0; background:#fbfcfd; color:#1f2933; font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1080px; margin:0 auto; padding:28px 20px 56px; }}
h1 {{ font-size:1.9rem; margin:0 0 8px; }}
h2 {{ font-size:1.2rem; margin:22px 0 8px; }}
.lead, .case {{ background:#fff; border:1px solid #d8dee6; border-radius:6px; padding:14px 16px; margin:12px 0; }}
.lead {{ border-left:4px solid #0f766e; }}
table {{ width:100%; border-collapse:collapse; font-size:12px; margin-top:10px; }}
th, td {{ border:1px solid #d8dee6; padding:6px 8px; text-align:left; }}
th {{ background:#f4f6f8; }}
code {{ background:#f1f5f9; padding:1px 4px; border-radius:3px; }}
</style>
</head>
<body>
<main>
<h1>Literal Web Hole Trace</h1>
<div class="lead">
<p>This is the reset experiment. It keeps the original object literal: public factor threads around <code>N</code>. Rows containing audit factors <code>p</code> or <code>q</code> are held out. The experiment then asks which missing offsets are still supported by public factor threads.</p>
<p>Red holes are audit hits: missing offsets that were direct <code>p</code> or <code>q</code> thread rows before holdout. Blue holes are other missing thread slots, usually primes or non-heldout absences. No modular ranking, no residue certificate, no factor claim.</p>
</div>
{''.join(cards)}
</main>
</body>
</html>
"""
    (HERE / "index.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = [analyze_case(case) for case in CASES]
    (OUT / "literal_web_hole_trace.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    write_jsonl(OUT / "top_holes.jsonl", [
        {"case": result["name"], **hole}
        for result in results
        for hole in result["top_holes"]
    ])
    write_summary_md(results)
    write_index_html(results)
    print(f"wrote {len(results)} cases to {OUT}")


if __name__ == "__main__":
    main()
