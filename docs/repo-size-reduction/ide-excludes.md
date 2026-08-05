# IDE excludes (Phase 1)

Committed excludes so tools skip local noise that is not part of the slim clone surface.

## VS Code / Cursor

- `.vscode/settings.json` — `files.watcherExclude`, `search.exclude`, `files.exclude`
- `.cursorignore` — Cursor indexing

Patterns: `lean-4/.lake/**`, `**/vendor/**`, `**/.gradle/**`, `media/**`, `**/output/**`, `**/scan_checkpoints_*/**`, venv/pycache.

## IntelliJ IDEA (local; `.idea/` is gitignored)

Add exclude folders under Project Structure or edit the module content roots to exclude:

- `lean-4/.lake`
- any `vendor` trees under `research/06-cryptology-rsa`
- `media`
- `**/output`
- `**/scan_checkpoints_*`

## Optional local deletes

These are regenerable and are already gitignored. Delete only when disk pressure requires it:

```bash
rm -rf lean-4/.lake
# BC vendor trees under research/06-cryptology-rsa/.../vendor/ (re-fetch if needed)
```

Local multi-GB noise does not fail the clone-size gate.
