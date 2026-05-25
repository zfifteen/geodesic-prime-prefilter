# Chamber-Deconvolved Balance Reduction Assembly

Date: 2026-05-24

Status: assembly note reducing the Chamber-Deconvolved Reciprocal Balance
Lemma to the Folded Packet Drift Inequality plus the final interface inputs.

The current bridge chain is:

```text
Direct Full-Radius BDH closure
+ Packetwise Completion Localization
+ Transport Capacity Balance and Exact Assembly
-> Folded Packet Drift Inequality
-> Chamber-Deconvolved Reciprocal Balance
```

This note records the exact implication and the remaining inputs.

## Packet Arithmetic

For each chamber packet

$$
P(p,q)=\{q\}\cup\{n:p<n<q,\ n=r^a,\ a\ge2\},
$$

write

$$
x_n=\log {n\over\sqrt{pq}},
\qquad
M_{p,q}=\max_{n\in P(p,q)}|x_n|.
$$

After Dirichlet deconvolution,

$$
\lambda(n)=\Lambda(n),
$$

so the packet weights are nonnegative on endpoint primes and interior prime
powers. The packet arithmetic gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z).
$$

## Analytic Control From Direct BDH

The closed Direct Full-Radius BDH Assembly supplies:

1. kernel-weighted major validity at `R_all`;
2. full unified major aperture control;
3. kernel-band completion-energy control;
4. controlled summation for the completion assembly.

This is supplied either by the explicit polylogarithmic literal assignment

$$
Q_0=(\log X)^{1/4},
\qquad
N=X^{1/4}(\log X)^{1+C_N},
$$

or, outside that kernel-length regime, by the Unified Packet-Frame Source
theorem.

## Completion Localization

Packetwise Completion Localization gives

$$
\operatorname{supp}(\eta^-_{p,q,z})
\subseteq
\{x:|x|\ge M_{p,q}\}.
$$

Therefore

$$
\rho_{p,q}(z)
\ge
M_{p,q}.
$$

This follows from:

```text
M_{p,q}<1/2
+ pole/trivial-zero radii >=1/2
+ zero-radius constants excluded from negative folded cost
```

## Capacity Balance And Exact Assembly

Transport Capacity Balance supplies exact packet drift cancellation:

$$
\int J_z(x)\,d\eta_{p,q,z}(x)
=
-D_{p,q}(z).
$$

The constructive route uses:

1. the finite-part packet identity;
2. the nonnegative common side deficit `Delta(z)>=0`;
3. the deterministic symmetric trivial-zero split
   $$
   \delta_{-1/2}
   =
   (1+\alpha_0(z))\delta_{-1/2}
   -
   \alpha_0(z)\delta_{-1/2},
   \qquad
   \alpha_0(z)={\Delta(z)\over |J_z(-1/2)|};
   $$
4. proportional packet allocation of opposite-sign capacity.

The split preserves exact assembly atom by atom and remains localized at
radius `1/2`.

## Folded Packet Drift Inequality

Combining packet arithmetic and localization:

$$
|D_{p,q}(z)|
\le
M_{p,q}R_{p,q}(z)
\le
\rho_{p,q}(z)R_{p,q}(z).
$$

This is the Aggregate Completion-Cost Bound. With capacity balance and exact
assembly, it gives the Folded Packet Drift Inequality for every chamber
packet.

## Chamber-Deconvolved Reciprocal Balance

Summing the packetwise folded inequalities under the controlled-summation
input gives a nonnegative reciprocal-balanced folded kernel in

$$
z=u^2.
$$

Equivalently, the completed deconvolved chamber-load source has a Stieltjes
representation

$$
S(z)=\int_0^\infty {d\mu(t)\over z+t}
$$

on the common domain, provided the final interface inputs below hold.

## Final Interface Inputs

The remaining inputs are exact:

1. **Direct-route analytic input.**
   Either the explicit polylog literal regime is admissible, including the
   kernel length
   $$
   N=X^{1/4}Q_0^4(\log X)^C,
   $$
   or the Unified Packet-Frame Source theorem supplies the three residual
   bounds.

2. **Finite-part packet identity.**
   $$
   \operatorname{F.p.}\sum_{(p,q)}D_{p,q}(z)
   =
   -B_{\mathrm{comp}}^{\mathrm{fp}}(z).
   $$

3. **Nonnegative common side deficit.**
   $$
   \Delta(z)=D_-(z)-T_+^0(z)=D_+(z)-T_-^0(z)\ge0.
   $$

4. **Exact assembly compatibility.**
   The packet allocation must sum to the standard completion correction on
   the common analytic domain.

## Result

The Chamber-Deconvolved Reciprocal Balance Lemma is now reduced to the
Folded Packet Drift Inequality plus four explicit interface inputs. Direct
BDH, localization, and the symmetric split remove the previous analytic
residual and support obstacles. The remaining bridge is finite-part packet
balance, nonnegative common side deficit, and exact assembly compatibility
under either the literal kernel-length regime or the packet-frame fallback.
