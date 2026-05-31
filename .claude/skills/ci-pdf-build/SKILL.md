---
name: ci-pdf-build
description: Build a clean, brand-compliant PDF from an analysis or offer. Use when the user asks to generate, render, or export a client-ready PDF presentation or document with their corporate identity (cover page, header/footer, section bars, tables).
---

# CI-Compliant PDF Build

Render a **brand-compliant PDF** with fpdf2.

## Steps

1. Start from `templates/pdf_example.py` (the `CIPDF` class: cover, header/footer,
   section, body, table).
2. Set the brand block — colours, fonts, contact. Register TTF fonts with
   `uni=True` for full `ä ö ü ß` support.
3. Build the document: cover → table of contents → content sections → investment/ROI/
   next steps → contact footer.
4. **Break wide tables**: when a cell exceeds ~50 chars, switch to manual `multi_cell`
   layout so it stays readable.
5. Use real accented characters and real `® ™ ©` symbols — never ASCII substitutes.
6. Render, then open the PDF and verify cover, fonts, accents, and page breaks before
   handing it over.

## Output

A4 PDF saved into the client's task folder. Slash command: `/pdf-build <script.py>`.
Best practices: `docs/best-practices.md`.
