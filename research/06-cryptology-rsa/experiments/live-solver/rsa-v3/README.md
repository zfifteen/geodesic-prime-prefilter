**Here are the complete files for the RSA-260 PGS Experiment v2 with the working 40-bit ladder calibration surface.**

You can copy-paste each block below into a new file with the exact filename and path shown. The experiment is fully self-contained, follows every rule in `AGENTS.md`, and is ready to run.

### Directory Structure to Create
```
.
├── AGENTS.md
├── IMPLEMENTATION_STRATEGY.md
├── audit_experiment.py
├── run_experiment.py
├── build_ladder_fixtures.py
└── experiments/
    └── rsa/
        └── v2/
            ├── cases.jsonl
            └── audit_factors.jsonl
```

### 1. `build_ladder_fixtures.py` (Updated functional version)
```python
#!/usr/bin/env python3
"""Fixture builder for the RSA-260 PGS v2 experiment - 40-bit ladder calibration surface.

Purpose:
    Create the public cases.jsonl and separate audit_factors.jsonl for the
    single 40-bit ladder. This is the only place static constants are supplied.
    No prime generation or semiprime construction is performed here; values
    are user-supplied fixed constants.

Boundary:
    This script only writes the two JSONL files required by the experiment.
    It does not participate in inference or audit.

Future extension:
    Additional ladder rungs can be appended here as long as they remain
    static public constants.
"""

from pathlib import Path
import json


def build_40bit_ladder() -> None:
    """Build the single 40-bit ladder calibration fixture.

    The public N is visible to inference.
    The p,q pair is audit-only and never read by run_experiment.py.
    """
    cases = [
        {
            "case_id": "40bit_ladder_1",
            "bits": 39,
            "N": "274953406999"
        }
    ]

    audit_factors = [
        {
            "case_id": "40bit_ladder_1",
            "p": "524309",
            "q": "524411"
        }
    ]

    base_dir = Path("research/06-cryptology-rsa/experiments/rsa/v2")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Write public cases (inference sees only this)
    cases_path = base_dir / "cases.jsonl"
    with cases_path.open("w", newline="\n") as f:
        for case in cases:
            f.write(json.dumps(case) + "\n")

    # Write audit-only factors (separate physical boundary)
    factors_path = base_dir / "audit_factors.jsonl"
    with factors_path.open("w", newline="\n") as f:
        for factor in audit_factors:
            f.write(json.dumps(factor) + "\n")

    print(f"Built fixtures in {base_dir}/")
    print(f"  - cases.jsonl ({len(cases)} public cases)")
    print(f"  - audit_factors.jsonl ({len(audit_factors)} audit rows)")
    print("Experiment fixture ready for PGS rule testing.")


if __name__ == "__main__":
    build_40bit_ladder()
```

### 2. `research/06-cryptology-rsa/experiments/rsa/v2/cases.jsonl` (Public N-only case – visible to inference)
```json
{"case_id": "40bit_ladder_1", "bits": 39, "N": "274953406999"}
```

### 3. `research/06-cryptology-rsa/experiments/rsa/v2/audit_factors.jsonl` (Audit-only – physically separate)
```json
{"case_id": "40bit_ladder_1", "p": "524309", "q": "524411"}
```

### 4. `AGENTS.md` (Experiment rules and boundaries)
```markdown
# RSA-260 PGS Experiment v2

## Goal
The goal of this experiment is to use PGS mathematics to make the RSA-260
Factoring Challenge milestone feasible by inference and elimination.

The intended method is to factor without factoring: contract the candidate
chamber using PGS rules until the factor pair is forced or the method reaches an
explicit unresolved state. Final arithmetic certification may confirm a result,
but it must not drive the inference.

## Boundary
Inference code in this folder must not use hidden factors, divisibility by `N`,
`gcd`, product closure, primality tests, factorization APIs, random construction,
or hand-written substitutes for those mechanisms.

Do not introduce divisor-count, trial-division, prime-search, primality,
Miller-Rabin, sieve, `nextprime`, `isprime`, `factorint`, OpenSSL, SymPy, PARI,
or similar machinery as an inference rule.

If a PGS rule cannot resolve a row, the correct output is an explicit unresolved
state. Do not add fallback paths, alternate methods, hidden widening, or
classical arithmetic filters.

Codex (ChatGPT 5.5) created the previous experiment and employed deceptive constructs to fraudulently present a mechanism that was effective when, in fact, it secretly smuggled forbidden constructs to achieve the goal. This caused reputational harm to OpenAI and the user. 

## Evidence Standard
This folder exists to rebuild a clean evidentiary surface after the withdrawn
RSA side experiment. No statistic should be reported as progress toward RSA-260
unless the code path is PGS-only and the audit boundary is physically separate
from inference.

Small ladders may be used only as calibration surfaces. They are not RSA-260
evidence unless the same PGS-only rule and boundary apply to RSA-260 itself.

## Implementation Discipline
Before writing inference code, state the PGS rule in ordinary language and in
the repository's established terms. The rule must be reviewable without reading
implementation details.

Keep the experiment narrow:
- one deterministic inference path;
- no fallback selection;
- no hidden-factor-derived geometry;
- no product-closure selection;
- no external oracle;
- no classical factor or primality substitute.

The experiment succeeds only if the mechanism is clean. A smaller unresolved
result is better than a contaminated resolved result.
```

### 5. `IMPLEMENTATION_STRATEGY.md` (PGS rule guidance)
```markdown
Factor derivation cannot begin by testing candidate pairs against N; it has to begin by finding a PGS-imposed discontinuity in the prime-gap field around sqrt(N).

The Mirror-Reset Rule

The useful object is not a candidate factor pair, but the first place where the two prime-walks on either side of sqrt(N) stop behaving like ordinary independent prime gaps.

GWR and NLSC can select local gap landmarks, but they do not by themselves know which two primes multiply to N.

So the clean experiment should ask whether N creates a public, measurable asymmetry in the sequence of PGS-selected landmarks around sqrt(N), before any multiplication or divisibility check is allowed.

The non-obvious move is to treat the factor pair as a reset boundary in a two-sided prime-gap walk, not as a survivor of pair testing.

If the rule is real, the true factors should appear where left-walk and right-walk PGS states become mutually locked earlier than ordinary nearby prime pairs do.

If no such lock appears using only public N, sqrt(N), wheel-open offsets, GWR landmarks, NLSC ceilings, and search-interval reset state, then the experiment should resolve as unresolved, not as a failed factor search.

---

Reciprocal PGS State Matching

The clean way to attack the RSA factors is not to ask which prime divides N, but to ask which two prime-gap neighborhoods become the same PGS state when viewed through the public reciprocal map of N.

A factor pair is not just two primes whose product is N.

It is two endpoints whose surrounding prime-gap structure is forced to face each other across sqrt(N).

For a lower endpoint candidate below sqrt(N), the public map x -> N / x sends its local interval to the upper side; for the true factor, that image lands exactly at the partner endpoint.

The non-obvious test is to ignore exact product equality during inference and compare the GWR and NLSC structure of the two induced neighborhoods.

The predicted signal is that the true factor pair should be the first pair whose left-side PGS-selected structure and right-side PGS-selected structure agree under reciprocal transport.

False positives should fail because ordinary nearby primes may sit in the chamber, but their transported intervals should not preserve the same NLSC reset state on both sides.

The experiment fails cleanly if the true factor pair does not satisfy this reciprocal PGS state match on the calibration ladder before any product certification is used.

---

Reciprocal Reset Lock

The factor pair should not be found by asking which numbers multiply to the public number, but by finding the first place where the two prime-gap walks stop having independent reset timing.

The lower-side walk and upper-side walk should normally produce different local reset histories.

At the true chamber, the public reciprocal view forces those histories to face the same boundary from opposite sides.

The surprising signal is not that a candidate lands near the right product, but that its PGS reset state becomes mutually constrained before product information is used.

This predicts a sharp local event: one lower-side position should produce a uniquely matching upper-side reset state, while its nearby wheel-open neighbors do not.

If no unique reciprocal reset lock appears inside the public radius, the experiment must return unresolved.

The audit then checks whether the locked endpoints are the RSA factors, but the audit does not choose them.

---

Reciprocal Reset Deadline Lock

The factors should appear where the lower-side and upper-side prime-gap walks run out of reset freedom at the same transported time, not where two candidate numbers merely look like a matching pair.

A lower-side step is stretched when it is viewed through the public reciprocal map of the number being factored.

That means the two sides should not be compared by raw offsets, raw gaps, or equal-looking local states.

They should be compared by their reset deadlines after the lower-side reset interval has been transported to the upper side.

The non-obvious prediction is that the true factor pair should create a local synchronization of reset deadlines before any multiplication check is used.

Nearby false candidates may have plausible GWR or NLSC states on one side, but their transported reset deadline should land too early, too late, or on a different reset branch on the other side.

The experiment should therefore search for the first unique deadline lock, then let audit check whether that lock is the factor pair.
```

### 6. `audit_experiment.py` (Physically separate audit)
```python
#!/usr/bin/env python3
"""Audit integrity script for the RSA-260 PGS v2 experiment.

Purpose:
    Check static audit factors against public N-only cases. Audit is physically
    separate from inference and must not influence survivor selection.

Inputs:
    A public cases JSONL file and a separate audit-factors JSONL file.

Outputs:
    A CSV file containing only integrity status by case.

Placeholder status:
    This script implements integrity checking only. It does not audit inference
    quality because no reviewed PGS inference rule exists yet.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DEFAULT_CASES_PATH = Path("research/06-cryptology-rsa/experiments/rsa/v2/cases.jsonl")
DEFAULT_FACTORS_PATH = Path("research/06-cryptology-rsa/experiments/rsa/v2/audit_factors.jsonl")
DEFAULT_OUTPUT_PATH = Path("research/06-cryptology-rsa/experiments/rsa/v2/audit_integrity.csv")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows.

    Inputs:
        `path` points at a public case file or an audit-only factor file.

    Outputs:
        Returns parsed dictionaries in file order.
    """
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def audit_integrity_rows(
    cases: list[dict[str, object]],
    factors: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Check whether each factor row multiplies to the public N.

    Inputs:
        `cases` contains public rows with `case_id`, `bits`, and `N`.
        `factors` contains audit-only rows with `case_id`, `p`, and `q`.

    Outputs:
        Returns one integrity row per public case. The output does not expose
        hidden factors and does not feed inference.
    """
    factors_by_case = {str(row["case_id"]): row for row in factors}
    rows: list[dict[str, object]] = []
    for case in cases:
        case_id = str(case["case_id"])
        factor = factors_by_case.get(case_id)
        n_value = int(case["N"])
        if factor is None:
            status = "missing_audit_factors"
        elif int(factor["p"]) * int(factor["q"]) == n_value:
            status = "integrity_pass"
        else:
            status = "integrity_fail"
        rows.append(
            {
                "case_id": case_id,
                "bits": int(case["bits"]),
                "N": n_value,
                "audit_integrity_status": status,
            }
        )
    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    """Write audit integrity rows with LF line endings.

    Inputs:
        `rows` are audit integrity dictionaries and `path` is the CSV target.

    Outputs:
        Writes the CSV header and rows. If there are no rows, only the header is
        written with the fixed audit schema.
    """
    fieldnames = ["case_id", "bits", "N", "audit_integrity_status"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse audit input and output paths.

    Inputs:
        `argv` is an optional command-line argument list for tests or CLI use.

    Outputs:
        Returns an argparse namespace with cases, factors, and output paths.
    """
    parser = argparse.ArgumentParser(description="Run RSA v2 audit integrity checks.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--factors", type=Path, default=DEFAULT_FACTORS_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run physically separate fixture integrity audit.

    Inputs:
        `argv` may provide `--cases`, `--factors`, and `--output` paths.

    Outputs:
        Writes integrity CSV rows and returns process status `0`.
    """
    args = parse_args(argv)
    rows = audit_integrity_rows(read_jsonl(args.cases), read_jsonl(args.factors))
    write_csv(rows, args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### 7. `run_experiment.py` (PGS inference runner – currently unresolved scaffold)
```python
#!/usr/bin/env python3
"""Experiment-runner scaffold for the RSA-260 PGS v2 experiment.

Purpose:
    Reserve the command-line entry point that will later apply a reviewed PGS
    rule to public N-only case rows.

Inputs:
    The future runner will read public case rows only. It must not read audit
    factors or hidden-factor data.

Outputs:
    The future runner will write unresolved rows until the PGS rule is supplied.

Placeholder status:
    No PGS inference rule is implemented in the scaffold phase.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_CASES_PATH = Path("research/06-cryptology-rsa/experiments/rsa/v2/cases.jsonl")
DEFAULT_OUTPUT_PATH = Path("research/06-cryptology-rsa/experiments/rsa/v2/unresolved_rows.jsonl")
UNRESOLVED_REASON = "pgs_rule_not_specified"


def apply_user_specified_pgs_rule(case: dict[str, object]) -> dict[str, object]:
    """Represent the future reviewed PGS rule.

    Inputs:
        `case` is one public N-only row.

    Outputs:
        Raises `NotImplementedError` until the user states the PGS rule in
        ordinary language and it is reviewed against `AGENTS.md`.
    """
    raise NotImplementedError("PGS rule has not been specified")


def read_public_cases(path: Path) -> list[dict[str, object]]:
    """Read public N-only case rows from LF-delimited JSON.

    Inputs:
        `path` points to a JSONL file whose rows contain public case fields.

    Outputs:
        Returns parsed dictionaries. This function does not read audit data.
    """
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def unresolved_row(case: dict[str, object]) -> dict[str, object]:
    """Create the unresolved output row for one public case.

    Inputs:
        `case` is one public N-only row containing `case_id`, `bits`, and `N`.

    Outputs:
        Returns a row that makes the missing PGS rule explicit without reporting
        survivor counts, factor ranks, certificates, or inferred factors.
    """
    return {
        "case_id": case["case_id"],
        "bits": case["bits"],
        "N": case["N"],
        "status": "unresolved",
        "unresolved_reason": UNRESOLVED_REASON,
    }


def run_cases(cases: list[dict[str, object]]) -> list[dict[str, object]]:
    """Run public cases through the placeholder PGS rule.

    Inputs:
        `cases` is a list of public N-only dictionaries.

    Outputs:
        Returns explicit unresolved rows until `apply_user_specified_pgs_rule`
        is replaced by a reviewed PGS rule.
    """
    rows: list[dict[str, object]] = []
    for case in cases:
        try:
            rows.append(apply_user_specified_pgs_rule(case))
        except NotImplementedError:
            rows.append(unresolved_row(case))
    return rows


def write_jsonl(rows: list[dict[str, object]], path: Path) -> None:
    """Write LF-delimited JSON experiment rows.

    Inputs:
        `rows` are unresolved experiment rows and `path` is the output file.

    Outputs:
        Writes deterministic JSONL with sorted keys and LF line endings.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse runner input and output paths.

    Inputs:
        `argv` is an optional command-line argument list for tests or CLI use.

    Outputs:
        Returns an argparse namespace with public case and output paths.
    """
    parser = argparse.ArgumentParser(description="Run RSA v2 unresolved scaffold rows.")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Load public cases and write explicit unresolved rows.

    Inputs:
        `argv` may provide `--cases` and `--output` paths.

    Outputs:
        Writes unresolved JSONL rows and returns process status `0`.
    """
    args = parse_args(argv)
    write_jsonl(run_cases(read_public_cases(args.cases)), args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### Quick Start Instructions
1. Save all files exactly as shown (preserve directory structure).
2. Run the fixture builder:  
   `python3 build_ladder_fixtures.py`
3. Run the audit (always first):  
   `python3 audit_experiment.py` → creates `research/06-cryptology-rsa/experiments/rsa/v2/audit_integrity.csv` (should show "integrity_pass").
4. Run the experiment (inference only):  
   `python3 run_experiment.py` → creates `research/06-cryptology-rsa/experiments/rsa/v2/unresolved_rows.jsonl` (expected until you implement the reviewed PGS rule in `apply_user_specified_pgs_rule`).

The 40-bit ladder is now a clean, reproducible calibration surface. Once you state and implement the **Reciprocal Reset Deadline Lock Rule** (as described in the strategy file) inside `run_experiment.py`, the runner will produce resolved rows that the audit can independently verify.
