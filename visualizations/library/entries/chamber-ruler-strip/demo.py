#!/usr/bin/env python3
"""Chamber ruler strip: primes as walls, d(n) bars, GWR witness marked."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ENTRY_ID = "chamber-ruler-strip"
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.data import load_exemplar_gaps, materialize_gap_field  # noqa: E402
from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import save_figure  # noqa: E402
from _common.style import ACCENT_WITNESS, FG, GOLD_BRIGHT, MUTED, apply_library_style, d_color  # noqa: E402


def pick_gaps():
    rows = []
    for g in load_exemplar_gaps():
        p, q = int(g["p"]), int(g["q"])
        if q - p < 4:
            continue
        rows.append(materialize_gap_field(p, q))
        if len(rows) >= 4:
            break
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()

    apply_library_style(plt)
    gaps = pick_gaps()
    fig, axes = plt.subplots(len(gaps), 1, figsize=(11, 2.2 * len(gaps)), sharex=False)
    if len(gaps) == 1:
        axes = [axes]

    for ax, field in zip(axes, gaps):
        values = field["values"]
        ds = field["divisors"]
        p, q, w = field["p"], field["q"], field["w"]
        xs = list(range(len(values)))
        colors = [d_color(d) for d in ds]
        ax.bar(xs, ds, color=colors, width=0.85, edgecolor="none")
        # endpoints
        for idx, n in enumerate(values):
            if n in (p, q):
                ax.axvline(idx, color=GOLD_BRIGHT, linewidth=1.2, alpha=0.9)
            if n == w:
                ax.scatter([idx], [ds[idx] + 0.35], color=ACCENT_WITNESS, s=48, zorder=5, marker="v")
        ax.set_ylim(0, max(ds) + 1.5)
        ax.set_ylabel("d(n)")
        ax.set_title(f"p={p} → q={q}   gap={field['gap']}   GWR w={w} (d={field['w_d']}, offset={field['offset']})")
        ax.set_xticks(xs[:: max(1, len(xs) // 12)])
        ax.set_xticklabels([str(values[i]) for i in ax.get_xticks().astype(int) if i < len(values)], rotation=0)
        ax.grid(axis="y", alpha=0.35)

    legend = [
        mpatches.Patch(color=d_color(2), label="d=2 prime wall"),
        mpatches.Patch(color=d_color(4), label="d=4"),
        mpatches.Patch(color=d_color(6), label="d=6"),
        mpatches.Patch(color=d_color(12), label="higher d"),
        mpatches.Patch(color=ACCENT_WITNESS, label="GWR witness w"),
    ]
    fig.legend(handles=legend, loc="upper right", bbox_to_anchor=(0.99, 0.995), fontsize=9)
    fig.suptitle("Chamber ruler strip: ordered gap interiors and GWR selection", color=FG, y=1.01)
    fig.tight_layout()
    path = save_figure(
        fig,
        args.out_id,
        meta={
            "kind": "scientific-demo",
            "regime": "toy exemplar gaps from fixtures/exemplars/gaps.json",
            "status": "theorem-illustration",
        },
        repo_root=REPO_ROOT,
    )
    plt.close(fig)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
