---
description: Write a tailored SEO consulting offer from analysis + client context
argument-hint: <client-domain>
---

Run **Workflow 3 — Writing an Offer** (see `docs/workflows.md`) for client `$ARGUMENTS`.

## Read first (do not skip)

Before drafting, load **all** client materials from `./clients/$ARGUMENTS/`:
- Keyword files (Excel)
- Existing audits (PDF — extract text first)
- Call transcripts / email threads / previous offers
- Status-Quo and Potential outputs (must exist — otherwise run `/visibly-seo-status-quo` and
  `/visibly-seo-potential` first)

## Client context to surface

- Budget constraints
- Internal resources (team size, agencies, in-house digital team)
- Decision makers & approval process
- Existing tools (CRM, ticketing, analytics)
- Pain points and goals from prior conversations

## Structure

- **Phase 0:** Setup & data review — explicitly recognise existing work (don't duplicate)
- **Phase 1:** Audit (SEO + optional SEA assessment)
- **Phase 2:** Monthly strategic accompaniment + enablement
- **Phase 3:** Optional advanced module (e.g. a signature methodology)

For each phase: scope, deliverables, timeline, investment.

Management-ready elements:
- Executive Summary (English if HQ is international)
- High-level milestone plan (quarterly)
- KPQ / KPI framework
- ROI section referencing the Potential-Analysis numbers

## Output

Save to `./clients/$ARGUMENTS/YYYY-MM-DD_Offer/`:
- `offer_<client>_<YYYY-MM-DD>.md` (source)
- Then run `/visibly-seo-pdf-build` to produce the brand-compliant PDF.

Pull your contact / bank / legal block from your own private notes — keep them out
of this repo.
