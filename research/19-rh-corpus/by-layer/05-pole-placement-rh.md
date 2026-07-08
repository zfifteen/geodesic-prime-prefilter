# Layer 5 — Pole placement / RH sentence

**Status mix:** `unresolved`, `narrative`  
**Proves RH?** This layer **is** the RH target — still **open**

After exact compression (L3), the Riemann Hypothesis becomes a **pole-placement
sentence** for the continued DNI ratio. Nothing in L1–L4 currently closes this.

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

If a future **source-to-spectral placement theorem** ([RH-035](../FINDINGS_INDEX.md)) closes, then:

1. Local GWR chamber invariants constrain summatory error terms.
2. Pole locus of $R(s)$ inherits those constraints after continuation.
3. RH sentence ([RH-051](../FINDINGS_INDEX.md)) would follow **only along that proof route**.

No such theorem is proved today.

---

## Explanatory geometry (not proof)

[docs/rh/critical-line-and-zero-geometry.md](../../../docs/rh/critical-line-and-zero-geometry.md) —
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