#!/usr/bin/env python3
"""Hard-enforce the PGS Quartet as real Grok subagents.

This is not prompt theater. On parent sessions inside prime-gap-structure, every
user turn must spawn all four required subagent types before any other tool is
allowed. Subagent child sessions are unrestricted so the team can work.

Events handled (single entrypoint; event name comes from env or stdin JSON):
  - user_prompt_submit / UserPromptSubmit: reset this turn's spawn ledger
  - subagent_start / SubagentStart: mark the *child* id (payload.subagentId),
    never the parent sessionId (harness puts parent id in sessionId)
  - post_tool_use / PostToolUse: record successful spawn_subagent role fills
  - pre_tool_use / PreToolUse: allow or deny based on ledger completeness

Harness notes (verified live on grok 0.2.93):
  - SubagentStart.sessionId is the PARENT; child is SubagentStart.subagentId
  - Child PreToolUse payloads include subagentType
  - A PreToolUse deny cancels the whole turn (cancellationCategory=HookDenied),
    so parents must spawn-first within a turn (cannot recover mid-turn after deny)

Durable off/on (checked by this hook process, not by blocked shell commands):
  1. Sticky file: ~/.grok/state/pgs-quartet-enabled  (0/off or 1/on)
     Helper: pgs-quartet on|off|status  (~/.grok/bin/pgs-quartet)
  2. Process env (must be set for the Grok CLI process, not inside a denied cmd):
       PGS_QUARTET=0 or PGS_QUARTET_ENABLED=0  -> gate off
       PGS_QUARTET=1 or PGS_QUARTET_ENABLED=1  -> gate on (overrides file)
       PGS_QUARTET_BYPASS=1                    -> emergency off
  Default when file missing and env unset: gate OFF (usability; opt in with
  `pgs-quartet on` or env=1).
"""

from __future__ import annotations

import fcntl
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

REQUIRED_TYPES: tuple[str, ...] = (
    "pgs-implementer",
    "pgs-auditor",
    "pgs-verifier",
    "pgs-scribe",
)

# Parent may only orchestrate until the four roles are filled this turn.
ORCHESTRATOR_TOOLS: frozenset[str] = frozenset(
    {
        "spawn_subagent",
        "Task",  # Claude/Cursor alias mapped by harness matcher; keep for safety
        "get_command_or_subagent_output",
        "wait_commands_or_subagents",
        "kill_command_or_subagent",
        "todo_write",
        "update_goal",
        "ask_user_question",
    }
)

PROJECT_MARKERS: tuple[str, ...] = (
    "/prime-gap-structure",
    "/prime-gap-structure/",
)

STATE_ROOT = Path.home() / ".grok" / "pgs-quartet-state"
# Sticky enable flag (cross-session). Content: 0/off or 1/on.
ENABLE_FLAG_PATH = Path.home() / ".grok" / "state" / "pgs-quartet-enabled"
SUBAGENT_KINDS = frozenset({"subagent", "subagent_resume", "subagent_fork"})

_OFF_TOKENS = frozenset({"0", "off", "false", "no", "disabled", "disable"})
_ON_TOKENS = frozenset({"1", "on", "true", "yes", "enabled", "enable"})


def _emit(obj: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(obj, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _allow(reason: str = "") -> None:
    out: dict[str, Any] = {"decision": "allow"}
    if reason:
        out["reason"] = reason
    _emit(out)


def _deny(reason: str) -> None:
    _emit({"decision": "deny", "reason": reason})


def _parse_on_off(raw: str) -> bool | None:
    """Return True/False if token is recognized, else None."""
    token = raw.strip().lower()
    if not token:
        return None
    # Accept first line / first word only (file may have comments later).
    token = token.splitlines()[0].strip().split()[0] if token.split() else token
    if token in _OFF_TOKENS:
        return False
    if token in _ON_TOKENS:
        return True
    return None


def _gate_enabled() -> tuple[bool, str]:
    """Whether the hard gate should enforce spawn requirements.

    Priority (highest first):
      1. PGS_QUARTET_BYPASS=1 -> off
      2. PGS_QUARTET_ENABLED or PGS_QUARTET process env (0/off or 1/on)
      3. Sticky file ~/.grok/state/pgs-quartet-enabled
      4. Default OFF (usability; opt in with pgs-quartet on or env=1)

    Env must be set on the Grok CLI process. Setting it only inside a blocked
    shell command does nothing (PreToolUse never runs that command).
    """
    if os.environ.get("PGS_QUARTET_BYPASS") == "1":
        return False, "PGS_QUARTET_BYPASS=1"

    for key in ("PGS_QUARTET_ENABLED", "PGS_QUARTET"):
        raw = os.environ.get(key)
        if raw is None:
            continue
        parsed = _parse_on_off(raw)
        if parsed is False:
            return False, f"{key}={raw.strip()}"
        if parsed is True:
            return True, f"{key}={raw.strip()}"

    try:
        if ENABLE_FLAG_PATH.is_file():
            content = ENABLE_FLAG_PATH.read_text(encoding="utf-8")
            parsed = _parse_on_off(content)
            if parsed is False:
                return False, f"sticky file {ENABLE_FLAG_PATH} off"
            if parsed is True:
                return True, f"sticky file {ENABLE_FLAG_PATH} on"
            # Unrecognized sticky content: treat as OFF (do not re-trap).
            return False, f"sticky file {ENABLE_FLAG_PATH} unrecognized (default off)"
    except OSError:
        pass

    return False, "default off"


def _read_stdin() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _event_name(payload: dict[str, Any]) -> str:
    env = (os.environ.get("GROK_HOOK_EVENT") or "").strip().lower()
    if env:
        return env
    for key in ("hookEventName", "event", "sessionUpdate"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip().lower()
    return ""


def _session_id(payload: dict[str, Any]) -> str:
    return (
        os.environ.get("GROK_SESSION_ID")
        or str(payload.get("sessionId") or payload.get("session_id") or "")
        or "unknown"
    )


def _paths(payload: dict[str, Any]) -> tuple[str, str]:
    cwd = str(
        payload.get("cwd")
        or os.environ.get("PWD")
        or os.getcwd()
        or ""
    )
    workspace = str(
        payload.get("workspaceRoot")
        or os.environ.get("GROK_WORKSPACE_ROOT")
        or os.environ.get("CLAUDE_PROJECT_DIR")
        or cwd
    )
    return cwd, workspace


def _in_pgs_project(cwd: str, workspace: str) -> bool:
    for path in (cwd, workspace):
        normalized = path.replace("\\", "/")
        if not normalized:
            continue
        for marker in PROJECT_MARKERS:
            if marker in normalized or normalized.rstrip("/").endswith(
                "prime-gap-structure"
            ):
                return True
    return False


def _state_path(session_id: str) -> Path:
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    safe = session_id.replace("/", "_")
    return STATE_ROOT / f"{safe}.json"


def _default_state() -> dict[str, Any]:
    return {
        "is_subagent": False,
        "turn": 0,
        "spawned": {name: False for name in REQUIRED_TYPES},
        "spawn_events": [],
        "updated_at": time.time(),
    }


def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _default_state()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _default_state()
    if not isinstance(data, dict):
        return _default_state()
    base = _default_state()
    base.update(data)
    spawned = base.get("spawned")
    if not isinstance(spawned, dict):
        spawned = {}
    base["spawned"] = {name: bool(spawned.get(name)) for name in REQUIRED_TYPES}
    base["is_subagent"] = bool(base.get("is_subagent"))
    try:
        base["turn"] = int(base.get("turn") or 0)
    except (TypeError, ValueError):
        base["turn"] = 0
    if not isinstance(base.get("spawn_events"), list):
        base["spawn_events"] = []
    return base


def _save_state(path: Path, state: dict[str, Any]) -> None:
    state = dict(state)
    state["updated_at"] = time.time()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
    # Exclusive create/write with lock so parallel PostToolUse cannot clobber.
    with open(tmp, "w", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def _with_locked_state(path: Path, mutator):
    """Load-modify-save under an advisory lock file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_suffix(".lock")
    with open(lock_path, "a+", encoding="utf-8") as lock_handle:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        state = _load_state(path)
        result = mutator(state)
        _save_state(path, state)
        return result, state


def _lookup_session_kind(session_id: str, cwd: str, workspace: str) -> str | None:
    """Best-effort read of session_kind from the on-disk session summary."""
    candidates: list[Path] = []
    home_sessions = Path.home() / ".grok" / "sessions"
    for base in (cwd, workspace):
        if not base:
            continue
        encoded = quote(base, safe="")
        candidates.append(home_sessions / encoded / session_id / "summary.json")
        # Some harness builds use a slightly different encoding; try raw slash form too.
        candidates.append(home_sessions / base.lstrip("/") / session_id / "summary.json")
    for summary in candidates:
        if not summary.is_file():
            continue
        try:
            data = json.loads(summary.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        kind = data.get("session_kind") or data.get("kind")
        if isinstance(kind, str) and kind:
            return kind
    return None


def _payload_marks_child(payload: dict[str, Any]) -> bool:
    """True when this tool/event is executing inside a subagent child.

    Live harness: child PreToolUse includes subagentType. SubagentStart includes
    subagentId while sessionId remains the parent.
    """
    if payload.get("subagentType") or payload.get("subagent_type"):
        return True
    if payload.get("subagentId") or payload.get("subagent_id"):
        # Only treat as "this invocation is the child" when the session id equals
        # the child id. SubagentStart has subagentId but sessionId=parent.
        child = str(payload.get("subagentId") or payload.get("subagent_id") or "")
        sid = str(payload.get("sessionId") or payload.get("session_id") or "")
        env_sid = os.environ.get("GROK_SESSION_ID") or ""
        if child and (sid == child or env_sid == child):
            return True
    return False


def _child_id_from_subagent_start(payload: dict[str, Any]) -> str:
    return str(payload.get("subagentId") or payload.get("subagent_id") or "").strip()


def _is_subagent_session(
    session_id: str, cwd: str, workspace: str, state: dict[str, Any], payload: dict[str, Any]
) -> bool:
    if _payload_marks_child(payload):
        return True
    if state.get("is_subagent"):
        return True
    kind = _lookup_session_kind(session_id, cwd, workspace)
    return kind in SUBAGENT_KINDS if kind else False


def _missing_roles(state: dict[str, Any]) -> list[str]:
    spawned = state.get("spawned") or {}
    return [name for name in REQUIRED_TYPES if not spawned.get(name)]


def _quartet_complete(state: dict[str, Any]) -> bool:
    return not _missing_roles(state)


def _tool_name(payload: dict[str, Any]) -> str:
    return str(payload.get("toolName") or payload.get("tool_name") or "")


def _tool_input(payload: dict[str, Any]) -> dict[str, Any]:
    raw = payload.get("toolInput") or payload.get("tool_input") or {}
    return raw if isinstance(raw, dict) else {}


def _subagent_type(tool_input: dict[str, Any]) -> str:
    value = tool_input.get("subagent_type") or tool_input.get("subagentType") or ""
    return str(value).strip()


def handle_user_prompt_submit(session_id: str, path: Path, payload: dict[str, Any]) -> None:
    # Child prompts also fire UserPromptSubmit with the child session id.
    # If this session was marked as a child, leave the ledger alone (and keep open).
    def mutator(state: dict[str, Any]) -> None:
        if state.get("is_subagent"):
            return
        # Never keep a parent stuck as "child" from older buggy gate versions.
        state["is_subagent"] = False
        state["turn"] = int(state.get("turn") or 0) + 1
        state["spawned"] = {name: False for name in REQUIRED_TYPES}
        state["spawn_events"] = []

    _with_locked_state(path, mutator)


def handle_subagent_start(payload: dict[str, Any]) -> None:
    """Mark the CHILD subagent id open. Do not touch the parent session ledger."""
    child_id = _child_id_from_subagent_start(payload)
    if not child_id:
        return
    path = _state_path(child_id)

    def mutator(state: dict[str, Any]) -> None:
        state["is_subagent"] = True

    _with_locked_state(path, mutator)


def handle_post_tool_use(session_id: str, path: Path, payload: dict[str, Any]) -> None:
    # Parent PostToolUse records fills. Child sessions must not rewrite parent ledger.
    if _payload_marks_child(payload):
        return
    tool = _tool_name(payload)
    if tool not in {"spawn_subagent", "Task"}:
        return
    role = _subagent_type(_tool_input(payload))
    if role not in REQUIRED_TYPES:
        return

    # Also mark child open if toolResult carries subagent_id (belt and suspenders).
    result = payload.get("toolResult") or {}
    result_text = ""
    if isinstance(result, dict):
        result_text = str(result.get("text") or "")
    elif isinstance(result, str):
        result_text = result
    for line in result_text.splitlines():
        if line.startswith("subagent_id:"):
            child = line.split(":", 1)[1].strip()
            if child:
                def mark_child(s: dict[str, Any]) -> None:
                    s["is_subagent"] = True

                _with_locked_state(_state_path(child), mark_child)

    def mutator(state: dict[str, Any]) -> None:
        if state.get("is_subagent"):
            # Parent ledger must never be a child marker.
            state["is_subagent"] = False
        spawned = state.setdefault("spawned", {name: False for name in REQUIRED_TYPES})
        spawned[role] = True
        events = state.setdefault("spawn_events", [])
        events.append({"role": role, "ts": time.time()})

    _with_locked_state(path, mutator)


def handle_pre_tool_use(session_id: str, path: Path, payload: dict[str, Any], cwd: str, workspace: str) -> None:
    enabled, enable_reason = _gate_enabled()
    if not enabled:
        _allow(f"quartet gate off ({enable_reason})")
        return

    state = _load_state(path)

    if _is_subagent_session(session_id, cwd, workspace, state, payload):
        # Persist child discovery on the *current* session id (the child).
        if not state.get("is_subagent"):
            def mark(s: dict[str, Any]) -> None:
                s["is_subagent"] = True

            _with_locked_state(path, mark)
        _allow("subagent session")
        return

    # Parent path: clear any stale child flag left by older gate versions.
    if state.get("is_subagent"):
        def unmark(s: dict[str, Any]) -> None:
            s["is_subagent"] = False

        _with_locked_state(path, unmark)
        state = _load_state(path)

    tool = _tool_name(payload)
    if not tool:
        _allow("missing tool name")
        return

    # Always allow pure orchestration tools. Spawn types are validated below.
    if tool in ORCHESTRATOR_TOOLS and tool not in {"spawn_subagent", "Task"}:
        _allow("orchestrator control tool")
        return

    if tool in {"spawn_subagent", "Task"}:
        role = _subagent_type(_tool_input(payload))
        if _quartet_complete(state):
            _allow("quartet complete; additional subagents permitted")
            return
        if role not in REQUIRED_TYPES:
            _deny(
                "PGS Quartet hard gate: spawn_subagent must use one of "
                f"{list(REQUIRED_TYPES)}. Got subagent_type={role!r}. "
                "Missing this turn: " + ", ".join(_missing_roles(state))
            )
            return
        if state.get("spawned", {}).get(role):
            # Allow re-spawn of same role (retry) but still incomplete overall.
            _allow(f"re-spawn allowed for {role}")
            return
        _allow(f"quartet fill: {role}")
        return

    if _quartet_complete(state):
        _allow("quartet complete for this turn")
        return

    missing = _missing_roles(state)
    _deny(
        "PGS Quartet hard gate: parent tools are blocked until all four subagents "
        "are spawned THIS USER TURN via spawn_subagent. "
        f"Required subagent_type values: {list(REQUIRED_TYPES)}. "
        f"Still missing: {missing}. "
        "SPAWN FIRST in this turn (background=true recommended). "
        "A mid-turn deny cancels the whole harness turn (HookDenied). "
        "Child subagent sessions are not gated. "
        "To disable the gate (sticky): run `pgs-quartet off` in a terminal "
        f"(writes {ENABLE_FLAG_PATH}), or set Grok process env "
        "PGS_QUARTET=0 / PGS_QUARTET_ENABLED=0 / PGS_QUARTET_BYPASS=1 "
        "(must be on the CLI process, not inside a blocked shell command)."
    )


def main() -> int:
    payload = _read_stdin()
    event = _event_name(payload)
    session_id = _session_id(payload)
    cwd, workspace = _paths(payload)
    path = _state_path(session_id)

    # Outside the PGS tree the gate is inert.
    if not _in_pgs_project(cwd, workspace):
        if event in {"pre_tool_use", "pretooluse"}:
            _allow("outside prime-gap-structure")
        return 0

    if event in {"user_prompt_submit", "userpromptsubmit", "before_submit_prompt"}:
        handle_user_prompt_submit(session_id, path, payload)
        return 0

    if event in {"subagent_start", "subagentstart"}:
        handle_subagent_start(payload)
        return 0

    if event in {"post_tool_use", "posttooluse", "after_tool_use"}:
        handle_post_tool_use(session_id, path, payload)
        return 0

    if event in {"pre_tool_use", "pretooluse", "before_tool_use"}:
        handle_pre_tool_use(session_id, path, payload, cwd, workspace)
        return 0

    # Unknown / passive events: do nothing harmful.
    if event in {"pre_tool_use", "pretooluse"}:
        _allow("unhandled event shape")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001 - fail closed on PreToolUse if possible
        # Hooks fail-open on crash; emit explicit deny when we still can.
        try:
            event = (os.environ.get("GROK_HOOK_EVENT") or "").lower()
            if event in {"pre_tool_use", "pretooluse"}:
                _deny(f"PGS Quartet gate internal error (fail-closed): {exc}")
                raise SystemExit(0)
        except Exception:
            pass
        raise
