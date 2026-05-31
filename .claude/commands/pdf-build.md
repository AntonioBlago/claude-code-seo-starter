---
description: Build a brand-compliant PDF from a Python script
argument-hint: <path/to/script.py>
---

Run **Workflow 4 — PDF Generation** (see `docs/workflows.md`).

## Rules

1. **Run the script** with your project virtualenv:
   ```bash
   python $ARGUMENTS
   ```
2. **Reuse a shared CI module** rather than copy-pasting colours/fonts into every
   script. Start from [`templates/pdf_example.py`](../../templates/pdf_example.py).
3. **Font registration** — register every font you use with `uni=True` so accented
   characters render. Keep fonts in a `fonts/` folder (not committed if licensed).
4. **Accented characters** — use real `ä ö ü ß é ñ`, never ASCII substitutes.
5. **Wide tables** — switch to manual `multi_cell` layout when cell text exceeds
   ~50 characters, so cells stay readable.

## After building

- Open the PDF and verify: cover colours, fonts render correctly, accents intact,
  page breaks clean.
- If anything is off: fix the script, rebuild. Don't hand over a broken PDF.

## Alternative

If a PDF MCP server is connected, prefer its `html_to_pdf` / `text_to_pdf` tools
for simple documents. Use fpdf2 only when you need fine-grained layout control.
