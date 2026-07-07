"""Remainder Research Super Team — named lane agents for multi-lane investigation.

Each agent owns one remainder lane, its collector script, and output contract.
The orchestrator (`run_investigation.py`) dispatches agents as subprocesses and
records per-agent status in SUPER_TEAM_RUN.json.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
LANE_DIR = HERE / "lane_collectors"


@dataclass(frozen=True)
class LaneAgent:
    """One investigative agent in the Remainder Research Super Team."""

    agent_id: str
    lane_name: str
    role: str
    collector_script: str
    output_artifact: str
    repro_command: str


def all_lane_agents() -> list[LaneAgent]:
    """Return the canonical six-lane super-team roster."""
    return [
        LaneAgent(
            agent_id="interior_rnm",
            lane_name="interior_R_n_M",
            role="Stream interior remainder vectors R(n,M_v1) and placement correlations",
            collector_script="research/remainders/collect_remainder_stats.py",
            output_artifact="research/remainders/output/1.5e6/raw_records.jsonl",
            repro_command=(
                "python research/remainders/collect_remainder_stats.py "
                "--max-p 1500000 --output-dir research/remainders/output/1.5e6/"
            ),
        ),
        LaneAgent(
            agent_id="super_signal_status",
            lane_name="gwr_super_signal",
            role="Record epistemic status of Twin-Prime Resonance (G2); no PROOF edits",
            collector_script="research/remainders/run_investigation.py (inline)",
            output_artifact="research/remainders/correlations/investigation/super_signal_status.json",
            repro_command="see docs/proof-enhancements/goals.md G2",
        ),
        LaneAgent(
            agent_id="endpoint_mask",
            lane_name="endpoint_residue_mask",
            role="Measure wheel-open mask resolution and q mod state on GWR chain",
            collector_script="research/remainders/lane_collectors/endpoint_residue_probe.py",
            output_artifact=(
                "research/remainders/correlations/investigation/endpoint_residue_probe_fresh.json"
            ),
            repro_command=(
                "python research/remainders/lane_collectors/endpoint_residue_probe.py "
                "--start-p 10000000000037 --max-gaps 10000 "
                "--output research/remainders/correlations/investigation/endpoint_residue_probe_fresh.json"
            ),
        ),
        LaneAgent(
            agent_id="mod30_ridge",
            lane_name="left_prime_mod30_ridge",
            role="Fresh right-edge share by p mod 30; merge pinned insight_probes JSON",
            collector_script="research/remainders/lane_collectors/mod30_ridge_probe.py",
            output_artifact=(
                "research/remainders/correlations/investigation/mod30_ridge_probe_fresh.json"
            ),
            repro_command=(
                "python research/remainders/lane_collectors/mod30_ridge_probe.py "
                "--max-p 200000 "
                "--output research/remainders/correlations/investigation/mod30_ridge_probe_fresh.json"
            ),
        ),
        LaneAgent(
            agent_id="state_budget",
            lane_name="state_budget_residue_cells",
            role="Residue-matched transition pair tests (powers 12–18)",
            collector_script="research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py",
            output_artifact="research/05-state-budget/output/state_budget_residue_matched_pair_summary.json",
            repro_command="python research/05-state-budget/scripts/state_budget_residue_matched_pair_test.py",
        ),
        LaneAgent(
            agent_id="rsa_backward",
            lane_name="rsa_backward_modulus_remainder",
            role="Modulus/remainder invariant closure search on toy semiprimes",
            collector_script=(
                "research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py"
            ),
            output_artifact=(
                "research/06-cryptology-rsa/output/semiprime_branch/"
                "pgs_semiprime_backward_invariant_closure_search_summary.json"
            ),
            repro_command=(
                "python research/06-cryptology-rsa/scripts/pgs_semiprime_backward_invariant_closure_search.py "
                "--max-n 5000 --output-dir research/06-cryptology-rsa/output/semiprime_branch"
            ),
        ),
    ]


def manifest_dict() -> dict:
    """JSON-serializable roster for SUPER_TEAM_MANIFEST / SUPER_TEAM_RUN."""
    return {
        "team_name": "Remainder Research Super Team",
        "agent_count": len(all_lane_agents()),
        "agents": [asdict(a) for a in all_lane_agents()],
    }