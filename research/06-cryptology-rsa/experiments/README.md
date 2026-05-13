# RSA Experiments Route Map

This directory is a set of topic-owned working cells. The old active
`experiments/rsa/v2` monolith is removed; historical notes may still mention
that path.

## Live

- `live-solver/rsa-v2/`: current public resolver, live contracts, default
  inference output, and resolver audit output.
- `live-solver/rsa-v3/`: next live resolver entrypoint when v3 work becomes
  active.
- `data-ladder/rsa-v2/`: fixture builders, ladder specs, public cases, audit
  fixtures, and generated provenance.

## Sidecar Evidence

- `transported-sidecars/rsa-v2/`: transported story law, d4 budget, d4 trace,
  exclusion debt, threat-tail, and width diagnostics.
- `certificate-mechanics/rsa-v2/`: commitment-story certificate probes and
  transported commitment ledger outputs.
- `grammar-evidence/rsa-v2/`: grammar catalogs, scans, inverse-word evidence,
  and grammar outputs.
- `modulus-recursive-catalogs/rsa-v2/`: modulus-gap probes, public RSA modulus
  docs, solved-challenge evidence, and exact catalog output.
- `frontier-holdouts/rsa-v2/`: normalized frontier and toy holdout closure
  probes.
- `order-entropy-sidecars/rsa-v2/`: Shor/order entropy comparison sidecar.
- `recursive-sidecars/rsa-v2/`: OECC recursive side-by-side scalability work.

## Proof, Review, And Archive

- `proof-workbenches/rsa-v2/`: proof-obligation and invariant workbench docs.
- `reviews-automation/rsa-v2/`: automation notes and Grok session records.
- `invalidated-solvers/rsa-v2/`: falsified solver-shape artifacts separated
  from live inference.
- `archive/rsa-v2/`: scratch and tmp material only.

## Current Terminology

`resolved` means at least one factor was found by the public inference
mechanism and then checked downstream by audit. Rows without such a public
factor are unresolved.

The current live RSA v2 resolver remains:

```text
public N -> reciprocal PGSPG certificate pair -> factor or unresolved
```

Sidecars describe pressure, blockers, and diagnostics. They do not participate
in live inference unless promoted by a public PGS theorem.
