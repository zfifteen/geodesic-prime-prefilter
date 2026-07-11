#!/usr/bin/env python3
"""Offline unit tests for the PGS Quartet hard gate (no Grok TUI required)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

GATE = Path(__file__).resolve().parents[1] / "bin" / "pgs_quartet_gate.py"
PGS_CWD = "/Users/velocityworks/IdeaProjects/prime-gap-structure/research/19-rh-corpus"
OTHER_CWD = "/tmp/not-the-project"


def run_gate(event: str, payload: dict, env_extra: dict | None = None) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["GROK_HOOK_EVENT"] = event
    env["GROK_SESSION_ID"] = payload.get("sessionId", "test-session")
    env["GROK_WORKSPACE_ROOT"] = payload.get("workspaceRoot", payload.get("cwd", PGS_CWD))
    # Isolate state root via HOME override.
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        [sys.executable, str(GATE)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def decision(stdout: str) -> dict:
    if not stdout:
        return {}
    # Last JSON line wins.
    line = stdout.splitlines()[-1]
    return json.loads(line)


class QuartetGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = self.tmp.name
        self.env = {"HOME": self.home}

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_outside_project_allows(self) -> None:
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "s-out",
                "cwd": OTHER_CWD,
                "workspaceRoot": OTHER_CWD,
                "toolName": "read_file",
                "toolInput": {"target_file": "x"},
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")

    def test_blocks_read_before_quartet(self) -> None:
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "s1",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "read_file",
                "toolInput": {"target_file": "AGENTS.md"},
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        d = decision(out)
        self.assertEqual(d.get("decision"), "deny")
        self.assertIn("pgs-implementer", d.get("reason", ""))

    def test_allows_spawn_of_required_type(self) -> None:
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "s2",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "spawn_subagent",
                "toolInput": {
                    "subagent_type": "pgs-auditor",
                    "prompt": "audit",
                    "description": "Audit draft",
                },
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")

    def test_denies_wrong_spawn_type_before_complete(self) -> None:
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "s3",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "spawn_subagent",
                "toolInput": {
                    "subagent_type": "explore",
                    "prompt": "look around",
                    "description": "Explore",
                },
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "deny")

    def test_full_quartet_unlocks_tools(self) -> None:
        sid = "s4"
        for role in (
            "pgs-implementer",
            "pgs-auditor",
            "pgs-verifier",
            "pgs-scribe",
        ):
            code, out, err = run_gate(
                "post_tool_use",
                {
                    "sessionId": sid,
                    "cwd": PGS_CWD,
                    "workspaceRoot": PGS_CWD,
                    "toolName": "spawn_subagent",
                    "toolInput": {"subagent_type": role, "prompt": "x", "description": role},
                },
                self.env,
            )
            self.assertEqual(code, 0, err)
            self.assertEqual(out, "")

        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": sid,
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "read_file",
                "toolInput": {"target_file": "AGENTS.md"},
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")

    def test_new_user_turn_resets_ledger(self) -> None:
        sid = "s5"
        for role in (
            "pgs-implementer",
            "pgs-auditor",
            "pgs-verifier",
            "pgs-scribe",
        ):
            run_gate(
                "post_tool_use",
                {
                    "sessionId": sid,
                    "cwd": PGS_CWD,
                    "workspaceRoot": PGS_CWD,
                    "toolName": "spawn_subagent",
                    "toolInput": {"subagent_type": role},
                },
                self.env,
            )

        run_gate(
            "user_prompt_submit",
            {"sessionId": sid, "cwd": PGS_CWD, "workspaceRoot": PGS_CWD},
            self.env,
        )

        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": sid,
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "run_terminal_command",
                "toolInput": {"command": "true"},
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "deny")

    def test_subagent_start_marks_child_not_parent(self) -> None:
        """Live harness: sessionId=parent, subagentId=child on SubagentStart."""
        parent = "parent-1"
        child = "child-1"
        run_gate(
            "subagent_start",
            {
                "sessionId": parent,
                "subagentId": child,
                "subagentType": "pgs-auditor",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
            },
            self.env,
        )
        # Parent must still be gated.
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": parent,
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "read_file",
                "toolInput": {},
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "deny")

        # Child must be open (session id = child, or subagentType present).
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": child,
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "write",
                "toolInput": {"file_path": "/tmp/x", "content": "y"},
                "subagentType": "pgs-auditor",
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")

    def test_child_pretool_with_subagentType_allows(self) -> None:
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "child-live",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "run_terminal_command",
                "toolInput": {"command": "echo ok"},
                "subagentType": "pgs-verifier",
            },
            self.env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")

    def test_bypass_env(self) -> None:
        env = dict(self.env)
        env["PGS_QUARTET_BYPASS"] = "1"
        code, out, err = run_gate(
            "pre_tool_use",
            {
                "sessionId": "s-bypass",
                "cwd": PGS_CWD,
                "workspaceRoot": PGS_CWD,
                "toolName": "read_file",
                "toolInput": {},
            },
            env,
        )
        self.assertEqual(code, 0, err)
        self.assertEqual(decision(out).get("decision"), "allow")


if __name__ == "__main__":
    unittest.main()
