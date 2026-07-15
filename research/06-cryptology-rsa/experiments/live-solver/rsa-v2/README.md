# RSA v2 Strategy Memory For Codex

This file is operational memory for future Codex sessions working inside
`research/06-cryptology-rsa/experiments/rsa/v2`. It is written for Codex, not as a package README.

For a fresh session, start with:

```text
SESSION_BOOTSTRAP.md
```

## Current State

The live v2 runner is a reciprocal PGSPG endpoint-chain resolver.

It starts at the previous public endpoint before `isqrt(N)` and treats that as
step zero of a single lower endpoint-chain traversal. At each step it derives
one lower PGSPG reset certificate, chooses the oriented transport coordinate,
transports through `floor(N / x)`, derives the opposite-side certificate, and
evaluates the fixed closure predicates. Strict reset closure is evaluated
first. Deadline-signature correction is evaluated second: a failed upper reset
transports back to one corrected lower endpoint, and that endpoint must
mutually close with the upper reset deadline while carrying the same public
reset signature.

This replaced two invalid solver shapes:

- a fixed additive chamber around `isqrt(N)`;
- a budgeted walk through many lower endpoints.

The square root is now an orientation coordinate only. It does not define a
candidate chamber, and it does not limit the possible factor distance. The
square-root chamber is not a separate mode; it is the first endpoint-chain
state.

## Active Grammar Evidence Track

The active grammar track is separate from the official runner. It is evidence
gathering for future PGS-native compatibility and exclusion rules.

Current strongest measured grammar finding:

```text
inverse recursive grammar appears as component sharing with ordered-word
exclusion.
```

Measured result:

```text
global scope:
  solved rows: 48
  lag-2 hits: 30
  lag-3 hits: 29
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 40

public-cell scope:
  solved rows: 48
  lag-2 hits: 14
  lag-3 hits: 11
  lag-2 + lag-3 word hits: 0
  component-sharing word exclusions: 22
```

Interpretation:

```text
Solved rows reuse recursive pieces from the deterministic expanded surface, but
avoid the expanded surface's ordered lag-2 + lag-3 reduced words.
```

This is a measured grammar result, not a proof and not a resolver.

Primary artifacts:

```text
TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md
PGS_GRAMMAR_EVIDENCE_FINDINGS.md
GRAMMAR_EVIDENCE_STATUS.md
GRAMMAR_PATTERN_SCAN.md
INVERSE_WORD_EXCLUSION_FINDING.md
grammar_inverse_word_exclusion_probe.py
output/grammar_inverse_word_exclusion/
output/fresh_rsa_challenge_inverse_word_exclusion/
```

## Active Transported Story Law Track

The strongest current transported-story measurement is:

```text
transported_story_law_v1:
  row_count = 512
  ledger_effective_survivor_count = 202
  recursive_row_count = 713
  recursive_final_survivor_count = 0
```

This is measured public evidence, not a theorem and not a resolver promotion.
The next mathematical task is recorded in:

```text
TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md
```

That artifact names the Prefix Non-Rewrite, Suffix Strict-Descent, Recursive
Anchor Recurrence, and Grammar Projection lemmas required to derive the sidecar
predicates from GWR/NLSC.

Current narrowed proof target:

```text
DirectFrontier(C, C') := FreshEndpoint(C') and Psi(RB(C, C'))

RB(C, C') =
(
  R(C, C'),
  source_closed_count - source_tail_count,
  induced_closed_count - induced_tail_count
)
```

`Psi(RB)` must be a public structural chamber-balance language, not an observed
class lookup. The measured guards for carrier-local prefix/threat equivalence,
typed material antecedents, and direct RB separation are in
`research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py`.

Current proof status:

```text
RB Sufficiency Sublemma: measured support guarded, structural proof missing
Carrier Localization Under Reciprocal Transport: structural proof missing
Psi(RB) structural definition: missing
PrefixMaterial(C, C') => not Psi(RB(C, C')): unproved
ThreatMaterial(C, C') => not Psi(RB(C, C')): unproved
FreshEndpoint recurrence boundary: separated from Psi(RB)
transported-story resolver promotion: separate from the live deadline
  correction rule
```

The minimal falsification condition for any proposed `Psi(RB)` is:

```text
there exists a public certificate pair (C, C') with
  PrefixMaterial(C, C') or ThreatMaterial(C, C')
  and Psi(RB(C, C'))
```

That falsifies the typed exclusion theorem for the proposed `Psi`. It does not
falsify local GWR/NLSC.

## Live Front Door

The live front door is:

```text
public N
-> isqrt(N) as orientation
-> previous public endpoint before isqrt(N)
-> PGSPG reset certificate on the lower side
-> y = floor(N / lower.reset_endpoint)
-> previous public endpoint before y
-> PGSPG reset certificate on the upper side
-> reciprocal reset-closure check
-> if reset closure fails, one upper-deadline correction check
-> refined public certificate-geometry acceptance
-> public endpoint class or unresolved
```

The runner never reads audit factors.

## PGSPG Concepts Carried Forward

The factorizer uses the PGS Prime Generator as the local state engine:

- public endpoint anchors;
- wheel-open offsets;
- exact divisor-count interval state;
- GWR carrier state;
- chamber reset;
- tail and threat reset-deadline fields;
- explicit unresolved states.

The factorizer does not place factorization logic inside the generator. It calls
the generator's chamber-reset certificate as a read-only local state adapter.

## Current Output

For each public `N`, the runner writes:

- `inference_rows.jsonl`;
- `survivor_rows.jsonl`;
- `summary.json`.

The current official rungs return:

```text
rsa_v2_40bit_static_001 -> endpoint_class_by_reciprocal_deadline_signature_correction
rsa_v2_50bit_static_001 -> unresolved_by_reciprocal_carrier_misalignment
rsa_v2_64bit_static_001 -> endpoint_class_by_mutual_certificate_closure
```

These residual/closure codes are the **rsa-v2 runner** pin. The 50-bit row stays
unresolved (no public endpoint class). On the **rsa-v3** residual stack the same
fixture migrates further under public geometry (dual-gap D → first-tail → joint
cell `C1T2L1`) while remaining unresolved; see
`../rsa-v3/output/residual_cell_C1T2L1/` and `../rsa-v3/RESIDUAL_TAXONOMY.md`.

The runner still does not read audit factors. Downstream audit currently reports
`factor_found = true` for the 40-bit and 64-bit rows. The 50-bit row is
unresolved before audit and does not emit a public endpoint class.

The current implementation shape is:

```text
UNIFIED_TRANSPORTED_CERTIFICATE_CHAIN
```

See `ORIENTED_ENDPOINT_CHAIN_BASELINE.md` for the historical linear baseline
and recursive jump comparison target.

Use `OECC_IMPROVEMENT_CHECKLIST.md` to track efficiency, scalability, law
clarity, and candidate-law experiments after the old OECC_LINEAR_V1 control
shape.

## Invalid Rules

Do not restore these as live selection rules:

- fixed `isqrt(N) +/- radius` candidate generation;
- endpoint-walk budgets as solver coverage;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive lock rounds that revisit the same reset endpoint;
- ranking by closeness to `isqrt(N)` as evidence of correctness;
- product closure as the PGS contraction rule.

## Arithmetic Boundary

Coordinates are carried as `gmpy2.mpz`, and divisor-count interval measurement
enters through the shared exact interval helper:

```text
divisor_counts_segment(lo, hi)
```

The RSA v2 runner does not carry a modulus-bit cutoff. Backend capability is a
property of the shared interval engine, not an RSA-local branch.

## Rung Extension Workflow

Rungs are data, not code.

Add public rungs to `ladder_spec.json`. Add audit endpoints separately to
`audit_spec.json` only when audit certification is available. The runner never
reads audit data.

Starting at RSA-100, use the public RSA Challenge moduli recorded in:

```text
RSA_PUBLIC_MODULI_THROUGH_260.md
```

The current runner will explicitly return unresolved for larger rungs until a
GMP interval backend exists.

## Next Live Work

The next mathematical task is:

```text
prove or falsify the typed transported non-rewrite law stated in
TRANSPORTED_STORY_LAW_PROOF_OBLIGATIONS.md:

prefix + lower/equal lock label => committed-prefix rewrite, not new frontier
suffix + lower lock label + deadline=threat => committed-threat-horizon rewrite,
  not new frontier
repeated recursive frontier anchor => recurrent frontier material, not new frontier
```

Until those lemmas are proved and reviewed, the correct official output is
unresolved.

Before substantial implementation, use the continuity and shape contract:

```text
research/00-index/continuity/continuity_and_shape_contract.md
```

The canonical repository bootstrap is:

```text
research/00-index/continuity/START_HERE.md
```

For this experiment, Grok should be used as research review before major rule
changes, with code, outputs, failed assumptions, and current hypotheses included
in the prompt.

Record substantial Grok collaborations in:

```text
research/06-cryptology-rsa/experiments/rsa/v2/grok_sessions/
```
