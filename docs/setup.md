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

## 3. Pick your tier — free (no key) or pro

This starter runs in **two tiers**. The committed `.mcp.json` is keyless, so the
free tier works the moment you launch — no account, no key, no `.env`.

| | Free tier (default) | Pro tier |
|---|---|---|
| **Key** | none | Visibly AI key (`lc_...`) |
| **Visibly tools** | 8 free (keyword classification, SEO checklist/guidance, URL-structure, locations) | all 32 (live GSC/GA, keywords, backlinks, competitors, on-page, crawl) |
| **Ranking data** | a GSC export you feed to the Python templates | live via `query_search_console` / `get_keywords` |
| **Credits** | none used | GSC/GA = 0 credits; DataForSEO-backed tools spend credits |

### 3a. Free tier — nothing to wire

The connection is already defined in `.mcp.json`, with **no auth header**:

```json
{
  "mcpServers": {
    "visiblyai": {
      "type": "http",
      "url": "https://mcp.visibly-ai.com/mcp"
    }
  }
}
```

Without the `headers` block the server serves the 8 free tools. For real ranking
data, export Search Console (Performance → Queries → CSV) and feed it straight to
the Python templates — the whole Status-Quo → Potential → Offer → PDF chain runs
locally and keyless:

```bash
python -m claude_tools.status_quo --gsc gsc_query.csv --keywords keywords.xlsx --out status_quo.xlsx
```

### 3b. Pro tier — add your Visibly AI key

1. Create an account at <https://visibly-ai.com> and grab your API key
   (Account → API Keys). Keys look like `lc_...`.
2. Connect it. The most reliable way (it resolves the key at write time and
   stores it in your **local** Claude config, outside git):

   ```bash
   claude mcp add --transport http visiblyai \
     https://mcp.visibly-ai.com/mcp \
     --header "Authorization: Bearer lc_your_key_here"
   ```

   > **Windows / PowerShell:** run it as a single line — the `\` line-continuation
   > is not valid there and trips the parser.

   That unlocks all 32 tools. To use real Google data at **0 credits**, also
   connect Google OAuth in your Visibly account (Account → Google connections) —
   then `query_search_console`, `query_analytics` and `get_keywords` read your own
   GSC/GA; DataForSEO is only used (and only spends credits) as the fallback for
   domains you haven't connected.
3. *Alternative (cloned repo):* copy `.env.example` → `.env`, set
   `VISIBLYAI_API_KEY=lc_...`, and add a `headers` block back to `.mcp.json`
   (`"Authorization": "Bearer ${VISIBLYAI_API_KEY}"`). Note that `${VAR}` header
   expansion has been flaky across Claude Code versions — the `claude mcp add`
   command above sidesteps that and is recommended.

### 3c. Optional — DataForSEO as a separate source (keyless tier)

If you want keyword volumes / SERP data without a Visibly key, add the DataForSEO
MCP alongside Visibly in `.mcp.json` and put `DATAFORSEO_LOGIN` /
`DATAFORSEO_PASSWORD` in your `.env`. Keep it optional: only add it if you have
those credentials, since a server with missing creds won't connect.

Need an account? Sign up at **[DataForSEO](https://dataforseo.com/?aff=186597)** —
pay-as-you-go SERP/keyword APIs, no monthly minimum.

## 4. Verify your setup

```bash
bash scripts/check-setup.sh
```

This checks that `.mcp.json` is present, the hook is executable, all four slash
commands exist, and reports which tier you're on (it does **not** fail when no key
is set — the free tier is a valid setup).

## 5. First run

```bash
claude
```

On first launch Claude Code asks you to approve the `visiblyai` MCP server —
approve it. Then:

```
/visibly-seo-status-quo example.com
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
| MCP server won't connect | The keyless server needs no key — just approve it on first launch and restart `claude`. Check you're online and `.mcp.json` is valid JSON. |
| Premium tool returns "Authentication required" (`-32001`) | That tool is pro-only. Add your Visibly key (§3b) — or stay on the free tier and use a GSC export instead. |
| Premium tool returns "Insufficient credits" | Top up credits, or connect Google OAuth so GSC/GA tools run at 0 credits. |
| `${VISIBLYAI_API_KEY}` reaches the server literally | `${VAR}` header expansion is unreliable across versions — use the `claude mcp add … --header` command (§3b) instead of a `headers` block. |
| Hook does nothing | Ensure `bash` is on PATH (Git Bash on Windows) and the hook path in `.claude/settings.json` is correct. |
| Permission prompts every call | Pre-approve tools in `.claude/settings.json` → `permissions.allow`. |
