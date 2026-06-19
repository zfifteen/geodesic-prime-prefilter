#!/usr/bin/env python3
"""Dispatch one hourly square-branch research job and update the ledger."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

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
LEDGER_PATH = ROOT / "research" / "04-bounded-compression" / "docs" / "square_branch_hourly.md"
TASK_BRANCH = "codex/hourly-square-branch"
FIRST_LAUNCH_BASE_BRANCH = "origin/main"
NEEDS_GROK_EXIT = 2


def python_bin() -> str:
    """Return the project Python interpreter."""
    return os.environ.get("PYTHON_BIN", "python3")


def resolve_command(command: list[str]) -> list[str]:
    """Map queued commands onto the configured Python interpreter."""
    if command and command[0] == "python3":
        return [python_bin(), *command[1:]]
    return command


def ensure_tracked_clean() -> None:
    """Abort when tracked files are dirty; allow untracked paths."""
    status = run_git("status", "--porcelain", "--untracked-files=no")
    if status:
        raise RuntimeError("hourly relay requires a clean tracked git worktree")


def prepare_hourly_branch(branch_name: str, first_launch_base_branch: str) -> None:
    """Fetch origin and move onto the relay branch, keeping in-progress edits."""
    run_git("fetch", "origin")
    remote_branch = f"origin/{branch_name}"
    local_exists = subprocess.run(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        cwd=ROOT,
    ).returncode == 0
    if remote_branch_exists(remote_branch):
        if local_exists:
            run_git("checkout", branch_name)
        else:
            run_git("checkout", "-b", branch_name, remote_branch)
        run_git("merge", "--ff-only", remote_branch)
        return
    if local_exists:
        run_git("checkout", branch_name)
        return
    run_git("checkout", "-b", branch_name, first_launch_base_branch)


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


def format_deterministic_result(item: dict[str, Any], completed: subprocess.CompletedProcess[str]) -> str:
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
    status: str,
    artifacts: list[str],
    next_step: str,
) -> None:
    """Append one hourly ledger block."""
    block = f"""
## {utc_timestamp_iso()} run

Mechanism:
{mechanism}

Method:
{method}

Result:
{result}

Status:
{status}

Artifacts:
{'; '.join(artifacts)}

Next step:
{next_step}
"""
    with LEDGER_PATH.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(block)


def commit_artifacts(paths: list[Path], message: str) -> str:
    """Commit relay artifacts on the task branch; push when possible."""
    prepare_hourly_branch(TASK_BRANCH, FIRST_LAUNCH_BASE_BRANCH)
    run_git("add", *[str(path.relative_to(ROOT)) for path in paths])
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
    return sha


def dispatch_deterministic(item: dict[str, Any]) -> int:
    """Run a deterministic queue item end-to-end."""
    command = resolve_command([str(part) for part in item["command"]])
    completed = run_command(command)
    pytest_cmd = resolve_command([str(part) for part in item.get("pytest", [])])
    pytest_completed = run_command(pytest_cmd) if pytest_cmd else None

    status = "ADVANCE"
    if completed.returncode != 0:
        status = "FAILED"
    elif pytest_completed is not None and pytest_completed.returncode != 0:
        status = "FAILED"

    result = format_deterministic_result(item, completed)
    if pytest_completed is not None:
        result += (
            f"\n\npytest exit code: {pytest_completed.returncode}\n"
            f"```\n{(pytest_completed.stdout + pytest_completed.stderr).strip()[-2000:]}\n```"
        )

    artifacts = [str(part) for part in item["command"]]
    if item.get("summary_json"):
        artifacts.append(item["summary_json"])

    append_ledger_block(
        mechanism=item["mechanism"],
        method="deterministic dispatch: " + " ".join(command),
        result=result,
        status=status,
        artifacts=artifacts,
        next_step=item.get("next_step", "Advance queue."),
    )

    commit_paths = [
        QUEUE_PATH,
        LEDGER_PATH,
        ROOT / "research" / "00-index" / "continuity" / "ACTIVE_TARGET.md",
    ]
    summary_rel = item.get("summary_json")
    if summary_rel:
        commit_paths.append(ROOT / summary_rel)
        output_dir = (ROOT / summary_rel).parent
        frontier = output_dir / "square_branch_dynamic_cutoff_search_frontier.csv"
        if frontier.exists():
            commit_paths.append(frontier)

    sha = commit_artifacts(
        commit_paths,
        f"hourly square-branch: {item['id']} ({status.lower()})",
    )
    print(f"hourly-dispatch: item={item['id']} status={status} commit={sha}")
    return 0 if status == "ADVANCE" else 1


def dispatch_grok(item: dict[str, Any], queue: dict[str, Any], executed_index: int) -> int:
    """Materialize the analytic job context for the Grok activation."""
    payload = {
        "activated_at": utc_timestamp_iso(),
        "executed_queue_index": executed_index,
        "next_queue_index": int(queue["index"]),
        "job": item,
        "ledger_path": str(LEDGER_PATH.relative_to(ROOT)),
        "task_branch": TASK_BRANCH,
    }
    write_json(CURRENT_JOB_PATH, payload)
    sha = commit_artifacts(
        [QUEUE_PATH, CURRENT_JOB_PATH],
        f"hourly square-branch: queue {item['id']} (grok handoff)",
    )
    print(f"hourly-dispatch: item={item['id']} needs_grok=1 commit={sha}")
    return NEEDS_GROK_EXIT


def main() -> int:
    """Dispatch exactly one hourly job."""
    ensure_tracked_clean()
    queue = load_queue()
    executed_index = int(queue["index"])
    item = current_item(queue)
    advance_queue_index(queue)

    if item.get("type") == "grok":
        return dispatch_grok(item, queue, executed_index)

    exit_code = dispatch_deterministic(item)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())