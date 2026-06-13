"""
claude_tools — reusable Python helpers behind the SEO skills.

These modules turn raw Visibly AI MCP / GSC data into the deliverable tables the
slash-command skills produce, using one shared CTR model and one shared CI:

    ctr_model       Keyword Study 2026 CTR curve + target-position matrix
    status_quo      cross-reference keywords × GSC, classify, flag quick wins → xlsx
    potential       click deltas, cluster rollup, lead/SEA/ROI scenarios → xlsx
    offer_economics phased pricing + ROI / payback for the offer
    ci_pdf          brand-compliant CIPDF class (imports templates/ci/brand.py)

Install the env once, then run any module:

    # from the repo root
    ./claude_tools/setup.ps1            # Windows  (creates claude_tools_venv/)
    bash claude_tools/setup.sh          # macOS / Linux / Git-Bash
    claude_tools_venv/Scripts/python -m claude_tools.status_quo --help
"""

__all__ = ["ctr_model", "status_quo", "potential", "offer_economics", "ci_pdf"]
