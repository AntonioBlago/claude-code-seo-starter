# The four workflows

The whole client engagement, broken into four chained phases. Each one is a slash
command in `.claude/commands/`. Run them in order; each builds on the last.

```
/status-quo  →  /potenzial  →  /angebot  →  /pdf-build
```

---

## Workflow 1 — SEO Status-Quo Analysis

**Goal:** Map a client's current organic visibility in their target market.

1. **List projects & connections** — `list_projects`, `get_google_connections`.
2. **Query GSC** — `query_search_console` with a country filter, `dimension=query`,
   `limit=500`.
3. **Also query page-level** — `dimension=page` to find underperforming URLs.
4. **Load client keyword data** — read the Excel/CSV of target keywords (search
   volume, positions, themes).
5. **Cross-reference** — map every target keyword against live GSC data (clicks,
   impressions, CTR, position).
6. **Classify** — Brand vs Generic vs Competitor; ranking status Top 3 / Page 1 /
   Page 2 / Weak / Not Ranking.
7. **Identify Quick Wins** — high impressions, low CTR (< 5 %).
8. **Competitor benchmark** — compare positions against known competitors.

**Output:** Status-Quo tables with GSC validation.

---

## Workflow 2 — Potential Analysis

**Goal:** Quantify realistic traffic and lead upside.

1. Start from the Status-Quo output.
2. Apply the **empirical CTR model** ([`ctr-model.md`](ctr-model.md)).
3. Set realistic 12-month target positions (by current position × search volume).
4. Compute click deltas per keyword: `(target clicks − current clicks)`.
5. Aggregate by cluster / theme.
6. **Lead calc (B2B):** contact rate 1.5 % / 2.5 % / 3.5 %, close rate 10-20 %,
   industry-specific average deal value.
7. **SEA equivalence:** `Δclicks × avg CPC` = ad-spend saved.
8. **ROI:** investment vs. (equivalent SEA value + lead value).

**Output:** cluster table, Top 20 keywords by delta, revenue scenarios, ROI.

---

## Workflow 3 — Writing an Offer

**Goal:** A tailored, phased SEO consulting offer.

1. **Read all client materials** — keyword files, existing audits, transcripts,
   previous offers.
2. **Understand context** — budget, internal resources, decision makers, existing
   tools, pain points.
3. **Structure into phases:**
   - Phase 0: Setup & data review (recognise existing work)
   - Phase 1: Audit (SEO + optional SEA)
   - Phase 2: Monthly strategic accompaniment + enablement
   - Phase 3: Optional advanced module
4. Per phase: scope, deliverables, timeline, investment.
5. **Management-ready elements:** Executive Summary, quarterly milestone plan,
   KPQ/KPI framework.
6. **ROI section** tied back to Workflow 2.
7. **Always reference existing work** — show prior analyses are integrated, not
   duplicated.

**Output:** Markdown document → PDF (Workflow 4).

---

## Workflow 4 — PDF Generation

**Goal:** A professional, brand-compliant PDF.

1. Register your fonts (with `uni=True` for accented characters).
2. Apply your brand: cover page, header/footer accent bars, coloured section
   titles, table headers, KPI boxes, alternating table rows.
3. Standard structure: Cover → Table of contents → Content → Investment / ROI /
   next steps / contact footer.
4. Verify the rendered PDF before handing it over.

**Output:** an A4 PDF saved to the client's task folder. Starter:
[`../templates/pdf_example.py`](../templates/pdf_example.py).
