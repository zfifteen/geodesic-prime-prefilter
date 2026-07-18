#!/usr/bin/env python3
"""Post PGS Lean heartbeat summary to #Prime-Gap-Structure (idempotent-ish)."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_BASE = os.environ.get("RC_BASE", "http://127.0.0.1:3000")
DEFAULT_SECRETS = Path.home() / ".grok" / "agency" / "secrets" / "rocketchat.env"
DEFAULT_CHANNEL = os.environ.get("PGS_LEAN_HB_RC_CHANNEL", "Prime-Gap-Structure")
DEFAULT_ROOM_ID = os.environ.get("PGS_LEAN_HB_ROOM_ID", "6a4f9a42b0e299fde39d6a14")
DEFAULT_LAST_RUN = Path(
    os.environ.get(
        "PGS_LEAN_HB_LAST_RUN",
        str(Path.home() / "logs" / "pgs-lean-heartbeat" / "last_run.json"),
    )
)
DEFAULT_POST_STATE = Path(
    os.environ.get(
        "PGS_LEAN_HB_RC_STATE",
        str(Path.home() / "logs" / "pgs-lean-heartbeat" / "last_rc_post.json"),
    )
)


def load_env(path: Path) -> dict[str, str]:
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
    data = None if body is None else json.dumps(body).encode()
    headers = {"Content-Type": "application/json"}
    if token and uid:
        headers["X-Auth-Token"] = token
        headers["X-User-Id"] = uid
    req = urllib.request.Request(f"{base}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def rest_login(base: str, username: str, password: str) -> tuple[str, str]:
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


def resolve_operator_auth(base: str, secrets: dict[str, str]) -> tuple[str, str]:
    token = (
        secrets.get("ROCKETCHAT_OPERATOR_TOKEN")
        or secrets.get("ROCKETCHAT_BOT_TOKEN")
        or ""
    ).strip()
    uid = (
        secrets.get("ROCKETCHAT_OPERATOR_USER_ID")
        or secrets.get("ROCKETCHAT_BOT_USER_ID")
        or ""
    ).strip()
    if token and uid:
        return token, uid
    user = (secrets.get("ROCKETCHAT_OPERATOR_USERNAME") or "hermes").strip()
    password = secrets.get("ROCKETCHAT_OPERATOR_PASSWORD") or ""
    if not password:
        raise RuntimeError("no operator token/uid or password in secrets")
    return rest_login(base, user, password)


def post_message(base: str, token: str, uid: str, room_id: str, text: str) -> str:
    payload = http_api(
        "POST",
        "/api/v1/chat.postMessage",
        base=base,
        token=token,
        uid=uid,
        body={"roomId": room_id, "text": text},
    )
    msg = payload.get("message") or {}
    mid = msg.get("_id")
    if not mid:
        raise RuntimeError(f"postMessage missing _id: {payload}")
    return str(mid)


def build_text(last_run: dict[str, Any], *, disabled: bool = False) -> str:
    when = last_run.get("completed_at") or last_run.get("activated_at") or ""
    if disabled:
        reason = last_run.get("disable_reason") or "goal/state"
        return (
            f"**PGS Lean heartbeat — DISABLED** ({when or 'now'})\n\n"
            f"Reason: {reason}\n"
            f"Label `com.velocityworks.pgs-lean-heartbeat` bootout attempted.\n"
            f"Re-enable only with principal ask + state `enabled: true`."
        )
    summary = (last_run.get("rc_summary") or last_run.get("unit_done") or "").strip()
    next_step = (last_run.get("next_step") or "").strip()
    handoffs = (last_run.get("peer_handoffs") or "").strip()
    status = (last_run.get("ops_status") or "OK").strip()
    lines = [
        f"**PGS Lean hourly heartbeat** ({when or 'now'}) · status `{status}`",
        "",
    ]
    if summary:
        lines.append(summary)
        lines.append("")
    if handoffs:
        lines.append(handoffs)
        lines.append("")
    if next_step:
        lines.append(f"Next: {next_step}")
        lines.append("")
    lines.append("_launchd `com.velocityworks.pgs-lean-heartbeat` · hourly · auto-off on DoD/DONE_")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    last_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LAST_RUN
    disabled = os.environ.get("PGS_LEAN_HB_DISABLED_POST", "").strip() in {"1", "true", "yes"}
    if not last_path.is_file() and not disabled:
        print(f"missing last_run: {last_path}", file=sys.stderr)
        return 1
    last_run: dict[str, Any] = {}
    if last_path.is_file():
        last_run = json.loads(last_path.read_text(encoding="utf-8"))
    text = build_text(last_run, disabled=disabled)
    digest = hashlib.sha256(text.encode()).hexdigest()
    if DEFAULT_POST_STATE.is_file():
        try:
            prev = json.loads(DEFAULT_POST_STATE.read_text(encoding="utf-8"))
            if prev.get("sha256") == digest:
                print("skip duplicate rc body")
                return 0
        except Exception:
            pass
    secrets = load_env(Path(os.environ.get("RC_SECRETS", str(DEFAULT_SECRETS))))
    base = os.environ.get("RC_BASE", DEFAULT_BASE).rstrip("/")
    token, uid = resolve_operator_auth(base, secrets)
    room_id = os.environ.get("PGS_LEAN_HB_ROOM_ID", DEFAULT_ROOM_ID).strip()
    mid = post_message(base, token, uid, room_id, text)
    DEFAULT_POST_STATE.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_POST_STATE.write_text(
        json.dumps(
            {
                "sha256": digest,
                "mid": mid,
                "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "channel": DEFAULT_CHANNEL,
                "room_id": room_id,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"posted mid={mid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
