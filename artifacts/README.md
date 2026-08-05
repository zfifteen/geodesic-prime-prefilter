# Artifacts pointer

Large experiment outputs, evidence dumps, scan checkpoints, and media **do not live in this git repo**.

## Sibling store

Path (sibling checkout):

```text
../prime-gap-structure-artifacts
```

Absolute default on this machine:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure-artifacts
```

See that store's `MANIFEST.md` for sha256 inventory of moved bulk.

## What stays here

- Source, tests, Lean sources (not `.lake`)
- `PROOF.md`, continuity prose, small summary JSON/MD
- Regen scripts and expected hashes

## Policy

Commit summaries and hashes. Write full row dumps only under untracked `output/` or into the sibling store.
