# Minimal Sparse Web-Weaving Research Meeting Minutes

## Context And Agenda

The meeting reiterated the user's sparse multiplicative-web objective to Grok and converted it into a closed experiment contract.

The object is the literal multiplicative web around `N = p*q`: inspect nearby offsets `t`, extract cheap public factor-thread evidence from composites `N + t`, hold out direct `p/q` rows, and ask whether public thread intersections still make at least one hidden factor thread visible in the supported-hole ranking.

The agenda was to negotiate the cheapest toy-scale web-weaving method that still preserves factor-thread evidence, without returning to modular ranking, residue certificates, full local factorization sweeps, candidate factor search, or hidden-factor leakage.

## Participants And Command Notes

- User: supplied the RSA-like scaling requirement and corrected success criterion: either `p` or `q` is enough to call success.
- Codex: facilitated the meeting, preserved the literal-web frame, corrected the success gate, and wrote this record.
- Grok CLI: served as the external research participant through local `grok` sessions only.

The opening command shape was:

```bash
grok --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --always-approve \
  --prompt-file /Users/velocityworks/IdeaProjects/prime-gap-structure/docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/minimal-sparse-web-weaving/transcript/round-00-opening.md \
  --output-format plain \
  --max-turns 80 \
  --disable-web-search
```

The opening headless run created Grok session `019e40aa-cd89-7000-8a21-0c49bbb349f3` and the first contract draft, but stdout capture failed with:

```text
Internal error: "max_turns exceeded: limit is 80, but got 82 messages"
```

The meeting continued by resuming that exact session id. No Agent Bus or xAI API fallback was used.

## Negotiated Deliverable

The deliverable is a closed toy-scale experiment contract:

```text
docs/gap-structure-factor-brief-evidence/multiplicative-web/literal-web-rewind/research-meetings/minimal-sparse-web-weaving/sparse_web_minimality_contract.html
```

Grok finalized it as `v1.0 Final -- Closed for Implementation`.

The contract is not an implementation and does not claim a theorem. It defines the first sparse literal-web experiment surface and the scoring rules needed for later implementation.

## Round Log

- `round-00-opening.md`: Codex preserved the user's sparse RSA-like requirement verbatim and reiterated it to Grok as a literal-web minimality problem.
- `round-01-codex.md`: Codex chose extraction-depth restriction before offset thinning and corrected Grok's initial both-factors success gate to the user's one-factor success condition.
- `round-02-codex.md`: Codex chose the ultra-minimal `trial_2_stop_1` policy as the lower-bound first probe and required zero-yield inspections to count as real cost.
- `round-03-codex.md`: Codex accepted Grok's methodological objection that a single `r = 2` comb is not a genuine web, and locked a minimum diversity gate of at least `3` distinct public `r` values before scoring.
- `round-04-grok.md`: Grok confirmed the contract was closed at v1.0 and ready for the next implementation decision.

The short Grok transcript files for rounds 01 through 03 were superseded by later resumed turns. The final Grok closure is recorded in `round-04-grok.md`.

## Convergences

- The experiment stays inside the literal multiplicative-web frame.
- The first axis is extraction depth on dense offsets, not offset thinning.
- The lower-bound policy is `trial_2_stop_1`: dense step `1`, trial division only by `2`, immediate stop.
- A single-thread parity comb is not a meaningful web.
- Runs require at least `3` distinct public thread values before one-factor or two-factor scoring.
- One hidden factor thread is enough for primary success.
- Both hidden factor threads remain a stronger secondary diagnostic.
- `p` and `q` are audit-only labels after computation.
- Zero-yield inspections count as cost.

## Falsification And Classification Rules

Primary scoring only applies after the diversity gate:

```text
distinct public r values >= 3
```

Eligible runs use:

```text
one_factor_success = at least one held-out p/q thread appears in the top 5 supported holes with support >= 1
```

The contract separately records:

- `two_factor_success`;
- `top18_direct_hits`;
- best hidden-thread rank;
- touched composites;
- trial attempts;
- zero-yield inspections;
- distinct public `r` count.

If fewer than `3` public `r` values appear, the run is classified:

```text
insufficient_thread_diversity
```

That classification is informative. It does not pass the one-factor gate and does not falsify the broader sparse-web hypothesis.

## Candidate Insight

The first meaningful sparse web is not the cheapest extractor by itself. It is the cheapest extractor that creates enough public thread diversity to form intersections and then ranks at least one held-out hidden thread inside the top-5 support window.

This preserves the user's core scaling pressure while avoiding a degenerate binary comb that would look cheap but would no longer test the multiplicative-web hypothesis.

## Unresolved Question

The contract is closed. Grok's remaining question is not methodological; it is implementation shape:

```text
A. Implement only trial_2_stop_1 and record insufficient_thread_diversity if that is the outcome.
B. Implement trial_2_stop_1 plus automatic escalation to trial_2_3_5_stop_1 on insufficient_thread_diversity.
```

No implementation choice was made in this meeting because the user asked for reiteration to Grok in a research meeting, not for the experiment to be written yet.

## Next Research Move

When the user approves implementation, the narrowest next move is:

```text
sparse_web_first_slice.py
```

It should run only the locked first slice on the 4 toy cases, emit the contract's required diagnostics, and avoid escalation unless the user explicitly chooses that implementation shape.
