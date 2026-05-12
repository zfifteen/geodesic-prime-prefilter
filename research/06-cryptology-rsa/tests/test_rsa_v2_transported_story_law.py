from __future__ import annotations

import ast
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "src" / "python"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402

V2 = ROOT / "research" / "06-cryptology-rsa" / "experiments" / "rsa" / "v2"
SCRIPT = V2 / "transported_story_law_probe.py"
RULE_ID = "transported_story_law_v1"
EXPECTED_COUNTS = {
    "row_count": 512,
    "ledger_effective_survivor_count": 202,
    "recursive_row_count": 713,
    "recursive_final_survivor_count": 0,
}


def load_module(path: Path):
    """Load one script module directly from its file path."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows from a test output path."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def transported_symbol(row: dict[str, object], value: object) -> str:
    """Return the transported prefix/suffix symbol for one public coordinate."""
    point = int(str(value))
    prefix_lo = int(str(row["transported_prefix_lo"]))
    prefix_hi = int(str(row["transported_prefix_hi"]))
    suffix_lo = int(str(row["transported_suffix_lo"]))
    suffix_hi = int(str(row["transported_suffix_hi"]))
    in_prefix = min(prefix_lo, prefix_hi) <= point <= max(prefix_lo, prefix_hi)
    in_suffix = min(suffix_lo, suffix_hi) <= point <= max(suffix_lo, suffix_hi)
    if in_prefix and in_suffix:
        return "B"
    if in_prefix:
        return "P"
    if in_suffix:
        return "S"
    return "O"


def induced_carrier_symbol(row: dict[str, object]) -> str | None:
    """Return the public transported symbol of the induced carrier event."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return None
    for kind, value in zip(
        row["induced_story_event_kinds"],
        row["induced_story_event_values"],
        strict=True,
    ):
        if kind == "carrier_lock" and value == carrier:
            return transported_symbol(row, value)
    return None


def induced_carrier_run_ordinal(row: dict[str, object]) -> int | None:
    """Return the one-based collapsed interval-run ordinal containing the carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return None
    ordinal = 0
    previous = None
    for kind, value in zip(
        row["induced_story_event_kinds"],
        row["induced_story_event_values"],
        strict=True,
    ):
        symbol = transported_symbol(row, value)
        if symbol != previous:
            ordinal += 1
            previous = symbol
        if kind == "carrier_lock" and value == carrier:
            return ordinal
    return None


def induced_carrier_event_index(row: dict[str, object]) -> int | None:
    """Return the exact induced story index of the carrier event."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return None
    for index, (kind, value) in enumerate(
        zip(
            row["induced_story_event_kinds"],
            row["induced_story_event_values"],
            strict=True,
        )
    ):
        if kind == "carrier_lock" and value == carrier:
            return index
    return None


def carrier_in_floor_cell(
    row: dict[str, object],
    source_lo_key: str,
    source_hi_key: str,
) -> bool:
    """Return the exact reciprocal-floor cell membership of the induced carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return False
    z = int(str(carrier))
    modulus = int(str(row["N"]))
    source_lo = int(str(row[source_lo_key]))
    source_hi = int(str(row[source_hi_key]))
    return z * source_lo <= modulus < (z + 1) * source_hi


def carrier_has_integer_preimage(
    row: dict[str, object],
    source_lo_key: str,
    source_hi_key: str,
) -> bool:
    """Return whether some integer source point floors to the induced carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return False
    z = int(str(carrier))
    modulus = int(str(row["N"]))
    source_lo = int(str(row[source_lo_key]))
    source_hi = int(str(row[source_hi_key]))
    preimage_lo = max(source_lo, modulus // (z + 1) + 1)
    preimage_hi = min(source_hi, modulus // z)
    return preimage_lo <= preimage_hi


def carrier_preimage_width(
    row: dict[str, object],
    source_lo_key: str,
    source_hi_key: str,
) -> int:
    """Return the source integer-preimage interval width for the induced carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return 0
    z = int(str(carrier))
    modulus = int(str(row["N"]))
    source_lo = int(str(row[source_lo_key]))
    source_hi = int(str(row[source_hi_key]))
    preimage_lo = max(source_lo, modulus // (z + 1) + 1)
    preimage_hi = min(source_hi, modulus // z)
    return max(0, preimage_hi - preimage_lo + 1)


def carrier_preimage_value(row: dict[str, object]) -> int | None:
    """Return the unique source integer preimage of the induced carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return None
    return int(str(row["N"])) // int(str(carrier))


def carrier_preimage_position(row: dict[str, object]) -> str:
    """Return the source-story position class of the unique carrier preimage."""
    lifted = carrier_preimage_value(row)
    assert lifted is not None
    carrier = int(str(row["source_carrier_event_value"]))
    reset = int(str(row["source_reset_event_value"]))
    deadline = int(str(row["source_deadline_event_value"]))
    if lifted == carrier:
        return "carrier"
    if lifted == reset:
        return "reset"
    threat = row["source_threat_event_value"]
    if threat is not None and lifted == int(str(threat)):
        return "lower_threat"
    if lifted == deadline:
        return "deadline"
    matches = {
        str(kind)
        for kind, value in zip(
            row["source_story_event_kinds"],
            row["source_story_event_values"],
            strict=True,
        )
        if int(str(value)) == lifted
    }
    if matches:
        return "+".join(sorted(matches))
    if carrier < lifted < reset:
        return "unrecorded_prefix_interior"
    if reset < lifted < deadline:
        return "unrecorded_suffix_interior"
    return "other"


def divisor_count(n: int) -> int:
    """Return the exact divisor count for one integer."""
    return int(divisor_counts_segment(n, n + 1)[0])


def carrier_has_source_story_event_preimage(
    row: dict[str, object],
    source_lo_key: str,
    source_hi_key: str,
) -> bool:
    """Return whether a recorded source story event floors to the induced carrier."""
    carrier = row["induced_carrier_event_value"]
    if carrier is None:
        return False
    z = int(str(carrier))
    modulus = int(str(row["N"]))
    source_lo = int(str(row[source_lo_key]))
    source_hi = int(str(row[source_hi_key]))
    for value in row["source_story_event_values"]:
        y = int(str(value))
        if min(source_lo, source_hi) <= y <= max(source_lo, source_hi):
            if modulus // y == z:
                return True
    return False


def interval_run_word(row: dict[str, object]) -> str:
    """Return the collapsed public P/S/B/O run word for one induced story."""
    runs: list[str] = []
    previous = None
    for value in row["induced_story_event_values"]:
        symbol = transported_symbol(row, value)
        if symbol != previous:
            runs.append(symbol)
            previous = symbol
    return "".join(runs)


def event_count(row: dict[str, object], prefix: str, event_kind: str) -> int:
    """Return one public event-count component."""
    return list(row[f"{prefix}_story_event_kinds"]).count(event_kind)


def source_balance(row: dict[str, object]) -> int:
    """Return the source closed-tail chamber balance."""
    return event_count(row, "source", "closed_offset") - event_count(
        row,
        "source",
        "tail",
    )


def induced_balance(row: dict[str, object]) -> int:
    """Return the induced closed-tail chamber balance."""
    return event_count(row, "induced", "closed_offset") - event_count(
        row,
        "induced",
        "tail",
    )


def lock_relation(row: dict[str, object]) -> str:
    """Return the public source/induced carrier lock-label relation."""
    source_lock = row["source_lock_carrier_d"]
    induced_lock = row["induced_lock_carrier_d"]
    if source_lock is None or induced_lock is None:
        return "missing"
    source_value = int(source_lock)
    induced_value = int(induced_lock)
    if induced_value < source_value:
        return "lower"
    if induced_value == source_value:
        return "equal"
    return "higher"


def run_balance_signature(row: dict[str, object]) -> tuple[str, int, int]:
    """Return the measured public RB(C,C') signature."""
    return (interval_run_word(row), source_balance(row), induced_balance(row))


def prefix_material(row: dict[str, object]) -> bool:
    """Return the public PrefixMaterial predicate used by Lemma 1."""
    return (
        row["induced_carrier_in_prefix_zone"]
        and int(row["induced_lock_carrier_d"]) <= int(row["source_lock_carrier_d"])
    )


def deadline_threat(row: dict[str, object]) -> bool:
    """Return whether the public source deadline is the lower-threat event."""
    return row["source_threat_event_value"] == row["source_deadline_event_value"]


def threat_material(row: dict[str, object]) -> bool:
    """Return the public ThreatMaterial predicate used by Lemma 2."""
    return (
        deadline_threat(row)
        and row["induced_carrier_in_suffix_zone"]
        and int(row["induced_lock_carrier_d"]) < int(row["source_lock_carrier_d"])
    )


def certificate_story_grammar_matches(kinds: list[object]) -> bool:
    """Return whether one event-kind word has the public certificate grammar."""
    word = [str(kind) for kind in kinds]
    index = 0
    while index < len(word) and word[index] == "closed_offset":
        index += 1
    if index < len(word) and word[index] == "carrier_lock":
        index += 1
    if index >= len(word) or word[index] != "reset":
        return False
    index += 1
    if index < len(word) and word[index] == "lower_threat":
        index += 1
    while index < len(word) and word[index] == "tail":
        index += 1
    return index == len(word) - 1 and word[index] == "deadline"


def test_transported_story_law_reproduces_direct_ledger_collapse(tmp_path):
    """The direct story-law probe reproduces the transported-ledger count contract."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert summary["rule_id"] == RULE_ID
    assert summary["falsification_status"] == "passed"
    assert summary["divergences"] == []
    assert summary["expected_counts"] == EXPECTED_COUNTS
    for field, expected in EXPECTED_COUNTS.items():
        assert summary[field] == expected

    assert len(rows) == EXPECTED_COUNTS["row_count"]
    assert len(recursive_rows) == EXPECTED_COUNTS["recursive_row_count"]
    assert summary["ledger_prefix_elimination_count"] == 101
    assert summary["ledger_suffix_elimination_count"] == 16
    assert summary["ledger_threat_ceiling_elimination_count"] == 0


def test_transported_story_law_certificate_story_grammar_is_fixed(tmp_path):
    """Source and induced story words follow the public certificate grammar."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    assert len(rows) == EXPECTED_COUNTS["row_count"]
    assert all(
        certificate_story_grammar_matches(row["source_story_event_kinds"])
        for row in rows
    )
    assert all(
        certificate_story_grammar_matches(row["induced_story_event_kinds"])
        for row in rows
    )


def test_transported_story_law_carrier_zones_are_floor_cells(tmp_path):
    """The public carrier zone flags equal exact reciprocal-floor cell tests."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_cell_count = 0
    suffix_cell_count = 0

    for row in rows:
        prefix_cell = carrier_in_floor_cell(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        )
        suffix_cell = carrier_in_floor_cell(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        )
        assert prefix_cell == row["induced_carrier_in_prefix_zone"]
        assert suffix_cell == row["induced_carrier_in_suffix_zone"]
        prefix_cell_count += int(prefix_cell)
        suffix_cell_count += int(suffix_cell)

    assert prefix_cell_count == 109
    assert suffix_cell_count == 219


def test_transported_story_law_floor_cells_have_integer_preimages(tmp_path):
    """The public carrier zone flags equal integer source-preimage existence."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_preimage_count = 0
    suffix_preimage_count = 0

    for row in rows:
        prefix_preimage = carrier_has_integer_preimage(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        )
        suffix_preimage = carrier_has_integer_preimage(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        )
        assert prefix_preimage == row["induced_carrier_in_prefix_zone"]
        assert suffix_preimage == row["induced_carrier_in_suffix_zone"]
        prefix_preimage_count += int(prefix_preimage)
        suffix_preimage_count += int(suffix_preimage)

    assert prefix_preimage_count == 109
    assert suffix_preimage_count == 219


def test_transported_story_law_carrier_preimages_are_singletons(tmp_path):
    """Every measured carrier-zone hit has a unique source integer preimage."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_zone_rows = [
        row
        for row in rows
        if row["induced_carrier_in_prefix_zone"]
    ]
    suffix_zone_rows = [
        row
        for row in rows
        if row["induced_carrier_in_suffix_zone"]
    ]
    prefix_material_rows = [row for row in rows if prefix_material(row)]
    threat_material_rows = [row for row in rows if threat_material(row)]

    assert len(prefix_zone_rows) == 109
    assert len(suffix_zone_rows) == 219
    assert all(
        carrier_preimage_width(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        ) == 1
        for row in prefix_zone_rows
    )
    assert all(
        carrier_preimage_width(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        ) == 1
        for row in suffix_zone_rows
    )
    assert all(
        carrier_preimage_width(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        ) == 1
        for row in prefix_material_rows
    )
    assert all(
        carrier_preimage_width(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        ) == 1
        for row in threat_material_rows
    )


def test_transported_story_law_story_event_preimage_shortcut_fails(tmp_path):
    """Carrier-zone membership is not only recorded source-event image matching."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_zone_rows = [
        row
        for row in rows
        if row["induced_carrier_in_prefix_zone"]
    ]
    suffix_zone_rows = [
        row
        for row in rows
        if row["induced_carrier_in_suffix_zone"]
    ]
    prefix_event_rows = [
        row
        for row in prefix_zone_rows
        if carrier_has_source_story_event_preimage(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        )
    ]
    suffix_event_rows = [
        row
        for row in suffix_zone_rows
        if carrier_has_source_story_event_preimage(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        )
    ]
    prefix_material_event_rows = [
        row
        for row in rows
        if prefix_material(row)
        and carrier_has_source_story_event_preimage(
            row,
            "source_carrier_event_value",
            "source_reset_event_value",
        )
    ]
    threat_material_event_rows = [
        row
        for row in rows
        if threat_material(row)
        and carrier_has_source_story_event_preimage(
            row,
            "source_reset_event_value",
            "source_deadline_event_value",
        )
    ]

    assert len(prefix_zone_rows) == 109
    assert len(prefix_event_rows) == 42
    assert len(suffix_zone_rows) == 219
    assert len(suffix_event_rows) == 58
    assert len(prefix_material_event_rows) == 36
    assert len(threat_material_event_rows) == 9


def test_transported_story_law_lift_divisor_count_is_not_lock_transport(tmp_path):
    """The unique source lift does not itself supply lock-label transport."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_rows = [row for row in rows if prefix_material(row)]
    threat_rows = [row for row in rows if threat_material(row)]

    def relation_counts(rows: list[dict[str, object]], key: str) -> Counter[int]:
        counts: Counter[int] = Counter()
        for row in rows:
            lifted = carrier_preimage_value(row)
            assert lifted is not None
            lifted_d = divisor_count(lifted)
            label = int(row[key])
            counts[(lifted_d > label) - (lifted_d < label)] += 1
        return counts

    assert relation_counts(prefix_rows, "source_lock_carrier_d") == {
        -1: 21,
        0: 18,
        1: 62,
    }
    assert relation_counts(prefix_rows, "induced_lock_carrier_d") == {
        -1: 21,
        0: 7,
        1: 73,
    }
    assert relation_counts(threat_rows, "source_lock_carrier_d") == {
        -1: 9,
        1: 3,
    }
    assert relation_counts(threat_rows, "induced_lock_carrier_d") == {
        -1: 6,
        0: 2,
        1: 4,
    }


def test_transported_story_law_lift_position_classes_are_stable(tmp_path):
    """The unique source lifts have stable source-segment position classes."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")

    def positions(rows: list[dict[str, object]]) -> Counter[str]:
        return Counter(carrier_preimage_position(row) for row in rows)

    assert positions(
        [row for row in rows if row["induced_carrier_in_prefix_zone"]]
    ) == {
        "unrecorded_prefix_interior": 67,
        "reset": 27,
        "carrier": 11,
        "closed_offset": 4,
    }
    assert positions(
        [row for row in rows if row["induced_carrier_in_suffix_zone"]]
    ) == {
        "unrecorded_suffix_interior": 161,
        "reset": 27,
        "closed_offset": 18,
        "deadline": 10,
        "lower_threat": 3,
    }
    assert positions([row for row in rows if prefix_material(row)]) == {
        "unrecorded_prefix_interior": 65,
        "reset": 21,
        "carrier": 11,
        "closed_offset": 4,
    }
    assert positions([row for row in rows if threat_material(row)]) == {
        "reset": 6,
        "unrecorded_suffix_interior": 3,
        "lower_threat": 3,
    }


def test_transported_story_law_prefix_nonreset_lifts_obey_source_non_descent(
    tmp_path,
):
    """PrefixMaterial non-reset lifts do not descend below the source label."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_rows = [row for row in rows if prefix_material(row)]
    by_position: dict[str, Counter[int]] = {}
    violations: list[dict[str, object]] = []

    for row in prefix_rows:
        lifted = carrier_preimage_value(row)
        assert lifted is not None
        lifted_d = divisor_count(lifted)
        source_label = int(row["source_lock_carrier_d"])
        position = carrier_preimage_position(row)
        relation = (lifted_d > source_label) - (lifted_d < source_label)
        by_position.setdefault(position, Counter())[relation] += 1
        if position != "reset" and lifted_d < source_label:
            violations.append(row)

    assert by_position == {
        "unrecorded_prefix_interior": {1: 60, 0: 5},
        "reset": {-1: 21},
        "carrier": {0: 11},
        "closed_offset": {1: 2, 0: 2},
    }
    assert violations == []


def test_transported_story_law_threat_interior_lifts_are_not_source_descent(
    tmp_path,
):
    """ThreatMaterial source descent occurs only at reset/threat boundaries."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    threat_rows = [row for row in rows if threat_material(row)]
    by_position: dict[str, Counter[int]] = {}
    interior_violations: list[dict[str, object]] = []

    for row in threat_rows:
        lifted = carrier_preimage_value(row)
        assert lifted is not None
        lifted_d = divisor_count(lifted)
        source_label = int(row["source_lock_carrier_d"])
        position = carrier_preimage_position(row)
        relation = (lifted_d > source_label) - (lifted_d < source_label)
        by_position.setdefault(position, Counter())[relation] += 1
        if position == "unrecorded_suffix_interior" and lifted_d < source_label:
            interior_violations.append(row)

    assert by_position == {
        "reset": {-1: 6},
        "unrecorded_suffix_interior": {1: 3},
        "lower_threat": {-1: 3},
    }
    assert interior_violations == []


def test_transported_story_law_carrier_symbol_matches_interval_predicates(tmp_path):
    """The carrier-local prefix/threat readings match the interval predicates."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_interval_count = 0
    prefix_symbol_count = 0
    threat_interval_count = 0
    threat_symbol_count = 0

    for row in rows:
        symbol = induced_carrier_symbol(row)
        source_lock = row["source_lock_carrier_d"]
        induced_lock = row["induced_lock_carrier_d"]
        assert source_lock is not None
        assert induced_lock is not None

        prefix_interval = (
            row["induced_carrier_in_prefix_zone"]
            and int(induced_lock) <= int(source_lock)
        )
        prefix_symbol = symbol in {"P", "B"} and int(induced_lock) <= int(source_lock)
        assert prefix_symbol == prefix_interval
        prefix_interval_count += int(prefix_interval)
        prefix_symbol_count += int(prefix_symbol)

        deadline_threat = row["source_threat_event_value"] == row["source_deadline_event_value"]
        threat_interval = (
            deadline_threat
            and row["induced_carrier_in_suffix_zone"]
            and int(induced_lock) < int(source_lock)
        )
        threat_symbol = (
            deadline_threat
            and symbol in {"S", "B"}
            and int(induced_lock) < int(source_lock)
        )
        assert threat_symbol == threat_interval
        threat_interval_count += int(threat_interval)
        threat_symbol_count += int(threat_symbol)

    assert prefix_interval_count == 101
    assert prefix_symbol_count == 101
    assert threat_interval_count == 12
    assert threat_symbol_count == 12


def test_transported_story_law_run_balance_separates_direct_material(tmp_path):
    """RB separates direct frontier/material rows while leaving stale history separate."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    effective = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_effective_survivor"]
    }
    eliminated = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_eliminated"]
    }
    stale = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_stale_transport_state"]
    }

    assert len({run_balance_signature(row) for row in rows}) == 475
    assert len(effective) == 193
    assert len(eliminated) == 104
    assert len(stale) == 200
    assert effective.isdisjoint(eliminated)
    assert len(effective & stale) == 9
    assert len(eliminated & stale) == 13


def test_transported_story_law_run_balance_uses_public_preledger_fields(tmp_path):
    """RB is computable after deleting ledger, frontier, and interval labels."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    forbidden_keys = {
        "frontier_new_transport_state",
        "induced_carrier_in_prefix_zone",
        "induced_carrier_in_suffix_zone",
        "induced_threat_before_transported_deadline",
        "induced_threat_in_committed_zone",
    }
    forbidden_prefixes = ("ledger_",)
    stripped_rows = []
    for row in rows:
        stripped = {
            key: value
            for key, value in row.items()
            if key not in forbidden_keys
            and not any(key.startswith(prefix) for prefix in forbidden_prefixes)
        }
        assert forbidden_keys.isdisjoint(stripped)
        assert not any(
            key.startswith(prefix)
            for key in stripped
            for prefix in forbidden_prefixes
        )
        stripped_rows.append(stripped)

    assert [
        run_balance_signature(row)
        for row in stripped_rows
    ] == [
        run_balance_signature(row)
        for row in rows
    ]
    assert len({run_balance_signature(row) for row in stripped_rows}) == 475


def test_transported_story_law_run_balance_has_no_typed_nontyped_overlap(tmp_path):
    """No measured RB class mixes typed material with non-typed rows."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    typed_rb = {
        run_balance_signature(row)
        for row in rows
        if prefix_material(row) or threat_material(row)
    }
    nontyped_rb = {
        run_balance_signature(row)
        for row in rows
        if not prefix_material(row) and not threat_material(row)
    }

    assert len(typed_rb) == 101
    assert len(nontyped_rb) == 374
    assert typed_rb.isdisjoint(nontyped_rb)


def test_transported_story_law_run_balance_determines_carrier_symbol(tmp_path):
    """Each measured RB class has one induced-carrier interval run."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    symbols_by_rb: dict[tuple[str, int, int], set[str | None]] = {}
    runs_by_rb: dict[tuple[str, int, int], set[int | None]] = {}
    for row in rows:
        symbols_by_rb.setdefault(run_balance_signature(row), set()).add(
            induced_carrier_symbol(row)
        )
        runs_by_rb.setdefault(run_balance_signature(row), set()).add(
            induced_carrier_run_ordinal(row)
        )

    ambiguous_symbols = {
        key: symbols
        for key, symbols in symbols_by_rb.items()
        if len(symbols) > 1
    }
    ambiguous_runs = {
        key: runs
        for key, runs in runs_by_rb.items()
        if len(runs) > 1
    }

    assert len(symbols_by_rb) == 475
    assert len(runs_by_rb) == 475
    assert ambiguous_symbols == {}
    assert ambiguous_runs == {}


def test_transported_story_law_recursive_run_balance_determines_carrier_symbol(tmp_path):
    """Recursive public RB classes also have one induced-carrier interval run."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")

    for measured_rows, expected_classes in (
        (recursive_rows, 661),
        (rows + recursive_rows, 661),
    ):
        symbols_by_rb: dict[tuple[str, int, int], set[str | None]] = {}
        runs_by_rb: dict[tuple[str, int, int], set[int | None]] = {}
        for row in measured_rows:
            symbols_by_rb.setdefault(run_balance_signature(row), set()).add(
                induced_carrier_symbol(row)
            )
            runs_by_rb.setdefault(run_balance_signature(row), set()).add(
                induced_carrier_run_ordinal(row)
            )

        ambiguous_symbols = {
            key: symbols
            for key, symbols in symbols_by_rb.items()
            if len(symbols) > 1
        }
        ambiguous_runs = {
            key: runs
            for key, runs in runs_by_rb.items()
            if len(runs) > 1
        }

        assert len(symbols_by_rb) == expected_classes
        assert len(runs_by_rb) == expected_classes
        assert ambiguous_symbols == {}
        assert ambiguous_runs == {}


def test_transported_story_law_run_balance_does_not_determine_exact_carrier_index(tmp_path):
    """RB determines the carrier run, not the exact induced event index."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")

    for measured_rows in (rows, recursive_rows, rows + recursive_rows):
        carrier_indices_by_rb: dict[tuple[str, int, int], set[int | None]] = {}
        closed_counts_by_rb: dict[tuple[str, int, int], set[int]] = {}
        story_lengths_by_rb: dict[tuple[str, int, int], set[int]] = {}
        for row in measured_rows:
            rb = run_balance_signature(row)
            carrier_indices_by_rb.setdefault(rb, set()).add(
                induced_carrier_event_index(row)
            )
            closed_counts_by_rb.setdefault(rb, set()).add(
                event_count(row, "induced", "closed_offset")
            )
            story_lengths_by_rb.setdefault(rb, set()).add(
                len(row["induced_story_event_kinds"])
            )

        assert sum(
            1 for values in carrier_indices_by_rb.values() if len(values) > 1
        ) == 5
        assert sum(
            1 for values in closed_counts_by_rb.values() if len(values) > 1
        ) == 5
        assert sum(
            1 for values in story_lengths_by_rb.values() if len(values) > 1
        ) == 5


def test_transported_story_law_carrier_run_requires_full_run_balance(tmp_path):
    """Carrier-run localization is not determined by run word or one balance alone."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    combined_rows = rows + recursive_rows

    projections: dict[str, dict[object, set[int | None]]] = {
        "word": {},
        "word_source_balance": {},
        "word_induced_balance": {},
        "word_balance_delta": {},
        "full_rb": {},
    }
    for row in combined_rows:
        word = interval_run_word(row)
        source_value = source_balance(row)
        induced_value = induced_balance(row)
        carrier_run = induced_carrier_run_ordinal(row)
        keys = {
            "word": word,
            "word_source_balance": (word, source_value),
            "word_induced_balance": (word, induced_value),
            "word_balance_delta": (word, induced_value - source_value),
            "full_rb": run_balance_signature(row),
        }
        for projection_name, key in keys.items():
            projections[projection_name].setdefault(key, set()).add(carrier_run)

    ambiguous_counts = {
        projection_name: sum(1 for values in mapping.values() if len(values) > 1)
        for projection_name, mapping in projections.items()
    }

    assert ambiguous_counts == {
        "word": 12,
        "word_source_balance": 18,
        "word_induced_balance": 17,
        "word_balance_delta": 6,
        "full_rb": 0,
    }


def test_transported_story_law_refinement_fields_projection_boundaries(tmp_path):
    """RB refinement fields have distinct measured projection boundaries."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    combined_rows = rows + recursive_rows

    def branch(row: dict[str, object]) -> str:
        is_prefix = prefix_material(row)
        is_threat = threat_material(row)
        if is_prefix and is_threat:
            return "prefix+threat"
        if is_prefix:
            return "prefix"
        if is_threat:
            return "threat"
        return "nontyped"

    label_functions = {
        "lock_relation": lock_relation,
        "deadline_threat": deadline_threat,
        "typed_branch": branch,
    }
    projection_counts: dict[str, dict[str, int]] = {}
    for label_name, label_function in label_functions.items():
        projections: dict[str, dict[object, set[object]]] = {
            "word": {},
            "word_source_balance": {},
            "word_induced_balance": {},
            "word_balance_delta": {},
            "full_rb": {},
        }
        for row in combined_rows:
            word = interval_run_word(row)
            source_value = source_balance(row)
            induced_value = induced_balance(row)
            label = label_function(row)
            keys = {
                "word": word,
                "word_source_balance": (word, source_value),
                "word_induced_balance": (word, induced_value),
                "word_balance_delta": (word, induced_value - source_value),
                "full_rb": run_balance_signature(row),
            }
            for projection_name, key in keys.items():
                projections[projection_name].setdefault(key, set()).add(label)
        projection_counts[label_name] = {
            projection_name: sum(
                1 for values in mapping.values() if len(values) > 1
            )
            for projection_name, mapping in projections.items()
        }

    assert projection_counts == {
        "lock_relation": {
            "word": 26,
            "word_source_balance": 8,
            "word_induced_balance": 36,
            "word_balance_delta": 16,
            "full_rb": 0,
        },
        "deadline_threat": {
            "word": 22,
            "word_source_balance": 0,
            "word_induced_balance": 39,
            "word_balance_delta": 17,
            "full_rb": 0,
        },
        "typed_branch": {
            "word": 16,
            "word_source_balance": 11,
            "word_induced_balance": 19,
            "word_balance_delta": 6,
            "full_rb": 0,
        },
    }


def test_transported_story_law_lock_relation_requires_full_run_word(tmp_path):
    """Carrier-run localization plus balances does not determine lock relation."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    combined_rows = rows + recursive_rows

    projection_functions = {
        "carrier_run_source_induced_balance": lambda row: (
            induced_carrier_run_ordinal(row),
            source_balance(row),
            induced_balance(row),
        ),
        "carrier_symbol_source_induced_balance": lambda row: (
            induced_carrier_symbol(row),
            source_balance(row),
            induced_balance(row),
        ),
        "carrier_run_balance_delta": lambda row: (
            induced_carrier_run_ordinal(row),
            induced_balance(row) - source_balance(row),
        ),
        "carrier_symbol_balance_delta": lambda row: (
            induced_carrier_symbol(row),
            induced_balance(row) - source_balance(row),
        ),
        "full_rb": run_balance_signature,
    }
    ambiguous_counts: dict[str, int] = {}
    for projection_name, projection_function in projection_functions.items():
        relations_by_projection: dict[object, set[str]] = {}
        for row in combined_rows:
            relations_by_projection.setdefault(projection_function(row), set()).add(
                lock_relation(row)
            )
        ambiguous_counts[projection_name] = sum(
            1 for values in relations_by_projection.values() if len(values) > 1
        )

    assert ambiguous_counts == {
        "carrier_run_source_induced_balance": 4,
        "carrier_symbol_source_induced_balance": 5,
        "carrier_run_balance_delta": 48,
        "carrier_symbol_balance_delta": 38,
        "full_rb": 0,
    }


def test_transported_story_law_typed_branch_projects_from_carrier_symbol_relation_deadline(tmp_path):
    """Typed branch is determined by carrier symbol, lock relation, and deadline state."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    combined_rows = rows + recursive_rows

    def branch(row: dict[str, object]) -> str:
        is_prefix = prefix_material(row)
        is_threat = threat_material(row)
        if is_prefix and is_threat:
            return "prefix+threat"
        if is_prefix:
            return "prefix"
        if is_threat:
            return "threat"
        return "nontyped"

    projection_functions = {
        "carrier_run_relation_deadline": lambda row: (
            induced_carrier_run_ordinal(row),
            lock_relation(row),
            deadline_threat(row),
        ),
        "carrier_symbol_relation_deadline": lambda row: (
            induced_carrier_symbol(row),
            lock_relation(row),
            deadline_threat(row),
        ),
        "carrier_run_relation_deadline_source_induced_balance": lambda row: (
            induced_carrier_run_ordinal(row),
            lock_relation(row),
            deadline_threat(row),
            source_balance(row),
            induced_balance(row),
        ),
        "carrier_symbol_relation_deadline_source_induced_balance": lambda row: (
            induced_carrier_symbol(row),
            lock_relation(row),
            deadline_threat(row),
            source_balance(row),
            induced_balance(row),
        ),
        "full_rb": run_balance_signature,
    }
    ambiguous_counts: dict[str, int] = {}
    for projection_name, projection_function in projection_functions.items():
        branches_by_projection: dict[object, set[str]] = {}
        for row in combined_rows:
            branches_by_projection.setdefault(projection_function(row), set()).add(
                branch(row)
            )
        ambiguous_counts[projection_name] = sum(
            1 for values in branches_by_projection.values() if len(values) > 1
        )

    assert ambiguous_counts == {
        "carrier_run_relation_deadline": 11,
        "carrier_symbol_relation_deadline": 0,
        "carrier_run_relation_deadline_source_induced_balance": 57,
        "carrier_symbol_relation_deadline_source_induced_balance": 0,
        "full_rb": 0,
    }


def test_transported_story_law_deadline_threat_is_source_balance_threshold(tmp_path):
    """On the public measured surface, source balance determines deadline threat."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    recursive_rows = read_jsonl(output_dir / "recursive_rows.jsonl")
    combined_rows = rows + recursive_rows

    states_by_source_balance: dict[int, set[bool]] = {}
    for row in combined_rows:
        states_by_source_balance.setdefault(source_balance(row), set()).add(
            deadline_threat(row)
        )

    assert states_by_source_balance == {
        **{balance: {False} for balance in range(8, 32)},
        32: {True},
        33: {True},
        34: {True},
    }
    assert all(
        deadline_threat(row) == (source_balance(row) >= 32)
        for row in combined_rows
    )


def test_transported_story_law_run_balance_determines_lock_relation(tmp_path):
    """Each measured RB class has one source/induced lock-label relation."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    relations_by_rb: dict[tuple[str, int, int], set[str]] = {}
    for row in rows:
        relations_by_rb.setdefault(run_balance_signature(row), set()).add(
            lock_relation(row)
        )

    ambiguous = {
        key: relations
        for key, relations in relations_by_rb.items()
        if len(relations) > 1
    }

    assert len(relations_by_rb) == 475
    assert ambiguous == {}


def test_transported_story_law_run_balance_determines_deadline_threat(tmp_path):
    """Each measured RB class has one source deadline-threat boundary state."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    deadline_state_by_rb: dict[tuple[str, int, int], set[bool]] = {}
    for row in rows:
        deadline_state_by_rb.setdefault(run_balance_signature(row), set()).add(
            deadline_threat(row)
        )

    ambiguous = {
        key: states
        for key, states in deadline_state_by_rb.items()
        if len(states) > 1
    }

    assert len(deadline_state_by_rb) == 475
    assert ambiguous == {}


def test_transported_story_law_typed_run_balance_branch_topology(tmp_path):
    """Prefix and threat RB classes form the measured typed RB topology."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_rb = {
        run_balance_signature(row)
        for row in rows
        if prefix_material(row)
    }
    threat_rb = {
        run_balance_signature(row)
        for row in rows
        if threat_material(row)
    }
    typed_rb = {
        run_balance_signature(row)
        for row in rows
        if prefix_material(row) or threat_material(row)
    }
    effective_rb = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_effective_survivor"]
    }
    eliminated_rb = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_eliminated"]
    }

    assert len(prefix_rb) == 95
    assert len(threat_rb) == 12
    assert len(prefix_rb & threat_rb) == 6
    assert len(prefix_rb | threat_rb) == 101
    assert typed_rb == prefix_rb | threat_rb
    assert typed_rb.isdisjoint(effective_rb)
    assert typed_rb.issubset(eliminated_rb)
    assert sorted(prefix_rb & threat_rb) == [
        ("OBO", 33, 17),
        ("OBO", 33, 20),
        ("OBO", 34, 17),
        ("OBPO", 34, 33),
        ("POBO", 33, 19),
        ("POBO", 34, 21),
    ]


def test_transported_story_law_run_balance_determines_typed_branch(tmp_path):
    """Each measured RB class has one typed branch class."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    branch_by_rb: dict[tuple[str, int, int], Counter[str]] = {}

    for row in rows:
        is_prefix = prefix_material(row)
        is_threat = threat_material(row)
        if is_prefix and is_threat:
            branch = "prefix+threat"
        elif is_prefix:
            branch = "prefix"
        elif is_threat:
            branch = "threat"
        else:
            branch = "nontyped"
        branch_by_rb.setdefault(run_balance_signature(row), Counter())[branch] += 1

    mixed = {
        key: counts
        for key, counts in branch_by_rb.items()
        if sum(1 for count in counts.values() if count) > 1
    }
    branch_class_counts = Counter(
        tuple(sorted(counts))
        for counts in branch_by_rb.values()
    )

    assert mixed == {}
    assert branch_class_counts == {
        ("nontyped",): 374,
        ("prefix",): 89,
        ("prefix+threat",): 6,
        ("threat",): 6,
    }


def test_transported_story_law_run_balance_keeps_recurrence_separate(tmp_path):
    """Effective/stale RB overlap is endpoint-history state, not direct material."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    effective = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_effective_survivor"]
    }
    eliminated = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_eliminated"]
    }
    stale = {
        run_balance_signature(row)
        for row in rows
        if row["ledger_stale_transport_state"]
    }

    assert sorted(effective & stale) == [
        ("O", 33, 11),
        ("OSO", 33, 21),
        ("OSOPO", 33, 25),
        ("OSPO", 33, 20),
        ("OSPO", 33, 21),
        ("SPOSO", 19, 25),
        ("SPOSPO", 17, 17),
        ("SPOSPO", 20, 20),
        ("SPOSPO", 22, 19),
    ]
    assert (effective & stale).isdisjoint(eliminated)


def test_transported_story_law_broad_run_balance_languages_are_invalid(tmp_path):
    """Run-word and balance supersets admit effective survivors."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    threat_run_words = {
        interval_run_word(row)
        for row in rows
        if threat_material(row)
    }
    equal_prefix_run_words = {
        interval_run_word(row)
        for row in rows
        if prefix_material(row)
        and int(row["induced_lock_carrier_d"]) == int(row["source_lock_carrier_d"])
    }

    def effective_count(rows: list[dict[str, object]]) -> int:
        return sum(bool(row["ledger_effective_survivor"]) for row in rows)

    threat_run_rows = [
        row for row in rows if interval_run_word(row) in threat_run_words
    ]
    threat_balance_rows = [
        row
        for row in threat_run_rows
        if induced_balance(row) < source_balance(row)
    ]
    threat_threshold_rows = [
        row
        for row in threat_balance_rows
        if source_balance(row) >= 32
    ]
    equal_prefix_run_rows = [
        row for row in rows if interval_run_word(row) in equal_prefix_run_words
    ]
    equal_prefix_lower_balance_rows = [
        row
        for row in equal_prefix_run_rows
        if induced_balance(row) <= source_balance(row)
    ]
    equal_prefix_higher_balance_rows = [
        row
        for row in equal_prefix_run_rows
        if induced_balance(row) >= source_balance(row)
    ]

    assert len(threat_run_rows) == 128
    assert effective_count(threat_run_rows) == 44
    assert len(threat_balance_rows) == 63
    assert effective_count(threat_balance_rows) == 21
    assert len(threat_threshold_rows) == 32
    assert effective_count(threat_threshold_rows) == 7

    assert len(equal_prefix_run_rows) == 128
    assert effective_count(equal_prefix_run_rows) == 8
    assert effective_count(equal_prefix_lower_balance_rows) == 7
    assert effective_count(equal_prefix_higher_balance_rows) == 1


def test_transported_story_law_monotone_balance_languages_are_invalid(tmp_path):
    """Shared run families invalidate coordinate-monotone balance regions."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    points_by_run: dict[str, dict[str, set[tuple[int, int]]]] = {}
    for row in rows:
        word = interval_run_word(row)
        points_by_run.setdefault(word, {"effective": set(), "typed": set()})
        if row["ledger_effective_survivor"]:
            points_by_run[word]["effective"].add(
                (source_balance(row), induced_balance(row))
            )
        if prefix_material(row) or threat_material(row):
            points_by_run[word]["typed"].add(
                (source_balance(row), induced_balance(row))
            )

    orientations = {
        "source_up_induced_up": (
            lambda effective, typed: effective[0] >= typed[0]
            and effective[1] >= typed[1]
        ),
        "source_up_induced_down": (
            lambda effective, typed: effective[0] >= typed[0]
            and effective[1] <= typed[1]
        ),
        "source_down_induced_up": (
            lambda effective, typed: effective[0] <= typed[0]
            and effective[1] >= typed[1]
        ),
        "source_down_induced_down": (
            lambda effective, typed: effective[0] <= typed[0]
            and effective[1] <= typed[1]
        ),
    }
    violations: dict[str, set[str]] = {name: set() for name in orientations}

    for word, classes in points_by_run.items():
        if not classes["effective"] or not classes["typed"]:
            continue
        for name, predicate in orientations.items():
            if any(
                predicate(effective, typed)
                for effective in classes["effective"]
                for typed in classes["typed"]
            ):
                violations[name].add(word)

    assert violations == {
        "source_up_induced_up": {"OBO", "OSPO", "OPO", "POBO", "OSPOPO"},
        "source_up_induced_down": {"OBO", "OSPO", "OPO", "SOPO"},
        "source_down_induced_up": {
            "OBO",
            "SPOSO",
            "POPOP",
            "OSPO",
            "OPO",
            "OBPO",
            "POBO",
            "OSPOPO",
        },
        "source_down_induced_down": {"OBO", "SPOSO", "OSPO", "OPO", "OSPOPO"},
    }


def test_transported_story_law_typed_material_antecedents_are_stable(tmp_path):
    """The measured PrefixMaterial/ThreatMaterial theorem inputs stay fixed."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    prefix_rows = [row for row in rows if prefix_material(row)]
    threat_rows = [row for row in rows if threat_material(row)]
    typed_rows = [
        row
        for row in rows
        if prefix_material(row) or threat_material(row)
    ]
    overlap_rows = [
        row
        for row in rows
        if prefix_material(row) and threat_material(row)
    ]

    assert len(prefix_rows) == 101
    assert len(threat_rows) == 12
    assert len(overlap_rows) == 6
    assert len(typed_rows) == 107
    assert not any(row["ledger_effective_survivor"] for row in typed_rows)
    assert all(row["ledger_eliminated"] for row in typed_rows)


def test_transported_story_law_threat_deadline_boundary_is_stable(tmp_path):
    """The Lemma 2 branch stays narrowed to public deadline=threat rows."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--output-dir", str(output_dir)]) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    threat_present_rows = [
        row
        for row in rows
        if row["source_threat_event_value"] is not None
    ]
    deadline_threat_rows = [row for row in rows if deadline_threat(row)]
    threat_rows = [row for row in rows if threat_material(row)]

    assert len(threat_present_rows) == 132
    assert len(deadline_threat_rows) == 115
    assert len(threat_rows) == 12
    assert all(deadline_threat(row) for row in threat_rows)


def test_transported_story_law_rows_are_public_sidecar_rows(tmp_path):
    """The direct story-law output carries only public diagnostic fields."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(
        [
            "--measured-rows",
            "4",
            "--output-dir",
            str(output_dir),
        ]
    ) == 0

    rows = read_jsonl(output_dir / "story_law_rows.jsonl")
    forbidden_fields = {
        "p",
        "q",
        "audit_status",
        "audit_integrity_status",
        "inference_audit_status",
        "product_check",
        "product_closure",
        "divisibility",
        "gcd",
        "isprime",
        "nextprime",
        "factorint",
        "resolver_label",
    }
    required_fields = {
        "case_id",
        "bits",
        "N",
        "rule_id",
        "source_anchor",
        "source_story_event_kinds",
        "source_story_event_values",
        "source_transport_carrier_image",
        "source_transport_reset_image",
        "source_transport_deadline_image",
        "transported_prefix_lo",
        "transported_prefix_hi",
        "transported_suffix_lo",
        "transported_suffix_hi",
        "induced_anchor",
        "induced_story_event_kinds",
        "induced_story_event_values",
        "ledger_prefix_elimination",
        "ledger_suffix_elimination",
        "ledger_threat_ceiling_elimination",
        "ledger_effective_survivor",
    }

    assert len(rows) == 8
    for row in rows:
        assert row["rule_id"] == RULE_ID
        assert required_fields.issubset(row)
        assert forbidden_fields.isdisjoint(row)


def test_transported_story_law_writes_lf_json_sidecars(tmp_path):
    """The story-law sidecar writes LF-only JSON and JSONL."""
    module = load_module(SCRIPT)
    output_dir = tmp_path / "story_law"

    assert module.main(["--measured-rows", "2", "--output-dir", str(output_dir)]) == 0

    for path in (
        output_dir / "story_law_rows.jsonl",
        output_dir / "recursive_rows.jsonl",
        output_dir / "summary.json",
    ):
        raw = path.read_bytes()
        assert raw.endswith(b"\n")
        assert b"\r\n" not in raw


def test_transported_story_law_source_has_no_forbidden_inference_constructs():
    """The direct story-law probe stays out of forbidden inference machinery."""
    source = SCRIPT.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_tokens = (
        "transported_exclusion_debt",
        "ledger_fields",
        "sympy",
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "randprime",
        "gcd",
        "OpenSSL",
        "subprocess",
        "direct_divisor_count",
        "prime_basis",
        "trial_division",
        "Miller",
        "audit_factors",
        "audit_spec",
        "random",
    )
    for token in forbidden_tokens:
        assert token not in source
    for node in ast.walk(tree):
        assert not isinstance(node, ast.Mod)
        if isinstance(node, ast.BinOp):
            assert not isinstance(node.op, ast.Mult)
