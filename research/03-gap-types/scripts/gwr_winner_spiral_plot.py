#!/usr/bin/env python3
"""Plot GWR-selected prime-gap interiors on an Ulam-style integer spiral."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap


SIDE = 151
LIMIT = SIDE * SIDE

FAMILY_ORDER = [
    "prime square",
    "prime cube",
    "even semiprime",
    "odd semiprime",
    "higher even",
    "higher odd",
]

FAMILY_COLORS = {
    "prime square": "#ffe66d",
    "prime cube": "#ffb703",
    "even semiprime": "#4ecdc4",
    "odd semiprime": "#ff6b6b",
    "higher even": "#6a8dff",
    "higher odd": "#b86cff",
}


def prime_flags(limit: int) -> list[bool]:
    flags = [True] * (limit + 1)
    flags[0] = False
    flags[1] = False
    for n in range(2, int(limit**0.5) + 1):
        if flags[n]:
            for multiple in range(n * n, limit + 1, n):
                flags[multiple] = False
    return flags


def divisor_counts(limit: int) -> list[int]:
    counts = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for multiple in range(d, limit + 1, d):
            counts[multiple] += 1
    return counts


def prime_factor_count(n: int, prime: list[bool]) -> tuple[int, int | None]:
    remaining = n
    factors = 0
    last_factor = None
    d = 2
    while d * d <= remaining:
        while remaining % d == 0:
            factors += 1
            last_factor = d
            remaining //= d
        d += 1 if d == 2 else 2
    if remaining > 1:
        factors += 1
        last_factor = remaining
    if factors == 1 and prime[n]:
        return factors, n
    return factors, last_factor


def prime_cube_root(n: int, prime: list[bool]) -> int | None:
    root = round(n ** (1.0 / 3.0))
    for candidate in range(max(2, root - 2), root + 3):
        if candidate * candidate * candidate == n and prime[candidate]:
            return candidate
    return None


def winner_family(winner: int, tau: int, prime: list[bool]) -> str:
    if tau == 3:
        root = int(winner**0.5)
        if root * root == winner and prime[root]:
            return "prime square"
    if tau == 4:
        if prime_cube_root(winner, prime) is not None:
            return "prime cube"
        factors, _ = prime_factor_count(winner, prime)
        if factors == 2:
            return "even semiprime" if winner % 2 == 0 else "odd semiprime"
    return "higher even" if winner % 2 == 0 else "higher odd"


def output_name(family: str) -> str:
    return "gwr_winner_ulam_spiral_" + family.replace(" ", "_") + ".png"


def spiral_xy(n: int) -> tuple[int, int]:
    if n == 1:
        return (0, 0)
    layer = 0
    while (2 * layer + 1) ** 2 < n:
        layer += 1
    side = 2 * layer
    maximum = (2 * layer + 1) ** 2
    offset = maximum - n
    if offset < side:
        return (layer - offset, -layer)
    if offset < 2 * side:
        return (-layer, -layer + (offset - side))
    if offset < 3 * side:
        return (-layer + (offset - 2 * side), layer)
    return (layer, layer - (offset - 3 * side))


def gwr_winners(primes: list[int], tau: list[int], prime: list[bool]) -> list[dict[str, int | str]]:
    winners = []
    for p, q in zip(primes, primes[1:]):
        interior = range(p + 1, q)
        if p + 1 >= q:
            continue
        minimum = min(tau[n] for n in interior)
        winner = next(n for n in interior if tau[n] == minimum)
        winners.append(
            {
                "p": p,
                "q": q,
                "gap": q - p,
                "winner": winner,
                "tau": minimum,
                "family": winner_family(winner, minimum, prime),
            }
        )
    return winners


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    prime = prime_flags(LIMIT)
    primes = [n for n in range(2, LIMIT + 1) if prime[n]]
    tau = divisor_counts(LIMIT)
    winners = gwr_winners(primes, tau, prime)

    half = SIDE // 2
    counts = Counter(str(row["family"]) for row in winners)

    output_paths = []
    for family in FAMILY_ORDER:
        grid = [[0 for _ in range(SIDE)] for _ in range(SIDE)]
        for n in primes:
            x, y = spiral_xy(n)
            grid[half - y][half + x] = 1
        for row in winners:
            if row["family"] != family:
                continue
            x, y = spiral_xy(int(row["winner"]))
            grid[half - y][half + x] = 2

        fig, ax = plt.subplots(figsize=(12, 12), dpi=220)
        fig.patch.set_facecolor("#0f1318")
        ax.set_facecolor("#0f1318")
        ax.imshow(
            grid,
            interpolation="nearest",
            cmap=ListedColormap(["#0f1318", "#25313d", FAMILY_COLORS[family]]),
            vmin=0,
            vmax=2,
        )
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#303945")
            spine.set_linewidth(1.3)

        ax.set_title(
            f"GWR Winner Spiral: {family.title()}",
            color="#f4f1ea",
            fontsize=21,
            pad=12,
        )
        ax.text(
            0.5,
            -0.035,
            f"Ulam coordinates through n = {LIMIT}. Highlighted cells are {family} winners selected by the leftmost minimum-divisor rule.",
            color="#b8c2cc",
            fontsize=9,
            ha="center",
            va="top",
            transform=ax.transAxes,
        )

        handles = [
            mpatches.Patch(color="#25313d", label="prime endpoint context"),
            mpatches.Patch(color=FAMILY_COLORS[family], label=f"{family}: {counts[family]}"),
        ]
        legend = ax.legend(
            handles=handles,
            loc="upper left",
            bbox_to_anchor=(0.018, 0.94),
            frameon=True,
            facecolor="#151b22",
            edgecolor="#303945",
            fontsize=8.5,
        )
        for text in legend.get_texts():
            text.set_color("#d7dde5")

        output_path = output_dir / output_name(family)
        fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close(fig)
        output_paths.append(output_path)

    for output_path in output_paths:
        print(output_path)


if __name__ == "__main__":
    main()
