#!/usr/bin/env python3
"""Export WHITEPAPER.pdf with embedded infographic and demo measurements."""

from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "WHITEPAPER.md"
INFOGRAPHIC = ROOT / "infographic.png"
DEMO_JSON = ROOT / "output" / "demo_results.json"
OUTPUT = ROOT / "WHITEPAPER.pdf"


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _load_sections() -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title = "Prime Order Is Fixed Before Zeta"
    current_lines: list[str] = []
    for raw in SOURCE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            if current_lines:
                sections.append((current_title, current_lines))
            current_title = line[3:].strip()
            current_lines = []
            continue
        if line.startswith("# "):
            continue
        if line.startswith("```"):
            continue
        if not line or line.startswith("| ---"):
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            current_lines.append(" : ".join(cells))
        else:
            current_lines.append(line)
    if current_lines:
        sections.append((current_title, current_lines))
    return sections


def _demo_table() -> Table | None:
    if not DEMO_JSON.is_file():
        return None
    data = json.loads(DEMO_JSON.read_text(encoding="utf-8"))
    rows = [["Gap", "GWR w", "min τ", "ρ_ch(2.5)", "|R err|"]]
    bridge_err = data["bridge"]["ratio_abs_error"]
    for gap in data["gap_examples"]:
        inc = gap.get("chamber_increments", {})
        rows.append(
            [
                f"{gap['p']} to {gap['q']}",
                str(gap["gwr_witness"]),
                str(gap["interior_min_divisor_count"]),
                f"{inc.get('rho_chamber', 0):.4f}",
                f"{bridge_err:.2e}",
            ]
        )
    table = Table(rows, colWidths=[1.1 * inch, 0.8 * inch, 0.7 * inch, 1.0 * inch, 1.0 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def main() -> int:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("Title", parent=styles["Title"], fontSize=20, spaceAfter=12)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceBefore=10, spaceAfter=6)
    body = styles["BodyText"]

    story: list = [Paragraph("Prime Order Is Fixed Before Zeta", title_style)]
    story.append(
        Paragraph(
            _esc("Prime Gap Structure, explanatory whitepaper. Integer source → exact compression → RH language."),
            body,
        )
    )
    story.append(Spacer(1, 0.15 * inch))

    if INFOGRAPHIC.is_file():
        img = Image(str(INFOGRAPHIC), width=6.5 * inch, height=8.45 * inch)
        story.append(img)
        story.append(Spacer(1, 0.2 * inch))

    demo_table = _demo_table()
    if demo_table:
        story.append(Paragraph("Measured chamber compression (demo output)", h2))
        story.append(demo_table)
        story.append(Spacer(1, 0.2 * inch))

    for section_title, lines in _load_sections():
        story.append(Paragraph(_esc(section_title), h2))
        for line in lines:
            story.append(Paragraph(_esc(line), body))
        story.append(Spacer(1, 0.08 * inch))

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )
    doc.build(story)
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())