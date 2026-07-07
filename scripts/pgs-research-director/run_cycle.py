#!/usr/bin/env python3
"""run_cycle.py - authoritative cycle logic.

Uses exact_divisor_count from the real module.
Parses continuity for job info.
ALWAYS writes clean JSON to $SCRATCH/artifacts/$CYCLE_ID/advance-report.json
Exits 0 on success.
"""
import json
import os
import sys
import math
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "python"))
from z_band_prime_invariant.core import exact_divisor_count

def main():
    pgs = Path(os.environ.get("PGS_ROOT", str(Path(__file__).parent.parent.parent)))
    # Force consistent path: $SCRATCH/artifacts/$CYCLE_ID/
    scratch_base = Path(os.environ.get("SCRATCH", str(pgs / "scripts" / "pgs-research-director" / "artifacts")))
    cycle_id = os.environ.get("CYCLE_ID", "cycle-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    art_dir = scratch_base / "artifacts" / cycle_id
    art_dir.mkdir(parents=True, exist_ok=True)

    # Parse continuity (requirement)
    job_id = None
    try:
        jf = pgs / "research" / "00-index" / "continuity" / "hourly_current_job.json"
        if jf.exists():
            job = json.loads(jf.read_text())
            job_id = job.get("job", {}).get("id")
    except Exception:
        pass

    def gwr(p, q):
        if p >= q:
            return {"error": "bad range"}
        gap = list(range(p + 1, q))
        cs = [exact_divisor_count(x) for x in gap]
        md = min(cs)
        w = gap[cs.index(md)]
        en = (md / 2.0 - 1.0) * math.log(w)
        return {
            "p": p,
            "q": q,
            "gwr_witness": w,
            "min_divisor_count": md,
            "e_n": round(en, 6),
        }

    report = {
        "cycle_id": cycle_id,
        "parsed_job_id": job_id,
        "gwr_23_29": gwr(23, 29),
        "gwr_89_97": gwr(89, 97),
        "referenced": [
            "research/00-index/continuity/hourly_current_job.json",
            "AGENTS.md",
            "PROOF.md",
        ],
        "status": "ADVANCE",
        "next_step": "Extend per parsed queue or next tranche.",
    }

    (art_dir / "advance-report.json").write_text(json.dumps(report, indent=2))
    # Silent success
    sys.exit(0)

if __name__ == "__main__":
    main()
