# Claude Code — SEO Agency & Freelancer Starter

> A batteries-included [Claude Code](https://claude.com/claude-code) blueprint for SEO freelancers and agencies. Wire up the **Visibly AI MCP**, get ready-made slash commands for the full client workflow — Status-Quo → Potential Analysis → Offer → CI-compliant PDF — and a smart hook that nudges Claude toward real SEO data instead of guessing.
>
> Built and battle-tested by **[Antonio Blago](https://antonioblago.de)** — SEO Freelancer & creator of the **Neuro-SEO System®**.

<p align="center">
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-whats-inside">What's inside</a> •
  <a href="#-the-workflows">Workflows</a> •
  <a href="#-the-ctr-model">CTR Model</a> •
  <a href="#-customise-it">Customise</a> •
  <a href="https://visibly-ai.com">Get a free key</a> •
  <a href="https://calendly.com/antonio-blago/vibe-coding-consultation?back=1&month=2026-06">Book a call</a>
</p>

---

## Why this exists

SEO consulting is the same five jobs over and over: pull the real ranking data, map it against the client's keyword set, quantify the opportunity, turn that into an offer, and ship a presentable PDF. Claude Code can do all of it — *if* you give it the data sources, the methodology, and the guardrails.

This repo packages exactly that. Install it, drop in a [Visibly AI](https://visibly-ai.com) key — **free tier available, 30 seconds to a key** — and you have an SEO analyst on tap that knows your process. Visibly AI is the data engine behind the whole workflow: GSC, keywords, backlinks, competitors and on-page audits through one MCP.

## ✨ What's inside

| Piece | What it does |
|---|---|
| **`.mcp.json`** | Pre-wired [Visibly AI MCP](https://visibly-ai.com) connection — GSC, keywords, backlinks, competitors, on-page audits, crawling. |
| **`/visibly-seo-status-quo`** | Maps a client's live organic visibility: GSC × target keywords, classification, quick wins. |
| **`/visibly-seo-potential`** | Potential analysis: empirical CTR model → realistic 12-month targets → traffic, lead & ROI math. |
| **`/visibly-seo-offer`** | Drafts a tailored, phased SEO consulting offer from your analysis + client context. |
| **`/visibly-seo-pdf-build`** | Turns any analysis script into a clean, brand-compliant PDF. |
| **SEO hook** | A `UserPromptSubmit` hook that detects SEO intent and steers Claude to Visibly AI MCP tools instead of generic scraping. |
| **`CLAUDE.md`** | A project-instruction template encoding the whole workflow + folder conventions. |
| **`docs/`** | The methodology written out: workflows, the CTR model, and best practices. |

## 🚀 Quickstart

There are two ways to use this — pick one.

### Option A — Install as a plugin (fastest)

```
/plugin marketplace add AntonioBlago/claude-code-seo-starter
/plugin install seo-starter@antonioblago
```

You get the `/visibly-seo-status-quo`, `/visibly-seo-potential`, `/visibly-seo-offer`, `/visibly-seo-pdf-build` commands, the
auto-invoked SEO skills, the SEO-intent hook, and the Visibly AI MCP — wired in.
Then just set your key (step 3 below). Restart with `/reload-plugins` if needed.

### Option B — Clone the template

Use the full repo (docs, PDF template, setup script) as a project scaffold.

### 1. Prerequisites

- [Claude Code](https://docs.claude.com/en/docs/claude-code) installed (`npm install -g @anthropic-ai/claude-code`)
- A [Visibly AI](https://visibly-ai.com) account — **[sign up free](https://visibly-ai.com)**, the free tier is enough to run the full workflow
- Python 3.11+ (only needed for the PDF / data-crunching helpers)

### 2. Get the blueprint

```bash
# Use it as a GitHub template, or just clone:
git clone https://github.com/AntonioBlago/claude-code-seo-starter.git
cd claude-code-seo-starter
```

### 3. Add your Visibly AI key

**Don't have a key yet?** Create a free account at **[visibly-ai.com](https://visibly-ai.com)** and copy your
API key from the dashboard — takes about 30 seconds, no card required.

```bash
cp .env.example .env
# then edit .env and paste your key:
# VISIBLY_AI_API_KEY=lc_xxxxxxxxxxxxxxxx
```

The `.mcp.json` reads the key from the environment — **no secret ever lands in git**.

### 4. Launch

```bash
claude
```

On first run, Claude Code will ask you to approve the Visibly AI MCP server. Approve it, then try:

```
/visibly-seo-status-quo example.com
```

That's it. You're running the full SEO workflow.

## 🔁 The workflows

Each slash command corresponds to one phase of a real client engagement. They chain:

```
/visibly-seo-status-quo <domain>   →   /visibly-seo-potential <domain>   →   /visibly-seo-offer <domain>   →   /visibly-seo-pdf-build <script.py>
   (where do we           (what's the upside,        (what should the          (hand the client a
    rank today?)           in clicks & €?)            client buy?)              polished PDF)
```

Full methodology is documented in **[`docs/workflows.md`](docs/workflows.md)**.

## 📈 The CTR model

The potential analysis is only as good as its click-through-rate curve. This repo ships the **[Keyword Study 2026](https://www.antonioblago.com/keyword-study-2026-organic-search-ctr)** — CTR by position from **first-party Google Search Console data** (1.3M keywords, 94 domains) — instead of the inflated textbook numbers most templates still use.

The differentiator: the curve is **intent-aware**. A navigational keyword at position 1 earns ~8.9% CTR; an informational one ~3.2%. Forecasting with one blended number quietly mis-states the upside. See **[`docs/ctr-model.md`](docs/ctr-model.md)** for the full intent-by-position table and the Python to apply it. Honest inputs → defensible forecasts → offers that survive scrutiny.

## 🎨 Customise it

Everything is plain Markdown and shell — fork and adapt:

- **Branding** — edit `CLAUDE.md` and `templates/pdf_example.py` with your colours, fonts, contact block.
- **Data source** — swap or add MCP servers in `.mcp.json` (GA4, Ahrefs, etc.).
- **Workflows** — the `.claude/commands/*.md` files *are* the workflows. Rewrite them in your own words.
- **Guardrails** — extend `.claude/hooks/seo-check.sh` with your own keyword triggers.

See **[`docs/setup.md`](docs/setup.md)** for a deeper walkthrough and **[`docs/best-practices.md`](docs/best-practices.md)** for the hard-won lessons.

## 📂 Repo layout

```
claude-code-seo-starter/
├── .claude-plugin/           # makes this repo an installable plugin + marketplace
│   ├── plugin.json           # plugin manifest
│   └── marketplace.json      # marketplace catalog (one repo = both)
├── .mcp.json                 # Visibly AI MCP connection (key via env)
├── .env.example              # copy → .env, add your key
├── CLAUDE.md                 # project instructions Claude reads on every run
├── .claude/
│   ├── commands/             # /visibly-seo-status-quo /visibly-seo-potential /visibly-seo-offer /visibly-seo-pdf-build
│   ├── skills/               # auto-invoked SEO skills (status-quo, potential, offer, pdf)
│   ├── hooks/                # seo-check.sh + hooks.json — SEO-intent nudge
│   └── settings.json         # hook registration + sane permissions (clone mode)
├── docs/
│   ├── setup.md              # detailed setup
│   ├── workflows.md          # the 4-phase methodology
│   ├── ctr-model.md          # empirical CTR curve
│   ├── folder-structure.md   # client knowledge base + CI base conventions
│   └── best-practices.md     # lessons learned
├── templates/
│   ├── ci/                   # CI base — brand.py (constants) + CI.md (reference)
│   ├── client-template/      # copy → clients/<domain>/ (CLAUDE.md + _knowledge/)
│   └── pdf_example.py        # minimal CI-PDF starter (fpdf2)
└── scripts/
    └── check-setup.sh        # verify your env is wired correctly
```

## 🤝 Contributing

PRs welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Found this useful? A ⭐ helps others find it.

## 📜 License

MIT — see [`LICENSE`](LICENSE). Use it commercially, fork it, ship it for your own clients.

## 💬 Want help setting it up?

If you'd rather have this dialled in to your agency's workflow — or want to talk SEO, Claude Code, or vibe coding — **[book a free consultation](https://calendly.com/antonio-blago/vibe-coding-consultation?back=1&month=2026-06)**.

---

<p align="center">
  Created by <strong><a href="https://antonioblago.de">Antonio Blago</a></strong> — SEO Freelancer & Neuro-SEO System®<br>
  <a href="https://calendly.com/antonio-blago/vibe-coding-consultation?back=1&month=2026-06"><strong>📅 Book a consultation</strong></a><br>
  <sub>If this saves you an afternoon per client, it did its job.</sub>
</p>
