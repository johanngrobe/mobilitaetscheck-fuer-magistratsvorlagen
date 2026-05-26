import datetime
import re
from io import BytesIO
from os import path

from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.services.pdf.base_pdf import BasePDF
from app.utils.pdf_util import calculate_average_impact, get_display_impact

# Colour palette – mirrors Tailwind classes used in the Vue UI
BLUE_500 = (59, 130, 246)
BLUE_600 = (37, 99, 235)
BLUE_700 = (29, 78, 216)
BLUE_100 = (219, 234, 254)
GRAY_100 = (243, 244, 246)
GRAY_200 = (229, 231, 235)
GRAY_500 = (107, 114, 128)
GRAY_700 = (55, 65, 81)
GRAY_900 = (17, 24, 39)
WHITE = (255, 255, 255)
RED_600 = (220, 38, 38)

# All eight impact levels with their PDF-display colors
LEGEND_ITEMS = [
    ("stark negativ", {"r": 255, "g": 16, "b": 16}),
    ("negativ", {"r": 255, "g": 95, "b": 95}),
    ("leicht negativ", {"r": 255, "g": 175, "b": 175}),
    ("neutral", {"r": GRAY_200[0], "g": GRAY_200[1], "b": GRAY_200[2]}),
    ("leicht positiv", {"r": 176, "g": 222, "b": 171}),
    ("positiv", {"r": 97, "g": 189, "b": 88}),
    ("stark positiv", {"r": 18, "g": 157, "b": 5}),
    ("nicht tangiert", {"r": WHITE[0], "g": WHITE[1], "b": WHITE[2]}),
]


def _luminance(r: int, g: int, b: int) -> float:
    return 0.299 * r + 0.587 * g + 0.114 * b


def _pdf_di(di: dict) -> dict:
    """PDF colour overrides: neutral → gray, nicht tangiert → white."""
    if di["label"] == "neutral":
        return {**di, "color": {"r": GRAY_200[0], "g": GRAY_200[1], "b": GRAY_200[2]}}
    if di["label"] == "Ziel nicht tangiert":
        return {**di, "color": {"r": WHITE[0], "g": WHITE[1], "b": WHITE[2]}}
    return di


class MobilitaetscheckPDF(BasePDF):

    # ── page chrome ──────────────────────────────────────────────────

    def header(self):
        script_dir = path.dirname(path.abspath(__file__))
        image_path = path.normpath(path.join(script_dir, "./assests/pimoo-logo.png"))
        try:
            self.image(image_path, 10, 8, 30)
        except Exception as e:
            print(e)
        self.set_font("free-sans", "", 9)
        self.set_xy(self.l_margin, 8)
        if getattr(self, "is_politik_autor", False):
            self.set_text_color(*RED_600)
            self.set_font("free-sans", "B", 9)
            self.cell(0, 8, "Nicht von Verwaltung", align="C")
            self.set_font("free-sans", "", 9)
            self.set_xy(self.l_margin, 8)
        self.set_text_color(*GRAY_500)
        self.cell(0, 8, datetime.date.today().strftime("%d.%m.%Y"), align="R")
        self.set_text_color(*GRAY_900)
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_text_color(*GRAY_500)
        self.set_font("free-sans", "", 8)
        self.cell(0, 8, f"Seite {self.page_no()}/{{nb}}", align="C")
        self.set_text_color(*GRAY_900)

    # ── helpers ───────────────────────────────────────────────────────

    def _label(self, x: float, text: str, w: float = 0):
        """Small bold uppercase blue label. w>0 → stays on same line."""
        self.set_x(x)
        self.set_text_color(*BLUE_700)
        self.set_font("free-sans", "B", 7)
        if w:
            self.cell(w, 4, text.upper())
        else:
            self.cell(0, 4, text.upper(), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*GRAY_900)

    def _force_stroke_state(self, color: tuple, lw: float):
        """Write draw color and line width directly to the current page stream.

        set_draw_color / set_line_width both deduplicate against global state, so
        they silently skip emission when self.page is switched directly (not via
        add_page).  This method bypasses that by calling _out unconditionally.
        """
        r, g, b = color
        self._out(f"{r / 255:.4f} {g / 255:.4f} {b / 255:.4f} RG")
        self._out(f"{lw * self.k:.2f} w")
        # Invalidate cached state so the next normal set_draw_color / set_line_width
        # call will also emit (prevents deduplication on the restored page).
        self.draw_color = None
        self.line_width = -1.0

    def _h_divider(self, x: float, w: float):
        self.set_draw_color(*GRAY_200)
        self.set_line_width(0.2)
        self.line(x, self.get_y(), x + w, self.get_y())

    def _pill(self, x: float, y: float, w: float, h: float, di: dict):
        """Coloured rounded pill with _pdf_di colour overrides applied."""
        di = _pdf_di(di)
        c = di["color"]
        r, g, b = c["r"], c["g"], c["b"]
        self.set_fill_color(r, g, b)
        if _luminance(r, g, b) > 200:
            self.set_draw_color(*GRAY_200)
            self.set_line_width(0.2)
            self.rect(x, y, w, h, style="FD", corner_radius=h / 2)
        else:
            self.set_draw_color(r, g, b)
            self.rect(x, y, w, h, style="F", corner_radius=h / 2)
        tc = GRAY_900 if _luminance(r, g, b) > 180 else WHITE
        self.set_text_color(*tc)
        self.set_font("free-sans", "B", 7)
        self.set_xy(x, y)
        self.cell(w, h, di["label"], align="C")
        self.set_text_color(*GRAY_900)

    def _write_html_block(self, html: str, x: float, w: float, font_size: float = 9):
        """Render HTML content (from Quill editor) within a constrained column."""
        if not html:
            return
        plain = re.sub(r"<[^>]+>", "", html).strip()
        if not plain:
            return
        old_lm = self.l_margin
        old_rm = self.r_margin
        self.set_left_margin(x)
        self.set_right_margin(self.w - x - w)
        self.set_x(x)
        self.set_font("free-sans", "", font_size)
        self.set_text_color(*GRAY_700)
        self.write_html(html)
        self.set_left_margin(old_lm)
        self.set_right_margin(old_rm)
        self.set_x(old_lm)
        self.set_text_color(*GRAY_900)

    def _legend(self, x: float, y: float):
        """Full 8-item legend strip with automatic line wrapping."""
        ph = 5
        max_x = self.l_margin + self.epw

        # "Legende:" prefix
        self.set_font("free-sans", "", 7)
        self.set_text_color(*GRAY_500)
        lbl = "Legende: "
        lw = self.get_string_width(lbl) + 1
        self.set_xy(x, y)
        self.cell(lw, ph, lbl)
        px = x + lw
        py = y

        self.set_font("free-sans", "B", 7)
        for label, col in LEGEND_ITEMS:
            tw = self.get_string_width(label) + 4
            if px + tw > max_x and px > x + lw:
                px = x + lw
                py += ph + 2
            r, g, b = col["r"], col["g"], col["b"]
            self.set_fill_color(r, g, b)
            if _luminance(r, g, b) > 200:
                self.set_draw_color(*GRAY_200)
                self.set_line_width(0.2)
                self.rect(px, py, tw, ph, style="FD", corner_radius=ph / 2)
            else:
                self.set_draw_color(r, g, b)
                self.rect(px, py, tw, ph, style="F", corner_radius=ph / 2)
            tc = GRAY_900 if _luminance(r, g, b) > 180 else WHITE
            self.set_text_color(*tc)
            self.set_xy(px, py)
            self.cell(tw, ph, label, align="C")
            self.set_text_color(*GRAY_900)
            px += tw + 2

        self.set_y(py + ph)

    # ── export ────────────────────────────────────────────────────────

    def export(self, eingabe: MobilitaetscheckEingabe):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        self.is_politik_autor = bool(
            eingabe.autor
            and getattr(eingabe.autor, "rolle", None)
            and eingabe.autor.rolle.name == "Politik"
        )
        self.add_page()
        self.set_text_color(*GRAY_900)
        cx, cw = self.l_margin, self.epw

        # ── title ─────────────────────────────────────────────────────
        self.set_font("free-sans", "B", 17)
        self.cell(
            0,
            10,
            "Mobilitätscheck für Magistratsvorlagen",
            align="C",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")

        # ── meta card ─────────────────────────────────────────────────
        pad = 4
        card_top = self.get_y()
        col_w = (cw - 2 * pad) / 2

        self.set_xy(cx + pad, card_top + pad)
        self.set_text_color(*BLUE_700)
        self.set_font("free-sans", "B", 7)
        self.cell(col_w, 4, "MAGISTRATSVORLAGENNUMMER")
        if eingabe.magistratsvorlage.verwaltungsvorgang_datum:
            self.cell(
                col_w, 4, "DATUM DER MAGISTRATSSITZUNG", new_x="LMARGIN", new_y="NEXT"
            )
        else:
            self.cell(0, 4, new_x="LMARGIN", new_y="NEXT")

        self.set_xy(cx + pad, self.get_y())
        self.set_text_color(*GRAY_900)
        self.set_font("free-sans", "B", 10)
        self.cell(col_w, 5, str(eingabe.magistratsvorlage.verwaltungsvorgang_nr))
        if eingabe.magistratsvorlage.verwaltungsvorgang_datum:
            self.cell(
                col_w,
                5,
                eingabe.magistratsvorlage.verwaltungsvorgang_datum.strftime("%d.%m.%Y"),
                new_x="LMARGIN",
                new_y="NEXT",
            )
        else:
            self.cell(0, 5, new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

        # Titel der Magistratsvorlage
        self._h_divider(cx + pad, cw - 2 * pad)
        self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
        self._label(cx + pad, "Titel der Magistratsvorlage")
        self.set_x(cx + pad)
        self.set_font("free-sans", "", 10)
        self.multi_cell(
            cw - 2 * pad, 5, str(eingabe.magistratsvorlage.name), new_x="LMARGIN", new_y="NEXT"
        )
        self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

        # Beschreibung der Magistratsvorlage (optional, HTML)
        if eingabe.magistratsvorlage.beschreibung:
            self._h_divider(cx + pad, cw - 2 * pad)
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
            self._label(cx + pad, "Beschreibung der Magistratsvorlage")
            self._write_html_block(
                eingabe.magistratsvorlage.beschreibung, cx + pad, cw - 2 * pad, font_size=9
            )
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

        # Name des Mobilitätschecks
        self._h_divider(cx + pad, cw - 2 * pad)
        self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
        self._label(cx + pad, "Name des Mobilitätschecks")
        self.set_x(cx + pad)
        self.set_font("free-sans", "", 10)
        self.multi_cell(
            cw - 2 * pad, 5, str(eingabe.name), new_x="LMARGIN", new_y="NEXT"
        )
        self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

        # Sachbearbeitung / Ersteller:in
        if eingabe.autor and self.is_politik_autor:
            self._h_divider(cx + pad, cw - 2 * pad)
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
            self._label(cx + pad, "Ersteller:in")
            autor_name = f"{eingabe.autor.vorname} {eingabe.autor.nachname}".strip()
            if eingabe.autor.gruppe:
                autor_name += f" ({eingabe.autor.gruppe.name})"
            self.set_x(cx + pad)
            self.set_font("free-sans", "", 10)
            self.cell(cw - 2 * pad, 5, autor_name, new_x="LMARGIN", new_y="NEXT")
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
        elif eingabe.autor and eingabe.autor.gruppe:
            self._h_divider(cx + pad, cw - 2 * pad)
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")
            self._label(cx + pad, "Sachbearbeitung")
            self.set_x(cx + pad)
            self.set_font("free-sans", "", 10)
            self.cell(
                cw - 2 * pad,
                5,
                eingabe.autor.gruppe.name,
                new_x="LMARGIN",
                new_y="NEXT",
            )
            self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

        meta_card_h = self.get_y() - card_top + pad
        self.set_draw_color(*GRAY_200)
        self.set_line_width(0.3)
        self.rect(cx, card_top, cw, meta_card_h, corner_radius=3)
        self.set_y(card_top + meta_card_h + 5)

        # ── Zielampel ─────────────────────────────────────────────────
        durchschnitt = calculate_average_impact(eingabe)

        self.set_font("free-sans", "B", 11)
        self.cell(
            0, 7, "Zielampel laut verkehrlichem Leitbild", new_x="LMARGIN", new_y="NEXT"
        )
        self.cell(0, 1, new_x="LMARGIN", new_y="NEXT")

        for oberziel in eingabe.eingabe_ziel_ober:
            di = _pdf_di(
                get_display_impact(
                    durchschnitt[oberziel.ziel_ober_id], oberziel.tangiert
                )
            )
            row_y, row_h = self.get_y(), 7
            c = di["color"]
            r, g, b = c["r"], c["g"], c["b"]
            self.set_fill_color(r, g, b)
            if _luminance(r, g, b) > 200:
                self.set_draw_color(*GRAY_200)
                self.set_line_width(0.2)
                self.rect(cx, row_y, cw, row_h, style="FD", corner_radius=3)
            else:
                self.set_draw_color(r, g, b)
                self.rect(cx, row_y, cw, row_h, style="F", corner_radius=3)
            tc = GRAY_900 if _luminance(r, g, b) > 180 else WHITE
            self.set_text_color(*tc)
            self.set_font("free-sans", "", 9)
            self.set_xy(cx + 4, row_y)
            self.cell(
                cw - 8, row_h, f"{oberziel.ziel_ober.nr}. {oberziel.ziel_ober.name}"
            )
            self.set_text_color(*GRAY_900)
            self.ln(row_h + 1)

        # full 8-item legend
        self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")
        self._legend(cx, self.get_y())
        self.cell(0, 5, new_x="LMARGIN", new_y="NEXT")

        # ── Detailbewertung ───────────────────────────────────────────
        self.add_page()
        self.set_font("free-sans", "B", 12)
        self.cell(0, 7, "Detailbewertung", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")

        pill_w = 42

        for oberziel in eingabe.eingabe_ziel_ober:
            tangiert = oberziel.tangiert
            di = _pdf_di(
                get_display_impact(durchschnitt[oberziel.ziel_ober_id], tangiert)
            )

            # header colours: background = Gesamtwirkung colour
            if tangiert:
                hc = di["color"]
                hdr_bg = (hc["r"], hc["g"], hc["b"])
                lum_hdr = _luminance(*hdr_bg)
                title_tc = GRAY_900 if lum_hdr > 180 else WHITE
                badge_bg = GRAY_200 if lum_hdr > 180 else WHITE
                badge_tc = GRAY_900 if lum_hdr > 180 else hdr_bg
            else:
                hdr_bg = GRAY_100
                title_tc = GRAY_700
                badge_bg = BLUE_100
                badge_tc = BLUE_700

            # dynamic header height for long names
            bsz = 6
            name_x_off = 3 + bsz + 2
            name_w_hdr = cw - name_x_off - pill_w - 6
            self.set_font("free-sans", "B", 9)
            nw = self.get_string_width(oberziel.ziel_ober.name)
            name_lines = max(1, int(nw / name_w_hdr) + 1 if nw > name_w_hdr else 1)
            header_h = max(10, name_lines * 5 + 4)

            # pre-emptive page break so header + first line of content start together
            if self.get_y() + header_h + 18 > self.h - self.b_margin:
                self.add_page()

            card_start_page = self.page_no()
            card_top = self.get_y()

            # ── header bar ──────────────────────────────────────────
            # Rounded top corners only: draw full rounded rect then square off the bottom
            self.set_fill_color(*hdr_bg)
            self.set_draw_color(*hdr_bg)
            self.rect(cx, card_top, cw, header_h, style="F", corner_radius=3)
            self.rect(cx, card_top + 3, cw, header_h - 3, style="F")

            # circle number badge
            bx = cx + 3
            by = card_top + (header_h - bsz) / 2
            self.set_fill_color(*badge_bg)
            self.set_draw_color(*badge_bg)
            self.rect(bx, by, bsz, bsz, style="F", corner_radius=bsz / 2)
            self.set_text_color(*badge_tc)
            self.set_font("free-sans", "B", 7)
            self.set_xy(bx, by)
            self.cell(bsz, bsz, str(oberziel.ziel_ober.nr), align="C")

            # oberziel name
            self.set_text_color(*title_tc)
            self.set_font("free-sans", "B", 9)
            name_top = card_top + (header_h - name_lines * 5) / 2
            self.set_xy(cx + name_x_off, name_top)
            self.multi_cell(
                name_w_hdr, 5, oberziel.ziel_ober.name, new_x="RIGHT", new_y="TOP"
            )

            # Gesamtwirkung pill – inverted (white) on any coloured header
            ph = 6
            pill_x = cx + cw - pill_w - 3
            pill_y = card_top + (header_h - ph) / 2
            if tangiert and _luminance(*hdr_bg) <= 200:
                self.set_fill_color(*WHITE)
                self.set_draw_color(*WHITE)
                self.rect(pill_x, pill_y, pill_w, ph, style="F", corner_radius=ph / 2)
                self.set_text_color(*hdr_bg)
                self.set_font("free-sans", "B", 7)
                self.set_xy(pill_x, pill_y)
                self.cell(pill_w, ph, di["label"], align="C")
                self.set_text_color(*GRAY_900)
            else:
                self._pill(pill_x, pill_y, pill_w, ph, di)

            self.set_y(card_top + header_h)

            # ── tangierte Unterziele ──────────────────────────────────
            for unterziel in oberziel.eingabe_ziel_unter:
                if not unterziel.tangiert:
                    continue

                uz_di = _pdf_di(
                    get_display_impact(unterziel.auswirkung, unterziel.tangiert)
                )

                # pre-emptive page break before unterziel (rough min height: 30mm)
                if self.get_y() + 30 > self.h - self.b_margin:
                    self.add_page()

                uz_start_page = self.page_no()
                uz_start_y = self.get_y()
                ind_x = cx + 7  # content, clear of accent line at cx

                # thin gray row divider
                self._h_divider(cx, cw)
                row_y = uz_start_y + 3

                # sub-number (blue)
                nr_text = f"{oberziel.ziel_ober.nr}.{unterziel.ziel_unter.nr}"
                nr_w = 13
                self.set_text_color(*BLUE_600)
                self.set_font("free-sans", "B", 8)
                self.set_xy(ind_x, row_y)
                self.cell(nr_w, 5, nr_text)

                # name – full available width (no impact pill in this row)
                name_w2 = cw - (ind_x - cx) - nr_w - 3
                self.set_text_color(*GRAY_900)
                self.set_font("free-sans", "", 9)
                self.set_xy(ind_x + nr_w, row_y)
                self.multi_cell(
                    name_w2, 5, unterziel.ziel_unter.name, new_x="LMARGIN", new_y="NEXT"
                )
                self.set_y(max(self.get_y(), row_y + 5) + 3)

                # detail row: [impact pill]  |  [RÄUMLICHE AUSWIRKUNG / value]
                detail_x = ind_x + nr_w
                half_w = (cw - (detail_x - cx) - 3) / 2

                # only label the right column
                self._label(detail_x, "Wirkungsrichtung und -stärke", w=-1)
                self._label(detail_x + half_w, "Räumliche Auswirkung")

                val_y = self.get_y()
                wir_pw, wir_ph = 38, 5
                self._pill(detail_x, val_y, wir_pw, wir_ph, uz_di)

                raeumlich = getattr(unterziel.auswirkung_raeumlich, "name", None) or "–"
                self.set_font("free-sans", "", 9)
                self.set_xy(detail_x + half_w, val_y)
                self.cell(half_w, wir_ph, raeumlich)
                self.set_y(val_y + wir_ph + 3)

                # Erläuterung
                content_w = cw - (detail_x - cx) - 3
                if unterziel.anmerkung:
                    self._label(detail_x, "Erläuterung")
                    self._write_html_block(unterziel.anmerkung, detail_x, content_w, font_size=9)
                    self.cell(0, 2, new_x="LMARGIN", new_y="NEXT")

                # Indikatoren
                if unterziel.indikatoren:
                    self._label(detail_x, "Indikatoren")
                    ind_ph = 5
                    ind_px = detail_x
                    ind_py = self.get_y()
                    max_px = cx + cw - 3
                    self.set_font("free-sans", "", 8)
                    for ind in unterziel.indikatoren:
                        tw = self.get_string_width(ind.name) + 6
                        if ind_px + tw > max_px and ind_px > detail_x:
                            ind_px = detail_x
                            ind_py += ind_ph + 2
                        self.set_fill_color(*BLUE_600)
                        self.set_draw_color(*BLUE_600)
                        self.rect(
                            ind_px,
                            ind_py,
                            tw,
                            ind_ph,
                            style="F",
                            corner_radius=ind_ph / 2,
                        )
                        self.set_text_color(*WHITE)
                        self.set_font("free-sans", "", 8)
                        self.set_xy(ind_px, ind_py)
                        quelle = getattr(ind, "quelle_url", None)
                        if quelle:
                            self.cell(tw, ind_ph, ind.name, link=quelle, align="C")
                        else:
                            self.cell(tw, ind_ph, ind.name, align="C")
                        self.set_text_color(*GRAY_900)
                        ind_px += tw + 2
                    self.set_y(ind_py + ind_ph + 3)

                self.cell(0, 3, new_x="LMARGIN", new_y="NEXT")

            # simple card border – uncolored, works across page breaks
            end_page = self.page_no()
            end_y = self.get_y()
            content_top = self.t_margin + 18  # below header on continuation pages

            if end_page == card_start_page:
                card_h = end_y - card_top
                if card_h > 0:
                    self.set_draw_color(*GRAY_200)
                    self.set_line_width(0.3)
                    self.rect(cx, card_top, cw, card_h, corner_radius=3)
            else:
                # Card spans pages: draw each page segment using self.page
                saved_page = self.page

                # Start page: top + left + right down to page bottom (open bottom)
                self.page = card_start_page
                self._force_stroke_state(GRAY_200, 0.3)
                page_bot = self.h - self.b_margin
                self.line(cx, card_top, cx + cw, card_top)
                self.line(cx, card_top, cx, page_bot)
                self.line(cx + cw, card_top, cx + cw, page_bot)

                # Intermediate pages: left + right full content height
                for _p in range(card_start_page + 1, end_page):
                    self.page = _p
                    self._force_stroke_state(GRAY_200, 0.3)
                    self.line(cx, content_top, cx, self.h - self.b_margin)
                    self.line(cx + cw, content_top, cx + cw, self.h - self.b_margin)

                # End page: left + right + bottom (open top)
                self.page = saved_page
                self._force_stroke_state(GRAY_200, 0.3)
                self.line(cx, content_top, cx, end_y)
                self.line(cx + cw, content_top, cx + cw, end_y)
                self.line(cx, end_y, cx + cw, end_y)

            self.cell(0, 4, new_x="LMARGIN", new_y="NEXT")

        pdf_output = BytesIO()
        self.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output
