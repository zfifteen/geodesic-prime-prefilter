#!/usr/bin/env python3
"""Plot a deterministic factor-thread web around a semiprime N = p q."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = math.isqrt(n)
    d = 3
    while d <= limit:
        if n % d == 0:
            return False
        d += 2
    return True


def factorization(n: int) -> dict[int, int]:
    value = n
    factors: dict[int, int] = {}
    d = 2
    while d * d <= value:
        while value % d == 0:
            factors[d] = factors.get(d, 0) + 1
            value //= d
        d = 3 if d == 2 else d + 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def divisor_count(factors: dict[int, int]) -> int:
    total = 1
    for exponent in factors.values():
        total *= exponent + 1
    return total


def previous_prime(n: int) -> int:
    candidate = n - 1
    while candidate >= 2:
        if is_prime(candidate):
            return candidate
        candidate -= 1
    raise ValueError("no previous prime")


def next_prime(n: int) -> int:
    candidate = n + 1
    while True:
        if is_prime(candidate):
            return candidate
        candidate += 1


def composite_rows(n_value: int, radius: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for value in range(n_value - radius, n_value + radius + 1):
        if value < 4 or value == n_value or is_prime(value):
            continue
        factors = factorization(value)
        rows.append(
            {
                "value": value,
                "offset": value - n_value,
                "side": "left" if value < n_value else "right",
                "factors": factors,
                "divisor_count": divisor_count(factors),
            }
        )
    return rows


def factor_label(factors: dict[int, int]) -> str:
    parts = []
    for prime, exponent in sorted(factors.items()):
        parts.append(str(prime) if exponent == 1 else f"{prime}^{exponent}")
    return " * ".join(parts)


def build_graph(p_value: int, q_value: int, radius: int) -> dict[str, object]:
    n_value = p_value * q_value
    rows = composite_rows(n_value, radius)
    factor_degrees: dict[int, int] = {}
    for row in rows:
        for prime in row["factors"]:
            factor_degrees[int(prime)] = factor_degrees.get(int(prime), 0) + 1

    p_gap = {
        "previous": previous_prime(p_value),
        "factor": p_value,
        "next": next_prime(p_value),
    }
    q_gap = {
        "previous": previous_prime(q_value),
        "factor": q_value,
        "next": next_prime(q_value),
    }
    factor_nodes = sorted(factor_degrees)
    shared_factors = [prime for prime in factor_nodes if factor_degrees[prime] > 1]
    audit_factor_hits = [prime for prime in factor_nodes if prime in {p_value, q_value}]

    nodes = [{"id": "N", "kind": "product", "value": n_value}]
    for row in rows:
        nodes.append(
            {
                "id": f"c:{row['value']}",
                "kind": "composite",
                "value": row["value"],
                "offset": row["offset"],
                "side": row["side"],
                "divisor_count": row["divisor_count"],
                "factorization": factor_label(row["factors"]),
            }
        )
    for prime in factor_nodes:
        kind = "audit_factor" if prime in {p_value, q_value} else "factor"
        nodes.append(
            {
                "id": f"f:{prime}",
                "kind": kind,
                "value": prime,
                "degree": factor_degrees[prime],
                "shared_intersection": factor_degrees[prime] > 1,
            }
        )

    edges = []
    for row in rows:
        for prime, exponent in sorted(row["factors"].items()):
            edges.append(
                {
                    "source": f"c:{row['value']}",
                    "target": f"f:{prime}",
                    "kind": "factor_thread",
                    "multiplicity": exponent,
                }
            )

    return {
        "N": n_value,
        "p": p_value,
        "q": q_value,
        "radius": radius,
        "p_gap": p_gap,
        "q_gap": q_gap,
        "composite_count": len(rows),
        "factor_node_count": len(factor_nodes),
        "shared_factor_count": len(shared_factors),
        "shared_factors": shared_factors,
        "audit_factor_hits": audit_factor_hits,
        "nodes": nodes,
        "edges": edges,
    }


def svg_text(x: float, y: float, text: str, size: int = 12, fill: str = "#1f2933", weight: str = "400") -> str:
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
        f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{safe}</text>'
    )


def render_svg(graph: dict[str, object]) -> str:
    width = 1280
    height = 820
    cx = width / 2
    cy = 380
    n_value = int(graph["N"])
    p_value = int(graph["p"])
    q_value = int(graph["q"])
    nodes = list(graph["nodes"])
    composites = [node for node in nodes if node["kind"] == "composite"]
    factors = [node for node in nodes if node["kind"] in {"factor", "audit_factor"}]

    left_rows = [node for node in composites if node["side"] == "left"]
    right_rows = [node for node in composites if node["side"] == "right"]
    factor_positions: dict[str, tuple[float, float]] = {}
    composite_positions: dict[str, tuple[float, float]] = {}

    for index, row in enumerate(left_rows):
        x = 150 + (index % 8) * 52
        y = 170 + (index // 8) * 44
        composite_positions[str(row["id"])] = (x, y)
    for index, row in enumerate(right_rows):
        x = width - 150 - (index % 8) * 52
        y = 170 + (index // 8) * 44
        composite_positions[str(row["id"])] = (x, y)

    for index, node in enumerate(factors):
        angle = math.pi * (0.08 + 0.84 * index / max(1, len(factors) - 1))
        x = cx + 470 * math.cos(angle)
        y = 650 - 210 * math.sin(angle)
        factor_positions[str(node["id"])] = (x, y)

    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 820" role="img">',
        '<rect width="1280" height="820" fill="#101820"/>',
        '<rect x="34" y="34" width="1212" height="752" rx="10" fill="#13222d" stroke="#334155"/>',
        svg_text(cx, 72, "Multiplicative web around N", 28, "#f8fafc", "700"),
        svg_text(cx, 102, "Composite factorizations near the product form threads and intersections.", 14, "#cbd5e1"),
    ]

    for edge in graph["edges"]:
        source = str(edge["source"])
        target = str(edge["target"])
        if source not in composite_positions or target not in factor_positions:
            continue
        x1, y1 = composite_positions[source]
        x2, y2 = factor_positions[target]
        stroke = "#f59e0b" if target in {f"f:{p_value}", f"f:{q_value}"} else "#38bdf8"
        opacity = "0.78" if target in {f"f:{p_value}", f"f:{q_value}"} else "0.32"
        width_value = 2.4 if int(edge["multiplicity"]) > 1 else 1.4
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{width_value}" opacity="{opacity}"/>'
        )

    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="58" fill="#0f766e" stroke="#99f6e4" stroke-width="3"/>')
    parts.append(svg_text(cx, cy - 8, "N", 30, "#ffffff", "700"))
    parts.append(svg_text(cx, cy + 22, str(n_value), 14, "#ffffff", "700"))

    for node in composites:
        x, y = composite_positions[str(node["id"])]
        fill = "#1e293b"
        stroke = "#64748b"
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        parts.append(svg_text(x, y + 4, str(node["offset"]), 10, "#e2e8f0", "700"))
        parts.append(svg_text(x, y + 30, f"d={node['divisor_count']}", 9, "#94a3b8"))

    for node in factors:
        x, y = factor_positions[str(node["id"])]
        value = int(node["value"])
        shared = bool(node["shared_intersection"])
        audit = value in {p_value, q_value}
        fill = "#f59e0b" if audit else ("#1d4ed8" if shared else "#334155")
        stroke = "#fde68a" if audit else ("#93c5fd" if shared else "#64748b")
        radius = 25 if audit else (20 if shared else 16)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        parts.append(svg_text(x, y + 4, str(value), 12 if audit else 10, "#ffffff", "700"))
        if shared:
            parts.append(svg_text(x, y + radius + 14, f"{node['degree']} threads", 9, "#cbd5e1"))

    p_gap = graph["p_gap"]
    q_gap = graph["q_gap"]
    parts.extend(
        [
            '<rect x="82" y="612" width="270" height="82" rx="8" fill="#0f172a" stroke="#475569"/>',
            svg_text(217, 642, f"gap around p: {p_gap['previous']} | {p_value} | {p_gap['next']}", 13, "#fde68a", "700"),
            svg_text(217, 670, "amber threads mark audit-visible p", 11, "#cbd5e1"),
            '<rect x="928" y="612" width="270" height="82" rx="8" fill="#0f172a" stroke="#475569"/>',
            svg_text(1063, 642, f"gap around q: {q_gap['previous']} | {q_value} | {q_gap['next']}", 13, "#fde68a", "700"),
            svg_text(1063, 670, "amber threads mark audit-visible q", 11, "#cbd5e1"),
            svg_text(cx, 752, "Blue nodes are shared intersections; amber nodes are known factor endpoints for audit.", 13, "#cbd5e1"),
        ]
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_summary(path: Path, graph: dict[str, object]) -> None:
    lines = [
        "# Multiplicative Web Summary",
        "",
        f"- `N = {graph['N']}`",
        f"- `p = {graph['p']}`",
        f"- `q = {graph['q']}`",
        f"- radius: `{graph['radius']}`",
        f"- composites plotted: `{graph['composite_count']}`",
        f"- factor nodes: `{graph['factor_node_count']}`",
        f"- shared factor intersections: `{graph['shared_factor_count']}`",
        f"- audit factor hits in nearby composite threads: `{graph['audit_factor_hits']}`",
        "",
        "## Boundary",
        "",
        "This output visualizes exact factor threads around `N`. It is an audit and",
        "concept surface, not a live factor inference rule.",
        "",
        "## Shared Factor Intersections",
        "",
    ]
    for factor in graph["shared_factors"]:
        lines.append(f"- `{factor}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, required=True, help="known audit lower factor")
    parser.add_argument("--q", type=int, required=True, help="known audit upper factor")
    parser.add_argument("--radius", type=int, default=70, help="symmetric window around N")
    parser.add_argument("--out-dir", type=Path, required=True, help="output directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.p < 2 or args.q < 2 or not is_prime(args.p) or not is_prime(args.q):
        raise SystemExit("--p and --q must be prime")
    if args.radius < 1:
        raise SystemExit("--radius must be positive")
    graph = build_graph(args.p, args.q, args.radius)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "graph.json").write_text(
        json.dumps(graph, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (args.out_dir / "web.svg").write_text(render_svg(graph), encoding="utf-8")
    write_summary(args.out_dir / "summary.md", graph)


if __name__ == "__main__":
    main()
