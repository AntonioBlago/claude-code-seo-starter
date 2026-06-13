"""
ci_pdf — the reusable, brand-compliant PDF class behind `/visibly-seo-pdf-build`.

This is the production sibling of templates/pdf_example.py: instead of hard-coding
the brand, it imports the single source of truth from templates/ci/brand.py and
adds the helpers real client documents need (KPI/ROI boxes, wide-table wrapping,
bullet lists). If the brand .ttf fonts aren't present yet it falls back to Helvetica
so it always runs.

Note on the fallback: Helvetica is a PDF core font and only covers Latin-1, so the
fallback transliterates typographic characters it can't encode (— ™ … " "). For full
Unicode (™, em-dash, …) point templates/ci/brand.py at real brand TTFs — then nothing
is transliterated.

    from claude_tools.ci_pdf import CIPDF
    pdf = CIPDF()
    pdf.cover("SEO Strategy & Offer", "Example GmbH", "2026-06-13")
    pdf.add_page(); pdf.section("1. Executive Summary"); pdf.body("…")
    pdf.kpi_box("ROI", "233 %", "good")
    pdf.output("offer.pdf")

CLI demo:
    python -m claude_tools.ci_pdf            # writes ci_pdf_demo.pdf
"""
from __future__ import annotations

import importlib
import importlib.util
import os
import sys

from fpdf import FPDF
from fpdf.enums import XPos, YPos

# --- Load the CI single source of truth (templates/ci/brand.py) --------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_brand():
    if _REPO_ROOT not in sys.path:
        sys.path.insert(0, _REPO_ROOT)
    try:                                    # namespace-package import
        return importlib.import_module("templates.ci.brand")
    except Exception:
        pass
    path = os.path.join(_REPO_ROOT, "templates", "ci", "brand.py")
    if os.path.exists(path):                # direct file import
        spec = importlib.util.spec_from_file_location("brand", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    raise ImportError("templates/ci/brand.py not found — fill in the CI base first.")


brand = _load_brand()

PRIMARY, SECONDARY = brand.PRIMARY, brand.SECONDARY
DARK, NEAR_BLACK = brand.DARK, brand.NEAR_BLACK
LIGHT_GRAY, WHITE = brand.LIGHT_GRAY, brand.WHITE
SUCCESS, WARNING, DANGER = brand.SUCCESS, brand.WARNING, brand.DANGER
_KPI_COLORS = {"good": SUCCESS, "warning": WARNING, "critical": DANGER, "info": SECONDARY}
# Second cue beyond colour so KPI state survives grayscale / colour-blindness.
_KPI_MARK = {"good": "+", "warning": "!", "critical": "x", "info": "i"}

# Latin-1 substitutes for the typographic chars Helvetica (core font) can't encode.
_LATIN1_FALLBACK = {
    "—": "-", "–": "-", "‘": "'", "’": "'",
    "“": '"', "”": '"', "…": "...", "™": " TM",
    " ": " ", "→": "->", "−": "-",
}

# Common cell() kwargs to advance to the next line (replaces deprecated ln=1).
_NL = {"new_x": XPos.LMARGIN, "new_y": YPos.NEXT}


class CIPDF(FPDF):
    """Brand-compliant A4 PDF. Uses brand fonts if available, else Helvetica."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("format", "A4")
        super().__init__(*args, **kwargs)
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(10, 20, 10)
        self.h_family, self.b_family = self._register_fonts()
        # Brand TTFs are full-Unicode; the Helvetica fallback is Latin-1 only.
        self.unicode_ok = self.h_family != "Helvetica"

    def _register_fonts(self):
        """Try the brand TTFs (uni=True); fall back to Helvetica if missing."""
        try:
            heading, body = brand.FONTS["heading"], brand.FONTS["body"]
            if all(os.path.exists(os.path.join(_REPO_ROOT, p)) or os.path.exists(p)
                   for p in (heading["regular"], heading["bold"], body["regular"])):
                def _p(rel):
                    return rel if os.path.exists(rel) else os.path.join(_REPO_ROOT, rel)
                self.add_font(heading["family"], "", _p(heading["regular"]))
                self.add_font(heading["family"], "B", _p(heading["bold"]))
                if heading.get("italic") and os.path.exists(_p(heading["italic"])):
                    self.add_font(heading["family"], "I", _p(heading["italic"]))
                self.add_font(body["family"], "", _p(body["regular"]))
                self.add_font(body["family"], "B", _p(body["bold"]))
                return heading["family"], body["family"]
        except Exception:
            pass
        return "Helvetica", "Helvetica"

    def _t(self, s) -> str:
        """Pass text through unchanged with brand fonts; transliterate to Latin-1
        when falling back to Helvetica so the build never crashes on Unicode."""
        s = str(s)
        if self.unicode_ok:
            return s
        s = "".join(_LATIN1_FALLBACK.get(ch, ch) for ch in s)
        return s.encode("latin-1", "replace").decode("latin-1")

    # --- structural elements --------------------------------------------------
    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*DARK)
        self.rect(0, 0, self.w, 14, "F")
        self.set_fill_color(*PRIMARY)
        self.rect(0, 14, self.w, 1.2, "F")
        self.set_xy(10, 4)
        self.set_text_color(*WHITE)
        self.set_font(self.h_family, "B", 9)
        self.cell(0, 6, self._t(brand.BRAND_NAME), align="L")

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*DARK)
        self.rect(0, self.h - 14, self.w, 14, "F")
        self.set_text_color(*WHITE)
        self.set_font(self.b_family, "", 7)
        self.set_y(-10)
        self.cell(0, 5, self._t(brand.CONTACT), align="C")
        self.set_y(-10)
        self.cell(0, 5, str(self.page_no()), align="R")

    def cover(self, title: str, client: str, date: str):
        self.add_page()
        self.set_fill_color(*DARK)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_fill_color(*PRIMARY)
        self.rect(0, 90, 60, 3, "F")
        self.set_xy(10, 100)
        self.set_text_color(*WHITE)
        self.set_font(self.h_family, "B", 26)
        self.multi_cell(0, 12, self._t(title))
        self.ln(4)
        self.set_x(10)
        self.set_text_color(*PRIMARY)
        self.set_font(self.h_family, "B", 13)
        self.cell(0, 8, self._t(brand.BRAND_TAGLINE), **_NL)
        self.ln(8)
        self.set_x(10)
        self.set_text_color(*WHITE)
        self.set_font(self.b_family, "", 12)
        self.cell(0, 7, self._t(f"Prepared for: {client}"), **_NL)
        self.set_x(10)
        self.cell(0, 7, self._t(date), **_NL)

    def section(self, title: str):
        self.ln(4)
        if self.get_y() > self.h - 40:
            self.add_page()
        self.set_fill_color(*PRIMARY)
        self.rect(self.get_x(), self.get_y() + 1, 3, 7, "F")
        self.set_x(self.get_x() + 6)
        self.set_text_color(*NEAR_BLACK)
        self.set_font(self.h_family, "B", 14)
        self.cell(0, 9, self._t(title), **_NL)
        self.ln(1)

    def body(self, text: str):
        self.set_text_color(*NEAR_BLACK)
        self.set_font(self.b_family, "", 11)
        self.multi_cell(0, 6, self._t(text))
        self.ln(2)

    def bullets(self, items):
        self.set_text_color(*NEAR_BLACK)
        self.set_font(self.b_family, "", 11)
        for it in items:
            self.set_x(12)
            self.cell(5, 6, self._t(chr(149)))  # bullet
            self.multi_cell(0, 6, self._t(it))
        self.ln(2)

    def kpi_box(self, label: str, value: str, state: str = "info"):
        """A colour-coded KPI/ROI box with a non-colour cue (good/warning/critical/info)."""
        color = _KPI_COLORS.get(state, SECONDARY)
        x, y, w, h = self.get_x(), self.get_y(), 60, 18
        if y > self.h - 30:
            self.add_page()
            x, y = self.get_x(), self.get_y()
        self.set_fill_color(*LIGHT_GRAY)
        self.rect(x, y, w, h, "F")
        self.set_fill_color(*color)
        self.rect(x, y, 3, h, "F")
        self.set_xy(x + 6, y + 2)
        self.set_text_color(*color)
        self.set_font(self.h_family, "B", 14)
        self.cell(w - 8, 8, self._t(f"{_KPI_MARK.get(state, '')} {value}".strip()))
        self.set_xy(x + 6, y + 11)
        self.set_text_color(*NEAR_BLACK)
        self.set_font(self.b_family, "", 8)
        self.cell(w - 8, 5, self._t(label))
        self.set_xy(x, y + h + 2)

    def table(self, headers, rows, widths=None, wide_threshold=42):
        """Header row + zebra body. Cells longer than `wide_threshold` chars wrap
        via multi_cell so wide content stays readable instead of overflowing."""
        avail = self.w - 20
        if widths:
            total = sum(widths)
            col_w = [w / total * avail for w in widths]
        else:
            col_w = [avail / len(headers)] * len(headers)

        self.set_font(self.h_family, "B", 10)
        self.set_fill_color(*PRIMARY)
        self.set_text_color(*WHITE)
        for w, head in zip(col_w, headers):
            self.cell(w, 8, self._t(head), border=0, align="C", fill=True)
        self.ln()

        self.set_text_color(*NEAR_BLACK)
        self.set_font(self.b_family, "", 10)
        for i, row in enumerate(rows):
            fill = LIGHT_GRAY if i % 2 else WHITE
            needs_wrap = any(len(str(c)) > wide_threshold for c in row)
            self.set_fill_color(*fill)
            if not needs_wrap:
                for w, cell in zip(col_w, row):
                    self.cell(w, 7, self._t(cell), border=0, align="C", fill=True)
                self.ln()
            else:
                x0, y0 = self.get_x(), self.get_y()
                line_h = 5
                heights = []
                for w, cell in zip(col_w, row):
                    lines = self.multi_cell(w, line_h, self._t(cell), split_only=True)
                    heights.append(max(1, len(lines)) * line_h)
                rh = max(heights)
                if y0 + rh > self.h - 18:
                    self.add_page()
                    x0, y0 = self.get_x(), self.get_y()
                x = x0
                for w, cell in zip(col_w, row):
                    self.set_xy(x, y0)
                    self.set_fill_color(*fill)
                    self.multi_cell(w, line_h, self._t(cell), border=0, align="L", fill=True)
                    x += w
                self.set_xy(x0, y0 + rh)
        self.ln(2)


def _demo():
    pdf = CIPDF()
    pdf.cover("SEO Strategy & Offer", "Example Client GmbH", "2026-06-13")
    pdf.add_page()
    pdf.section("1. Executive Summary")
    pdf.body("Demo of the reusable CIPDF class. Real documents replace this with "
             "the Status-Quo, Potential and Offer content. Accents render: ä ö ü ß é ñ — ® ™ ©.")
    pdf.section("2. Potential (12 months)")
    pdf.table(
        ["Cluster", "Current clicks", "Target clicks", "Delta"],
        [["Brand", "1,200", "1,500", "+300"],
         ["Generic / commercial", "800", "3,400", "+2,600"],
         ["Informational", "300", "1,100", "+800"]],
        widths=[3, 2, 2, 1.5],
    )
    pdf.kpi_box("ROI (realistic)", "233 %", "good")
    out = "ci_pdf_demo.pdf"
    pdf.output(out)
    print(f"Wrote {out} (fonts: {pdf.h_family}/{pdf.b_family}, unicode={pdf.unicode_ok})")


if __name__ == "__main__":
    _demo()
