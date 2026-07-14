#!/usr/bin/env python3
"""Witness offset w-p under the proved dynamic cutoff C(q)=max(64, ceil(0.5 log(q)^2)).

Toy offsets are computed exactly on small exemplar gaps. The curve is the theorem bound.
This does not plot a high-scale measured cloud; caption must keep that separation.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ENTRY_ID = "witness-offset-envelope"
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.data import load_exemplar_gaps, materialize_gap_field  # noqa: E402
from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import save_figure  # noqa: E402
from _common.style import ACCENT_WITNESS, FG, GOLD, GOLD_BRIGHT, MUTED, apply_library_style  # noqa: E402


def C(q: float) -> float:
    return max(64.0, math.ceil(0.5 * (math.log(q) ** 2)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()
    apply_library_style(plt)

    qs = []
    offsets = []
    labels = []
    for g in load_exemplar_gaps():
        p, q = int(g["p"]), int(g["q"])
        if q - p < 4:
            continue
        field = materialize_gap_field(p, q)
        qs.append(q)
        offsets.append(field["offset"])
        labels.append(f"{p}→{q}")

    q_line = np.geomspace(20, 1e6, 400)
    c_line = np.array([C(float(q)) for q in q_line])

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.fill_between(q_line, 0, c_line, color=GOLD, alpha=0.15, label="theorem region 0 ≤ w-p ≤ C(q)")
    ax.plot(q_line, c_line, color=GOLD_BRIGHT, linewidth=2.0, label=r"$C(q)=\max(64,\lceil 0.5\log(q)^2\rceil)$")
    ax.scatter(qs, offsets, color=ACCENT_WITNESS, s=70, zorder=5, label="toy GWR offsets (exemplars)")
    for x, y, lab in zip(qs, offsets, labels):
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(6, 6), fontsize=8, color=MUTED)
    ax.set_xscale("log")
    ax.set_xlabel("q (log scale)")
    ax.set_ylabel("witness offset w − p")
    ax.set_title("Bounded compression: selected-witness offset under the proved envelope")
    ax.set_ylim(0, max(80, max(offsets) + 10))
    ax.grid(True, which="both", alpha=0.35)
    ax.legend(loc="upper left")
    fig.text(
        0.5,
        0.01,
        "Boundary: bounds w−p, not raw gap size q−p. Toy points are pedagogical; high-scale audit clouds are separate.",
        ha="center",
        color=MUTED,
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path = save_figure(
        fig,
        args.out_id,
        meta={
            "kind": "theorem-envelope-plus-toy-points",
            "bound": "C(q)=max(64, ceil(0.5*log(q)^2))",
            "regime": "toy exemplar offsets only under theorem curve",
        },
        repo_root=REPO_ROOT,
    )
    plt.close(fig)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
