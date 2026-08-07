# 128-bit Rung Phase 2 Continuity Note

**Date:** 2026-08-07  
**Status:** Active implementation track  
**Parent plan:** `research/06-cryptology-rsa/docs/128-bit-rung-arithmetic-plan.md`

---

## Purpose of this note

This file exists so a later session can resume the 128-bit arithmetic expansion without reverse-engineering the previous work. It records the locked sequence, the current gate, and the exact commands to run.

---

## Locked sequence (do not reorder)

1. Prove intermediate arithmetic near the 2^64 boundary with `mpz_t`.
2. Only after that suite is green, complete final certificate population.
3. Keep the dense phase-space traversal inside C memory.
4. Return only the final certificate (or an unresolved code) to Python.
5. Derive tail capacity from the measured V3 surface on the lower rungs.
6. Never introduce classical filters (`gcd`, `%`, primality, product) into the inference path.

Reason for the order: a silent wrap-around near 2^64 shifts the d(n) field, misidentifies the Gap Winner, corrupts reciprocal transport, and produces a false unresolved status. The arithmetic foundation must be proven first.

---

## Current gate (2026-08-07)

**First concrete deliverable of Phase 2 is complete in source form.**

- New test: `src/c/high-scale-pgs/tests/test_mpz_overflow_boundary.c`
- Makefile target: `make test-mpz-overflow`
- Interval under test: closed [2^63, 2^65]
- Coverage:
  - values just below, at, and above 2^63, 2^64, 2^65
  - addition, multiplication, floor division that cross the 64-bit boundary
  - integer square-root of a perfect square above 2^64
  - explicit proof that native unsigned 64-bit addition of (2^64-1)+1 would wrap while `mpz_t` does not
  - anchor-scale floor division and isqrt near 2^127 / 2^64

**Stop condition:** if `make test-mpz-overflow` fails, do not wire any V3 reciprocal-closure logic.

**Go condition:** when the suite exits 0, proceed to complete final certificate population while keeping dense traversal inside C.

---

## How to resume in a new session

From the repository root on an Apple Silicon machine with Homebrew GMP/MPFR:

```bash
cd src/c/high-scale-pgs
make clean
make test-mpz-overflow
```

Expected output ends with:

```text
PASS: 2^64 boundary arithmetic is solid under mpz_t.
Next: complete final certificate population while keeping dense traversal in C.
```

Exit code must be 0.

If the host is not Apple Silicon, the Makefile will refuse to build. That is intentional.

---

## Files touched so far

| Path | Role |
|------|------|
| `research/06-cryptology-rsa/docs/128-bit-rung-arithmetic-plan.md` | Master plan (adversarial constraints applied) |
| `research/06-cryptology-rsa/docs/128-bit-rung-phase2-continuity.md` | This continuity note |
| `src/c/high-scale-pgs/tests/test_mpz_overflow_boundary.c` | Overflow suite |
| `src/c/high-scale-pgs/Makefile` | New target `test-mpz-overflow` |

---

## Next concrete tasks (after the overflow suite is green)

1. Complete population of the final `pgs_certificate_t` fields that are still missing or incomplete for high-scale anchors (especially `tail_after_reset_count` / offsets and lower-threat fields).
2. Enforce that every intermediate calculation inside `pgs_chamber.c` that can exceed 2^64 uses `mpz_t`.
3. Keep the dense candidate/chamber loop entirely inside C; do not return intermediate states across the ctypes boundary.
4. Add instrumentation (call count, wall time, anchor bit length) on the final certificate path only.
5. Only then route the existing 128-bit ladder case through the hardened path and capture the public status.

---

## Explicit non-goals for the current gate

- Do not implement V3 reciprocal-closure predicates yet.
- Do not change the Python inference path yet.
- Do not alter the public-versus-audit separation.
- Do not introduce classical pre-filters.

---

## Continuity checklist for the next session

- [ ] Run `make test-mpz-overflow` and confirm exit code 0.
- [ ] Record the exact terminal output in a short note or commit message.
- [ ] Only after green: open `src/c/high-scale-pgs/src/pgs_chamber.c` and begin final certificate field completion under the C-side isolation contract.
- [ ] Update this continuity note with the new stop/go gate after that step.

---

End of continuity note.
