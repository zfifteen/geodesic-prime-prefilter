# Integer Order Before Zeta: Whitepaper Package

Plain-language whitepaper explaining why prime order is fixed at the integer
layer before the zeta function enters.

**Hub home:** indexed as [RH-041](../../research/19-rh-corpus/FINDINGS_INDEX.md) in
[research/19-rh-corpus/](../../research/19-rh-corpus/README.md).

## Contents

| File | Description |
| --- | --- |
| `WHITEPAPER.md` | Main document (minimal jargon) |
| `WHITEPAPER.pdf` | PDF export (`export_whitepaper_pdf.py`) |
| `integer_order_demo.py` | Runnable demonstration script |
| `infographic.svg` / `infographic.png` | One-page visual summary |
| `output/demo_results.json` | Machine-readable output from the script |

## Run

From the repository root:

```bash
python3 experiments/integer-order-before-zeta-whitepaper-2026-07/integer_order_demo.py
```

Requires Python 3.11+ and `mpmath`.

PDF (optional; depends on local tooling available to the exporter):

```bash
python3 experiments/integer-order-before-zeta-whitepaper-2026-07/export_whitepaper_pdf.py
```
