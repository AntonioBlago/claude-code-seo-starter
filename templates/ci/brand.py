"""
CI base — single source of truth for your corporate identity.

Import these constants everywhere instead of hard-coding colours and fonts into
each script. Replace the values with your own brand. `templates/pdf_example.py`
imports from here.

    from templates.ci.brand import PRIMARY, DARK, BRAND_NAME, FONTS
"""

# --- Colours (RGB tuples) ----------------------------------------------------
PRIMARY = (246, 87, 30)       # accent / section bars / table headers
SECONDARY = (47, 138, 229)    # secondary accent (e.g. blue)
DARK = (12, 17, 21)           # cover background / header / footer
NEAR_BLACK = (23, 23, 22)     # body text
LIGHT_GRAY = (248, 248, 248)  # alternating table rows
WHITE = (255, 255, 255)
SUCCESS = (26, 188, 156)      # KPI good
WARNING = (255, 145, 44)      # KPI warning
DANGER = (207, 46, 46)        # KPI critical

# Hex variants (for HTML/Markdown exports)
HEX = {
    "primary": "#f6571e",
    "secondary": "#2f8ae5",
    "dark": "#0c1115",
    "near_black": "#171716",
    "light_gray": "#f8f8f8",
    "success": "#1abc9c",
    "warning": "#ff912c",
    "danger": "#cf2e2e",
}

# --- Identity ----------------------------------------------------------------
BRAND_NAME = "Your Name / Agency"
BRAND_TAGLINE = "Your Tagline"
CONTACT = "you@example.com  ·  +00 000 000 000  ·  example.com"
WEBSITE = "https://example.com"

# --- Fonts -------------------------------------------------------------------
# Point at your .ttf files. Register every weight with uni=True so accented
# characters (ä ö ü ß, é, ñ …) and real ® ™ © symbols render.
FONT_DIR = "fonts"
FONTS = {
    "heading": {
        "family": "Heading",
        "regular": f"{FONT_DIR}/Heading-Regular.ttf",
        "bold": f"{FONT_DIR}/Heading-Bold.ttf",
        "italic": f"{FONT_DIR}/Heading-Italic.ttf",
    },
    "body": {
        "family": "Body",
        "regular": f"{FONT_DIR}/Body-Regular.ttf",
        "bold": f"{FONT_DIR}/Body-Bold.ttf",
    },
}


def register_fonts(pdf):
    """Register all CI fonts on an fpdf2 instance (uni=True for accents)."""
    h, b = FONTS["heading"], FONTS["body"]
    pdf.add_font(h["family"], "", h["regular"], uni=True)
    pdf.add_font(h["family"], "B", h["bold"], uni=True)
    pdf.add_font(h["family"], "I", h["italic"], uni=True)
    pdf.add_font(b["family"], "", b["regular"], uni=True)
    pdf.add_font(b["family"], "B", b["bold"], uni=True)
