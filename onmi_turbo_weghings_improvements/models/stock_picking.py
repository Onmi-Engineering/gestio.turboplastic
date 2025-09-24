from datetime import timedelta, datetime, date
import calendar
from odoo import fields, models, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    date_planned = fields.Datetime(
        string='Date final weight', index=True, copy=False, store=True, readonly=False)

    def _get_report_language(self):
        """
        Devuelve el idioma del informe basado en el partner o el idioma del usuario
        """
        lang = False
        if self.partner_id:
            lang = self.partner_id.lang
        if not lang:
            lang = self.env.user.lang
        if not lang:
            lang = 'es_ES'  # Idioma por defecto
        return lang

    def _compute_totals(self):
        # Eliminamos la llamada a super para evitar conflictos
        # super(StockPicking, self)._compute_totals()

        for rec in self:
            rec.total_ordered = 0.0
            rec.total_delivered = 0.0
            rec.total_wasted = 0.0
            for line in rec.move_ids_without_package:
                rec.total_ordered += line.product_uom_qty

                # En Odoo 18, parece que quantity_done ya no existe en stock.move
                # Obtenemos la cantidad hecha de las líneas de movimiento asociadas
                move_lines = self.env['stock.move.line'].search([
                    ('move_id', '=', line.id)
                ])
                qty_done = sum(move_line.qty_done for move_line in move_lines) if move_lines else 0.0
                rec.total_delivered += qty_done

            for w in rec.weighing_ids:
                rec.total_wasted += w.waste
                rec.total_ordered += w.waste

    def action_confirm_weighings(self):
        super(StockPicking, self).action_confirm_weighings()
        self.date_planned = datetime.now()

    def action_reset_weighings(self):
        super(StockPicking, self).action_reset_weighings()
        self.date_planned = False

    def change_descriptions(self):
        active_ids = self.env.context.get('active_ids', [])
        picking = self.env['stock.picking'].browse(active_ids)
        for rec in picking:
            # Cambiado de rec.move_lines a rec.move_ids_without_package
            for pic in rec.move_ids_without_package:
                for sale in rec.sale_id.order_line:
                    if pic.sale_line_id == sale:
                        pic.description_picking = sale.name