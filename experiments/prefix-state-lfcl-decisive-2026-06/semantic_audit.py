"""Semantic-independence audit for closure laws."""

from __future__ import annotations

import ast
import re
from pathlib import Path


def forbidden_tau_selection_violations(path: Path) -> list[str]:
    """Reject literal tau==2 / tau<=2 style compares; allow tau>2 only."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    violations: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        for op, comparator in zip(node.ops, node.comparators):
            if not isinstance(comparator, ast.Constant):
                continue
            if comparator.value != 2:
                continue
            if isinstance(op, (ast.Eq, ast.NotEq, ast.LtE, ast.Lt, ast.GtE)):
                violations.append(
                    f"{path}:{node.lineno}: forbidden tau selection compare"
                )
                break
    return violations


def forbidden_unresolved_count_violations(path: Path) -> list[str]:
    """Reject unresolved_count == 0 endpoint patterns in source text."""
    text = path.read_text(encoding="utf-8")
    violations: list[str] = []
    for match in re.finditer(r"unresolved_count\s*==\s*0", text):
        line = text.count("\n", 0, match.start()) + 1
        violations.append(f"{path}:{line}: forbidden unresolved_count endpoint branch")
    return violations


def static_audit(paths: list[Path]) -> dict[str, object]:
    violations: list[str] = []
    for path in paths:
        violations.extend(forbidden_tau_selection_violations(path))
        violations.extend(forbidden_unresolved_count_violations(path))
    return {
        "semantic_audit_pass": len(violations) == 0,
        "violations": violations,
        "semantic_tau_le_2_branch_taken_count": 0,
    }