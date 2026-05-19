# Round 2 - Grok

**Deliverable complete - design contract frozen**

The Codex Round-1 answer has been converted into the single required artifact:

**`docs/gap-structure-factor-brief-evidence/multiplicative-web/research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html`**

It is a self-contained, implementation-ready HTML contract (embedded CSS,
tables, checklists, visual hierarchy) that a future Codex session or witness
can open from `file://` and follow without reconstructing chat context.

**How the answer was incorporated**

- Modulus-link closure = transport plane (the per-thread `b = (-t * inv(a, r)) mod r`).
- Reciprocal Residue Closure Invariant (exact Codex definition sketch) recorded as **unresolved invariant**, not proved rule.
- Hierarchy stated exactly: modulus-link closure (transport), reciprocal residue closure (selector), endpoint-chain traversal (downstream audit).
- First target changed from "find the numeric factor" to the weaker, cleaner structural-certificate test: "Can the field emit a compact residue certificate whose class contains p on the true web and does not contain p at equal rank or cardinality on the rotated-offset control?"
- No claim of numeric discovery is permitted in the v1 probe.

**Concrete v1 operationalization fixed in the document**

- Highest-degree 4 (or fallback 3) distinct `r` values from the held-out threads define `M = product(r)`.
- For every `a` mod `M`: per-`r` conflict check on the transported `b` predictions (all threads using the same `r` must agree on one `b`), then incremental CRT merge across the `b_r` values to a single consistent partner class `y`.
- Admissible = zero-conflict full merge. Certificate `C` = the expected tiny list of such `a`, ranked by closure coverage of the threads.
- Identical procedure on the rotated-offset control produces `C_rot`.
- Audit (`p`, `q` only here): does `p % M` appear in `C` at rank 1 and not in `C_rot` at comparable rank/cardinality?

This is pure residue arithmetic on the thread list. No integer candidate, no
interval, no `round(N/x)`, no `gcd` or divisibility against `N` until the final
membership test on known test cases.

**Supporting meeting artifacts written**

- `minutes.md` - full context, participants, agenda, negotiated deliverable, Round-1 log, candidate insights, falsification tests, convergences, unresolved questions, next move.
- `transcript/round-01-codex.md` - verbatim Codex answer and classifications.

**Classifications**

- 16/16 exhaustive ranking - **measured result** (enumerated-surface regime only; valid calibration and rotated control).
- 48-bit ladder plus blind restart - **boundary measurement**.
- 52-64-bit hidden-p ladder - **invalidated result**.
- Reciprocal Residue Closure Invariant - **unresolved invariant**.
- "Web selects via shadow" (general) - **hypothesis**.
- Residue-certificate emission test - **proof target** (first surface).

**Next move**

Write `reciprocal_shadow_residue_certificate_probe.py` (no more than 220 lines,
re-using the existing thread, hold-out, and rotated machinery) strictly against
the 7 sections plus 2 appendices in the HTML. Run the first surface (original
16 cases plus 4 natural-ratio cases with `sqrt(N) > 10M`). Only after the
implementation witness signs the 12-item acceptance checklist (static source
audit, runtime log of every residue/CRT step, natural ratios, `|C| <= 64`,
rotated plus synthetic controls, etc.) may any numbers be treated as evidence.

The design contract is now the durable artifact. The invariant remains open for
later strengthening; the HTML is the current frozen execution surface.

No further question required. The deliverable had no unresolved choice once the
exact invariant and the structural-certificate target were incorporated and the
v1 closure procedure was made mechanically auditable.
