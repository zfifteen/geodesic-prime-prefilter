#!/usr/bin/env python3
"""Copy committed GWR story figure into library out/ (legacy wrap)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ENTRY_ID = "gwr-figure-01-exemplar-gap-profiles"
LEGACY_REL = Path("research/02-gwr-dni/story/story/plots/figure_01_exemplar_gap_profiles.png")
HERE = Path(__file__).resolve().parent
LIBRARY_ROOT = HERE.parents[1]
if str(LIBRARY_ROOT) not in sys.path:
    sys.path.insert(0, str(LIBRARY_ROOT))

from _common.paths import REPO_ROOT  # noqa: E402
from _common.render import copy_legacy_asset  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-id", default=ENTRY_ID)
    args = parser.parse_args()
    src = REPO_ROOT / LEGACY_REL
    path = copy_legacy_asset(
        src,
        args.out_id,
        meta={"legacy_rel": str(LEGACY_REL), "story_figure": "figure_01"},
        repo_root=REPO_ROOT,
    )
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
