---
name: visibly-seo-pdf-build
description: Build a clean, brand-compliant PDF from an analysis or offer. Use when the user asks to generate, render, or export a client-ready PDF presentation or document with their corporate identity — cover page, header/footer, section bars, tables, ROI boxes.
---

# CI-Compliant PDF Build

Render a **brand-compliant, client-ready PDF** with fpdf2 (or a PDF MCP if one is
connected — prefer it when available).

## Step 1 — Start from the Python template

Import the reusable `CIPDF` class from
[`claude_tools/ci_pdf.py`](../../../claude_tools/ci_pdf.py) — it already implements cover,
header/footer, section bars, body, bullets, wrapping tables and KPI/ROI boxes, and pulls
all brand colours/fonts from [`templates/ci/brand.py`](../../../templates/ci/brand.py)
(one source of truth). Don't reinvent the layout or re-declare the CI.

```python
from claude_tools.ci_pdf import CIPDF
pdf = CIPDF()
pdf.cover("SEO Strategy & Offer", "Example GmbH", "2026-06-13")
pdf.add_page(); pdf.section("1. Executive Summary"); pdf.body("…")
pdf.kpi_box("ROI (realistic)", "233 %", "good")
pdf.output("clients/<domain>/<date>_Offer/offer.pdf")
```

Run via the venv: `.\claude_tools_venv\Scripts\python.exe your_build_script.py`
(setup once with `.\claude_tools\setup.ps1`). `templates/pdf_example.py` remains a
standalone, zero-config reference if you want a copy to hack on without the package.

## Step 2 — Register fonts correctly

`CIPDF` registers the brand fonts for you (always with `uni=True`, so `ä ö ü ß é ñ`
render) **if** `templates/ci/brand.py` points `FONTS` at real `.ttf` files that exist —
otherwise it falls back to Helvetica so the build never crashes. So the one-time job is:
drop the brand TTFs in `fonts/` and set their paths in `brand.py`. Headings and body
should use distinct brand fonts.

If you build a PDF outside `CIPDF`, register fonts the same way — always `uni=True`:

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
