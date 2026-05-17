We found a clean prime-gap filter for factor locations: when a composite lands at the selected point inside its visible prime gap and the hidden factor endpoints have balanced right gaps, 45,337 impossible factor-neighborhood placements were excluded with zero exact falsifications. Save this if you are tracking the factor-location branch.

![Prime gap factor filter overview](01-factor-filter-overview.png)

---

Start with the visible side. A composite number sits inside a gap between two consecutive primes. That public gap contains a selected point computed from the gap's own divisor structure. In the clean case, the composite lands exactly at that selected point. That public hit is the part to watch.

![Selected public gap](02-selected-public-gap.png)

---

Now look at the factor side. Each hidden prime factor has neighboring gaps around it. The clean condition is read from the right-opening gaps after the two factor endpoints. In residue language, both endpoint slots avoid 1 and 23, and at least one endpoint slot hits 7, 13, or 19. This is the piece worth stress-testing.

![Balanced factor endpoints](03-balanced-factor-endpoints.png)

---

The contrast test is what makes this sharp. Balanced factor endpoints alone leak when the composite is not at the selected public point. At the selected point, balanced endpoints give 45,337 exclusions and zero falsifications. Move away from that public point and the same endpoint idea starts leaking. This matrix is the shareable evidence.

![Selected point contrast](04-selected-point-contrast.png)

---

This is a measured law candidate for the factor-location theorem. Broad representation search is done for this layer. The proof target is now narrow: explain why the selected public gap position stabilizes the balanced endpoint exclusion surface. Follow the next step: turn the measured kernel into the theorem.

![Theorem target](05-theorem-target.png)
