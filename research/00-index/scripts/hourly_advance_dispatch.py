#!/usr/bin/env python3
"""Dispatch one hourly square-branch research job and update the ledger."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import traceback
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from hourly_delta import (  # noqa: E402
    OPS_FAILED,
    OPS_OK,
    OPS_PARTIAL,
    RESEARCH_ADVANCE,
    RESEARCH_FAILED,
    classify_deterministic,
    key_numbers_from_signature,
    summary_signature,
)
from hourly_research_relay_common import (  # noqa: E402
    ROOT as RELAY_ROOT,
    remote_branch_exists,
    run_git,
    utc_timestamp_iso,
    write_json,
)

assert ROOT == RELAY_ROOT

QUEUE_PATH = ROOT / "research" / "00-index" / "continuity" / "hourly_queue.json"
CURRENT_JOB_PATH = ROOT / "research" / "00-index" / "continuity" / "hourly_current_job.json"
BASELINE_PATH = ROOT / "research" / "00-index" / "continuity" / "hourly_baseline_signature.json"
PRIOR_SIG_PATH = ROOT / "research" / "00-index" / "continuity" / "hourly_prior_signature.json"
LEDGER_PATH = ROOT / "research" / "04-bounded-compression" / "docs" / "square_branch_hourly.md"
TASK_BRANCH = "codex/hourly-square-branch"
FIRST_LAUNCH_BASE_BRANCH = "origin/main"
NEEDS_GROK_EXIT = 2
LOG_DIR = Path(os.environ.get("LOG_DIR", str(Path.home() / "logs" / "pgs-hourly")))
LAST_RUN_PATH = LOG_DIR / "last_run.json"


def python_bin() -> str:
    """Return the project Python interpreter."""
    return os.environ.get("PYTHON_BIN", "python3")


def resolve_command(command: list[str]) -> list[str]:
    """Map queued commands onto the configured Python interpreter."""
    if command and command[0] == "python3":
        return [python_bin(), *command[1:]]
    return command


def prepare_hourly_branch(branch_name: str, first_launch_base_branch: str) -> None:
    """Move onto the relay branch inside the isolated worktree."""
    run_git("fetch", "origin")
    current = run_git("branch", "--show-current")
    remote_branch = f"origin/{branch_name}"
    local_exists = (
        subprocess.run(
            ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
            cwd=ROOT,
        ).returncode
        == 0
    )

    if current == branch_name:
        if remote_branch_exists(remote_branch):
            subprocess.run(
                ["git", "merge", "--ff-only", remote_branch],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        return

    if remote_branch_exists(remote_branch):
        if local_exists:
            run_git("checkout", branch_name)
        else:
            run_git("checkout", "-b", branch_name, remote_branch)
        subprocess.run(
            ["git", "merge", "--ff-only", remote_branch],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        return

    if local_exists:
        run_git("checkout", branch_name)
        return

    try:
        run_git("checkout", "-b", branch_name, first_launch_base_branch)
    except subprocess.CalledProcessError:
        run_git("checkout", "-b", branch_name)


def load_queue() -> dict[str, Any]:
    """Load the rotating hourly queue."""
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(queue: dict[str, Any]) -> None:
    """Persist queue index rotation."""
    QUEUE_PATH.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")


def current_item(queue: dict[str, Any]) -> dict[str, Any]:
    """Return the active queue item."""
    items = queue["items"]
    index = int(queue["index"]) % len(items)
    return items[index]


def advance_queue_index(queue: dict[str, Any]) -> None:
    """Rotate to the next queue item for the following hour."""
    queue["index"] = (int(queue["index"]) + 1) % len(queue["items"])
    save_queue(queue)


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run one command in the repo root."""
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def load_summary(path: Path) -> dict[str, Any] | None:
    """Load a JSON summary when present."""
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def load_baseline_signature() -> dict[str, Any] | None:
    """Load the frozen certified baseline signature when present."""
    if not BASELINE_PATH.exists():
        return None
    payload = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    signature = payload.get("signature")
    return signature if isinstance(signature, dict) else None


def load_prior_signature() -> dict[str, Any] | None:
    """Load the last recorded scientific signature."""
    if not PRIOR_SIG_PATH.exists():
        return None
    payload = json.loads(PRIOR_SIG_PATH.read_text(encoding="utf-8"))
    signature = payload.get("signature")
    return signature if isinstance(signature, dict) else None


def save_prior_signature(signature: dict[str, Any] | None, job_id: str) -> None:
    """Persist the latest scientific signature for future delta checks."""
    if signature is None:
        return
    write_json(
        PRIOR_SIG_PATH,
        {
            "updated_at": utc_timestamp_iso(),
            "job_id": job_id,
            "signature": signature,
        },
    )


def write_last_run(payload: dict[str, Any]) -> None:
    """Write the activation summary consumed by Rocket.Chat notify."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    write_json(LAST_RUN_PATH, payload)


def relay_code_paths() -> list[Path]:
    """Return ops files synced into the worktree that should ride with commits."""
    return [
        ROOT / "scripts" / "pgs-hourly-advance.sh",
        ROOT / "scripts" / "pgs-hourly-ensure-worktree.sh",
        ROOT / "scripts" / "pgs_hourly_rocketchat_notify.py",
        ROOT / "scripts" / "launchd" / "com.velocityworks.pgs-hourly-advance.plist",
        ROOT / "research" / "00-index" / "scripts" / "hourly_advance_dispatch.py",
        ROOT / "research" / "00-index" / "scripts" / "hourly_delta.py",
        ROOT / "research" / "00-index" / "scripts" / "hourly_research_relay_common.py",
        ROOT / "research" / "00-index" / "hourly-advance-prompt.txt",
        ROOT / "research" / "00-index" / "continuity" / "HOURLY_RELAY_CONTRACT.md",
        ROOT / "research" / "00-index" / "continuity" / "hourly_baseline_signature.json",
    ]


def format_deterministic_result(
    item: dict[str, Any],
    completed: subprocess.CompletedProcess[str],
) -> str:
    """Build a ledger Result section for deterministic jobs."""
    lines = [
        f"Command exit code: {completed.returncode}",
        f"stdout tail:\n```\n{completed.stdout.strip()[-2000:]}\n```",
    ]
    if completed.stderr.strip():
        lines.append(f"stderr tail:\n```\n{completed.stderr.strip()[-1000:]}\n```")

    summary_rel = item.get("summary_json")
    if summary_rel:
        summary = load_summary(ROOT / summary_rel)
        if summary is not None:
            max_row = summary.get("max_row") or {}
            lines.extend(
                [
                    f"tested_prime_count: {summary.get('tested_prime_count')}",
                    f"first_counterexample: {summary.get('first_counterexample')}",
                    f"max_utilization: {summary.get('max_dynamic_cutoff_utilization')}",
                    f"max_p: {max_row.get('p')}",
                    f"max_offset: {max_row.get('offset')}",
                    f"elapsed_seconds: {summary.get('elapsed_seconds')}",
                ]
            )
    return "\n".join(lines)


def append_ledger_block(
    *,
    mechanism: str,
    method: str,
    result: str,
    research_status: str,
    ops_status: str,
    delta: str,
    artifacts: list[str],
    next_step: str,
) -> None:
    """Append one hourly ledger block with dual status labels."""
    block = f"""
## {utc_timestamp_iso()} run

Mechanism:
{mechanism}

Method:
{method}

Result:
{result}

Research status:
{research_status}

Ops status:
{ops_status}

Delta:
{delta}

Artifacts:
{'; '.join(artifacts)}

Next step:
{next_step}
"""
    with LEDGER_PATH.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(block)


def _path_is_ignored(rel: str) -> bool:
    """Return True when git reports the path as ignored."""
    completed = subprocess.run(
        ["git", "check-ignore", "-q", rel],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def commit_artifacts(paths: list[Path], message: str) -> tuple[str | None, str]:
    """
    Commit relay artifacts on the task branch; push when possible.

    Returns (sha_or_none, ops_status). Ignored output files are force-added so
    measured summaries remain durable on the task branch.
    """
    try:
        prepare_hourly_branch(TASK_BRANCH, FIRST_LAUNCH_BASE_BRANCH)
        existing: list[Path] = []
        seen: set[str] = set()
        for path in paths:
            if not path.exists():
                continue
            rel = str(path.relative_to(ROOT))
            if rel in seen:
                continue
            seen.add(rel)
            existing.append(path)
        if not existing:
            return run_git("rev-parse", "HEAD"), OPS_PARTIAL

        normal: list[str] = []
        forced: list[str] = []
        for path in existing:
            rel = str(path.relative_to(ROOT))
            if _path_is_ignored(rel):
                forced.append(rel)
            else:
                normal.append(rel)

        if normal:
            run_git("add", "--", *normal)
        if forced:
            # Measured summaries live under **/output/* (gitignored by policy).
            run_git("add", "-f", "--", *forced)

        staged = run_git("diff", "--cached", "--name-only")
        if not staged.strip():
            return run_git("rev-parse", "HEAD"), OPS_OK

        run_git("commit", "-m", message)
        sha = run_git("rev-parse", "HEAD")
        push = subprocess.run(
            ["git", "push", "-u", "origin", f"HEAD:{TASK_BRANCH}"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if push.returncode != 0:
            print(
                "hourly-dispatch: push failed; kept local commit "
                f"{sha} on {TASK_BRANCH}: {push.stderr.strip()}"
            )
            return sha, OPS_PARTIAL
        return sha, OPS_OK
    except Exception as exc:  # noqa: BLE001 - surface ops failure without killing science
        print(f"hourly-dispatch: commit path failed: {exc}")
        traceback.print_exc()
        return None, OPS_FAILED


def dispatch_deterministic(item: dict[str, Any], queue: dict[str, Any]) -> int:
    """Run a deterministic queue item end-to-end with delta classification."""
    command = resolve_command([str(part) for part in item["command"]])
    completed = run_command(command)
    pytest_cmd = resolve_command([str(part) for part in item.get("pytest", [])])
    pytest_completed = run_command(pytest_cmd) if pytest_cmd else None

    command_ok = completed.returncode == 0
    pytest_ok = True if pytest_completed is None else pytest_completed.returncode == 0

    summary = None
    if item.get("summary_json"):
        summary = load_summary(ROOT / str(item["summary_json"]))
    current_sig = summary_signature(summary)
    prior_sig = load_prior_signature()
    baseline_sig = load_baseline_signature()

    research_status, delta = classify_deterministic(
        command_ok=command_ok,
        pytest_ok=pytest_ok,
        current_signature=current_sig,
        prior_signature=prior_sig,
        baseline_signature=baseline_sig,
    )

    result = format_deterministic_result(item, completed)
    if pytest_completed is not None:
        result += (
            f"\n\npytest exit code: {pytest_completed.returncode}\n"
            f"```\n{(pytest_completed.stdout + pytest_completed.stderr).strip()[-2000:]}\n```"
        )
    result += f"\n\nDelta classification: {delta}"

    artifacts = [" ".join(command)]
    if item.get("summary_json"):
        artifacts.append(str(item["summary_json"]))

    # Rotate after attempt so NO_DELTA escalates to the next frontier job.
    advance_queue_index(queue)

    append_ledger_block(
        mechanism=item["mechanism"],
        method="deterministic dispatch: " + " ".join(command),
        result=result,
        research_status=research_status,
        ops_status=OPS_OK,
        delta=delta,
        artifacts=artifacts,
        next_step=item.get("next_step", "Advance queue."),
    )

    if research_status == RESEARCH_ADVANCE and current_sig is not None:
        save_prior_signature(current_sig, item["id"])
    elif research_status == RESEARCH_FAILED:
        pass
    elif current_sig is not None and prior_sig is None:
        # Record first observation even when NO_DELTA vs baseline so later runs compare.
        save_prior_signature(current_sig, item["id"])

    commit_paths = relay_code_paths() + [
        QUEUE_PATH,
        LEDGER_PATH,
        PRIOR_SIG_PATH,
        BASELINE_PATH,
        ROOT / "research" / "00-index" / "continuity" / "ACTIVE_TARGET.md",
        ROOT / "research" / "00-index" / "continuity" / "HOURLY_RELAY_CONTRACT.md",
    ]
    if item.get("summary_json"):
        summary_path = ROOT / str(item["summary_json"])
        if summary_path.exists():
            commit_paths.append(summary_path)
            # Include sibling frontier CSV when present.
            frontier = summary_path.with_name(
                summary_path.name.replace("_summary.json", "_frontier.csv")
            )
            if frontier.exists():
                commit_paths.append(frontier)

    sha, ops_status = commit_artifacts(
        commit_paths,
        f"hourly square-branch: {item['id']} ({research_status.lower()})",
    )

    write_last_run(
        {
            "activated_at": utc_timestamp_iso(),
            "job_id": item["id"],
            "job_type": "deterministic",
            "mechanism": item.get("mechanism"),
            "research_status": research_status,
            "ops_status": ops_status,
            "delta": delta,
            "key_numbers": key_numbers_from_signature(current_sig),
            "artifacts": artifacts,
            "commit": sha,
            "task_branch": TASK_BRANCH,
            "next_step": item.get("next_step", "Advance queue."),
            "pgs_root": str(ROOT),
            "error": None,
        }
    )

    print(
        f"hourly-dispatch: item={item['id']} research={research_status} "
        f"ops={ops_status} commit={sha}"
    )
    return 0 if research_status == RESEARCH_ADVANCE else 1


def dispatch_grok(item: dict[str, Any], queue: dict[str, Any], executed_index: int) -> int:
    """Materialize the analytic job context for the Grok activation."""
    advance_queue_index(queue)
    payload = {
        "activated_at": utc_timestamp_iso(),
        "executed_queue_index": executed_index,
        "next_queue_index": int(queue["index"]),
        "job": item,
        "ledger_path": str(LEDGER_PATH.relative_to(ROOT)),
        "task_branch": TASK_BRANCH,
    }
    write_json(CURRENT_JOB_PATH, payload)
    sha, ops_status = commit_artifacts(
        relay_code_paths() + [QUEUE_PATH, CURRENT_JOB_PATH],
        f"hourly square-branch: queue {item['id']} (grok handoff)",
    )
    write_last_run(
        {
            "activated_at": utc_timestamp_iso(),
            "job_id": item["id"],
            "job_type": "grok",
            "mechanism": item.get("mechanism"),
            "research_status": "UNRESOLVED",
            "ops_status": ops_status,
            "delta": "grok analytic handoff queued; research delta pending agent completion",
            "key_numbers": {},
            "artifacts": [str(CURRENT_JOB_PATH.relative_to(ROOT))],
            "commit": sha,
            "task_branch": TASK_BRANCH,
            "next_step": item.get("next_step", "Complete grok job and ledger."),
            "pgs_root": str(ROOT),
            "error": None,
            "needs_grok": True,
        }
    )
    print(f"hourly-dispatch: item={item['id']} needs_grok=1 commit={sha}")
    return NEEDS_GROK_EXIT


def main() -> int:
    """Dispatch exactly one hourly job from the isolated worktree."""
    try:
        queue = load_queue()
        executed_index = int(queue["index"])
        item = current_item(queue)

        if item.get("type") == "grok":
            return dispatch_grok(item, queue, executed_index)

        return dispatch_deterministic(item, queue)
    except Exception as exc:  # noqa: BLE001
        write_last_run(
            {
                "activated_at": utc_timestamp_iso(),
                "job_id": None,
                "job_type": None,
                "research_status": RESEARCH_FAILED,
                "ops_status": OPS_FAILED,
                "delta": "dispatch crashed before completion",
                "key_numbers": {},
                "artifacts": [],
                "commit": None,
                "task_branch": TASK_BRANCH,
                "next_step": "Inspect hourly.log and fix dispatch.",
                "pgs_root": str(ROOT),
                "error": str(exc),
            }
        )
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
