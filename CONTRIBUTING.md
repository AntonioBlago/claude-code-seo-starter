# Contributing

Thanks for wanting to improve this blueprint! It's meant to be a living starter
for SEO freelancers and agencies running Claude Code.

## Ground rules

- **Never commit secrets or client data.** No API keys, no real client names, no
  GSC exports. `.env` and `clients/` are gitignored — keep it that way.
- **Keep it generic + reusable.** Contributions should help *any* SEO consultant,
  not encode one agency's private process.
- **Workflows are Markdown.** The slash commands in `.claude/commands/` and the
  docs in `docs/` are the heart of this repo. Improvements there are the most
  valuable.

## Good contributions

- New or sharper slash commands (e.g. technical-audit, content-gap, internal-linking).
- Extra MCP integrations in `.mcp.json` (GA4, Ahrefs, a PDF MCP).
- Better hook triggers or new safety hooks.
- Methodology improvements in `docs/` — especially anything backed by data.

## How to submit

1. Fork the repo.
2. Create a branch: `git checkout -b feature/your-idea`.
3. Make your change. Run `bash scripts/check-setup.sh` if you touched setup.
4. Open a PR describing what it adds and why.

## Questions

Open an issue, or reach out via [antonioblago.de](https://antonioblago.de).
