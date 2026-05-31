# Setup guide

A deeper walkthrough than the README quickstart.

## 1. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Docs: <https://docs.claude.com/en/docs/claude-code>

## 2. Get the blueprint

Either click **“Use this template”** on GitHub, or clone:

```bash
git clone https://github.com/AntonioBlago/claude-code-seo-starter.git
cd claude-code-seo-starter
```

## 3. Wire up Visibly AI

1. Create an account at <https://visibly.ai> and grab your API key (Account → API).
   Keys look like `lc_...`.
2. Copy the env template and paste your key:
   ```bash
   cp .env.example .env
   # edit .env → VISIBLY_AI_API_KEY=lc_your_key_here
   ```
3. The connection itself is already defined in `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "visiblyai": {
         "type": "http",
         "url": "https://mcp.visibly-ai.com/mcp",
         "headers": { "Authorization": "Bearer ${VISIBLY_AI_API_KEY}" }
       }
     }
   }
   ```
   The `${VISIBLY_AI_API_KEY}` is read from your environment — **the key never
   lands in git.**

## 4. Verify your setup

```bash
bash scripts/check-setup.sh
```

This checks that `.env` exists, the key is set, `.mcp.json` is present, and the
hook is executable.

## 5. First run

```bash
claude
```

On first launch Claude Code asks you to approve the `visiblyai` MCP server —
approve it. Then:

```
/status-quo example.com
```

If the hook is working, any SEO-flavoured prompt gets a gentle nudge toward the
Visibly AI tools.

## 6. Make it yours

- **`CLAUDE.md`** — fill in the `[YOUR NAME / AGENCY]` brand block (name, colours,
  fonts, contact, output language).
- **`templates/pdf_example.py`** — set your CI colours and fonts.
- **`.claude/commands/*.md`** — adjust the workflows to how you actually work.
- **`.claude/hooks/seo-check.sh`** — add your own keyword triggers.
- **`.mcp.json`** — add more data sources (GA4, Ahrefs, a PDF MCP, etc.).

## Troubleshooting

| Symptom | Fix |
|---|---|
| MCP server won't connect | Check `.env` has a valid `VISIBLY_AI_API_KEY`; restart `claude`. |
| Hook does nothing | Ensure `bash` is on PATH (Git Bash on Windows) and the hook path in `.claude/settings.json` is correct. |
| `${VISIBLY_AI_API_KEY}` shows up literally | Your shell didn't export the var — Claude Code loads `.env` automatically, but if you run tools manually, `export` it first. |
| Permission prompts every call | Pre-approve tools in `.claude/settings.json` → `permissions.allow`. |
