# Paragraph 01 Evidence: The Public Factor Question

## Public Claim To Support

Factoring begins with one visible number and two hidden prime factors. The
research branch asks whether the visible ordered structure around that number
contains enough deterministic information to recover at least one hidden factor.

## Supporting Evidence

- `research/06-cryptology-rsa/README.md` defines the cryptology chapter object
  as RSA v2/v3, semiprimes, modulus-link structure, reciprocal closure,
  structural certificates, and unresolved survivor states.
- `research/06-cryptology-rsa/README.md` states the required frame as:
  locked endpoint chain, transport through the public modulus, reciprocal
  endpoint closure, residual state, and then either a structural certificate or
  an unresolved state.
- `research/06-cryptology-rsa/experiments/README.md` states the current live
  resolver target as:
  `public N -> reciprocal PGSPG certificate pair -> factor or unresolved`.
- Recent commits show this branch centered on the factor bridge, not general
  cryptography exposition:
  - `14c9d662` - Add Public Endpoint Determinacy Kernel
  - `370e11b2` - Refactor RSA v2 runner to unify square-root chamber and
    endpoint-chain traversal
  - `ea29166d` - Add PEDK round 21 square fiber root selector

## Status Boundary

- The object is factor recovery from public structure.
- The current universal proof is not complete.
- Classical factor checks remain downstream audit, not the inference route.

## Infographic Concept

A product `N` sits in the center. Two hidden endpoints flank it as locked
factor positions. A visible public ruler around `N` shows local interval marks,
with a question arrow from the public ruler to one hidden endpoint.

