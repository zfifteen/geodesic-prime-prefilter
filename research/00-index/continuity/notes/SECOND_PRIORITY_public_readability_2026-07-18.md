# SECOND PRIORITY — Public-facing readability (principal 2026-07-18)

**Status:** Active **second** priority (below Lean core-stack top priority)  
**Set:** 2026-07-18 · #Prime-Gap-Structure  
**Program pin:** [ACTIVE_TARGET.md](../ACTIVE_TARGET.md)

## Directive (restated)

Public-facing documentation must be easy to open and easy to start reading.

1. **Begin** in conversational, plain prose suitable for a typical tenth-grade
   reader: concrete objects first, ordinary-language mechanism, then project
   names.
2. **Then** give the full technical treatment at research depth (definitions,
   invariants, theorem / measured / audit / hypothesis / unresolved separation,
   limits).
3. **Never** label those layers in the document itself (no “grade 10,” “for
   beginners,” “PhD section,” “advanced,” reading-level badges, etc.).
4. **`PROOF.md` is exempt** — keep its current mathematical tone; do not force
   the dual-layer rewrite onto the live proof reference.

## In scope

- Root and chapter READMEs meant for humans
- `docs/` guides and public HTML (including gallery / essay surfaces when public)
- Continuity HTML briefs that outsiders or new agents might open as orientation
- New public docs by default

## Out of scope / do not thrash

- `PROOF.md` tone rewrite
- Secret ops, launchd, internal wake logs
- Changing theorem status or softening proved claims in the plain open
- Replacing precision with metaphor that hides status separation

## Relationship to top priority

Lean formalization remains **#1**. Readability work is **#2**: do it on public
docs as they are touched, and as dedicated polish passes when Lean is not the
active slice — not as an excuse to freeze Lean.

## Implementation habit

When editing or creating a public doc:

```text
plain open (what you can picture) →
mechanism in ordinary words →
project terms →
formal statements + status labels →
exact limits
```

No meta-labels for “which audience.”

*Principal directive 2026-07-18. Hermes pin.*
