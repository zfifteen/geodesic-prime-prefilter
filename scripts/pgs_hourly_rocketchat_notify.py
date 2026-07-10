#!/usr/bin/env python3
"""Post one PGS hourly activation summary to Rocket.Chat #Prime-Gap-Structure."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE = os.environ.get("RC_BASE", "http://127.0.0.1:3000")
DEFAULT_SECRETS = Path.home() / ".grok" / "agency" / "secrets" / "rocketchat.env"
DEFAULT_CHANNEL = os.environ.get("PGS_HOURLY_RC_CHANNEL", "Prime-Gap-Structure")
DEFAULT_LAST_RUN = Path(
    os.environ.get("PGS_HOURLY_LAST_RUN", str(Path.home() / "logs" / "pgs-hourly" / "last_run.json"))
)
DEFAULT_POST_STATE = Path(
    os.environ.get(
        "PGS_HOURLY_RC_STATE",
        str(Path.home() / "logs" / "pgs-hourly" / "last_rc_post.json"),
    )
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


def _fmt_int(value: Any) -> str | None:
    """Format integers with thousands separators when possible."""
    if value is None:
        return None
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


def _fmt_float(value: Any, digits: int = 6) -> str | None:
    """Format a float for memo prose."""
    if value is None:
        return None
    try:
        return f"{float(value):.{digits}g}"
    except (TypeError, ValueError):
        return str(value)


def _research_headline(status: str) -> str:
    """One plain-English research outcome line."""
    mapping = {
        "ADVANCE": "Research moved forward this hour.",
        "NO_DELTA": "No new research delta (replay or unchanged signature).",
        "FAILED": "The research job failed.",
        "UNRESOLVED": "The hour ended without a decisive research result.",
    }
    return mapping.get(status, f"Research status: {status or 'UNKNOWN'}.")


def _ops_headline(status: str) -> str:
    """One plain-English ops outcome line."""
    mapping = {
        "OK": "Relay machinery completed cleanly.",
        "PARTIAL": "Research artifacts were produced, but a secondary ops step was incomplete.",
        "BLOCKED": "The hour could not start (lock or bootstrap block).",
        "FAILED": "Ops machinery failed.",
    }
    return mapping.get(status, f"Ops status: {status or 'UNKNOWN'}.")


def _job_type_phrase(job_type: Any) -> str:
    """Human label for job type."""
    if job_type == "deterministic":
        return "deterministic probe"
    if job_type == "grok":
        return "analytic (Grok) job"
    if job_type:
        return str(job_type)
    return "unspecified job"


def _short_artifact(path: Any) -> str | None:
    """Prefer short repo-relative artifact paths over full command lines."""
    text = str(path or "").strip()
    if not text:
        return None
    # Skip long command lines; keep file-like artifacts.
    if " " in text and not text.endswith((".json", ".md", ".csv", ".html", ".py")):
        return None
    markers = (
        "research/",
        "experiments/",
        "docs/",
        "scripts/",
        "lean-4/",
    )
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            return text[idx:]
    if text.endswith((".json", ".md", ".csv", ".html")):
        return text
    return None


def _regime_sentence(numbers: dict[str, Any]) -> str | None:
    """Describe the measured prime-root regime in plain English."""
    min_p = _fmt_int(numbers.get("min_prime"))
    max_p = _fmt_int(numbers.get("max_prime"))
    tested = _fmt_int(numbers.get("tested_prime_count"))
    if min_p and max_p and tested:
        return (
            f"We swept square-branch prime roots from {min_p} through {max_p} "
            f"({tested} roots tested)."
        )
    if tested:
        return f"We tested {tested} prime roots on the active surface."
    return None


def _result_sentences(numbers: dict[str, Any], research_status: str) -> list[str]:
    """Build the measured-result paragraph sentences."""
    sentences: list[str] = []
    regime = _regime_sentence(numbers)
    if regime:
        sentences.append(regime)

    counter = numbers.get("first_counterexample")
    if "tested_prime_count" in numbers or "max_prime" in numbers:
        if counter in (None, "none", ""):
            sentences.append("No counterexample to the dynamic-cutoff bound appeared in this band.")
        else:
            sentences.append(f"First counterexample observed at {counter}.")

    util = _fmt_float(numbers.get("max_utilization"))
    extremal = _fmt_int(numbers.get("max_p"))
    offset = _fmt_int(numbers.get("max_offset"))
    if util and extremal and offset:
        sentences.append(
            f"The hardest row sat at root r = {extremal} with offset D(r) = {offset} "
            f"and dynamic-cutoff utilization {util}."
        )
    elif extremal and offset:
        sentences.append(
            f"The hardest row sat at root r = {extremal} with offset D(r) = {offset}."
        )

    if research_status == "NO_DELTA" and not sentences:
        sentences.append("The scientific signature matched a prior certified surface.")
    return sentences


def _humanize_delta(delta: str, numbers: dict[str, Any]) -> str:
    """Turn common machine delta phrases into memo prose."""
    text = (delta or "").strip()
    if not text:
        return text
    lower = text.lower()
    max_prime = _fmt_int(numbers.get("max_prime"))
    if "new falsification regime through max_prime=" in lower and max_prime:
        return f"Extended the square-branch falsification surface through {max_prime}."
    if "matches frozen certified baseline" in lower:
        return "This run reproduced the frozen certified baseline surface (no new band)."
    if "matches prior hourly run" in lower:
        return "This run reproduced the previous hourly scientific signature (no new delta)."
    if "command exited nonzero" in lower:
        return "The research command exited nonzero (no new measured advance)."
    if "first counterexample observed" in lower:
        return text[0].upper() + text[1:] if text else text
    if text and text[0].islower():
        return text[0].upper() + text[1:]
    return text


def _headline_from_run(
    research_status: str,
    delta: str,
    numbers: dict[str, Any],
    mechanism: str,
) -> str:
    """Lead with the strongest plain finding for this hour."""
    if research_status == "ADVANCE" and delta:
        return delta
    if research_status == "FAILED":
        return delta or "This hour's research job failed before a new delta landed."
    if research_status == "NO_DELTA":
        return delta or "No new research delta this hour (signature replay)."
    if research_status == "UNRESOLVED":
        return delta or "The hour ended without a decisive research result."
    if mechanism:
        return mechanism
    return _research_headline(research_status)


def _residual_claim_rows(numbers: dict[str, Any]) -> list[tuple[str, str]]:
    """Extract RC* / P* style residual claim outcomes for a markdown table."""
    rows: list[tuple[str, str]] = []
    reserved = {
        "min_prime",
        "max_prime",
        "tested_prime_count",
        "first_counterexample",
        "max_utilization",
        "max_p",
        "max_offset",
        "elapsed_seconds",
        "pytest_passed",
    }
    for key in sorted(numbers.keys(), key=lambda k: str(k)):
        if key in reserved:
            continue
        value = numbers[key]
        key_s = str(key)
        # Prefer explicit residual claim labels (RC6, P1, H-210, ...).
        if key_s.startswith(("RC", "P", "H")) or key_s.endswith(("_holds", "_status")):
            rows.append((key_s, str(value)))
        elif isinstance(value, str) and value.lower() in {"holds", "falsified", "open", "failed"}:
            rows.append((key_s, value))
    return rows


def _extra_number_rows(numbers: dict[str, Any]) -> list[tuple[str, str]]:
    """Numeric companion rows that are not residual claim labels."""
    rows: list[tuple[str, str]] = []
    preferred = (
        ("tested_prime_count", "Roots tested"),
        ("min_prime", "Min prime root"),
        ("max_prime", "Max prime root"),
        ("max_utilization", "Max utilization"),
        ("max_p", "Extremal root r"),
        ("max_offset", "Extremal offset D(r)"),
        ("min_phase_gap", "Min phase gap"),
        ("oq2_offset", "o_q=2 offset"),
        ("oq4_offset", "o_q=4 offset"),
        ("oq6_offset", "o_q=6 offset"),
        ("oq2_abs_d_minus_540", "abs(D-540) at o_q=2"),
        ("oq4_abs_d_minus_540", "abs(D-540) at o_q=4"),
        ("oq6_abs_d_minus_540", "abs(D-540) at o_q=6"),
        ("pytest_passed", "Pytest passed"),
    )
    for key, label in preferred:
        if key not in numbers:
            continue
        raw = numbers[key]
        if key in {"tested_prime_count", "min_prime", "max_prime", "max_p", "max_offset"}:
            shown = _fmt_int(raw) or str(raw)
        elif key in {"max_utilization", "min_phase_gap"}:
            shown = _fmt_float(raw) or str(raw)
        else:
            shown = _fmt_int(raw) or _fmt_float(raw) or str(raw)
        rows.append((label, shown))
    return rows


def format_message(run: dict[str, Any]) -> str:
    """
    Render a thorough, structured research memo for Rocket.Chat.

    Match the operator style used in channel Q&A: plain headline, what ran,
    measured table, status separation, next pressure, not-claiming line,
    then compact artifact/branch footnotes.
    """
    research_status = str(run.get("research_status") or "UNKNOWN")
    ops_status = str(run.get("ops_status") or "UNKNOWN")
    numbers = run.get("key_numbers") or {}
    if not isinstance(numbers, dict):
        numbers = {}

    when = run.get("activated_at") or "unknown time"
    job_id = run.get("job_id") or "unspecified"
    mechanism = (run.get("mechanism") or "").strip()
    delta = _humanize_delta(str(run.get("delta") or ""), numbers)
    next_step = (run.get("next_step") or "").strip()
    branch = run.get("task_branch") or "codex/hourly-square-branch"
    commit = run.get("commit")
    commit_short = str(commit)[:12] if commit else "uncommitted"
    error = run.get("error")
    job_type = _job_type_phrase(run.get("job_type"))

    artifact_paths: list[str] = []
    for item in run.get("artifacts") or []:
        short = _short_artifact(item)
        if short and short not in artifact_paths:
            artifact_paths.append(short)
        if len(artifact_paths) >= 6:
            break

    headline = _headline_from_run(research_status, delta, numbers, mechanism)

    lines: list[str] = [
        f"**PGS hourly research memo** ({when} UTC)",
        "",
        f"**Headline:** {headline}",
        "",
        f"_Status labels: research **{research_status}** · ops **{ops_status}** "
        f"({_ops_headline(ops_status).rstrip('.')})._",
        "",
        "### What this hour actually did",
        "",
        f"**Job:** `{job_id}` ({job_type})",
    ]
    if mechanism:
        lines.append(f"**Mechanism:** {mechanism}")
    if delta and delta != headline:
        lines.append(f"**Delta:** {delta}")

    result_bits = _result_sentences(numbers, research_status)
    residual_rows = _residual_claim_rows(numbers)
    number_rows = _extra_number_rows(numbers)

    if result_bits or residual_rows or number_rows:
        lines.extend(["", "### Measured / residual result", ""])
        if result_bits:
            lines.append(" ".join(result_bits))
            lines.append("")
        if residual_rows:
            lines.extend(
                [
                    "| Residual claim | Outcome |",
                    "| --- | --- |",
                ]
            )
            for claim, outcome in residual_rows:
                lines.append(f"| `{claim}` | {outcome} |")
            lines.append("")
        if number_rows:
            lines.extend(
                [
                    "| Quantity | Value |",
                    "| --- | ---: |",
                ]
            )
            for label, value in number_rows:
                lines.append(f"| {label} | {value} |")
            lines.append("")

    lines.extend(
        [
            "### Why this matters for the schedule",
            "",
        ]
    )
    if research_status == "ADVANCE":
        lines.append(
            "This is an **hourly ADVANCE**: a new measured regime, residual claim table, "
            "or constructive proof-pressure artifact with a falsification command. "
            "It is **not** a theorem promotion. `PROOF.md` still owns proved status."
        )
    elif research_status == "NO_DELTA":
        lines.append(
            "This hour did not move the scientific signature. Replays are honest "
            "non-progress; the queue should escalate to the next frontier job."
        )
    elif research_status == "FAILED":
        lines.append(
            "The research path failed (command, missing artifact path, or pytest). "
            "Ops may still commit the ledger. Fix the path or probe before treating "
            "this as science."
        )
    else:
        lines.append(
            "The hour ended without a decisive advance or failure. Keep status "
            "labels separated; do not upgrade unresolved work to proved claims."
        )

    if next_step:
        lines.extend(["", "### Next pressure", "", next_step])

    lines.extend(
        [
            "",
            "### Not claiming",
            "",
            "- No new theorem status beyond `PROOF.md`",
            "- No RH / PNT / RSA-scale resolution from this hour alone",
            "- Audit and residual tables stay **measured** unless a separate "
            "human-approved proof promotion says otherwise",
        ]
    )

    if artifact_paths:
        lines.extend(["", "### Artifacts", ""])
        for path in artifact_paths:
            lines.append(f"- `{path}`")

    lines.extend(
        [
            "",
            "---",
            f"_Branch `{branch}` @ `{commit_short}` · ledger "
            f"`research/04-bounded-compression/docs/square_branch_hourly.md`_",
        ]
    )

    if error:
        lines.extend(["", f"**Error detail:** {error}"])

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


def acquire_post_lock(lock_path: Path, timeout_s: float = 30.0) -> bool:
    """Single-flight lock so concurrent notify processes cannot double-post."""
    import time

    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                age = time.time() - lock_path.stat().st_mtime
                if age > 120:
                    lock_path.unlink(missing_ok=True)
                    continue
            except OSError:
                pass
            time.sleep(0.2)
    return False


def release_post_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink(missing_ok=True)
    except OSError:
        pass


def message_fingerprint(text: str) -> str:
    """Stable hash of the memo body (secondary dedupe only)."""
    normalized = "\n".join(line.rstrip() for line in text.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def activation_key(run: dict[str, Any]) -> str:
    """
    Identity of one hourly activation, independent of memo wording.

    Same job_id + activated_at = same hour. Reformatting, filling completed_at
    later, or --force alone must not create a second channel post for that hour.
    (Including completed_at caused double posts when last_run was rewritten mid-hour.)
    """
    job_id = str(run.get("job_id") or "").strip() or "unknown-job"
    activated = str(run.get("activated_at") or "").strip() or "unknown-time"
    raw = f"{job_id}|{activated}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_post_state(path: Path) -> dict[str, Any]:
    """Load prior RC post state when present."""
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def save_post_state(path: Path, payload: dict[str, Any]) -> None:
    """Persist the last successful RC post identity."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Load last_run.json and post to Rocket.Chat. Never raises to shell by default."""
    argv = list(sys.argv[1:] if argv is None else argv)
    # --force only re-allows a reworded body for a *new* activation key.
    # --force-same-activation is the only escape hatch to repost the same hour
    # (emergency only; default path must never double-post).
    force_body = False
    force_same_activation = False
    if "--force-same-activation" in argv:
        force_same_activation = True
        argv = [arg for arg in argv if arg != "--force-same-activation"]
    if "--force" in argv:
        force_body = True
        argv = [arg for arg in argv if arg != "--force"]
    last_run_path = Path(argv[0]) if argv else DEFAULT_LAST_RUN
    base = os.environ.get("RC_BASE", DEFAULT_BASE)
    secrets_path = Path(os.environ.get("ROCKETCHAT_SECRETS", str(DEFAULT_SECRETS)))
    channel = os.environ.get("PGS_HOURLY_RC_CHANNEL", DEFAULT_CHANNEL)
    state_path = Path(os.environ.get("PGS_HOURLY_RC_STATE", str(DEFAULT_POST_STATE)))

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
        body_fp = message_fingerprint(text)
        act_key = activation_key(run)
        prior = load_post_state(state_path)
        lock_path = state_path.with_suffix(state_path.suffix + ".lock")

        if not acquire_post_lock(lock_path):
            print("pgs-hourly-rc: skip — could not acquire post lock (another notify running)")
            return 0
        try:
            # Re-read state under lock (another process may have just posted).
            prior = load_post_state(state_path)

            # Primary: never post twice for the same activation (same hour/job).
            prior_act = prior.get("activation_key") or ""
            if prior_act and prior_act == act_key and not force_same_activation:
                print(
                    "pgs-hourly-rc: skip already-posted activation "
                    f"(job={run.get('job_id')} activated={run.get('activated_at')} "
                    f"prior_msg={prior.get('msg_id')})"
                )
                return 0

            # Secondary: skip identical body text even across activations.
            if (
                not force_body
                and not force_same_activation
                and prior.get("fingerprint") == body_fp
            ):
                print(
                    "pgs-hourly-rc: skip duplicate memo body "
                    f"(fingerprint={body_fp[:12]} prior_msg={prior.get('msg_id')})"
                )
                return 0

            # Claim the activation *before* the network post so a crash mid-post
            # still blocks a second attempt (prefer one missed over a double).
            if not force_same_activation:
                save_post_state(
                    state_path,
                    {
                        **prior,
                        "activation_key": act_key,
                        "fingerprint": body_fp,
                        "claim_at": datetime.now(timezone.utc).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "msg_id": prior.get("msg_id"),
                        "job_id": run.get("job_id"),
                        "activated_at": run.get("activated_at"),
                        "last_run_path": str(last_run_path),
                        "status": "claiming",
                    },
                )

            secrets = load_env(secrets_path)
            token, uid = rest_login(
                base,
                secrets["ROCKETCHAT_OPERATOR_USERNAME"],
                secrets["ROCKETCHAT_OPERATOR_PASSWORD"],
            )
            room_id = resolve_room_id(base, token, uid, channel)
            mid = post_message(base, token, uid, room_id, text)
            save_post_state(
                state_path,
                {
                    "posted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fingerprint": body_fp,
                    "activation_key": act_key,
                    "msg_id": mid,
                    "channel": channel,
                    "job_id": run.get("job_id"),
                    "activated_at": run.get("activated_at"),
                    "completed_at": run.get("completed_at"),
                    "research_status": run.get("research_status"),
                    "ops_status": run.get("ops_status"),
                    "last_run_path": str(last_run_path),
                    "status": "posted",
                },
            )
            print(f"pgs-hourly-rc: posted to #{channel} msg_id={mid}")
            return 0
        finally:
            release_post_lock(lock_path)
    except Exception as exc:  # noqa: BLE001 - notify must not kill research hours
        print(f"pgs-hourly-rc: notify failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
