# Final V2 Cross-Audit Report - Public Selector Experiment

## Contract

The controlling contract is:

```text
../residue_certificate_v2_public_selector_contract.html
```

The experiment tested a public certificate-ranking rule, not numeric factor discovery. The V1 certificate layer stayed frozen. V2 added the leftmost minimum-divisor witness and reciprocal deviation ranking over the V1 48-residue certificate.

## Final Classification

The two-part experiment is classified as `invalidated_result`.

Both independent implementations were admissible. Both produced the same aggregate measured behavior:

- true certificate cardinality: 48 on every case;
- rotated control certificate cardinality: 0 on every case;
- deterministic synthetic control certificate cardinality: 0 on every case;
- structural wins by true `p % M`: 0 of 20;
- final classification: `invalidated_result`.

The V2 ranking hypothesis is falsified on the frozen 20-case surface.

## Grok Execution

Part One directory:

```text
part-01-grok-performs-codex-audits/
```

Grok produced:

- `reciprocal_shadow_v2_public_selector_probe_grok.py`
- `output/summary.json`
- `output/certificate.jsonl`
- `output/runtime_residue_crt_log.jsonl`
- `output/summary.md`
- `self_checklist.md`
- `grok_execution_notes.md`

Part One measured result:

- 20 cases executed.
- `M = 210` and selected factors `[2, 3, 5, 7]` on every case.
- True certificate cardinality was 48 on every case.
- Both controls were empty on every case.
- Minimal structural key tie size was 2 or 4 on every case.
- True `p % M` was the unique structural winner in 0 cases.
- Aggregate classification was `invalidated_result`.

## Codex Audit

Codex classified Part One as admissible `invalidated_result`.

Audit evidence:

- No hidden `p`, `q`, or `N` appeared inside certificate generation or V2 ranking.
- No candidate interval, prime stream, segmented sieve, root walk, `gcd(candidate, N)`, `N % candidate`, divisibility gate, product closure, random control, or unfixed threshold appeared in the inference path.
- V1 certificate members were produced by conflict-check plus CRT.
- GWR witness extraction matched the V2 contract.
- V2 deviation ranking matched the contract.
- Final `p % M` audit occurred only after all structural scores existed.

## Codex Execution

Part Two directory:

```text
part-02-codex-performs-grok-audits/
```

Codex produced:

- `reciprocal_shadow_v2_public_selector_probe_codex.py`
- `output/summary.json`
- `output/certificate.jsonl`
- `output/runtime_residue_crt_log.jsonl`
- `output/summary.md`
- `self_checklist.md`
- `codex_execution_notes.md`

Part Two measured result:

- 20 cases executed.
- `M = 210` and selected factors `[2, 3, 5, 7]` on every case.
- True certificate cardinality was 48 on every case.
- Both controls were empty on every case.
- Minimal structural key tie size was 2 or 4 on every case.
- True `p % M` was the unique structural winner in 0 cases.
- Aggregate classification was `invalidated_result`.

## Grok Audit

Grok classified Part Two as admissible `invalidated_result`.

Grok accepted:

- construction/audit separation;
- V1 conflict-check plus CRT layer;
- Section 6 GWR witness extraction;
- Section 7 V2 deviation formula;
- final `a` as a reporting tie-break only;
- all three controls;
- required artifact fields and runtime logs.

Grok rejected the V2 selector hypothesis because the measured surface produced 0 of 20 structural wins.

## Agreement

The independent implementations agree on all classification-critical behavior:

- both controls empty in all cases;
- true certificate has 48 residues in all cases;
- true `p % M` has 0 unique structural wins;
- minimal structural key is tied in every case;
- final classification is `invalidated_result`.

This is stronger than a mere implementation mismatch. The same hypothesis failed in both independently audited lanes.

## Accepted Measured Result

No accepted measured result exists for the V2 public selector.

The accepted measured statement is:

> Under the frozen V2 contract, the leftmost minimum-divisor reciprocal deviation ranking does not isolate the hidden factor residue on the first 20-case surface. Both independent runs produced 0 of 20 unique structural wins while controls remained empty.

## Invalidated Finding

The invalidated hypothesis is:

> Ranking the V1 48-residue certificate by the leftmost minimum-divisor witness deviation `(dev_primary, support_score)` supplies a tight public residue selector.

The failure mode is specific:

- the V1 layer still distinguishes true web from controls;
- the V2 ranking partitions the 48 residues;
- the minimal structural key is always tied;
- the true residue is never the unique structural winner.

## Unresolved Next Step

The next research target is not to tune the support threshold or relax uniqueness. Those moves would weaken the falsification boundary.

The next valid target is a new public selector object or a new public modulus selection rule that changes the information being read, while preserving:

- no hidden factors in generation or ranking;
- no candidate walks;
- no prime streams or root scans;
- no divisibility, product-closure, or `gcd(candidate, N)` inference gates;
- deterministic controls;
- cross-audit before any accepted claim.
