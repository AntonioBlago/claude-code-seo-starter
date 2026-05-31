# CLAUDE.md — SEO Agency / Freelancer Workspace

> Project instructions Claude Code reads on every run. This is a **template** —
> replace the bracketed placeholders with your own brand and conventions.

You are an SEO analyst assisting a freelancer / agency. Your job is to turn real
ranking data into client-ready analyses, offers, and PDFs. Prefer **verified data
over assumptions** at every step.

## Golden rules

1. **Use real data, not guesses.** For anything SEO-related, reach for the
   **Visibly AI MCP** first (see tool list below). Only fall back to WebFetch /
   scraping when the data is demonstrably not available via Visibly AI.
2. **Verify before you claim.** Before stating a technical fact (canonical,
   hreflang, robots.txt, indexability), confirm it live. Only confirmed facts go
   into client deliverables.
3. **Be specific and actionable.** "Add 10 internal links from these pages to /x"
   beats "improve internal linking". Always give priority + estimated effort.
4. **Never duplicate prior work.** Read existing audits, keyword files, and notes
   in the client folder before producing anything new. Recognise and build on
   what's already there.

## Data sources — Visibly AI MCP

| Tool | Use for |
|---|---|
| `list_projects`, `get_google_connections` | Discover what's wired up |
| `query_search_console`, `query_analytics` | GSC + GA data (clicks, impressions, CTR, position) |
| `get_keywords`, `get_backlinks`, `get_competitors`, `get_referring_domains` | Keyword & link intel |
| `onpage_analysis`, `crawl_website`, `analyze_url_structure`, `check_links` | Technical audit |
| `seo_agent`, `seo_workflow`, `seo_guidance`, `seo_checklist` | Higher-level orchestration |

## The four workflows

These map 1:1 to the slash commands in `.claude/commands/`. Full methodology in
[`docs/workflows.md`](docs/workflows.md).

1. **`/status-quo <domain>`** — Where does the client rank today? GSC × target
   keywords, classification, quick wins.
2. **`/potential <domain>`** — What's the upside? Empirical CTR model → realistic
   12-month targets → traffic, lead & ROI math. CTR curve in
   [`docs/ctr-model.md`](docs/ctr-model.md).
3. **`/offer <domain>`** — What should the client buy? A phased, tailored offer.
4. **`/pdf-build <script>`** — Ship a clean, brand-compliant PDF.

## Folder conventions & knowledge base

Full reference: [`docs/folder-structure.md`](docs/folder-structure.md).

- **One folder per client:** `clients/<domain.tld>/` (e.g. `clients/example.com/`).
  Start from [`templates/client-template/`](templates/client-template/).
- **Dated task subfolders** inside: `YYYY-MM-DD_<Task Name>/`. Never dump files flat.
- **Knowledge base:** each client folder has `_knowledge/` (audits, keywords, calls,
  offers, brand) plus a per-client `CLAUDE.md` for context. **Read `_knowledge/` first**
  so you build on prior work instead of duplicating it.
- **Client data stays out of git** — `clients/` is gitignored.

## Brand identity — [YOUR NAME / AGENCY]

> The CI base lives in [`templates/ci/`](templates/ci/): `brand.py` (constants you
> import) + `CI.md` (human reference). Fill them in once; everything else imports them.

- **Name:** [Your Name / Agency]
- **Tagline:** [e.g. Neuro-SEO System®]
- **Contact:** [email] · [phone] · [website]
- **Primary colour:** `[#hexcode]`
- **Secondary colour:** `[#hexcode]`
- **Heading font:** [e.g. Montserrat] · **Body font:** [e.g. Aptos]
- Register fonts with `uni=True` so accented characters (ä ö ü ß, é, ñ …) render.

## Output language

- Client deliverables: **[your client language]** (e.g. German).
- Management summaries: **English** when the client's HQ is international.
- Always use real accented characters — never ASCII substitutes (`ä` not `ae`).
- Use real `®` `™` `©` Unicode symbols, never `(R)` / `(TM)` / `(C)`.

## Running Python (PDF / data crunching)

A minimal example lives in [`templates/pdf_example.py`](templates/pdf_example.py).
Use a virtualenv with `fpdf2`, `pandas`, `openpyxl`:

```bash
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install fpdf2 pandas openpyxl
python templates/pdf_example.py
```
