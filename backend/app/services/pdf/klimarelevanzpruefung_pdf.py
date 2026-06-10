from io import BytesIO

from app.models.klimarelevanzpruefung_eingabe import KlimarelevanzpruefungEingabe
from app.services.pdf.base_pdf import BasePDF


class KlimarelevanzpruefungPDF(BasePDF):

    FOOTNOTES = {
        1: "Zum Vergleich: eine 80 Jahre alte Buche mit 33 cm Durchmesser und 20 m Höhe speichert ca. eine Tonne CO2. Quelle: Bayerische Landesanstalt für Wald und Forstwirtschaft (LWF) https://www.lwf.bayern.de/mam/cms04/service/dateien/mb27_kohlenstoff_2023_rz_web_bf.pdf",
        2: 'Die Energetische Sanierung von Altbauten verursachen unter Einbeziehung der Nutzungsphase (50 Jahre) etwa 50 Prozent des CO2-Fußabdrucks eines Neubaus. Quelle: Senger et al. 2022 "Energetische Sanierung von Bestandsgebäuden oder Neubau: ökologische Bewertung hinsichtlich Materialbedarf, Primärenergieverbrauch und damit verbundenen Treibhausgas-Emissionen", Wuppertal Institut für Klima, Umwelt, Energie',
        3: "Bei der Anschaffung von Maschinen und Materialien fallen bei allen Ausführungen Treibhausgasemissionen in der Produktionskette und im Transport an. Für den Betrieb darüber hinaus Energie in Form von Strom, Treibstoff oder durch die Verarbeitung. Auch weitere ökologische Faktoren wie z.B. Wasserverbrauch oder umweltschädliche Stoffe in der Produktion können anfallen, wirken sich allerdings nicht direkt auf die Treibhausgasbilanz oder die Klimaanpassung hier vor Ort aus.",
        4: "Eingriffe in den Boden können im Regelfall nicht am gleichen Schutzgut in gleicher Wertigkeit ausgeglichen werden, da die allgemeine Flächenknappheit zu einer zunehmenden Versiegelung führt.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.used_footnotes = set()
        self.page_footnotes = {}  # Maps page number to set of footnote numbers
        self.rendered_footnotes = set()  # Track which footnotes have been rendered

    def _add_footnote_to_page(self, footnote_num: int):
        """Register a footnote for the current page"""
        page = self.page_no()
        if page not in self.page_footnotes:
            self.page_footnotes[page] = set()
        self.page_footnotes[page].add(footnote_num)
        self.used_footnotes.add(footnote_num)

    def _get_footnotes_height(self, footnote_nums: set) -> float:
        """Calculate height needed for given footnotes"""
        if not footnote_nums:
            return 0
        height = 8  # Divider line + padding
        content_width = self.w - 20
        self.set_font("free-sans", "", 7)
        superscripts = {1: "¹", 2: "²", 3: "³", 4: "⁴"}
        for num in sorted(footnote_nums):
            if num in self.FOOTNOTES and num not in self.rendered_footnotes:
                marker = superscripts.get(num, str(num))
                text = f"{marker} {self.FOOTNOTES[num]}"
                lines = self.multi_cell(
                    content_width, 3.5, text, border=0, split_only=True
                )
                height += len(lines) * 3.5 + 2
        return height

    def footer(self):
        # Get footnotes for current page that haven't been rendered yet
        page = self.page_no()
        page_notes = self.page_footnotes.get(page, set())
        new_notes = page_notes - self.rendered_footnotes

        if new_notes:
            # Calculate space needed
            footnote_height = self._get_footnotes_height(new_notes)
            footer_y = -(footnote_height + 12)  # Extra space for page number
            self.set_y(footer_y)

            # Draw subtle divider line
            content_width = self.w - 20
            self.set_draw_color(180, 180, 180)
            self.set_line_width(0.3)
            line_width = content_width * 0.3
            self.line(
                self.l_margin, self.get_y(), self.l_margin + line_width, self.get_y()
            )
            self.ln(3)

            # Render footnotes
            self.set_font("free-sans", "", 7)
            superscripts = {1: "¹", 2: "²", 3: "³", 4: "⁴"}
            for footnote_num in sorted(new_notes):
                if footnote_num in self.FOOTNOTES:
                    marker = superscripts.get(footnote_num, str(footnote_num))
                    text = f"{marker} {self.FOOTNOTES[footnote_num]}"
                    self.multi_cell(
                        content_width,
                        3.5,
                        text,
                        border=0,
                        new_x="LMARGIN",
                        new_y="NEXT",
                    )
                    self.ln(1)
                    self.rendered_footnotes.add(footnote_num)

        # Page number at the very bottom
        self.set_y(-10)
        self.set_font("free-sans", "", 8)
        self.cell(0, 10, f"Seite {self.page_no()}/{{nb}}", align="C")

    NUM_COL_WIDTH = 10
    CHECK_COL_WIDTH = 15
    RULE_INSET = 1.5  # mm gap on each side of a column boundary (midrule only)

    @staticmethod
    def _fmt_num(value) -> str:
        """Format a number with comma as decimal separator and no trailing zeros."""
        if value is None:
            return "?"
        formatted = f"{float(value):g}"
        return formatted.replace(".", ",")

    def _get_text_col_width(self):
        return self.w - 20 - self.NUM_COL_WIDTH - 2 * self.CHECK_COL_WIDTH

    def _col_x(self):
        """Return the five x-positions that bound the four columns."""
        x0 = self.l_margin
        x1 = x0 + self.NUM_COL_WIDTH
        x2 = x1 + self._get_text_col_width()
        x3 = x2 + self.CHECK_COL_WIDTH
        x4 = x3 + self.CHECK_COL_WIDTH
        return x0, x1, x2, x3, x4

    def _draw_h_rule(self, y: float, line_width: float = 0.3):
        """Solid full-width horizontal rule."""
        x0, x1, x2, x3, x4 = self._col_x()
        self.set_line_width(line_width)
        self.set_draw_color(0, 0, 0)
        self.line(x0, y, x4, y)

    def _draw_h_rule_gapped(self, y: float, line_width: float = 0.3):
        """Segmented rule with a small gap at each column boundary."""
        x0, x1, x2, x3, x4 = self._col_x()
        g = self.RULE_INSET
        self.set_line_width(line_width)
        self.set_draw_color(0, 0, 0)
        self.line(x0, y, x1 - g, y)
        self.line(x1 + g, y, x2 - g, y)
        self.line(x2 + g, y, x3 - g, y)
        self.line(x3 + g, y, x4, y)

    def _add_table_header(self):
        """Booktabs-style header: thick toprule, text, partial midrule, Pos./Neg., midrule."""
        self.set_font("free-sans", "B", 9)
        row1_h = 6
        row2_h = 6
        total_h = row1_h + row2_h
        x0, x1, x2, x3, x4 = self._col_x()
        y_start = self.get_y()

        # Toprule (thick, solid)
        self._draw_h_rule(y_start, line_width=0.5)

        # Nr. vertically centred across both header rows
        self.set_xy(x0, y_start + (total_h - 5) / 2)
        self.cell(self.NUM_COL_WIDTH, 5, "Nr.", border=0, align="C")

        # "Klimawirkung" over the two check columns

        self.set_xy(x2, y_start)
        self.cell(2 * self.CHECK_COL_WIDTH, row1_h, "Klimawirkung", border=0, align="C")

        # Partial midrule under "Klimawirkung" — solid, spans both check columns
        self.set_line_width(0.2)
        self.set_draw_color(0, 0, 0)
        self.line(x2, y_start + row1_h, x4, y_start + row1_h)

        # Row 2: "Pos." and "Neg."
        self.set_xy(x2, y_start + row1_h)
        self.cell(self.CHECK_COL_WIDTH, row2_h, "Pos.", border=0, align="C")
        self.set_xy(x3, y_start + row1_h)
        self.cell(self.CHECK_COL_WIDTH, row2_h, "Neg.", border=0, align="C")

        # Midrule below header (gapped at column boundaries)
        self._draw_h_rule_gapped(y_start + total_h, line_width=0.3)

        self.set_xy(x0, y_start + total_h)

    def _add_table_row(
        self,
        row_num: int,
        positive_text: str = "",
        negative_text: str = "",
        draw_top_border: bool = False,
        show_number: bool = True,
        fill: bool = False,
    ):
        """Add a row with numbering, combined text, and x-markers for positive/negative impact"""
        # Detect footnote markers in text (don't track yet - wait until we know the page)
        footnote_markers = {"²": 2, "³": 3, "⁴": 4}
        combined_text = positive_text + negative_text
        row_footnotes = set()
        for marker, num in footnote_markers.items():
            if marker in combined_text:
                row_footnotes.add(num)

        text_col_width = self._get_text_col_width()
        row_text = positive_text if positive_text else negative_text
        row_text = (
            row_text.replace(" Begründung: ", "\nBegründung:\x00")
            .replace(" Erläuterung: ", "\nErläuterung:\x00")
            .replace(": ", ":\n")
            .replace(":\x00", ": ")
        )

        # Calculate height needed for row
        self.set_font("free-sans", "", 9)
        text_lines = self.multi_cell(
            text_col_width, 5, row_text, border=0, split_only=True
        )
        row_height = max(len(text_lines), 1) * 5 + 2

        # Calculate space needed for footnotes on current page
        current_page = self.page_no()
        current_footnotes = (
            self.page_footnotes.get(current_page, set()) - self.rendered_footnotes
        )
        potential_footnotes = current_footnotes | row_footnotes
        footnote_space = self._get_footnotes_height(
            potential_footnotes - self.rendered_footnotes
        )

        # Check if we need a new page (row + footnotes must fit)
        bottom_margin = max(
            25, footnote_space + 15
        )  # At least 25mm, or footnotes + page number
        page_break_occurred = False
        page_before_break = None
        y_before_break = None

        if self.get_y() + row_height > self.h - bottom_margin:
            page_before_break = self.page_no()
            y_before_break = self.get_y()
            page_break_occurred = True
            self.add_page()
            self._add_table_header()

        # Now track footnotes for the actual page where this row is rendered
        for num in row_footnotes:
            self._add_footnote_to_page(num)

        y_start = self.get_y()

        # Column positions
        x0, x1, x2, x3, x4 = self._col_x()

        # Background shading for alternating rows (full table width)
        if fill:
            self.set_fill_color(240, 240, 240)
            fill_height = max(len(text_lines), 1) * 5
            self.rect(x1, y_start, x4 - x1, fill_height, style="F")

        # Thin group-separator rule above this row (no vertical lines)
        if draw_top_border:
            self._draw_h_rule(y_start, line_width=0.2)

        # Draw text column
        self.set_font("free-sans", "", 9)
        self.set_xy(x1, y_start)
        self.multi_cell(x2 - x1, 5, row_text, border=0, align="L")
        y_after_text = self.get_y()

        # Calculate actual row height
        actual_height = y_after_text - y_start
        y_end = y_start + actual_height

        # Draw x-marker in appropriate check column
        marker_y = y_start + (actual_height - 5) / 2
        self.set_font("free-sans", "", 9)
        if positive_text:
            self.set_xy(x2, marker_y)
            self.cell(self.CHECK_COL_WIDTH, 5, "x", border=0, align="C")
        elif negative_text:
            self.set_xy(x3, marker_y)
            self.cell(self.CHECK_COL_WIDTH, 5, "x", border=0, align="C")

        # Move to next row
        self.set_y(y_end)

        # Return info for group number positioning and page break status
        return {
            "y_start": y_start,
            "y_end": y_end,
            "row_num": row_num if show_number else None,
            "page_break": page_break_occurred,
            "page_before_break": page_before_break,
            "y_before_break": y_before_break,
        }

    def _draw_group_number_on_page(
        self,
        group_num: int,
        y_start: float,
        y_end: float,
        num_col_width: float,
        page: int,
    ):
        """Draw the group number on a specific page"""
        # Save current state
        current_page = self.page_no()
        current_y = self.get_y()

        # Switch to the target page
        self.page = page

        # Draw the number
        self.set_font("free-sans", "", 9)
        text_height = 5
        group_height = y_end - y_start
        y_centered = y_start + (group_height - text_height) / 2
        self.set_xy(self.l_margin, y_centered)
        self.cell(num_col_width, text_height, str(group_num), border=0, align="C")

        # Restore state
        self.page = current_page
        self.set_y(current_y)

    def _draw_group_number(
        self, group_num: int, y_start: float, y_end: float, num_col_width: float
    ):
        """Draw the group number vertically centered within the group's total height"""
        # Save current position
        current_y = self.get_y()

        self.set_font("free-sans", "", 9)
        text_height = 5
        group_height = y_end - y_start
        y_centered = y_start + (group_height - text_height) / 2
        self.set_xy(self.l_margin, y_centered)
        self.cell(num_col_width, text_height, str(group_num), border=0, align="C")

        # Restore position for next row
        self.set_y(current_y)

    def _collect_all_rows(self, eingabe: KlimarelevanzpruefungEingabe):
        """Collect all rows from all questionnaires with group info"""
        rows = []  # List of (group, positive_text, negative_text)

        # FB1 - Fragebogen A
        fb1 = eingabe.fb1 if eingabe.f1 else None
        if fb1:
            # a1: Maschinen/Materialien
            if fb1.a1q1 == 1 and fb1.a1q2:
                rows.append(
                    (
                        "a1",
                        "",
                        f"Im Rahmen des Vorhabens wird/werden {fb1.a1q2} angeschafft.³",
                    )
                )

            if fb1.a1q3 == 1:
                rows.append(
                    (
                        "a1",
                        f"Bei der Anschaffung wurde auf Nachhaltigkeitskriterien geachtet. Erläuterung: {fb1.a1q4 or ''}",
                        "",
                    )
                )
            elif fb1.a1q3 == 2:
                rows.append(
                    (
                        "a1",
                        "",
                        f"Bei der Auswahl wurde nicht auf Nachhaltigkeitskriterien geachtet. Begründung: {fb1.a1q5 or ''}",
                    )
                )

            # a2: Energetische Aufwertung / Baumaßnahmen
            if fb1.a2q2 in [3, 4]:
                if fb1.a2q3:
                    rows.append(
                        (
                            "a2",
                            "Bei dem Vorhaben wird ein bestehendes Gebäude energetisch aufgewertet.²",
                            "",
                        )
                    )
                    if fb1.a2q4:
                        rows.append(
                            (
                                "a2",
                                f"Dabei wird der Energiestandard {fb1.a2q4_item.name} erreicht. Begründung für den genannten Standard {fb1.a2q5 or ''}",
                                "",
                            )
                        )
            if fb1.a2q2 in [1, 2]:
                if fb1.a2q6 == 6:
                    rows.append(
                        (
                            "a2",
                            "",
                            f"Es wird lediglich der Energiestandard {fb1.a2q6_item.name} erreicht und damit das gesetzliche Mindestmaß erfüllt. Begründung für den genannten Standard: {fb1.a2q7 or ''}²",
                        )
                    )
                elif fb1.a2q6:
                    rows.append(
                        (
                            "a2",
                            f"Es wird der Energiestandard {fb1.a2q6_item.name} erreicht. Es wurde sich für den genannten Standard entschieden, da {fb1.a2q7 or ''}²",
                            "",
                        )
                    )

            if fb1.a2q8 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben wird darauf geachtet, dass Niederschlag möglichst vor Ort versickert.",
                        "",
                    )
                )
            elif fb1.a2q8 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben wird nicht darauf geachtet, dass Niederschlag möglichst vor Ort versickert. Begründung: {fb1.a2q9 or ''}",
                    )
                )

            if fb1.a2q10 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben wird darauf geachtet, dass Kaltluftströme ungehindert fließen können.",
                        "",
                    )
                )
            elif fb1.a2q10 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben wird nicht darauf geachtet, dass Kaltluftströme ungehindert fließen können. Begründung: {fb1.a2q11 or ''}",
                    )
                )

            if fb1.a2q12 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei dem Vorhaben finden Maßnahmen gegen die örtliche Hitzebildung Anwendung.",
                        "",
                    )
                )
            elif fb1.a2q12 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei dem Vorhaben finden keine Maßnahmen gegen die örtliche Hitzebildung Anwendung. Begründung: {fb1.a2q13 or ''}",
                    )
                )

            if fb1.a2q14 == 1:
                rows.append(
                    (
                        "a2",
                        "Bei den Vergabekriterien wurde auf Nachhaltigkeit geachtet.",
                        "",
                    )
                )
            elif fb1.a2q14 == 2:
                rows.append(
                    (
                        "a2",
                        "",
                        f"Bei den Vergabekriterien wurde nicht auf Nachhaltigkeit geachtet. Begründung: {fb1.a2q15 or ''}",
                    )
                )

            # a3: Flächenversiegelung
            if fb1.a3q1 == 1:
                neg_text = f"Bei dem Vorhaben werden Flächen im Umfang von {self._fmt_num(fb1.a3q2)} m² neu versiegelt.⁴"
                if fb1.a3q3:
                    neg_text += f"Bisherige Nutzung der Fläche: {fb1.a3q3}"
                rows.append(("a3", "", neg_text))

                if fb1.a3q4 == 1:
                    rows.append(
                        (
                            "a3",
                            f"Für die Versiegelung sind Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a3q5 or ''}",
                            "",
                        )
                    )
                elif fb1.a3q4 == 2:
                    rows.append(
                        (
                            "a3",
                            "",
                            f"Für die Versiegelung sind keine Ausgleichsmaßnahmen vorgesehen. Begründung: {fb1.a3q6 or ''}",
                        )
                    )

            # a4: Flächenentsiegelung
            if fb1.a4q1 == 1:
                pos_text = f"Bei dem Vorhaben werden Flächen im Umfang von {self._fmt_num(fb1.a4q2)} m² entsiegelt."
                if fb1.a4q3:
                    pos_text += f"Bisherige Nutzung der Fläche: {fb1.a4q3}"
                rows.append(("a4", pos_text, ""))

                if fb1.a4q4 == 1:
                    rows.append(
                        (
                            "a4",
                            "",
                            "Die Entsiegelung ist Teil einer Ausgleichsmaßnahme.",
                        )
                    )

            # a5: Grünflächen
            if fb1.a5q1 == 1:
                pos_text = f"Bei dem Vorhaben werden Grünflächen im Umfang von {fb1.a5q2 or '?'} m² aufgewertet. Erläuterung: {fb1.a5q5 or ''}"
                if fb1.a5q3:
                    pos_text += f"Bisherige Nutzung der Fläche: {fb1.a5q3}"
                rows.append(("a5", pos_text, ""))

                if fb1.a5q4 == 1:
                    rows.append(
                        ("a5", "", "Die Aufwertung ist Teil einer Ausgleichsmaßnahme.")
                    )

            # a6: Begrünung entfernt
            if fb1.a6q1 == 1:
                rows.append(
                    (
                        "a6",
                        "",
                        f"Bei dem Vorhaben wird Begrünung entfernt. Erläuterung: {fb1.a6q2 or ''}",
                    )
                )

                if fb1.a6q3 == 1:
                    rows.append(
                        (
                            "a6",
                            f"Für die Versiegelung sind Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a6q4 or ''}",
                            "",
                        )
                    )
                elif fb1.a6q3 == 2:
                    rows.append(
                        (
                            "a6",
                            "",
                            f"Für die Versiegelung sind keine Ausgleichsmaßnahmen vorgesehen. Erläuterung: {fb1.a6q5 or ''}",
                        )
                    )

            # a7: Klimaschädliche Wirkung
            if fb1.a7q1 == 1:
                rows.append(
                    (
                        "a7",
                        "",
                        f"Das Vorhaben hat folgende klimaschädliche Wirkung: {fb1.a7q2 or ''}",
                    )
                )

            # a8: Klimaschützende Wirkung
            if fb1.a8q1 == 1:
                rows.append(
                    (
                        "a8",
                        f"Das Vorhaben hat folgende klimaschützende / Klimaresilienz fördernde Wirkung: {fb1.a8q2 or ''}",
                        "",
                    )
                )

        # FB2 - Fragebogen B
        fb2 = eingabe.fb2 if eingabe.f2 else None
        if fb2:
            if fb2.b1q1 == 1:
                # b1: B-Plan Festsetzungen
                if fb2.b1q2 == 1:
                    rows.append(
                        ("b1", "Im B-Plan wurde eine PV-Pflicht verankert.", "")
                    )
                elif fb2.b1q2 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine PV-Pflicht verankert. Erläuterung: {fb2.b1q3 or ''}",
                        )
                    )

                if fb2.b1q4 == 1:
                    rows.append(
                        ("b1", "Im B-Plan wurde eine Gründachpflicht verankert.", "")
                    )
                elif fb2.b1q4 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine Gründachpflicht verankert. Erläuterung: {fb2.b1q5 or ''}",
                        )
                    )

                if fb2.b1q6 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurde eine nachhaltige Regenwasserbewirtschaftung verankert. Erläuterung: {fb2.b1q7 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q6 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde keine nachhaltige Regenwasserbewirtschaftung verankert. Erläuterung: {fb2.b1q8 or ''}",
                        )
                    )

                if fb2.b1q9 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden weitere wasserrückhaltende Maßnahmen verankert. Erläuterung: {fb2.b1q10 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q9 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurden keine weiteren wasserrückhaltenden Maßnahmen verankert. Erläuterung: {fb2.b1q11 or ''}",
                        )
                    )

                if fb2.b1q12 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden weitere hitzepräventive Maßnahmen verankert. Erläuterung: {fb2.b1q13 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q12 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurden keine weiteren hitzepräventiven Maßnahmen verankert. Erläuterung: {fb2.b1q14 or ''}",
                        )
                    )

                if fb2.b1q15 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan wurden ein Fokus auf platzsparendes Bauen gelegt und möglichst wenig Fläche versiegelt. Erläuterung: {fb2.b1q16 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q15 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan wurde kein Fokus auf platzsparendes Bauen gelegt. Erläuterung: {fb2.b1q17 or ''}",
                        )
                    )

                if fb2.b1q18 == 1:
                    rows.append(
                        (
                            "b1",
                            f"Im B-Plan werden die Kaltluftschneisen geschützt. Erläuterung: {fb2.b1q19 or ''}",
                            "",
                        )
                    )
                elif fb2.b1q18 == 2:
                    rows.append(
                        (
                            "b1",
                            "",
                            f"Im B-Plan werden die Kaltluftschneisen nicht geschützt. Erläuterung: {fb2.b1q20 or ''}",
                        )
                    )

            # b2: Konzept/Planung
            if fb2.b2q2:
                rows.append(
                    (
                        "b2",
                        f"Durch das Vorhaben können indirekt positive Auswirkungen auf physische Maßnahmen mit Klimawirkung entstehen. Erläuterung: {fb2.b2q2}",
                        "",
                    )
                )
            if fb2.b2q3:
                rows.append(
                    (
                        "b2",
                        "",
                        f"Durch das Vorhaben können indirekt negative Auswirkungen auf physische Maßnahmen mit Klimawirkung entstehen. Erläuterung: {fb2.b2q3}",
                    )
                )
            if fb2.b2q4 == 1 and fb2.b2q5:
                rows.append(
                    (
                        "b2",
                        f"Dabei wurden folgende Nachhaltigkeitskriterien beachtet: {fb2.b2q5}",
                        "",
                    )
                )

        # FB3 - Fragebogen C
        fb3 = eingabe.fb3 if eingabe.f3 else None
        if fb3:
            # c1: Positive Beeinflussung
            if fb3.c1q1 == 1:
                if fb3.c1q2 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird das Konsumverhalten klimapositiv beeinflusst. Erläuterung: {fb3.c1q3 or ''}",
                            "",
                        )
                    )
                if fb3.c1q4 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird die Mobilität klimapositiv beeinflusst. Erläuterung: {fb3.c1q5 or ''}",
                            "",
                        )
                    )
                if fb3.c1q6 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird das Wissen über Klimaschutz oder Klimaanpassung positiv beeinflusst. Erläuterung: {fb3.c1q7 or ''}",
                            "",
                        )
                    )
                if fb3.c1q8 == 1:
                    rows.append(
                        (
                            "c1",
                            f"Durch das Vorhaben wird klimarelevantes Verhalten positiv beeinflusst. Erläuterung: {fb3.c1q9 or ''}",
                            "",
                        )
                    )

            # c2: Negative Beeinflussung
            if fb3.c2q1 == 1:
                if fb3.c2q2 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird das Konsumverhalten klimanegativ beeinflusst. Erläuterung: {fb3.c2q3 or ''}",
                        )
                    )
                if fb3.c2q4 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird die Mobilität klimanegativ beeinflusst. Erläuterung: {fb3.c2q5 or ''}",
                        )
                    )
                if fb3.c2q6 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird das Wissen über Klimaschutz oder Klimaanpassung negativ beeinflusst. Erläuterung: {fb3.c2q7 or ''}",
                        )
                    )
                if fb3.c2q8 == 1:
                    rows.append(
                        (
                            "c2",
                            "",
                            f"Durch das Vorhaben wird klimarelevantes Verhalten negativ beeinflusst. Erläuterung: {fb3.c2q9 or ''}",
                        )
                    )

        # FB4 - Fragebogen D
        fb4 = eingabe.fb4 if eingabe.f4 else None
        if fb4:
            if fb4.d1q1:
                rows.append(
                    (
                        "d1",
                        f"Das Vorhaben hat folgende positive Klimarelevanz: {fb4.d1q1}",
                        "",
                    )
                )

            if fb4.d2q1:
                rows.append(
                    (
                        "d2",
                        "",
                        f"Das Vorhaben hat folgende negative Klimarelevanz: {fb4.d2q1}",
                    )
                )

        return rows

    def _export_fb5(self, f5: bool):
        """Export Fragebogen F (f5) - Keine Klimawirksamkeit"""
        if not f5:
            return

        self.set_font("free-sans", "B", 12)
        self.cell(
            0, 8, "Fragebogen F: Keine Klimawirksamkeit", new_x="LMARGIN", new_y="NEXT"
        )
        self.set_font("free-sans", "", 10)
        self.cell(
            0,
            6,
            "Das Vorhaben ist in keiner Weise klimawirksam.",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(5)

    def export(self, eingabe: KlimarelevanzpruefungEingabe):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=20)
        # Reset footnote tracking for each export
        self.used_footnotes = set()
        self.page_footnotes = {}
        self.rendered_footnotes = set()
        self.add_page()

        # Title
        self.set_font("free-sans", "B", 14)
        self.cell(
            0,
            6,
            f'Klimacheck zur Vorlage „{eingabe.magistratsvorlage.name}"',
            border=False,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_font("free-sans", "", 14)
        self.cell(
            0,
            6,
            f"Vorlagennummer: {eingabe.magistratsvorlage.verwaltungsvorgang_nr}",
            border=False,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(10)

        # Collect all rows and export as single table
        rows = self._collect_all_rows(eingabe)

        if rows:
            self._add_table_header()

            prev_group = None
            group_num = 0
            group_y_start = None
            group_y_end = None
            group_page_start = None

            for i, (group, positive_text, negative_text) in enumerate(rows):
                is_new_group = prev_group != group
                is_last_row = i == len(rows) - 1
                next_group = rows[i + 1][0] if not is_last_row else None
                is_last_in_group = is_last_row or next_group != group

                # Increment group number and reset y tracking when group changes
                if is_new_group:
                    group_num += 1
                    group_y_start = self.get_y()
                    group_page_start = self.page_no()

                draw_top_border = prev_group is not None and prev_group != group
                row_result = self._add_table_row(
                    group_num,
                    positive_text,
                    negative_text,
                    draw_top_border,
                    show_number=False,
                    fill=bool(i % 2),
                )

                # Handle page break within a group - draw number on old page first
                if (
                    row_result["page_break"]
                    and group_page_start == row_result["page_before_break"]
                ):
                    # Draw number for the portion on the old page
                    # Calculate bottom of content area on the old page (before footer)
                    old_page_y_end = row_result["y_before_break"]
                    self._draw_group_number_on_page(
                        group_num,
                        group_y_start,
                        old_page_y_end,
                        self.NUM_COL_WIDTH,
                        row_result["page_before_break"],
                    )
                    # Reset group start for the new page (after table header)
                    group_y_start = row_result["y_start"]
                    group_page_start = self.page_no()

                group_y_end = row_result["y_end"]

                # Draw number when group ends (either last row or next row is different group)
                if is_last_in_group:
                    self._draw_group_number(
                        group_num, group_y_start, group_y_end, self.NUM_COL_WIDTH
                    )

                prev_group = group

            # Draw final bottomrule (thick)
            if group_y_end is not None:
                self._draw_h_rule(group_y_end, line_width=0.5)

        self.ln(5)

        # Export F5 separately (no climate relevance)
        if eingabe.f5:
            self._export_fb5(eingabe.f5)

        # Create a bytes buffer to save the PDF
        pdf_output = BytesIO()
        self.output(pdf_output)

        # Move the buffer pointer to the beginning
        pdf_output.seek(0)

        return pdf_output
