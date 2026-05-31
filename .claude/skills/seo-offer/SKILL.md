---
name: seo-offer
description: Draft a tailored, phased SEO consulting offer. Use when the user asks to write a proposal, Angebot, statement of work, or retainer for a prospect — turning analysis data plus client context (budget, team, decision process, tools) into a structured, priced, management-ready offer.
---

# SEO Offer / Proposal

Turn analysis + client context into a **phased, priced, credible offer** that survives
procurement scrutiny.

## Step 1 — Read everything first

Before writing a line, ingest: the Status-Quo and Potential outputs, any prior audits,
call notes/transcripts, previous offers and emails. **Recognising existing work** is the
single biggest trust signal — it makes you a partner, not a vendor. Never duplicate
analysis the client already paid for; reference and build on it.

## Step 2 — Capture client context

- Budget constraints and approval process (who signs off, at what threshold).
- Internal resources: team size, in-house vs. agency, dev/digital capacity.
- Existing stack: CRM, analytics, ticketing, CMS — the offer must fit their reality.
- Stated pain points and goals from the conversations.

## Step 3 — Structure the offer in phases

For **each** phase give: scope · deliverables · timeline · investment.

- **Phase 0 — Setup & data review.** Onboarding, access, explicit recognition of prior work.
- **Phase 1 — Audit.** Technical + content SEO; optional SEA assessment.
- **Phase 2 — Strategic accompaniment + enablement** (monthly retainer). Roadmap
  execution, prioritisation, and *teaching the team* — enablement is what makes a
  retainer renew.
- **Phase 3 — Optional advanced module** (e.g. Neuro-SEO / GEO / AI-search visibility).

## Step 4 — Add management-ready elements

- Executive summary (in English if the HQ is international).
- Quarterly milestone plan.
- KPQ/KPI framework — the questions leadership wants answered, and the metrics that do.
- **ROI section tied directly to the Potential numbers** (clicks → leads → revenue, and
  SEA spend saved). The offer's price must be visibly smaller than the value it unlocks.

## Step 5 — Be specific

Vague offers lose. "Add 10 internal links from these 5 pages to /target" beats "improve
internal linking". Give priority and estimated effort per workstream.

## Output

`clients/<domain>/YYYY-MM-DD_Offer/visibly-seo-offer_<date>.md` → then hand to `ci-pdf-build` /
`/visibly-seo-pdf-build` for the client-ready PDF. Slash command: `/visibly-seo-offer <domain>`.
Methodology: `docs/workflows.md`.
