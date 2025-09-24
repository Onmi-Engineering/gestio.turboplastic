from odoo import fields, models, api


class DiscrepancyLinesPurchase(models.Model):
    _name = 'discrepancy.lines.purchase'
    _description = 'Discrepancy lines Purchase'

    product_id = fields.Many2one('product.product')

    qty = fields.Float('Qty')

    purchase_line = fields.Many2one('purchase.order.line')

    order_id = fields.Many2one('purchase.order')
