#!/usr/bin/env python3
"""Gap+DNI public map probe: residual atlas primary (hypothesis pressure).

PGS-native only. Emits map layers 0-3 from public resolver diagnostics and
measured residual ranks. Does not trial-divide, gcd, or isprime for inference.

Status: measured probe on named fixtures; residual map remains hypothesis.
No verified/validated language (no map-family 10^18 surface).
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

# Live resolver package (run with cwd = rsa-v3 or sys.path inject).
RSA_V3 = Path(__file__).resolve().parents[1] / "live-solver" / "rsa-v3"
sys.path.insert(0, str(RSA_V3))

from gwr_carrier_closure import (  # noqa: E402
    evaluate_gwr_carrier_transport_closure,
    is_historical_false_endpoint_class,
    is_joint_cell_C1T2L1,
    residual_vector_R,
)
from residual import is_resolved_status  # noqa: E402
from resolver import git_commit, load_public_cases, resolve_cases  # noqa: E402


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
FIXTURES = RSA_V3 / "fixtures" / "regression_cases.jsonl"


def _public_s(n: int) -> int:
    return int(math.isqrt(n))


def _layer0_from_result(summary: dict, residual: dict | None, cert: dict | None) -> dict:
    n = int(summary["N"])
    return {
        "layer": 0,
        "name": "chamber_endpoint_atlas",
        "s": _public_s(n),
        "N": str(n),
        "closure_status": summary.get("closure_status"),
        "residual_code": None if residual is None else residual.get("residual_code"),
        "structural_certificate_present": cert is not None,
        "lower_certificate_present": (
            None if residual is None else residual.get("lower_certificate_present")
        ),
        "upper_certificate_present": (
            None if residual is None else residual.get("upper_certificate_present")
        ),
        "step_index": None if residual is None else residual.get("step_index"),
        "stage": None if residual is None else residual.get("stage"),
    }


def _layer1_from_vector(vector: dict | None, ledger: dict | None) -> dict:
    comps = (ledger or {}).get("components") or {}
    return {
        "layer": 1,
        "name": "gwr_dni_local_ranks",
        "component_holds": {
            k: bool(v.get("holds")) for k, v in comps.items() if isinstance(v, dict)
        },
        "residual_vector_R": None
        if vector is None
        else {
            "r_carrier": vector.get("r_carrier"),
            "r_tail": vector.get("r_tail"),
            "r_lock": vector.get("r_lock"),
            "delta_c": vector.get("delta_c"),
            "delta_t": vector.get("delta_t"),
            "boundD": vector.get("boundD"),
            "lock": vector.get("lock"),
            "gap": vector.get("gap"),
        },
    }


def _layer2_transport(vector: dict | None, n: int) -> dict:
    # Public transport residuals only (already computed ranks use floor(N/x)).
    return {
        "layer": 2,
        "name": "modulus_link_transport_field",
        "s": _public_s(n),
        "pinch_S": None if vector is None else vector.get("pinch_S"),
        "delta_c": None if vector is None else vector.get("delta_c"),
        "delta_t": None if vector is None else vector.get("delta_t"),
        "note": "pinch/delta from public floor transport; no classical gates",
    }


def _layer3_decision(
    *,
    resolved: bool,
    residual_code: str | None,
    vector: dict | None,
    decision_residual: str | None,
) -> dict:
    cell = None if vector is None else vector.get("decision_cell")
    return {
        "layer": 3,
        "name": "residual_atlas_decision",
        "map_class": "certificate" if resolved else "named_residual",
        "residual_code": residual_code,
        "decision_residual": decision_residual,
        "decision_cell": cell,
        "is_joint_cell_C1T2L1": False if vector is None else is_joint_cell_C1T2L1(vector),
    }


def _extract_vector_from_residual(residual: dict | None) -> dict | None:
    if residual is None:
        return None
    diag = residual.get("diagnostics") or {}
    ledger = diag.get("residual_component_ledger") or {}
    vec = ledger.get("residual_vector_R")
    if isinstance(vec, dict) and "r_carrier" in vec:
        return vec
    return None


def map_row_from_resolve(result: dict) -> dict[str, Any]:
    summary = result["summary"]
    residual = result.get("residual")
    cert = result.get("structural_certificate")
    n = int(summary["N"])
    vector = _extract_vector_from_residual(residual)
    ledger = None
    if residual is not None:
        ledger = (residual.get("diagnostics") or {}).get("residual_component_ledger")
    resolved = is_resolved_status(str(summary.get("closure_status") or ""))
    decision_residual = None if not isinstance(ledger, dict) else ledger.get(
        "decision_residual"
    )
    return {
        "case_id": summary["case_id"],
        "bits": summary.get("bits"),
        "N": str(n),
        "source": "live_resolver_public",
        "layers": [
            _layer0_from_result(summary, residual, cert),
            _layer1_from_vector(vector, ledger if isinstance(ledger, dict) else None),
            _layer2_transport(vector, n),
            _layer3_decision(
                resolved=resolved,
                residual_code=None if residual is None else residual.get("residual_code"),
                vector=vector,
                decision_residual=decision_residual,
            ),
        ],
        "layer4_audit_candidate_list": None,  # intentionally absent (not inference)
        "classical_inference_fields": [],  # hard empty
    }


def map_row_synthetic_tp() -> dict[str, Any]:
    """64-bit true-close pin from residual_cell unit geometry (public fields only)."""
    n64 = 10376454699372036973
    lower64 = {
        "carrier_w": 3221225471,
        "carrier_d": 4,
        "gap_offset": 12,
        "lock_carrier_offset": 10,
        "reset_endpoint": 3221225473,
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
        "tail_after_reset_offsets": [18],
        "active_count": 1,
        "unresolved_count": 6,
    }
    upper64 = {
        "carrier_w": 3221275489,
        "carrier_d": 4,
        "gap_offset": 14,
        "anchor": 3221275487,
        "active_count": 1,
        "unresolved_count": 6,
    }
    vector = residual_vector_R(n64, lower64, upper64)
    holds, _, residual_code = evaluate_gwr_carrier_transport_closure(
        n64, lower64, upper64, require_lock_and_profile=True
    )
    return {
        "case_id": "unit_64bit_true_close_pin",
        "bits": 64,
        "N": str(n64),
        "source": "unit_public_certificate_fields",
        "gwr_stack_holds": holds,
        "gwr_residual_if_fail": residual_code,
        "layers": [
            {
                "layer": 0,
                "name": "chamber_endpoint_atlas",
                "s": _public_s(n64),
                "N": str(n64),
                "structural_certificate_present": bool(holds),
                "note": "synthetic public cert fields (not full chain walk)",
            },
            _layer1_from_vector(vector, None),
            _layer2_transport(vector, n64),
            _layer3_decision(
                resolved=bool(holds),
                residual_code=None if holds else residual_code,
                vector=vector,
                decision_residual=None if holds else residual_code,
            ),
        ],
        "layer4_audit_candidate_list": None,
        "classical_inference_fields": [],
    }


def map_row_false_class_anti_admission() -> dict[str, Any]:
    """Historical false mutual-close class must not be map_class certificate."""
    blocked = is_historical_false_endpoint_class("32047651", "32059633")
    return {
        "case_id": "historical_false_endpoint_class_50bit",
        "source": "anti_admission_public",
        "historical_false_class_blocked": blocked,
        "layers": [
            {
                "layer": 3,
                "name": "residual_atlas_decision",
                "map_class": "blocked_false_class" if blocked else "LEAK",
                "decision_cell": None,
                "note": "anti-admission is public residual honesty, not factor test",
            }
        ],
        "layer4_audit_candidate_list": None,
        "classical_inference_fields": [],
    }


def evaluate_gates(maps: list[dict]) -> dict[str, Any]:
    by_id = {m["case_id"]: m for m in maps}
    m40 = by_id.get("rsa_v2_40bit_static_001")
    m50 = by_id.get("rsa_v2_50bit_static_001")
    m64 = by_id.get("unit_64bit_true_close_pin")
    mfalse = by_id.get("historical_false_endpoint_class_50bit")

    def layer3(m: dict | None) -> dict | None:
        if m is None:
            return None
        for layer in m.get("layers") or []:
            if layer.get("layer") == 3:
                return layer
        return None

    l40, l50, l64 = layer3(m40), layer3(m50), layer3(m64)

    gates = {
        "G1_40bit_certificate_class": {
            "expect": "map_class=certificate",
            "observed": None if l40 is None else l40.get("map_class"),
            "pass": bool(l40 and l40.get("map_class") == "certificate"),
        },
        "G2_50bit_joint_cell_C1T2L1": {
            "expect": "named_residual + C1T2L1 / unresolved_by_joint_cell_C1T2L1",
            "observed": {
                "map_class": None if l50 is None else l50.get("map_class"),
                "decision_cell": None if l50 is None else l50.get("decision_cell"),
                "residual_code": None if l50 is None else l50.get("residual_code"),
                "is_joint_cell_C1T2L1": None
                if l50 is None
                else l50.get("is_joint_cell_C1T2L1"),
            },
            "pass": bool(
                l50
                and l50.get("map_class") == "named_residual"
                and (
                    l50.get("is_joint_cell_C1T2L1") is True
                    or l50.get("decision_cell") == "C1T2L1"
                    or l50.get("residual_code") == "unresolved_by_joint_cell_C1T2L1"
                )
            ),
        },
        "G3_true_close_not_C1T2L1": {
            "expect": "true-close pin not joint C1T2L1; preferably certificate / C0T0L0",
            "observed": {
                "map_class": None if l64 is None else l64.get("map_class"),
                "decision_cell": None if l64 is None else l64.get("decision_cell"),
                "is_joint_cell_C1T2L1": None
                if l64 is None
                else l64.get("is_joint_cell_C1T2L1"),
                "gwr_stack_holds": None if m64 is None else m64.get("gwr_stack_holds"),
            },
            "pass": bool(
                l64
                and l64.get("is_joint_cell_C1T2L1") is False
                and l64.get("decision_cell") != "C1T2L1"
            ),
        },
        "G4_no_classical_inference_fields": {
            "expect": "classical_inference_fields empty on all map rows",
            "observed": {
                m["case_id"]: m.get("classical_inference_fields") for m in maps
            },
            "pass": all(not m.get("classical_inference_fields") for m in maps),
        },
        "G5_layer4_not_used_as_inference": {
            "expect": "layer4_audit_candidate_list is null (residual primary)",
            "observed": {
                m["case_id"]: m.get("layer4_audit_candidate_list") for m in maps
            },
            "pass": all(m.get("layer4_audit_candidate_list") is None for m in maps),
        },
        "G6_anti_admission_false_class": {
            "expect": "historical false endpoint class blocked",
            "observed": None
            if mfalse is None
            else mfalse.get("historical_false_class_blocked"),
            "pass": bool(mfalse and mfalse.get("historical_false_class_blocked") is True),
        },
    }

    # Discrimination: residual cells differ across 50 FP vs 64 TP
    gates["G7_residual_discrimination_50_vs_64"] = {
        "expect": "50-bit cell C1T2L1 and 64-bit cell C0T0L0 (distinct residual atlas)",
        "observed": {
            "50": None if l50 is None else l50.get("decision_cell"),
            "64": None if l64 is None else l64.get("decision_cell"),
        },
        "pass": bool(
            l50
            and l64
            and l50.get("decision_cell") == "C1T2L1"
            and l64.get("decision_cell") == "C0T0L0"
        ),
    }

    all_pass = all(g["pass"] for g in gates.values())
    return {
        "all_pass": all_pass,
        "gates": gates,
        "hypothesis_legs": (
            "YES_ON_NAMED_FIXTURES"
            if all_pass
            else "PARTIAL_OR_FAIL"
        ),
        "status_label": "measured_on_named_fixtures_only",
        "not_claims": [
            "not theorem",
            "not RSA-scale solve",
            "not verified/validated (no 10^18 map surface)",
            "residual map ranks remain hypothesis",
        ],
    }


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    cases = load_public_cases(FIXTURES)
    commit = git_commit()
    results = resolve_cases(cases, max_steps=None, commit=commit)

    maps = [map_row_from_resolve(r) for r in results]
    maps.append(map_row_synthetic_tp())
    maps.append(map_row_false_class_anti_admission())

    gate_report = evaluate_gates(maps)
    residual_hist = Counter()
    for m in maps:
        for layer in m.get("layers") or []:
            if layer.get("layer") == 3 and layer.get("residual_code"):
                residual_hist[layer["residual_code"]] += 1
            if layer.get("layer") == 3 and layer.get("decision_cell"):
                residual_hist[f"cell:{layer['decision_cell']}"] += 1

    write_jsonl(OUTPUT / "map_layers.jsonl", maps)
    write_json(OUTPUT / "gate_report.json", gate_report)
    write_json(
        OUTPUT / "summary.json",
        {
            "experiment": "gap_dni_public_map_probe",
            "git_commit": commit,
            "case_count_maps": len(maps),
            "residual_histogram_measured_only": dict(residual_hist),
            "gate_all_pass": gate_report["all_pass"],
            "hypothesis_legs": gate_report["hypothesis_legs"],
            "status_label": gate_report["status_label"],
            "outputs": [
                str(OUTPUT / "map_layers.jsonl"),
                str(OUTPUT / "gate_report.json"),
                str(OUTPUT / "summary.json"),
            ],
        },
    )

    # Compact RESULT.md
    lines = [
        "# Gap+DNI public map probe RESULT",
        "",
        f"**Status:** measured on named fixtures only  ",
        f"**Hypothesis legs:** `{gate_report['hypothesis_legs']}`  ",
        f"**All gates pass:** `{gate_report['all_pass']}`  ",
        f"**Git commit:** `{commit}`  ",
        "",
        "## Gates",
        "",
    ]
    for name, g in gate_report["gates"].items():
        lines.append(
            f"- **{name}**: `{'PASS' if g['pass'] else 'FAIL'}` — expect {g['expect']}; "
            f"observed `{json.dumps(g['observed'], sort_keys=True)}`"
        )
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `output/map_layers.jsonl`",
            "- `output/gate_report.json`",
            "- `output/summary.json`",
            "",
            "## Explicit non-claims",
            "",
        ]
    )
    for nc in gate_report["not_claims"]:
        lines.append(f"- {nc}")
    lines.append("")
    (OUTPUT / "RESULT.md").write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(gate_report, indent=2, sort_keys=True))
    return 0 if gate_report["all_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
