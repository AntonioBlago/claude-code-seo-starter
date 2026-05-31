---
name: ci-pdf-build
description: Build a clean, brand-compliant PDF from an analysis or offer. Use when the user asks to generate, render, or export a client-ready PDF presentation or document with their corporate identity — cover page, header/footer, section bars, tables, ROI boxes.
---

# CI-Compliant PDF Build

Render a **brand-compliant, client-ready PDF** with fpdf2 (or a PDF MCP if one is
connected — prefer it when available).

## Step 1 — Start from the template

Build on `templates/pdf_example.py` — the `CIPDF` class already implements cover,
header/footer, section bars, body, and tables. Don't reinvent the layout.

## Step 2 — Register fonts correctly

Point the brand fonts at their `.ttf` files and **always register with `uni=True`** —
otherwise `ä ö ü ß é ñ` break. Headings and body should use distinct brand fonts.

```python
pdf.add_font("Heading", "",  f"{FONT_DIR}/Heading-Regular.ttf", uni=True)
pdf.add_font("Heading", "B", f"{FONT_DIR}/Heading-Bold.ttf",    uni=True)
pdf.add_font("Body",    "",  f"{FONT_DIR}/Body-Regular.ttf",    uni=True)
```

## Step 3 — Apply the CI

- Cover: dark background, accent bar, white title, brand + client + date + contact.
- Header/footer: dark bar + accent line; brand left, contact centred.
- Section titles: accent bar + bold heading font.
- Tables: accent header row (white text), alternating white / light-gray body rows.
- KPI / ROI boxes: colour-coded (good / warning / critical) — avoid pure red-green only;
  add a second cue so it survives grayscale and colour-blind readers.

## Step 4 — Standard structure

Cover → table of contents → content sections → investment / ROI / next steps → contact
footer.

## Step 5 — Typography & correctness rules

- **Real accented characters**, never ASCII (`für`, not `fuer`).
- **Real symbols**: `® ™ ©`, never `(R)` / `(TM)` / `(C)`.
- **Break wide tables**: when a cell exceeds ~50 characters, switch from a simple table
  row to manual `multi_cell` layout so the text wraps and stays readable.

## Step 6 — Verify before shipping

Open the rendered PDF and check cover, fonts, accents, table wrapping, and page breaks.
Never hand over a PDF you haven't looked at.

## Output

A4 PDF in the client's task folder. Slash command: `/visibly-seo-pdf-build <script.py>`.
Best practices: `docs/best-practices.md`.
