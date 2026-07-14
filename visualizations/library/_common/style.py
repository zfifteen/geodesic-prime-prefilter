"""Matplotlib theme for scientific library plots.

Editorial noir plates for the public course live under website/.
Library demos may use this clearer scientific theme while keeping a dark base.
"""

from __future__ import annotations

from typing import Any

# Shared palette (aligned with website STYLE_BIBLE, readable axes)
BG = "#0e0e10"
FG = "#e8e4d9"
MUTED = "#9a9588"
GOLD = "#c9a962"
GOLD_BRIGHT = "#e0c47a"
GRAPHITE = "#2a2a30"
ACCENT_PRIME = "#e0c47a"
ACCENT_WITNESS = "#ff6b5a"
ACCENT_D4 = "#7ec8e3"
ACCENT_HIGH_D = "#5a5a66"
GRID = "#2a2a30"


def apply_library_style(plt_module: Any) -> None:
    """Apply rcParams for library demos."""
    plt_module.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "savefig.facecolor": BG,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": FG,
            "text.color": FG,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "grid.color": GRID,
            "grid.alpha": 0.55,
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "semibold",
            "figure.titlesize": 14,
            "legend.facecolor": GRAPHITE,
            "legend.edgecolor": MUTED,
            "legend.labelcolor": FG,
        }
    )


def d_color(d: int) -> str:
    if d == 2:
        return ACCENT_PRIME
    if d == 4:
        return ACCENT_D4
    if d <= 6:
        return GOLD
    return ACCENT_HIGH_D
