"""Marketplace tests (K2.1, K2.3). Run: python -m pytest tests -q"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"

# The seo-starter entry as released before homebase was added. It must not change.
SEO_STARTER_ENTRY = {
    "name": "seo-starter",
    "source": "./",
    "description": "Visibly AI MCP + full SEO client workflow (status-quo, potential, offer, CI-PDF) with the "
                   "intent-aware Keyword Study 2026 CTR model.",
}


def load():
    return json.loads(MARKETPLACE.read_text(encoding="utf-8"))


def test_k2_1_marketplace_is_valid_json_with_both_entries():
    """K2.1: valid JSON, marketplace name unchanged, exactly the two plugins seo-starter and homebase."""
    m = load()
    assert m["name"] == "antonioblago"
    assert m["owner"]["name"]
    assert [p["name"] for p in m["plugins"]] == ["seo-starter", "homebase"]


def test_k2_1_homebase_source_is_the_github_repo():
    """K2.1: homebase comes from AntonioBlago/claude-homebase, without a version pin in the entry."""
    entry = next(p for p in load()["plugins"] if p["name"] == "homebase")
    assert entry["source"] == {"source": "github", "repo": "AntonioBlago/claude-homebase"}
    assert entry["description"].strip()
    assert "version" not in entry  # the version lives in the plugin's own plugin.json


def test_k2_1_seo_starter_entry_is_unchanged():
    """K2.1: the existing plugin keeps its entry and still points at this repo root."""
    entry = next(p for p in load()["plugins"] if p["name"] == "seo-starter")
    assert entry == SEO_STARTER_ENTRY
    assert (ROOT / ".claude-plugin" / "plugin.json").is_file()
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert plugin["name"] == "seo-starter"


def test_k2_1_plugin_names_are_unique_and_not_reserved():
    names = [p["name"] for p in load()["plugins"]]
    assert len(names) == len(set(names))
    assert not any(n.startswith(("claude-", "anthropic-", "anthropics-", "cc-plugin-")) for n in names)


def test_k2_3_readme_explains_install_auto_update_and_starter_set():
    """K2.3: README shows both install commands, the Marketplaces tab for auto-update and links the Starter Set once."""
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "/plugin marketplace add AntonioBlago/claude-code-seo-starter" in readme
    assert "/plugin install seo-starter@antonioblago" in readme
    assert "/plugin install homebase@antonioblago" in readme
    assert "**Marketplaces**" in readme and "Enable auto-update" in readme
    assert len(re.findall(r"antonioblago\.com/skills/claude-code-starter-set", readme)) == 1
