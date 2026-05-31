"""
Minimal brand-compliant PDF starter (fpdf2).

This is a *template* — replace the BRAND block with your own colours, fonts, and
contact details, then build real client documents on top of it.

    python -m venv .venv && . .venv/Scripts/activate   # Windows: .venv\\Scripts\\activate
    pip install fpdf2
    python templates/pdf_example.py

Output: example_offer.pdf in the current directory.
"""

from fpdf import FPDF

# --- BRAND --- replace with your own CI -------------------------------------
PRIMARY = (246, 87, 30)      # accent / section bars     (e.g. orange #f6571e)
DARK = (12, 17, 21)          # cover background / footer  (#0c1115)
NEAR_BLACK = (23, 23, 22)    # body text                  (#171716)
LIGHT_GRAY = (248, 248, 248) # alternating table rows     (#f8f8f8)
WHITE = (255, 255, 255)

BRAND_NAME = "Your Name / Agency"
BRAND_TAGLINE = "Your Tagline"
CONTACT = "you@example.com  ·  +00 000 000 000  ·  example.com"

# If you have brand fonts, point these at the .ttf files and register them below.
# FONT_DIR = "fonts"
# Otherwise we fall back to the built-in Helvetica (no accent issues for fpdf2's
# core fonts, but register a Unicode TTF with uni=True for full ä ö ü ß support).


class CIPDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return  # cover handles its own layout
        self.set_fill_color(*DARK)
        self.rect(0, 0, self.w, 14, "F")
        self.set_fill_color(*PRIMARY)
        self.rect(0, 14, self.w, 1.2, "F")
        self.set_xy(10, 4)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 6, BRAND_NAME, align="L")

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-14)
        self.set_fill_color(*DARK)
        self.rect(0, self.h - 14, self.w, 14, "F")
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "", 7)
        self.set_y(-10)
        self.cell(0, 5, CONTACT, align="C")

    def cover(self, title: str, client: str, date: str):
        self.add_page()
        self.set_fill_color(*DARK)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_fill_color(*PRIMARY)
        self.rect(0, 90, 60, 3, "F")
        self.set_xy(10, 100)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 26)
        self.multi_cell(0, 12, title)
        self.ln(4)
        self.set_x(10)
        self.set_font("Helvetica", "", 13)
        self.set_text_color(*PRIMARY)
        self.cell(0, 8, BRAND_TAGLINE, ln=1)
        self.ln(8)
        self.set_x(10)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 7, f"Prepared for: {client}", ln=1)
        self.set_x(10)
        self.cell(0, 7, date, ln=1)

    def section(self, title: str):
        self.ln(4)
        self.set_fill_color(*PRIMARY)
        self.rect(self.get_x(), self.get_y() + 1, 3, 7, "F")
        self.set_x(self.get_x() + 6)
        self.set_text_color(*NEAR_BLACK)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 9, title, ln=1)
        self.ln(1)

    def body(self, text: str):
        self.set_text_color(*NEAR_BLACK)
        self.set_font("Helvetica", "", 11)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def table(self, headers, rows):
        col_w = (self.w - 20) / len(headers)
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(*PRIMARY)
        self.set_text_color(*WHITE)
        for h in headers:
            self.cell(col_w, 8, h, border=0, align="C", fill=True)
        self.ln()
        self.set_text_color(*NEAR_BLACK)
        self.set_font("Helvetica", "", 10)
        for i, row in enumerate(rows):
            fill = i % 2 == 1
            self.set_fill_color(*(LIGHT_GRAY if fill else WHITE))
            for cell in row:
                self.cell(col_w, 7, str(cell), border=0, align="C", fill=True)
            self.ln()


def build():
    pdf = CIPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(10, 20, 10)

    pdf.cover("SEO Strategy & Offer", "Example Client GmbH", "2026-05-31")

    pdf.add_page()
    pdf.section("1. Executive Summary")
    pdf.body(
        "This is a template. Replace this text with your findings from the "
        "Status-Quo and Potential analyses. Keep prose tight; put the numbers "
        "in tables."
    )

    pdf.section("2. Potential (12 months)")
    pdf.table(
        ["Cluster", "Current clicks", "Target clicks", "Delta"],
        [
            ["Brand", "1,200", "1,500", "+300"],
            ["Generic / commercial", "800", "3,400", "+2,600"],
            ["Informational", "300", "1,100", "+800"],
        ],
    )
    pdf.ln(3)
    pdf.body(
        "Forecast uses the intent-aware Keyword Study 2026 CTR curve "
        "(see docs/ctr-model.md), not idealised textbook numbers."
    )

    out = "example_offer.pdf"
    pdf.output(out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    build()
