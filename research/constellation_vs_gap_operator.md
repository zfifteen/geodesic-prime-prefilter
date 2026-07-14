# Constellation Admissibility vs PGS Next-Prime Operator

This note clarifies the strict categorical boundary between classical constellation theory (as discussed in modular covering arguments) and the Prime Gap Structure (PGS) consecutive-gap operator.

## 1. Core Distinctions

| Feature | Classical Constellation Theory | PGS Next-Prime Operator |
| :--- | :--- | :--- |
| **Object of Study** | A *pattern* of primes at fixed offsets (e.g., $p, p+2, p+6$). | An *ordered gap* from a known prime $p$ to the consecutive next prime $q$. |
| **Primary Question** | Can this simultaneous pattern occur infinitely often? | What is $q$, and what interior structure sits in the gap $(p,q)$? |
| **Inference Mode** | Modular covering / Sieve geometry (admissibility tests). | Divisor field, DNI, GWR, chamber reset, endpoint chain, and residual code. |
| **Nature of Bounds** | Zhang/Maynard bound of $246$ for *any* prime pairs. | Deterministic local GWR witness offset bound (Cramér-scale) inside a gap. |
| **Status of Claims** | Constellations are either proved dead (e.g., 3,5,7) or remain an open conjecture (twin primes). | Next-prime / universal bounded compression is a *theorem* under stated hypotheses. |

## 2. Explicit Rejections (What Not to Claim)

To prevent category errors, the following conceptual merges are strictly forbidden:
- **No sieve-first generator:** We do not use modular covering or admissibility tests to choose generator outputs.
- **No $k$-tuple search as a residual close:** PGS residual maps (like checking conditions where $g=2$) must not be redefined as an admissible $k$-tuple search. The uniqueness of (3,5,7) does not grant permission to claim triple twins are free.
- **Zhang bound $\neq$ PGS theorem:** Progress on classical bounded gaps (e.g., pairs within 246) does not validate PGS compression, and PGS bounded compression does not solve the twin prime conjecture.

## 3. Alignment to Live PGS Questions

Instead of a twin-prime campaign, PGS is strictly aligned to:
**Public residual $\rightarrow$ endpoint class (first-tail pressure).**

When studying gap behaviors, a PGS residual probe may *measure* how often certain gap events appear under GWR conditions. This is an exercise in residual honesty on named codes—mapping exact local structures—rather than trying to force an infinitude proof.
