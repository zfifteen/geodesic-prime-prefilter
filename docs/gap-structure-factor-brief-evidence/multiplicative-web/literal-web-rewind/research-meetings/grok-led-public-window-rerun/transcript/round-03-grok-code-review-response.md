# Grok Code Review Response: Adaptive Alphabet V3

## Findings

### 1. Public Runner Leakage

Grok found no hidden factor leakage in `public_adaptive_alphabet_runner.py`.

The public entry point receives only `n`, and policy constants are hardcoded public values:

- `PUBLIC_THREAD_PREFIXES`
- `PUBLIC_RADII`
- `PUBLIC_TOP_K`

Grok found no `p`, `q`, factor expressions, or secret-dependent logic in the public module. The emitted public JSON records carry `"public_only": true`.

### 2. Private Audit Boundary

Grok found that `private_adaptive_alphabet_audit.py` keeps `p/q` post-freeze only.

The audit constructs `n = p * q`, calls the public runner with only `n`, writes the public result to `public_frozen/`, and only then constructs target offsets for scoring.

### 3. Ranking Logic Status

Grok classified the ranking logic as a valid measurement of one specific heuristic:

```text
support count, signature rarity, signature weight, then proximity
```

It does not prove an adaptive-alphabet law. The v3 regression on the second continuation case is a legitimate falsification of this particular rank function under alphabet growth.

### 4. Strongest Flaw

Grok's strongest methodology objection:

The current apparatus is still a classical additive-window divisibility measurement, not a PGS-native object or invariant. It is valid as a boundary measurement of this heuristic, but it is not evidence for a PGS-native factor selection rule.

Grok's strongest code-level flaw:

The private audit duplicated the public ranking and signature-counting machinery. If the public policy changed in one file but not the audit, the full-rank audit numbers could silently diverge from the public ranking rule.

### 5. Requested Concrete Fix

Grok requested this fix:

```text
Extract the pure-public nomination and ranking machinery into one shared public policy module, then have both the public runner and private audit import it.
```

The audit should remain a post-freeze consumer and use `p/q` only for lookup and classification.
