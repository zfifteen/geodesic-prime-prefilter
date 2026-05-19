# Paragraph 01 Research Note

## Plain Claim

The first panel should open with the concrete factoring problem. A public number
is known. Its two prime factors are hidden. The research question is whether
the ordered structure visible around the public number contains enough
deterministic information to point back to at least one hidden factor.

## What The Evidence Supports

The repository supports this as the branch object:

- the cryptology chapter is organized around semiprime structure, reciprocal
  closure, structural certificates, and unresolved survivor states;
- the experiments route map states the live target as public product to factor
  or unresolved state;
- the endpoint law states that RSA moduli expose deterministic endpoint
  structure;
- the live runner starts from public `N`, transports public interval state
  through `floor(N / x)`, and emits either endpoint structure or unresolved
  state before downstream audit.

## What The First Paragraph Must Avoid

- Do not say the branch proves factoring.
- Do not say the branch is a faster factoring method.
- Do not use internal abbreviations in the first paragraph.
- Do not begin with square-root search or classical factorization.
- Do not blur endpoint structure with factor recovery.

## Draft Public Paragraph

Factoring starts with one visible number and two hidden prime factors. This
research branch asks whether the visible order around that number contains
enough structure to point back to one of the hidden factors. The current work
does not treat the product as a blank object waiting for trial division. It
treats the product as sitting inside a public neighborhood whose ordered marks
can be transported from one side of the product to the other. The central
question is whether that public structure forces a factor endpoint, or whether
the honest result remains unresolved.

## Evidence Status

```text
theorem_status = no universal factor theorem claimed
implementation_status = live public endpoint-chain runner exists
measured_status = deterministic endpoint structure is present on committed surfaces
audit_status = downstream audit remains separate from public inference
unresolved_state = public structure does not yet imply a universal factor proof
invalidated_rule = classical factor checks are not the inference route
```

## Infographic Direction

Make the visual literal:

```text
hidden factor endpoint      public product N      hidden factor endpoint
        ? ---------------- visible ordered marks ---------------- ?
```

The visual should show that the known object is the public product and the
visible local structure around it. The hidden factors should be present but not
named as already recovered.

