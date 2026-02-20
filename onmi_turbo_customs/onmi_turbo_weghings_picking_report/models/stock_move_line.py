from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'


    weighing_id = fields.Many2one('weighing', compute='_compute_weighing_id', store=True)


    def _compute_weighing_id(self):
        for rec in self:
            if rec.move_id.weighing_id:
                rec.weighing_id = rec.move_id.weighing_id
            else:
                rec.weighing_id = False


# def _get_aggregated_product_quantities(self, **kwargs):
#     """
#     Inherit _get_aggregated_product_quantities in order to include values from stock picking report valued
#     """
#     aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
#     for aggregated_move_line in aggregated_move_lines:
#         aggregated_move_lines[aggregated_move_line]['first_weight'] = 0.0
#         aggregated_move_lines[aggregated_move_line]['second_weight'] = 0.0
#
#         # En Odoo 18, 'qty_done' puede haberse cambiado, verificamos su existencia
#         quantity = aggregated_move_lines[aggregated_move_line].get('qty_done', 0.0)
#         # Si 'qty_done' no existe, intentamos con 'quantity'
#         if quantity == 0.0:
#             quantity = aggregated_move_lines[aggregated_move_line].get('quantity', 0.0)
#             # Aseguramos compatibilidad añadiendo 'qty_done' si no existe
#             if quantity > 0.0:
#                 aggregated_move_lines[aggregated_move_line]['qty_done'] = quantity
#
#         move_line = self.env['stock.move.line'].search([
#             ('product_id', '=', aggregated_move_lines[aggregated_move_line]['product'].id),
#             ('picking_id', '=', self.picking_id.id),
#             ('qty_done', '=', quantity)
#         ], limit=1)
#
#         if move_line:
#             first_weight = move_line.move_id.weighing_id.first_weight
#             aggregated_move_lines[aggregated_move_line]['first_weight'] = first_weight
#             second_weight = move_line.move_id.weighing_id.second_weight
#             aggregated_move_lines[aggregated_move_line]['second_weight'] = second_weight
#
#     return aggregated_move_lines
    def _get_aggregated_product_quantities(self, **kwargs):
        """
        Inherit _get_aggregated_product_quantities in order to include values from stock picking report valued
        """
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            aggregated_move_lines[aggregated_move_line]['first_weight'] = 0.0
            aggregated_move_lines[aggregated_move_line]['second_weight'] = 0.0

            # En Odoo 18, 'qty_done' puede haberse cambiado, verificamos su existencia
            quantity = aggregated_move_lines[aggregated_move_line].get('qty_done', 0.0)
            # Si 'qty_done' no existe, intentamos con 'quantity'
            if quantity == 0.0:
                quantity = aggregated_move_lines[aggregated_move_line].get('quantity', 0.0)
                # Aseguramos compatibilidad añadiendo 'qty_done' si no existe
                if quantity > 0.0:
                    aggregated_move_lines[aggregated_move_line]['qty_done'] = quantity

            # Buscar todas las líneas que coincidan con el producto y el albarán
            move_lines = self.env['stock.move.line'].search([
                ('product_id', '=', aggregated_move_lines[aggregated_move_line]['product'].id),
                ('picking_id', '=', self.picking_id.id)
            ])

            if move_lines:
                for move_line in move_lines:
                    weighing = move_line.weighing_id or move_line.move_id.weighing_id
                    if weighing:
                        aggregated_move_lines[aggregated_move_line]['first_weight'] = weighing.first_weight
                        aggregated_move_lines[aggregated_move_line]['second_weight'] = weighing.second_weight
                        break
                if aggregated_move_lines[aggregated_move_line]['first_weight'] == 0.0 and move_lines:
                    weighing = move_lines[0].weighing_id or move_lines[0].move_id.weighing_id
                    if weighing:
                        aggregated_move_lines[aggregated_move_line]['first_weight'] = weighing.first_weight
                        aggregated_move_lines[aggregated_move_line]['second_weight'] = weighing.second_weight

        return aggregated_move_lines
