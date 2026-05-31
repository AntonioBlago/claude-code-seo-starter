# Discoverability checklist — getting the plugin & MCP found

Two assets to surface: the **plugin/marketplace** (`AntonioBlago/claude-code-seo-starter`)
and the **remote MCP server** (`https://mcp.visibly-ai.com/mcp`). Each listing is a top-of-funnel
entry point that ends at a free Visibly AI key. Work the list top to bottom — the first two are
the highest payoff for the effort.

Status legend: ✅ done in-repo · 🔑 needs your GitHub login / a form · ⏳ timing-dependent.

---

## 1. Official MCP Registry — ✅ manifest ready, 🔑 publish step is yours

The authoritative registry MCP clients are starting to index. The manifest lives at
[`server.json`](../server.json) (remote `streamable-http`, GitHub namespace `io.github.antonioblago/visibly-ai` —
**no DNS verification needed**, the GitHub OAuth login proves ownership).

Publish (one-time, interactive — the OAuth device-flow login can't be scripted):

```bash
# 1. Install the publisher CLI (see latest release for your OS):
#    https://github.com/modelcontextprotocol/registry/releases/latest
# 2. From the repo root:
mcp-publisher login github      # opens github.com/login/device, enter the code
mcp-publisher publish           # reads ./server.json, validates, publishes
# 3. Verify:
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.antonioblago/visibly-ai"
```

If `publish` complains about a missing `repository.id`, run `mcp-publisher init` once to let it
backfill the GitHub repo id, then re-publish. Registry is in **preview** — expect occasional
schema bumps; keep `$schema` in `server.json` current.

**Payoff: high.** This is the source other directories (Glama, PulseMCP, client pickers) sync from.

---

## 2. punkpeye/awesome-mcp-servers — 🔑 one PR

The most-linked MCP list, mirrored to glama.ai. Fork
<https://github.com/punkpeye/awesome-mcp-servers>, add **one line** under the **Marketing**
section (`### 🎯 Marketing` — verify the current heading before submitting; sections get
re-org'd), keep alphabetical order by org/repo, open a PR.

Entry line (`☁️` = cloud/remote):

```markdown
- [AntonioBlago/claude-code-seo-starter](https://github.com/AntonioBlago/claude-code-seo-starter) ☁️ - Remote MCP for SEO/GEO: Google Search Console, keyword research, backlinks, competitor benchmarking, on-page audits & crawls via the Visibly AI platform. Free tier — connect at `https://mcp.visibly-ai.com/mcp`.
```

PR title tip: maintainer fast-tracks tidy contributions; keep the diff to the single line.
Optionally register the server at <https://glama.ai/mcp/servers> for an auto-indexed listing + score badge.

**Payoff: high. Effort: ~10 min.**

---

## 3. Anthropic community plugin marketplace — 🔑 form review

Beyond `/plugin marketplace add <github>`, Anthropic runs a reviewed **community** marketplace
that surfaces inside Claude Code. Submit via the in-app `/plugin` submission flow (or the plugins
submission page in Claude settings). Pre-flight before submitting:

- `README.md` has clear install + usage (✅ already)
- `.claude-plugin/plugin.json` has `name`, `version`, `description` (✅)
- `.claude-plugin/marketplace.json` valid (✅)
- Plugin installs cleanly from a fresh clone

Install string to advertise everywhere:

```
/plugin marketplace add AntonioBlago/claude-code-seo-starter
/plugin install seo-starter@antonioblago
```

**Payoff: very high if accepted** (only official third-party surface inside Claude Code).
**Effort: medium** (review queue, no SLA).

---

## 4. awesome-claude-code lists — ⏳ submit when structure is stable

<https://github.com/hesreallyhim/awesome-claude-code> (large, Claude-Code-specific). It has been
mid-reorganisation — watch the repo, then PR an entry under the Plugins/Marketplaces section in
whatever format the new TOC uses. Draft entry:

```markdown
- [seo-starter](https://github.com/AntonioBlago/claude-code-seo-starter) — Plugin + marketplace for SEO/GEO consultants: bundles the Visibly AI MCP, the `/visibly-seo-*` workflow commands, auto-invoked skills, and CI-compliant PDF export. `/plugin marketplace add AntonioBlago/claude-code-seo-starter`
```

**Payoff: high. Effort: low — but time it to the new structure so the PR isn't bounced.**

---

## 5. GitHub repo metadata — ✅ done

- **Homepage** → `https://visibly-ai.com` (the funnel target, shown on the repo card).
- **Topics**: `mcp`, `mcp-server`, `claude-code`, `claude-code-plugin`, `claude-plugin`,
  `anthropic`, `anthropic-claude`, `seo`, `seo-tools`, `search-console`, `geo`,
  `generative-engine-optimization`, `visibly-ai`.

Adjust anytime with `gh repo edit AntonioBlago/claude-code-seo-starter --add-topic <topic>`.

---

## Recurring hygiene

- Keep the install string and `https://visibly-ai.com` consistent across every listing.
- A short demo GIF/screenshot in the README lifts conversion on every channel that renders it.
- Re-check `server.json` `$schema` and the awesome-list section names quarterly — both drift.
- Each listing should land the reader on the **free-key** signup. That link is the whole point.
