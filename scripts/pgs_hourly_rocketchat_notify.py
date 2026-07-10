#!/usr/bin/env python3
"""Post one PGS hourly activation summary to Rocket.Chat #Prime-Gap-Structure."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE = os.environ.get("RC_BASE", "http://127.0.0.1:3000")
DEFAULT_SECRETS = Path.home() / ".grok" / "agency" / "secrets" / "rocketchat.env"
DEFAULT_CHANNEL = os.environ.get("PGS_HOURLY_RC_CHANNEL", "Prime-Gap-Structure")
DEFAULT_LAST_RUN = Path(
    os.environ.get("PGS_HOURLY_LAST_RUN", str(Path.home() / "logs" / "pgs-hourly" / "last_run.json"))
)


def load_env(path: Path) -> dict[str, str]:
    """Parse KEY=value secrets file."""
    env: dict[str, str] = {}
    if not path.is_file():
        raise FileNotFoundError(f"missing secrets: {path}")
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def http_api(
    method: str,
    path: str,
    *,
    base: str,
    token: str | None = None,
    uid: str | None = None,
    body: dict[str, Any] | None = None,
    timeout: float = 20.0,
) -> dict[str, Any]:
    """Call one Rocket.Chat REST endpoint and return JSON."""
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token and uid:
        headers["X-Auth-Token"] = token
        headers["X-User-Id"] = uid
    req = urllib.request.Request(f"{base}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def rest_login(base: str, username: str, password: str) -> tuple[str, str]:
    """Login and return (authToken, userId)."""
    payload = http_api(
        "POST",
        "/api/v1/login",
        base=base,
        body={"user": username, "password": password},
    )
    if payload.get("status") != "success":
        raise RuntimeError(f"login failed: {payload}")
    data = payload["data"]
    return data["authToken"], data["userId"]


def resolve_room_id(base: str, token: str, uid: str, channel_name: str) -> str:
    """Resolve a public channel or private group by name."""
    name = channel_name.lstrip("#")
    for api_path, list_key in (
        ("/api/v1/channels.list.joined", "channels"),
        ("/api/v1/groups.list", "groups"),
    ):
        payload = http_api("GET", api_path, base=base, token=token, uid=uid)
        for room in payload.get(list_key) or []:
            if (room.get("name") or "") == name:
                return str(room["_id"])
    # Fallback exact info endpoints.
    for api_path in (
        f"/api/v1/channels.info?roomName={name}",
        f"/api/v1/groups.info?roomName={name}",
    ):
        try:
            payload = http_api("GET", api_path, base=base, token=token, uid=uid)
        except urllib.error.HTTPError:
            continue
        room = payload.get("channel") or payload.get("group")
        if room and room.get("_id"):
            return str(room["_id"])
    raise RuntimeError(f"room not found: {channel_name}")


def format_message(run: dict[str, Any]) -> str:
    """Render the fixed hourly scoreboard message."""
    numbers = run.get("key_numbers") or {}
    number_bits = []
    for key in (
        "min_prime",
        "max_prime",
        "tested_prime_count",
        "first_counterexample",
        "max_utilization",
        "max_p",
        "max_offset",
    ):
        if key in numbers and numbers[key] is not None:
            number_bits.append(f"{key}={numbers[key]}")
    numbers_line = ", ".join(number_bits) if number_bits else "none"
    artifacts = run.get("artifacts") or []
    artifacts_line = "; ".join(str(item) for item in artifacts[:4]) if artifacts else "none"
    commit = run.get("commit") or "none"
    branch = run.get("task_branch") or "codex/hourly-square-branch"
    error = run.get("error")
    lines = [
        f"PGS hourly · {run.get('activated_at') or 'unknown-time'}",
        f"Job: {run.get('job_id') or 'none'} · type: {run.get('job_type') or 'none'}",
        f"Research: {run.get('research_status') or 'UNKNOWN'}",
        f"Ops: {run.get('ops_status') or 'UNKNOWN'}",
        f"Delta: {run.get('delta') or 'none'}",
        f"Key numbers: {numbers_line}",
        f"Artifacts: {artifacts_line}",
        f"Next: {run.get('next_step') or 'none'}",
        f"Branch: {branch} @ {commit}",
    ]
    if error:
        lines.append(f"Error: {error}")
    return "\n".join(lines)


def post_message(base: str, token: str, uid: str, room_id: str, text: str) -> str:
    """Post as the authenticated user and return message id."""
    payload = http_api(
        "POST",
        "/api/v1/chat.postMessage",
        base=base,
        token=token,
        uid=uid,
        body={"roomId": room_id, "text": text},
    )
    if not payload.get("success"):
        raise RuntimeError(f"chat.postMessage failed: {payload}")
    mid = (payload.get("message") or {}).get("_id")
    return str(mid) if mid else ""


def main(argv: list[str] | None = None) -> int:
    """Load last_run.json and post to Rocket.Chat. Never raises to shell by default."""
    argv = argv if argv is not None else sys.argv[1:]
    last_run_path = Path(argv[0]) if argv else DEFAULT_LAST_RUN
    base = os.environ.get("RC_BASE", DEFAULT_BASE)
    secrets_path = Path(os.environ.get("ROCKETCHAT_SECRETS", str(DEFAULT_SECRETS)))
    channel = os.environ.get("PGS_HOURLY_RC_CHANNEL", DEFAULT_CHANNEL)

    try:
        if not last_run_path.is_file():
            run = {
                "activated_at": "unknown",
                "job_id": None,
                "job_type": None,
                "research_status": "FAILED",
                "ops_status": "FAILED",
                "delta": f"missing last_run file: {last_run_path}",
                "key_numbers": {},
                "artifacts": [],
                "commit": None,
                "next_step": "Inspect hourly wrapper.",
                "error": f"missing {last_run_path}",
            }
        else:
            run = json.loads(last_run_path.read_text(encoding="utf-8"))

        text = format_message(run)
        secrets = load_env(secrets_path)
        token, uid = rest_login(
            base,
            secrets["ROCKETCHAT_OPERATOR_USERNAME"],
            secrets["ROCKETCHAT_OPERATOR_PASSWORD"],
        )
        room_id = resolve_room_id(base, token, uid, channel)
        mid = post_message(base, token, uid, room_id, text)
        print(f"pgs-hourly-rc: posted to #{channel} msg_id={mid}")
        return 0
    except Exception as exc:  # noqa: BLE001 - notify must not kill research hours
        print(f"pgs-hourly-rc: notify failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
