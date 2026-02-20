from odoo import models
import datetime

class CustomVatNumberXlsx(models.AbstractModel):
    _inherit = "report.l10n_es_vat_book.l10n_es_vat_book_xlsx"

    def generate_xlsx_report(self, workbook, data, objects):
        """Modificada para evitar error de comparación entre bool y str."""

        book = objects[0]
        draft_export = bool(book.state not in ["done", "posted"])

        # Issued
        issued_sheet = self.create_issued_sheet(workbook, book, draft_export)
        lines = book.issued_line_ids + book.rectification_issued_line_ids
        # Modificación: asegurarse de que no haya valores None o False
        lines = lines.sorted(key=lambda l: (l.invoice_date or datetime.date.min, l.ref or ''))
        row = 8
        for line in lines:
            with_total = True
            for tax_line in line.tax_line_ids:
                if not tax_line.special_tax_group:
                    self.fill_issued_row_data(
                        issued_sheet, row, line, tax_line, with_total, draft_export
                    )
                    with_total = False
                    row += 1

        # Received
        received_sheet = self.create_received_sheet(workbook, book, draft_export)
        lines = book.received_line_ids + book.rectification_received_line_ids
        # Modificación: asegurarse de que no haya valores None o False
        lines = lines.sorted(key=lambda l: (l.invoice_date or datetime.date.min, l.ref or ''))
        row = 8
        for line in lines:
            with_total = True
            for tax_line in line.tax_line_ids:
                if not tax_line.special_tax_group:
                    self.fill_received_row_data(
                        received_sheet, row, line, tax_line, with_total, draft_export
                    )
                    with_total = False
                    row += 1


    def fill_issued_row_data(
            self, sheet, row, line, tax_line, with_total, draft_export
    ):

        country_code, identifier_type, vat_number = (
                line.partner_id and line.partner_id._parse_aeat_vat_info() or ("ES", "", "")
        )

        sheet.write("A" + str(row), self.format_boe_date(line.invoice_date))

        ref = line.ref or ""
        sheet.write("C" + str(row), ref[:-20])  # Primeros 20 caracteres
        sheet.write("D" + str(row), ref[-20:])  # Últimos 20 caracteres

        sheet.write("E" + str(row), "")  # Número final
        sheet.write("F" + str(row), identifier_type)

        if country_code != "ES":
            sheet.write("G" + str(row), country_code)
        sheet.write("H" + str(row), vat_number)

        if not vat_number and (
                line.partner_id.aeat_anonymous_cash_customer or not line.partner_id
        ):
            sheet.write("I" + str(row), "Venta anónima")
        else:
            sheet.write("I" + str(row), (line.partner_id.name or "")[:40])

        # TODO: Sustituir factura
        # sheet.write('J' + str(row), line.invoice_id.refund_invoice_id.number or '')

        sheet.write("K" + str(row), "")  # Clave de operación

        if with_total:
            sheet.write("L" + str(row), line.total_amount)

        sheet.write("M" + str(row), tax_line.base_amount)
        sheet.write("N" + str(row), tax_line.tax_id.amount)
        sheet.write("O" + str(row), tax_line.tax_amount)

        if tax_line.special_tax_id:
            map_vals = line.vat_book_id.get_special_taxes_dic()[
                tax_line.special_tax_id.id
            ]
            sheet.write(
                map_vals["fee_type_xlsx_column"] + str(row),
                tax_line.special_tax_id.amount,
            )
            sheet.write(
                map_vals["fee_amount_xlsx_column"] + str(row),
                tax_line.special_tax_amount,
            )

        if draft_export:
            last_column = sheet.dim_colmax
            num_row = row - 1
            sheet.write(num_row, last_column, tax_line.tax_id.name)
