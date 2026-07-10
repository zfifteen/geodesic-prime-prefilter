"""Boundary checks: inference must not import forbidden classical selectors."""

from __future__ import annotations

import ast
from pathlib import Path

# Inference modules under rsa-v3 that must stay clean.
INFERENCE_MODULES = (
    "resolver.py",
    "gwr_carrier_closure.py",
    "structural_certificate.py",
    "verifier.py",
    "residual.py",
    "run_resolver.py",
)

FORBIDDEN_IMPORT_NAMES = frozenset(
    {
        "sympy",
        "isprime",
        "nextprime",
        "primerange",
        "factorint",
        "gcd",
        "miller_rabin",
        "ecpp",
    }
)

FORBIDDEN_ATTR_CALLS = frozenset(
    {
        "isprime",
        "nextprime",
        "factorint",
        "gcd",
        "miller_rabin",
    }
)

# Names that may appear in comments/docs of verifier error messages are fine;
# we only scan AST import and call nodes.


def scan_file(path: Path) -> list[str]:
    """Return list of boundary violations in one Python file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    violations: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root in FORBIDDEN_IMPORT_NAMES or alias.name in FORBIDDEN_IMPORT_NAMES:
                    violations.append(f"{path.name}: import {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            root = mod.split(".")[0]
            if root in FORBIDDEN_IMPORT_NAMES or mod in FORBIDDEN_IMPORT_NAMES:
                violations.append(f"{path.name}: from {mod} import ...")
            for alias in node.names:
                if alias.name in FORBIDDEN_IMPORT_NAMES:
                    violations.append(f"{path.name}: from {mod} import {alias.name}")
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_ATTR_CALLS:
                violations.append(f"{path.name}: call {func.id}()")
            elif isinstance(func, ast.Attribute) and func.attr in FORBIDDEN_ATTR_CALLS:
                violations.append(f"{path.name}: call ...{func.attr}()")
    return violations


def scan_inference_tree(root: Path | None = None) -> list[str]:
    """Scan all A1 inference modules for forbidden classical selectors."""
    base = root or Path(__file__).resolve().parent
    violations: list[str] = []
    for name in INFERENCE_MODULES:
        path = base / name
        if path.exists():
            violations.extend(scan_file(path))
    return violations
