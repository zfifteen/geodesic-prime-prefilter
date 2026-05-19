# Grok Code Review Request: Adaptive Alphabet V3

Codex implemented a new runner with adaptive window and adaptive thread alphabets under the last valid Grok contract.

Please perform a code review, not a design cheerlead.

Review paths:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/public_adaptive_alphabet_runner.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/private_adaptive_alphabet_audit.py
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/grok-led-public-window-rerun/output/audit_adaptive_alphabet_v3/summary.md
```

Public contract:

- Public runner receives only `N` and public constants.
- Public thread prefixes are hardcoded small-prime tuples.
- Public radii are hardcoded powers of two.
- Public ranking is support count, signature rarity, signature weight, then proximity.
- Private audit uses `p/q` only after public output is frozen.

Measured result:

```text
toy_23x31: hit rank 2 at R=256, threads=3
toy_43x59: hit rank 3 at R=256, threads=3
toy_61x83: hit rank 6 at R=256, threads=3
toy_89x113: hit rank 8 at R=256, threads=3
continuation_00_131101x144203: no top-1000 hit, best final full rank 10079
continuation_01_1048583x1153441: no top-1000 hit, best final full rank 669144
```

Known concern:

The v3 policy appears to make the second continuation case worse than v2 because adding thread alphabets creates many higher-support or rarer public signatures that outrank the factor offset. That may mean the adaptive alphabet idea is correct but the rank function is wrong.

Review questions:

1. Does the public runner leak hidden factor information?
2. Does the private audit keep `p/q` post-freeze only?
3. Is the ranking logic methodologically valid for testing adaptive alphabets?
4. What is the strongest code-level or methodology-level flaw?
5. What one concrete fix should Codex make next, if any?

Return findings first, with file/line references if possible.
