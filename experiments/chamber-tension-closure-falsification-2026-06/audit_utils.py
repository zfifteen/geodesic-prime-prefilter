"""Audit helpers for the chamber-tension-closure experiment."""

from __future__ import annotations

import ast
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
            if isinstance(op, (ast.Eq, ast.NotEq, ast.LtE, ast.Lt)):
                violations.append(
                    f"{path}:{node.lineno}: forbidden tau selection compare"
                )
                break
            if isinstance(op, ast.GtE):
                violations.append(
                    f"{path}:{node.lineno}: forbidden tau selection compare"
                )
                break
    return violations


def elimination_slice_violations(probe_path: Path) -> list[str]:
    """Scan classify_candidate and eliminate_candidates bodies only."""
    import importlib.util

    gate_path = (
        probe_path.parent / "forbidden_dependency_gate.py"
    )
    spec = importlib.util.spec_from_file_location("forbidden_gate", gate_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load gate from {gate_path}")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    source = probe_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(probe_path))
    violations: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in {
            "classify_candidate",
            "eliminate_candidates",
        }:
            segment = ast.get_source_segment(source, node) or ""
            temp = probe_path.parent / f".audit_{node.name}.py"
            temp.write_text(segment + "\n", encoding="utf-8")
            try:
                violations.extend(gate.forbidden_dependency_violations(temp))
            finally:
                temp.unlink(missing_ok=True)
    return violations