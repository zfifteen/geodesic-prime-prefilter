# Certified Finite Base Schema (R2)

This schema defines the standard JSON artifact required for any computational enumeration used as a premise in `PROOF.md`. A finite base is considered `finite-certified` only if a corresponding valid JSON certificate and its hashed artifact exist and are reproducible.

## Objective

To establish a strict epistemic boundary between analytic proofs and finite computations. The universal theorems in `PROOF.md` are completed by the analytic arguments together with the exhaustive verification recorded in the certificates.

## JSON Schema Requirements

Every certificate must include the following fields:

- `lemma_id`: (string) The identifier mapping to the `PROOF.md` anchor.
  - Examples: `gwr_finite_base_v1`, `bounded_compression_base_v1`, `residual_k128_v1`.
- `range`: (object) The domain evaluated.
  - Examples: `{"p_min": 2, "p_max_exclusive": 5000000001}` or `{"q_max_exclusive": 8886111}` or `{"k_max": 128}`.
- `counts`: (object) Verification metrics.
  - `gaps`: The number of prime gaps verified.
  - `earlier_integers`: The number of earlier integers checked (if applicable).
  - `failures`: The number of counterexamples found (must be 0 for certification).
- `failure_examples`: (array) A list of counterexamples. If `failures > 0`, this array is populated. A non-empty array blocks certification.
- `generator`: (object) Provenance of the script used to generate the artifact.
  - `script_path`: Path to the verification script.
  - `commit_hash`: The Git commit hash of the script at the time of execution.
  - `params`: Any specific CLI arguments or parameters used.
- `artifact_hash`: (string) The SHA256 hash of the full output table/artifact.
- `verified_at`: (string) ISO-8601 timestamp of the verification run.

## Emission

Regenerate all certificates from pinned `PROOF.md` audit counts:

```bash
python3 docs/proof-enhancements/scripts/emit_certificates.py
```

## Example Certificate

```json
{
  "lemma_id": "gwr_finite_base_v1",
  "range": {
    "p_min": 2,
    "p_max_exclusive": 5000000001
  },
  "counts": {
    "gaps": 220336055,
    "earlier_integers": 826172978,
    "failures": 0
  },
  "failure_examples": [],
  "generator": {
    "script_path": "research/02-gwr-dni/scripts/proof/verify_gwr.py",
    "commit_hash": "a1b2c3d4...",
    "params": "--max-p 5000000000"
  },
  "artifact_hash": "sha256-hash-here",
  "verified_at": "2026-07-07T12:00:00Z"
}
```
