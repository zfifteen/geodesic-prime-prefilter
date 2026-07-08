#!/usr/bin/env python3
"""Export WHITEPAPER.md to a readable PDF (reportlab)."""

from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "WHITEPAPER.md"
OUTPUT = ROOT / "WHITEPAPER.pdf"


def md_to_flowables(text: str, styles) -> list:
    flow = []
    body = styles["BodyText"]
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, spaceAfter=10)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, spaceAfter=8)
    mono = ParagraphStyle("Mono", parent=body, fontName="Courier", fontSize=8, leading=10)

    for raw in text.splitlines():
        line = raw.rstrip()
        if not line:
            flow.append(Spacer(1, 0.12 * inch))
            continue
        if line.startswith("# "):
            flow.append(Paragraph(_esc(line[2:]), h1))
        elif line.startswith("## "):
            flow.append(Paragraph(_esc(line[3:]), h2))
        elif line.startswith("```"):
            continue
        elif line.startswith("|") or line.startswith("- "):
            flow.append(Paragraph(_esc(line), body))
        else:
            style = mono if line.startswith("    ") or "  " in line[:4] else body
            flow.append(Paragraph(_esc(line), style))
    return flow


def _esc(s: str) -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def main() -> int:
    text = SOURCE.read_text(encoding="utf-8")
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    doc.build(md_to_flowables(text, styles))
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())