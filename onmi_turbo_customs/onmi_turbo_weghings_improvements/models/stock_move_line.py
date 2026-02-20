import base64
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_done = fields.Float('Done', default=0.0,
                            digits='Product Unit of Measure', copy=False)
    weighing_id = fields.Many2one(
        'weighing', compute='_compute_weighing_id', store=True)

    def _compute_weighing_id(self):
        for rec in self:
            weighing_related = self.env['weighing'].search(
                [('move_line_id.id', '=', rec.id)])
            if weighing_related:
                for w in weighing_related:
                    rec.weighing_id = w
            else:
                rec.weighing_id = False

    def _get_aggregated_product_quantities(self, **kwargs):
        """
        Inherit _get_aggregated_product_quantities in order to include values from stock picking report valued
        """
        aggregated_move_lines = super()._get_aggregated_product_quantities(**kwargs)
        for aggregated_move_line in aggregated_move_lines:
            # Aseguramos que 'code_led' existe en el diccionario
            if 'code_led' not in aggregated_move_lines[aggregated_move_line]:
                aggregated_move_lines[aggregated_move_line]['code_led'] = ''

            for rec in self:
                weighing_line = self.env['weighing'].search([
                    ('product_id', '=',
                     aggregated_move_lines[aggregated_move_line]['product'].id),
                    ('picking_id', '=', self.picking_id.id)
                ])
                code_ler = ''
                if weighing_line:
                    for we in weighing_line:
                        if we.code_led:
                            code_ler += we.code_led + "\n"
                            aggregated_move_lines[aggregated_move_line]['code_led'] = code_ler
                        if we.code_led == False:
                            aggregated_move_lines[aggregated_move_line]['code_led'] = ''

        return aggregated_move_lines