import base64
from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class StockRule(models.Model):
    _inherit = "stock.rule"

    sale_line_id = fields.Many2one('sale.order.line', string="Origin Sale Order Line")

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):

        move_values = super()._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin,
                                                     company_id, values)

        descrip = self.env['sale.order.line'].browse([values['sale_line_id']])
        picking_description = descrip.name
        move_values['description_picking'] = picking_description
        for field in self._get_custom_move_fields():
            if field in values:
                move_values[field] = values.get(field)
        return move_values
