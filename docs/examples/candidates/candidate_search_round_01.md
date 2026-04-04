**Candidate Search Round 01: High-Impact Cryptographic and Numerical Libraries**  
**Date:** Saturday, April 04, 2026  
**Agent/Model:** Grok (with web_search and targeted repository analysis)  
**Search Scope:** Widely used open-source projects involving prime generation, primality testing, or sieving in performance-critical paths (RSA/DSA key generation, arbitrary-precision math, cryptographic toolkits). Prioritized libraries with documented Miller-Rabin/trial-division hotspots, active maintenance, and measurable real-world workloads. Excluded toy implementations, non-active projects, or those where primes are incidental (e.g., pure I/O or networking tools). Focused on concrete insertion points for a reject-only DCI/GWR-style prefilter.  
**Constraints/Assumptions:** Scored conservatively per rubric (0-2 per axis). Preferred projects with existing trial-division pre-screens, deterministic candidate paths, and local A/B benchmarks. Python-first for easiest smoke-testing; C/C++/Java for broader impact. All candidates allow reject-only prefilter without correctness regression.

### Ranked Candidates

**Rank 1: OpenSSL**  
- **Repository URL:** https://github.com/openssl/openssl  
- **License:** Apache-2.0  
- **Primary language:** C  
- **Why it is a fit:** Core to global TLS/SSL infrastructure and RSA key generation. Prime generation is on the hot path for every RSA keypair creation; the library already performs trial division before expensive Miller-Rabin rounds, making a structural prefilter a natural, low-risk enhancement.  
- **Exact prime-related hotspot:** `crypto/bn/bn_prime.c` – `BN_generate_prime_ex2` / `BN_generate_prime_ex` (and internal `find_prime` / trial-division loop). Candidates are generated randomly, sieved with small primes, then tested with Miller-Rabin (5+ rounds for cryptographic sizes).  
- **Likely insertion point for a DCI/GWR prefilter:** Inside the candidate loop in `bn_prime.c` (after basic bit-setting and initial trial division but before full Miller-Rabin). Add as a fast reject-only call on the `BIGNUM` candidate.  
- **Best A/B benchmark metric:** RSA key-generation latency (e.g., `openssl speed rsa` or custom `BN_generate_prime_ex` micro-benchmark) or Miller-Rabin invocation count per key.  
- **Ease of smoke-testing inside this repo:** Medium (extractable C harness using the existing `apps/prime.c` or a minimal test calling `BN_generate_prime_ex`; no full vendoring needed for POC).  
- **Expected integration difficulty:** Low-medium (single-file patch in bn_prime.c; existing callback and context APIs make it clean).  
- **Why a successful result would matter in practice:** OpenSSL powers ~90%+ of web TLS and countless embedded/crypto devices. A measurable speedup in key generation (especially 2048/4096-bit) would be immediately noticeable in certificate issuance, VPN setup, and high-volume key-rotation workloads; easy to explain as “faster secure key generation via better composite filtering.”  
- **Six-axis score:** Prime-hotspot relevance: 2 | Clear insertion point: 2 | Benchmarkability: 2 | Correctness safety: 2 | Adoption impact: 2 | Smoke-test feasibility: 1 → **Total: 11/12**

**Rank 2: GNU Multiple Precision Arithmetic Library (GMP)**  
- **Repository URL:** https://gmplib.org/ (official; Git mirrors e.g. https://github.com/alisw/GMP)  
- **License:** LGPL-3.0-or-later (with GMP exceptions)  
- **Primary language:** C (with assembly optimizations)  
- **Why it is a fit:** Foundational bigint library used by OpenSSL, GnuPG, Python (gmpy2), SymPy, etc. Its primality routines are called billions of times across ecosystems; already does small-factor trial division before Miller-Rabin.  
- **Exact prime-related hotspot:** `mpz/probab_prime_p.c` + `mpz/millerrabin.c` – `mpz_probab_prime_p` (trial division by small primes → Miller-Rabin).  
- **Likely insertion point for a DCI/GWR prefilter:** Early in `mpz_probab_prime_p` (after initial small-prime trial division but before Miller-Rabin base selection and modular exponentiations).  
- **Best A/B benchmark metric:** `mpz_probab_prime_p` calls per second or full primality test latency on 1024/2048-bit candidates.  
- **Ease of smoke-testing inside this repo:** Medium-high (GMP’s test suite and `mpz` examples allow isolated harness; Python bindings via gmpy2 enable quick POC).  
- **Expected integration difficulty:** Low (core mpz function; well-documented internal APIs).  
- **Why a successful result would matter in practice:** GMP underpins virtually all high-precision crypto and scientific computing. A faster prefilter would cascade to faster RSA keygen everywhere, plus symbolic math workloads; highly legible win (“the world’s fastest bigint library just got faster at finding primes”).  
- **Six-axis score:** Prime-hotspot relevance: 2 | Clear insertion point: 2 | Benchmarkability: 2 | Correctness safety: 2 | Adoption impact: 2 | Smoke-test feasibility: 2 → **Total: 12/12** (but conservatively docked for slightly broader scope)

**Rank 3: Libgcrypt (GNU Crypto Library)**  
- **Repository URL:** https://github.com/gpg/libgcrypt  
- **License:** LGPL-2.1-or-later  
- **Primary language:** C  
- **Why it is a fit:** Used by GnuPG, SSH, and many crypto tools. Prime generation is central to RSA/DSA/EC key creation and follows X9.31-style algorithms with explicit trial division + probabilistic testing.  
- **Exact prime-related hotspot:** `cipher/primegen.c` – `gcry_prime_generate` and internal candidate screening / Miller-Rabin path.  
- **Likely insertion point for a DCI/GWR prefilter:** In the prime candidate loop inside `primegen.c` (post-random generation, pre-full probabilistic tests).  
- **Best A/B benchmark metric:** `gcry_prime_generate` latency or key-generation throughput in RSA/DSA operations.  
- **Ease of smoke-testing inside this repo:** Medium (existing test suite + `tests/` harness; small C wrapper suffices).  
- **Expected integration difficulty:** Low (modular primegen subsystem).  
- **Why a successful result would matter in practice:** Powers GnuPG (email encryption, signing) and many secure tools. Faster prime gen directly improves key creation UX and high-security workloads; clear narrative for maintainers.  
- **Six-axis score:** Prime-hotspot relevance: 2 | Clear insertion point: 2 | Benchmarkability: 2 | Correctness safety: 2 | Adoption impact: 1 | Smoke-test feasibility: 1 → **Total: 10/12**

**Rank 4: Bouncy Castle (Java)**  
- **Repository URL:** https://github.com/bcgit/bc-java  
- **License:** MIT  
- **Primary language:** Java  
- **Why it is a fit:** Dominant Java cryptography provider (used in Android, enterprise servers, OpenPGP). RSA keypair generation explicitly generates primes via probable-prime checks with trial division.  
- **Exact prime-related hotspot:** `core/src/main/java/org/bouncycastle/crypto/generators/RSAKeyPairGenerator.java` and underlying `BigInteger` probable-prime path (or lightweight API equivalents).  
- **Likely insertion point for a DCI/GWR prefilter:** Inside the prime-candidate generation loop in `RSAKeyPairGenerator` (before full Miller-Rabin-style tests).  
- **Best A/B benchmark metric:** RSA keypair generation time or candidate rejection rate.  
- **Ease of smoke-testing inside this repo:** High (pure Java; JUnit tests and lightweight API allow isolated benchmark in a few lines).  
- **Expected integration difficulty:** Low (Java is patch-friendly; clear modular structure).  
- **Why a successful result would matter in practice:** Java ecosystem handles massive enterprise/crypto volume. Win would be immediately usable in servers, mobile, and libraries; easy demo via public benchmarks.  
- **Six-axis score:** Prime-hotspot relevance: 2 | Clear insertion point: 2 | Benchmarkability: 2 | Correctness safety: 2 | Adoption impact: 1 | Smoke-test feasibility: 2 → **Total: 11/12**

**Rank 5: SymPy (Python Symbolic Mathematics Library)**  
- **Repository URL:** https://github.com/sympy/sympy  
- **License:** BSD-3-Clause  
- **Primary language:** Python  
- **Why it is a fit:** Widely used in scientific computing, education, and prototyping. `isprime`, `nextprime`, and prime-range functions are user-facing and already combine trial division with probabilistic tests; perfect for rapid Python POC before C ports.  
- **Exact prime-related hotspot:** `sympy/ntheory/primetest.py` (`isprime`) and `sympy/ntheory/generate.py` (`nextprime`, `primerange`).  
- **Likely insertion point for a DCI/GWR prefilter:** Early in `isprime` / candidate loop (after small-factor checks, before Miller-Rabin or BPSW).  
- **Best A/B benchmark metric:** `nextprime` or `isprime` throughput on large-integer batches.  
- **Ease of smoke-testing inside this repo:** Very high (pure Python; minimal harness or Jupyter notebook suffices; no compilation).  
- **Expected integration difficulty:** Very low (Python; easy to prototype and benchmark).  
- **Why a successful result would matter in practice:** Accelerates number-theory research, crypto prototyping, and data-science pipelines. Demonstrates the technique in an accessible language; high visibility in scientific communities.  
- **Six-axis score:** Prime-hotspot relevance: 1 | Clear insertion point: 2 | Benchmarkability: 2 | Correctness safety: 2 | Adoption impact: 1 | Smoke-test feasibility: 2 → **Total: 10/12**

### Shortlist
- **Top 3 candidates to evaluate first:** (1) OpenSSL, (2) GMP, (3) SymPy.  
- **Why these 3 are the best immediate next step:** OpenSSL + GMP deliver maximum real-world impact (crypto everywhere + foundational math); SymPy offers the fastest path to a working smoke-test proof-of-concept in Python that can be ported later. All have narrow, auditable insertion points and existing trial-division stages that align perfectly with DCI/GWR as a reject-only prefilter.  
- **Single best first smoke-test target:** SymPy. Its pure-Python implementation, simple integer I/O, and built-in benchmarks make it trivial to add a prefilter, measure Miller-Rabin call reduction, and validate correctness in <100 lines—ideal for an early, reproducible win inside this repo before tackling C libraries.  

This document preserves full details for future agents. Next steps could include extracting minimal harnesses for the shortlist and running initial A/B tests.
