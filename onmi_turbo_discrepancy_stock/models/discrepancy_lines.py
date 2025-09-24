from odoo import fields, models, api


class DiscrepancyLineas(models.Model):
    _name = 'discrepancy.lines'
    _description = 'Description'

    product_id = fields.Many2one('product.product')
    qty = fields.Float('Qty')

    order_line = fields.Many2one('sale.order.line')
    order_id = fields.Many2one('sale.order')
    order_ids = fields.Many2many('sale.order')
