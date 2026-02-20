from odoo import fields, models, api


class ModelName(models.Model):
    _inherit = 'stock.move.line'
    waste_qty = fields.Float('Waste qty', compute='compute_waste_qty', store=False)

    def compute_waste_qty(self):
        for rec in self:
            rec.waste_qty = 0.0
            weighing = self.env['weighing'].search([('move_line_id', '=', rec.move_id.id)])
            if weighing:
                rec.waste_qty = weighing.waste

    def _get_aggregated_product_quantities(self, **kwargs):
        """
        Inherit _get_aggregated_product_quantities in order to include values from stock picking report valued
        """
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            # En Odoo 18, 'qty_done' puede haberse cambiado, verificamos su existencia
            quantity = aggregated_move_lines[aggregated_move_line].get('qty_done', 0.0)
            # Si 'qty_done' no existe, intentamos con 'quantity'
            if quantity == 0.0:
                quantity = aggregated_move_lines[aggregated_move_line].get('quantity', 0.0)
                # Aseguramos compatibilidad añadiendo 'qty_done' si no existe
                if quantity > 0.0:
                    aggregated_move_lines[aggregated_move_line]['qty_done'] = quantity

            # Buscamos el move_line usando la cantidad obtenida
            move_line = self.env['stock.move.line'].search([
                ('product_id', '=', aggregated_move_lines[aggregated_move_line]['product'].id),
                ('picking_id', '=', self.picking_id.id),
                ('qty_done', '=', quantity)
            ], limit=1)

            if move_line:
                aggregated_move_lines[aggregated_move_line]['waste_qty'] = str(move_line.waste_qty) + ' kg'
            else:
                aggregated_move_lines[aggregated_move_line]['waste_qty'] = ''

        return aggregated_move_lines