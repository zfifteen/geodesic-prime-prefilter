# Layer 5: Pole placement / RH sentence (downstream catalog only)

**Status mix:** `unresolved`, `narrative`  
**Proves RH?** No; the RH sentence is **open**  
**May drive new work?** **No.** This layer catalogs a downstream reading. It
must not set experiment design. Hard rule: [FRAME_CONTRACT.md](../FRAME_CONTRACT.md).

After exact compression (L3), the Riemann Hypothesis *would be* a
**pole-placement sentence** for the continued DNI ratio *if* a source law forced
that placement. Nothing in L1 to L4 currently forces it. Do not reverse the
arrow and design from this sentence backward into PGS.

---

## RH sentence (program form)

All nontrivial poles of

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)}
$$

lie on

$$
\operatorname{Re}(s)=\frac{1}{2}.
$$

Equivalent to: all nontrivial zeros of $\zeta(s)$ lie on the critical line.

**ID:** [RH-051](../FINDINGS_INDEX.md) · **Status:** `unresolved`

---

## What proved layers **do** supply

| Upstream | Contribution to L5 | Does not prove RH |
|----------|-------------------|-------------------|
| L1 GWR + $C(q)$ | Local witness geometry is bounded and deterministic | Offset bound ≠ zero placement |
| L2 $E(n)=0$ | Prime returns on integer scale | ≠ $\operatorname{Re}(s)=\tfrac12$ |
| L3 exact identities | $R(s)$ is the packaged divisor field | Compression ≠ placement |
| L4 d=4 corollaries | Chamber fractional position bounds | Uniform $\le\tfrac12$ falsified ([RH-033](../FINDINGS_INDEX.md)) |
| F18-001 $\tfrac12$ | Arithmetic origin of bound coefficient | Hypothesis F18-003 only rhymes with line |

---

## Obstruction surface

[docs/rh/off-critical-pole-exclusion.md](../../../docs/rh/off-critical-pole-exclusion.md) records why earlier
placement routes failed and what a valid source-to-spectral theorem must exclude:

- Failed identity carriers
- Independent gap-length freedom
- Chamber log-weight remainders
- Extra divisor-count fields without spectral closure

**ID:** [RH-050](../FINDINGS_INDEX.md)

---

## Conditional map (honest framing)

Only if a future **source-first** summatory law exists, and only if a transfer
from that law to continued $R$ is proved, would the RH sentence follow. The
draft [RH-035](../FINDINGS_INDEX.md) kernel is **dormant** (not a live path) until
redesigned from bulk source operators without RH as the design driver.

No such theorem is proved today. Closing RH is not the acceptance test for
L1 to L4 work.

### What deterministic gap structure does **not** imply (today)

| Source fact | Does not force |
|-------------|----------------|
| $w-p\le C(q)$ | Zeros on $\operatorname{Re}(s)=\tfrac12$ |
| $D(s)=\zeta(s)^2$ exact | Placement of nontrivial poles of $R$ |
| F18-001 factor $\tfrac12$ | Critical-line theorem ([RH-040](../FINDINGS_INDEX.md) quarantined hypothesis) |
| d=4 $\mathrm{frac\_pos}$ bounds | Uniform half-line placement (falsified: [RH-033](../FINDINGS_INDEX.md)) |
| Multi-s partial sums ([RH-105](../FINDINGS_INDEX.md)) | Analytic continuation or RH |

State these boundaries in any public claim that mentions RH.

---

## Explanatory geometry (not proof)

[docs/rh/critical-line-and-zero-geometry.md](../../../docs/rh/critical-line-and-zero-geometry.md) :
strip symmetry, functional equation center at $\tfrac12$, zero heights as
spectral coordinates. Status: `narrative` ([RH-052](../FINDINGS_INDEX.md)).

---

## Indexed findings

| ID | Status | Title | Path |
|----|--------|-------|------|
| [RH-050](../FINDINGS_INDEX.md) | unresolved | Off-critical pole exclusion | [off-critical-pole-exclusion.md](../../../docs/rh/off-critical-pole-exclusion.md) |
| [RH-051](../FINDINGS_INDEX.md) | unresolved | RH pole-placement sentence | [status-ledger.md](../../../docs/rh/status-ledger.md) |
| [RH-052](../FINDINGS_INDEX.md) | narrative | Critical line geometry | [critical-line-and-zero-geometry.md](../../../docs/rh/critical-line-and-zero-geometry.md) |

**Public closing line:** PGS proves integer gap structure and exact zeta compression.
Placing every nontrivial pole on the critical line remains open.

[Stack overview](../SOURCE_STACK.md) · [Full index](../FINDINGS_INDEX.md) · [L6 bridge](./06-explicit-formula-bridge.md)