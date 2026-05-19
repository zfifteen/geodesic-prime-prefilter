# Grok Compliance Certification

Status:

```text
certified_compliant
```

Grok certified that the new factor-recovery contract implementation
(`public_n_only_nomination_runner.py` plus `canonical_membership_audit.py`) and
the 128-bit / 256-bit reruns under `recovery_contract_128bit/` and
`recovery_contract_256bit/` adhere to the public evidence integrity contract
and the six-gate prevention contract for instruction-following and
oracle-contamination prevention.

## Certified Points

- Public N-only phase separation: `public_n_only_nomination_runner.py` contains
  no references to private factor fields and runs from `N` alone.
- Public freeze before private audit: both rungs produced frozen
  `public_output.jsonl` and `public_manifest.json` before canonical audit.
- Canonical membership checker only: `canonical_membership_audit.py` loads
  frozen public distances, reads the two hidden audit factors from the command
  line, performs direct membership tests, and emits `recovered` or `missed`.
- Audit outputs: both 128-bit and 256-bit status files report `missed`.
- Narrative discipline: `recovery_contract_rerun_summary.md` uses only
  contract-allowed labels and explicitly invalidates the prior rank-audit
  artifacts as recovery evidence.
- Quarantine: no post-freeze private-factor sidecar, rank study, containment
  measurement, band measurement, or visualization exists inside the
  `recovery_contract_*/` trees.
- Input hygiene: `cases/public_128_256.jsonl` supplies only `N` values.

## Grok Residual Risks

- Pre-freeze oracle influence on public-rule design remains possible in
  principle.
- The public-freeze and post-freeze gate printouts were made in the chat and
  certification request, but the gate records are not yet separate machine
  artifacts for each run.
- The canonical checker emits membership-derived helper fields
  (`p_emitted`, `q_emitted`, `recovered_factor`), which Grok treated as a minor
  literal expansion because they do not enable ranking, scoring, containment, or
  recovery promotion.
- Cross-session or out-of-tree smuggling of private measurements remains
  outside the scope of the pinned artifacts.

## Certification Conclusion

No violations of required order, quarantine, canonical-only audit, or
status-label discipline were found in the reviewed files.

The 128-bit and 256-bit reruns are admissible as `missed` evidence under the
contract. The prior anchor-band scale claims remain invalidated for recovery
purposes.
