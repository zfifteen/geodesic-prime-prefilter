# Codex Audit - Part One

**Experiment lane:** Part One - Grok performs, Codex audits  
**Performer source:** `reciprocal_shadow_residue_certificate_probe_grok.py`  
**Raw outputs:** `output/summary.json`, `output/certificate.jsonl`, `output/runtime_residue_crt_log.jsonl`, `output/summary.md`  
**Controlling contract:** `../reciprocal_shadow_correct_experiment_design.html`  
**Audit classification:** `boundary_measurement`

## Audit Result

Part One is admissible as a boundary measurement. It is not an accepted measured result for factor-residue selection.

The implementation produced the required raw artifact classes, used deterministic true/rotated/synthetic surfaces, and kept the certificate generator separated from final `p % M` membership audit. The observed certificate behavior is weaker than the target: every case selected `r = [2, 3, 5, 7]`, `M = 210`, and the true certificate contained exactly the 48 residues coprime to 210. This contains `p % M`, but it does not rank it tightly. The result therefore measures a closure boundary of the defined rule, not a successful selector.

## Source Audit Evidence

- `compute_residue_certificate` receives held-out rows, a case label, and a surface label. AST inspection found no `p`, `q`, `N`, `isqrt`, `gcd`, `isprime`, or `nextprime` names in that function.
- `build_case` uses `p` and `q` for benchmark construction and direct-row holdout. This is an allowed role under the contract.
- `main` uses `p` only after all three certificates are produced, for `p % M` membership and rank audit. This is an allowed final-audit role.
- Grep inspection found no integer candidate interval, prime stream, segmented sieve, downward `sqrt(N)` walk, `gcd(candidate, N)`, `N % candidate`, or product-closure gate inside the generator path.
- The only `math.isqrt` occurrence is used in `main` to report `p_over_sqrtN`; it is not used for generation, ranking, or admissibility.
- Runtime logs contain one record per admitted residue class and show modular inverse plus CRT arithmetic over offsets and selected thread factors.

## Output Audit Evidence

- Cases executed: 20.
- Surface: original 16 reference cases plus 4 natural-ratio larger cases.
- Low-ratio cases: 4 total, all in the added larger cases.
- Classifications emitted by Grok: 20 `boundary_measurement`.
- True-web certificate cardinality: always 48.
- Rotated-control certificate cardinality: always 0.
- Deterministic synthetic-control certificate cardinality: always 0.
- Selected modulus factors: always `[2, 3, 5, 7]`.
- `p % M` appears in every true-web certificate.
- `p % M` never appears in either control certificate because both controls emit empty certificates.
- True-web rank of `p % M` is mid-range, not a rank-1 or rank-2 nomination.

## Checklist Audit

The self-checklist is substantially faithful to the contract, with two recorded boundaries:

- Checklist item 7 is partial because the original 16 reference cases contain no low-ratio cases. The added 4 larger cases satisfy the low-ratio requirement, but the inherited 16-case surface cannot satisfy the stricter wording in the HTML literally.
- The source is 572 lines, exceeding the contract's stated smallest implementation path target of `<= 220` lines. This does not create hidden-factor leakage, but it is an implementation-form deviation and makes the artifact less compact than requested.

## Codex Classification

Part One is accepted only as `boundary_measurement`.

The rule, exactly as operationalized, distinguishes true offset pairing from the rotated and deterministic synthetic controls, but it does so by collapsing the true certificate to the full coprime class modulo 210. That is structural signal, not factor-residue selection. No accepted measured result exists yet.
