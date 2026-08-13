# Status tiers

A 30-second map of this repository.

`PROOF.md` controls theorem status.
This page does not replace it. It says what a reader may treat as proved,
what is a finite measurement, and what is still a probe.

| Tier | In one sentence |
| --- | --- |
| **1 Proved** | Local integer theorems in `PROOF.md`, including universal bounded compression and Prime-Square Proximity. |
| **2 Measured** | Finite executed surfaces, including No-Later-Simpler-Composite zero violations through `10^18`. Not an infinite proof. |
| **3 Experimental** | RSA endpoint probes, Mersenne exponent-wall work, and the DNI-to-zeta / RH reading path. No RSA-scale resolver theorem. RH is not proved. |

Wording audit: [docs/reframe/AUDIT.md](reframe/AUDIT.md).

---

## A. Tier 1: Proved

Authority: [PROOF.md](../PROOF.md).

These are local integer theorems. They do not prove RH, PNT, or a bound on
raw consecutive-prime gap size `q - p`.

| Result | Statement | Pointer |
| --- | --- | --- |
| Next-prime rule | Given a prime `p`, the next prime is `q = min{ n > p : tau(n) = 2 }`. | `PROOF.md` Headline 1, The Algorithm, Why The Algorithm Returns The Next Prime |
| Gap Winner Rule (interior maximizer) | Inside a nonempty gap, the leftmost min-`tau` integer `w` is the unique maximizer of `F(n) = (1 - tau(n)/2) log n` (equivalently the leftmost min of `E(n)` / maximizer of raw `Z`). | `PROOF.md` Headline 2, Interior Maximizer Theorem, Ordered Comparison Lemma |
| Modular zero lemma on `M_v1` | On the fixed remainder vector modulo `(2, 3, 5, 7, 30, 210, 2310)`, four or more zeros occur if and only if `30` divides `w`. Modular fact only. Not a gap-size lock. | `PROOF.md` Modular zero lemma on remainder vector `M_v1` |
| Universal bounded compression | For every consecutive prime gap with nonempty interior, the GWR-selected witness satisfies `w - p <= max(64, ceil(0.5 * log(q)^2))`. This bounds the **selected-witness offset**, not `q - p`. | `PROOF.md` Headline 3, Document Status |
| Prime-Square Proximity Theorem (2026-07-05) | On the square branch `tau(w) = 3`, `r^2 - p <= max(64, ceil(0.5 * log(r^2)^2))`. Closes the square branch of UBC. | `PROOF.md` Prime-Square Proximity Theorem |

No-Later-Simpler-Composite, as "no later interior integer has strictly smaller
`tau` than `w`", is an immediate corollary of leftmost min-`tau` selection.
That corollary sits with GWR. The separate `10^18` zero-violation sweep is
Tier 2.

### Dependencies (state these; do not hide them)

Not "basic divisor arithmetic only."

- Exact `tau` arithmetic and the ordered gap interior.
- Named finite premises, packaged in Lean and pinned in `PROOF.md`:
  `gwr_finite_base_v1`, `bounded_compression_base_v1`, `residual_k128_v1`.
- Classical imports used in the prose spine: Bertrand (CL-001),
  divisor-pair bound (CL-002), `tau(r^2) = 3` (CL-003).
- Lean is a downstream audit mirror. It does not rerun the exhaustions.
  The only core-path axiom is `tau_prime_square_eq_three` (CL-003).
  See [lean-4/SORRY_AXIOM_INVENTORY.md](../lean-4/SORRY_AXIOM_INVENTORY.md).

Do not rewrite these theorems as "only verified up to `10^18`."
Finite premises complete the stated proofs. They are not the theorem bound.

---

## B. Tier 2: Measured to `10^18`

Computational enumeration and committed implementation surfaces.
Not an infinite proof, even when the count is zero violations.

| Surface | What was executed | Pointer |
| --- | --- | --- |
| No-Later-Simpler-Composite stress | Zero observed later-simpler-composite violations through `10^18` on the committed stress surface. Corroborates the GWR corollary. Does not replace `PROOF.md`. | `docs/RESULTS.md`, `assert_results.tsv`, `visualizations/gallery/` |
| Generator decade ladder | `2816 / 2816` exact `{"p", "q"}` records, `10^8` through `10^18`, 256 primes per decade. Implementation evidence for the generator, not a new theorem. | `docs/RESULTS.md`, `AGENTS.md` Mandatory `10^18` Evidence Surface |
| Exact recursive walk (named regimes) | `743,075 / 743,075` transition rows on the combined `10^6 + 10^7` surface; `664,578 / 664,578` recoveries from prime 11 through `10,000,121`; sampled decade ladder hit rate `1.0` on 860 steps. | `docs/RESULTS.md`, `docs/core/RECURSIVE_PRIME_WALK.md` |
| RSA endpoint-class ledger (committed rungs) | `rsa_v2_40bit_static_001` `factor_found=true` (endpoint class). `rsa_v2_50bit_static_001` `factor_found=false` under the v2 runner (expected unresolved baseline). `rsa_v2_64bit_static_001` `factor_found=true` (endpoint class). 128-bit and 256-bit curated probes return unresolved public class as the expected high-scale baseline. | `research/06-cryptology-rsa/README.md` |

Program-level "verified" / "validated" language still requires an executed
`10^18` surface under `AGENTS.md`. A `10^18` pass is not an RH proof and
not an RSA-scale theorem.

---

## C. Tier 3: Experimental hypothesis

Probes. Residual maps. Reading paths. Say unresolved when unresolved.

| Probe | What it is | What it is not |
| --- | --- | --- |
| RSA v2 / v3 endpoint chain | Locked-chain traversal, floor transport `floor(N / upper.reset_endpoint)`, reciprocal closure, residual taxonomy including `unresolved_by_joint_cell`. | Not a factorization claim unless a named audit row reports `factor_found=true`. No RSA-scale resolver theorem is claimed. |
| RSA 50-bit V3 pair `(32047633, 32059651)` | `carrier_reciprocal_closure` hypothesis on a public reciprocal floor pair (2026-08-07). | Not a factor solve. |
| Curated 40 / 50 / 64 / 128 / 256-bit examples | Probe widths for the live runners. | Not a demonstrated 512-bit or 1024-bit+ success. |
| Mersenne exponent wall `2^e` | Experimental generator that reads gap structure around the exponent wall. | Not a theorem that enumerates Mersenne primes. |
| DNI coordinates `E(n) = (d(n)/2 - 1) ln n`, `Z(n) = e^{-E(n)}` | Exact coordinate reformulation used by local theorems and by the RH reading path. | The coordinates do not prove RH. |
| `docs/rh/` reading path | Coefficient-side interpretation after classical identities `D(s) = zeta(s)^2` and `(e^2/2) K(s)/D(s) = -zeta'/zeta`. | Not an RH proof. Source-to-spectral placement remains unresolved. |

Explicit non-claims:

- No RSA-scale resolver theorem is claimed.
- No factorization claim unless the named audit reports `factor_found=true`.
- 256-bit and larger RSA moduli are probe / unresolved-class territory on
  the committed public surface, not a reported factor success.
- The Riemann Hypothesis is not proved.

Primary homes:

- `research/06-cryptology-rsa/`
- `docs/rh/`
- `docs/rh/dni-to-zeta-compression.md`
