# RSA v2 Temporary Algorithm Sandbox

This directory is for disposable proof code.

Code here may be used to flesh out algorithms before they are integrated into
the real experiment pipeline. Nothing in this directory is a production result
until it is reviewed, rewritten against the experiment boundary, and promoted
out of `tmp`.

Rules still apply:

- use public `N` as the inference input;
- derive PGS state from code, not answer-bearing fixtures;
- use GMP-compatible arithmetic for factorizer coordinates;
- keep product closure after PGS survivor contraction;
- return unresolved rather than adding fallback paths.

