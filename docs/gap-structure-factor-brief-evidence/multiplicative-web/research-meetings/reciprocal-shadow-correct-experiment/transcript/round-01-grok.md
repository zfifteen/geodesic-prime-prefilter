# Round 1 - Grok

**Lead opening - Reciprocal Shadow Correct Experiment**

The agenda is the only honest one possible after the documented failures. The
starting material (the user request plus the three preserved failure statements
plus the exact evidence surfaces) is also accurate and correctly scoped. I will
classify every claim in the supplied packet, then identify the concrete leakage
vectors that any design must mechanically block, then propose the deliverable
with one required sharpening, then ask the single necessary question.

**Claim classifications (verbatim from packet)**

- "fixed-window ranking run scored all prime lower-endpoint candidates in each finite tested surface and ranked p first in 16 / 16 tested semiprimes" - **measured result**, confined to the exhaustive-enumeration regime (N <= 35 026 003, pi(sqrt(N)) small enough to materialize). The rotated-offset control is part of the same measured result and shows the signal is attached to the true offset-to-factor pairing, not the marginal multiset.
- "48-bit candidate-walk ladder and blind restart through 52 bits are not valid factor-selection evidence. They walk public candidates until an audit factor is encountered." - **boundary measurement**, correctly labeled. The 97/100 root bias in build_case plus downward segmented walk from sqrt(N) made the encounter distance artificially short; the coherence number recorded at the hit is therefore not evidence of selection by the web.
- "first 52..64-bit new-rung run used hidden p as candidate-stream lower bound" - **invalidated result**. The line `segmented_prime_flags(p_value, sqrt_n)` and the subsequent `candidate = p_value + offset` are direct, non-auditable use of the secret as a generation bound. The numbers are unusable as inference evidence; they are only usable as failure artifacts.
- "produce an experiment where the reciprocal-shadow field itself defines a compact candidate set, candidate order, certificate, or falsification target, without hidden p/q and without ordinary candidate walking to the factor" - **unresolved** (the live proof target for this meeting). No current artifact supplies such a generator.
- The 16/16 result "supports the indirect-web hypothesis" - **hypothesis** when extrapolated beyond the enumerated surface; it is only a measured existence proof inside that surface.
- "The next stricter version should infer the partner residue from the vote field itself" - **hypothesis** for a stronger protocol; the current probe still uses the classical `round(N / candidate)` hyperbola estimate inside scoring.

**Leakage, circularity, and invalidity vectors identified**

1. **Hidden-factor leakage (already executed)**: any numeric expression after `build_case` returns that contains the value of p or q, or any interval whose lower or upper bound is a function of p or q. The 64-bit ladder is the canonical instance.
2. **Ordinary candidate-walk leakage (already executed)**: any generator whose public interval or sequence is independent of the concrete thread residues and offsets of the web for that N, when the length of the interval is large enough that p is statistically guaranteed to appear inside it. The blind restart and the 48-bit ladder (even after the p-bound was removed) are instances. The 97/100 construction bias is a second-order form of the same error: it shrinks the walk distance by construction.
3. **Secondary-key bias leakage (latent in the "good" probe)**: the sort key `abs(candidate - sqrt(N))` in `candidate_rows_for_case` privileges the near-square-root band. Any future generator that preferentially emits candidates near sqrt(N) re-creates the same trivial band that the ladders exploited.
4. **Exhaustive-surface circularity**: "score every prime <= sqrt(N) then ask whether p wins the sort" is valid measurement when pi(sqrt(N)) is tiny; it is not a selector when pi(sqrt(N)) is 10^8 or larger. The design must treat the 16/16 result as a signal-strength calibration, not as the inference procedure itself.
5. **Factor-API leakage during web construction**: the `composite_rows` / `factorization` calls on N +/- t for fixed t = 300 are part of building the input object (the local multiplicative web). They are allowed for that purpose only. Any code that treats the difficulty of factoring those rows as "progress toward factoring N" or that uses the same factoring primitive on candidate lower endpoints is mixing the layers.
6. **Inference-gate leakage**: any `gcd(candidate, N)`, `N % candidate`, `is_prime` used as an early-accept or pruning rule inside the generator or scorer, or any product-closure test before audit. The current score functions are clean on this point; the new generator must stay clean.
7. **Case-construction leakage**: any test surface whose p/sqrt(N) ratios are artificially concentrated (the 97/100 ladder) or whose p values are the output of the same prime-stream logic later used in scoring. Natural ratios (including p much less than sqrt(N)) are required for the first corrected surface.

All of the above are already visible in the three Python scripts and the three
boundary/invalidated documents. The design must convert them into an auditable
checklist so the implementation witness cannot re-introduce them by
re-interpretation.

**Proposed concrete deliverable (refined)**

The meeting will produce one artifact only:

`research-meetings/reciprocal-shadow-correct-experiment/reciprocal_shadow_correct_experiment_design.html`

(a self-contained HTML file, no external assets, LF endings, openable from file://).

It must contain, in this exact order and with these exact section headings, the
following:

1. The object being measured (one paragraph, PGS-native phrasing: "whether the modulus-link residual state obtained by reciprocal transport across the held-out divisor threads of the fixed-radius local web around a public semiprime N produces a structural certificate - a compact ordered list of lower-endpoint candidates or a residue system - whose scored members place the hidden lower endpoint first by shadow coherence, with certificate cardinality much smaller than pi(sqrt(N))").
2. Allowed and forbidden inputs (two-column table with concrete examples drawn from the invalidated scripts).
3. Candidate-generation or certificate mechanism (must be a pure, deterministic function of the thread list alone; "enumerate primes in any public interval" is explicitly ruled out; the document must name at least one minimal constructive route that satisfies the rule).
4. Exact success condition (per-case and aggregate; must reference both the true web and the two controls).
5. Exact falsification condition (three independent ways the experiment can be declared failed on the first surface).
6. Leakage controls (static source-audit list of 8 forbidden patterns with file:line citations from the three bad scripts, plus runtime logging requirements on every arithmetic step that emits a member of the certificate).
7. Smallest implementation path (a <=250-line probe script contract: re-use of existing `composite_rows` + heldout logic, one concrete generator, scoring only inside the generated set, output schema that includes certificate size and rank, first surface = the original 16 cases + 4 new natural-ratio cases with sqrt(N) > 10^7, plus the exact acceptance checklist of 12 items that the implementation witness will sign off before any numbers are admitted as evidence).

The document must also contain a one-page "forbidden patterns" table and the
12-item acceptance checklist as appendices so they can be printed and used
during code review.

This is the negotiated deliverable. Once Codex records agreement on its exact
contents, the meeting either closes or moves to the single next question
required to hand the spec to an implementer. No code is written during the
meeting.

**The single question**

Which PGS-native object - endpoint-chain traversal or modulus-link closure -
supplies the constructive step that turns the reciprocal-shadow vote field (the
set of (offset, r) threads) into an explicit compact candidate list or residue
system without an external numeric interval? If neither construct is yet
sufficient to name a generator, what is the smallest additional invariant or
transport rule that must be stated in the design before a non-walking procedure
can be specified?

That is the only question. All other elements of the 7-point contract can be
written from the artifacts already present in this folder and the three failure
scripts.
