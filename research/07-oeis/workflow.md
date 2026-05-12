# OEIS Candidate Workflow

## Candidate Packet Contract

Each candidate sequence gets one folder under `candidates/` with:

- `README.md`: object, formula or rule, theorem status, measured status, and
  plain-language description.
- `generate.py`: deterministic generator with no random path and no fallback.
- `terms.txt`: initial terms, one line, comma-separated.
- `duplicate-search.md`: OEIS search strings, date searched, and observed
  nearest matches.
- `submission-draft.md`: neutral OEIS-style draft with references and links.

## Acceptance Gate

A candidate is ready for external submission only when:

- the generator reproduces `terms.txt`;
- theorem status is separate from measured terms;
- duplicate search has been recorded;
- the draft avoids project-internal jargon unless it is defined plainly;
- the candidate has a real mathematical object, not just presentation style.

## Current State

No candidate has been selected in this branch. The workflow is ready for the
first candidate packet after the research corpus map settles.
