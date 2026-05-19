# Research Meeting Opening - Minimal Sparse Web-Weaving

## Agenda

Reiterate the user's sparse multiplicative-web objective to Grok, review the literal-web evidence, and negotiate one concrete deliverable: a toy-scale experiment contract for the cheapest sparse web-weaving method that still preserves factor-thread evidence.

## User Starting Material, Preserved Verbatim

What I want to do is eventually scale thi method to the known, solved RSA challenges.

So, I want to design the tests to be as RSA like as possible.

In order to have any chance at all of scaling, the method needs to be as efficient as possible:

- No umecessary computations. 
- We should perform the minimum number of factorizations of the composites surrounding N as possible to create the "we" with enough "threads" to enable factor inference.
- We should use cheap, small factorizations, like dividing by 2 and stop as sson as possible.
- I'm open to other methods of "fast and cheap" ways to create that inference web.

Yes, correct. We should start at the toy scales we're doing now to determine what is the minimal sparse, fast and cheap web-weaving method we can employ that still produces the factor thread evidence.

## Reiteration For Grok

The user is not asking for another modular ranking system, another residue certificate, or a full local factorization sweep.

The object is the literal multiplicative web around a semiprime `N = p*q`:

- offsets `t` around `N`;
- nearby composites `N + t`;
- cheap public factor-thread evidence extracted from those composites;
- missing slots implied by repeated public threads;
- audit-only labels showing whether those missing slots correspond to held-out `p` or `q` thread rows.

The current full-web baseline factors all nearby composites in a window, holds out direct `p/q` rows, and shows that public factor threads still point to the hidden-thread holes.

The next research question is:

> How little public thread evidence is required to preserve that same factor-thread signal?

The toy-scale job is to deliberately degrade the full web:

- inspect fewer offsets;
- extract fewer factors per inspected composite;
- prefer cheap small-factor tests;
- stop extracting from a composite as soon as it contributes enough thread evidence;
- avoid complete factorization unless used only as a tiny baseline or audit comparison.

A sparse method succeeds if it still produces the factor-thread evidence:

- supported missing offsets;
- top supported holes dominated by held-out `p/q` thread rows;
- enough repeated public threads to reconstruct the hidden-thread pattern seen in the full literal web.

A sparse method fails when the cheap partial web no longer preserves that hidden-thread evidence.

## Current Evidence And File Paths

Repository root:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure
```

Literal-web finding:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/README.md
```

Full literal web script:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace.py
```

Scale ladder:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/literal_web_hole_trace_ladder.py
```

Measured ladder summary:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/output/literal_web_hole_trace_ladder/summary.md
```

Measured result:

- The literal full-web method works on all tested rungs through `8009 x 10007`.
- The signal did not fail before the current feasibility cap.
- The first wall is cost: the method currently needs a wide composite-factorization window.

## Boundaries

Stay inside the literal-web frame:

- no modular ranking;
- no residue certificate layer;
- no candidate search over possible factors;
- no `gcd(candidate, N)` inference;
- no `N % candidate` inference;
- hidden `p` and `q` are audit-only;
- any proposed sparse method is a hypothesis until tested;
- keep theorem/proof status separate from measured toy evidence.

## Requested Grok Role

Apply your maximum available reasoning.

Opine first on the reiterated objective: finding the minimal sparse, fast, cheap web-weaving method at toy scale that still produces factor-thread evidence. Then propose or negotiate one concrete meeting deliverable.

The deliverable should be specific enough that Codex can implement it later without inventing the experiment design. Good deliverables include:

- a sparse-web experiment contract;
- a falsification test for sparse web evidence;
- a staged minimality ladder over offset sampling and partial factor extraction;
- a clear statement of which cheap observations should be tested first.

After your opening opinion and proposed deliverable, ask exactly one question for Codex to answer before the next round.
